# coding: utf-8

from enum import Enum

import discord
from discord import TextChannel, Message, NotFound, Forbidden, HTTPException

from lib.config import Config

config: Config = Config.from_file()


class ChannelNames(Enum):
    """
    Enum for channel names.
    """

    LiveStreamsChannel = 'streams'
    BotSpamChannel = 'bot-spam'
    MatchesChannel = 'matches'
    LobbyChannel = 'lobby'


class AlertType(Enum):
    """
    Enum for alert types.
    """

    Primary = 1
    Info = 2
    Success = 3
    Warning = 4
    Error = 5


class AlertColor(Enum):
    """
    Enum for alert colors.
    """

    Primary = config.default_embed_color
    Info = 4810126
    Success = 4820574
    Warning = 9342025
    Error = 9324873


class AlertEmotes(Enum):
    """
    Enum for alert emotes.
    """

    Primary = ':bookmark_tabs:'
    Info = ':information_source:'
    Success = ':white_check_mark:'
    Warning = ':warning:'
    Error = ':no_entry:'


class AlertHeadings(Enum):
    """
    Enum for alert headings.
    """

    Primary = 'Alert'
    Info = 'Info'
    Success = 'Success!'
    Warning = 'Warning!'
    Error = 'Error!'


class TextChannelUtil(object):
    """
    Various text channel utilities.
    """

    @staticmethod
    async def fetch_message(channel: TextChannel, message_id: int) -> Message | None:
        """
        Gets a message by ID.
        :param channel:
        :param message_id:
        """
        try:
            message: Message = await channel.fetch_message(message_id)
        except NotFound:
            return None
        except Forbidden:
            return None
        except HTTPException:
            return None

        return message

    @staticmethod
    async def send_alert(channel: TextChannel, alert_type: AlertType, content: str) -> discord.Message:
        """
        Sends an alert message into a channel.
        :param channel:
        :param alert_type:
        :param content:
        """
        color: int = AlertColor[alert_type.name].value
        emote: str = AlertEmotes[alert_type.name].value
        heading: str = AlertHeadings[alert_type.name].value

        embed: discord.Embed = discord.Embed(
            colour=color
        )

        embed.add_field(
            name=f'{emote} {heading}',
            value=f'\u200B\n{content}'
        )

        return await channel.send(embed=embed)

    @staticmethod
    async def send_primary(channel: TextChannel, content: str) -> discord.Message:
        """
        Sends a primary alert into a channel.
        :param channel:
        :param content:
        """
        return await TextChannelUtil.send_alert(channel, AlertType.Primary, content)

    @staticmethod
    async def send_info(channel: TextChannel, content: str) -> discord.Message:
        """
        Sends an info alert info a channel.
        :param channel:
        :param content:
        """
        return await TextChannelUtil.send_alert(channel, AlertType.Info, content)

    @staticmethod
    async def send_success(channel: TextChannel, content: str) -> discord.Message:
        """
        Sends a success alert into a channel.
        :param channel:
        :param content:
        """
        return await TextChannelUtil.send_alert(channel, AlertType.Success, content)

    @staticmethod
    async def send_warning(channel: TextChannel, content: str) -> discord.Message:
        """
        Sends a warning alert into a channel.
        :param channel:
        :param content:
        """
        return await TextChannelUtil.send_alert(channel, AlertType.Warning, content)

    @staticmethod
    async def send_error(channel: TextChannel, content: str) -> discord.Message:
        """
        Sends an error alert into a channel.

        :param channel:
        :param content:
        """
        return await TextChannelUtil.send_alert(channel, AlertType.Error, content)
