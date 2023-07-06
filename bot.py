# coding: utf-8

from typing import List

from discord import TextChannel, Member
from tortoise import run_async, Tortoise

from db.init import init
from db.models.player import Player
from lib.services import config, logger, bot
from lib.views.lobby_buttons_view import LobbyButtonsView
from utils.activity import ActivityUtil
from utils.bot import BotUtil
from utils.guild import GuildUtil
from utils.member import MemberUtil
from utils.text_channel import ChannelNames

run_async(init())


@bot.event
async def on_ready():
    logger.info(f'{bot.user} is ready and online!')

    # persistent views
    bot.add_view(LobbyButtonsView())


@bot.event
async def on_member_join(member: Member):
    logger.info(f'Creating a new player record for player {member.id}')

    await Player.create(discord_id=member.id)

    if config.welcome_dm:
        await MemberUtil.send_dm(member, config.welcome_dm)


@bot.event
async def on_presence_update(before: Member, after: Member):
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
    logger.info(f'Deleting existing record for player {member.id}')

    player: Player = await Player.find_or_create(member.id)
    await Player.delete(player)


extensions: List[str] = BotUtil.get_available_extensions()

for extension in extensions:
    loaded_extensions = bot.extensions.keys()

    if extension not in loaded_extensions:
        bot.load_extension(extension)
        print(f'Loaded extension {extension}')

bot.run(config.bot_secret)


async def close_connections():
    await Tortoise.close_connections()


run_async(close_connections())
