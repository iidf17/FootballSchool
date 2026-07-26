from fastapi import Depends
from sqlalchemy.orm import Session
from application.use_cases.create_player import CreatePlayerUseCase
from application.use_cases.create_training import CreateTrainingUseCase
from application.use_cases.mark_attendance import MarkAttendanceUseCase
from infrastructure.db.repositories.sqlalchemy_attendance_repository import SqlAlchemyAttendanceRepository
from infrastructure.db.repositories.sqlalchemy_player_repository import SqlAlchemyPlayerRepository
from infrastructure.db.session import get_db_session
from infrastructure.db.repositories.sqlalchemy_training_repository import SqlAlchemyTrainingRepository


def get_training_repository(
    session: Session = Depends(get_db_session)
) -> SqlAlchemyTrainingRepository:
    return SqlAlchemyTrainingRepository(session)


def get_create_training_use_case(
    repository: SqlAlchemyTrainingRepository = Depends(get_training_repository)
) -> CreateTrainingUseCase:
    return CreateTrainingUseCase(repository)


def get_attendance_repository(
    session: Session = Depends(get_db_session)
) -> SqlAlchemyAttendanceRepository:
    return SqlAlchemyAttendanceRepository(session)


def get_mark_attendance_use_case(
    attendance_repository: SqlAlchemyAttendanceRepository = Depends(get_attendance_repository),
    training_repository: SqlAlchemyTrainingRepository = Depends(get_training_repository),
) -> MarkAttendanceUseCase:
    return MarkAttendanceUseCase(attendance_repository, training_repository)


def get_player_repository(
    session: Session = Depends(get_db_session)
) -> SqlAlchemyPlayerRepository:
    return SqlAlchemyPlayerRepository(session)


def get_create_player_use_case(
    repository: SqlAlchemyPlayerRepository = Depends(get_player_repository)
) -> CreatePlayerUseCase:
    return CreatePlayerUseCase(repository)
