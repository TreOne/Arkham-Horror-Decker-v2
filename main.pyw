import sys
from utility.resource_path import resource_path
from PyQt5.QtCore import QTranslator, QSettings
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow


def prepare_app(app_var):
    app_settings = QSettings("TreOne", "Arkham Horror Decker")

    # Внешний вид приложения
    theme_style = app_settings.value("Theme Style", 'Fusion')
    if theme_style == 'Fusion':
        app_var.setStyle('Fusion')

    # Руссификация интерфейса QT
    translator = QTranslator(app_var)
    translator.load(resource_path('resources/qtbase_ru.qm'))
    app_var.installTranslator(translator)


if __name__ == '__main__':
    # Запуск основного потока
    app = QApplication(sys.argv)
    prepare_app(app)
    main_window = MainWindow()
    # main_window.showMaximized()
    main_window.show()
    sys.exit(app.exec_())
