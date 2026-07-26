from typing import Protocol
from domain.entities.player import Player


class PlayerRepository(Protocol):
    def get_by_id(self, player_id: int) -> Player | None:
        ...

    def get_all(self) -> list[Player]:
        ...

    def save(self, player: Player) -> Player:
        ...