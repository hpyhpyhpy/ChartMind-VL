from pathlib import Path
from typing import Any

import yaml


REQUIRED_SECTIONS = {
    "model",
    "dataset",
    "lora",
    "training",
    "evaluation",
    "output",
}


def load_config(path: str | Path = "configs/qwen25vl_chartqa.yaml") -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    if not isinstance(config, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")

    missing_sections = REQUIRED_SECTIONS - set(config)
    if missing_sections:
        missing = ", ".join(sorted(missing_sections))
        raise ValueError(f"Config missing required sections: {missing}")

    return config
