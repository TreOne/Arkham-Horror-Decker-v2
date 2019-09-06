import json
import copy
import os
import re
from PyQt5.QtCore import QFile
from classes.logger import log
from classes import constants

# Скомпилированное регулярное выражение для пути
path_regex = re.compile(r'\"(image|path)\":.*?\"(.*?)\"', re.UNICODE)
path_context = {}


class JsonDataStore:
    """Этот класс позволяет получать/устанавливать ключи и значения,
    а так же сохранять их в json файлы и загружать данные из них.
    Внутреннее хранилище это словарь. Модуль json используется для сериализации и десериализации
    данных из json в словарь. Предполагается, что ключи имеют строковый тип, но методы суперклассов get/set,
    могут использовать разные типы ключей. Методы write_to_file и read_from_file агностичны к типу ключа."""

    def __init__(self):
        self._data = {}
        self.data_type = "json данные"  # Для ведения журнала сообщений

    def get(self, key):
        """Получить копию значения из хранилища"""
        key = key.lower()
        return copy.deepcopy(self._data.get(key, None))

    def set(self, key, value):
        """Записать значение в хранилище"""
        key = key.lower()
        self._data[key] = value

    def merge_settings(self, default, user):
        """Объединить словари"""
        for key in default:
            if key not in user:
                # Добавить отсутствующий ключ в словарь user
                user[key] = default[key]
        return user

    def read_from_file(self, file_path, path_mode="ignore"):
        """Загрузить данные из JSON файла"""
        try:
            # Если не указан файл проекта, то загружаем проект по умолчанию
            if file_path is None:
                default_project_file = QFile(":/default/_project.json")
                default_project_file.open(QFile.ReadOnly)
                contents = bytes(default_project_file.readAll()).decode('UTF-8')
            else:
                # В противном случае, загружаем проект из указанного файла
                with open(file_path, 'r', encoding='utf8') as f:
                    contents = f.read()
            if contents:
                if path_mode == "absolute":
                    # Преобразование всех путей в абсолютные
                    contents = self.convert_paths_to_absolute(file_path, contents)
                return json.loads(contents, strict=False)
        except Exception as ex:
            msg = ("Не могу загрузить {} из файла: {}".format(self.data_type, ex))
            log.error(msg)
            raise Exception(msg)
        msg = ("Не могу загрузить {} из пустого файла.".format(self.data_type))
        log.warning(msg)
        raise Exception(msg)

    def write_to_file(self, file_path, data, make_paths_relative=False, previous_path=None):
        """Сохранить данные в JSON файл"""
        try:
            contents = json.dumps(data, indent=4)
            if make_paths_relative:
                # Преобразование всех путей в относительные
                contents = self.convert_paths_to_relative(file_path, previous_path, contents)
            with open(file_path, 'w') as f:
                f.write(contents)
        except Exception as ex:
            msg = "Не удается сохранить {} в файл:\n{}\n{}".format(self.data_type, file_path, ex)
            log.error(msg)
            raise Exception(msg)

    def convert_paths_to_relative(self, file_path, previous_path, data):
        """Преобразование всех путей в относительные (относительно пути file_path)"""
        try:
            path_context["new_project_folder"] = os.path.dirname(file_path)
            path_context["existing_project_folder"] = os.path.dirname(file_path)
            if previous_path:
                path_context["existing_project_folder"] = os.path.dirname(previous_path)

            data = re.sub(path_regex, self.replace_string_to_relative, data)
        except Exception as ex:
            log.error("Ошибка при преобразовании абсолютных путей в относительные: %s" % str(ex))
        return data

    def replace_string_to_relative(self, match):
        """Преобразовать пути в найденном совпадении на относительные пути"""
        key = match.groups(0)[0]
        path = match.groups(0)[1]
        utf_path = json.loads('"%s"' % path, encoding="utf-8")  # Преобразовать строку байтов в unicode
        folder_path, file_path = os.path.split(os.path.abspath(utf_path))

        # Найти абсолютный путь к файлу (при необходимости)
        # Преобразование пути в правильный относительный путь (на основе существующей папки)
        orig_abs_path = os.path.abspath(utf_path)

        # Удалить файл из abs path
        orig_abs_folder = os.path.split(orig_abs_path)[0]

        # Вычислить новый относительный путь
        new_rel_path_folder = os.path.relpath(orig_abs_folder, path_context.get("new_project_folder", ""))
        new_rel_path = os.path.join(new_rel_path_folder, file_path).replace("\\", "/")
        new_rel_path = json.dumps(new_rel_path)  # Экранировать слэши
        return '"%s": %s' % (key, new_rel_path)

    def convert_paths_to_absolute(self, file_path, data):
        """Преобразование всех путей в абсолютные с помощью регулярного выражения"""
        try:
            path_context["new_project_folder"] = os.path.dirname(file_path)
            path_context["existing_project_folder"] = os.path.dirname(file_path)

            data = re.sub(path_regex, self.replace_string_to_absolute, data)

        except Exception as ex:
            log.error("Ошибка при преобразовании относительных путей в абсолютные: %s" % str(ex))

        return data

    def replace_string_to_absolute(self, match):
        """Преобразовать пути в найденном совпадении на абсолютные пути"""
        key = match.groups(0)[0]
        path = match.groups(0)[1]

        # Найти абсолютный путь к файлу (при необходимости)
        utf_path = json.loads('"%s"' % path, encoding="utf-8")  # Преобразовать строку байтов в unicode
        if "@transitions" not in utf_path:
            # Преобразование пути в правильный относительный путь (на основе существующей папки)
            new_path = os.path.abspath(os.path.join(path_context.get("existing_project_folder", ""), utf_path))
            new_path = json.dumps(new_path)  # Экранировать слэши
            return '"%s": %s' % (key, new_path)

        # Определить, найден ли путь @transitions
        else:
            new_path = path.replace("@transitions", os.path.join(constants.PATH, "transitions"))
            new_path = json.dumps(new_path)  # Экранировать слэши
            return '"%s": %s' % (key, new_path)
