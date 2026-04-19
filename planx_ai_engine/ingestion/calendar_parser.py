from models.calendar_day import CalendarDay
from ingestion.normalizers import clean_text, clean_bool, clean_optional_text
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = ["date", "day_name", "is_exam_day", "is_holiday", "holiday_name", "notes"]


def parse_calendar_days(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "planx_academic_calendar.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            CalendarDay(
                date=clean_text(row["date"]),
                day_name=clean_text(row["day_name"]),
                is_exam_day=clean_bool(row["is_exam_day"]),
                is_holiday=clean_bool(row["is_holiday"]),
                holiday_name=clean_optional_text(row["holiday_name"]),
                notes=clean_optional_text(row["notes"]),
            )
        )
    return result