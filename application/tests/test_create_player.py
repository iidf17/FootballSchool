from datetime import date, time

import pytest
from domain.entities.player import Player, Position
from application.use_cases.create_player import CreatePlayerUseCase
from domain.entities.team import Team
from domain.exceptions import PlayerAgeNotEligibleError
from domain.rules.player_rules import is_eligible_age


class FakePlayerRepository:
    def __init__(self):
        self._players: list[Player] = []

    def get_by_id(self, player_id: int) -> Player | None:
        return next((p for p in self._players if p.id == player_id), None)

    def get_all(self) -> list[Player]:
        return self._players

    def save(self, player: Player) -> Player:
        self._players.append(player)
        return player
    

class FakeTeamRepository:
    def __init__(self):
        self._teams: list[Team] = []

    def get_by_id(self, team_id: int) -> Team | None:
        return next((t for t in self._teams if t.id == team_id), None)

    def get_all(self) -> list[Team]:
        return self._teams

    def save(self, team: Team) -> Team:
        self._teams.append(team)
        return team
    
    
def test_create_player_succeeds_when_age_eligible():
    repo = FakePlayerRepository()
    team_repo = FakeTeamRepository()
    team_repo.save(Team(id=1, name="U10", min_age=9, max_age=10))
    
    use_case = CreatePlayerUseCase(repo, team_repo)

    result = use_case.execute(
        first_name='Sam',
        last_name='Ben',
        birth_date=date(2016, 8, 10),
        position=Position.FORWARD,
        team_id=1,
        season_start_date=date(2026, 9, 1)
    )

    assert result.first_name == 'Sam'
    assert result in repo.get_all()

def test_create_player_raises_when_age_not_eligible():
    repo = FakePlayerRepository()
    team_repo = FakeTeamRepository()
    team_repo.save(Team(id=1, name="U10", min_age=9, max_age=10))
    
    use_case = CreatePlayerUseCase(repo, team_repo)

    with pytest.raises(PlayerAgeNotEligibleError):
        use_case.execute(
            first_name='Sam',
            last_name='Ben',
            birth_date=date(2012, 8, 10),
            position=Position.FORWARD,
            team_id=1,
            season_start_date=date(2026, 9, 1)
        )