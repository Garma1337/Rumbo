# coding: utf-8

from typing import NoReturn

import discord.utils
from discord import TextChannel, ApplicationContext, Option, Embed, slash_command, Message, Cog, Bot

from commands.autocomplete import AutoCompletion
from db.models.lobby import Lobby
from db.models.player import Player
from lib.managers.lobbymanager import LobbyManager
from lib.views.lobby_buttons_view import LobbyButtonsView
from utils.text_channel import ChannelNames


class LobbyCommand(Cog):

    @slash_command(name='lobby', description='Create a new lobby.')
    async def lobby(
            self,
            context: ApplicationContext,
            insta: Option(bool, required=False, default=False),
            region_lock: Option(required=False, default=None, choices=AutoCompletion.get_regions())
    ) -> NoReturn:
        await context.defer()

        matches_channel: TextChannel | None = discord.utils.get(
            context.guild.channels,
            name=ChannelNames.MatchesChannel.value
        )

        if not matches_channel:
            await context.respond('The matches channel does not exist. You cannot create a lobby.')
            return

        message: Message = await matches_channel.send('...')
        creator: Player = await Player.find_or_create(context.user.id)

        lobby: Lobby = await Lobby.create(
            creator=creator,
            tracks='',
            guild=context.guild.id,
            channel=matches_channel.id,
            message=message.id,
            started=0,
            insta=insta,
            region_lock=region_lock
        )

        embed: Embed = await LobbyManager.get_embed(lobby)
        await message.edit(content=None, embed=embed, view=LobbyButtonsView())

        await context.respond('Your lobby was successfully created.')


def setup(bot: Bot):
    bot.add_cog(LobbyCommand())
