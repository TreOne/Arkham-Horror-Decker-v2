from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon


class Symbol(QIcon):
    agility = "a"
    lore = intellect = "b"
    strength = combat = "c"
    will = willpower = "p"
    wild = "?"

    rogue = "d"
    survivor = "e"
    guardian = "f"
    mystic = "g"
    seeker = "h"

    action = "i"
    fast = free = lightning = "j"
    reaction = "!"

    skull = "k"
    cultist = "l"
    auto_fail = "m"
    elder_thing = "n"
    eldersign = elder_sign = "o"
    tablet = "q"

    unique = "s"
    per_investigator = "u"
    null = "t"

    def __init__(self, symbol, size=50, color=QColor("black")):
        super().__init__()
        self.symbol = symbol
        self.__size = QSize(size, size)
        self.__color = color
        pixmap = self._get_pixmap()
        self._draw_icon(pixmap, symbol)
        self.addPixmap(pixmap)

    def set_size(self, size):
        self.__size = QSize(size, size)

    def set_color(self, color):
        self.__color = color

    def _get_pixmap(self):
        pixmap = QPixmap(self.__size)
        pixmap.fill(Qt.transparent)
        return pixmap

    def _draw_icon(self, pixmap, symbol):
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.begin(pixmap)
        painter.setPen(self._get_color(symbol))
        # TODO: Решить вопрос с размером иконок
        font_size = self.__size.height() * 0.6
        painter.setFont(QFont('arkham-icons', font_size))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, symbol)
        painter.end()

    def _get_color(self, symbol):
        # TODO: Добавить остальные цвета
        colors = {self.mystic: "#4331b9"}
        return QColor(colors.get(symbol, "black"))
