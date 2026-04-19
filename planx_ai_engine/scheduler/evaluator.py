from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from scheduler.soft_constraints import (
    PenaltyComponent,
    SoftConstraintWeights,
    evaluate_soft_constraints,
)


@dataclass(frozen=True)
class ScheduleEvaluation:
    total_penalty: int
    components: List[PenaltyComponent] = field(default_factory=list)
    component_penalties: Dict[str, int] = field(default_factory=dict)
    feasible: bool = True
    summary: Dict[str, Any] = field(default_factory=dict)


def evaluate_schedule(
    data_bundle: Any,
    schedule_result: Any,
    weights: SoftConstraintWeights | None = None,
    feasible: bool = True,
) -> ScheduleEvaluation:
    """
    Full Phase 5 evaluator.

    Responsibilities:
    1) Call soft constraint layer
    2) Aggregate total penalty
    3) Build structured evaluation report
    """
    components = evaluate_soft_constraints(
        data_bundle=data_bundle,
        schedule_result=schedule_result,
        weights=weights,
    )

    component_penalties = {
        component.name: component.penalty
        for component in components
    }

    total_penalty = sum(component.penalty for component in components)

    summary = {
        "assigned_exams": len(schedule_result.assignments),
        "unassigned_exams": len(schedule_result.unassigned_exams),
        "component_count": len(components),
    }

    return ScheduleEvaluation(
        total_penalty=total_penalty,
        components=components,
        component_penalties=component_penalties,
        feasible=feasible,
        summary=summary,
    )