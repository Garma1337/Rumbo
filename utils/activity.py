# coding: utf-8

import discord


class ActivityUtil(object):

    @staticmethod
    def is_crash_team_rumble_stream(activity: discord.BaseActivity) -> bool:
        if not isinstance(activity, discord.Streaming):
            return False

        return activity.type == discord.ActivityType.streaming and activity.game.lower() == 'Crash Team Rumble'.lower()
