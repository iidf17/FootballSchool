import pytest

from application.use_cases.create_team import CreateTeamUseCase
from domain.entities.team import InvalidAgeRangeError, Team


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


def test_create_team_succeeds_with_valid_range():
    repo = FakeTeamRepository()
    use_case = CreateTeamUseCase(repo)

    result = use_case.execute(name="U10", min_age=9, max_age=10)

    assert result.name == 'U10'
    assert result in repo.get_all()

def test_create_team_raises_with_invalid_range():
    repo = FakeTeamRepository()
    use_case = CreateTeamUseCase(repo)

    with pytest.raises(InvalidAgeRangeError):
        use_case.execute(name="U10", min_age=19, max_age=10)