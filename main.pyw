import sys
from classes.app import App


def main():
    # Запуск основного потока
    app = App(sys.argv)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
