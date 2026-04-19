from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class ExamAssignment:
    exam_id: str
    course_code: str
    course_name: str
    slot_id: str
    date: str
    day_name: str
    period_id: str
    start_time: str
    end_time: str
    room_ids: List[str]
    total_capacity: int


@dataclass
class ScheduleResult:
    assignments: Dict[str, ExamAssignment] = field(default_factory=dict)
    unassigned_exams: List[str] = field(default_factory=list)

    # slot_id -> list of assigned course_codes
    slot_to_course_codes: Dict[str, List[str]] = field(default_factory=dict)

    # slot_id -> set of occupied room_ids
    room_usage_by_slot: Dict[str, Set[str]] = field(default_factory=dict)

    messages: List[str] = field(default_factory=list)