# coding: utf-8
from typing import NoReturn

import discord

from commands.autocomplete import AutoCompletion
from commands.cog_base import CogBase
from db.models.player import Player
from lib.playermanager import PlayerManager, PlayerProfile


class Profile(CogBase):
    """
    Profile commands cog.
    """

    @discord.slash_command(name='profile', description='Show your profile.')
    async def show(self, context: discord.ApplicationContext, user: discord.SlashCommandOptionType.mentionable = None) -> NoReturn:
        """
        Profile command.
        :param user:
        :param context:
        """
        await context.defer()

        if not user:
            user_id = context.user.id
        else:
            user_id = user.id

        player: Player = await Player.find_or_create(str(user_id))
        profile: PlayerProfile = await PlayerManager.get_profile(player)

        if context.user.avatar:
            avatar_url = context.user.avatar.url
        else:
            avatar_url = context.user.default_avatar.url

        embed: discord.Embed = profile.get_embed(
            context.user.display_name,
            context.user.joined_at,
            context.user.bot,
            avatar_url
        )

        await context.respond(embed=embed)

    @discord.slash_command(name='set_activision_id', description='Set your activision ID.')
    async def set_activision_id(self, context: discord.ApplicationContext, activision_id: discord.Option()) -> NoReturn:
        """
        set_activision_id command.
        :param context:
        :param activision_id:
        """
        await context.defer()

        player: Player = await Player.find_or_create(str(context.user.id))
        await PlayerManager.set_activision_id(player, activision_id)

        await context.respond(f'Your activision ID has been set to {activision_id}.')

    @discord.slash_command(name='set_flag', description='Set your country flag.')
    async def set_flag(
            self,
            context: discord.ApplicationContext,
            region: discord.Option(choices=AutoCompletion.get_regions()),
            flag: discord.Option(autocomplete=discord.utils.basic_autocomplete(AutoCompletion.get_flags))) -> NoReturn:
        """
        set_flag command.
        :param context:
        :param region:
        :param flag:
        :return:
        """
        await context.defer()

        player: Player = await Player.find_or_create(str(context.user.id))

        try:
            await PlayerManager.set_flag(player, flag)
            await context.respond(f'Your flag has been set to {flag}.')
        except ValueError as e:
            await context.respond(e)
            return

    @discord.slash_command(name='set_nat_type', description='Set your NAT type.')
    async def set_nat_type(
            self,
            context: discord.ApplicationContext,
            nat_type: discord.Option(choices=AutoCompletion.get_nat_types())) -> NoReturn:
        """
        set_nat_type command.
        :param context:
        :param nat_type:
        :return:
        """
        await context.defer()

        player: Player = await Player.find_or_create(str(context.user.id))

        try:
            await PlayerManager.set_nat_type(player, nat_type)
            await context.respond(f'Your NAT type has been set to {nat_type}.')
        except ValueError as e:
            await context.respond(e)
            return

    @discord.slash_command(name='set_console', description='Set your console.')
    async def set_console(
            self,
            context: discord.ApplicationContext,
            console: discord.Option(choices=AutoCompletion.get_consoles())) -> NoReturn:
        """
        set_console command.
        :param context:
        :param console:
        :return:
        """
        await context.defer()

        player: Player = await Player.find_or_create(str(context.user.id))

        try:
            await PlayerManager.set_console(player, console)
            await context.respond(f'Your console has been set to {console}.')
        except ValueError as e:
            await context.respond(e)
            return


def setup(bot: discord.Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Profile(bot))
