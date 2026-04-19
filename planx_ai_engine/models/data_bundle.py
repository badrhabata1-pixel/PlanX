from dataclasses import dataclass, field
from typing import List

from models.course import Course
from models.student import Student
from models.enrollment import Enrollment
from models.exam_offering import ExamOffering
from models.room import Room
from models.period import Period
from models.calendar_day import CalendarDay
from models.date_period_slot import DatePeriodSlot
from models.level_policy import LevelPolicy
from models.exam_rule import ExamRule
from models.system_assumption import SystemAssumption
from models.room_availability import RoomAvailability


@dataclass
class PlanXDataBundle:
    courses: List[Course] = field(default_factory=list)
    students: List[Student] = field(default_factory=list)
    enrollments: List[Enrollment] = field(default_factory=list)
    exam_offerings: List[ExamOffering] = field(default_factory=list)
    rooms: List[Room] = field(default_factory=list)
    periods: List[Period] = field(default_factory=list)
    calendar_days: List[CalendarDay] = field(default_factory=list)
    date_period_slots: List[DatePeriodSlot] = field(default_factory=list)
    level_policies: List[LevelPolicy] = field(default_factory=list)
    exam_rules: List[ExamRule] = field(default_factory=list)
    system_assumptions: List[SystemAssumption] = field(default_factory=list)
    room_availability: List[RoomAvailability] = field(default_factory=list)