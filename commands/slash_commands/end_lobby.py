# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, slash_command, Cog, Bot


class EndLobbyCommand(Cog):

    @slash_command(name='end_lobby', description='End your lobby.')
    async def end_lobby(self, context: ApplicationContext) -> NoReturn:
        await context.defer()
        await context.respond('Not implemented yet.')


def setup(bot: Bot):
    bot.add_cog(EndLobbyCommand())
