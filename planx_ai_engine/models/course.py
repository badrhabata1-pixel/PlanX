from dataclasses import dataclass


@dataclass
class Course:
    """
    Represents the stable course entity.
    This is the academic course itself, not the specific exam in a semester.
    """
    course_code: str
    course_name: str
    department: str | None = None
    level: str | None = None

from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    course_code: str
    course_name: str
    academic_semester: Optional[str] = None