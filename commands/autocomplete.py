# coding: utf-8

from typing import List

from discord import AutocompleteContext, ActivityType

from lib.db import DbUtil


class AutoCompletion(object):

    @staticmethod
    def get_activity_types() -> List[str]:
        return [
            ActivityType.playing.name,
            ActivityType.listening.name,
            ActivityType.watching.name
        ]

    @staticmethod
    def get_nat_types() -> List[str]:
        nat_types = DbUtil.get_nat_types()
        return [nat_type['name'] for nat_type in nat_types]

    @staticmethod
    def get_regions() -> List[str]:
        regions = DbUtil.get_regions()
        return [region['name'] for region in regions]

    @staticmethod
    def get_consoles() -> List[str]:
        consoles = DbUtil.get_consoles()
        return [console['name'] for console in consoles]

    @staticmethod
    async def get_flags(context: AutocompleteContext) -> List[str]:
        regions = DbUtil.get_regions()

        region_name = context.options['region']
        filtered_regions = filter(lambda r: r['name'] == region_name, regions)

        if not regions:
            return []

        region = list(filtered_regions)[0]
        return list(region['countries'])
