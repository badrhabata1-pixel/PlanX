from dataclasses import dataclass
from typing import Optional


@dataclass
class CalendarDay:
    date: str
    day_name: str
    is_exam_day: bool
    is_holiday: bool
    holiday_name: Optional[str] = None
    notes: Optional[str] = None