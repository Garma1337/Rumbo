# coding: utf-8

from discord import TextChannel, Guild, NotFound, Forbidden, HTTPException, InvalidData


class GuildUtil(object):

    @staticmethod
    async def fetch_channel(guild: Guild, channel_id: int) -> TextChannel | None:
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
