#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from chartvqa.config import load_config
from chartvqa.training import run_training


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Qwen2.5-VL + ChartQA QLoRA smoke training."
    )
    parser.add_argument(
        "--config",
        default="configs/qwen25vl_chartqa.yaml",
        help="Path to the YAML config file.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Override training.max_steps for smoke runs.",
    )
    parser.add_argument(
        "--skip-initial-eval",
        action="store_true",
        help="Skip trainer.evaluate() before training.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    config = load_config(args.config)

    print("== ChartMind-VL LoRA training ==")
    print(f"config: {args.config}")
    print(f"model: {config['model']['id']}")
    print(f"dataset: {config['dataset']['id']}")
    print(f"output_dir: {config['training']['output_dir']}")
    print(f"max_steps: {args.max_steps or config['training']['max_steps']}")

    run_training(
        config,
        max_steps=args.max_steps,
        skip_initial_eval=args.skip_initial_eval,
    )


if __name__ == "__main__":
    main()
