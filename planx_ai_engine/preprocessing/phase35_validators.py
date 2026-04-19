from __future__ import annotations

from typing import List

from preprocessing.model_stabilizer import Phase35StabilizedData


def validate_phase35_data(bundle, stabilized: Phase35StabilizedData) -> List[str]:
    """
    Validate Phase 3.5 stabilized data before entering Phase 4.
    """
    messages: List[str] = []

    if not stabilized.stabilized_exams:
        raise ValueError("Phase 3.5 validation failed: stabilized_exams is empty.")

    if not stabilized.stabilized_periods:
        raise ValueError("Phase 3.5 validation failed: stabilized_periods is empty.")

    if not stabilized.stabilized_room_availability:
        raise ValueError("Phase 3.5 validation failed: stabilized_room_availability is empty.")

    room_ids = {
        getattr(room, "room_id", getattr(room, "room_code", "")).strip()
        for room in bundle.rooms
    }

    period_ids = {
        period.period_id
        for period in stabilized.stabilized_periods
    }

    for exam in stabilized.stabilized_exams:
        if not exam.exam_id:
            raise ValueError(f"Phase 3.5 validation failed: missing exam_id for {exam.course_code}.")
        if not exam.course_code:
            raise ValueError("Phase 3.5 validation failed: missing course_code in stabilized exam.")
        if exam.student_count < 0:
            raise ValueError(f"Phase 3.5 validation failed: negative student_count for {exam.course_code}.")
        if exam.duration_minutes <= 0:
            raise ValueError(f"Phase 3.5 validation failed: non-positive duration for {exam.course_code}.")
        if not exam.allowed_room_type:
            raise ValueError(f"Phase 3.5 validation failed: missing allowed_room_type for {exam.course_code}.")

    messages.append(f"Stabilized exams validated: {len(stabilized.stabilized_exams)}")

    for period in stabilized.stabilized_periods:
        if not period.period_id:
            raise ValueError("Phase 3.5 validation failed: stabilized period missing period_id.")
        if period.duration_minutes <= 0:
            raise ValueError(
                f"Phase 3.5 validation failed: non-positive duration for period {period.period_id}."
            )

    messages.append(f"Stabilized periods validated: {len(stabilized.stabilized_periods)}")

    for row in stabilized.stabilized_room_availability:
        if row.room_id not in room_ids:
            raise ValueError(
                f"Phase 3.5 validation failed: unknown room_id {row.room_id} in stabilized room availability."
            )
        if row.period_id not in period_ids:
            raise ValueError(
                f"Phase 3.5 validation failed: unknown period_id {row.period_id} in stabilized room availability."
            )

    messages.append(
        f"Stabilized room availability rows validated: {len(stabilized.stabilized_room_availability)}"
    )
    messages.append("Phase 3.5 completed successfully.")

    return messages

