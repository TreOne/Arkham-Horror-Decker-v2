from PyQt5.QtWidgets import QDialog
from classes import ui_util


class OpenUrlDialog(QDialog):
    """Окно 'Открыть ссылку'"""
    def __init__(self):
        QDialog.__init__(self)

        ui_util.load_ui(self, 'open_url')
        ui_util.init_ui(self)