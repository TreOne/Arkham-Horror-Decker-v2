from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon


class ArkhamIcons:
    reaction = "!"
    fast = "j"
    free = "j"
    eldersign = "o"
    elder_sign = "o"
    lightning = "j"
    action = "i"
    strength = "c"
    combat = "c"
    agility = "a"
    will = "p"
    willpower = "p"
    lore = "b"
    intellect = "b"
    wild = "?"
    unique = "s"
    elder_thing = "n"
    skull = "k"
    auto_fail = "m"
    cultist = "l"
    tablet = "q"
    per_investigator = "u"
    null = "t"
    guardian = "f"
    mystic = "g"
    seeker = "h"
    rogue = "d"
    survivor = "e"

    def __init__(self, size):
        self.pixmap = QPixmap(QSize(size, size))

    def _clear(self):
        self.pixmap.fill(Qt.transparent)

    def get(self, symbol):
        self._clear()
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.begin(self.pixmap)
        painter.setPen(self._get_color(symbol))
        # TODO: Решить вопрос с размером иконок
        font_size = self.pixmap.size().height() * 0.85
        painter.setFont(QFont('arkham-icons', font_size))
        painter.drawText(self.pixmap.rect(), Qt.AlignCenter, symbol)
        painter.end()
        return QIcon(self.pixmap)

    def _get_color(self, symbol):
        # TODO: Добавить остальные цвета
        colors = {self.mystic: "#4331b9"}
        return QColor(colors.get(symbol, "None"))
