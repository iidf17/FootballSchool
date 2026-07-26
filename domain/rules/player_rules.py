from datetime import date
from domain.entities.player import Player
from domain.entities.team import Team


def calculate_age(birth_date: date, on_date: date) -> int:
    age = on_date.year - birth_date.year
    had_birthday = (on_date.month, on_date.day) >= (birth_date.month, birth_date.day)
    if not had_birthday:
        age -= 1
    return age


def is_eligible_age(player: Player, team: Team, season_start_date: date) -> bool:
    age = calculate_age(player.birth_date, season_start_date)
    return team.min_age <= age <= team.max_age