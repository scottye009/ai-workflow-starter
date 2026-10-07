from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class ClassificationMetrics:
    accuracy: float
    precision: float
    recall: float
    f1: float


def classification_metrics(
    y_true: Iterable[int],
    y_pred: Iterable[int],
) -> ClassificationMetrics:
    true = list(y_true)
    pred = list(y_pred)

    if len(true) != len(pred) or not true:
        raise ValueError("y_true and y_pred must have the same non-zero length.")

    tp = sum(t == 1 and p == 1 for t, p in zip(true, pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(true, pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(true, pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(true, pred))

    accuracy = (tp + tn) / len(true)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return ClassificationMetrics(accuracy, precision, recall, f1)


def task_success_rate(results: Iterable[bool]) -> float:
    values = list(results)
    if not values:
        raise ValueError("results cannot be empty.")
    return sum(values) / len(values)


def escalation_rate(escalated: Iterable[bool]) -> float:
    values = list(escalated)
    if not values:
        raise ValueError("escalated cannot be empty.")
    return sum(values) / len(values)


if __name__ == "__main__":
    print(classification_metrics([1, 1, 0, 0], [1, 0, 0, 0]))
    print("task_success_rate:", task_success_rate([True, True, False]))
