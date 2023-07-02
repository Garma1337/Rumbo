# coding: utf-8

from typing import List, NoReturn

import discord


class MessageUtil(object):
    """
    Various message utilities.
    """

    @staticmethod
    async def wait_for_reactions(
            bot: discord.Bot,
            message: discord.Message,
            users: List[discord.Member],
            timeout: int,
            emoji: str
    ) -> NoReturn:
        """
        Waits for reactions of a list of users on a message. All reactions must be unique.
        """
        collected_reactions: List[discord.Member] = []

        while True:
            def reaction_filter(reaction: discord.Reaction, user: discord.User):
                """
                Checks for reactions of a certain user.
                :param reaction:
                :param user:
                :return:
                """
                return str(reaction.emoji) == emoji and reaction.message.id == message.id and user in users

            r, u = await bot.wait_for('reaction_add', timeout=timeout, check=reaction_filter)

            if u in collected_reactions:
                continue

            collected_reactions.append(u)

            if len(collected_reactions) == len(users):
                break
