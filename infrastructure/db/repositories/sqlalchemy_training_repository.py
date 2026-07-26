# infrastructure/db/repositories/sqlalchemy_training_repository.py
from datetime import date
from sqlalchemy.orm import Session
from domain.entities.training import Training
from infrastructure.db.models import TrainingModel


class SqlAlchemyTrainingRepository:
    def __init__(self, session: Session):
        self._session = session

    def _to_domain(self, model: TrainingModel) -> Training:
        # твоя задача: превратить TrainingModel в Training
        return Training(
            id=model.id,
            date=model.date, 
            start_time=model.start_time,
            end_time=model.end_time,
            location=model.location
        )

    def _to_model(self, entity: Training) -> TrainingModel:
        # твоя задача: превратить Training в TrainingModel (для сохранения)
        return TrainingModel(
            date=entity.date, 
            start_time=entity.start_time,
            end_time=entity.end_time,
            location=entity.location
        )

    def get_by_id(self, training_id: int) -> Training | None:
        model = self._session.get(TrainingModel, training_id)
        if model is None:
            return None
        return self._to_domain(model)

    def get_all(self) -> list[Training]:
        models = self._session.query(TrainingModel).all()
        return [self._to_domain(m) for m in models]

    def get_by_date_range(self, start: date, end: date) -> list[Training]:
        models = (
            self._session.query(TrainingModel)
            .filter(TrainingModel.date >= start, TrainingModel.date <= end)
            .all()
        )
        return [self._to_domain(m) for m in models]

    def save(self, training: Training) -> Training:
        model = self._to_model(training)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)