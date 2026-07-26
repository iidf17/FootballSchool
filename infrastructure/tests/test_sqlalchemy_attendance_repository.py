# infrastructure/tests/test_sqlalchemy_attendance_repository.py
from datetime import date, datetime, time
import pytest
from sqlalchemy.exc import IntegrityError
from domain.entities.attendance import Attendance, AttendanceStatus
from domain.entities.player import Player, Position
from domain.entities.training import Training
from infrastructure.db.repositories.sqlalchemy_player_repository import SqlAlchemyPlayerRepository
from infrastructure.db.repositories.sqlalchemy_training_repository import SqlAlchemyTrainingRepository
from infrastructure.db.session import SessionLocal
from infrastructure.db.repositories.sqlalchemy_attendance_repository import SqlAlchemyAttendanceRepository


def test_save_batch_rolls_back_entirely_on_duplicate():
    session = SessionLocal()
    repo = SqlAlchemyAttendanceRepository(session)
    repo_player = SqlAlchemyPlayerRepository(session)

    repo_training = SqlAlchemyTrainingRepository(session)
    training = Training(id=0, date=date(2026, 8, 1), start_time=time(18, 0), end_time=time(19, 0), location="Стадион теста")
    saved_training = repo_training.save(training)

    now = datetime.now()
    player = Player(id=1,first_name='Al',last_name='Dol',birth_date=date(2016, 7, 12),position=Position.FORWARD)
    repo_player.save(player)
    attendances = [
        Attendance(id=0, player_id=1, training_id=saved_training.id, status=AttendanceStatus.PRESENT, marked_at=now),
        Attendance(id=0, player_id=1, training_id=saved_training.id, status=AttendanceStatus.ABSENT, marked_at=now),  # дубликат player_id+training_id
    ]

    with pytest.raises(IntegrityError):
        repo.save_batch(attendances)

    session.rollback()  # откатываем "зависшую" транзакцию перед следующей проверкой

    assert repo.get_by_training_id(saved_training.id) == []

    session.close()