from __future__ import annotations

import re
import string
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any, Mapping


METRIC_NAMES = ("exact_match", "token_f1", "numeric_accuracy")
NUMBER_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?%?")


def normalize_answer(text: str) -> str:
    lowered = text.lower()
    without_punctuation = lowered.translate(str.maketrans("", "", string.punctuation))
    tokens = [
        token
        for token in without_punctuation.split()
        if token not in {"a", "an", "the"}
    ]
    return " ".join(tokens)


def exact_match(prediction: str, answer: str) -> float:
    return float(normalize_answer(prediction) == normalize_answer(answer))


def token_f1(prediction: str, answer: str) -> float:
    prediction_tokens = normalize_answer(prediction).split()
    answer_tokens = normalize_answer(answer).split()

    if not prediction_tokens and not answer_tokens:
        return 1.0
    if not prediction_tokens or not answer_tokens:
        return 0.0

    common = Counter(prediction_tokens) & Counter(answer_tokens)
    overlap = sum(common.values())
    if overlap == 0:
        return 0.0

    precision = overlap / len(prediction_tokens)
    recall = overlap / len(answer_tokens)
    return 2 * precision * recall / (precision + recall)


def _extract_numbers(text: str) -> list[float]:
    numbers: list[float] = []
    for match in NUMBER_RE.findall(text):
        cleaned = match.replace(",", "").rstrip("%")
        try:
            numbers.append(float(cleaned))
        except ValueError:
            continue
    return numbers


def numeric_match(prediction: str, answer: str) -> float:
    prediction_numbers = _extract_numbers(prediction)
    answer_numbers = _extract_numbers(answer)

    if not answer_numbers:
        return exact_match(prediction, answer)
    if not prediction_numbers:
        return 0.0

    for answer_number in answer_numbers:
        if any(_close_number(predicted, answer_number) for predicted in prediction_numbers):
            return 1.0
    return 0.0


def _close_number(left: float, right: float) -> bool:
    tolerance = max(1e-3, abs(right) * 1e-3)
    return abs(left - right) <= tolerance


def score_prediction(prediction: str, answer: str) -> dict[str, float]:
    return {
        "exact_match": exact_match(prediction, answer),
        "token_f1": token_f1(prediction, answer),
        "numeric_accuracy": numeric_match(prediction, answer),
    }


def summarize_scores(
    rows: Iterable[Mapping[str, Any]],
) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["mode"])].append(row)

    summary: dict[str, dict[str, float | int]] = {}
    for mode, mode_rows in grouped.items():
        count = len(mode_rows)
        mode_summary: dict[str, float | int] = {"count": count}
        for metric_name in METRIC_NAMES:
            mode_summary[metric_name] = sum(
                float(row[metric_name]) for row in mode_rows
            ) / count
        summary[mode] = mode_summary

    return summary
