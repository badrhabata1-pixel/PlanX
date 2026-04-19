from __future__ import annotations

from typing import List

from models.data_bundle import PlanXDataBundle
from preprocessing.conflict_builder import ConflictPrepResult


def validate_phase3_inputs(
    data_bundle: PlanXDataBundle,
    prep_result: ConflictPrepResult,
) -> List[str]:
    """
    Validate the outputs of Phase 3.

    Returns a list of human-readable validation messages.
    Raises ValueError if a critical validation fails.
    """
    messages: List[str] = []

    # Raw bundle checks
    if not data_bundle.students:
        raise ValueError("Phase 3 validation failed: students dataset is empty.")

    if not data_bundle.courses:
        raise ValueError("Phase 3 validation failed: courses dataset is empty.")

    if not data_bundle.enrollments:
        raise ValueError("Phase 3 validation failed: enrollments dataset is empty.")

    if not data_bundle.rooms:
        raise ValueError("Phase 3 validation failed: rooms dataset is empty.")

    if not data_bundle.periods:
        raise ValueError("Phase 3 validation failed: periods dataset is empty.")

    messages.append("Raw bundle validation passed.")

    # Core maps
    if not prep_result.student_to_courses:
        raise ValueError("Phase 3 validation failed: student_to_courses is empty.")

    if not prep_result.course_to_students:
        raise ValueError("Phase 3 validation failed: course_to_students is empty.")

    messages.append("Core map validation passed.")

    # Coverage checks
    messages.append(
        f"Students with enrollments: {len(prep_result.student_to_courses)} / {len(data_bundle.students)}"
    )
    messages.append(
        f"Courses with enrolled students: {len(prep_result.course_to_students)} / {len(data_bundle.courses)}"
    )

    # Conflict matrix checks
    if prep_result.conflict_matrix is None:
        raise ValueError("Phase 3 validation failed: conflict_matrix is missing.")

    messages.append(
        f"Conflict pair entries generated: {len(prep_result.conflict_matrix)}"
    )

    for (course_a, course_b), value in prep_result.conflict_matrix.items():
        reverse_value = prep_result.conflict_matrix.get((course_b, course_a))
        if reverse_value != value:
            raise ValueError(
                f"Phase 3 validation failed: asymmetric conflict detected between "
                f"{course_a} and {course_b}."
            )

    messages.append("Conflict matrix symmetry validation passed.")

    # Priority scores
    if not prep_result.exam_priority_scores:
        raise ValueError("Phase 3 validation failed: exam_priority_scores is empty.")

    messages.append(
        f"Priority scores generated for {len(prep_result.exam_priority_scores)} exams."
    )

    messages.append("Phase 3 validation completed successfully.")

    return messages