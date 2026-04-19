from dataclasses import dataclass


@dataclass
class Student:
    """
    Represents a student in the system.
    """
    student_id: str
    student_name: str | None = None
    level: str | None = None
    department: str | None = None

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    student_id: str
    student_name: str
    level_text: Optional[str] = None
    cgpa: Optional[float] = None