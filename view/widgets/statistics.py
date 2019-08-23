from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDockWidget, qApp

from view.ui.statistics_widget_ui import Ui_StatisticsWidget


class StatisticsWidget(QDockWidget, Ui_StatisticsWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        parent.addDockWidget(Qt.RightDockWidgetArea, self)

        background_color = qApp.palette().color(QPalette.Base).name()
        border_color = qApp.palette().color(QPalette.Mid).name()

        self.setStyleSheet("QDockWidget > QWidget {"
                           f"background-color: {background_color};"
                           f"border: 1 solid {border_color};"
                           "}")
