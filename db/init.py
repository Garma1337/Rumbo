# coding: utf-8

from typing import List, NoReturn

from tortoise import Tortoise

from lib.services import logger


async def init() -> NoReturn:
    models: List[str] = [
        'db.models.player',
        'db.models.team',
        'db.models.lobby',
    ]

    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': models}
    )

    # Generate the schema
    await Tortoise.generate_schemas()
    logger.info(f'Database initiated successfully!')
