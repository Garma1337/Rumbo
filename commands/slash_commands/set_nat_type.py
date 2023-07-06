# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, Option, slash_command, Cog, Bot

from commands.autocomplete import AutoCompletion
from db.models.player import Player
from lib.managers.playermanager import PlayerManager


class SetNatTypeCommand(Cog):

    @slash_command(name='set_nat_type', description='Set your NAT type.')
    async def set_nat_type(
            self,
            context: ApplicationContext,
            nat_type: Option(choices=AutoCompletion.get_nat_types())
    ) -> NoReturn:
        await context.defer()

        player: Player = await Player.find_or_create(context.user.id)

        try:
            await PlayerManager.set_nat_type(player, nat_type)
            await context.respond(f'Your NAT type has been set to {nat_type}.')
        except ValueError as e:
            await context.respond(e)
            return


def setup(bot: Bot):
    bot.add_cog(SetNatTypeCommand())
