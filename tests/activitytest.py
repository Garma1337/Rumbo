# coding: utf-8

import unittest

import discord as discord

from utils.activity import ActivityUtil


class ActivityTest(unittest.TestCase):

    def test_rumble_stream_is_rumble_stream(self):
        activity: discord.Streaming = discord.Streaming(
            name='4 vs. 4 War against Italians',
            url='https://twitch.tv/garma1337',
            state='Crash Team Rumble'
        )

        is_ctr_stream: bool = ActivityUtil.is_ctr_stream(activity)
        self.assertTrue(is_ctr_stream)

    def test_other_stream_is_not_rumble_stream(self):
        activity: discord.Streaming = discord.Streaming(
            name='200% Speedruns',
            url='https://twitch.tv/pie',
            state='Crash Bash'
        )

        is_ctr_stream: bool = ActivityUtil.is_ctr_stream(activity)
        self.assertFalse(is_ctr_stream)

    def test_other_activity_is_not_rumble_stream(self):
        activity: discord.Activity = discord.Activity(state='Watching anime')

        is_ctr_stream: bool = ActivityUtil.is_ctr_stream(activity)
        self.assertFalse(is_ctr_stream)
