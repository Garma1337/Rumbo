# coding: utf-8

import logging
import os
from typing import NoReturn

from lib.config import Config
from lib.filesystem import FileSystem


class Logger(object):

    def __init__(self, config: Config):
        current_directory: str = FileSystem.get_directory_path(__file__)
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
        self.logger.debug(message)

    def info(self, message: str) -> NoReturn:
        self.logger.info(message)

    def warning(self, message: str) -> NoReturn:
        self.logger.warning(message)

    def error(self, message: str) -> NoReturn:
        self.logger.error(message)

    def critical(self, message: str) -> NoReturn:
        self.logger.critical(message)
