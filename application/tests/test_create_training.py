from datetime import date, time

import pytest
from domain.entities.training import Training
from application.use_cases.create_training import CreateTrainingUseCase
from domain.exceptions import TrainingOverlapError


class FakeTrainingRepository:
    def __init__(self):
        self._trainings: list[Training] = []

    def get_by_id(self, training_id: int) -> Training | None:
        return next((t for t in self._trainings if t.id == training_id), None)

    def get_all(self) -> list[Training]:
        return self._trainings

    def get_by_date_range(self, start: date, end: date) -> list[Training]:
        return [t for t in self._trainings if start <= t.date <= end]

    def save(self, training: Training) -> Training:
        self._trainings.append(training)
        return training


def test_create_training_succeeds_when_no_overlap():
    repo = FakeTrainingRepository()
    use_case = CreateTrainingUseCase(repo)

    result = use_case.execute(
        training_date=date(2026, 7, 20),
        start_time=time(18, 0),
        end_time=time(19, 0),
        location="Стадион А",
    )

    assert result.location == "Стадион А"


def test_create_training_raises_when_overlap():
    repo = FakeTrainingRepository()
    use_case = CreateTrainingUseCase(repo)

    # сначала создаём одну тренировку
    use_case.execute(
        training_date=date(2026, 7, 20),
        start_time=time(18, 0),
        end_time=time(19, 0),
        location="Стадион А",
    )
    with pytest.raises(TrainingOverlapError):
        use_case.execute(
            training_date=date(2026, 7, 20),
            start_time=time(18, 30),
            end_time=time(20, 0),
            location="Стадион Б",
        )


def test_create_training_succeeds_when_same_time_different_teams():
    repo = FakeTrainingRepository()
    use_case = CreateTrainingUseCase(repo)

    use_case.execute(training_date=date(2026, 8, 10), start_time=time(18,00), end_time=time(19,00), location="Stadion 1", team_ids=[1])
    result =  use_case.execute(training_date=date(2026, 8, 10), start_time=time(18,00), end_time=time(19,00), location="Stadion 2", team_ids=[2])

    assert result in repo.get_all()
