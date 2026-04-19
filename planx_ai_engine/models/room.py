from dataclasses import dataclass


@dataclass
class Room:
    """
    Represents a room that can host exams.
    """
    room_id: str
    room_name: str
    capacity: int
    room_type: str
    building: str | None = None
    is_available: bool = True

from dataclasses import dataclass
from typing import Optional


@dataclass
class Room:
    room_name: str
    room_code: str
    capacity: int
    room_type: str
    faculty: Optional[str] = None