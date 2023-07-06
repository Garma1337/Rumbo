# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, Option, slash_command, Cog, Bot

from commands.autocomplete import AutoCompletion
from db.models.player import Player
from lib.managers.playermanager import PlayerManager


class SetConsoleCommand(Cog):

    @slash_command(name='set_console', description='Set your console.')
    async def set_console(
            self,
            context: ApplicationContext,
            console: Option(choices=AutoCompletion.get_consoles())
    ) -> NoReturn:
        await context.defer()

        player: Player = await Player.find_or_create(context.user.id)

        try:
            await PlayerManager.set_console(player, console)
            await context.respond(f'Your console has been set to {console}.')
        except ValueError as e:
            await context.respond(e)
            return


def setup(bot: Bot):
    bot.add_cog(SetConsoleCommand())
