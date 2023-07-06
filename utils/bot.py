# coding: utf-8

import os
from typing import List

from discord import Guild, Bot, Forbidden, HTTPException

from lib.filesystem import FileSystem


class BotUtil(object):

    @staticmethod
    async def fetch_guild(bot: Bot, guild_id: int) -> Guild | None:
        try:
            guild: Guild = await bot.fetch_guild(guild_id)
        except Forbidden:
            return None
        except HTTPException:
            return None

        return guild

    @staticmethod
    def get_available_extensions() -> List[str]:
        extensions: List[str] = []

        current_directory: str = FileSystem.get_directory_path(__file__)

        directories: List[dict[str, str]] = [
            {
                'directory' : os.path.join(current_directory, '..', 'commands', 'message_commands'),
                'prefix': 'commands.message_commands'
            },
            {
                'directory': os.path.join(current_directory, '..', 'commands', 'slash_commands'),
                'prefix': 'commands.slash_commands'
            },
            {
                'directory': os.path.join(current_directory, '..', 'commands', 'user_commands'),
                'prefix': 'commands.user_commands'
            }
        ]

        for directory in directories:
            files: List[str] = FileSystem.get_files_in_directory(directory['directory'])
            module_files: List[str] = list(filter(lambda f: not f.startswith('__'), files))

            for module_file in module_files:
                extensions.append(f'{directory["prefix"]}.{module_file.replace(".py", "")}')

        return extensions
