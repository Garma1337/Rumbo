# coding: utf-8

from tortoise import Model, fields


class Lobby(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField('models.Player')
    maps = fields.TextField()
    guild = fields.CharField(max_length=30, null=True)
    channel = fields.CharField(max_length=30, null=True)
    message = fields.CharField(max_length=30, null=True)
    started = fields.SmallIntField()
    started_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
