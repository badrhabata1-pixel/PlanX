from dataclasses import dataclass
from typing import Optional


@dataclass
class LevelPolicy:
    level_id: int
    level_name: str
    exam_group: str
    allowed_exam_days: str
    min_gap_days_between_exams: int
    max_exams_per_day: int
    notes: Optional[str] = None