from PyQt5.QtCore import QSettings, QTranslator

from utility.constants import AUTHOR, APP_NAME
from utility.helper_function import resource_path


class AppPreparer:
    """
    Класс подготовки главного окна к запуску.
    """
    def __init__(self):
        self.app = None
        self.app_settings = QSettings(AUTHOR, APP_NAME)

    def prepare_app(self, app):
        """Подготовить приложение"""
        self.app = app
        self._apply_theme()
        self._translate()

    def _apply_theme(self):
        """Внешний вид приложения"""
        theme_style = self.app_settings.value("Theme Style", 'Fusion')
        if theme_style == 'Fusion':
            self.app.setStyle('Fusion')

    def _translate(self):
        """Руссификация интерфейса QT"""
        translator = QTranslator(self.app)
        translator.load(resource_path('resources/qtbase_ru.qm'))
        self.app.installTranslator(translator)
