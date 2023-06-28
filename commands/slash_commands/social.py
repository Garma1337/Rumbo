# coding: utf-8

from typing import NoReturn

import discord

from commands.cog_base import CogBase
from db.models.player import Player
from db.models.team import Team


class Social(CogBase):
    """
    Social commands.
    """

    @discord.slash_command(name='create_team', description='Create a team with 3 other players.')
    async def create_team(self,
                          context: discord.ApplicationContext,
                          player1: discord.SlashCommandOptionType.mentionable,
                          player2: discord.SlashCommandOptionType.mentionable,
                          player3: discord.SlashCommandOptionType.mentionable) -> NoReturn:
        """
        create_team command.
        :param context:
        :param player1:
        :param player2:
        :param player3:
        :return:
        """
        await context.defer()

        mentioned_players = [context.user, player1, player2, player3]

        unique_players = {}
        for mentioned_player in mentioned_players:
            unique_players[mentioned_player.id] = 1

        if len(unique_players) != len(mentioned_players):
            await context.respond('You need to mention 3 unique players.')
            return

        own_mentions = list(filter(lambda m: m.id == context.user.id, mentioned_players))
        if len(own_mentions) > 1:
            await context.respond('You cannot team up with yourself.')
            return

        players = []

        for mentioned_player in mentioned_players:
            player = Player.filter(discord_id=mentioned_player.id)

            if not player:
                await context.respond(f'The player {mentioned_player.id} does not exist.')
                return

            players.append(player)

        message: discord.Message = await context.channel.send(
            f'Please confirm that you want to be part of <@{mentioned_players[0].id}>\'s team.')
        await message.add_reaction('✅')

        bot = discord.Bot()

        try:
            def check(reaction, user):
                """
                Checks for reactions of a certain user.
                :param reaction:
                :param user:
                :return:
                """
                return str(reaction.emoji) == '✅' and user in mentioned_players

            await bot.wait_for('reaction_add', timeout=60, check=check)
        except TimeoutError:
            await context.respond('Command cancelled. Players did not react in time.')
            return

        await Team.create(players=players)
        await context.respond(
            f'The team of <@{mentioned_players[0].id}>, <@{mentioned_players[1].id}>, <@{mentioned_players[2].id}> '
            f'and <@{mentioned_players[3].id}> has been created successfully.'
        )


def setup(bot: discord.Bot) -> NoReturn:
    """
    Sets up the cog.
    :param bot:
    """
    bot.add_cog(Social(bot))
