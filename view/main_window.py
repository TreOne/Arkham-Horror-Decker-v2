from PyQt5.QtCore import QSize, QPoint, QFile, QTextStream, Qt, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from utility.helper_function import get_icon
from utility.variables import settings, APP_NAME
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
        self.load_size_and_position()
        self.set_current_file('')

    def load_size_and_position(self):
        """Загрузка настроек размера и положения окна"""
        size = settings.value("Size", QSize(400, 400))
        position = settings.value("Position", QPoint(200, 200))
        self.resize(size)
        self.move(position)

    def save_size_and_position(self):
        """Сохранение настроек размера и положения окна"""
        settings.setValue("Position", self.pos())
        settings.setValue("Size", self.size())

    def closeEvent(self, event):
        if self.maybe_save():
            self.save_size_and_position()
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        is_modified = True
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

        self.setWindowTitle("%s[*] - %s" % (shown_name, APP_NAME))

    def stripped_name(self, full_file_name):
        return QFileInfo(full_file_name).fileName()
