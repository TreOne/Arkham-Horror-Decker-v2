from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon


class ArkhamIcon(QIcon):
    def __init__(self, char, color=None, size=50):
        super().__init__()
        self.char = char
        self.__size = QSize(size, size)
        self.__color = color
        pixmap = QPixmap(self.__size)
        pixmap.fill(Qt.transparent)
        self._draw_icon(pixmap)
        self.addPixmap(pixmap)

    def set_size(self, size):
        self.__size = QSize(size, size)

    def set_color(self, color):
        self.__color = color

    def _draw_icon(self, pixmap):
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.begin(pixmap)
        painter.setPen(self._get_color())
        # TODO: Решить вопрос с размером иконок
        font_size = self.__size.height() * 0.6
        painter.setFont(QFont('arkham-icons', font_size))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, self.char)
        painter.end()

    def _get_color(self):
        colors = {
            "p": QColor("#003961"),
            "b": QColor("#4e1a45"),
            "c": QColor("#661e09"),
            "a": QColor("#00543a"),
            "?": QColor("#635120"),

            "d": QColor("#107116"),
            "e": QColor("#cc3038"),
            "f": QColor("#2b80c5"),
            "g": QColor("#4331b9"),
            "h": QColor("#ec8426"),
        }
        default_color = QColor("black")
        return self.__color if self.__color is not None else colors.get(self.char, default_color)


class Symbol:
    def __init__(self):
        super().__init__()
        self.agility = ArkhamIcon("a")
        self.lore = self.intellect = ArkhamIcon("b")
        self.strength = self.combat = ArkhamIcon("c")
        self.will = self.willpower = ArkhamIcon("p")
        self.wild = ArkhamIcon("?")

        self.rogue = ArkhamIcon("d")
        self.survivor = ArkhamIcon("e")
        self.guardian = ArkhamIcon("f")
        self.mystic = ArkhamIcon("g")
        self.seeker = ArkhamIcon("h")

        self.action = ArkhamIcon("i")
        self.fast = self.free = self.lightning = ArkhamIcon("j")
        self.reaction = ArkhamIcon("!")

        self.skull = ArkhamIcon("k")
        self.cultist = ArkhamIcon("l")
        self.auto_fail = ArkhamIcon("m")
        self.elder_thing = ArkhamIcon("n")
        self.eldersign = self.elder_sign = ArkhamIcon("o")
        self.tablet = ArkhamIcon("q")

        self.unique = ArkhamIcon("s")
        self.per_investigator = ArkhamIcon("u")
        self.null = ArkhamIcon("t")
