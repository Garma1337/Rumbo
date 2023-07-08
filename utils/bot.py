# coding: utf-8

import os
from typing import List

import discord.utils
from discord import Guild, Forbidden, HTTPException, Message, TextChannel

from lib.filesystem import FileSystem
from lib.services import bot, config, logger
from utils.text_channel import ChannelNames


class BotUtil(object):

    @staticmethod
    async def log_dm(message: Message):
        guild: Guild = await BotUtil.fetch_guild(config.guild)
        dm_channel: TextChannel | None = discord.utils.get(guild.channels, name=ChannelNames.BotDmChannel.value)

        if dm_channel:
            attachments: List[str] = []

            for attachment in message.attachments:
                attachments.append(attachment.url)

            quoted_content: str | None = ''
            quoted_content_lines: List[str] = []
            content: str = message.content
            if content:
                content_lines: List[str] = content.split('\n')
                for content_line in content_lines:
                    quoted_content_lines.append(f'> {content_line}')

                quoted_content = '\n'.join(quoted_content_lines)

            log_lines: List[str] = [
                f'**Received DM by <@{message.author.id}> ({message.author.display_name}#{message.author.discriminator})**',
                '**Message content:**',
                quoted_content,
                '**Attachments:**'
                '\n'.join(attachments)
            ]

            await dm_channel.send('\n'.join(log_lines))
        else:
            logger.warning(f'Received DM from {message.author.id}, but there is no channel to post it to')

    @staticmethod
    async def fetch_guild(guild_id: int) -> Guild | None:
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
                'directory': os.path.join(current_directory, '..', 'commands', 'message_commands'),
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
