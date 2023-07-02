# coding: utf-8

from typing import List, NoReturn

from discord import ApplicationContext, Option, Bot, Message, default_permissions, slash_command, \
    SlashCommandOptionType
from discord.ui import Modal

from commands.cog_base import CogBase
from commands.slash_commands.admin import PostMessageModal
from utils.member import MemberUtil


class Moderation(CogBase):
    """
    Moderation commands.
    """

    @slash_command(name='dm', description='DM a user as Rumbo.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def dm(self, context: ApplicationContext, user: SlashCommandOptionType.mentionable) -> NoReturn:
        """
        DM a user as Rumbo.
        :param context:
        :param user:
        """
        await context.defer()

        CogBase.log_command_usage('dm', context.user, [user.id])

        post_message_modal: Modal = PostMessageModal(title='Send message')
        await context.send_modal(post_message_modal)
        await post_message_modal.wait()

        await MemberUtil.send_dm(user, post_message_modal.message)

    @slash_command(name='purge', description='Remove X amount of messages from the current channel.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def purge(self, context: ApplicationContext, num_messages: Option(int)) -> NoReturn:
        """
        Purge command.
        :param context:
        :param num_messages:
        :return:
        """
        await context.defer()

        CogBase.log_command_usage('purge', context.user, [num_messages])

        max_purge_messages: int = 500

        if num_messages > max_purge_messages:
            await context.respond(f'The maximum number of messages that can be deleted is {max_purge_messages}.')
            return

        history: List[Message] = await context.channel.history(limit=num_messages).flatten()
        await context.respond(f'Deleting {len(history)} messages ...')

        for message in history:
            await message.delete()

        await context.respond(f'{len(history)} messages were successfully deleted.')


def setup(bot: Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Moderation(bot))
