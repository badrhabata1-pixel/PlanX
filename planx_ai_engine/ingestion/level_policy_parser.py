from models.level_policy import LevelPolicy
from ingestion.normalizers import clean_text, clean_int, clean_optional_text
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = [
    "level_id",
    "level_name",
    "exam_group",
    "allowed_exam_days",
    "min_gap_days_between_exams",
    "max_exams_per_day",
    "notes",
]


def parse_level_policies(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "planx_level_exam_policy.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            LevelPolicy(
                level_id=clean_int(row["level_id"]),
                level_name=clean_text(row["level_name"]),
                exam_group=clean_text(row["exam_group"]),
                allowed_exam_days=clean_text(row["allowed_exam_days"]),
                min_gap_days_between_exams=clean_int(row["min_gap_days_between_exams"]),
                max_exams_per_day=clean_int(row["max_exams_per_day"]),
                notes=clean_optional_text(row["notes"]),
            )
        )
    return result