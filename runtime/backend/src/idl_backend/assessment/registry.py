from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Any, Callable

from .tasks.classification import generate_classification_scenario
from .tasks.decision import analyze_decision_intake, generate_extra_decision_factors
from .tasks.loss import parse_probability_loss_design
from .tasks.short_answer import evaluate_short_answer


TaskHandler = Callable[[dict[str, Any], float], dict[str, Any]]


@dataclass(frozen=True)
class Endpoint:
    path: str
    handler: TaskHandler
    request_example: str


ENDPOINTS = (
    Endpoint("/classification/scenario", generate_classification_scenario, "{subject, context?}"),
    Endpoint("/decision/intake", analyze_decision_intake, "{decision}"),
    Endpoint(
        "/decision/extra-factors",
        generate_extra_decision_factors,
        "{decision, positive_label, negative_label, primary_factor_name, context?}",
    ),
    Endpoint("/short-answer/evaluate", evaluate_short_answer, "{question, reference_answer, answer} or {task_id, answer}"),
    Endpoint("/loss/probability-design", parse_probability_loss_design, "{answer}"),
)

ROUTES = {endpoint.path: endpoint.handler for endpoint in ENDPOINTS}
