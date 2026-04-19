from __future__ import annotations

from scheduler.state import ExamAssignment, ScheduleResult
from scheduler.hard_constraints import slot_accepts_exam, has_student_conflict_in_slot
from scheduler.room_selector import select_rooms_for_exam


def build_feasible_schedule(bundle, phase3_result, stabilized_phase35) -> ScheduleResult:
    """
    Phase 4A:
    Build the first feasible schedule using a priority-based greedy constructor.
    """
    result = ScheduleResult()

    exams = list(stabilized_phase35.stabilized_exams)
    slots = list(bundle.date_period_slots)
    room_rows = list(stabilized_phase35.stabilized_room_availability)
    priority_scores = phase3_result.exam_priority_scores

    # Sort exams by:
    # 1) priority score descending
    # 2) student count descending
    exams.sort(
        key=lambda exam: (
            priority_scores.get(exam.course_code, 0),
            exam.student_count,
        ),
        reverse=True,
    )

    for exam in exams:
        assigned = False

        for slot in slots:
            if not slot_accepts_exam(exam, slot):
                continue

            if has_student_conflict_in_slot(
                exam=exam,
                slot_id=slot.slot_id,
                schedule_result=result,
                conflict_matrix=phase3_result.conflict_matrix,
            ):
                continue

            selected_rooms = select_rooms_for_exam(
                exam=exam,
                slot=slot,
                stabilized_room_availability=room_rows,
                room_usage_by_slot=result.room_usage_by_slot,
            )

            if not selected_rooms:
                continue

            assignment = ExamAssignment(
                exam_id=exam.exam_id,
                course_code=exam.course_code,
                course_name=exam.course_name,
                slot_id=slot.slot_id,
                date=slot.date,
                day_name=slot.day_name,
                period_id=slot.period_id,
                start_time=slot.start_time,
                end_time=slot.end_time,
                room_ids=[room.room_id for room in selected_rooms],
                total_capacity=sum(room.capacity for room in selected_rooms),
            )

            result.assignments[exam.course_code] = assignment
            result.slot_to_course_codes.setdefault(slot.slot_id, []).append(exam.course_code)
            result.room_usage_by_slot.setdefault(slot.slot_id, set()).update(
                room.room_id for room in selected_rooms
            )

            assigned = True
            break

        if not assigned:
            result.unassigned_exams.append(exam.course_code)

    result.messages.append(
        f"Assigned exams: {len(result.assignments)} / {len(exams)}"
    )
    result.messages.append(
        f"Unassigned exams: {len(result.unassigned_exams)}"
    )

    return result