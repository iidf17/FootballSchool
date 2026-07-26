from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


@dataclass
class Attendance:
    id: int
    player_id: int
    training_id: int
    status: AttendanceStatus
    marked_at: datetime