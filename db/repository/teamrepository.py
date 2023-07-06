# coding: utf-8

from db.models.player import Player
from db.models.team import Team
from db.repository.repository import RepositoryInterface


class TeamRepository(RepositoryInterface):

    @staticmethod
    async def find_one_by_player(player: Player) -> Team | None:
        team: Team = await Team.filter(players__discord_id__contains=player.discord_id).first()
        return team
