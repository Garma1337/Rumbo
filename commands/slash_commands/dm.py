# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, default_permissions, slash_command, SlashCommandOptionType, Cog, Bot
from discord.ui import Modal

from commands.post import PostMessageModal
from utils.member import MemberUtil


class DmCommand(Cog):

    @slash_command(name='dm', description='DM a user as Rumbo.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def dm(self, context: ApplicationContext, user: SlashCommandOptionType.mentionable) -> NoReturn:
        await context.defer()

        post_message_modal: Modal = PostMessageModal(title='Send message')
        await context.send_modal(post_message_modal)
        await post_message_modal.wait()

        await MemberUtil.send_dm(user, post_message_modal.message)


def setup(bot: Bot):
    bot.add_cog(DmCommand())
