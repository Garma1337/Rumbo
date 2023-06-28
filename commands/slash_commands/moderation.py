# coding: utf-8

from typing import List, NoReturn

import discord

from commands.cog_base import CogBase


class Moderation(CogBase):
    """
    Moderation commands.
    """

    @discord.slash_command(name='purge', description='Remove X amount of messages from the current channel')
    @discord.default_permissions(manage_messages=True)
    async def purge(self, context: discord.ApplicationContext, num_messages: discord.Option(int)) -> NoReturn:
        """
        Purge command.
        :param context:
        :param num_messages:
        :return:
        """
        await context.defer()

        max_purge_messages: int = 500

        if num_messages > max_purge_messages:
            await context.respond(f'The maximum number of messages that can be deleted is {max_purge_messages}.')
            return

        history: List[discord.Message] = await context.channel.history(limit=num_messages).flatten()
        await context.respond(f'Deleting {len(history)} messages ...')

        for message in history:
            await message.delete()

        await context.respond(f'{len(history)} messages were successfully deleted.')


def setup(bot: discord.Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Moderation(bot))
