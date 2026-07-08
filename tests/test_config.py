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


def test_lora_1epoch_config_runs_full_epoch_without_smoke_step_cap() -> None:
    config = load_config("configs/qwen25vl_chartqa_lora_1epoch.yaml")

    assert config["dataset"]["train_split"] == "train[:1%]"
    assert config["training"]["output_dir"] == "outputs/qwen25vl-chartqa-lora-1epoch"
    assert config["training"]["num_train_epochs"] == 1
    assert config["training"]["max_steps"] == -1
    assert config["training"]["save_strategy"] == "epoch"
    assert config["training"]["eval_strategy"] == "no"
