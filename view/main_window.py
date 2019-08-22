from PyQt5.QtWidgets import QMainWindow

from utility.helper_function import get_icon
from view.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Класс MainWindow отвечает за визуальное представление главного окна.
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon('app.svg'))
