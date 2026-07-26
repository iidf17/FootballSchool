import pytest
from domain.entities.team import Team, InvalidAgeRangeError


def test_team_with_valid_age_range_creates_successfully():
    team = Team(id=1, name="U10", min_age=9, max_age=10)
    assert team.min_age == 9
    assert team.max_age == 10


def test_team_with_invalid_age_range_raises_error():
    with pytest.raises(InvalidAgeRangeError):
        Team(id=1, name="Invalid", min_age=10, max_age=9)