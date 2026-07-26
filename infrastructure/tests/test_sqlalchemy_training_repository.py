# infrastructure/tests/test_sqlalchemy_training_repository.py
from datetime import date, time
from domain.entities.training import Training
from infrastructure.db.session import SessionLocal
from infrastructure.db.repositories.sqlalchemy_training_repository import SqlAlchemyTrainingRepository


def test_save_and_get_by_id():
    session = SessionLocal()
    repo = SqlAlchemyTrainingRepository(session)

    training = Training(
        id=0,  # заглушка, репозиторий сам присвоит настоящий id
        date=date(2026, 8, 1),
        start_time=time(18, 0),
        end_time=time(19, 0),
        location="Тестовый стадион",
    )

    saved = repo.save(training)
    
    assert saved.id != 0
    assert repo.get_by_id(saved.id).location == "Тестовый стадион"

    session.close()