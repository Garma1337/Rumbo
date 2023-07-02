# coding: utf-8

import unittest

from lib.db import DbUtil


class DbUtilTest(unittest.TestCase):

    def test_can_find_nat_type_by_valid_key(self):
        nat_type: dict[str, str] | None = DbUtil.find_nat_type_by_key('nat1')

        self.assertTrue('key' in nat_type)
        self.assertTrue('name' in nat_type)
        self.assertTrue('description' in nat_type)
        self.assertTrue('default' in nat_type)

    def test_cannot_find_nat_type_by_invalid_key(self):
        nat_type: dict[str, str] | None = DbUtil.find_nat_type_by_key('abc')

        self.assertEqual(nat_type, None)

    def test_can_find_console_by_valid_key(self):
        console: dict[str, str] | None = DbUtil.find_console_by_key('PS4')

        self.assertTrue('key' in console)
        self.assertTrue('name' in console)
        self.assertTrue('description' in console)
        self.assertTrue('emote' in console)
        self.assertTrue('default' in console)

    def test_cannot_find_console_by_invalid_key(self):
        console: dict[str, str] | None = DbUtil.find_console_by_key('abc')

        self.assertEqual(console, None)

    def test_can_find_region_by_valid_key(self):
        region: dict[str, str] | None = DbUtil.find_region_by_key('region1')

        self.assertTrue('key' in region)
        self.assertTrue('name' in region)
        self.assertTrue('description' in region)
        self.assertTrue('default' in region)
        self.assertTrue('profileEnabled' in region)
        self.assertTrue('nearbyRegions' in region)
        self.assertTrue('countries' in region)

    def test_cannot_find_region_by_invalid_key(self):
        region: dict[str, str] | None = DbUtil.find_console_by_key('abc')

        self.assertEqual(region, None)
