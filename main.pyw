import sys
from utility.app_wrapper import App
from view.main_window import MainWindow

# Запуск основного потока
app = App(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
