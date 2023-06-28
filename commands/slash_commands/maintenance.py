# coding: utf-8

from typing import List, NoReturn

import discord

from bot import bot_started
from commands.cog_base import CogBase
from lib.carbon import Carbon
from lib.config import Config
from utils.text_channel import TextChannelUtil


class Maintenance(CogBase):
    """
    Maintenance commands.
    """

    @discord.slash_command(name='ping', description='Ping the bot.')
    async def ping(self, context: discord.ApplicationContext) -> NoReturn:
        """
        Ping command.
        :param context:
        """
        await context.defer()

        config: Config = Config.from_file()

        ping_embed = discord.Embed(
            colour=config.default_embed_color
        )

        statistics: List[str] = [
            f'**Latency**: {round(self.bot.latency, 3)} seconds',
            f'**Uptime**: {Carbon.getCurrentTimestamp() - bot_started} seconds'
        ]

        ping_embed.add_field(
            name='**Statistics**',
            value='\n'.join(statistics),
            inline=False
        )

        await context.respond('Success!', embed=ping_embed)

    @discord.slash_command(name='test', description='Test stuff.')
    @discord.default_permissions(administrator=True)
    async def test(self, context: discord.ApplicationContext) -> NoReturn:
        """
        test commands.
        :param context:
        :return:
        """
        await context.defer()

        await TextChannelUtil.send_primary(context.channel, 'testing alert')
        await TextChannelUtil.send_info(context.channel, 'testing alert')
        await TextChannelUtil.send_success(context.channel, 'testing alert')
        await TextChannelUtil.send_warning(context.channel, 'testing alert')
        await TextChannelUtil.send_error(context.channel, 'testing alert')


def setup(bot: discord.Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Maintenance(bot))
