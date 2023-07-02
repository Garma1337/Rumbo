# coding: utf-8

from tortoise import Model, fields


class Lobby(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField('models.Player', related_name='created_lobby')
    maps = fields.TextField(null=True)
    guild = fields.CharField(max_length=30, null=True)
    channel = fields.CharField(max_length=30, null=True)
    message = fields.CharField(max_length=30, null=True)
    started = fields.SmallIntField()
    insta = fields.SmallIntField()
    max_players = fields.IntField(default=8)
    solo_queue = fields.ManyToManyField('models.Player', related_name='lobby')
    teams = fields.ManyToManyField('models.Team', related_name='lobby')
    region_lock = fields.CharField(max_length=30, null=True)
    started_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
