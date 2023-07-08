# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, SlashCommandOptionType, Message, slash_command, Cog, Bot

from db.models.player import Player
from db.models.team import Team
from lib.services import bot
from utils.message import MessageUtil


class CreateTeamCommand(Cog):

    @slash_command(name='create_team', description='Create a team with 3 other players.')
    async def create_team(
            self,
            context: ApplicationContext,
            player1: SlashCommandOptionType.mentionable,
            player2: SlashCommandOptionType.mentionable,
            player3: SlashCommandOptionType.mentionable
    ) -> NoReturn:
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

        bot_mentions = list(filter(lambda m: m.bot, mentioned_players))
        if len(bot_mentions) > 0:
            await context.respond('You cannot team up with a bot.')
            return

        players = []

        for mentioned_player in mentioned_players:
            player = Player.filter(discord_id=mentioned_player.id)

            if not player:
                await context.respond(f'The player {mentioned_player.id} does not exist.')
                return

            players.append(player)

        message: Message = await context.channel.send(
            f'Please confirm that you want to be part of <@{mentioned_players[0].id}>\'s team.')
        await message.add_reaction('✅')

        try:
            await MessageUtil.wait_for_reactions(bot, message, mentioned_players, 60, '✅')
        except TimeoutError:
            await context.respond('Command cancelled. Players did not react in time.')
            return

        await Team.create(players=players)
        await context.respond(
            f'The team of <@{mentioned_players[0].id}>, <@{mentioned_players[1].id}>, <@{mentioned_players[2].id}> '
            f'and <@{mentioned_players[3].id}> has been created successfully.'
        )


def setup(bot: Bot):
    bot.add_cog(CreateTeamCommand())
