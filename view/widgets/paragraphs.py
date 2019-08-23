from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget


class ParagraphsWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__("Paragraphs", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        paragraphs_list = QListWidget(self)
        paragraphs_list.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
            "28 days.",
            "We have dispatched those items that were in stock. The rest of "
            "your order will be dispatched once all the remaining items "
            "have arrived at our warehouse. No additional shipping "
            "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
            "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
            "your order anyway. We'll add this underpayment to your next "
            "bill.",
            "Unfortunately you did not send enough money. Please remit an "
            "additional $. Your order will be dispatched as soon as the "
            "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
            "items, or should we return the excess to you?"))

        self.setWidget(paragraphs_list)
        parent.addDockWidget(Qt.RightDockWidgetArea, self)
