from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class PenaltyComponent:
    name: str
    penalty: int
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SoftConstraintWeights:
    consecutive_exams: int = 10
    same_day_multiple_exams: int = 6
    crowded_day: int = 3
    room_underutilization: int = 1
    excessive_room_splitting: int = 2


def evaluate_soft_constraints(
    data_bundle: Any,
    schedule_result: Any,
    weights: SoftConstraintWeights | None = None,
) -> List[PenaltyComponent]:
    """
    Main entry point for Phase 5 soft constraint evaluation.
    Returns a list of penalty components. Total score is computed later
    by evaluator.py.
    """
    weights = weights or SoftConstraintWeights()

    components: List[PenaltyComponent] = []

    student_exam_map = _build_student_exam_map(data_bundle, schedule_result)
    slot_index_map = _build_slot_index_map(data_bundle)
    exams_by_day = _build_exams_by_day(schedule_result)

    components.append(
        penalty_consecutive_exams(
            student_exam_map=student_exam_map,
            slot_index_map=slot_index_map,
            weight=weights.consecutive_exams,
        )
    )

    components.append(
        penalty_same_day_multiple_exams(
            student_exam_map=student_exam_map,
            weight=weights.same_day_multiple_exams,
        )
    )

    components.append(
        penalty_crowded_days(
            exams_by_day=exams_by_day,
            weight=weights.crowded_day,
        )
    )

    components.append(
        penalty_room_underutilization(
            data_bundle=data_bundle,
            schedule_result=schedule_result,
            weight=weights.room_underutilization,
        )
    )

    components.append(
        penalty_excessive_room_splitting(
            schedule_result=schedule_result,
            weight=weights.excessive_room_splitting,
        )
    )

    return components


def penalty_consecutive_exams(
    student_exam_map: Dict[str, List[Dict[str, Any]]],
    slot_index_map: Dict[str, int],
    weight: int,
) -> PenaltyComponent:
    """
    Penalize students having exams in consecutive slots on the same day.
    """
    consecutive_count = 0
    affected_students = 0

    for student_id, exams in student_exam_map.items():
        sorted_exams = sorted(
            exams,
            key=lambda x: slot_index_map.get(x["slot_id"], 10**9)
        )

        local_hits = 0
        for i in range(len(sorted_exams) - 1):
            current_exam = sorted_exams[i]
            next_exam = sorted_exams[i + 1]

            if current_exam["date"] != next_exam["date"]:
                continue

            current_slot_index = slot_index_map.get(current_exam["slot_id"])
            next_slot_index = slot_index_map.get(next_exam["slot_id"])

            if (
                current_slot_index is not None
                and next_slot_index is not None
                and next_slot_index - current_slot_index == 1
            ):
                local_hits += 1

        if local_hits > 0:
            affected_students += 1
            consecutive_count += local_hits

    return PenaltyComponent(
        name="consecutive_exams",
        penalty=consecutive_count * weight,
        details={
            "violations": consecutive_count,
            "affected_students": affected_students,
            "weight": weight,
        },
    )


def penalty_same_day_multiple_exams(
    student_exam_map: Dict[str, List[Dict[str, Any]]],
    weight: int,
) -> PenaltyComponent:
    """
    Penalize students having more than one exam on the same day.
    """
    violation_units = 0
    affected_students = 0

    for student_id, exams in student_exam_map.items():
        exams_per_day: Dict[str, int] = defaultdict(int)
        for exam in exams:
            exams_per_day[exam["date"]] += 1

        local_units = 0
        for _, count in exams_per_day.items():
            if count > 1:
                # penalize extras beyond the first exam of the day
                local_units += (count - 1)

        if local_units > 0:
            affected_students += 1
            violation_units += local_units

    return PenaltyComponent(
        name="same_day_multiple_exams",
        penalty=violation_units * weight,
        details={
            "violations": violation_units,
            "affected_students": affected_students,
            "weight": weight,
        },
    )


def penalty_crowded_days(
    exams_by_day: Dict[str, List[str]],
    weight: int,
) -> PenaltyComponent:
    """
    Penalize imbalance across days.
    A day is considered crowded if it exceeds the average number of exams.
    """
    if not exams_by_day:
        return PenaltyComponent(
            name="crowded_days",
            penalty=0,
            details={"violations": 0, "weight": weight},
        )

    total_exams = sum(len(exams) for exams in exams_by_day.values())
    total_days = len(exams_by_day)
    average = total_exams / total_days

    crowded_units = 0
    crowded_days = {}

    for day, exams in exams_by_day.items():
        extra = max(0, len(exams) - int(average))
        if extra > 0:
            crowded_units += extra
            crowded_days[day] = {
                "exam_count": len(exams),
                "average": average,
                "extra": extra,
            }

    return PenaltyComponent(
        name="crowded_days",
        penalty=crowded_units * weight,
        details={
            "violations": crowded_units,
            "crowded_days": crowded_days,
            "weight": weight,
        },
    )


