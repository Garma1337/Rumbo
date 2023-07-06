# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, Member, user_command, Bot, Cog

from commands.draft import draft


class UserDraftCommand(Cog):

    @user_command(name='Start Draft')
    async def draft(self, context: ApplicationContext, member: Member) -> NoReturn:
        await context.defer()
        await draft(context.channel, context.user, member)


def setup(bot: Bot):
    bot.add_cog(UserDraftCommand())
