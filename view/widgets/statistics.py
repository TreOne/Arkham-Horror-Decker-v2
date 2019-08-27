import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDockWidget
from classes import ui_util
from classes.app import get_app
from classes.constants import PATH


class StatisticsWidget(QDockWidget):
    """Виджет статистики"""

    ui_path = os.path.join(PATH, 'view', 'ui', 'statistics_widget.ui')

    def __init__(self, parent):
        QDockWidget.__init__(self)

        ui_util.load_ui(self, self.ui_path)
        ui_util.init_ui(self)

        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        parent.addDockWidget(Qt.RightDockWidgetArea, self)

        app = get_app()
        background_color = app.palette().color(QPalette.Base).name()
        border_color = app.palette().color(QPalette.Mid).name()

        self.setStyleSheet(f"""
                                QWidget#statistics_layout {{
                                    background-color: {background_color};
                                    border: 1px solid {border_color};
                                }}
                                QLabel {{
                                    margin: 2px 0px 0px 2px;
                                }}
                            """)
