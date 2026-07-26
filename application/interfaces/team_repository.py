from typing import Protocol
from domain.entities.team import Team


class TeamRepository(Protocol):
    def get_by_id(self, team_id: int) -> Team | None:
        ...

    def get_all(self) -> list[Team]:
        ...

    def save(self, team: Team) -> Team:
        ...