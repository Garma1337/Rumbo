# coding: utf-8

from enum import Enum
from typing import List, NoReturn

import discord
from discord import DMChannel, Role

from lib.services import logger


class RoleNames(Enum):
    AdminRole = 'Admin'
    TeamRole = 'Team'
    MutedRole = 'Muted'
    LiveRole = 'Live'


class MemberUtil(object):

    @staticmethod
    def is_team(member: discord.Member) -> bool:
        team_roles: List[str] = [RoleNames.AdminRole.value, RoleNames.TeamRole.value]

        for team_role in team_roles:
            role: Role | None = discord.utils.get(member.guild.roles, name=team_role)

            if not role:
                continue

            if member.get_role(role.id):
                return True

        return False

    @staticmethod
    async def send_dm(member: discord.Member, message: str) -> NoReturn:
        dm_channel: DMChannel | None = member.dm_channel
        if not dm_channel:
            logger.info(f'Creating new DM channel for user {member.id}')
            dm_channel: DMChannel = await member.create_dm()

        await dm_channel.send(message)
