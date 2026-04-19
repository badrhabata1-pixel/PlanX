from __future__ import annotations

from scheduler.state import ExamAssignment
from scheduler.hard_constraints import slot_accepts_exam, has_student_conflict_in_slot
from scheduler.room_selector import select_rooms_for_exam


def _find_exam_by_course_code(stabilized_phase35, course_code: str):
    for exam in stabilized_phase35.stabilized_exams:
        if exam.course_code == course_code:
            return exam
    return None


def _find_assignment_by_course_code(schedule_result, course_code: str):
    return schedule_result.assignments.get(course_code)


def _remove_assignment(schedule_result, course_code: str):
    """
    Remove an existing assignment cleanly from schedule state.
    Returns the removed assignment object, or None.
    """
    assignment = schedule_result.assignments.pop(course_code, None)
    if assignment is None:
        return None

    slot_courses = schedule_result.slot_to_course_codes.get(assignment.slot_id, [])
    if course_code in slot_courses:
        slot_courses.remove(course_code)

    used_rooms = schedule_result.room_usage_by_slot.get(assignment.slot_id, set())
    for room_id in assignment.room_ids:
        used_rooms.discard(room_id)

    return assignment


def _add_assignment(schedule_result, exam, slot, selected_rooms):
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

    schedule_result.assignments[exam.course_code] = assignment
    schedule_result.slot_to_course_codes.setdefault(slot.slot_id, []).append(exam.course_code)
    schedule_result.room_usage_by_slot.setdefault(slot.slot_id, set()).update(
        room.room_id for room in selected_rooms
    )


def _restore_removed_assignment(schedule_result, exam, removed_assignment):
    """
    Restore a previously removed assignment exactly as it was.
    """
    schedule_result.assignments[exam.course_code] = removed_assignment
    schedule_result.slot_to_course_codes.setdefault(removed_assignment.slot_id, []).append(exam.course_code)
    schedule_result.room_usage_by_slot.setdefault(removed_assignment.slot_id, set()).update(
        removed_assignment.room_ids
    )


def _sorted_slots_for_repair(bundle, schedule_result):
    """
    Prefer slots with fewer already assigned exams first,
    because they are easier to fit into.
    """
    slots = list(bundle.date_period_slots)

    slots.sort(
        key=lambda slot: len(schedule_result.slot_to_course_codes.get(slot.slot_id, []))
    )
    return slots


def _try_direct_insert(exam, slots, room_rows, phase3_result, schedule_result):
    """
    Try assigning an exam directly without disturbing current assignments.
    """
    for slot in slots:
        if not slot_accepts_exam(exam, slot):
            continue

        if has_student_conflict_in_slot(
            exam=exam,
            slot_id=slot.slot_id,
            schedule_result=schedule_result,
            conflict_matrix=phase3_result.conflict_matrix,
        ):
            continue

        selected_rooms = select_rooms_for_exam(
            exam=exam,
            slot=slot,
            stabilized_room_availability=room_rows,
            room_usage_by_slot=schedule_result.room_usage_by_slot,
        )

        if not selected_rooms:
            continue

        _add_assignment(schedule_result, exam, slot, selected_rooms)
        return True

    return False


def repair_unassigned_exams(bundle, phase3_result, stabilized_phase35, schedule_result):
    """
    Phase 4B:
    Stronger repair heuristic for currently unassigned exams.

    Strategy:
    1. direct retry over lightly occupied slots
    2. replacement of a lower-priority assigned exam
    3. reinsert removed exam elsewhere
    """
    room_rows = list(stabilized_phase35.stabilized_room_availability)
    priority_scores = phase3_result.exam_priority_scores

    unassigned_sorted = sorted(
        schedule_result.unassigned_exams,
        key=lambda code: priority_scores.get(code, 0),
        reverse=True,
    )

    repaired = []
    still_unassigned = []

    for course_code in unassigned_sorted:
        exam = _find_exam_by_course_code(stabilized_phase35, course_code)
        if exam is None:
            still_unassigned.append(course_code)
            continue

        slots = _sorted_slots_for_repair(bundle, schedule_result)

        # ---------------------------------
        # Step 1: direct retry
        # ---------------------------------
        if _try_direct_insert(
            exam=exam,
            slots=slots,
            room_rows=room_rows,
            phase3_result=phase3_result,
            schedule_result=schedule_result,
        ):
            repaired.append(course_code)
            continue

        # ---------------------------------
        # Step 2: replace lower-priority exam
        # ---------------------------------
        assigned = False

        for slot in slots:
            slot_courses = list(schedule_result.slot_to_course_codes.get(slot.slot_id, []))

            # try replacing only lower-priority exams
            slot_courses.sort(key=lambda c: priority_scores.get(c, 0))

            for existing_course_code in slot_courses:
                existing_priority = priority_scores.get(existing_course_code, 0)
                current_priority = priority_scores.get(course_code, 0)

                # only replace if the new exam is harder / more important
                if current_priority <= existing_priority:
                    continue

                existing_exam = _find_exam_by_course_code(stabilized_phase35, existing_course_code)
                existing_assignment = _find_assignment_by_course_code(schedule_result, existing_course_code)

                if existing_exam is None or existing_assignment is None:
                    continue

                removed_assignment = _remove_assignment(schedule_result, existing_course_code)
                if removed_assignment is None:
                    continue

                # Try placing the harder unassigned exam in this slot
                can_place_new_exam = (
                    slot_accepts_exam(exam, slot)
                    and not has_student_conflict_in_slot(
                        exam=exam,
                        slot_id=slot.slot_id,
                        schedule_result=schedule_result,
                        conflict_matrix=phase3_result.conflict_matrix,
                    )
                )

                if not can_place_new_exam:
                    _restore_removed_assignment(schedule_result, existing_exam, removed_assignment)
                    continue

                selected_rooms = select_rooms_for_exam(
                    exam=exam,
                    slot=slot,
                    stabilized_room_availability=room_rows,
                    room_usage_by_slot=schedule_result.room_usage_by_slot,
                )

                if not selected_rooms:
                    _restore_removed_assignment(schedule_result, existing_exam, removed_assignment)
                    continue

                _add_assignment(schedule_result, exam, slot, selected_rooms)

                # Reinsert removed exam somewhere else
                alt_slots = _sorted_slots_for_repair(bundle, schedule_result)
                reinserted = _try_direct_insert(
                    exam=existing_exam,
                    slots=alt_slots,
                    room_rows=room_rows,
                    phase3_result=phase3_result,
                    schedule_result=schedule_result,
                )

                if reinserted:
                    repaired.append(course_code)
                    assigned = True
                    break

                # rollback if removed exam cannot be reinserted
                _remove_assignment(schedule_result, exam.course_code)
                _restore_removed_assignment(schedule_result, existing_exam, removed_assignment)

            if assigned:
                break

        if not assigned:
            still_unassigned.append(course_code)

    schedule_result.unassigned_exams = still_unassigned
    schedule_result.messages.append(
        f"Repair step assigned additional exams: {len(repaired)}"
    )
    schedule_result.messages.append(
        f"Remaining unassigned after repair: {len(schedule_result.unassigned_exams)}"
    )

    return schedule_result