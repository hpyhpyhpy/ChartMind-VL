from pathlib import Path

import pytest

from chartvqa.config import load_config


def test_load_config_raises_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(missing_path)


def test_default_config_contains_required_sections() -> None:
    config = load_config("configs/qwen25vl_chartqa.yaml")

    assert set(config) >= {
        "model",
        "dataset",
        "lora",
        "training",
        "evaluation",
        "output",
    }
