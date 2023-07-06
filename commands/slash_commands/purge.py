# coding: utf-8

from typing import List, NoReturn

from discord import ApplicationContext, Option, Message, default_permissions, slash_command, Cog, Bot


class PurgeCommand(Cog):

    @slash_command(name='purge', description='Remove X amount of messages from the current channel.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def purge(self, context: ApplicationContext, num_messages: Option(int)) -> NoReturn:
        await context.defer()

        max_purge_messages: int = 500

        if num_messages > max_purge_messages:
            await context.respond(f'The maximum number of messages that can be deleted is {max_purge_messages}.')
            return

        history: List[Message] = await context.channel.history(limit=num_messages).flatten()
        await context.respond(f'Deleting {len(history)} messages ...')

        for message in history:
            await message.delete()

        await context.respond(f'{len(history)} messages were successfully deleted.')


def setup(bot: Bot):
    bot.add_cog(PurgeCommand())
