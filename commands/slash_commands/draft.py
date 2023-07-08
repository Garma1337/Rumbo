# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, SlashCommandOptionType, slash_command, Cog, Bot

from commands.draft import draft


class DraftCommand(Cog):

    @slash_command(name='draft', description='Map drafting between 2 players.')
    async def draft(self, context: ApplicationContext, opponent: SlashCommandOptionType.mentionable) -> NoReturn:
        await context.defer()
        await draft(context.channel, context.user, opponent)


def setup(bot: Bot):
    bot.add_cog(DraftCommand())
