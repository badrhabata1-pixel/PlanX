from __future__ import annotations

import copy
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from scheduler.evaluator import ScheduleEvaluation, evaluate_schedule


@dataclass(frozen=True)
class ImprovementStep:
    action: str
    exam_codes: Tuple[str, ...]
    before_penalty: int
    after_penalty: int
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ImprovementResult:
    improved_schedule: Any
    initial_evaluation: ScheduleEvaluation
    final_evaluation: ScheduleEvaluation
    history: List[ImprovementStep] = field(default_factory=list)
    iterations_run: int = 0
    improvements_applied: int = 0


def improve_schedule(
    bundle: Any,
    phase3_result: Any,
    stabilized_phase35: Any,
    schedule_result: Any,
    validate_schedule_fn: Any,
    max_iterations: int = 10,
    max_swap_pairs: int = 120,
) -> ImprovementResult:
    """
    Phase 5 / Part 3:
    - Try safe improving moves
    - Then try safe improving swaps
    - Accept only if:
        1) schedule remains feasible
        2) total penalty strictly decreases
    """
    current_schedule = copy.deepcopy(schedule_result)
    current_evaluation = evaluate_schedule(bundle, current_schedule)
    initial_evaluation = current_evaluation
    history: List[ImprovementStep] = []

    ordered_exam_codes = _get_ordered_exam_codes(phase3_result, current_schedule)
    slot_metadata_map = _build_slot_metadata_map(bundle, current_schedule)
    candidate_slot_ids = list(slot_metadata_map.keys())

    improvements_applied = 0
    iterations_run = 0

    for iteration in range(max_iterations):
        iterations_run += 1
        improved_in_this_iteration = False

        # -------------------------------------------------
        # 1) Try single-exam moves
        # -------------------------------------------------
        for exam_code in ordered_exam_codes:
            current_assignment = current_schedule.assignments[exam_code]
            current_slot_id = current_assignment.slot_id

            for target_slot_id in candidate_slot_ids:
                if target_slot_id == current_slot_id:
                    continue

                candidate_schedule = copy.deepcopy(current_schedule)
                _apply_move(
                    candidate_schedule=candidate_schedule,
                    exam_code=exam_code,
                    target_slot_id=target_slot_id,
                    slot_metadata_map=slot_metadata_map,
                )

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
                    history.append(
                        ImprovementStep(
                            action="move",
                            exam_codes=(exam_code,),
                            before_penalty=current_evaluation.total_penalty,
                            after_penalty=candidate_evaluation.total_penalty,
                            details={
                                "from_slot": current_slot_id,
                                "to_slot": target_slot_id,
                                "validation_messages": validation_messages,
                            },
                        )
                    )
                    current_schedule = candidate_schedule
                    current_evaluation = candidate_evaluation
                    improvements_applied += 1
                    improved_in_this_iteration = True
                    break

            if improved_in_this_iteration:
                break

        if improved_in_this_iteration:
            continue

        # -------------------------------------------------
        # 2) Try exam swaps
        # -------------------------------------------------
        swap_pairs_checked = 0
        exam_count = len(ordered_exam_codes)

        for i in range(exam_count):
            exam_a = ordered_exam_codes[i]

            for j in range(i + 1, exam_count):
                exam_b = ordered_exam_codes[j]

                swap_pairs_checked += 1
                if swap_pairs_checked > max_swap_pairs:
                    break

                assignment_a = current_schedule.assignments[exam_a]
                assignment_b = current_schedule.assignments[exam_b]

                if assignment_a.slot_id == assignment_b.slot_id:
                    continue

                candidate_schedule = copy.deepcopy(current_schedule)
                _apply_swap(
                    candidate_schedule=candidate_schedule,
                    exam_a=exam_a,
                    exam_b=exam_b,
                    slot_metadata_map=slot_metadata_map,
                )

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
                    history.append(
                        ImprovementStep(
                            action="swap",
                            exam_codes=(exam_a, exam_b),
                            before_penalty=current_evaluation.total_penalty,
                            after_penalty=candidate_evaluation.total_penalty,
                            details={
                                "slot_a_before": assignment_a.slot_id,
                                "slot_b_before": assignment_b.slot_id,
                                "validation_messages": validation_messages,
                            },
                        )
                    )
                    current_schedule = candidate_schedule
                    current_evaluation = candidate_evaluation
                    improvements_applied += 1
                    improved_in_this_iteration = True
                    break

            if improved_in_this_iteration or swap_pairs_checked > max_swap_pairs:
                break

        if not improved_in_this_iteration:
            break

    return ImprovementResult(
        improved_schedule=current_schedule,
        initial_evaluation=initial_evaluation,
        final_evaluation=current_evaluation,
        history=history,
        iterations_run=iterations_run,
        improvements_applied=improvements_applied,
    )


