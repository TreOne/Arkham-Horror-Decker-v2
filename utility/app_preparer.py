from PyQt5.QtCore import QTranslator
from utility.helper_function import resource_path
from utility.variables import settings


class AppPreparer:
    """
    Класс подготовки главного окна к запуску.
    """
    def __init__(self):
        self.app = None

    def prepare_app(self, app):
        """Подготовить приложение"""
        self.app = app
        self._apply_theme()
        self._translate()

    def _apply_theme(self):
        """Внешний вид приложения"""
        theme_style = settings.value("Theme Style", 'Fusion')
        if theme_style == 'Fusion':
            self.app.setStyle('Fusion')

    def _translate(self):
        """Руссификация интерфейса QT"""
        translator = QTranslator(self.app)
        translator.load(resource_path('resources/qtbase_ru.qm'))
        self.app.installTranslator(translator)
