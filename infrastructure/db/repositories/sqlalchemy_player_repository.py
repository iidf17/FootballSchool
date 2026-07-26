# infrastructure/db/repositories/sqlalchemy_player_repository.py
from sqlalchemy.orm import Session
from domain.entities.player import Player, Position, PlayerStatus
from infrastructure.db.models import PlayerModel


class SqlAlchemyPlayerRepository:
    def __init__(self, session: Session):
        self._session = session

    def _to_domain(self, model: PlayerModel) -> Player:
        return Player(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            birth_date=model.birth_date,
            position=Position(model.position),
            status=PlayerStatus(model.status)
        )

    def _to_model(self, entity: Player) -> PlayerModel:
        return PlayerModel(
            first_name=entity.first_name,
            last_name=entity.last_name,
            birth_date=entity.birth_date,
            position=entity.position.value,
            status=entity.status.value
        )

    def get_by_id(self, player_id: int) -> Player | None:
        model = self._session.get(PlayerModel, player_id)
        if model is None:
            return None
        return self._to_domain(model)

    def get_all(self) -> list[Player]:
        models = self._session.query(PlayerModel).all()
        return [self._to_domain(m) for m in models]

    def save(self, player: Player) -> Player:
        model = self._to_model(player)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)