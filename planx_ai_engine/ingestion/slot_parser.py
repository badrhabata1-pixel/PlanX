from models.date_period_slot import DatePeriodSlot
from ingestion.normalizers import clean_text, clean_bool
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = [
    "slot_id",
    "date",
    "day_name",
    "period_id",
    "start_time",
    "end_time",
    "slot_type",
    "is_schedulable_by_default",
]


def parse_date_period_slots(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "planx_date_period_slots.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            DatePeriodSlot(
                slot_id=clean_text(row["slot_id"]),
                date=clean_text(row["date"]),
                day_name=clean_text(row["day_name"]),
                period_id=clean_text(row["period_id"]),
                start_time=clean_text(row["start_time"]),
                end_time=clean_text(row["end_time"]),
                slot_type=clean_text(row["slot_type"]),
                is_schedulable_by_default=clean_bool(row["is_schedulable_by_default"]),
            )
        )
    return result