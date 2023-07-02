# coding: utf-8

import json
import os

from lib.filesystem import FileSystem


class ConfigException(Exception):
    """
    Custom exception for everything related to the configuration.
    """
    pass


class Config(object):
    """
    Global bot configuration.
    """
    def __init__(
            self,
            bot_user_id: str,
            enable_debug: bool,
            owner: str,
            guild: str,
            bot_secret: str,
            default_embed_color: int,
            log_level: int,
            welcome_dm: str | None
    ):
        self.bot_user_id = bot_user_id
        self.enable_debug = enable_debug
        self.owner = owner
        self.guild = guild
        self.bot_secret = bot_secret
        self.default_embed_color = default_embed_color
        self.log_level = log_level
        self.welcome_dm = welcome_dm

    @staticmethod
    def from_file():
        """
        Creates a new configuration object from the config file.
        :return:
        """
        config_file_path = os.path.join(FileSystem.get_directory(__file__), '..', 'settings.json')
        content: str = FileSystem.read_file(config_file_path)
        settings: dict[str, str] = json.loads(content)

        return Config(
            settings['bot_user_id'],
            bool(settings['enable_debug']),
            settings['owner'],
            settings['guild'],
            settings['bot_secret'],
            int(settings['default_embed_color']),
            int(settings['log_level']),
            settings['welcome_dm']
        )
