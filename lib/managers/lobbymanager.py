# coding: utf-8

import random
from datetime import datetime
from typing import List, NoReturn

from discord import Embed, Guild, TextChannel, Message

from db.models.lobby import Lobby
from db.models.player import Player
from db.models.team import Team
from db.repository.teamrepository import TeamRepository
from lib.db import DbUtil
from lib.services import config, bot
from utils.bot import BotUtil
from utils.guild import GuildUtil
from utils.text_channel import TextChannelUtil, ChannelNames


class LobbyManager(object):

    @staticmethod
    async def get_embed(lobby: Lobby) -> Embed:
        icon: str = 'https://i.imgur.com/dQFJiy3.png'
        players: List[Player] = await LobbyManager.get_players(lobby)
        maps: List[str] = LobbyManager.get_maps(lobby)

        embed: Embed = Embed(
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

        player_count: int = LobbyManager.get_player_count(lobby)

        if player_count > 0:
            embed.add_field(
                name=':busts_in_silhouette: **Players**',
                value=LobbyManager.get_players_text(lobby)
            )
            embed.add_field(
                name=':credit_card: **Activision ID**',
                value='\n'.join([player.activision_id for player in players])
            )

        if len(maps) > 0:
            embed.add_field(
                name=':stadium: **Maps**',
                value='\n'.join(LobbyManager.get_maps(lobby))
            )

        embed.add_field(
            name=':bust_in_silhouette: **Creator**',
            value=LobbyManager.get_player_text(lobby.creator)
        )

        return embed

    @staticmethod
    async def add_player_to_lobby(lobby: Lobby, player: Player) -> NoReturn:
        team: Team = await TeamRepository.find_one_by_player(player)
        if team:
            players: List[player] = team.players
        else:
            players: List[player] = [player]

        violations: List[str] = LobbyManager.get_join_violations(lobby, players)

        if len(violations) > 0:
            guild: Guild | None = await BotUtil.fetch_guild(bot, lobby.guild)
            lobby_channel: TextChannel | None = GuildUtil.find_channel_by_name(guild, ChannelNames.LobbyChannel.value)

            content: str = '\n'.join(violations)
            await lobby_channel.send(content)
            return

        lobby.teams.add(players)
        await lobby.save()

        if LobbyManager.get_player_count(lobby) == lobby.max_players:
            await LobbyManager.start_lobby(lobby)

    @staticmethod
    async def remove_player_from_lobby(lobby: Lobby, player: Player) -> NoReturn:
        team: Team = await TeamRepository.find_one_by_player(player)
        if team:
            players: List[player] = team.players
        else:
            players: List[player] = [player]

        lobby.teams.remove(players)
        await lobby.save()

    @staticmethod
    def get_join_violations(lobby: Lobby, players: List[Player]) -> List[str]:
        violations: List[str] = []

        for player in players:
            if not player.activision_id:
                violations.append(f'<@{player.discord_id}>, you need to set your activision ID to join this lobby.')

            if lobby.region_lock:
                if not player.region:
                    violations.append(f'<@{player.discord_id}>, you need to set your region to join this lobby.')
                else:
                    if player.region != lobby.region_lock:
                        violations.append(f'<@{player.discord_id}>, you are from a different region and cannot join '
                                          f'this lobby.')

        return violations

    @staticmethod
    async def start_lobby(lobby: Lobby) -> NoReturn:
        pass

    @staticmethod
    async def get_players(lobby: Lobby) -> List[Player]:
        teams: List[Team] = await Team.filter(lobby=lobby)

        players: List[Player] = [team.players.flat() for team in teams]
        players.extend(lobby.solo_queue)

        return players

    @staticmethod
    def get_player_count(lobby: Lobby) -> int:
        count = 0

        for team in lobby.teams:
            count += len(team.players)

        count += len(lobby.solo_queue)
        return count

    @staticmethod
    def get_maps(lobby: Lobby) -> List[str]:
        if not lobby.maps:
            return []

        maps: List[str] = str(lobby.maps).split(',')
        return maps

    @staticmethod
    def get_title(lobby: Lobby) -> str:
        if not lobby.started:
            state = 'Gathering'
        else:
            state = 'Ongoing'

        return f'{state} 4 vs. 4 lobby (random maps)'

    @staticmethod
    def get_player_text(player: Player) -> str:
        if not player.flag:
            flag = ':united_nations:'
        else:
            flag = player.flag

        return f'{flag} <@{player.discord_id}>'

    @staticmethod
    def get_players_text(lobby: Lobby) -> str:
        lines: List[str] = []

        if len(lobby.teams) > 0:
            lines.append('**Teams:**')

            team_count: int = 1
            for team in lobby.teams:
                player_count: int = 1
                lines.append(f'**Team {team_count}**')

                for player in team.players:
                    lines.append(f'{player_count}. {LobbyManager.get_player_text(player)}')
                    player_count += 1

                team_count += 1

        if len(lobby.solo_queue) > 0:
            lines.append('**Solo Queue**')

            for player in lobby.solo_queue:
                lines.append(LobbyManager.get_player_text(player))

        return '\n'.join(lines)

    @staticmethod
    async def update_message(lobby: Lobby) -> NoReturn:
        lobby_message: Message | None = await LobbyManager.get_lobby_message(lobby)

        if lobby_message:
            lobby_embed: Embed = await LobbyManager.get_embed(lobby)
            await lobby_message.edit(embed=lobby_embed)

    @staticmethod
    async def end_lobby(lobby: Lobby) -> NoReturn:
        await lobby.delete()

        lobby_message: Message | None = await LobbyManager.get_lobby_message(lobby)

        if lobby_message:
            await lobby_message.delete()

    @staticmethod
    async def get_lobby_message(lobby: Lobby) -> Message | None:
        guild: Guild | None = await BotUtil.fetch_guild(bot, lobby.guild)

        if not guild:
            return None

        channel: TextChannel = await GuildUtil.fetch_channel(guild, lobby.channel)

        if not channel:
            return None

        message: Message = await TextChannelUtil.fetch_message(channel, lobby.message)

        if not message:
            return None

        return message

    @staticmethod
    async def generate_maps(count: int) -> List[str]:
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
