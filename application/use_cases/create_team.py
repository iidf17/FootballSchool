from domain.entities.team import Team
from application.interfaces.team_repository import TeamRepository


class CreateTeamUseCase:
    def __init__(self, team_repository: TeamRepository):
        self._repository = team_repository

    def execute(self, name: str, min_age: int, max_age: int) -> Team:
        candidate = Team(id=0, name=name, min_age=min_age, max_age=max_age)
        return self._repository.save(candidate)