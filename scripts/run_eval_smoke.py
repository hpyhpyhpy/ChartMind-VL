#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from run_eval import main as run_eval_main


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a small base vs LoRA evaluation smoke test."
    )
    parser.add_argument(
        "--config",
        default="configs/qwen25vl_chartqa.yaml",
        help="Path to YAML config.",
    )
    parser.add_argument(
        "--adapter",
        default="outputs/qwen25vl-chartqa-smoke",
        help="LoRA adapter path.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=20,
        help="Number of test samples for the smoke evaluation.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=64,
        help="Maximum generated answer tokens.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run_eval_main(
        [
            "--config",
            args.config,
            "--mode",
            "both",
            "--adapter",
            args.adapter,
            "--split",
            "test",
            "--max-samples",
            str(args.max_samples),
            "--max-new-tokens",
            str(args.max_new_tokens),
            "--output-csv",
            "reports/eval_smoke_results.csv",
            "--summary-json",
            "reports/eval_smoke_summary.json",
        ]
    )


if __name__ == "__main__":
    main()
