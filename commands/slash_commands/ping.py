# coding: utf-8

from typing import List, NoReturn

from discord import ApplicationContext, Embed, slash_command, Cog, Bot

from _started import bot_started
from lib.carbon import Carbon
from lib.services import config, bot


class PingCommand(Cog):

    @slash_command(name='ping', description='Ping the bot.')
    async def ping(self, context: ApplicationContext) -> NoReturn:
        await context.defer()

        ping_embed: Embed = Embed(
            colour=config.default_embed_color
        )

        statistics: List[str] = [
            f'**Latency**: {round(bot.latency, 3)} seconds',
            f'**Uptime**: {Carbon.getCurrentTimestamp() - bot_started} seconds'
        ]

        ping_embed.add_field(
            name='**Statistics**',
            value='\n'.join(statistics),
            inline=False
        )

        await context.respond('Success!', embed=ping_embed)


def setup(bot: Bot):
    bot.add_cog(PingCommand())
