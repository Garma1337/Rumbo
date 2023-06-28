# coding: utf-8

import discord


class ActivityUtil(object):
    """
    Various activity utilities.
    """

    @staticmethod
    def is_crash_team_rumble_stream(activity: discord.BaseActivity) -> bool:
        """
        Checks if an activity is a crash team rumble stream.
        :param activity:
        :return:
        """
        if not isinstance(activity, discord.Streaming):
            return False

        return activity.type == discord.ActivityType.streaming and activity.game.lower() == 'Crash Team Rumble'.lower()
