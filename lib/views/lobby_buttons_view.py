# coding: utf-8

from typing import NoReturn

from discord import TextChannel, ButtonStyle, Button, Interaction
from discord.ui import View, button

from db.models.lobby import Lobby
from db.models.player import Player
from lib.managers.lobbymanager import LobbyManager
from utils.guild import GuildUtil
from utils.member import MemberUtil
from utils.text_channel import ChannelNames


class LobbyButtonsView(View):

    def __init__(self):
        super().__init__(timeout=None)

    @button(label='Join', style=ButtonStyle.blurple, emoji='✅', custom_id='lobby_join_button')
    async def join(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
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

    @button(label='Leave', emoji='❌', custom_id='lobby_leave_button')
    async def leave(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
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

    @button(label='Delete', emoji='🗑️', custom_id='lobby_delete_button')
    async def delete(self, clicked_button: Button, interaction: Interaction) -> NoReturn:
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
