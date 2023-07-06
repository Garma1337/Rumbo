# coding: utf-8

from db.models.lobby import Lobby
from db.models.player import Player
from db.repository.repository import RepositoryInterface


class LobbyRepository(RepositoryInterface):

    @staticmethod
    async def find_one_by_player(player: Player) -> Lobby | None:
        pass
