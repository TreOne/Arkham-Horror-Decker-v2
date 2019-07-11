import configparser
import os


class Settings:
    """
    Класс для считывания и записи настроек из конфигурационного файла.
    """

    def __init__(self):
        self.APP_NAME = 'Arkham Horror Decker'

        config_dir_name = '.' + self.APP_NAME.lower().replace(' ', '_')
        self.APP_CONFIG_DIR = os.path.join(os.path.expanduser("~"), config_dir_name)
        self.APP_CONFIG_FILENAME = os.path.join(self.APP_CONFIG_DIR, 'config.ini')

        self.config = configparser.ConfigParser()
        if not os.path.exists(self.APP_CONFIG_FILENAME):
            self.create_config()
        self.config.read(self.APP_CONFIG_FILENAME)

    def get(self, section, setting):
        value = self.config.get(section, setting)
        return value

    def set(self, section, setting, value):
        self.config.set(section, setting, value)
        with open(self.APP_CONFIG_FILENAME, 'w') as config_file:
            self.config.write(config_file)

    def create_config(self):
        if not os.path.exists(self.APP_CONFIG_DIR):
            os.makedirs(self.APP_CONFIG_DIR)
        self.config.add_section("Appearance")
        self.set('Appearance', 'theme_style', 'fusion')
