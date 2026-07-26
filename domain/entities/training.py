from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Training:
    id: int
    date: date
    start_time: time
    end_time: time
    location: str
    team_ids: list[int] = field(default_factory=list)

    def _teams_overlap(self, other: "Training") -> bool:
        if not self.team_ids or not other.team_ids:
            # пустой список = "для всех групп" → всегда пересекается с любой
            return True
        return bool(set(self.team_ids) & set(other.team_ids))

    def overlaps_with(self, other: "Training") -> bool:
        if self.date != other.date:
            return False
        time_overlap = self.start_time < other.end_time and other.start_time < self.end_time
        return time_overlap and self._teams_overlap(other)