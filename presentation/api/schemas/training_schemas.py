# presentation/api/schemas/training_schemas.py
from datetime import date, time
from pydantic import BaseModel, field_validator, model_validator


class TrainingCreateSchema(BaseModel):
    date: date
    start_time: time
    end_time: time
    location: str

    @field_validator('date')
    @classmethod
    def date_not_in_past(cls, value: date) -> date: # type: ignore
        if value < date.today():
            raise ValueError("Дата не может быть прошлым числом")
        return value

    @model_validator(mode='after')
    def check_times(self) -> 'TrainingCreateSchema':
        if self.end_time <= self.start_time:
            raise ValueError("Конец тренировки не может быть раньше начала")
        return self


class TrainingResponseSchema(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time
    location: str

    model_config = {"from_attributes": True}