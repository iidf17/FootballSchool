from datetime import date, time
from domain.entities.player import Player, Position, PlayerStatus
from domain.entities.team import Team
from domain.rules.player_rules import is_eligible_age


def test_player_with_eligible_age_returns_true ():
    team = Team(id=1, name="U10", min_age=9, max_age=10)
    player_a = Player(id=1,
                    team_id=team.id,
                    first_name='Dan',last_name='man',
                    birth_date=date(2016,7,12),
                    position=Position.DEFENDER)

    assert is_eligible_age(player_a, team, date.today()) is True

def test_player_with_eligible_age_returns_false ():
    team = Team(id=1, name="U10", min_age=9, max_age=10)
    player_b = Player(id=1,
                    team_id=team.id,
                    first_name='Alex',last_name='Kale',
                    birth_date=date(2014,7,12),
                    position=Position.FORWARD)

    assert is_eligible_age(player_b, team, date.today()) is False