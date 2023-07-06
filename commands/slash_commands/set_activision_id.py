# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, Option, slash_command, Cog, Bot

from db.models.player import Player
from lib.managers.playermanager import PlayerManager


class SetActivisionIdCommand(Cog):

    @slash_command(name='set_activision_id', description='Set your activision ID.')
    async def set_activision_id(self, context: ApplicationContext, activision_id: Option()) -> NoReturn:
        await context.defer()

        player: Player = await Player.find_or_create(context.user.id)
        await PlayerManager.set_activision_id(player, activision_id)

        await context.respond(f'Your activision ID has been set to {activision_id}.')


def setup(bot: Bot):
    bot.add_cog(SetActivisionIdCommand())
