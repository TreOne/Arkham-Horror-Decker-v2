import sys
from utility.resource_path import resource_path
from utility.settings import Settings
from PyQt5.QtCore import QTranslator
from PyQt5 import QtWidgets


def prepare_app(app_var):
    app_settings = Settings()

    # Внешний вид приложения
    theme_style = app_settings.get('appearance', 'theme_style')  # default/fusion
    if theme_style == 'fusion':
        app_var.setStyle('Fusion')

    # Руссификация интерфейса QT
    translator = QTranslator(app_var)
    translator.load(resource_path('resources/qtbase_ru.qm'))
    app_var.installTranslator(translator)


if __name__ == '__main__':
    # Запуск основного потока
    app = QtWidgets.QApplication(sys.argv)
    prepare_app(app)
    # main_window = MWView()
    sys.exit(app.exec_())
