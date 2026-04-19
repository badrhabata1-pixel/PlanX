from models.system_assumption import SystemAssumption
from ingestion.normalizers import clean_text
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = ["parameter", "value", "source_or_reason"]


def parse_system_assumptions(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "planx_system_assumptions.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            SystemAssumption(
                parameter=clean_text(row["parameter"]),
                value=clean_text(row["value"]),
                source_or_reason=clean_text(row["source_or_reason"]),
            )
        )
    return result