from abc import ABC, abstractmethod


class IStorage(ABC):
    """

    """
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def list_movies(self, movies_list=None):
        pass

    @abstractmethod
    def add_movie(self):
        pass

    @abstractmethod
    def delete_movie(self):
        pass

    @abstractmethod
    def update_movie(self):
        pass

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, new_file_path):
        self.file_path = new_file_path

