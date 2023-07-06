# coding: utf-8

import time
from datetime import datetime


class Carbon(object):

    @staticmethod
    def getCurrentTimestamp() -> int:
        return int(time.time())

    @staticmethod
    def toDateTime(date: datetime) -> str:
        return date.strftime('%Y-%m-%d %H:%I:%S')
