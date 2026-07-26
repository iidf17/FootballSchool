from dataclasses import dataclass
from domain.entities.attendance import AttendanceStatus


@dataclass
class AttendanceMarkRequest:
    player_id: int
    status: AttendanceStatus