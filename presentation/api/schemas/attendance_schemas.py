from datetime import datetime

from pydantic import BaseModel
from domain.entities.attendance import AttendanceStatus


class AttendanceMarkItemSchema(BaseModel):
    player_id: int
    status: AttendanceStatus


class AttendanceMarkRequestSchema(BaseModel):
    items: list[AttendanceMarkItemSchema]


class AttendanceResponseSchema(BaseModel):
    id: int
    player_id: int
    training_id: int
    status: AttendanceStatus
    marked_at: "datetime"

    model_config = {"from_attributes": True}