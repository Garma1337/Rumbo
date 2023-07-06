# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, Option, slash_command, Cog, Bot
from discord.utils import basic_autocomplete

from commands.autocomplete import AutoCompletion
from db.models.player import Player
from lib.managers.playermanager import PlayerManager


class SetFlagCommand(Cog):

    @slash_command(name='set_flag', description='Set your country flag.')
    async def set_flag(
            self,
            context: ApplicationContext,
            region: Option(choices=AutoCompletion.get_regions()),
            flag: Option(autocomplete=basic_autocomplete(AutoCompletion.get_flags))
    ) -> NoReturn:
        await context.defer()

        player: Player = await Player.find_or_create(context.user.id)

        try:
            await PlayerManager.set_flag(player, flag)
            await context.respond(f'Your flag has been set to {flag}.')
        except ValueError as e:
            await context.respond(e)
            return


def setup(bot: Bot):
    bot.add_cog(SetFlagCommand())
