from __future__ import annotations

from typing import List

from scheduler.hard_constraints import room_matches_exam, can_rooms_host_exam


def get_available_rooms_for_slot(
    slot,
    stabilized_room_availability: list,
    room_usage_by_slot: dict,
) -> List[object]:
    """
    Return all currently available rooms for a given slot,
    excluding already occupied rooms in that slot.
    """
    occupied = room_usage_by_slot.get(slot.slot_id, set())

    candidates = []
    for row in stabilized_room_availability:
        if not row.is_available:
            continue

        if row.room_id in occupied:
            continue

        if row.date != slot.date:
            continue

        if row.period_id != slot.period_id:
            continue

        if row.start_time != slot.start_time:
            continue

        if row.end_time != slot.end_time:
            continue

        candidates.append(row)

    return candidates


def select_rooms_for_exam(
    exam,
    slot,
    stabilized_room_availability: list,
    room_usage_by_slot: dict,
) -> List[object]:
    """
    Select one or more rooms for an exam under hard constraints.
    Strategy:
    - filter by slot
    - filter by room type
    - if splitting not allowed -> choose one room with enough capacity
    - else greedily accumulate largest rooms until enough capacity
    """
    available_rooms = get_available_rooms_for_slot(
        slot=slot,
        stabilized_room_availability=stabilized_room_availability,
        room_usage_by_slot=room_usage_by_slot,
    )

    compatible_rooms = [
        room for room in available_rooms
        if room_matches_exam(room, exam)
    ]

    if not compatible_rooms:
        return []

    # Single-room attempt first if splitting not allowed
    if not getattr(exam, "splitting_allowed", True):
        single_room_options = sorted(
            compatible_rooms,
            key=lambda r: r.capacity
        )
        for room in single_room_options:
            if room.capacity >= exam.student_count:
                return [room]
        return []

    # Multi-room greedy selection
    compatible_rooms = sorted(
        compatible_rooms,
        key=lambda r: r.capacity,
        reverse=True,
    )

    selected = []
    total_capacity = 0

    for room in compatible_rooms:
        selected.append(room)
        total_capacity += room.capacity

        if can_rooms_host_exam(exam, selected):
            return selected

    return []