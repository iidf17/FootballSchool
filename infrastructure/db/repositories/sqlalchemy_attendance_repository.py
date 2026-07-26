# infrastructure/db/repositories/sqlalchemy_attendance_repository.py
from sqlalchemy.orm import Session
from domain.entities.attendance import Attendance, AttendanceStatus
from infrastructure.db.models import AttendanceModel


class SqlAlchemyAttendanceRepository:
    def __init__(self, session: Session):
        self._session = session

    def _to_domain(self, model: AttendanceModel) -> Attendance:
        return Attendance(
            id=model.id,
            player_id=model.player_id,
            training_id=model.training_id,
            status=AttendanceStatus(model.status),
            marked_at=model.marked_at
        )

    def _to_model(self, entity: Attendance) -> AttendanceModel:
        return AttendanceModel(
            player_id=entity.player_id,
            training_id=entity.training_id,
            status=entity.status.value,
            marked_at=entity.marked_at
        )

    def get_by_training_id(self, training_id: int) -> list[Attendance]:
        models = (
            self._session.query(AttendanceModel)
            .filter(AttendanceModel.training_id == training_id)
            .all()
        )
        return [self._to_domain(m) for m in models]

    def save_batch(self, attendances: list[Attendance]) -> list[Attendance]:
        models = []
        for a in attendances:
            models.append(self._to_model(a))
        self._session.add_all(models)
        self._session.commit()
        at = []
        for model in models:
            self._session.refresh(model)
            at.append(self._to_domain(model))
        return at