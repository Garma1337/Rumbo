# coding: utf-8

from typing import NoReturn

from discord import TextChannel, ButtonStyle, Button, Interaction, ApplicationContext, Option, Bot, Embed, \
    slash_command, Message
from discord.ui import View, button

from commands.autocomplete import AutoCompletion
from commands.cog_base import CogBase
from db.models.lobby import Lobby
from db.models.player import Player
from lib.lobbymanager import LobbyManager
from utils.guild import GuildUtil
from utils.member import MemberUtil
from utils.text_channel import ChannelNames


class LobbyButtons(View):

    @button(label='Join', style=ButtonStyle.blurple, emoji='✅')
    async def join(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
        """
        Join a lobby.
        :param clicked_button:
        :param interaction:
        """
        await interaction.response.defer()

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        if not lobby:
            return

        lobby_channel: TextChannel = GuildUtil.find_channel_by_name(interaction.guild, ChannelNames.LobbyChannel.value)

        if lobby.started:
            await lobby_channel.send(f'<@{interaction.user.id}>, you cannot join this lobby because it has already '
                                     f'started.')
            return

        player: Player = await Player.find_or_create(interaction.user.id)

        await LobbyManager.add_player_to_lobby(lobby, player)
        await LobbyManager.update_message(lobby)

    @button(label='Leave', emoji='❌')
    async def leave(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
        """
        Leave a lobby.
        :param clicked_button:
        :param interaction:
        """
        await interaction.response.defer()

        player: Player = await Player.find_or_create(interaction.user.id)

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        lobby_channel: TextChannel = GuildUtil.find_channel_by_name(interaction.guild, ChannelNames.LobbyChannel.value)

        if lobby.started:
            await lobby_channel.send(f'<@{interaction.user.id}>, you cannot leave this lobby because it has already '
                                     f'started.')
            return

        await LobbyManager.remove_player_from_lobby(lobby, player)
        await LobbyManager.update_message(lobby)

    @button(label='Delete', emoji='🗑️')
    async def delete(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
        """
        Delete a lobby.
        :param clicked_button:
        :param interaction:
        """
        await interaction.response.defer()

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        if not lobby.started and interaction.user.id == lobby.creator.discord_id:
            await LobbyManager.end_lobby(lobby)
            return

        is_team: bool = MemberUtil.is_team(interaction.user)
        if lobby.started and is_team:
            await LobbyManager.end_lobby(lobby)
            return


class LobbyCog(CogBase):
    """
    Lobby commands cog.
    """

    @slash_command(name='lobby', description='Create a new lobby.')
    async def lobby(
            self,
            context: ApplicationContext,
            insta: Option(bool, required=False, default=False),
            region_lock: Option(required=False, default=None, choices=AutoCompletion.get_regions())
    ) -> NoReturn:
        """
        Lobby command.
        :param context:
        :param insta:
        :param region_lock:
        """
        await context.defer()

        CogBase.log_command_usage('lobby', context.user, [insta, region_lock])

        matches_channel: TextChannel = GuildUtil.find_channel_by_name(context.guild, ChannelNames.MatchesChannel.value)
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
        await message.edit(content=None, embed=embed, view=LobbyButtons())

        await context.respond('Your lobby was successfully created.')

    @slash_command(name='end_lobby', description='End your lobby.')
    async def end_lobby(self, context: ApplicationContext) -> NoReturn:
        """
        end_lobby command.
        :param context:
        """
        await context.defer()

        CogBase.log_command_usage('end_lobby', context.user)

        await context.respond('Not implemented yet.')


def setup(bot: Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(LobbyCog(bot))
