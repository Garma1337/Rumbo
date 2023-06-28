# coding: utf-8

from tortoise import Model, fields


class Team(Model):
    id = fields.IntField(pk=True)
    players = fields.ManyToManyField('models.Player')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    lobby = fields.ForeignKeyField('models.Lobby', related_name='teams', null=True)
