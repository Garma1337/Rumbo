# coding: utf-8

from typing import NoReturn

import discord
from discord import TextChannel

from commands.cog_base import CogBase
from db.models.lobby import Lobby
from db.models.player import Player
from db.models.team import Team
from lib.lobbymanager import LobbyManager
from lib.teammanager import TeamManager
from utils.guild import GuildUtil
from utils.member import MemberUtil
from utils.text_channel import ChannelNames


class LobbyButtons(discord.ui.View):

    @discord.ui.button(label='Join', style=discord.ButtonStyle.blurple, emoji='✅')
    async def join(self, button: discord.Button, interaction: discord.Interaction) -> NoReturn:
        """
        Join a lobby.
        :param button:
        :param interaction:
        """
        await interaction.response.defer()

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        lobby_channel: TextChannel = GuildUtil.find_channel(interaction.guild, ChannelNames.LobbyChannel.value)

        if lobby.started:
            await lobby_channel.send(f'<@{interaction.user.id}>, you cannot join this lobby because it has already '
                                     f'started.')
            return

        player: Player = await Player.find_or_create(str(interaction.user.id))
        team: Team = await TeamManager.find_team_by_player(player)

        if not team:
            await lobby_channel.send(f'<@{interaction.user.id}>, you cannot join this lobby because you are not part '
                                     f'of a team.')
            return

        lobby.teams.add(team)
        await lobby.save()

    @discord.ui.button(label='Leave', style=discord.ButtonStyle.primary, emoji='❌')
    async def leave(self, button: discord.Button, interaction: discord.Interaction) -> NoReturn:
        """
        Leave a lobby.
        :param button:
        :param interaction:
        """
        await interaction.response.defer()

        player: Player = await Player.find_or_create(str(interaction.user.id))
        team: Team = await TeamManager.find_team_by_player(player)

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        lobby.teams.remove(team)
        await lobby.save()

    @discord.ui.button(label='Delete', style=discord.ButtonStyle.primary, emoji='')
    async def delete(self, button: discord.Button, interaction: discord.Interaction) -> NoReturn:
        """
        Delete a lobby.
        :param button:
        :param interaction:
        """
        await interaction.response.defer()

        lobby: Lobby = await Lobby.filter(
            guild=interaction.guild.id,
            channel=interaction.channel.id,
            message=interaction.message.id
        ).first()

        if not lobby.started and interaction.user.id == lobby.creator.discord_id:
            await lobby.delete()
            await interaction.message.delete()
            return

        is_team: bool = MemberUtil.is_team(interaction.user)
        if lobby.started and is_team:
            await lobby.delete()
            await interaction.message.delete()
            return


class LobbyCog(CogBase):
    """
    Lobby commands cog.
    """

    @discord.slash_command(name='lobby', description='Create a new lobby.')
    async def lobby(self, context: discord.ApplicationContext) -> NoReturn:
        """
        lobby command.
        :param context:
        """
        await context.defer()

        matches_channel: TextChannel = GuildUtil.find_channel(context.guild, ChannelNames.MatchesChannel.value)
        message: discord.Message = await matches_channel.send('...')

        creator: Player = await Player.find_or_create(str(context.user.id))

        lobby: Lobby = await Lobby.create(
            creator=creator,
            tracks='',
            guild=context.guild.id,
            channel=context.channel.id,
            message=message.id,
            started=0
        )

        embed: discord.Embed = await LobbyManager.get_embed(lobby)
        await message.edit(content=None, embed=embed, view=LobbyButtons())

        await context.respond('Your lobby was successfully created.')

    @discord.slash_command(name='end_lobby', description='End your lobby.')
    async def end_lobby(self, context: discord.ApplicationContext) -> NoReturn:
        """
        end_lobby command.
        :param context:
        """
        await context.defer()
        await context.respond('Not implemented yet.')


def setup(bot: discord.Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(LobbyCog(bot))
