# coding: utf-8

import unittest
from datetime import datetime

from lib.carbon import Carbon


class CarbonTest(unittest.TestCase):

    def test_date_is_converted_to_datetime(self):
        date: datetime = datetime.fromtimestamp(1688068830)
        formatted: str = Carbon.toDateTime(date)

        self.assertEqual(date.strftime('%Y-%m-%d %H:%I:%S'), formatted)
