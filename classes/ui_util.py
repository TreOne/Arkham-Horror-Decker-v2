import os
import time
import xml.etree.ElementTree
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from classes.app import get_settings, get_app
from classes.logger import log

DEFAULT_THEME_NAME = "Humanity"


def load_theme():
    """ Load the current OS theme, or fallback to a default one """

    s = get_settings()

    # If theme not reported by OS
    if QIcon.themeName() == '' and not s.value("theme") == "No Theme":

        # Address known Ubuntu bug of not reporting configured theme name, use default ubuntu theme
        if os.getenv('DESKTOP_SESSION') == 'ubuntu':
            QIcon.setThemeName('unity-icon-theme')

        # Windows/Mac use packaged theme
        else:
            QIcon.setThemeName(DEFAULT_THEME_NAME)


def load_ui(window, path):
    """ Load a Qt *.ui file, and also load an XML parsed version """
    # Attempt to load the UI file 5 times
    # This is a hack, and I'm trying to avoid a really common error which might be a
    # race condition. [zipimport.ZipImportError: can't decompress data; zlib not available]
    # This error only happens when cx_Freeze is used, and the app is launched.
    error = None
    for attempt in range(1, 6):
        try:
            # Load ui from configured path
            uic.loadUi(path, window)

            # Successfully loaded UI file, so clear any previously encountered errors
            error = None
            break

        except Exception as ex:
            # Keep track of this error
            error = ex
            time.sleep(0.1)

    # Raise error (if any)
    if error:
        raise error

    # Save xml tree for ui
    window.uiTree = xml.etree.ElementTree.parse(path)


def get_default_icon(theme_name):
    """ Get a QIcon, and fallback to default theme if OS does not support themes. """

    # Default path to backup icons
    start_path = ":/icons/" + DEFAULT_THEME_NAME + "/"
    icon_path = search_dir(start_path, theme_name)
    return QIcon(icon_path), icon_path


def search_dir(base_path, theme_name):
    """ Search for theme name """

    # Search each entry in this directory
    base_dir = QDir(base_path)
    for e in base_dir.entryList():
        # Path to current item
        path = base_dir.path() + "/" + e
        base_filename = e.split('.')[0]

        # If file matches theme name, return
        if base_filename == theme_name:
            return path

        # If this is a directory, search within it
        dir = QDir(path)
        if dir.exists():
            # If found below, return it
            res = search_dir(path, theme_name)
            if res:
                return res

    # If no match found in dir, return None
    return None


def get_icon(theme_name):
    """Get either the current theme icon or fallback to default theme (for custom icons). Returns None if none
    found or empty name."""

    if theme_name:
        has_icon = QIcon.hasThemeIcon(theme_name)
        fallback_icon, fallback_path = get_default_icon(theme_name)
        if has_icon or fallback_icon:
            return QIcon.fromTheme(theme_name, fallback_icon)
    return None


def init_element(window, elem):
    """Инициализировать иконки элемента"""
    name = ''
    if hasattr(elem, 'objectName'):
        name = elem.objectName()
        connect_auto_events(window, elem, name)

    # Установить иконку, если возможно
    if hasattr(elem, 'setIcon') and name != '':  # Есть своя иконка
        setup_icon(window, elem, name)


def setup_icon(window, elem, name, theme_name=None):
    """Используя xml окна, установить значок для данного элемента. Если передано имя темы, загрузить значок из нее"""
    # TODO: Продолжить осмотр этого класса
    type_filter = 'action'
    if isinstance(elem, QWidget):  # Поиск виджета с именем вместо этого
        type_filter = 'widget'
    # Найти набор иконок в дереве (если есть)
    iconset = window.uiTree.find('.//' + type_filter + '[@name="' + name + '"]/property[@name="icon"]/iconset')
    if iconset != None or theme_name:  # For some reason "if iconset:" doesn't work the same as "!= None"
        if not theme_name:
            theme_name = iconset.get('theme', '')
        # Get Icon (either current theme or fallback)
        icon = get_icon(theme_name)
        if icon:
            elem.setIcon(icon)


def connect_auto_events(window, elem, name):
    """Соединить все евенты в *.ui файлах с соответствующими именами методов"""
    # Проверить все слоты
    if hasattr(elem, 'trigger'):
        func_name = name + "_trigger"
        if hasattr(window, func_name) and callable(getattr(window, func_name)):
            func = getattr(window, func_name)
            elem.triggered.connect(func)
    if hasattr(elem, 'click'):
        func_name = name + "_click"
        if hasattr(window, func_name) and callable(getattr(window, func_name)):
            func = getattr(window, func_name)
            elem.clicked.connect(func)


def init_ui(window):
    """Инициализация всех дочерних виджетов и экшенов окна"""
    log.info('Инициализация пользовательского интерфейса для {}'.format(window.objectName()))

    try:
        if hasattr(window, 'setWindowTitle') and window.windowTitle() != "":
            window.setWindowTitle(window.windowTitle())
            # Центрирование окна
            center(window)

        # Обходим все виджеты
        for widget in window.findChildren(QWidget):
            init_element(window, widget)

        # Обходим все экшены
        for action in window.findChildren(QAction):
            init_element(window, action)
    except:
        log.info('Не удалось инициализировать элемент в {}'.format(window.objectName()))


def center(window):
    """Центрирование виджета"""
    frame_gm = window.frameGeometry()
    center_point = get_app().window.frameGeometry().center()
    frame_gm.moveCenter(center_point)
    window.move(frame_gm.topLeft())
