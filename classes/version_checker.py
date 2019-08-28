import requests
import threading
from classes.app import get_app
from classes import constants
from classes.logger import log


def get_current_version():
    """Возвращает текущую версию приложения"""
    t = threading.Thread(target=_get_version_from_http)
    t.start()


def _get_version_from_http():
    """Проверяет текущую версию приложения на сайте"""

    url = "http://coa.tre.one/version/json/"

    try:
        r = requests.get(url, headers={"user-agent": "%s-%s" % (constants.APP_NAME_WITHOUT_SPACES,
                                                                constants.VERSION)}, verify=False)
        log.info("На сайте обнаружена версия приложения: %s" % r.text)
        app_version = r.json()["app_version"]
        get_app().window.FoundVersionSignal.emit(app_version)
    except:
        log.error("Не удалось получить данные о версии из: %s" % url)
