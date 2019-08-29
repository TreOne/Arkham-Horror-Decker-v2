import glob
import os
import shutil

from classes import constants
from classes.json_data import JsonDataStore
from classes.logger import log


class ProjectDataStore(JsonDataStore):

    def __init__(self):
        JsonDataStore.__init__(self)
        self.data_type = "данные проекта"  # Используется в сообщениях об ошибках
        self.default_project_filepath = os.path.join(constants.PROJECTS_PATH, 'default', '_default.project')

        # Путь по умолчанию
        self.current_filepath = None

        # Track changes after save
        self.has_unsaved_changes = False

        # Load default project data on creation
        # self.new()

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
        self._data["version"] = {constants.APP_NAME: constants.VERSION}

        # Пробуем сохранить файл настроек проекта (выкидывает ошибку при сбое)
        self.write_to_file(file_path, self._data, path_mode="relative", previous_path=self.current_filepath)
        self.current_filepath = file_path

        # Добавляем в "Последние файлы"
        # TODO: Раскомментировать, когда будет доделана система Последние файлы
        # self.add_to_recent_files(file_path)

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
