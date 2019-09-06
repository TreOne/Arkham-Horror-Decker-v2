import time
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon, QFontDatabase, QFontMetrics
from classes.logger import log

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
    def __init__(self, char, size=50):
        super().__init__()
        self.char = char
        self._font_init(size)
        pixmap = self._draw_icon()
        self.addPixmap(pixmap)

    def _font_init(self, size):
        font_id = QFontDatabase.addApplicationFont(':/fonts/arkham-icons.ttf')
        font = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font)
        self.font.setPixelSize(size)

    def _draw_icon(self):
        fm = QFontMetrics(self.font)
        rect = QRect(0, 0, fm.horizontalAdvance(self.char), fm.height())
        pixmap = QPixmap(rect.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(self._get_color())
        painter.setFont(self.font)
        painter.drawText(rect, Qt.AlignCenter, self.char)
        painter.end()
        return pixmap

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
        return colors.get(self.char, default_color)


class Symbol:
    """Класс для ленивой загрузки и кэширования символов"""
    _cache = dict()

    def __getattr__(self, char):
        if char not in self._cache:
            self._cache[char] = ArkhamIcon(self.dict[char])
        return self._cache[char]

    def __init__(self):
        self.dict = {
            "agility": agility,
            "intellect": intellect,
            "lore": intellect,
            "strength": strength,
            "combat": strength,
            "will": will,
            "willpower": will,
            "wild": wild,

            "rogue": rogue,
            "survivor": survivor,
            "guardian": guardian,
            "mystic": mystic,
            "seeker": seeker,

            "action": action,
            "fast": fast,
            "free": fast,
            "lightning": fast,
            "reaction": reaction,

            "skull": skull,
            "cultist": cultist,
            "auto_fail": auto_fail,
            "elder_thing": elder_thing,
            "elder_sign": elder_sign,
            "eldersign": elder_sign,
            "tablet": tablet,

            "unique": unique,
            "per_investigator": per_investigator,
            "null": null,
        }

        log.info("Подключен модуль Символы Аркхэма")
