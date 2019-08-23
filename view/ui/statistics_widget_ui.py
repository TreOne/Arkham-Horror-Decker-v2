# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statistics_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StatisticsWidget(object):
    def setupUi(self, StatisticsWidget):
        StatisticsWidget.setObjectName("StatisticsWidget")
        StatisticsWidget.resize(400, 300)
        self.statistics_layout = QtWidgets.QWidget()
        self.statistics_layout.setObjectName("statistics_layout")
        self.formLayout = QtWidgets.QFormLayout(self.statistics_layout)
        self.formLayout.setObjectName("formLayout")
        self.label_card_count = QtWidgets.QLabel(self.statistics_layout)
        self.label_card_count.setObjectName("label_card_count")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_card_count)
        self.card_count = QtWidgets.QLabel(self.statistics_layout)
        self.card_count.setObjectName("card_count")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.card_count)
        StatisticsWidget.setWidget(self.statistics_layout)

        self.retranslateUi(StatisticsWidget)
        QtCore.QMetaObject.connectSlotsByName(StatisticsWidget)

    def retranslateUi(self, StatisticsWidget):
        _translate = QtCore.QCoreApplication.translate
        StatisticsWidget.setWindowTitle(_translate("StatisticsWidget", "Статистика"))
        self.label_card_count.setText(_translate("StatisticsWidget", "Карт в колоде:"))
        self.card_count.setText(_translate("StatisticsWidget", "0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StatisticsWidget = QtWidgets.QDockWidget()
    ui = Ui_StatisticsWidget()
    ui.setupUi(StatisticsWidget)
    StatisticsWidget.show()
    sys.exit(app.exec_())

