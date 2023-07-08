# coding: utf-8

from enum import Enum

import discord
from discord import TextChannel, Message, NotFound, Forbidden, HTTPException

from lib.services import config


class ChannelNames(Enum):
    BotDmChannel = 'bot-dms'
    LiveStreamsChannel = 'streams'
    BotSpamChannel = 'bot-spam'
    MatchesChannel = 'matches'
    LobbyChannel = 'lobby'


class AlertType(Enum):
    Primary = 1
    Info = 2
    Success = 3
    Warning = 4
    Error = 5


class AlertColor(Enum):
    Primary = config.default_embed_color
    Info = 4810126
    Success = 4820574
    Warning = 9342025
    Error = 9324873


class AlertEmotes(Enum):
    Primary = ':bookmark_tabs:'
    Info = ':information_source:'
    Success = ':white_check_mark:'
    Warning = ':warning:'
    Error = ':no_entry:'


class AlertHeadings(Enum):
    Primary = 'Alert'
    Info = 'Info'
    Success = 'Success!'
    Warning = 'Warning!'
    Error = 'Error!'


class TextChannelUtil(object):

    @staticmethod
    async def fetch_message(channel: TextChannel, message_id: int) -> Message | None:
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
        return await TextChannelUtil.send_alert(channel, AlertType.Primary, content)

    @staticmethod
    async def send_info(channel: TextChannel, content: str) -> discord.Message:
        return await TextChannelUtil.send_alert(channel, AlertType.Info, content)

    @staticmethod
    async def send_success(channel: TextChannel, content: str) -> discord.Message:
        return await TextChannelUtil.send_alert(channel, AlertType.Success, content)

    @staticmethod
    async def send_warning(channel: TextChannel, content: str) -> discord.Message:
        return await TextChannelUtil.send_alert(channel, AlertType.Warning, content)

    @staticmethod
    async def send_error(channel: TextChannel, content: str) -> discord.Message:
        return await TextChannelUtil.send_alert(channel, AlertType.Error, content)
