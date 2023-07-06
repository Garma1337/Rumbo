# coding: utf-8

from discord import TextChannel, ApplicationContext
from discord.ui import Modal

from lib.modals.post_message_modal import PostMessageModal


async def post_as_rumbo(context: ApplicationContext, channel: TextChannel):
    """
    Sends a message as Rumbo.
    """
    post_message_modal: Modal = PostMessageModal(title='Send message')
    await context.send_modal(post_message_modal)
    await post_message_modal.wait()

    await channel.send(post_message_modal.message)
