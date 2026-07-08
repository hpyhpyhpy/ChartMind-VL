from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable
from typing import Any, Mapping


NUMBER_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?%?")


def _to_float(value: Any) -> float:
    return float(value)


def _is_correct(row: Mapping[str, Any]) -> bool:
    return (
        _to_float(row.get("exact_match", 0.0)) >= 1.0
        or _to_float(row.get("numeric_accuracy", 0.0)) >= 1.0
    )


def classify_pair(
    base_row: Mapping[str, Any],
    lora_row: Mapping[str, Any],
) -> str:
    base_correct = _is_correct(base_row)
    lora_correct = _is_correct(lora_row)

    if not base_correct and lora_correct:
        return "lora_improved"
    if base_correct and not lora_correct:
        return "lora_regressed"
    if base_correct and lora_correct:
        return "both_correct"
    return "both_wrong"


def _has_number(text: str) -> bool:
    return bool(NUMBER_RE.search(text))


def describe_error_type(row: Mapping[str, Any]) -> str:
    if _is_correct(row):
        return "回答正确"

    answer = str(row.get("answer", ""))
    prediction = str(row.get("prediction", ""))
    exact = _to_float(row.get("exact_match", 0.0))
    token = _to_float(row.get("token_f1", 0.0))
    numeric = _to_float(row.get("numeric_accuracy", 0.0))

    if _has_number(answer) and _has_number(prediction) and numeric < 1.0:
        return "数值错误"
    if exact < 1.0 and token > 0.0:
        return "部分匹配但不精确"
    if prediction.strip() == "":
        return "空回答"
    return "完全不匹配"


def analyze_badcases(
    rows: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    by_index: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        index = str(row["index"])
        mode = str(row["mode"])
        by_index.setdefault(index, {})[mode] = row

    cases: list[dict[str, Any]] = []
    summary_counter: Counter[str] = Counter()

    for index in sorted(by_index, key=lambda item: int(item) if item.isdigit() else item):
        pair = by_index[index]
        if "base" not in pair or "lora" not in pair:
            continue

        base_row = pair["base"]
        lora_row = pair["lora"]
        case_type = classify_pair(base_row, lora_row)
        summary_counter[case_type] += 1

        cases.append(
            {
                "index": index,
                "case_type": case_type,
                "question": base_row.get("question", ""),
                "answer": base_row.get("answer", ""),
                "base_prediction": base_row.get("prediction", ""),
                "lora_prediction": lora_row.get("prediction", ""),
                "base_error_type": describe_error_type(base_row),
                "lora_error_type": describe_error_type(lora_row),
                "base_exact_match": _to_float(base_row.get("exact_match", 0.0)),
                "lora_exact_match": _to_float(lora_row.get("exact_match", 0.0)),
                "base_token_f1": _to_float(base_row.get("token_f1", 0.0)),
                "lora_token_f1": _to_float(lora_row.get("token_f1", 0.0)),
                "base_numeric_accuracy": _to_float(
                    base_row.get("numeric_accuracy", 0.0)
                ),
                "lora_numeric_accuracy": _to_float(
                    lora_row.get("numeric_accuracy", 0.0)
                ),
            }
        )

    return {
        "summary": dict(summary_counter),
        "cases": cases,
    }
