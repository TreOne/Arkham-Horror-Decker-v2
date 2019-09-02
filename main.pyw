import sys

try:
    from classes import constants
    print("Загрузка модулей из текущего каталога: %s" % constants.PATH)
except ImportError:
    # TODO: Реализовать функцию
    # sys.path.append(installer.INSTALL_PATH)
    from classes import constants
    print("Загрузка модулей из каталога установки: %s" % constants.PATH)


from classes.app import App


def main():
    # Запуск основного потока
    app = App(sys.argv)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
