from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import DefaultDict, Dict, List, Set, Tuple

from models.enrollment import Enrollment
from models.data_bundle import PlanXDataBundle


@dataclass
class ConflictPrepResult:
    """
    Stores the main preprocessing outputs needed before scheduling.

    This Phase 3 result includes:
    - student_to_courses
    - course_to_students
    - conflict_matrix
    - exam_priority_scores
    """
    student_to_courses: Dict[str, List[str]]
    course_to_students: Dict[str, List[str]]
    conflict_matrix: Dict[Tuple[str, str], int]
    exam_priority_scores: Dict[str, float]


def build_student_to_courses(enrollments: List[Enrollment]) -> Dict[str, List[str]]:
    """
    Build a mapping:
        student_id -> sorted list of unique course_codes

    Why this matters:
    Each student is the source of conflicts between the exams they take.
    """
    mapping: DefaultDict[str, Set[str]] = defaultdict(set)

    for enrollment in enrollments:
        mapping[enrollment.student_id].add(enrollment.course_code)

    return {
        student_id: sorted(course_codes)
        for student_id, course_codes in mapping.items()
    }


def build_course_to_students(enrollments: List[Enrollment]) -> Dict[str, List[str]]:
    """
    Build a mapping:
        course_code -> sorted list of unique student_ids

    Why this matters:
    This gives us course size and helps later in exam ordering and room assignment.
    """
    mapping: DefaultDict[str, Set[str]] = defaultdict(set)

    for enrollment in enrollments:
        mapping[enrollment.course_code].add(enrollment.student_id)

    return {
        course_code: sorted(student_ids)
        for course_code, student_ids in mapping.items()
    }


def build_conflict_matrix(
    student_to_courses: Dict[str, List[str]]
) -> Dict[Tuple[str, str], int]:
    """
    Build a symmetric conflict matrix where:

        conflict_matrix[(course_a, course_b)] = number of shared students

    Notes:
    - self-conflicts are excluded
    - both (A, B) and (B, A) are stored
    """
    conflict_matrix: DefaultDict[Tuple[str, str], int] = defaultdict(int)

    for student_id, course_list in student_to_courses.items():
        unique_courses = sorted(set(course_list))

        if len(unique_courses) < 2:
            continue

        for course_a, course_b in combinations(unique_courses, 2):
            conflict_matrix[(course_a, course_b)] += 1
            conflict_matrix[(course_b, course_a)] += 1

    return dict(conflict_matrix)


def compute_exam_priority_scores(
    course_to_students: Dict[str, List[str]],
    conflict_matrix: Dict[Tuple[str, str], int],
) -> Dict[str, float]:
    """
    Compute a simple priority score for each exam.

    Current formula:
        priority = exam_size + total_conflict_weight

    This helps later when deciding which exams should be scheduled first.
    """
    conflict_totals: DefaultDict[str, int] = defaultdict(int)

    for (course_a, course_b), shared_count in conflict_matrix.items():
        conflict_totals[course_a] += shared_count

    priority_scores: Dict[str, float] = {}

    for course_code, student_ids in course_to_students.items():
        exam_size = len(student_ids)
        total_conflict_weight = conflict_totals.get(course_code, 0)
        priority_scores[course_code] = float(exam_size + total_conflict_weight)

    return priority_scores


def prepare_conflict_preprocessing(data_bundle: PlanXDataBundle) -> ConflictPrepResult:
    """
    Phase 3 entry point.

    Takes the full PlanXDataBundle from Phase 2
    and transforms it into scheduling-ready conflict structures.
    """
    enrollments = data_bundle.enrollments

    student_to_courses = build_student_to_courses(enrollments)
    course_to_students = build_course_to_students(enrollments)
    conflict_matrix = build_conflict_matrix(student_to_courses)
    exam_priority_scores = compute_exam_priority_scores(
        course_to_students=course_to_students,
        conflict_matrix=conflict_matrix,
    )

    return ConflictPrepResult(
        student_to_courses=student_to_courses,
        course_to_students=course_to_students,
        conflict_matrix=conflict_matrix,
        exam_priority_scores=exam_priority_scores,
    )