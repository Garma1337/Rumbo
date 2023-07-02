# coding: utf-8

from typing import NoReturn

from discord import slash_command, ApplicationContext, InputTextStyle, Interaction, SlashCommandOptionType, Bot, \
    default_permissions, Option, ActivityType, Activity
from discord.ui import Modal, InputText

from commands.autocomplete import AutoCompletion
from commands.cog_base import CogBase


class PostMessageModal(Modal):
    """
    Modal to post a message.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.message = None
        self.add_item(InputText(label='Message', style=InputTextStyle.long))

    async def callback(self, interaction: Interaction) -> NoReturn:
        self.message = self.children[0].value
        await interaction.response.defer()
        self.stop()


class Admin(CogBase):
    """
    Various administrative functions to manage Rumbo.
    """

    @slash_command(name='change_presence', description='Change Rumbo\'s presence.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def change_presence(
            self,
            context: ApplicationContext,
            activity_type: Option(choices=AutoCompletion.get_activity_types()),
            status: Option()
    ) -> NoReturn:
        """
        Change Rumbo's presence.
        :param context:
        :param activity_type:
        :param status:
        """
        await context.defer()

        CogBase.log_command_usage('change_presence', context.user, [activity_type, status])

        id_mapping: dict[str, int] = {
            ActivityType.playing.name: ActivityType.playing,
            ActivityType.listening.name: ActivityType.listening,
            ActivityType.watching.name: ActivityType.watching,
        }

        activity_id: int | None = None
        if activity_type in id_mapping:
            activity_id = id_mapping[activity_type]

        if not activity_id:
            await context.respond('You did not specify a valid activity.')
            return

        await self.bot.change_presence(activity=Activity(type=activity_id, name=status))
        await context.respond('Rumbo\'s presence has been changed.')

    @slash_command(name='post', description='Send a message as Rumbo.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def post(self, context: ApplicationContext, channel: SlashCommandOptionType.channel) -> NoReturn:
        """
        Send a message as Rumbo.
        :param context:
        :param channel:
        """
        await context.defer()

        CogBase.log_command_usage('post', context.user, [channel.id])

        post_message_modal: Modal = PostMessageModal(title='Send message')
        await context.send_modal(post_message_modal)
        await post_message_modal.wait()

        await channel.send(post_message_modal.message)


def setup(bot: Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Admin(bot))
