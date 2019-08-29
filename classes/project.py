import os

from classes import constants
from classes.json_data import JsonDataStore


class ProjectDataStore(JsonDataStore):
    """Класс представляет собой проект отдельной колоды (отдельной ссылки на базу)"""

    def __init__(self):
        JsonDataStore.__init__(self)
        self.data_type = "данные проекта"  # Используется в сообщениях об ошибках
        self.default_project_filepath = os.path.join(constants.PATH, 'settings', '_default.project')

        # Set default filepath to user's home folder
        self.current_filepath = None

        # Track changes after save
        self.has_unsaved_changes = False

        # Load default project data on creation
        # self.new()

    def needs_save(self):
        """Возвращает информацию о необходимости сохранения проекта"""
        return self.has_unsaved_changes
