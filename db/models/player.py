# coding: utf-8

from tortoise import Model, fields


class Player(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.BigIntField()
    activision_id = fields.CharField(max_length=50, null=True)
    nat = fields.CharField(max_length=10, null=True)
    flag = fields.CharField(max_length=10, null=True)
    region = fields.CharField(max_length=20, null=True)
    console = fields.CharField(max_length=20, null=True)
    favorite_character = fields.CharField(max_length=30, null=True)
    favorite_map = fields.CharField(max_length=30, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    @staticmethod
    async def find_or_create(discord_id: int):
        player: Player = await Player.filter(discord_id=discord_id).first()

        if not player:
            player: Player = await Player.create(discord_id=discord_id)

        return player
