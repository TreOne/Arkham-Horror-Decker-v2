import sys
from classes.app import App
from view.main_window import MainWindow


def main():
    # Запуск основного потока
    app = App(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
