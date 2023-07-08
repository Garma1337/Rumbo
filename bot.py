# coding: utf-8

from typing import List

import discord.utils
from discord import TextChannel, Member, Message, ChannelType, Role
from tortoise import run_async, Tortoise

from db.init import init
from db.models.player import Player
from lib.services import config, logger, bot
from lib.views.lobby_buttons_view import LobbyButtonsView
from utils.activity import ActivityUtil
from utils.bot import BotUtil
from utils.member import MemberUtil, RoleNames
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
async def on_member_update(before: Member, after: Member):
    muted_role: Role | None = discord.utils.get(after.guild.roles, name=RoleNames.MutedRole.value)
    if not muted_role:
        return

    if not before.timed_out and after.timed_out:
        if not after.get_role(muted_role.id):
            await after.add_roles([muted_role], reason='Timed out')

    if before.timed_out and not after.timed_out:
        if after.get_role(muted_role.id):
            await after.remove_roles([muted_role], reason='Timeout expired')


@bot.event
async def on_message(message: Message):
    if message.author.id == bot.user.id:
        return

    if message.channel.type == ChannelType.private:
        await BotUtil.log_dm(message)


@bot.event
async def on_presence_update(before: Member, after: Member):
    live_role: Role | None = discord.utils.get(after.guild.roles, name=RoleNames.LiveRole.value)

    if not ActivityUtil.is_ctr_stream(before.activity) and ActivityUtil.is_ctr_stream(after.activity):
        stream_channel: TextChannel | None = discord.utils.get(
            before.guild.channels,
            name=ChannelNames.LiveStreamsChannel.value
        )

        if stream_channel:
            await stream_channel.send(f'<@{before.id}> is now streaming!')

        if live_role and not after.get_role(live_role.id):
            await after.add_roles([live_role], reason='User went live')

    if ActivityUtil.is_ctr_stream(before.activity) and not ActivityUtil.is_ctr_stream(after.activity):
        if live_role and after.get_role(live_role.id):
            await after.remove_roles([live_role], reason='User went offline')


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
        logger.info(f'Loaded extension {extension}')

bot.run(config.bot_secret)


async def close_connections():
    await Tortoise.close_connections()


run_async(close_connections())
