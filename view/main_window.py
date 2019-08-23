from PyQt5.QtCore import QSize, QPoint, QFile, QTextStream, Qt, QFileInfo, QByteArray
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, qApp
from utility.app import App
from utility.helper_function import get_icon
from utility.variables import APP_NAME
from view.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Визуальное представление главного окна.
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.current_file = ''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon('app.svg'))
        self.restore_window_settings()
        self.set_current_file('')

    def restore_window_settings(self):
        """Загрузка настроек размера и положения окна"""
        self.restoreGeometry(App.settings.value("Geometry", QByteArray()))
        self.restoreState(App.settings.value("Window State", QByteArray()))

    def save_window_settings(self):
        """Сохранение настроек размера и положения окна"""
        App.settings.setValue("Geometry", self.saveGeometry())
        App.settings.setValue("Window State", self.saveState())

    def closeEvent(self, event):
        if self.maybe_save():
            self.save_window_settings()
            event.accept()
        else:
            event.ignore()

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
