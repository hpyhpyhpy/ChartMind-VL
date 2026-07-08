import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("scripts/run_eval_smoke.py")


def _load_run_eval_smoke_module():
    spec = importlib.util.spec_from_file_location("run_eval_smoke", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_args_uses_small_eval_defaults() -> None:
    module = _load_run_eval_smoke_module()

    args = module.parse_args([])

    assert args.config == "configs/qwen25vl_chartqa.yaml"
    assert args.adapter == "outputs/qwen25vl-chartqa-smoke"
    assert args.max_samples == 20
    assert args.max_new_tokens == 64


def test_parse_args_accepts_remote_overrides() -> None:
    module = _load_run_eval_smoke_module()

    args = module.parse_args(
        [
            "--adapter",
            "outputs/custom",
            "--max-samples",
            "5",
            "--max-new-tokens",
            "16",
        ]
    )

    assert args.adapter == "outputs/custom"
    assert args.max_samples == 5
    assert args.max_new_tokens == 16
