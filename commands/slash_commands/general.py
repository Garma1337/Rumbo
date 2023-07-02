# coding: utf-8

from typing import List, NoReturn

from discord import ApplicationContext, Embed, Bot, slash_command, default_permissions

from _started import bot_started
from commands.cog_base import CogBase
from lib.carbon import Carbon
from lib.services import config
from utils.text_channel import TextChannelUtil


class General(CogBase):
    """
    General commands.
    """

    @slash_command(name='ping', description='Ping the bot.')
    async def ping(self, context: ApplicationContext) -> NoReturn:
        """
        Ping command.
        :param context:
        """
        await context.defer()

        CogBase.log_command_usage('ping', context.user)

        ping_embed: Embed = Embed(
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

    @slash_command(name='test', description='Test stuff.')
    @default_permissions(administrator=True)
    async def test(self, context: ApplicationContext) -> NoReturn:
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


def setup(bot: Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(General(bot))
