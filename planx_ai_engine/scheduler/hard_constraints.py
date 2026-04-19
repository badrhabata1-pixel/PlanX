from __future__ import annotations


def slot_accepts_exam(exam, slot) -> bool:
    """
    Check slot-level hard conditions.
    """
    if not getattr(slot, "is_schedulable_by_default", True):
        return False

    fixed_period_id = getattr(exam, "fixed_period_id", None)
    if fixed_period_id is not None and slot.period_id != fixed_period_id:
        return False

    return True


def exams_conflict(course_a: str, course_b: str, conflict_matrix: dict) -> bool:
    """
    Two exams conflict if they share at least one student.
    """
    return conflict_matrix.get((course_a, course_b), 0) > 0


def has_student_conflict_in_slot(
    exam,
    slot_id: str,
    schedule_result,
    conflict_matrix: dict,
) -> bool:
    """
    Check whether assigning this exam to this slot would create
    a student conflict with already assigned exams in the same slot.
    """
    assigned_courses = schedule_result.slot_to_course_codes.get(slot_id, [])

    for assigned_course in assigned_courses:
        if exams_conflict(exam.course_code, assigned_course, conflict_matrix):
            return True

    return False


def room_matches_exam(room_row, exam) -> bool:
    """
    Basic room-type compatibility.
    """
    required_type = getattr(exam, "allowed_room_type", "").strip().lower()
    actual_type = getattr(room_row, "room_type", "").strip().lower()

    if required_type in ("", "any"):
        return True

    return required_type == actual_type


def can_rooms_host_exam(exam, selected_rooms: list) -> bool:
    """
    Check capacity + splitting rules.
    """
    if not selected_rooms:
        return False

    total_capacity = sum(room.capacity for room in selected_rooms)

    if total_capacity < exam.student_count:
        return False

    if not getattr(exam, "splitting_allowed", True) and len(selected_rooms) > 1:
        return False

    max_rooms = getattr(exam, "max_rooms", None)
    if max_rooms is not None and len(selected_rooms) > max_rooms:
        return False

    return True