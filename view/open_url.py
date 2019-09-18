import json
import re
import requests
from PyQt5.QtWidgets import QDialog
from classes import ui_util
from bs4 import BeautifulSoup


class OpenUrlDialog(QDialog):
    """Окно 'Открыть ссылку'"""
    def __init__(self):
        QDialog.__init__(self)
        ui_util.load_ui(self, 'open_url')
        ui_util.init_ui(self)

        self.deck_info = None  # Переменная для хранения информации о загруженной колоде

        # TODO: Демо URL для отладки.
        self.field_url.setText('https://arkhamdb.com/decklist/view/6486/lola-for-cowards-hard-expert-1.0')

    def btn_open_url_click(self):
        # Получаем HTML страницу
        url = self.field_url.text()
        page_html = requests.get(url).text
        self.get_deck_info_from_html(page_html)

    def get_deck_info_from_html(self, html):
        # Разбираем полученный HTML (Вытягиваем JS и из него тащим JSON объект с картами)
        parsed_html = BeautifulSoup(html)
        js_on_page = parsed_html.findAll('script', type='text/javascript')
        self.find_deck_info_in_js_array(js_on_page)

    def find_deck_info_in_js_array(self, js_array):
        for script in js_array:
            if "app.deck.init" in script.text:
                deck_info_match = re.search(r"app\.deck\.init\((.*)\);", script.text)
                self.deck_info = json.loads(deck_info_match[1]) if deck_info_match else None
