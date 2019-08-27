import os

VERSION = "2.1"
APP_NAME = "Arkham Horror Decker"
APP_NAME_ABBR = "AHD"
APP_NAME_RUS = "Карты Аркхэма"
DESCRIPTION = "Помощник по созданеию колод"
AUTHOR = "TreOne"
COPYRIGHT = "Copyright (c) 2008-2018 %s" % AUTHOR

APP_NAME_WITHOUT_SPACES = APP_NAME.lower().replace(" ", "-")
CWD = os.getcwd()
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Каталог приложения
HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, f".{APP_NAME_WITHOUT_SPACES}")

RESOURCES_PATH = os.path.join(PATH, "resources")

# Создаем пути, если они не существуют
for folder in [USER_PATH, RESOURCES_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder, exist_ok=True)
