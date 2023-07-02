# coding: utf-8

import unittest
from typing import List

from commands.autocomplete import AutoCompletion


class AutoCompleteTest(unittest.TestCase):

    def test_can_get_nat_types(self):
        nat_types: List[str] = AutoCompletion.get_nat_types()

        self.assertTrue(isinstance(nat_types, list))

        for nat_type in nat_types:
            self.assertTrue(isinstance(nat_type, str))

    def test_can_get_regions(self):
        regions: List[str] = AutoCompletion.get_regions()

        self.assertTrue(isinstance(regions, list))

        for region in regions:
            self.assertTrue(isinstance(region, str))

    def test_can_get_consoles(self):
        consoles: List[str] = AutoCompletion.get_consoles()

        self.assertTrue(isinstance(consoles, list))

        for console in consoles:
            self.assertTrue(isinstance(console, str))
