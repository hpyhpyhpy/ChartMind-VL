import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("scripts/train_lora.py")


def _load_train_lora_module():
    spec = importlib.util.spec_from_file_location("train_lora", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_args_uses_default_config() -> None:
    module = _load_train_lora_module()

    args = module.parse_args([])

    assert args.config == "configs/qwen25vl_chartqa.yaml"
    assert args.max_steps is None
    assert args.skip_initial_eval is False


def test_parse_args_accepts_smoke_training_overrides() -> None:
    module = _load_train_lora_module()

    args = module.parse_args(
        [
            "--config",
            "custom.yaml",
            "--max-steps",
            "1",
            "--skip-initial-eval",
        ]
    )

    assert args.config == "custom.yaml"
    assert args.max_steps == 1
    assert args.skip_initial_eval is True
