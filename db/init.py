# coding: utf-8

from typing import List, NoReturn

from tortoise import Tortoise


async def init() -> NoReturn:
    """
    Initialises the database.
    """

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
    print(f'Database initiated successfully!')
