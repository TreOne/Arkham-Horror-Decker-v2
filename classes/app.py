import locale
import platform
import sys
import traceback
from PyQt5 import QtGui
from PyQt5.QtCore import QTranslator, QSettings, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR


def get_app():
    """Возвращает текущий QApplication объект"""
    return QApplication.instance()


def get_settings():
    """Возвращает текущий объект настроек QApplication"""
    return QApplication.instance().settings


class App(QApplication):
    """
    Класс подготовки главного окна к запуску.
    """

    def __init__(self, *args):
        QApplication.__init__(self, *args)

        try:
            # Импорт модулей
            from classes import constants
            from classes.logger import log, reroute_output

            # Отметка начала сессии
            import time
            log.info("------------------------------------------------")
            locale.setlocale(locale.LC_ALL, '')
            log.info(time.strftime("%d %B %Y %H:%M:%S", time.localtime()).center(48))  # Пример: 26 Август 2019 16:14:04
            log.info('Запуск новой сессии'.center(48))

            from classes.helper_function import resource_path
            from classes.symbols import Symbol

            # Перенаправление stdout и stderr в логер
            reroute_output()
        except (ImportError, ModuleNotFoundError) as ex:
            tb = traceback.format_exc()
            QMessageBox.warning(None, "Ошибка импорта модулей",
                                "Модуль: %(name)s\n\n%(tb)s" % {"name": ex.name, "tb": tb})
            # Остановить запуск и выйти
            sys.exit()
        except Exception:
            sys.exit()

        # Запись служебной информации
        try:
            log.info("------------------------------------------------")
            log.info(("%s (version %s)" % (constants.APP_NAME, constants.VERSION)).center(48))
            log.info("------------------------------------------------")

            log.info("Платформа: %s" % platform.platform())
            log.info("Процессор: %s" % platform.processor())
            log.info("Тип: %s" % platform.machine())
            log.info("Python: %s" % platform.python_version())
            log.info("Qt5: %s" % QT_VERSION_STR)
            log.info("PyQt5: %s" % PYQT_VERSION_STR)
        except Exception:
            pass

        # Записываем окончание сессии при получении сигнала от QT
        self.aboutToQuit.connect(self.on_log_the_end)

        # Переменные необходимые для правильной работы приложения
        self.setApplicationName(constants.APP_NAME)
        self.setApplicationDisplayName(constants.APP_NAME_RUS)
        self.setOrganizationName(constants.AUTHOR)
        self.setApplicationVersion(constants.VERSION)

        # Инициализация настроек
        App.settings = QSettings()

        # Инициализация иконок
        App.symbol = Symbol()

        # Инициализируемловца необработанных исключений
        from classes import exceptions
        sys.excepthook = exceptions.exception_handler

        # Создаем главное окно приложения
        from view.main_window import MainWindow
        self.window = MainWindow()

        self._apply_theme()
        self._translate()
        self._load_fonts()

    def _apply_theme(self):
        """Внешний вид приложения"""
        theme_style = self.settings.value("Theme Style", "Fusion")
        if theme_style == "Fusion":
            self.setStyle("Fusion")

    def _translate(self):
        """Руссификация интерфейса QT"""
        from classes.helper_function import resource_path
        translator = QTranslator(self)
        translator.load(resource_path('resources/qtbase_ru.qm'))
        self.installTranslator(translator)

    def _load_fonts(self):
        """Загрузка кастомных шрифтов"""
        from classes.helper_function import resource_path
        # Medieval
        QtGui.QFontDatabase.addApplicationFont(resource_path('resources/fonts/medieval.ttf'))

    @pyqtSlot()
    def on_log_the_end(self):
        """Отметка об окончании основного потока QT"""
        try:
            from classes.logger import log
            import time
            log.info("------------------------------------------------")
            log.info('Сессия окончена'.center(48))
            log.info(time.strftime("%d %B %Y %H:%M:%S", time.localtime()).center(48))  # Пример: 26 Август 2019 16:14:04
            log.info("================================================")
        except Exception:
            pass

        # return 0 on success
        return 0

    def run(self):
        """Запуск основного потока QT приложения"""
        res = self.exec_()
        return res
