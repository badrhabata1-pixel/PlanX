from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class StabilizedExam:
    """
    Scheduling-ready exam object produced in Phase 3.5
    without changing the original ingestion model.
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
    academic_semester: str | None = None


@dataclass
class StabilizedPeriod:
    """
    Scheduling-ready period object produced in Phase 3.5
    without changing the original Period model.
    """
    period_id: str
    start_time: str
    end_time: str
    duration_minutes: int
    allowed_exam_modes: List[str]


@dataclass
class StabilizedRoomAvailability:
    """
    Canonical room availability row with unified internal room identifier.
    We call it room_id internally, even if the raw source used room_code.
    """
    room_id: str
    room_name: str
    room_type: str
    capacity: int
    date: str
    day_name: str
    period_id: str
    start_time: str
    end_time: str
    slot_type: str
    is_available: bool
    notes: str | None = None


@dataclass
class Phase35StabilizedData:
    """
    Final Phase 3.5 output package.
    This is the clean layer that Phase 4 will consume.
    """
    stabilized_exams: List[StabilizedExam]
    stabilized_periods: List[StabilizedPeriod]
    stabilized_room_availability: List[StabilizedRoomAvailability]


def infer_exam_attributes(student_count: int) -> tuple[str, int, str]:
    """
    Infer basic exam attributes from observed university timetable patterns.

    Current lightweight rule set:
    - small exams: often placed in labs / small rooms
    - medium exams: mixed usage is common
    - large exams: must not be restricted to halls only, because
      real university schedules often use halls + labs + other rooms

    Returns:
        (exam_mode, duration_minutes, allowed_room_type)
    """
    if student_count <= 50:
        return "essay", 60, "lab"

    if student_count <= 300:
        return "mixed", 90, "any"

    return "mixed", 90, "any"


def stabilize_exam_offerings(raw_exam_offerings: List[object]) -> List[StabilizedExam]:
    """
    Upgrade simple/raw exam offerings into scheduling-ready objects
    without changing the original raw model.

    Expected currently available raw fields:
    - course_code
    - course_name
    - students_no
    - academic_semester
    """
    result: List[StabilizedExam] = []

    for eo in raw_exam_offerings:
        student_count = int(getattr(eo, "students_no", 0))
        exam_mode, duration_minutes, allowed_room_type = infer_exam_attributes(student_count)

        result.append(
            StabilizedExam(
                exam_id=f"EXAM-{eo.course_code}",
                course_code=eo.course_code,
                course_name=eo.course_name,
                student_count=student_count,
                exam_mode=exam_mode,
                duration_minutes=duration_minutes,
                allowed_room_type=allowed_room_type,
                splitting_allowed=True,
                max_rooms=None,
                fixed_period_id=None,
                academic_semester=getattr(eo, "academic_semester", None),
            )
        )

    return result


def stabilize_periods(raw_periods: List[object]) -> List[StabilizedPeriod]:
    """
    Upgrade simple/raw periods into scheduling-ready objects.

    Expected currently available raw fields:
    - period_id
    - start_time
    - end_time
    """
    result: List[StabilizedPeriod] = []

    for p in raw_periods:
        result.append(
            StabilizedPeriod(
                period_id=p.period_id,
                start_time=p.start_time,
                end_time=p.end_time,
                duration_minutes=120,
                allowed_exam_modes=[],
            )
        )

    return result


def normalize_room_availability(
    rooms: List[object],
    availability_rows: List[object],
) -> List[StabilizedRoomAvailability]:
    """
    Normalize room availability rows so Phase 4 can rely on one canonical
    internal room identifier.

    Matching strategy:
    1. row.room_code == room.room_id OR room.room_code
    2. fallback: row.room_name == room.room_name

    This keeps Phase 3.5 compatible with the current project state,
    where some room models may use room_id and others may use room_code.
    """

    def get_room_internal_id(room: object) -> str:
        """
        Return the canonical internal identifier for a room,
        supporting both room_id and room_code.
        """
        return getattr(room, "room_id", getattr(room, "room_code", "")).strip()

    room_id_by_name = {
        room.room_name.strip().lower(): get_room_internal_id(room)
        for room in rooms
    }

    valid_room_ids = {
        get_room_internal_id(room)
        for room in rooms
    }

    normalized: List[StabilizedRoomAvailability] = []

    for row in availability_rows:
        raw_room_name = row.room_name.strip()
        raw_room_code = getattr(row, "room_code", "").strip()

        normalized_room_id = None

        if raw_room_code in valid_room_ids:
            normalized_room_id = raw_room_code
        else:
            normalized_room_id = room_id_by_name.get(raw_room_name.lower())

        if normalized_room_id is None:
            raise ValueError(
                f"Phase 3.5 normalization failed: could not map room availability row "
                f"to room identifier (room_name='{raw_room_name}', room_code='{raw_room_code}')."
            )

        normalized.append(
            StabilizedRoomAvailability(
                room_id=normalized_room_id,
                room_name=raw_room_name,
                room_type=row.room_type,
                capacity=int(row.capacity),
                date=row.date,
                day_name=row.day_name,
                period_id=row.period_id,
                start_time=row.start_time,
                end_time=row.end_time,
                slot_type=row.slot_type,
                is_available=bool(row.is_available),
                notes=row.notes,
            )
        )

    return normalized


def stabilize_phase35(bundle) -> Phase35StabilizedData:
    """
    Full Phase 3.5 stabilization entry point.

    Takes the existing Phase 2/3 bundle as-is and produces a clean,
    scheduler-ready layer for Phase 4.
    """
    stabilized_exams = stabilize_exam_offerings(bundle.exam_offerings)
    stabilized_periods = stabilize_periods(bundle.periods)
    stabilized_room_availability = normalize_room_availability(
        bundle.rooms,
        bundle.room_availability,
    )

    return Phase35StabilizedData(
        stabilized_exams=stabilized_exams,
        stabilized_periods=stabilized_periods,
        stabilized_room_availability=stabilized_room_availability,
    )