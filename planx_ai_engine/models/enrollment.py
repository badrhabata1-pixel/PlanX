from dataclasses import dataclass


@dataclass
class Enrollment:
    """
    Represents the relationship between a student and a course.
    Each row means: one student is enrolled in one course.
    """
    student_id: str
    course_code: str

from dataclasses import dataclass


@dataclass
class Enrollment:
    student_id: str
    course_code: str