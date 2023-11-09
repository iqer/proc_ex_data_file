import os
from abc import abstractmethod

from const import RES_PATH


class File:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_path = os.path.sep.join([RES_PATH, file_name])
        if self.file_name.endswith('.txt'):
            self.output_file_name = self.file_name.replace('.txt', '.xlsx')
        elif self.file_name.endswith('.xml'):
            self.output_file_name = self.file_name.replace('.xml', '.xlsx')
        self.output_file_path = os.path.sep.join([RES_PATH, self.output_file_name])
        self._load_data_lines()
        self._check_data_lines()
        self._proc_data_lines()

    @abstractmethod
    def _load_data_lines(self):
        pass

    @abstractmethod
    def _check_data_lines(self):
        pass

    @abstractmethod
    def _proc_data_lines(self):
        pass

    @abstractmethod
    def to_excel(self):
        pass
