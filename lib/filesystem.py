# coding: utf-8

import os


class FileSystemException(Exception):
    """
    Exception class for filesystem operations.
    """
    pass


class FileSystem(object):
    """
    Various filesystem operation utilities.
    """

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads content from a file and returns it as string.
        :param file_path:
        :return:
        """
        if not os.path.exists(file_path):
            raise FileSystemException('File "{}" does not exist'.format(file_path))

        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def get_directory(file: str) -> str:
        """
        Returns the absolute path to a directory.
        :param file:
        :return:
        """
        return os.path.dirname(os.path.realpath(file))
