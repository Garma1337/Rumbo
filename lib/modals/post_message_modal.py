# coding: utf-8

from typing import NoReturn

from discord import InputText, InputTextStyle, Interaction
from discord.ui import Modal


class PostMessageModal(Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.message = None
        self.add_item(InputText(label='Message', style=InputTextStyle.long))

    async def callback(self, interaction: Interaction) -> NoReturn:
        self.message = self.children[0].value
        await interaction.response.defer()
        self.stop()
