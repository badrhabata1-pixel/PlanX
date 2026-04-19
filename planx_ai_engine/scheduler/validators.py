from __future__ import annotations

from typing import List

from scheduler.hard_constraints import exams_conflict


def validate_phase4_schedule(bundle, phase3_result, stabilized_phase35, schedule_result) -> List[str]:
    """
    Validate the Phase 4 feasible schedule.
    """
    messages: List[str] = []

    total_exams = len(stabilized_phase35.stabilized_exams)
    assigned_count = len(schedule_result.assignments)
    unassigned_count = len(schedule_result.unassigned_exams)

    if assigned_count + unassigned_count != total_exams:
        raise ValueError(
            "Phase 4 validation failed: assigned + unassigned does not match total exams."
        )

    messages.append(
        f"Assignment coverage validated: {assigned_count} assigned + {unassigned_count} unassigned = {total_exams}"
    )

    # Validate no room duplication per slot
    for slot_id, room_ids in schedule_result.room_usage_by_slot.items():
        if len(room_ids) != len(set(room_ids)):
            raise ValueError(
                f"Phase 4 validation failed: duplicate room usage detected in slot {slot_id}."
            )

    messages.append("Room usage uniqueness validation passed.")

    # Validate no conflicting exams in same slot
    for slot_id, course_codes in schedule_result.slot_to_course_codes.items():
        for i in range(len(course_codes)):
            for j in range(i + 1, len(course_codes)):
                a = course_codes[i]
                b = course_codes[j]
                if exams_conflict(a, b, phase3_result.conflict_matrix):
                    raise ValueError(
                        f"Phase 4 validation failed: conflict detected in slot {slot_id} between {a} and {b}."
                    )

    messages.append("Student conflict validation passed.")

    # Validate assignment room capacity
    exam_by_code = {
        exam.course_code: exam
        for exam in stabilized_phase35.stabilized_exams
    }

    for course_code, assignment in schedule_result.assignments.items():
        exam = exam_by_code[course_code]
        if assignment.total_capacity < exam.student_count:
            raise ValueError(
                f"Phase 4 validation failed: insufficient room capacity for {course_code}."
            )

    messages.append("Capacity validation passed.")
    messages.append("Phase 4 feasible schedule validation completed successfully.")

    return messages