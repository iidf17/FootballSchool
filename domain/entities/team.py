from dataclasses import dataclass
from domain.exceptions import DomainError

class InvalidAgeRangeError(DomainError):
    pass


@dataclass
class Team:
    id: int
    name: str
    min_age: int
    max_age: int

    def __post_init__(self):
        if self.min_age >= self.max_age:
            raise InvalidAgeRangeError(
                f"min_age ({self.min_age}) должен быть меньше max_age ({self.max_age})"
            )