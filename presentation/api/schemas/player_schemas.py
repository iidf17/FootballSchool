from datetime import date
from pydantic import BaseModel
from domain.entities.player import Position, PlayerStatus


class PlayerCreateSchema(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    position: Position
    season_start_date: date


class PlayerResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    position: Position
    status: PlayerStatus

    model_config = {"from_attributes": True}