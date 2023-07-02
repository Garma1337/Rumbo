# coding: utf-8

from typing import List

from discord import TextChannel, Member
from tortoise import run_async, Tortoise

from db.init import init
from db.models.player import Player
from lib.services import config, logger, bot
from utils.activity import ActivityUtil
from utils.guild import GuildUtil
from utils.member import MemberUtil
from utils.text_channel import ChannelNames

run_async(init())


@bot.event
async def on_ready():
    """
    Executes eventhandlers when the bot is ready.
    """
    logger.info(f'{bot.user} is ready and online!')


@bot.event
async def on_member_join(member: Member):
    """
    Executes eventhandlers when a member joins.
    :param member:
    """
    logger.info(f'Creating a new player record for player {member.id}')

    await Player.create(discord_id=member.id)

    if config.welcome_dm:
        await MemberUtil.send_dm(member, config.welcome_dm)


@bot.event
async def on_presence_update(before: Member, after: Member):
    """
    Executes eventhandlers when a member's presence is updated
    :param before:
    :param after:
    """
    if not ActivityUtil.is_crash_team_rumble_stream(before.activity) and ActivityUtil.is_crash_team_rumble_stream(
            after.activity):
        stream_channel: TextChannel = GuildUtil.find_channel_by_name(
            before.guild,
            ChannelNames.LiveStreamsChannel.value
        )

        if stream_channel:
            await stream_channel.send(f'<@{before.id}> is now streaming!')


@bot.event
async def on_member_leave(member: Member):
    """
    Executes eventhandlers when a member leaves the server.
    :param member:
    """
    logger.info(f'Deleting existing record for player {member.id}')

    player: Player = await Player.find_or_create(member.id)
    await Player.delete(player)


extensions: List[str] = [
    'admin',
    'general',
    'lobby',
    'moderation',
    'profile',
    'social'
]

for extension in extensions:
    loaded_extensions = bot.extensions.keys()
    extension_name: str = f'commands.slash_commands.{extension}'

    if extension_name not in loaded_extensions:
        bot.load_extension(extension_name)

bot.run(config.bot_secret)


async def close_connections():
    """
    Closes database connections.
    """
    await Tortoise.close_connections()


run_async(close_connections())
