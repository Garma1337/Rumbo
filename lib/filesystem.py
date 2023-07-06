# coding: utf-8

import os
from typing import List


class FileSystemException(Exception):
    """
    Exception class for filesystem operations.
    """
    pass


class FileSystem(object):

    @staticmethod
    def read_file(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileSystemException('File "{}" does not exist'.format(file_path))

        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def get_directory_path(file: str) -> str:
        return os.path.dirname(os.path.realpath(file))

    @staticmethod
    def get_files_in_directory(path: str) -> List[str]:
        return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

    @staticmethod
    def get_directories_in_directory(path: str) -> List[str]:
        return [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]
