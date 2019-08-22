import sys
from utility.app_preparer import AppPreparer
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow


if __name__ == '__main__':
    # Запуск основного потока
    app = QApplication(sys.argv)
    preparer = AppPreparer()
    preparer.prepare_app(app)
    main_window = MainWindow()
    # main_window.showMaximized()
    main_window.show()
    sys.exit(app.exec_())
