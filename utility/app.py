from PyQt5.QtCore import QTranslator, QSettings
from PyQt5.QtWidgets import QApplication
from utility.helper_function import resource_path
from utility.variables import APP_NAME, AUTHOR, VERSION, APP_NAME_RUS


class App(QApplication):
    """
    Класс подготовки главного окна к запуску.
    """
    settings = None

    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName(APP_NAME)
        self.setApplicationDisplayName(APP_NAME_RUS)
        self.setOrganizationName(AUTHOR)
        self.setApplicationVersion(VERSION)
        App.settings = QSettings()

        self._apply_theme()
        self._translate()

    def _apply_theme(self):
        """Внешний вид приложения"""
        theme_style = self.settings.value("Theme Style", 'Fusion')
        if theme_style == 'Fusion':
            self.setStyle('Fusion')

    def _translate(self):
        """Руссификация интерфейса QT"""
        translator = QTranslator(self)
        translator.load(resource_path('resources/qtbase_ru.qm'))
        self.installTranslator(translator)
