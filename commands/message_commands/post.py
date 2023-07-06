# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, default_permissions, Message, message_command, Cog, Bot

from commands.post import post_as_rumbo


class MessagePostCommand(Cog):

    @message_command(name='Post message as Rumbo')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def post(self, context: ApplicationContext, message: Message) -> NoReturn:
        await context.defer()
        await post_as_rumbo(context, message.channel)


def setup(bot: Bot):
    bot.add_cog(MessagePostCommand())
