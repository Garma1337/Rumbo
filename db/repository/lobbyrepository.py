# coding: utf-8

from db.models.lobby import Lobby
from db.models.player import Player
from db.repository.repository import RepositoryInterface


class LobbyRepository(RepositoryInterface):
    """
    Lobby repository.
    """

    @staticmethod
    async def find_one_by_player(player: Player) -> Lobby | None:
        """
        Finds a lobby for a player.
        :param player:
        """
        pass
