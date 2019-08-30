import glob
import os
import random
import shutil
from classes import constants
from classes.json_data import JsonDataStore
from classes.logger import log


class ProjectDataStore(JsonDataStore):

    def __init__(self):
        JsonDataStore.__init__(self)
        self.data_type = "данные проекта"  # Используется в сообщениях об ошибках
        self.default_project_filepath = os.path.join(constants.DEFAULT_PROJECT_PATH, '_project.json')

        # Путь по умолчанию
        self.current_file_path = None

        # Отслеживание изменений в проекте
        self.has_unsaved_changes = False

        # Загружаем настройки по умолчанию
        self.load_default_project_settings()

    def needs_save(self):
        """Возвращает информацию о необходимости сохранения проекта"""
        return self.has_unsaved_changes

    def save(self, file_path, move_temp_files=True):
        """Сохранить проект на диск"""
        log.info("Сохранение проекта: {}".format(file_path))

        # Перенос всех временных файлов в папку проекта
        if move_temp_files:
            self.move_temp_paths_to_project_folder(file_path)

        # Добавляем информацию о версии приложения
        self._data["app_version"] = constants.VERSION

        # Пробуем сохранить файл настроек проекта (выкидывает ошибку при сбое)
        self.write_to_file(file_path, self._data, path_mode="relative", previous_path=self.current_file_path)
        self.current_file_path = file_path

        # Добавляем в "Последние файлы"
        self.add_to_recent_files(file_path)

        self.has_unsaved_changes = False

    def move_temp_paths_to_project_folder(self, file_path):
        """Перемещает все временные файлы в папку проекта"""
        try:
            new_project_folder = os.path.dirname(file_path)
            new_images_folder = os.path.join(new_project_folder, "images")

            # Создаем папку для хранения изображений
            if not os.path.exists(new_images_folder):
                os.mkdir(new_images_folder)

            # Копируем все изображения в папку проекта
            for filename in glob.glob(os.path.join(constants.IMAGES_PATH, '*.*')):
                shutil.copy(filename, new_images_folder)

        except Exception as ex:
            log.error("Ошибка при перемещении временных файлов в папку проекта: %s" % str(ex))

    def add_to_recent_files(self, file_path):
        """Добавить проект в список 'Последние файлы'"""
        if not file_path or "backup.coa" in file_path:
            return  # Не добавлять резервную копию в список

        from classes.app import get_settings
        settings = get_settings()
        recent_projects = settings.value("recent_projects", list())

        # Проверяем, что file_path является абсолютным
        file_path = os.path.abspath(file_path)

        # Удаляем существующий проект
        if file_path in recent_projects:
            recent_projects.remove(file_path)

        # Удаляем самый старый элемент (если нужно)
        if len(recent_projects) > 10:
            del recent_projects[0]

        # Добавить путь к файлу в конец списка
        recent_projects.append(file_path)

        # Сохраняем список
        settings.setValue("recent_projects", recent_projects)

    def load(self, file_path, clear_images=True):
        """Загрузка проекта из файла"""
        self.load_default_project_settings()

        if file_path:
            log.info("Загрузка проекта: {}".format(file_path))

            # Данные проекта по умолчанию
            default_project = self._data

            try:
                # Загружаем проект
                project_data = self.read_from_file(file_path, path_mode="absolute")
            except Exception as ex:
                raise ex

            # Объединить параметры по умолчанию и параметры проекта
            self._data = self.merge_settings(default_project, project_data)

            self.current_file_path = file_path
            self.has_unsaved_changes = False

            # Копируем все изображения проекта в рабочую папку изображений
            loaded_project_folder = os.path.dirname(self.current_file_path)
            project_images_folder = os.path.join(loaded_project_folder, "images")
            if os.path.exists(project_images_folder) and clear_images:
                # Удаляем удаляем каталог с изображениями
                shutil.rmtree(constants.IMAGES_PATH, True)

                # Копируеем каталог с изображениями из папки проекта в рабочий каталог
                shutil.copytree(project_images_folder, constants.IMAGES_PATH)

            # Добавляем путь в список "Последние файлы"
            self.add_to_recent_files(file_path)

            # Обновление всех структур данных
            self.upgrade_project_data_structures()

    def load_default_project_settings(self):
        """Загружает файл настроек проекта по умолчанию (выкидывает ошибку при сбое)"""
        self._data = self.read_from_file(self.default_project_filepath)
        self.current_file_path = None
        self.has_unsaved_changes = False
        # Генерируем ID проекта
        self._data["id"] = self.generate_id()

    def upgrade_project_data_structures(self):
        """Устранение проблем с файлами проекта (если таковые имеются)"""
        app_version = self._data["app_version"]
        log.info("Применяем исправления проекта версии %s" % app_version)
        # Исправить идентификатор проекта по умолчанию (если найден)
        if self._data.get("id") == "T0":
            self._data["id"] = self.generate_id()

    @staticmethod
    def generate_id(digits=10):
        """Генерирует случайный ID"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        id = ""
        for i in range(digits):
            c_index = random.randint(0, len(chars) - 1)
            id += (chars[c_index])
        return id
