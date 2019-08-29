import os
import webbrowser

from PyQt5.QtCore import QFile, QTextStream, Qt, QFileInfo, QByteArray, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, QSizePolicy, QWidget, QToolButton
from classes import ui_util, constants
from classes.app import get_app, get_settings
from classes.logger import log
from classes.version import get_current_version
from resources import app_rc

app = get_app()
settings = get_settings()


class MainWindow(QMainWindow):
    """Главное окно"""

    found_version_signal = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        app_rc.qInitResources()
        self.current_file = ''
        self.recent_menu = None

        # Устанавливаем главное окно для ссылки на него во время инициализации потомков
        app.window = self

        ui_util.load_ui(self, 'main_window')
        ui_util.init_ui(self)

        # Получить данные о текущей версии приложения через HTTP
        self.found_version_signal.connect(self.found_current_version)
        get_current_version()

        self.not_fullscreen_window_state = Qt.WindowNoState
        self.restore_window_settings()

        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        # QTimer для Автосохранений
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.setInterval(settings.value("autosave-interval", 5) * 1000 * 60)
        self.auto_save_timer.timeout.connect(self.auto_save_project)
        if settings.value("enable-auto-save", True):
            self.auto_save_timer.start()

        self.set_current_file('')
        self.show()

    @pyqtSlot(str)
    def found_current_version(self, new_version):
        """Обработка полученного ответа о текущей версии приложения на сайте"""
        log.info('Текущая версия приложения:  %s (На сайте: %s)' % (constants.VERSION, new_version))

        # Сравнение версий (алфавитное сравнение строк версий должно работать нормально)
        if constants.VERSION < new_version:
            # Добавить разделитель и кнопку "Новая версия доступна" на панели инструментов (по умолчанию скрыта)
            spacer = QWidget(self)
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.toolbar.addWidget(spacer)

            # Установить текст для QAction
            self.action_update_app.setVisible(True)
            self.action_update_app.setText("Доступно обновление")
            self.action_update_app.setToolTip("Доступно обновление: <b>%s</b>" % new_version)

            # Добавить кнопку Обновление доступно (с иконкой и текстом)
            update_button = QToolButton()
            update_button.setDefaultAction(self.action_update_app)
            update_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.toolbar.addWidget(update_button)

    def action_update_app_trigger(self, event):
        download_url = constants.APP_SITE + "/download"
        try:
            webbrowser.open(download_url)
            log.info("Успешно открыта страница скачивания новой версии")
        except:
            QMessageBox.warning(self, "Ошибка!", "Не удается открыть страницу загрузки обновления!<br>"
                                                 "Попробуйте сделать это вручную:<br>"
                                                 "<a href='{url}'>{url}</a>" .format(url=download_url))

    def restore_window_settings(self):
        """Загрузка настроек размера и положения окна"""
        self.restoreGeometry(app.settings.value("Geometry", QByteArray()))
        self.restoreState(app.settings.value("Window State", QByteArray()))

        # Устанавливаем флаги в меню в соответствии с состояниями элементов
        self.action_view_toolbar.setChecked(self.toolbar.isVisibleTo(self))
        self.action_fullscreen.setChecked(self.isFullScreen())

    def save_window_settings(self):
        """Сохранение настроек размера и положения окна"""
        app.settings.setValue("Geometry", self.saveGeometry())
        app.settings.setValue("Window State", self.saveState())

    def auto_save_project(self):
        """Автосохранение проекта"""
        # TODO: Доделать метод
        # Get current filepath (if any)
        file_path = get_app().project.current_filepath
        if get_app().project.needs_save():
            log.info("auto_save_project")

            if file_path:
                # A Real project file exists
                # Append .osp if needed
                if ".osp" not in file_path:
                    file_path = "%s.osp" % file_path

                # Save project
                log.info("Auto save project file: %s" % file_path)
                self.save_project(file_path)

                # Remove backup.osp (if any)
                recovery_path = os.path.join(constants.BACKUP_PATH, "backup.osp")
                if os.path.exists(recovery_path):
                    # Delete backup.osp since we just saved the actual project
                    os.unlink(recovery_path)

            else:
                # No saved project found
                recovery_path = os.path.join(constants.BACKUP_PATH, "backup.osp")
                log.info("Creating backup of project file: %s" % recovery_path)
                get_app().project.save(recovery_path, move_temp_files=False, make_paths_relative=False)

                # Clear the file_path (which is set by saving the project)
                get_app().project.current_filepath = None
                get_app().project.has_unsaved_changes = True

    def closeEvent(self, event):
        log.info('------------------ Выключение ------------------')
        if self.maybe_save():
            self.save_window_settings()
            event.accept()
        else:
            event.ignore()

    def action_fullscreen_trigger(self, event):
        """Переключить режим полного экрана"""
        if not self.isFullScreen():
            # Сохраняем состояние окна, чтобы можно было вернуться к нему
            self.not_fullscreen_window_state = self.windowState()
            self.showFullScreen()
        else:
            self.setWindowState(self.not_fullscreen_window_state)

    def action_about_trigger(self, event):
        """Отобразить диалог О программе"""
        from view.about import About
        win = About()
        win.exec_()

    def maybe_save(self):
        is_modified = False
        if is_modified:
            ret = QMessageBox.warning(self, constants.APP_NAME, "У вас остались несохраненные изменения.\n"
                                                                "Хотите ли вы сохранить измененния?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            if ret == QMessageBox.Cancel:
                return False
        return True

    def save(self):
        if self.current_file:
            return self.save_file(self.current_file)
        return self.save_as()

    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self)
        if file_name:
            return self.save_file(file_name)
        return False

    def save_file(self, file_name):
        file = QFile(file_name)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, constants.APP_NAME,
                                "Запись в файл невозможна %s:\n%s." % (file_name, file.errorString()))
            return False

        out_file = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_file << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.set_current_file(file_name)
        self.statusBar().showMessage("Файл сохранен", 2000)
        return True

    def set_current_file(self, file_name):
        self.current_file = file_name
        self.setWindowModified(False)

        if self.current_file:
            shown_name = self.stripped_name(self.current_file)
        else:
            shown_name = 'untitled.txt'
        self.setWindowTitle("%s[*]" % shown_name)

    def stripped_name(self, full_file_name):
        return QFileInfo(full_file_name).fileName()
