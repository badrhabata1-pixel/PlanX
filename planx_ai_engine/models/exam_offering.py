from dataclasses import dataclass


@dataclass
class ExamOffering:
    """
    Represents the exam instance for a specific semester/term.
    This is NOT the general course entity.
    It contains semester-specific exam requirements.
    """
    exam_id: str
    course_code: str
    course_name: str
    student_count: int
    exam_mode: str
    duration_minutes: int
    allowed_room_type: str
    splitting_allowed: bool = True
    max_rooms: int | None = None
    fixed_period_id: str | None = None

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExamOffering:
    course_code: str
    course_name: str
    students_no: int
    academic_semester: Optional[str] = None