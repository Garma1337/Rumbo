# coding: utf-8

from enum import Enum

import discord


class RoleNames(Enum):
    """
    Enum for role names.
    """

    AdminRole = 'Admin'
    TeamRole = 'Team'


class MemberUtil(object):
    """
    Various guild member utilities.
    """

    @staticmethod
    def has_role(member: discord.Member, role_name: str) -> bool:
        """
        Checks if a member has a certain role.
        :param member:
        :param role_name:
        :return:
        """
        roles = list(filter(lambda r: r.name == role_name, member.roles))
        return len(roles) > 0

    @staticmethod
    def is_team(member: discord.Member) -> bool:
        """
        Returns if a member is a team member.
        :param member:
        :return:
        """
        return MemberUtil.has_role(member, RoleNames.AdminRole.value) or MemberUtil.has_role(member, RoleNames.TeamRole.value)
