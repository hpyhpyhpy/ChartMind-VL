#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import gc
import json
import sys
from pathlib import Path
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from chartvqa.config import load_config
from chartvqa.data import load_chartqa_splits, normalize_chartqa_sample
from chartvqa.evaluation import score_prediction, summarize_scores
from chartvqa.inference import answer_chart, load_inference_model


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate ChartMind-VL base model and LoRA adapter on ChartQA."
    )
    parser.add_argument(
        "--config",
        default="configs/qwen25vl_chartqa.yaml",
        help="Path to YAML config.",
    )
    parser.add_argument(
        "--mode",
        choices=["base", "lora", "both"],
        default="both",
        help="Which model variant to evaluate.",
    )
    parser.add_argument(
        "--adapter",
        default="outputs/qwen25vl-chartqa-smoke",
        help="LoRA adapter path for mode=lora or mode=both.",
    )
    parser.add_argument(
        "--split",
        choices=["train", "validation", "test"],
        default="test",
        help="Dataset split to evaluate.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Limit evaluated samples. Defaults to evaluation.max_samples.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=64,
        help="Maximum generated answer tokens.",
    )
    parser.add_argument(
        "--output-csv",
        default="reports/eval_results.csv",
        help="Path to write per-sample results.",
    )
    parser.add_argument(
        "--summary-json",
        default="reports/eval_summary.json",
        help="Path to write aggregate metrics.",
    )
    return parser.parse_args(argv)


def _modes_to_run(mode: str) -> list[str]:
    if mode == "both":
        return ["base", "lora"]
    return [mode]


def _iter_limited(split: Any, limit: int) -> list[Mapping[str, Any]]:
    return [split[index] for index in range(min(limit, len(split)))]


def _evaluate_mode(
    mode: str,
    samples: list[Mapping[str, Any]],
    config: Mapping[str, Any],
    adapter_path: str,
    max_new_tokens: int,
) -> list[dict[str, Any]]:
    resolved_adapter = adapter_path if mode == "lora" else None
    model, processor = load_inference_model(config, resolved_adapter)
    rows: list[dict[str, Any]] = []

    for index, raw_sample in enumerate(samples):
        sample = normalize_chartqa_sample(raw_sample)
        prediction = answer_chart(
            sample,
            model,
            processor,
            max_new_tokens=max_new_tokens,
        )
        scores = score_prediction(prediction, sample.answer)
        rows.append(
            {
                "mode": mode,
                "index": index,
                "question": sample.question,
                "answer": sample.answer,
                "prediction": prediction,
                "question_type": sample.question_type or "",
                **scores,
            }
        )
        print(
            f"[{mode}] {index + 1}/{len(samples)} "
            f"EM={scores['exact_match']:.0f} "
            f"F1={scores['token_f1']:.3f} "
            f"NUM={scores['numeric_accuracy']:.0f}"
        )

    del model
    del processor
    gc.collect()
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:
        pass

    return rows


def _write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "mode",
        "index",
        "question",
        "answer",
        "prediction",
        "question_type",
        "exact_match",
        "token_f1",
        "numeric_accuracy",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: str | Path, payload: Mapping[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    config = load_config(args.config)
    max_samples = (
        args.max_samples
        if args.max_samples is not None
        else int(config["evaluation"]["max_samples"])
    )
    splits = load_chartqa_splits(config)
    samples = _iter_limited(splits[args.split], max_samples)

    print("== ChartMind-VL evaluation ==")
    print(f"config: {args.config}")
    print(f"split: {args.split}")
    print(f"max_samples: {len(samples)}")
    print(f"mode: {args.mode}")

    rows: list[dict[str, Any]] = []
    for mode in _modes_to_run(args.mode):
        rows.extend(
            _evaluate_mode(
                mode=mode,
                samples=samples,
                config=config,
                adapter_path=args.adapter,
                max_new_tokens=args.max_new_tokens,
            )
        )

    summary = summarize_scores(rows)
    _write_csv(args.output_csv, rows)
    _write_json(args.summary_json, summary)
    print(f"wrote rows: {args.output_csv}")
    print(f"wrote summary: {args.summary_json}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
