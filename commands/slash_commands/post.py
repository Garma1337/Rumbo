# coding: utf-8

from typing import NoReturn

from discord import slash_command, ApplicationContext, SlashCommandOptionType, default_permissions, Cog, Bot

from commands.post import post_as_rumbo


class PostCommand(Cog):

    @slash_command(name='post', description='Send a message as Rumbo.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def post(self, context: ApplicationContext, channel: SlashCommandOptionType.channel) -> NoReturn:
        await context.defer()
        await post_as_rumbo(context, channel)


def setup(bot: Bot):
    bot.add_cog(PostCommand())
