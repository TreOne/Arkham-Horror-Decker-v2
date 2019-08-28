from PyQt5.QtCore import QFile, QTextStream, Qt, QFileInfo, QByteArray, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from classes import ui_util
from classes.app import get_app
from classes.constants import APP_NAME
from classes.logger import log
from classes.version_checker import get_current_version
from resources import app_rc

app = get_app()


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

        self.set_current_file('')
        self.show()

    @pyqtSlot(str)
    def found_current_version(self, version):
        """Обработка полученного ответа о текущей версии приложения на сайте"""
        log.info('found_current_version: Обнаружена персия приложения: %s' % version)
        # TODO: Доделать определение версии приложения.

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
            ret = QMessageBox.warning(self, APP_NAME, "У вас остались несохраненные изменения.\n"
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
            QMessageBox.warning(self, APP_NAME, "Запись в файл невозможна %s:\n%s." % (file_name, file.errorString()))
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
