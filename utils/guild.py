# coding: utf-8

import discord

from discord import TextChannel


class GuildUtil(object):
    """
    Various guild utilities.
    """

    @staticmethod
    def find_channel(guild: discord.Guild, channel_name: str) -> TextChannel | None:
        """
        Finds a channel inside a guild by name.
        :param guild:
        :param channel_name:
        :return:
        """
        filtered = list(filter(lambda c: c.name.lower() == channel_name.lower(), guild.text_channels))

        if len(filtered) == 0:
            return None

        return filtered[0]
