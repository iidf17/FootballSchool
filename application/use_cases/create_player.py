from datetime import date
from application.interfaces.team_repository import TeamRepository
from domain.entities.player import Player, Position, PlayerStatus
from domain.rules.player_rules import is_eligible_age
from domain.exceptions import PlayerAgeNotEligibleError, TeamNotFoundError
from application.interfaces.player_repository import PlayerRepository


class CreatePlayerUseCase:
    def __init__(
            self, 
            player_repository: PlayerRepository,
            team_repository: TeamRepository
        ):
            self._repository = player_repository
            self._team_repository = team_repository

    def execute(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        position: Position,
        team_id: int,
        season_start_date: date,
    ) -> Player:
        team = self._team_repository.get_by_id(team_id)
        if team is None:
            raise TeamNotFoundError(f"Команда {team_id} не найдена")

        candidate = Player(
            id=0,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            position=position,
            team_id=team_id,
            status=PlayerStatus.ACTIVE,
        )

        if not is_eligible_age(candidate, team, season_start_date):
            raise PlayerAgeNotEligibleError(
                f"Игрок {first_name} {last_name} не подходит по возрасту для команды {team.name})"
            )

        return self._repository.save(candidate)