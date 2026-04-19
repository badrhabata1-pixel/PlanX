from models.exam_rule import ExamRule
from ingestion.normalizers import clean_text, clean_bool
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = ["constraint_type", "description", "is_hard"]


def parse_exam_rules(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "exam_rules.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            ExamRule(
                constraint_type=clean_text(row["constraint_type"]),
                description=clean_text(row["description"]),
                is_hard=clean_bool(row["is_hard"]),
            )
        )
    return result