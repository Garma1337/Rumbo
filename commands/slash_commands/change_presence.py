# coding: utf-8

from typing import NoReturn

from discord import slash_command, ApplicationContext, default_permissions, Option, ActivityType, Activity, Cog, Bot

from commands.autocomplete import AutoCompletion
from lib.services import bot


class ChangePresenceCommand(Cog):

    @slash_command(name='change_presence', description='Change Rumbo\'s presence.')
    @default_permissions(manage_channels=True)
    @default_permissions(manage_messages=True)
    async def change_presence(
            self,
            context: ApplicationContext,
            activity_type: Option(choices=AutoCompletion.get_activity_types()),
            status: Option()
    ) -> NoReturn:
        await context.defer()

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

        await bot.change_presence(activity=Activity(type=activity_id, name=status))
        await context.respond('Rumbo\'s presence has been changed.')


def setup(bot: Bot):
    bot.add_cog(ChangePresenceCommand())
