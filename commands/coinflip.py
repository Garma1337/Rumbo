# coding: utf-8

import random
from enum import Enum
from typing import NoReturn, List

from discord import SelectOption, Interaction, Member, TextChannel
from discord.ui import View, select, Select


class CoinflipSide(Enum):
    Heads = 'Heads'
    Tails = 'Tails'
    Upright = 'Upright'


all_coinflip_sides = [CoinflipSide.Heads.value, CoinflipSide.Tails.value, CoinflipSide.Upright.value]


class CoinflipResult(object):

    def __init__(self, member: Member, random_side: str, selected_side: str):
        self.member = member
        self.random_side = random_side
        self.selected_side = selected_side


class CoinflipView(View):

    def __init__(self, member: Member):
        super().__init__(timeout=60)
        self.member = member
        self.selected_side = None

    @select(placeholder='Choose a map', options=[SelectOption(label=side) for side in all_coinflip_sides])
    async def callback(self, select_menu: Select, interaction: Interaction) -> NoReturn:
        if interaction.user.id != self.member.id:
            await interaction.response.defer()
            return

        select_menu.disabled = True
        await interaction.response.edit_message(view=self)

        self.selected_side = select_menu.values[0]
        self.stop()


async def coinflip(channel: TextChannel, member: Member) -> CoinflipResult:
    options: List[str] = all_coinflip_sides
    weights: List[float] = [0.495, 0.495, 0.01]

    random_side: str = random.choices(options, weights=weights)

    coinflip_view: CoinflipView = CoinflipView(member)
    await channel.send('I just flipped a coin. On which side did it land?', view=CoinflipView(member))
    await coinflip_view.wait()

    selected_side: str = coinflip_view.selected_side
    return CoinflipResult(member, random_side, selected_side)
