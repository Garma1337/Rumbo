# coding: utf-8

from enum import Enum
from typing import List

from discord import Member, TextChannel, Message, Embed

from commands.coinflip import CoinflipResult, coinflip
from lib.services import config
from lib.views.map_selection_view import MapSelectionView


class DraftAction(Enum):
    Ban = 'ban'
    Pick = 'pick'


class DraftedMap(object):

    def __init__(self, map_name: str, picking_player: Member, action: DraftAction):
        self.map_name = map_name
        self.picking_player = picking_player
        self.action = action


class DraftResult(object):

    def __init__(self, drafted_maps: List[DraftedMap]):
        self.drafted_maps = drafted_maps


def get_embed(picked_maps: List[DraftedMap]) -> Embed:
    picked_map_list: str = ''
    map_index: int = 1

    for picked_map in picked_maps:
        picked_map_list += f'{map_index}. {picked_map.map_name} (<@{picked_map.picking_player.id}>)\n'
        map_index += 1

    players: set[Member] = set([picked_map.picking_player for picked_map in picked_maps])

    draft_embed: Embed = Embed(
        title='Draft',
        description=f'The players doing the draft were {", ".join([f"<@{player.id}>" for player in players])}',
        colour=config.default_embed_color
    )
    draft_embed.add_field(name='Banned Maps', value='-')
    draft_embed.add_field(name='Picked Maps', value=picked_map_list)

    return draft_embed


async def draft(channel: TextChannel, player1: Member, player2: Member, map_count: int = 5) -> DraftResult:
    starting_player: Member = player1
    second_player: Member = player2

    odd_map_count: bool = map_count % 2 > 0

    if odd_map_count:
        await channel.send('The number of maps is uneven. The first picker will be decided by a coinflip.')

        coinflip_result: CoinflipResult = await coinflip(channel, player1)

        if coinflip_result.random_side != coinflip_result.selected_side:
            starting_player = player2
            second_player = player1

    drafted_maps: List[DraftedMap] = []

    for x in range(1, map_count + 1):
        if odd_map_count:
            if x % 2 == 1:
                picking_player: Member = starting_player
            else:
                picking_player: Member = second_player
        else:
            if x % 4 in [0, 1]:
                picking_player: Member = starting_player
            else:
                picking_player: Member = second_player

        map_selection_view: MapSelectionView = MapSelectionView(picking_player)
        message: Message = await channel.send(
            f'<@{picking_player.id}>, it is your turn to pick!',
            view=map_selection_view
        )

        await map_selection_view.wait()

        await channel.send(f'<@{picking_player.id}> picked {map_selection_view.picked_map}!')
        await message.delete()

        drafted_maps.append(DraftedMap(map_selection_view.picked_map, picking_player, DraftAction.Pick))

    draft_embed: Embed = get_embed(drafted_maps)
    await channel.send(embed=draft_embed)

    return DraftResult(drafted_maps)

