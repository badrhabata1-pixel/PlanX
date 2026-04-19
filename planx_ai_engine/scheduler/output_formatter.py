from __future__ import annotations

from typing import Any, Dict, List


def build_final_schedule_rows(
    bundle: Any,
    schedule_result: Any,
    stabilized_phase35: Any,
) -> List[Dict[str, Any]]:
    exam_requirements = _build_exam_requirements_map(stabilized_phase35)

    rows: List[Dict[str, Any]] = []

    for assignment in schedule_result.assignments.values():
        exam_info = exam_requirements.get(assignment.course_code, {})

        row = {
            "date": assignment.date,
            "day_name": assignment.day_name,
            "time": f"{assignment.start_time} - {assignment.end_time}",
            "course_code": assignment.course_code,
            "course_title": assignment.course_name,
            "students_numbers": exam_info.get("student_count", assignment.total_capacity),
            "exam_type": exam_info.get("exam_mode", "unknown"),
            "places": ", ".join(assignment.room_ids),
            "room_count": len(assignment.room_ids),
            "total_capacity": assignment.total_capacity,
            "slot_id": assignment.slot_id,
            "period_id": assignment.period_id,
        }

        rows.append(row)

    rows.sort(
        key=lambda row: (
            str(row["date"]),
            str(row["time"]),
            str(row["course_code"]),
        )
    )

    return rows


def print_final_schedule(rows: List[Dict[str, Any]]) -> None:
    print("\n" + "=" * 120)
    print("PLANX FINAL EXAM SCHEDULE")
    print("=" * 120)

    for row in rows:
        print(
            f"{row['date']} | {row['time']} | "
            f"{row['course_code']} | {row['course_title']} | "
            f"Students: {row['students_numbers']} | "
            f"Type: {row['exam_type']} | "
            f"Places: {row['places']}"
        )


def print_final_schedule_summary(
    schedule_result: Any,
    evaluation: Any,
) -> None:
    print("\n" + "=" * 120)
    print("PLANX FINAL SUMMARY")
    print("=" * 120)

    print(f"Assigned exams      : {len(schedule_result.assignments)}")
    print(f"Unassigned exams    : {len(schedule_result.unassigned_exams)}")
    print(f"Final total penalty : {evaluation.total_penalty}")
    print(f"Feasible            : {evaluation.feasible}")

    print("\nPenalty breakdown:")
    for name, penalty in evaluation.component_penalties.items():
        print(f"- {name}: {penalty}")

    if schedule_result.unassigned_exams:
        print("\nUnassigned exams:")
        for exam_code in schedule_result.unassigned_exams:
            print(f"- {exam_code}")


def _build_exam_requirements_map(stabilized_phase35: Any) -> Dict[str, Dict[str, Any]]:
    requirements: Dict[str, Dict[str, Any]] = {}

    for exam in stabilized_phase35.stabilized_exams:
        requirements[exam.course_code] = {
            "student_count": getattr(exam, "student_count", 0),
            "exam_mode": getattr(exam, "exam_mode", "unknown"),
        }

    return requirements