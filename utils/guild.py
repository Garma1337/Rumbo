# coding: utf-8

from typing import List

from discord import TextChannel, Guild, NotFound, Forbidden, HTTPException, InvalidData


class GuildUtil(object):
    """
    Various guild utilities.
    """

    @staticmethod
    async def fetch_channel(guild: Guild, channel_id: int) -> TextChannel | None:
        """
        Gets a channel by its ID.
        :param guild:
        :param channel_id:
        :return:
        """
        try:
            channel: TextChannel = await guild.fetch_channel(channel_id)
        except InvalidData:
            return None
        except NotFound:
            return None
        except Forbidden:
            return None
        except HTTPException:
            return None

        return channel

    @staticmethod
    def find_channel_by_name(guild: Guild, channel_name: str) -> TextChannel | None:
        """
        Finds a channel inside a guild by name.
        :param guild:
        :param channel_name:
        :return:
        """
        channels: List[TextChannel] = list(filter(lambda c: c.name.lower() == channel_name.lower(), guild.channels))

        if len(channels) == 0:
            return None

        return channels[0]
