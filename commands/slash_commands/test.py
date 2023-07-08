# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, slash_command, default_permissions, Cog, Bot

from db.models.team import Team
from utils.text_channel import TextChannelUtil


class TestCommand(Cog):

    @slash_command(name='test', description='Test stuff.')
    @default_permissions(administrator=True)
    async def test(self, context: ApplicationContext) -> NoReturn:
        await context.defer()

        await TextChannelUtil.send_primary(context.channel, 'testing alert')
        await TextChannelUtil.send_info(context.channel, 'testing alert')
        await TextChannelUtil.send_success(context.channel, 'testing alert')
        await TextChannelUtil.send_warning(context.channel, 'testing alert')
        await TextChannelUtil.send_error(context.channel, 'testing alert')


def setup(bot: Bot):
    bot.add_cog(TestCommand())
