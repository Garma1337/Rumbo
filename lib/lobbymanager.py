# coding: utf-8

import random
from datetime import datetime
from typing import List

import discord

from db.models.lobby import Lobby
from db.models.player import Player
from db.models.team import Team
from lib.config import Config
from lib.db import DbUtil


class LobbyManager(object):
    """
    Lobby manager.
    """

    @staticmethod
    async def get_embed(lobby: Lobby) -> discord.Embed:
        """
        Returns the embed for the lobby.
        :param lobby:
        :return:
        """
        config: Config = Config.from_file()
        icon: str = 'https://i.imgur.com/dQFJiy3.png'
        players: List[Player] = await LobbyManager.get_players(lobby)
        maps: List[str] = LobbyManager.get_maps(lobby)

        embed: discord.Embed = discord.Embed(
            colour=config.default_embed_color,
            timestamp=datetime.now()
        )
        embed.set_footer(
            text=f'ID: {lobby.id}',
            icon_url=icon
        )
        embed.set_author(
            name=LobbyManager.get_title(lobby),
            icon_url=icon
        )

        if len(players) > 0:
            embed.add_field(
                name=':busts_in_silhouette: **Players**',
                value='\n'.join([LobbyManager.get_player_text(player) for player in players])
            )
            embed.add_field(
                name=':credit_card: **Activision ID**',
                value='\n'.join([player.activision_id for player in players])
            )

        if len(maps) > 0:
            embed.add_field(
                name=':stadium: **Maps**',
                value='\n'.join([])
            )

        embed.add_field(
            name=':bust_in_silhouette: **Creator**',
            value=LobbyManager.get_player_text(lobby.creator)
        )

        return embed

    @staticmethod
    async def get_players(lobby: Lobby) -> List[Player]:
        """
        Gets all players in a lobby.
        :param lobby:
        :return:
        """
        teams: List[Team] = await Team.filter(lobby=lobby)
        return [team.players.flat() for team in teams]

    @staticmethod
    def get_maps(lobby: Lobby) -> List[str]:
        """
        Returns the maps for a lobby.
        :param lobby:
        :return:
        """
        maps: List[str] = str(lobby.maps).split(',')
        return maps

    @staticmethod
    def get_title(lobby: Lobby) -> str:
        """
        Returns the title of a lobby.
        :param lobby:
        :return:
        """
        if not lobby.started:
            state = 'Gathering'
        else:
            state = 'Ongoing'

        return f'{state} 4 vs. 4 lobby (random maps)'

    @staticmethod
    def get_player_text(player: Player) -> str:
        """
        Returns the full display name of a player.
        :param player:
        :return:
        """
        if not player.flag:
            flag = ':united_nations:'
        else:
            flag = player.flag

        return f'{flag} <@{player.discord_id}>'

    @staticmethod
    async def find_lobby_by_player(player: Player) -> Lobby | None:
        """
        Finds a lobby for a player.
        :param player:
        """
        pass

    @staticmethod
    async def generate_maps(count: int) -> List[str]:
        """
        Generates a list of maps.
        :param count:
        :return:
        """
        generated_maps: List[str] = []

        maps = DbUtil.get_maps()
        playable_maps = list(filter(lambda m: m['playable'], maps))

        if count > len(playable_maps):
            raise ValueError('The number of maps to be generated is bigger than there are playable maps.')

        while len(playable_maps) < count:
            random_index = random.randint(0, len(playable_maps) - 1)
            random_map = playable_maps[random_index]

            generated_maps.append(random_map['name'])

        return generated_maps
