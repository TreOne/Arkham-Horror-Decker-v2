import sys
import os
from PyQt5.QtGui import QIcon


def resource_path(relative):
    """
    Помощник для поиска путей файлов.
    После компиляции программы в .exe , ресурсные файлы хранятся во временной папке.
    Для того, чтобы использовать одни пути при разработке и при запуске программы в .exe используется эта функция.
    Например, для подключения файла 'resources/qtbase_ru.qm' используйте:
        filename = resource_path('resources/qtbase_ru.qm')
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def get_icon(name):
    return QIcon(resource_path('resources/icons/' + name))
