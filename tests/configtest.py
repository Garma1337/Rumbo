# coding: utf-8

import unittest

from lib.services import config


class ConfigTest(unittest.TestCase):

    def test_can_get_config(self):
        self.assertTrue(config.bot_user_id is not None)
        self.assertTrue(config.enable_debug is not None)
        self.assertTrue(config.owner is not None)
        self.assertTrue(config.bot_secret is not None)
        self.assertTrue(config.default_embed_color is not None)
        self.assertTrue(config.guild is not None)
        self.assertTrue(config.log_level is not None)
