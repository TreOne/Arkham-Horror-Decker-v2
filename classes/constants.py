import os
from datetime import datetime

VERSION = "2.1"
APP_NAME = "Cards of Arkham"
APP_NAME_ABBR = "COA"
APP_NAME_RUS = "Карты Аркхэма"
DESCRIPTION = "Помощник по изучению колод"
AUTHOR = "TreOne"
AUTHOR_EMAIL = "tre@tre.one"
COPYRIGHT = "Все права защищены. (c) 2018-%s %s" % (datetime.now().year, AUTHOR)

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
