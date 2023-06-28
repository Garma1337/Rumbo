# coding: utf-8

from db.models.player import Player
from db.models.team import Team


class TeamManager(object):
    """
    Class to manage teams.
    """

    @staticmethod
    async def find_team_by_player(player: Player) -> Team | None:
        """
        Finds all teams that a player belongs to.
        :param player:
        :return:
        """
        team: Team = await Team.filter(players__discord_id__contains=player.discord_id).first()
        return team
