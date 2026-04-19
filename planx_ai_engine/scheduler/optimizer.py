from __future__ import annotations

import copy
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from scheduler.evaluator import ScheduleEvaluation, evaluate_schedule


@dataclass(frozen=True)
class OptimizationStep:
    action: str
    exam_codes: Tuple[str, ...]
    before_penalty: int
    after_penalty: int
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OptimizationResult:
    optimized_schedule: Any
    initial_evaluation: ScheduleEvaluation
    final_evaluation: ScheduleEvaluation
    history: List[OptimizationStep] = field(default_factory=list)
    iterations_run: int = 0
    improvements_applied: int = 0


def optimize_schedule(
    bundle: Any,
    phase3_result: Any,
    stabilized_phase35: Any,
    schedule_result: Any,
    validate_schedule_fn: Any,
    max_iterations: int = 8,
    top_exam_limit: int = 20,
    max_swap_pairs: int = 80,
) -> OptimizationResult:
    current_schedule = copy.deepcopy(schedule_result)
    current_evaluation = evaluate_schedule(bundle, current_schedule)
    initial_evaluation = current_evaluation
    history: List[OptimizationStep] = []

    slot_metadata_map = _build_slot_metadata_map(bundle, current_schedule)
    all_slot_ids = list(slot_metadata_map.keys())

    exam_requirements = _build_exam_requirements_map(stabilized_phase35)
    room_catalog = _build_room_catalog(bundle)
    availability_index = _build_room_availability_index(stabilized_phase35)

    iterations_run = 0
    improvements_applied = 0

    for iteration_idx in range(max_iterations):
        print(f"[Optimizer] Iteration {iteration_idx + 1}/{max_iterations}")
        iterations_run += 1

        exam_pressure_scores = _build_exam_pressure_scores(
            bundle=bundle,
            schedule_result=current_schedule,
            exam_requirements=exam_requirements,
        )

        targeted_exam_codes = [
            exam_code
            for exam_code, _ in sorted(
                exam_pressure_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
            if exam_code in current_schedule.assignments
        ][:top_exam_limit]

        print(f"[Optimizer] Targeted exams count: {len(targeted_exam_codes)}")

        if not targeted_exam_codes:
            print("[Optimizer] No targeted exams found. Stopping.")
            break

        best_candidate_schedule = None
        best_candidate_evaluation = None
        best_step = None

        # -------------------------------------------------
        # 1) Best-improving moves
        # -------------------------------------------------
        for exam_code in targeted_exam_codes:
            current_assignment = current_schedule.assignments[exam_code]
            current_slot_id = current_assignment.slot_id

            for target_slot_id in all_slot_ids:
                if target_slot_id == current_slot_id:
                    continue

                candidate_schedule = copy.deepcopy(current_schedule)

                moved = _apply_move_with_room_reselection(
                    candidate_schedule=candidate_schedule,
                    exam_code=exam_code,
                    target_slot_id=target_slot_id,
                    slot_metadata_map=slot_metadata_map,
                    exam_requirements=exam_requirements,
                    room_catalog=room_catalog,
                    availability_index=availability_index,
                )

                if not moved:
                    continue

                feasible, validation_messages = _is_schedule_feasible(
                    bundle=bundle,
                    phase3_result=phase3_result,
                    stabilized_phase35=stabilized_phase35,
                    candidate_schedule=candidate_schedule,
                    validate_schedule_fn=validate_schedule_fn,
                )

                if not feasible:
                    continue

                candidate_evaluation = evaluate_schedule(bundle, candidate_schedule)

                if candidate_evaluation.total_penalty < current_evaluation.total_penalty:
                    if (
                        best_candidate_evaluation is None
                        or candidate_evaluation.total_penalty
                        < best_candidate_evaluation.total_penalty
                    ):
                        best_candidate_schedule = candidate_schedule
                        best_candidate_evaluation = candidate_evaluation
                        best_step = OptimizationStep(
                            action="targeted_move",
                            exam_codes=(exam_code,),
                            before_penalty=current_evaluation.total_penalty,
                            after_penalty=candidate_evaluation.total_penalty,
                            details={
                                "from_slot": current_slot_id,
                                "to_slot": target_slot_id,
                                "validation_messages": validation_messages,
                            },
                        )

        # -------------------------------------------------
        # 2) Best-improving swaps
        # -------------------------------------------------
        swap_pairs_checked = 0

        for i in range(len(targeted_exam_codes)):
            exam_a = targeted_exam_codes[i]

            for j in range(i + 1, len(targeted_exam_codes)):
                exam_b = targeted_exam_codes[j]
                swap_pairs_checked += 1

                if swap_pairs_checked > max_swap_pairs:
                    break

                assignment_a = current_schedule.assignments[exam_a]
                assignment_b = current_schedule.assignments[exam_b]

                if assignment_a.slot_id == assignment_b.slot_id:
                    continue

                candidate_schedule = copy.deepcopy(current_schedule)

                swapped = _apply_swap_with_room_reselection(
                    candidate_schedule=candidate_schedule,
                    exam_a=exam_a,
                    exam_b=exam_b,
                    slot_metadata_map=slot_metadata_map,
                    exam_requirements=exam_requirements,
                    room_catalog=room_catalog,
                    availability_index=availability_index,
                )

                if not swapped:
                    continue

                feasible, validation_messages = _is_schedule_feasible(
                    bundle=bundle,
                    phase3_result=phase3_result,
                    stabilized_phase35=stabilized_phase35,
                    candidate_schedule=candidate_schedule,
                    validate_schedule_fn=validate_schedule_fn,
                )

                if not feasible:
                    continue

                candidate_evaluation = evaluate_schedule(bundle, candidate_schedule)

                if candidate_evaluation.total_penalty < current_evaluation.total_penalty:
                    if (
                        best_candidate_evaluation is None
                        or candidate_evaluation.total_penalty
                        < best_candidate_evaluation.total_penalty
                    ):
                        best_candidate_schedule = candidate_schedule
                        best_candidate_evaluation = candidate_evaluation
                        best_step = OptimizationStep(
                            action="targeted_swap",
                            exam_codes=(exam_a, exam_b),
                            before_penalty=current_evaluation.total_penalty,
                            after_penalty=candidate_evaluation.total_penalty,
                            details={
                                "slot_a_before": assignment_a.slot_id,
                                "slot_b_before": assignment_b.slot_id,
                                "validation_messages": validation_messages,
                            },
                        )

            if swap_pairs_checked > max_swap_pairs:
                break

        if best_candidate_schedule is None:
            print("[Optimizer] No improving candidate found in this iteration.")
            break

        print(
            f"[Optimizer] Accepted {best_step.action}: "
            f"{best_step.before_penalty} -> {best_step.after_penalty}"
        )

        current_schedule = best_candidate_schedule
        current_evaluation = best_candidate_evaluation
        history.append(best_step)
        improvements_applied += 1

    return OptimizationResult(
        optimized_schedule=current_schedule,
        initial_evaluation=initial_evaluation,
        final_evaluation=current_evaluation,
        history=history,
        iterations_run=iterations_run,
        improvements_applied=improvements_applied,
    )


def _build_exam_pressure_scores(
    bundle: Any,
    schedule_result: Any,
    exam_requirements: Dict[str, Dict[str, Any]],
) -> Dict[str, int]:
    pressure = defaultdict(int)
    student_exam_map = _build_student_exam_map(bundle, schedule_result)
    slot_order = _build_slot_order_from_schedule(schedule_result)

    for _, exams in student_exam_map.items():
        sorted_exams = sorted(
            exams,
            key=lambda item: slot_order.get(item["slot_id"], 10**9),
        )

        exams_per_day = defaultdict(list)
        for exam in sorted_exams:
            exams_per_day[exam["date"]].append(exam)

        for _, day_exams in exams_per_day.items():
            if len(day_exams) > 1:
                for exam in day_exams:
                    pressure[exam["course_code"]] += 3 * (len(day_exams) - 1)

            for idx in range(len(day_exams) - 1):
                current_exam = day_exams[idx]
                next_exam = day_exams[idx + 1]

                current_slot_index = slot_order.get(current_exam["slot_id"])
                next_slot_index = slot_order.get(next_exam["slot_id"])

                if (
                    current_slot_index is not None
                    and next_slot_index is not None
                    and next_slot_index - current_slot_index == 1
                ):
                    pressure[current_exam["course_code"]] += 7
                    pressure[next_exam["course_code"]] += 7

    for course_code, assignment in schedule_result.assignments.items():
        room_count = len(assignment.room_ids)
        if room_count > 1:
            pressure[course_code] += 2 * (room_count - 1)

        student_count = exam_requirements.get(course_code, {}).get("student_count", 0)
        unused_capacity = max(0, assignment.total_capacity - student_count)
        pressure[course_code] += unused_capacity // 25

    return dict(pressure)


def _build_student_exam_map(
    bundle: Any,
    schedule_result: Any,
) -> Dict[str, List[Dict[str, Any]]]:
    student_exam_map = defaultdict(list)

    for enrollment in bundle.enrollments:
        course_code = enrollment.course_code
        if course_code not in schedule_result.assignments:
            continue

        assignment = schedule_result.assignments[course_code]
        student_exam_map[enrollment.student_id].append(
            {
                "course_code": course_code,
                "slot_id": assignment.slot_id,
                "date": assignment.date,
                "period_id": assignment.period_id,
            }
        )

    return dict(student_exam_map)


def _build_slot_order_from_schedule(schedule_result: Any) -> Dict[str, int]:
    unique_slots = {}

    for assignment in schedule_result.assignments.values():
        unique_slots[assignment.slot_id] = (
            str(assignment.date),
            str(assignment.start_time),
            str(assignment.period_id),
        )

    ordered_slot_ids = sorted(unique_slots.keys(), key=lambda slot_id: unique_slots[slot_id])
    return {slot_id: idx for idx, slot_id in enumerate(ordered_slot_ids)}


def _build_slot_metadata_map(bundle: Any, schedule_result: Any) -> Dict[str, Dict[str, Any]]:
    slot_metadata_map = {}

    date_period_slots = getattr(bundle, "date_period_slots", None)
    if date_period_slots:
        for slot in date_period_slots:
            slot_id = getattr(slot, "slot_id", None)
            if slot_id is None:
                slot_id = f"{getattr(slot, 'date')}_{getattr(slot, 'period_id')}"

            slot_metadata_map[slot_id] = {
                "slot_id": slot_id,
                "date": getattr(slot, "date", None),
                "day_name": getattr(slot, "day_name", None),
                "period_id": getattr(slot, "period_id", None),
                "start_time": getattr(slot, "start_time", None),
                "end_time": getattr(slot, "end_time", None),
            }

    if not slot_metadata_map:
        for assignment in schedule_result.assignments.values():
            slot_metadata_map[assignment.slot_id] = {
                "slot_id": assignment.slot_id,
                "date": assignment.date,
                "day_name": assignment.day_name,
                "period_id": assignment.period_id,
                "start_time": assignment.start_time,
                "end_time": assignment.end_time,
            }

    return slot_metadata_map


def _build_exam_requirements_map(stabilized_phase35: Any) -> Dict[str, Dict[str, Any]]:
    requirements = {}

    for exam in stabilized_phase35.stabilized_exams:
        requirements[exam.course_code] = {
            "student_count": getattr(exam, "student_count", 0),
            "allowed_room_type": getattr(exam, "allowed_room_type", None),
            "splitting_allowed": getattr(exam, "splitting_allowed", True),
            "max_rooms": getattr(exam, "max_rooms", None),
            "exam_mode": getattr(exam, "exam_mode", None),
        }

    return requirements


def _build_room_catalog(bundle: Any) -> Dict[str, Dict[str, Any]]:
    room_catalog = {}

    for room in bundle.rooms:
        room_code = str(getattr(room, "room_code"))
        room_catalog[room_code] = {
            "room_id": room_code,
            "room_name": room.room_name,
            "room_type": getattr(room, "room_type", ""),
            "capacity": getattr(room, "capacity", 0),
        }

    return room_catalog


def _build_room_availability_index(stabilized_phase35: Any) -> Dict[str, Dict[str, Any]]:
    index = defaultdict(dict)

    for row in stabilized_phase35.stabilized_room_availability:
        slot_id = getattr(row, "slot_id", None)
        if slot_id is None:
            slot_id = f"{row.date}_{row.period_id}"

        if getattr(row, "is_available", False):
            index[slot_id][str(row.room_id)] = row

    return {slot_id: dict(room_map) for slot_id, room_map in index.items()}


def _apply_move_with_room_reselection(
    candidate_schedule: Any,
    exam_code: str,
    target_slot_id: str,
    slot_metadata_map: Dict[str, Dict[str, Any]],
    exam_requirements: Dict[str, Dict[str, Any]],
    room_catalog: Dict[str, Dict[str, Any]],
    availability_index: Dict[str, Dict[str, Any]],
) -> bool:
    assignment = candidate_schedule.assignments[exam_code]
    requirement = exam_requirements.get(exam_code, {})

    occupied_rooms = set(candidate_schedule.room_usage_by_slot.get(target_slot_id, set()))
    selected_rooms = _select_rooms_for_exam(
        requirement=requirement,
        target_slot_id=target_slot_id,
        occupied_rooms=occupied_rooms,
        room_catalog=room_catalog,
        availability_index=availability_index,
    )

    if not selected_rooms:
        return False

    target_meta = slot_metadata_map[target_slot_id]
    assignment.slot_id = target_meta["slot_id"]
    assignment.date = target_meta["date"]
    assignment.day_name = target_meta["day_name"]
    assignment.period_id = target_meta["period_id"]
    assignment.start_time = target_meta["start_time"]
    assignment.end_time = target_meta["end_time"]
    assignment.room_ids = selected_rooms
    assignment.total_capacity = sum(room_catalog[room_id]["capacity"] for room_id in selected_rooms)

    _rebuild_schedule_indexes(candidate_schedule)
    return True


def _apply_swap_with_room_reselection(
    candidate_schedule: Any,
    exam_a: str,
    exam_b: str,
    slot_metadata_map: Dict[str, Dict[str, Any]],
    exam_requirements: Dict[str, Dict[str, Any]],
    room_catalog: Dict[str, Dict[str, Any]],
    availability_index: Dict[str, Dict[str, Any]],
) -> bool:
    assignment_a = candidate_schedule.assignments[exam_a]
    assignment_b = candidate_schedule.assignments[exam_b]

    slot_a = assignment_a.slot_id
    slot_b = assignment_b.slot_id

    requirement_a = exam_requirements.get(exam_a, {})
    requirement_b = exam_requirements.get(exam_b, {})

    occupied_in_slot_a = set(candidate_schedule.room_usage_by_slot.get(slot_a, set()))
    occupied_in_slot_b = set(candidate_schedule.room_usage_by_slot.get(slot_b, set()))

    for room_id in assignment_a.room_ids:
        occupied_in_slot_a.discard(room_id)
    for room_id in assignment_b.room_ids:
        occupied_in_slot_b.discard(room_id)

    selected_rooms_for_a = _select_rooms_for_exam(
        requirement=requirement_a,
        target_slot_id=slot_b,
        occupied_rooms=occupied_in_slot_b,
        room_catalog=room_catalog,
        availability_index=availability_index,
    )
    if not selected_rooms_for_a:
        return False

    selected_rooms_for_b = _select_rooms_for_exam(
        requirement=requirement_b,
        target_slot_id=slot_a,
        occupied_rooms=occupied_in_slot_a,
        room_catalog=room_catalog,
        availability_index=availability_index,
    )
    if not selected_rooms_for_b:
        return False

    meta_a = slot_metadata_map[slot_a]
    meta_b = slot_metadata_map[slot_b]

    assignment_a.slot_id = meta_b["slot_id"]
    assignment_a.date = meta_b["date"]
    assignment_a.day_name = meta_b["day_name"]
    assignment_a.period_id = meta_b["period_id"]
    assignment_a.start_time = meta_b["start_time"]
    assignment_a.end_time = meta_b["end_time"]
    assignment_a.room_ids = selected_rooms_for_a
    assignment_a.total_capacity = sum(room_catalog[r]["capacity"] for r in selected_rooms_for_a)

    assignment_b.slot_id = meta_a["slot_id"]
    assignment_b.date = meta_a["date"]
    assignment_b.day_name = meta_a["day_name"]
    assignment_b.period_id = meta_a["period_id"]
    assignment_b.start_time = meta_a["start_time"]
    assignment_b.end_time = meta_a["end_time"]
    assignment_b.room_ids = selected_rooms_for_b
    assignment_b.total_capacity = sum(room_catalog[r]["capacity"] for r in selected_rooms_for_b)

    _rebuild_schedule_indexes(candidate_schedule)
    return True


def _select_rooms_for_exam(
    requirement: Dict[str, Any],
    target_slot_id: str,
    occupied_rooms: set,
    room_catalog: Dict[str, Dict[str, Any]],
    availability_index: Dict[str, Dict[str, Any]],
) -> Optional[List[str]]:
    student_count = requirement.get("student_count", 0)
    allowed_room_type = requirement.get("allowed_room_type", None)
    splitting_allowed = requirement.get("splitting_allowed", True)
    max_rooms = requirement.get("max_rooms", None)

    available_room_ids = []
    available_rooms_in_slot = availability_index.get(target_slot_id, {})

    for room_id, _ in available_rooms_in_slot.items():
        if room_id in occupied_rooms:
            continue

        room_info = room_catalog.get(room_id)
        if not room_info:
            continue

        if not _room_type_matches(allowed_room_type, room_info["room_type"]):
            continue

        available_room_ids.append(room_id)

    if not available_room_ids:
        return None

    single_room_candidates = [
        room_id
        for room_id in available_room_ids
        if room_catalog[room_id]["capacity"] >= student_count
    ]
    if single_room_candidates:
        best_single = min(
            single_room_candidates,
            key=lambda room_id: room_catalog[room_id]["capacity"],
        )
        return [best_single]

    if not splitting_allowed:
        return None

    sorted_room_ids = sorted(
        available_room_ids,
        key=lambda room_id: room_catalog[room_id]["capacity"],
        reverse=True,
    )

    selected = []
    capacity_sum = 0

    for room_id in sorted_room_ids:
        selected.append(room_id)
        capacity_sum += room_catalog[room_id]["capacity"]

        if max_rooms is not None and len(selected) > max_rooms:
            return None

        if capacity_sum >= student_count:
            return selected

    return None


def _room_type_matches(allowed_room_type: Optional[str], actual_room_type: str) -> bool:
    if not allowed_room_type:
        return True

    allowed = str(allowed_room_type).strip().lower()
    actual = str(actual_room_type).strip().lower()

    if allowed in ("any", "all"):
        return True
    if allowed == "lab":
        return "lab" in actual
    if allowed in ("hall", "lecture_hall"):
        return "hall" in actual
    if allowed in ("tutorial", "tut"):
        return "tut" in actual or "tutorial" in actual

    return allowed in actual


def _rebuild_schedule_indexes(schedule_result: Any) -> None:
    slot_to_course_codes = defaultdict(list)
    room_usage_by_slot = defaultdict(set)

    for course_code, assignment in schedule_result.assignments.items():
        slot_to_course_codes[assignment.slot_id].append(course_code)
        for room_id in assignment.room_ids:
            room_usage_by_slot[assignment.slot_id].add(room_id)

    schedule_result.slot_to_course_codes = dict(slot_to_course_codes)
    schedule_result.room_usage_by_slot = {
        slot_id: set(room_ids)
        for slot_id, room_ids in room_usage_by_slot.items()
    }


def _is_schedule_feasible(
    bundle: Any,
    phase3_result: Any,
    stabilized_phase35: Any,
    candidate_schedule: Any,
    validate_schedule_fn: Any,
) -> Tuple[bool, List[str]]:
    try:
        validation_messages = validate_schedule_fn(
            bundle=bundle,
            phase3_result=phase3_result,
            stabilized_phase35=stabilized_phase35,
            schedule_result=candidate_schedule,
        )
    except Exception as exc:
        return False, [str(exc)]

    if candidate_schedule.unassigned_exams:
        return False, validation_messages

    bad_keywords = (
        "failed",
        "violation",
        "invalid",
        "error",
        "conflict",
    )

    for message in validation_messages:
        lowered = message.lower()
        if any(keyword in lowered for keyword in bad_keywords):
            return False, validation_messages

    return True, validation_messages