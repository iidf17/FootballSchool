from typing import Protocol
from domain.entities.attendance import Attendance


class AttendanceRepository(Protocol):
    def get_by_training_id(self, training_id: int) -> list[Attendance]:
        ...

    def save_batch(self, attendances: list[Attendance]) -> list[Attendance]:
        ...