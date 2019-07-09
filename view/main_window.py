from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from view.ui.main_window_ui import Ui_MainWindow
from utility.resource_path import resource_path


class MainWindow(QMainWindow):
    """
    Класс MainWindow отвечает за визуальное представление главного окна.
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path('resources/icons/app.svg')))
