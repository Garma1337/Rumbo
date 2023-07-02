# coding: utf-8

import logging
import os
from typing import NoReturn

from lib.config import Config
from lib.filesystem import FileSystem


class Logger(object):
    """
    Simple file logger.
    """

    def __init__(self, config: Config):
        current_directory: str = FileSystem.get_directory(__file__)
        log_file_path: str = os.path.join(current_directory, '..', 'bot.log')

        self.logger = logging.getLogger('Default')
        self.logger.setLevel(config.log_level)

        default_formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')

        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(config.log_level)
        file_handler.setFormatter(default_formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(config.log_level)
        stream_handler.setFormatter(default_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def debug(self, message: str) -> NoReturn:
        """
        Logs a debug message.
        :param message:
        """
        self.logger.debug(message)

    def info(self, message: str) -> NoReturn:
        """
        Logs an info message.
        :param message:
        """
        self.logger.info(message)

    def warning(self, message: str) -> NoReturn:
        """
        Logs a warning message.
        :param message:
        """
        self.logger.warning(message)

    def error(self, message: str) -> NoReturn:
        """
        Logs an error message.
        :param message:
        """
        self.logger.error(message)

    def critical(self, message: str) -> NoReturn:
        """
        Logs a critical message.
        :param message:
        """
        self.logger.critical(message)
