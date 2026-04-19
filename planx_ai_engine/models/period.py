from dataclasses import dataclass, field
from typing import List


@dataclass
class Period:
    """
    Represents a valid exam time slot.
    """
    period_id: str
    exam_date: str
    start_time: str
    end_time: str
    duration_minutes: int
    allowed_exam_modes: List[str] = field(default_factory=list)

from dataclasses import dataclass


@dataclass
class Period:
    period_id: str
    start_time: str
    end_time: str