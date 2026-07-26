from typing import Protocol
from domain.entities.training import Training


class TrainingRepository(Protocol):
    def get_by_id(self, training_id: int) -> Training | None:
        ...

    def get_all(self) -> list[Training]:
        ...

    def get_by_date_range(self, start: "date", end: "date") -> list[Training]:
        ...

    def save(self, training: Training) -> Training:
        ...