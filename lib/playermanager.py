# coding: utf-8

from datetime import datetime
from typing import List, NoReturn

import discord

from db.models.player import Player
from lib.carbon import Carbon
from lib.config import Config
from lib.db import DbUtil


class PlayerProfile(object):
    """
    Player profiles.
    """

    def __init__(self, discord_id, activision_id, nat_type, country, region, console, favorite_character, favorite_map):
        self.discord_id = discord_id
        self.activision_id = activision_id
        self.nat_type = nat_type
        self.country = country
        self.region = region
        self.console = console
        self.favorite_character = favorite_character
        self.favorite_map = favorite_map

    def get_embed(self, display_name: str, joined_at: datetime, is_bot: bool, avatar_url: str) -> discord.Embed:
        """
        Returns the embed to render a player profile.
        :param display_name:
        :param joined_at:
        :param is_bot:
        :param avatar_url:
        :return:
        """
        profile_fields: List[str] = [
            f'**Activision ID**: {self.activision_id}',
            f'**NAT Type**: {self.nat_type}',
            f'**Country**: {self.country}',
            f'**Region**: {self.region}',
            f'**Joined**: {Carbon.toDateTime(joined_at)}'
        ]

        game_fields: List[str] = [
            f'**Console**: {self.console}',
            f'**Favorite Character**: {self.favorite_character}',
            f'**Favorite Map**: {self.favorite_map}',
        ]

        if is_bot:
            profile_fields.append('**Discord Bot** :robot:')

        config: Config = Config.from_file()

        embed: discord.Embed = discord.Embed(colour=config.default_embed_color)
        embed.set_footer(text=f'ID: {self.discord_id}')
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(
            name=f'{display_name}\'s profile',
            icon_url=avatar_url
        )

        embed.add_field(name=':busts_in_silhouette: Profile', value='\n'.join(profile_fields))
        embed.add_field(name=':video_game: Game Data', value='\n'.join(game_fields))

        return embed


class PlayerManager(object):
    """
    Class to manage players.
    """

    @staticmethod
    async def set_activision_id(player: Player, activision_id: str) -> NoReturn:
        """
        Set's a player's activision ID.
        :param player:
        :param activision_id:
        """
        player.activision_id = activision_id
        await player.save()

    @staticmethod
    async def set_flag(player: Player, flag: str) -> NoReturn:
        """
        Sets a player's flag.
        :param player:
        :param flag:
        """
        regions = DbUtil.get_regions()
        filtered_regions = filter(lambda r: flag in r['countries'], regions)

        if not filtered_regions:
            raise ValueError(f'Invalid flag passed as argument ({flag}).')

        region = list(filtered_regions)[0]

        player.flag = flag
        player.region = region['key']

        await player.save()

    @staticmethod
    async def set_nat_type(player: Player, nat_type: str) -> NoReturn:
        """
        Sets a player's NAT type.
        :param player:
        :param nat_type:
        """
        nat_types = DbUtil.get_nat_types()
        filtered_nat_types = filter(lambda n: n['name'] == nat_type, nat_types)

        if not filtered_nat_types:
            raise ValueError(f'Invalid NAT type passed as argument ({nat_type}')

        nat_type = list(filtered_nat_types)[0]

        player.nat = nat_type['key']
        await player.save()

    @staticmethod
    async def set_console(player: Player, console: str) -> NoReturn:
        """
        Sets a player's console.
        :param player:
        :param console:
        """
        consoles = DbUtil.get_consoles()
        filtered_consoles = filter(lambda c: c['name'] == console, consoles)

        if not filtered_consoles:
            raise ValueError(f'Invalid console passed as argument ({console}')

        console = list(filtered_consoles)[0]

        player.console = console['key']
        await player.save()

    @staticmethod
    async def get_profile(player: Player) -> PlayerProfile:
        """
        Returns data for a player's profile.
        :param player:
        :return:
        """
        nat_type = DbUtil.find_nat_type_by_key(player.nat)
        region = DbUtil.find_region_by_key(player.region)
        console = DbUtil.find_console_by_key(player.console)

        return PlayerProfile(
            player.discord_id,
            player.activision_id if player.activision_id else '-',
            nat_type['name'] if nat_type else '-',
            player.flag if player.flag else '-',
            region['name'] if region else '-',
            console['name'] if console else '-',
            player.favorite_character if player.favorite_character else '-',
            player.favorite_map if player.favorite_map else '-'
        )
