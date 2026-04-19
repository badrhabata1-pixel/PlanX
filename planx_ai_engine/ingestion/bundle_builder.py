from models.data_bundle import PlanXDataBundle


def build_data_bundle(
    courses,
    students,
    enrollments,
    exam_offerings,
    rooms,
    periods,
    calendar_days,
    date_period_slots,
    level_policies,
    exam_rules,
    system_assumptions,
    room_availability,
):
    return PlanXDataBundle(
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