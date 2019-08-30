import os
import sys
import locale
import platform
import traceback
from PyQt5.QtCore import QTranslator, QSettings, pyqtSlot, Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMessageBox, QStyleFactory
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR

from classes import project

try:
    # Включить High-DPI разрешение
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
except AttributeError:
    pass  # Заглушка для старых Qt5 версий


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
            self.__start_time = time.time()  # Время начала инициализации
            log.info("------------------------------------------------")
            locale.setlocale(locale.LC_ALL, '')
            log.info(time.strftime("%d %B %Y %H:%M:%S", time.localtime()).center(48))  # Пример: 26 Август 2019 16:14:04
            log.info('Запуск новой сессии'.center(48))

            from classes import symbols, ui_util

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
        App.symbol = symbols.Symbol()

        # Инициализируемловца необработанных исключений
        from classes import exceptions
        sys.excepthook = exceptions.exception_handler

        # Подключаем обьект для хранения данных текущего
        self.project = project.ProjectDataStore()

        # Загрузить пользовательскую тему, если тема не задана ОС
        ui_util.load_theme()

        # Установить шрифт для всех тем
        if self.settings.value("Theme") != "No Theme":
            # Загрузить встроенный шрифт
            try:
                font_path = os.path.join(constants.RESOURCES_PATH, "fonts", "roboto.ttf")
                log.info("Установка шрифта из %s" % font_path)
                font_id = QFontDatabase.addApplicationFont(font_path)
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font = QFont(font_family)
                font.setPointSizeF(10.5)
                QApplication.setFont(font)
            except Exception as ex:
                log.error("Ошибка установки шрифта roboto.ttf: %s" % str(ex))

        # Загрузка кастомных шрифтов
        try:
            medieval_font_path = os.path.join(constants.RESOURCES_PATH, "fonts", "medieval.ttf")
            log.info("Установка шрифта из %s" % medieval_font_path)
            medieval_font_id = QFontDatabase.addApplicationFont(medieval_font_path)
            medieval_font_family = QFontDatabase.applicationFontFamilies(medieval_font_id)[0]
            medieval_font = QFont(medieval_font_family)
            medieval_font.setPointSizeF(10.5)
            self.settings.setValue("Medieval Font", medieval_font)
        except Exception as ex:
            log.error("Ошибка установки шрифта medieval.ttf: %s" % str(ex))

        # Установить темную тему (экспериментальная опция)
        if self.settings.value("theme") == ui_util.DEFAULT_THEME_NAME + ": Dark":
            log.info("Установка тёмной темы")
            self.setStyle(QStyleFactory.create("Fusion"))

            dark_palette = self.palette()

            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.Light, QColor(68, 68, 68))
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218, 192))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(104, 104, 104))

            # Disabled palette
            dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(255, 255, 255, 128))
            dark_palette.setColor(QPalette.Disabled, QPalette.Base, QColor(68, 68, 68))
            dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(255, 255, 255, 128))
            dark_palette.setColor(QPalette.Disabled, QPalette.Button, QColor(53, 53, 53, 128))
            dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(255, 255, 255, 128))
            dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(151, 151, 151, 192))
            dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, Qt.black)

            # Tooltips
            dark_palette.setColor(QPalette.ToolTipBase, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)

            self.setPalette(dark_palette)
            self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 0px solid white; }")

        # Руссификация интерфейса QT
        ru_qtbase_path = os.path.join(constants.RESOURCES_PATH, "qtbase_ru.qm")
        log.info("Установка руссификации интерфейса QT из %s" % ru_qtbase_path)
        translator = QTranslator(self)
        translator.load(ru_qtbase_path)
        self.installTranslator(translator)

        # Создаем главное окно приложения
        from view.main_window import MainWindow
        MainWindow()

        log.info("------------------------------------------------")
        log.info("Инициализация приложения завершена".center(48))
        elapsed_time = time.time() - self.__start_time
        log.info(("Потребовалось времени: %.3f сек" % elapsed_time).center(48))
        log.info("------------------------------------------------")

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
        # Возвращаем 0 в случае успеха
        return 0

    def run(self):
        """Запуск основного потока QT приложения"""
        res = self.exec_()
        return res
