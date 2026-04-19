from models.room_availability import RoomAvailability
from ingestion.normalizers import clean_text, clean_int, clean_bool, clean_optional_text
from ingestion.validators import validate_required_columns


REQUIRED_COLUMNS = [
    "room_name",
    "room_code",
    "room_type",
    "capacity",
    "date",
    "day_name",
    "period_id",
    "start_time",
    "end_time",
    "slot_type",
    "is_available",
    "notes",
]


def parse_room_availability(df):
    validate_required_columns(df, REQUIRED_COLUMNS, "room_availability_template.csv")

    result = []
    for _, row in df.iterrows():
        result.append(
            RoomAvailability(
                room_name=clean_text(row["room_name"]),
                room_code=clean_text(row["room_code"]),
                room_type=clean_text(row["room_type"]),
                capacity=clean_int(row["capacity"]),
                date=clean_text(row["date"]),
                day_name=clean_text(row["day_name"]),
                period_id=clean_text(row["period_id"]),
                start_time=clean_text(row["start_time"]),
                end_time=clean_text(row["end_time"]),
                slot_type=clean_text(row["slot_type"]),
                is_available=clean_bool(row["is_available"]),
                notes=clean_optional_text(row["notes"]),
            )
        )
    return result