from models import Course, Student, Enrollment, Room, Period, ExamOffering

from ingestion.loaders import load_csv_file
from ingestion.roster_parser import parse_roster_excel
from ingestion.room_parser import parse_rooms
from ingestion.period_parser import parse_periods
from ingestion.calendar_parser import parse_calendar_days
from ingestion.slot_parser import parse_date_period_slots
from ingestion.level_policy_parser import parse_level_policies
from ingestion.rule_parser import parse_exam_rules
from ingestion.assumption_parser import parse_system_assumptions
from ingestion.room_availability_parser import parse_room_availability
from ingestion.bundle_builder import build_data_bundle

from preprocessing import (
    prepare_conflict_preprocessing,
    validate_phase3_inputs,
)

from config import (
    ROSTER_FILE,
    ROOMS_FILE,
    PERIODS_FILE,
    CALENDAR_FILE,
    SLOTS_FILE,
    LEVEL_POLICY_FILE,
    RULES_FILE,
    ASSUMPTIONS_FILE,
    ROOM_AVAILABILITY_FILE,
)


def main():
    print("PlanX AI Engine - Phase 1")
    print("Schema models loaded successfully.")

    # -----------------------------
    # Phase 2: Data ingestion
    # -----------------------------
    courses, exam_offerings, students, enrollments = parse_roster_excel(str(ROSTER_FILE))

    rooms_df = load_csv_file(str(ROOMS_FILE))
    periods_df = load_csv_file(str(PERIODS_FILE))
    calendar_df = load_csv_file(str(CALENDAR_FILE))
    slots_df = load_csv_file(str(SLOTS_FILE))
    level_policy_df = load_csv_file(str(LEVEL_POLICY_FILE))
    rules_df = load_csv_file(str(RULES_FILE))
    assumptions_df = load_csv_file(str(ASSUMPTIONS_FILE))
    room_availability_df = load_csv_file(str(ROOM_AVAILABILITY_FILE))

    rooms = parse_rooms(rooms_df)
    periods = parse_periods(periods_df)
    calendar_days = parse_calendar_days(calendar_df)
    date_period_slots = parse_date_period_slots(slots_df)
    level_policies = parse_level_policies(level_policy_df)
    exam_rules = parse_exam_rules(rules_df)
    system_assumptions = parse_system_assumptions(assumptions_df)
    room_availability = parse_room_availability(room_availability_df)

    bundle = build_data_bundle(
        courses=courses,
        students=students,
        enrollments=enrollments,
        exam_offerings=exam_offerings,
        rooms=rooms,
        periods=periods,
        calendar_days=calendar_days,
        date_period_slots=date_period_slots,
        level_policies=level_policies,
        exam_rules=exam_rules,
        system_assumptions=system_assumptions,
        room_availability=room_availability,
    )

    print("Phase 2 completed successfully.")
    print(f"Courses: {len(bundle.courses)}")
    print(f"Exam offerings: {len(bundle.exam_offerings)}")
    print(f"Students: {len(bundle.students)}")
    print(f"Enrollments: {len(bundle.enrollments)}")
    print(f"Rooms: {len(bundle.rooms)}")
    print(f"Periods: {len(bundle.periods)}")
    print(f"Calendar days: {len(bundle.calendar_days)}")
    print(f"Date-period slots: {len(bundle.date_period_slots)}")
    print(f"Level policies: {len(bundle.level_policies)}")
    print(f"Exam rules: {len(bundle.exam_rules)}")
    print(f"System assumptions: {len(bundle.system_assumptions)}")
    print(f"Room availability rows: {len(bundle.room_availability)}")

   # print(bundle.courses[:3]) phase 2 tsting <------------------------------
   # print(bundle.exam_offerings[:3])
   # print(bundle.enrollments[:3])

    if bundle.students:
        print("Sample student:", bundle.students[0])

    if bundle.enrollments:
        print("Sample enrollment:", bundle.enrollments[0])

    if bundle.exam_offerings:
        print("Sample exam offering:", bundle.exam_offerings[0])

    # -----------------------------
    # Phase 3: Conflict preprocessing
    # -----------------------------
    print("Starting Phase 3: Conflict Matrix & Constraint Preparation...")

    phase3_result = prepare_conflict_preprocessing(bundle)
    validation_messages = validate_phase3_inputs(bundle, phase3_result)

    print("Phase 3 completed successfully.")
    print(f"Students in student_to_courses: {len(phase3_result.student_to_courses)}")
    print(f"Courses in course_to_students: {len(phase3_result.course_to_students)}")
    print(f"Conflict pairs: {len(phase3_result.conflict_matrix)}")
    print(f"Priority scores: {len(phase3_result.exam_priority_scores)}")

    for message in validation_messages:
        print(f"- {message}")

    sample_student_id = next(iter(phase3_result.student_to_courses))
    print(
        f"Sample student mapping: {sample_student_id} -> "
        f"{phase3_result.student_to_courses[sample_student_id]}"
    )

    sample_course_code = next(iter(phase3_result.course_to_students))
    print(
        f"Sample course mapping: {sample_course_code} -> "
        f"{len(phase3_result.course_to_students[sample_course_code])} students"
    )

    if phase3_result.conflict_matrix:
        sample_conflict_pair = next(iter(phase3_result.conflict_matrix))
        print(
            f"Sample conflict: {sample_conflict_pair} -> "
            f"{phase3_result.conflict_matrix[sample_conflict_pair]}"
        )


if __name__ == "__main__":
    main()