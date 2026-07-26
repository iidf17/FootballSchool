from datetime import date, datetime, time
import pytest
from application.dto.attendance_dto import AttendanceMarkRequest
from application.use_cases.create_training import CreateTrainingUseCase
from domain.entities.attendance import Attendance, AttendanceStatus
from application.use_cases.mark_attendance import MarkAttendanceUseCase, TrainingNotFoundError
from domain.entities.training import Training

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
    

class FakeAttendanceRepository:
    def __init__(self):
        self._attendance: list[Attendance] = []

    def get_by_training_id(self, training_id: int) -> list[Attendance]:
        return [a for a in self._attendance if a.training_id == training_id]

    def save_batch(self, attendances: list[Attendance]) -> list[Attendance]:
        self._attendance.extend(attendances)
        return attendances


def test_mark_attendance_succeeds():
    attendance_repo = FakeAttendanceRepository()
    training_repo = FakeTrainingRepository()
    
    attendance_use_case = MarkAttendanceUseCase(attendance_repo, training_repo)
    training_use_case = CreateTrainingUseCase(training_repo)
    
    training_use_case.execute(
        training_date=date(2026, 7, 20),
        start_time=time(18, 0),
        end_time=time(19, 0),
        location="Стадион А",
    )

    requests  = [
        AttendanceMarkRequest(1, AttendanceStatus.PRESENT),
        AttendanceMarkRequest(2, AttendanceStatus.ABSENT),
        AttendanceMarkRequest(3, AttendanceStatus.LATE)
    ]
    result = attendance_use_case.execute(0, requests=requests)
    assert len(result) == 3 
    assert result[0].status == AttendanceStatus.PRESENT


def test_mark_attendance_raises_when_training_not_found():
    attendance_repo = FakeAttendanceRepository()
    training_repo = FakeTrainingRepository()
    
    attendance_use_case = MarkAttendanceUseCase(attendance_repo, training_repo)
    
    requests  = [
        AttendanceMarkRequest(1, AttendanceStatus.PRESENT),
        AttendanceMarkRequest(2, AttendanceStatus.ABSENT),
        AttendanceMarkRequest(3, AttendanceStatus.LATE)
    ]
    with pytest.raises(TrainingNotFoundError):
        attendance_use_case.execute(99, requests=requests)
