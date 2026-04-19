from dataclasses import dataclass
from typing import Optional


@dataclass
class RoomAvailability:
    room_name: str
    room_code: str
    room_type: str
    capacity: int
    date: str
    day_name: str
    period_id: str
    start_time: str
    end_time: str
    slot_type: str
    is_available: bool
    notes: Optional[str] = None