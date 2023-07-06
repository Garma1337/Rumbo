# coding: utf-8

from typing import List, NoReturn

from discord import SelectOption, Member, Interaction
from discord.ui import View, Select, select

from lib.db import DbUtil

playable_maps: List[SelectOption] = [SelectOption(label=map['name']) for map in DbUtil.get_maps() if map['playable']]


class MapSelectionView(View):

    def __init__(self, picking_player: Member):
        super().__init__(timeout=60)
        self.picking_player = picking_player
        self.picked_map = None

    @select(placeholder='Choose a map', options=playable_maps)
    async def callback(self, select_menu: Select, interaction: Interaction) -> NoReturn:
        await interaction.response.defer()

        if interaction.user.id != self.picking_player.id:
            return

        self.picked_map = select_menu.values[0]
        self.stop()
