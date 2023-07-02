# coding: utf-8

from typing import NoReturn, List, Any

import discord
from discord import Member, Cog

from lib.services import logger


class CogBase(Cog):
    """
    Base class for cogs.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @staticmethod
    def log_command_usage(command_name: str, user: Member, params: List[Any] | None = None) -> NoReturn:
        """
        Logs the usage of a command.
        :param command_name:
        :param user:
        :param params:
        """
        if params is None:
            logger.info(f'/{command_name} command used by {user.id}')
        else:
            logger.info(f'/{command_name} command used by {user.id} with params [{", ".join(params)}]')
