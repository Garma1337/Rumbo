# coding: utf-8

from typing import List

from discord import AutocompleteContext, ActivityType

from lib.db import DbUtil


class AutoCompletion(object):
    """
    Autocomplete helpers.
    """

    @staticmethod
    def get_activity_types() -> List[str]:
        """
        Returns an array of activities.
        :return:
        """
        return [
            ActivityType.playing.name,
            ActivityType.listening.name,
            ActivityType.watching.name
        ]

    @staticmethod
    def get_nat_types() -> List[str]:
        """
        Returns an array of all NAT type names to use for autocompletion.
        :return:
        """
        nat_types = DbUtil.get_nat_types()
        return [nat_type['name'] for nat_type in nat_types]

    @staticmethod
    def get_regions() -> List[str]:
        """
        Returns an array of all region names to use for autocompletion.
        :return:
        """
        regions = DbUtil.get_regions()
        return [region['name'] for region in regions]

    @staticmethod
    def get_consoles() -> List[str]:
        """
        Returns an array of all console names to use for autocompletion.
        :return:
        """
        consoles = DbUtil.get_consoles()
        return [console['name'] for console in consoles]

    @staticmethod
    async def get_flags(context: AutocompleteContext) -> List[str]:
        """
        Returns an array of all flags to use for autocompletion. To use this, the region needs to be selectable in the slash command as well.
        :param context:
        :return:
        """
        regions = DbUtil.get_regions()

        region_name = context.options['region']
        filtered_regions = filter(lambda r: r['name'] == region_name, regions)

        if not regions:
            return []

        region = list(filtered_regions)[0]
        return list(region['countries'])
