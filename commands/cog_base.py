# coding: utf-8

import discord
from discord.ext import commands


class CogBase(commands.Cog):
    """
    Base class for cogs.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot
