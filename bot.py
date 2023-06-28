# coding: utf-8

from typing import List

import discord
from discord import TextChannel
from tortoise import run_async

from db.init import init
from db.models.player import Player
from lib.carbon import Carbon
from lib.config import Config
from utils.activity import ActivityUtil
from utils.guild import GuildUtil
from utils.text_channel import ChannelNames

bot = discord.Bot(intents=discord.Intents.all())
bot_started = Carbon.getCurrentTimestamp()

run_async(init())

config = Config.from_file()


@bot.event
async def on_ready():
    """
    Executes eventhandlers when the bot is ready.
    """
    print(f'{bot.user} is ready and online!')


@bot.event
async def on_member_join(member: discord.Member):
    """
    Executes eventhandlers when a member joins.
    :param member:
    """
    await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.')
    await Player.create(discord_id=member.id)


@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    """
    Executes eventhandlers when a member's presence is updated
    :param before:
    :param after:
    """
    if not ActivityUtil.is_crash_team_rumble_stream(before.activity) and ActivityUtil.is_crash_team_rumble_stream(
            after.activity):
        stream_channel: TextChannel = GuildUtil.find_channel(before.guild, ChannelNames.LiveStreamsChannel.value)

        if stream_channel:
            await stream_channel.send(f'<@{before.id}> is now streaming!')


extensions: List[str] = [
    'lobby',
    'maintenance',
    'moderation',
    'profile',
    'social'
]

for extension in extensions:
    bot.load_extension(f'commands.slash_commands.{extension}')

bot.run(config.bot_secret)
