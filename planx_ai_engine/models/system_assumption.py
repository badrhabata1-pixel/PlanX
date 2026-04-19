from dataclasses import dataclass


@dataclass
class SystemAssumption:
    parameter: str
    value: str
    source_or_reason: str