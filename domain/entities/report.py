from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class ReportStatus(str, Enum):
    PENDING = "pending"    # задача поставлена в очередь (Celery/RQ)
    READY = "ready"
    FAILED = "failed"


@dataclass
class Report:
    id: int
    period_start: date
    period_end: date
    status: ReportStatus
    created_at: datetime
    file_path: str | None = None  # путь к сгенерированному файлу (когда status = READY)