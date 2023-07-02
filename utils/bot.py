# coding: utf-8

from discord import Guild, Bot, Forbidden, HTTPException, Intents


class BotUtil(object):
    """
    Various bot utilities.
    """

    @staticmethod
    async def fetch_guild(bot: Bot, guild_id: int) -> Guild | None:
        """
        Finds a guild by ID.
        :param bot:
        :param guild_id:
        :return:
        """
        try:
            guild: Guild = await bot.fetch_guild(guild_id)
        except Forbidden:
            return None
        except HTTPException:
            return None

        return guild
