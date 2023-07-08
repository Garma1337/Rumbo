# coding: utf-8

import unittest
from typing import List

from lib.math import Math, MathException


class MathTest(unittest.TestCase):

    def test_can_partition_8_sets_into_2_sets_of_4(self):
        objects = MathTest.get_objects()
        parititons = Math.greedy_partition(objects, 2, 4, 'rank')

        self.assertListEqual([p['name'] for p in parititons[0]], ['Megumi', 'Broz', 'Dashy', 'JuliaBandicoot'])
        self.assertListEqual([p['name'] for p in parititons[1]], ['Jecux', 'Turismo', 'Garma', 'Fiskaren'])

    def test_can_partition_8_sets_into_4_sets_of_2(self):
        objects = MathTest.get_objects()
        parititons = Math.greedy_partition(objects, 4, 2, 'rank')

        self.assertListEqual([p['name'] for p in parititons[0]], ['Megumi', 'JuliaBandicoot'])
        self.assertListEqual([p['name'] for p in parititons[1]], ['Jecux', 'Fiskaren'])
        self.assertListEqual([p['name'] for p in parititons[2]], ['Turismo', 'Garma'])
        self.assertListEqual([p['name'] for p in parititons[3]], ['Broz', 'Dashy'])

    def test_cannot_partition_8_sets_into_4_sets_of_4(self):
        objects = MathTest.get_objects()
        self.assertRaises(MathException, Math.greedy_partition, objects, 4, 4, 'rank')

    def test_cannot_partition_8_sets_into_sets_of_3(self):
        objects = MathTest.get_objects()
        self.assertRaises(MathException, Math.greedy_partition, objects, 3, 3, 'rank')

    def test_cannot_specify_wrong_value_key(self):
        objects = MathTest.get_objects()
        self.assertRaises(ValueError, Math.greedy_partition, objects, 2, 4, 'test')

    @staticmethod
    def get_objects() -> List[dict[str, int | str]]:
        return [
            {'name': 'Garma', 'rank': 1337},
            {'name': 'Turismo', 'rank': 2158},
            {'name': 'Megumi', 'rank': 2804},
            {'name': 'Jecux', 'rank': 2562},
            {'name': 'Fiskaren', 'rank': 834},
            {'name': 'Dashy', 'rank': 1562},
            {'name': 'Broz', 'rank': 1834},
            {'name': 'JuliaBandicoot', 'rank': 127},
        ]
