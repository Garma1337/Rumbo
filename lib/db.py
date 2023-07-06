# coding: utf-8

import json
import os
from typing import List

from lib.filesystem import FileSystem


class DbUtil(object):

    @staticmethod
    def get_consoles() -> List[dict[str, str]]:
        file_content: str = FileSystem.read_file(os.path.join(FileSystem.get_directory_path(__file__), '..', 'db', 'consoles.json'))
        return json.loads(file_content)

    @staticmethod
    def get_maps() -> List[dict[str, str]]:
        file_content: str = FileSystem.read_file(os.path.join(FileSystem.get_directory_path(__file__), '..', 'db', 'maps.json'))
        return json.loads(file_content)

    @staticmethod
    def get_nat_types() -> List[dict[str, str]]:
        file_content: str = FileSystem.read_file(os.path.join(FileSystem.get_directory_path(__file__), '..', 'db', 'nat_types.json'))
        return json.loads(file_content)

    @staticmethod
    def get_regions() -> List[dict[str, str]]:
        file_content: str = FileSystem.read_file(os.path.join(FileSystem.get_directory_path(__file__), '..', 'db', 'regions.json'))
        return json.loads(file_content)

    @staticmethod
    def find_nat_type_by_key(nat_type_key: str) -> dict[str, str] | None:
        nat_types = DbUtil.get_nat_types()
        filtered_nat_types = list(filter(lambda n: n['key'] == nat_type_key, nat_types))

        if len(filtered_nat_types) == 0:
            return None

        return filtered_nat_types[0]

    @staticmethod
    def find_region_by_key(region_key: str) -> dict[str, str] | None:
        regions = DbUtil.get_regions()
        filtered_regions = list(filter(lambda r: r['key'] == region_key, regions))

        if len(filtered_regions) == 0:
            return None

        return filtered_regions[0]

    @staticmethod
    def find_console_by_key(console_key: str) -> dict[str, str] | None:
        consoles = DbUtil.get_consoles()
        filtered_consoles = list(filter(lambda c: c['key'] == console_key, consoles))

        if len(filtered_consoles) == 0:
            return None

        return filtered_consoles[0]
