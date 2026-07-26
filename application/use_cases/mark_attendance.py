from datetime import datetime
from domain.entities.attendance import Attendance
from application.interfaces.attendance_repository import AttendanceRepository
from application.interfaces.training_repository import TrainingRepository
from application.dto.attendance_dto import AttendanceMarkRequest
from domain.exceptions import DomainError


class TrainingNotFoundError(DomainError):
    pass


class MarkAttendanceUseCase:
    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        training_repository: TrainingRepository,
    ):
        self._attendance_repository = attendance_repository
        self._training_repository = training_repository

    def execute(
        self, training_id: int, requests: list[AttendanceMarkRequest]
    ) -> list[Attendance]:
        training = self._training_repository.get_by_id(training_id)
        if training is None:
            raise TrainingNotFoundError(f"Тренировка {training_id} не найдена")

        now = datetime.now()
        attendances = [
            Attendance(
                id=0,
                player_id=req.player_id,
                training_id=training_id,
                status=req.status,
                marked_at=now,
            )
            for req in requests
        ]

        return self._attendance_repository.save_batch(attendances)