from datetime import date, time
from domain.entities.training import Training
from domain.rules.training_rules import has_overlap
from domain.exceptions import TrainingOverlapError
from application.interfaces.training_repository import TrainingRepository


class CreateTrainingUseCase:
    def __init__(self, training_repository: TrainingRepository):
        self._repository = training_repository

    def execute(
        self,
        training_date: date,
        start_time: time,
        end_time: time,
        location: str,
        team_ids: list[int] | None = None,
    ) -> Training:
        existing_trainings = self._repository.get_by_date_range(
            start=training_date, end=training_date
        )

        candidate = Training(
            id=0,
            date=training_date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            team_ids=team_ids or [],
        )

        if has_overlap(candidate, existing_trainings):
            raise TrainingOverlapError(
                f"Тренировка пересекается с уже существующей на {training_date}"
            )

        return self._repository.save(candidate)