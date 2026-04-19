from dataclasses import dataclass


@dataclass
class ExamRule:
    constraint_type: str
    description: str
    is_hard: bool