def _get_ordered_exam_codes(phase3_result: Any, schedule_result: Any) -> List[str]:
    """
    Use phase3 priority scores if available.
    Higher priority exams are tried first.
    """
    priority_scores = getattr(phase3_result, "exam_priority_scores", {}) or {}

    return sorted(
        list(schedule_result.assignments.keys()),
        key=lambda code: priority_scores.get(code, 0),
        reverse=True,
    )


def _build_slot_metadata_map(bundle: Any, schedule_result: Any) -> Dict[str, Dict[str, Any]]:
    slot_metadata_map: Dict[str, Dict[str, Any]] = {}

    # Preferred source: bundle.date_period_slots
    date_period_slots = getattr(bundle, "date_period_slots", None)
    if date_period_slots:
        for slot in date_period_slots:
            slot_id = getattr(slot, "slot_id", None)
            if slot_id is None:
                continue

            slot_metadata_map[slot_id] = {
                "slot_id": slot_id,
                "date": getattr(slot, "date", None),
                "day_name": getattr(slot, "day_name", None),
                "period_id": getattr(slot, "period_id", None),
                "start_time": getattr(slot, "start_time", None),
                "end_time": getattr(slot, "end_time", None),
            }

    # Fallback: derive from existing assignments
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


def _apply_move(
    candidate_schedule: Any,
    exam_code: str,
    target_slot_id: str,
    slot_metadata_map: Dict[str, Dict[str, Any]],
) -> None:
    assignment = candidate_schedule.assignments[exam_code]
    target_meta = slot_metadata_map[target_slot_id]

    assignment.slot_id = target_meta["slot_id"]
    assignment.date = target_meta["date"]
    assignment.day_name = target_meta["day_name"]
    assignment.period_id = target_meta["period_id"]
    assignment.start_time = target_meta["start_time"]
    assignment.end_time = target_meta["end_time"]

    _rebuild_schedule_indexes(candidate_schedule)


def _apply_swap(
    candidate_schedule: Any,
    exam_a: str,
    exam_b: str,
    slot_metadata_map: Dict[str, Dict[str, Any]],
) -> None:
    assignment_a = candidate_schedule.assignments[exam_a]
    assignment_b = candidate_schedule.assignments[exam_b]

    slot_a = assignment_a.slot_id
    slot_b = assignment_b.slot_id

    meta_a = slot_metadata_map[slot_a]
    meta_b = slot_metadata_map[slot_b]

    assignment_a.slot_id = meta_b["slot_id"]
    assignment_a.date = meta_b["date"]
    assignment_a.day_name = meta_b["day_name"]
    assignment_a.period_id = meta_b["period_id"]
    assignment_a.start_time = meta_b["start_time"]
    assignment_a.end_time = meta_b["end_time"]

    assignment_b.slot_id = meta_a["slot_id"]
    assignment_b.date = meta_a["date"]
    assignment_b.day_name = meta_a["day_name"]
    assignment_b.period_id = meta_a["period_id"]
    assignment_b.start_time = meta_a["start_time"]
    assignment_b.end_time = meta_a["end_time"]

    _rebuild_schedule_indexes(candidate_schedule)


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

    return True, validation_messages