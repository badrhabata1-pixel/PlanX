from dataclasses import dataclass


@dataclass
class DatePeriodSlot:
    slot_id: str
    date: str
    day_name: str
    period_id: str
    start_time: str
    end_time: str
    slot_type: str
    is_schedulable_by_default: bool