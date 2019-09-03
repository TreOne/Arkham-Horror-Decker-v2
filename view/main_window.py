import os
import shutil
import webbrowser
from PyQt5.QtCore import Qt, QFileInfo, QByteArray, pyqtSlot, pyqtSignal, QTimer, QTranslator
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QSizePolicy, QWidget, QToolButton
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
    open_project_signal = pyqtSignal(str)
    recover_backup_signal = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        app_rc.qInitResources()

        # Руссифицируем QT диалоги
        log.info("Установка руссификации интерфейса QT")
        qt_base_translator = QTranslator(app)
        if qt_base_translator.load(":/i18n/qtbase_ru.qm"):
            app.installTranslator(qt_base_translator)
        else:
            log.error("Ошибка при установке руссификации интерфейса QT.")

        # Устанавливаем главное окно для ссылки на него во время инициализации потомков
        app.window = self

        self.recent_menu = None

        ui_util.load_ui(self, 'main_window')
        ui_util.init_ui(self)

        # Получить данные о текущей версии приложения через HTTP
        self.found_version_signal.connect(self.found_current_version)
        get_current_version()

        self.recover_backup_signal.connect(self.recover_backup)

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

        # Подключаем сигнал open_project_signal
        self.open_project_signal.connect(self.open_project)

        # self.set_current_file('')
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
            self.action_update_app.setToolTip("Ваша версия: <b>{}</b><br>"
                                              "Доступна: <b>{}</b>".format(constants.VERSION, new_version))

            # Добавить кнопку Обновление доступно (с иконкой и текстом)
            update_button = QToolButton()
            update_button.setDefaultAction(self.action_update_app)
            update_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.toolbar.addWidget(update_button)

    def closeEvent(self, event):
        # Предложить пользователю сохранить проект (при необходимости)
        if app.project.needs_save():
            log.info("Предлагаем пользователю сохранить проект перед закрытием приложения")
            ret = QMessageBox.question(self, "Сохранить проект?",
                                       'Сохранить изменения в проекте "{}"?'.format(app.project.get("title")),
                                       QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.action_save_trigger(event)
                if app.project.needs_save():
                    log.info("Процесс сохранения был отменен. Не закрываем окно приложения!")
                    event.ignore()
                    return
            elif ret == QMessageBox.Cancel:
                log.info("Пользователь отменил закрытие приложения")
                event.ignore()
                return
            elif ret == QMessageBox.No:
                log.info("Пользователь отказался сохранять проект")

        log.info("------------------ Выключение ------------------")
        self.save_window_settings()
        app.processEvents()
        event.accept()

    def recover_backup(self):
        """Восстановление файла резервной копии (если есть)"""
        log.info("Проверка наличия резервной копии проекта")
        # Проверяем существование файла backup
        recovery_path = os.path.join(constants.BACKUP_PATH, "backup.json")

        if os.path.exists(recovery_path):
            log.info("Восстанавливаем проект из резервной копии: %s" % recovery_path)
            self.open_project(recovery_path, clear_images=False)

            # Очистите путь к файлу (который устанавливается при сохранения проекта)
            app.project.has_unsaved_changes = True
            self.set_current_file(None)

            # Отображаем сообщение для пользователя
            QMessageBox.information(self, "Резервная копия восстановлена", "Ваш последний проект был восстановлен.")

        else:
            # Резервных копий не найдено
            # Загружаем пустой проект (для установки настроек по умолчанию)
            app.project.load("")
            self.set_current_file(None)

    def open_project(self, file_path, clear_images=True):
        """Открывает проект из file_path"""
        # Сначала проверяем путь к файлу (возможно, пользователь отменил выбор пути)
        if not file_path:
            return

        # У нас есть несохраненные изменения?
        if app.project.needs_save():
            log.info("Предлагаем пользователю сохранить проект перед открытием нового проекта")
            ret = QMessageBox.question(self, "Сохранить проект?",
                                       'Сохранить изменения в проекте "{}"?'.format(app.project.get("title")),
                                       QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.action_save.trigger()
                if app.project.needs_save():
                    log.info("Процесс сохранения был отменен. Не продолжаем действие!")
                    return
            elif ret == QMessageBox.Cancel:
                log.info("Пользователь отменил создание нового проекта")
                return
            elif ret == QMessageBox.No:
                log.info("Пользователь отказался сохранять проект")

        # Устанавливаем курсор в режим ожидания
        app.setOverrideCursor(QCursor(Qt.WaitCursor))

        try:
            if os.path.exists(file_path):
                if clear_images:
                    self.clear_all_images()

                app.project.load(file_path, clear_images)
                self.set_current_file(file_path)

                # Загружаем последние проекты
                self.load_recent_menu()

                log.info("Загружен проект {}".format(file_path))
            else:
                log.info("Проект не обнаружен {}".format(file_path))
                self.statusBar().showMessage("Проект {} отсутствует "
                                             "(возможно, он был перемещен или удален).".format(file_path), 5000)
                self.remove_recent_project(file_path)
                self.load_recent_menu()

        except Exception as ex:
            log.error("Ошибка при открытии проекта {}".format(file_path))
            QMessageBox.warning(self, "Ошибка при открытии проекта!", str(ex))

        # Востанавливаем вид курсора
        app.restoreOverrideCursor()

    def action_new_trigger(self, event):
        # У нас есть несохраненные изменения?
        if app.project.needs_save():
            log.info("Предлагаем пользователю сохранить проект перед созданием нового проекта.")
            ret = QMessageBox.question(self, "Сохранить проект?",
                                       'Сохранить изменения в проекте "{}"?'.format(app.project.get("title")),
                                       QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.action_save.trigger()
                if app.project.needs_save():
                    log.info("Процесс сохранения был отменен. Не продолжаем действие!")
                    return
            elif ret == QMessageBox.Cancel:
                log.info("Пользователь отменил создание нового проекта")
                return
            elif ret == QMessageBox.No:
                log.info("Пользователь отказался сохранять проект")

        self.clear_all_images()

        # Очистить данные
        app.project.load("")
        self.set_current_file(None)

        log.info("Создан новый проект")

    def action_open_trigger(self, event):
        recommended_path = app.project.current_filepath
        if not recommended_path:
            recommended_path = constants.HOME_PATH

        # У нас есть несохраненные изменения?
        if get_app().project.needs_save():
            log.info("Предлагаем пользователю сохранить проект перед открытием другого проекта")
            ret = QMessageBox.question(self, "Сохранить проект?",
                                       'Сохранить изменения в проекте "{}"?'.format(app.project.get("title")),
                                       QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.action_save_trigger(event)
                if app.project.needs_save():
                    log.info("Процесс сохранения был отменен. Не продолжаем действие!")
                    return
            elif ret == QMessageBox.Cancel:
                log.info("Пользователь отменил открытие другого проекта")
                return
            elif ret == QMessageBox.No:
                log.info("Пользователь отказался сохранять проект")

        # Запускаем диалоговое окно
        file_path, file_type = QFileDialog.getOpenFileName(self, "Открыть проект...", recommended_path,
                                                           "{} (*.json)".format(constants.APP_NAME))

        # Загружаем файл проекта
        self.open_project_signal.emit(file_path)

    def clear_all_images(self):
        """Удалить все изображения"""
        try:
            if os.path.exists(constants.IMAGES_PATH):
                log.info("Удаляем все изображения из %s" % constants.IMAGES_PATH)
                shutil.rmtree(constants.IMAGES_PATH, True)
                os.mkdir(constants.IMAGES_PATH)

            backup_path = os.path.join(constants.BACKUP_PATH, "backup.json")
            if os.path.exists(backup_path):
                log.info("Удаляем файлы сохранений: %s" % backup_path)
                os.unlink(backup_path)
        except:
            log.info("Ошибка при очистке папки с изображениями: %s" % constants.IMAGES_PATH)

    def load_recent_menu(self):
        """Очищает и загрузить список последних проектов"""
        # Получаем список последних проектов
        recent_projects = settings.value("recent_projects")

        # Добавить меню последние проекты (после "Открыть")
        import functools
        if not self.recent_menu:
            # Создаем меню "Последние проекты"
            self.recent_menu = self.menu_file.addMenu(QIcon.fromTheme("file-restore-outline"), "Последние проекты")
            self.menu_file.insertMenu(self.action_recent_placeholder, self.recent_menu)
        else:
            # Очищаем содержимое
            self.recent_menu.clear()

        # Наполняем меню последними проектами
        for file_path in reversed(recent_projects):
            new_action = self.recent_menu.addAction(file_path)
            new_action.triggered.connect(functools.partial(self.recent_project_clicked, file_path))

    def remove_recent_project(self, file_path):
        """Удаляет проект из меню "Последние проекты", если приложение не может его найти"""
        recent_projects = settings.value("recent_projects")
        if file_path in recent_projects:
            recent_projects.remove(file_path)
        settings.setValue("recent_projects", recent_projects)

    def recent_project_clicked(self, file_path):
        """Загрузка проекта из меню 'Последние проекты'"""
        self.open_project_signal.emit(file_path)

    def auto_save_project(self):
        """Автосохранение проекта"""
        if app.project.needs_save():
            # Получить current_filepath (если есть)
            file_path = app.project.current_filepath

            if file_path:
                # Сохраняем проект
                log.info("Автосохранение проекта: %s" % file_path)
                self.save_project(file_path)

                # Удаляем backup.json (если есть), так как мы только что сохранили актуальный проект
                recovery_path = os.path.join(constants.BACKUP_PATH, "backup.json")
                if os.path.exists(recovery_path):
                    os.unlink(recovery_path)
            else:
                # Сохраненный проект не найден
                recovery_path = os.path.join(constants.BACKUP_PATH, "backup.json")
                log.info("Сохдаем резервную копию проекта: %s" % recovery_path)
                # TODO: Проверить: Надо ли использовать make_paths_relative=False или True. Есть подозрение, что True
                app.project.save(recovery_path, move_temp_files=False, make_paths_relative=False)

                # Очистите current_filepath (который устанавливается путем сохранения проекта)
                app.project.current_filepath = None
                app.project.has_unsaved_changes = True

    def action_save_trigger(self, event):
        # Использовать current_filepath, если имеется, в противном случае спросить пользователя
        file_path = app.project.current_filepath
        if not file_path:
            recommended_filename = app.project.get("title") + ".json"
            recommended_path = os.path.join(constants.HOME_PATH, recommended_filename)
            file_path, file_type = QFileDialog.getSaveFileName(self, "Сохранить проект...",
                                                               recommended_path,
                                                               "{} (*.json)".format(constants.APP_NAME))

        if file_path:
            # Сохраняем проект
            self.save_project(file_path)

    def save_project(self, file_path):
        """Сохраняет проект по указанному пути"""
        # Добавляем расширение файла если надо
        if not file_path.endswith(".json"):
            file_path = file_path + ".json"
        try:
            # Сохраняем проект по указанному пути
            app.project.save(file_path)

            # Обновить заголовок окна и состояние кнопок созхранения
            self.set_current_file(file_path)

            # Обновляем список последних проектов
            self.load_recent_menu()

            log.info("Проект сохранен {}".format(file_path))
            self.statusBar().showMessage("Файл сохранен", 2000)

        except Exception as ex:
            log.error("Не удалось сохранить проект %s. %s" % (file_path, str(ex)))
            QMessageBox.warning(self, "Ошибка при сохранении проекта", str(ex))

    def set_current_file(self, file_path):
        app.project.current_filepath = file_path

        need_save = app.project.needs_save()
        self.setWindowModified(need_save)
        self.action_save.setEnabled(need_save)
        self.action_save_as.setEnabled(need_save)

        if app.project.current_filepath:
            shown_name = QFileInfo(app.project.current_filepath).fileName()
        else:
            shown_name = app.project.get("title")
        self.setWindowTitle("%s[*]" % shown_name)

    def action_update_app_trigger(self, event):
        download_url = constants.APP_SITE + "/download"
        try:
            webbrowser.open(download_url)
            log.info("Успешно открыта страница скачивания новой версии")
        except:
            QMessageBox.warning(self, "Ошибка!", "Не удается открыть страницу загрузки обновления!<br>"
                                                 "Попробуйте сделать это вручную:<br>"
                                                 "<a href='{url}'>{url}</a>".format(url=download_url))

    def restore_window_settings(self):
        """Загрузка настроек размера и положения окна"""
        log.info("Загружаем настройки главного окна")
        self.restoreGeometry(app.settings.value("Geometry", QByteArray()))
        self.restoreState(app.settings.value("Window State", QByteArray()))

        # Устанавливаем флаги в меню в соответствии с состояниями элементов
        self.action_view_toolbar.setChecked(self.toolbar.isVisibleTo(self))
        self.action_fullscreen.setChecked(self.isFullScreen())

    def save_window_settings(self):
        """Сохранение настроек размера и положения окна"""
        log.info("Сохраняем настройки главного окна")
        app.settings.setValue("Geometry", self.saveGeometry())
        app.settings.setValue("Window State", self.saveState())

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