def penalty_room_underutilization(
    data_bundle: Any,
    schedule_result: Any,
    weight: int,
) -> PenaltyComponent:
    """
    Penalize large unused room capacity relative to assigned exam size.
    Assumes:
      - schedule_result.assignments[course_code].room_ids
      - schedule_result.assignments[course_code].total_capacity
      - data_bundle.exam_offerings iterable with students_no
    """
    exam_size_map = _build_exam_size_map(data_bundle)

    total_unused_capacity = 0
    affected_exams = 0

    for course_code, assignment in schedule_result.assignments.items():
        assigned_capacity = getattr(assignment, "total_capacity", 0)
        exam_size = exam_size_map.get(course_code, 0)

        if assigned_capacity > exam_size:
            unused = assigned_capacity - exam_size
            total_unused_capacity += unused
            affected_exams += 1

    return PenaltyComponent(
        name="room_underutilization",
        penalty=total_unused_capacity * weight,
        details={
            "unused_capacity": total_unused_capacity,
            "affected_exams": affected_exams,
            "weight": weight,
        },
    )


def penalty_excessive_room_splitting(
    schedule_result: Any,
    weight: int,
) -> PenaltyComponent:
    """
    Penalize exams split across many rooms.
    The first room is normal; extra rooms add small penalty.
    """
    split_units = 0
    affected_exams = 0

    for _, assignment in schedule_result.assignments.items():
        room_ids = getattr(assignment, "room_ids", []) or []
        if len(room_ids) > 1:
            affected_exams += 1
            split_units += (len(room_ids) - 1)

    return PenaltyComponent(
        name="excessive_room_splitting",
        penalty=split_units * weight,
        details={
            "violations": split_units,
            "affected_exams": affected_exams,
            "weight": weight,
        },
    )


def _build_student_exam_map(
    data_bundle: Any,
    schedule_result: Any,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Returns:
        {
            student_id: [
                {
                    "course_code": ...,
                    "slot_id": ...,
                    "date": ...,
                    "period_id": ...
                },
                ...
            ]
        }
    """
    assignments = schedule_result.assignments
    student_exam_map: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for enrollment in data_bundle.enrollments:
        course_code = enrollment.course_code
        if course_code not in assignments:
            continue

        assignment = assignments[course_code]
        student_exam_map[enrollment.student_id].append(
            {
                "course_code": course_code,
                "slot_id": assignment.slot_id,
                "date": assignment.date,
                "period_id": assignment.period_id,
            }
        )

    return student_exam_map


def _build_slot_index_map(data_bundle: Any) -> Dict[str, int]:
    """
    Build stable ordering for slots using date-period slots if available.
    Falls back to periods ordering if needed.
    """
    slot_index_map: Dict[str, int] = {}

    # Preferred: data_bundle.date_period_slots
    date_period_slots = getattr(data_bundle, "date_period_slots", None)
    if date_period_slots:
        for idx, slot in enumerate(date_period_slots):
            slot_id = getattr(slot, "slot_id", None)
            if slot_id is not None:
                slot_index_map[slot_id] = idx
        return slot_index_map

    # Fallback: derive from periods if they already encode date/order
    periods = getattr(data_bundle, "periods", [])
    for idx, period in enumerate(periods):
        slot_id = getattr(period, "slot_id", None)
        if slot_id is not None:
            slot_index_map[slot_id] = idx

    return slot_index_map


def _build_exams_by_day(schedule_result: Any) -> Dict[str, List[str]]:
    exams_by_day: Dict[str, List[str]] = defaultdict(list)

    for course_code, assignment in schedule_result.assignments.items():
        exams_by_day[assignment.date].append(course_code)

    return exams_by_day


def _build_exam_size_map(data_bundle: Any) -> Dict[str, int]:
    exam_size_map: Dict[str, int] = {}

    for exam in getattr(data_bundle, "exam_offerings", []):
        students_no = getattr(exam, "students_no", 0)
        exam_size_map[exam.course_code] = students_no

    return exam_size_map