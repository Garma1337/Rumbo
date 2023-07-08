# coding: utf-8

import json
import os

from lib.filesystem import FileSystem


class ConfigException(Exception):
    pass


class Config(object):

    def __init__(
            self,
            enable_debug: bool,
            owner: int,
            guild: int,
            bot_secret: str,
            default_embed_color: int,
            log_level: int,
            welcome_dm: str | None
    ):
        self.enable_debug = enable_debug
        self.owner = owner
        self.guild = guild
        self.bot_secret = bot_secret
        self.default_embed_color = default_embed_color
        self.log_level = log_level
        self.welcome_dm = welcome_dm

    @staticmethod
    def from_file():
        config_file_path = os.path.join(FileSystem.get_directory_path(__file__), '..', 'settings.json')
        content: str = FileSystem.read_file(config_file_path)
        settings: dict[str, str] = json.loads(content)

        return Config(
            bool(settings['enable_debug']),
            int(settings['owner']),
            int(settings['guild']),
            settings['bot_secret'],
            int(settings['default_embed_color']),
            int(settings['log_level']),
            settings['welcome_dm']
        )
