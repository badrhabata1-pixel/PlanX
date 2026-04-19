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

from scheduler.excel_exporter import export_schedule_to_excel

from preprocessing import (
    prepare_conflict_preprocessing,
    validate_phase3_inputs,
    stabilize_phase35,
    validate_phase35_data,
)

from scheduler import (
    build_feasible_schedule,
    validate_phase4_schedule,
    repair_unassigned_exams,
)

from scheduler.soft_constraints import evaluate_soft_constraints
from scheduler.evaluator import evaluate_schedule
from scheduler.improver import improve_schedule
from scheduler.optimizer import optimize_schedule
from scheduler.output_formatter import (
    build_final_schedule_rows,
    print_final_schedule,
    print_final_schedule_summary,
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


def run_phase5_part1_soft_constraints_test(data_bundle, schedule_result):
    print("\n" + "=" * 80)
    print("PHASE 5 / PART 1 - SOFT CONSTRAINTS TEST")
    print("=" * 80)

    components = evaluate_soft_constraints(data_bundle, schedule_result)

    if not components:
        print("❌ FAILED: No penalty components were returned.")
        return False

    total_penalty = 0

    for component in components:
        print(f"\nComponent: {component.name}")
        print(f"Penalty : {component.penalty}")
        print(f"Details : {component.details}")

        if not isinstance(component.penalty, int):
            print("❌ FAILED: Penalty is not an integer.")
            return False

        if component.penalty < 0:
            print("❌ FAILED: Penalty is negative.")
            return False

        total_penalty += component.penalty

    print("\n" + "-" * 80)
    print(f"TOTAL RAW PENALTY = {total_penalty}")
    print("-" * 80)

    expected_names = {
        "consecutive_exams",
        "same_day_multiple_exams",
        "crowded_days",
        "room_underutilization",
        "excessive_room_splitting",
    }

    returned_names = {component.name for component in components}
    missing = expected_names - returned_names

    if missing:
        print(f"❌ FAILED: Missing components: {sorted(missing)}")
        return False

    print("✅ PASSED: Phase 5 Part 1 is working correctly.")
    return True


def run_phase5_part2_evaluator_test(data_bundle, schedule_result):
    print("\n" + "=" * 80)
    print("PHASE 5 / PART 2 - EVALUATOR TEST")
    print("=" * 80)

    evaluation = evaluate_schedule(
        data_bundle=data_bundle,
        schedule_result=schedule_result,
    )

    print(f"Feasible       : {evaluation.feasible}")
    print(f"Total penalty  : {evaluation.total_penalty}")
    print(f"Summary        : {evaluation.summary}")

    print("\nComponent penalties:")
    for name, penalty in evaluation.component_penalties.items():
        print(f"- {name}: {penalty}")

    if not isinstance(evaluation.total_penalty, int):
        print("❌ FAILED: total_penalty is not an integer.")
        return False

    if evaluation.total_penalty < 0:
        print("❌ FAILED: total_penalty is negative.")
        return False

    if len(evaluation.components) == 0:
        print("❌ FAILED: evaluation returned zero components.")
        return False

    if len(evaluation.component_penalties) != len(evaluation.components):
        print("❌ FAILED: mismatch between components and component_penalties.")
        return False

    recomputed_total = sum(component.penalty for component in evaluation.components)
    if recomputed_total != evaluation.total_penalty:
        print(
            "❌ FAILED: total_penalty does not match sum of component penalties. "
            f"expected={recomputed_total}, actual={evaluation.total_penalty}"
        )
        return False

    if evaluation.summary.get("assigned_exams") != len(schedule_result.assignments):
        print("❌ FAILED: assigned_exams summary is incorrect.")
        return False

    if evaluation.summary.get("unassigned_exams") != len(schedule_result.unassigned_exams):
        print("❌ FAILED: unassigned_exams summary is incorrect.")
        return False

    print("✅ PASSED: Phase 5 Part 2 is working correctly.")
    return True


def run_phase5_part3_improver_test(
    data_bundle,
    phase3_result,
    stabilized_phase35,
    schedule_result,
):
    print("\n" + "=" * 80)
    print("PHASE 5 / PART 3 - IMPROVER TEST")
    print("=" * 80)

    improvement_result = improve_schedule(
        bundle=data_bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=schedule_result,
        validate_schedule_fn=validate_phase4_schedule,
        max_iterations=10,
        max_swap_pairs=120,
    )

    initial_penalty = improvement_result.initial_evaluation.total_penalty
    final_penalty = improvement_result.final_evaluation.total_penalty

    print(f"Initial penalty     : {initial_penalty}")
    print(f"Final penalty       : {final_penalty}")
    print(f"Iterations run      : {improvement_result.iterations_run}")
    print(f"Improvements applied: {improvement_result.improvements_applied}")

    if improvement_result.history:
        print("\nImprovement history:")
        for step in improvement_result.history:
            print(
                f"- {step.action} | exams={step.exam_codes} | "
                f"{step.before_penalty} -> {step.after_penalty}"
            )
    else:
        print("\nNo improving move was accepted.")

    if final_penalty > initial_penalty:
        print("❌ FAILED: improver made the schedule worse.")
        return False, improvement_result

    try:
        final_validation_messages = validate_phase4_schedule(
            bundle=data_bundle,
            phase3_result=phase3_result,
            stabilized_phase35=stabilized_phase35,
            schedule_result=improvement_result.improved_schedule,
        )
    except Exception as exc:
        print("❌ FAILED: improved schedule is not feasible.")
        print(f"Validator exception: {exc}")
        return False, improvement_result

    print("\nFinal validation messages:")
    for message in final_validation_messages:
        print(f"- {message}")

    if final_penalty < initial_penalty:
        print("✅ PASSED: Phase 5 Part 3 improved the schedule successfully.")
    else:
        print("✅ PASSED: Phase 5 Part 3 ran safely with no worsening.")

    return True, improvement_result


def run_phase5_part4_optimizer_test(
    data_bundle,
    phase3_result,
    stabilized_phase35,
    schedule_result,
):
    print("\n" + "=" * 80)
    print("PHASE 5 / PART 4 - STRONG OPTIMIZATION TEST")
    print("=" * 80)

    optimization_result = optimize_schedule(
        bundle=data_bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=schedule_result,
        validate_schedule_fn=validate_phase4_schedule,
        max_iterations=2,
        top_exam_limit=6,
        max_swap_pairs=12,
    )

    initial_penalty = optimization_result.initial_evaluation.total_penalty
    final_penalty = optimization_result.final_evaluation.total_penalty

    print(f"Initial penalty     : {initial_penalty}")
    print(f"Final penalty       : {final_penalty}")
    print(f"Iterations run      : {optimization_result.iterations_run}")
    print(f"Improvements applied: {optimization_result.improvements_applied}")

    if optimization_result.history:
        print("\nOptimization history:")
        for step in optimization_result.history:
            print(
                f"- {step.action} | exams={step.exam_codes} | "
                f"{step.before_penalty} -> {step.after_penalty}"
            )
    else:
        print("\nNo improving optimization step was accepted.")

    if final_penalty > initial_penalty:
        print("❌ FAILED: optimizer made the schedule worse.")
        return False, optimization_result

    try:
        final_validation_messages = validate_phase4_schedule(
            bundle=data_bundle,
            phase3_result=phase3_result,
            stabilized_phase35=stabilized_phase35,
            schedule_result=optimization_result.optimized_schedule,
        )
    except Exception as exc:
        print("❌ FAILED: optimized schedule is not feasible.")
        print(f"Validator exception: {exc}")
        return False, optimization_result

    print("\nFinal validation messages:")
    for message in final_validation_messages:
        print(f"- {message}")

    if final_penalty < initial_penalty:
        print("✅ PASSED: Phase 5 Part 4 improved the schedule successfully.")
    else:
        print("✅ PASSED: Phase 5 Part 4 ran safely with no worsening.")

    return True, optimization_result


def run_phase6_output_formatter_test(
    data_bundle,
    stabilized_phase35,
    final_schedule_result,
):
    print("\n" + "=" * 80)
    print("PHASE 6 - FINAL OUTPUT FORMATTER TEST")
    print("=" * 80)

    final_evaluation = evaluate_schedule(
        data_bundle=data_bundle,
        schedule_result=final_schedule_result,
    )

    rows = build_final_schedule_rows(
        bundle=data_bundle,
        schedule_result=final_schedule_result,
        stabilized_phase35=stabilized_phase35,
    )

    if not rows:
        print("❌ FAILED: No schedule rows were produced.")
        return False, None, None

    print(f"Generated rows: {len(rows)}")

    sample_row = rows[0]
    required_keys = {
        "date",
        "day_name",
        "time",
        "course_code",
        "course_title",
        "students_numbers",
        "exam_type",
        "places",
        "room_count",
        "total_capacity",
        "slot_id",
        "period_id",
    }

    missing_keys = required_keys - set(sample_row.keys())
    if missing_keys:
        print(f"❌ FAILED: Missing keys in schedule row: {sorted(missing_keys)}")
        return False, None, None

    print("\nSample formatted row:")
    for key, value in sample_row.items():
        print(f"- {key}: {value}")

    print_final_schedule(rows[:10])
    print_final_schedule_summary(final_schedule_result, final_evaluation)

    print("✅ PASSED: Phase 6 output formatter is working correctly.")
    return True, rows, final_evaluation


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

    if phase3_result.student_to_courses:
        sample_student_id = next(iter(phase3_result.student_to_courses))
        print(
            f"Sample student mapping: {sample_student_id} -> "
            f"{phase3_result.student_to_courses[sample_student_id]}"
        )

    if phase3_result.course_to_students:
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

    # -----------------------------
    # Phase 3.5: Model stabilization
    # -----------------------------
    print("Starting Phase 3.5: Model Stabilization...")

    stabilized_phase35 = stabilize_phase35(bundle)
    phase35_messages = validate_phase35_data(bundle, stabilized_phase35)

    print("Phase 3.5 completed successfully.")
    print(f"Stabilized exams: {len(stabilized_phase35.stabilized_exams)}")
    print(f"Stabilized periods: {len(stabilized_phase35.stabilized_periods)}")
    print(
        "Stabilized room availability rows: "
        f"{len(stabilized_phase35.stabilized_room_availability)}"
    )

    for message in phase35_messages:
        print(f"- {message}")

    if stabilized_phase35.stabilized_exams:
        print("Sample stabilized exam:", stabilized_phase35.stabilized_exams[0])

    if stabilized_phase35.stabilized_periods:
        print("Sample stabilized period:", stabilized_phase35.stabilized_periods[0])

    if stabilized_phase35.stabilized_room_availability:
        print(
            "Sample stabilized room availability:",
            stabilized_phase35.stabilized_room_availability[0],
        )

    # -----------------------------
    # Phase 4: Feasible schedule construction
    # -----------------------------
    print("Starting Phase 4: Feasible Schedule Construction...")

    phase4_result = build_feasible_schedule(
        bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
    )

    phase4_messages = validate_phase4_schedule(
        bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=phase4_result,
    )

    print("Phase 4 completed successfully.")
    print(f"Assigned exams: {len(phase4_result.assignments)}")
    print(f"Unassigned exams: {len(phase4_result.unassigned_exams)}")

    for message in phase4_result.messages:
        print(f"- {message}")

    for message in phase4_messages:
        print(f"- {message}")

    if phase4_result.assignments:
        first_assignment = next(iter(phase4_result.assignments.values()))
        print("Sample assignment:", first_assignment)

    if phase4_result.unassigned_exams:
        print("Sample unassigned exam:", phase4_result.unassigned_exams[0])

    # -----------------------------
    # Phase 4B: Repair layer
    # -----------------------------
    print("Starting Phase 4B: Repair Layer...")

    phase4_result = repair_unassigned_exams(
        bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=phase4_result,
    )

    phase4b_messages = validate_phase4_schedule(
        bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=phase4_result,
    )

    print("Phase 4B completed successfully.")
    print(f"Assigned exams after repair: {len(phase4_result.assignments)}")
    print(f"Unassigned exams after repair: {len(phase4_result.unassigned_exams)}")

    for message in phase4_result.messages:
        print(f"- {message}")

    for message in phase4b_messages:
        print(f"- {message}")

    if phase4_result.unassigned_exams:
        print("Remaining unassigned exam sample:", phase4_result.unassigned_exams[0])

    # -----------------------------
    # Phase 5 - Part 1: Soft constraints evaluation
    # -----------------------------
    phase5_part1_passed = run_phase5_part1_soft_constraints_test(
        data_bundle=bundle,
        schedule_result=phase4_result,
    )

    if not phase5_part1_passed:
        print("\n❌ Stop here. Fix Phase 5 Part 1 before moving to evaluator.py")
        return

    print("\n✅ Ready for Phase 5 Part 2: Evaluator Layer")

    # -----------------------------
    # Phase 5 - Part 2: Evaluator layer
    # -----------------------------
    phase5_part2_passed = run_phase5_part2_evaluator_test(
        data_bundle=bundle,
        schedule_result=phase4_result,
    )

    if not phase5_part2_passed:
        print("\n❌ Stop here. Fix Phase 5 Part 2 before moving to improver.py")
        return

    print("\n✅ Ready for Phase 5 Part 3: Improver Layer")

    # -----------------------------
    # Phase 5 - Part 3: Improver layer
    # -----------------------------
    phase5_part3_passed, phase5_improvement_result = run_phase5_part3_improver_test(
        data_bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=phase4_result,
    )

    if not phase5_part3_passed:
        print("\n❌ Stop here. Fix Phase 5 Part 3 before moving to Phase 5 Part 4.")
        return

    print("\n✅ Ready for Phase 5 Part 4: Strong Optimization Layer")

    # -----------------------------
    # Phase 5 - Part 4: Strong optimization layer
    # -----------------------------
    phase5_part4_passed, phase5_optimization_result = run_phase5_part4_optimizer_test(
        data_bundle=bundle,
        phase3_result=phase3_result,
        stabilized_phase35=stabilized_phase35,
        schedule_result=phase5_improvement_result.improved_schedule,
    )

    if not phase5_part4_passed:
        print("\n❌ Stop here. Fix Phase 5 Part 4 before moving to Phase 6.")
        return

    print("\n✅ Phase 5 completed successfully with strong optimization.")
    print("✅ Ready for Phase 6: Final Output Formatter")

    # -----------------------------
    # Phase 6: Final output formatter
    # -----------------------------
    print("\nStarting Phase 6: Final Output Formatter...")

    phase6_passed, final_rows, final_evaluation = run_phase6_output_formatter_test(
        data_bundle=bundle,
        stabilized_phase35=stabilized_phase35,
        final_schedule_result=phase5_optimization_result.optimized_schedule,
    )

    if not phase6_passed:
        print("\n❌ Stop here. Fix Phase 6 output formatter.")
        return

    print("\n✅ Phase 6 completed successfully.")
    print("✅ PlanX Engine completed successfully.")

    # -----------------------------
    # Phase 6B: Excel export
    # -----------------------------
    # كود التصدير الجديد بالتاريخ والوقت
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    final_filename = f"planx_schedule_{timestamp}.xlsx"

    excel_output_path = export_schedule_to_excel(
        rows=final_rows,
        evaluation=final_evaluation,
        output_path=final_filename, 
    )

    # السطر ده ضروري جداً عشان الـ PHP يعرف يلقط الاسم الجديد
    print(f"GENERATED_FILENAME:{final_filename}")

    print(f"\n✅ Excel file exported successfully: {excel_output_path}")


if __name__ == "__main__":
    
    main()