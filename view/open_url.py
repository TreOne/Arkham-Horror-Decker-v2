import json
import re
import requests
from PyQt5.QtWidgets import QDialog
from classes import ui_util
from bs4 import BeautifulSoup, SoupStrainer
import markdown
from classes.app import get_app
from classes.logger import log


class OpenUrlDialog(QDialog):
    """Окно 'Открыть ссылку'"""
    def __init__(self):
        QDialog.__init__(self, parent=get_app().window)
        ui_util.load_ui(self, 'open_url')
        ui_util.init_ui(self)

        self.deck_info = None  # Переменная для хранения информации о загруженной колоде

        # TODO: Демо URL для отладки.
        self.field_url.setText('https://arkhamdb.com/decklist/view/2381')

    def btn_open_url_click(self):
        """Нажата кнопка Открыть"""
        url = self.field_url.text()
        log.info('Загружаем колоду по ссылке: {}'.format(url))
        page_html = requests.get(url, timeout=1).text
        self.get_deck_info_from_html(page_html)
        if self.deck_info is not None:
            log.info('Загружаем информацию о колоде: "{}".'.format(self.deck_info['name']))
            self.close()

    def get_deck_info_from_html(self, page_html):
        """Разбираем полученный HTML"""
        only_script_tags = SoupStrainer("script", type='text/javascript')
        parsed_html = BeautifulSoup(page_html, features="html.parser", parse_only=only_script_tags)
        js_on_page = parsed_html.findAll(only_script_tags)
        self.find_deck_info_in_js_array(js_on_page)

    def find_deck_info_in_js_array(self, js_array):
        log.info('Начинаем перебор {} скриптов для поиска информации о колоде.'.format(len(js_array)))
        for script in js_array:
            if "app.deck.init" in script.text:
                log.info('Найден скрипт с информацией о колоде.')
                deck_info_match = re.search(r"app\.deck\.init\((.*)\);", script.text)
                if deck_info_match:
                    self.deck_info = json.loads(deck_info_match[1])
                    self.description_markdown_to_html()
                return
        log.critical('Не удалось найти информацию о колоде на странице!')

    def description_markdown_to_html(self):
        self.deck_info['description_html'] = markdown.markdown(self.deck_info['description_md'])
