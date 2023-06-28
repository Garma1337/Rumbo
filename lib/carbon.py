# coding: utf-8

import time
from datetime import datetime


class Carbon(object):
    """
    Various date(time) functions.
    """

    @staticmethod
    def getCurrentTimestamp() -> int:
        """
        Returns the current unix timestamp.
        :return:
        """
        return int(time.time())

    @staticmethod
    def toDateTime(date: datetime) -> str:
        """
        Converts a date object into an y-m-d h:i:s string.
        :param date:
        :return:
        """
        return date.strftime('%Y-%m-%d %H:%I:%S')
