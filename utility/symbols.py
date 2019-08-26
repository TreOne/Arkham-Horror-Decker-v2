from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon, QFontDatabase, QFontMetrics

from utility.helper_function import resource_path

agility = "a"
intellect = "b"
strength = "c"
will = "p"
wild = "?"

rogue = "d"
survivor = "e"
guardian = "f"
mystic = "g"
seeker = "h"

action = "i"
fast = "j"
reaction = "!"

skull = "k"
cultist = "l"
auto_fail = "m"
elder_thing = "n"
elder_sign = "o"
tablet = "q"

unique = "s"
per_investigator = "u"
null = "t"


class ArkhamIcon(QIcon):
    def __init__(self, char, color=None, size=50):
        super().__init__()
        self.char = char
        self.__color = color

        # arkham-icons
        font_id = QFontDatabase.addApplicationFont(resource_path('resources/fonts/arkham-icons.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family)
        self.font.setPixelSize(size)
        pixmap = self._draw_icon()
        self.addPixmap(pixmap)

    def set_color(self, color):
        self.__color = color

    def _draw_icon(self):
        rect = self._get_bounding_rect()
        pixmap = QPixmap(rect.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(self._get_color())
        painter.setFont(self.font)
        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, self.char)
        painter.end()
        return pixmap

    def _get_bounding_rect(self):
        font_metrics = QFontMetrics(self.font)
        bounding_rect = font_metrics.tightBoundingRect(self.char)
        char_rect = QRect(0, 0, bounding_rect.width(), bounding_rect.height())
        return char_rect

    def _get_color(self):
        colors = {
            agility: QColor("#00543a"),
            intellect: QColor("#4e1a45"),
            strength: QColor("#661e09"),
            will: QColor("#003961"),
            wild: QColor("#635120"),

            rogue: QColor("#107116"),
            survivor: QColor("#cc3038"),
            guardian: QColor("#2b80c5"),
            mystic: QColor("#4331b9"),
            seeker: QColor("#ec8426"),
        }
        default_color = QColor("black")
        return self.__color if self.__color is not None else colors.get(self.char, default_color)


class Symbol:
    def __init__(self):
        self.agility = ArkhamIcon(agility)
        self.intellect = self.lore = ArkhamIcon(intellect)
        self.strength = self.combat = ArkhamIcon(strength)
        self.will = self.willpower = ArkhamIcon(will)
        self.wild = ArkhamIcon(wild)

        self.rogue = ArkhamIcon(rogue)
        self.survivor = ArkhamIcon(survivor)
        self.guardian = ArkhamIcon(guardian)
        self.mystic = ArkhamIcon(mystic)
        self.seeker = ArkhamIcon(seeker)

        self.action = ArkhamIcon(action)
        self.free = self.fast = self.lightning = ArkhamIcon(fast)
        self.reaction = ArkhamIcon(reaction)

        self.skull = ArkhamIcon(skull)
        self.cultist = ArkhamIcon(cultist)
        self.auto_fail = ArkhamIcon(auto_fail)
        self.elder_thing = ArkhamIcon(elder_thing)
        self.elder_sign = self.eldersign = ArkhamIcon(elder_sign)
        self.tablet = ArkhamIcon(tablet)

        self.unique = ArkhamIcon(unique)
        self.per_investigator = ArkhamIcon(per_investigator)
        self.null = ArkhamIcon(null)
