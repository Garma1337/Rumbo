# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, SlashCommandOptionType, Embed, slash_command, Cog, Bot

from db.models.player import Player
from lib.managers.playermanager import PlayerManager, PlayerProfile


class ProfileCommand(Cog):

    @slash_command(name='profile', description='Show your profile.')
    async def profile(self, context: ApplicationContext, user: SlashCommandOptionType.mentionable = None) -> NoReturn:
        await context.defer()

        if not user:
            user_id = context.user.id
        else:
            user_id = user.id

        player: Player = await Player.find_or_create(user_id)
        player_profile: PlayerProfile = await PlayerManager.get_profile(player)

        if context.user.avatar:
            avatar_url = context.user.avatar.url
        else:
            avatar_url = context.user.default_avatar.url

        player_profile_embed: Embed = player_profile.get_embed(
            context.user.display_name,
            context.user.joined_at,
            context.user.bot,
            avatar_url
        )

        await context.respond(embed=player_profile_embed)


def setup(bot: Bot):
    bot.add_cog(ProfileCommand())
