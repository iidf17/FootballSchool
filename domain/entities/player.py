from dataclasses import dataclass
from datetime import date
from enum import Enum


class Position(str, Enum):
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    FORWARD = "forward"


class PlayerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"  # ушёл из школы, но история сохраняется


@dataclass
class Player:
    id: int
    first_name: str
    last_name: str
    birth_date: date
    position: Position
    team_id: int
    status: PlayerStatus = PlayerStatus.ACTIVE

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"