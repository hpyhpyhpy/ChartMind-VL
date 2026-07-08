import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("scripts/run_eval.py")


def _load_run_eval_module():
    spec = importlib.util.spec_from_file_location("run_eval", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_args_uses_default_eval_outputs() -> None:
    module = _load_run_eval_module()

    args = module.parse_args([])

    assert args.config == "configs/qwen25vl_chartqa.yaml"
    assert args.mode == "both"
    assert args.split == "test"
    assert args.adapter == "outputs/qwen25vl-chartqa-smoke"
    assert args.output_csv == "reports/eval_results.csv"
    assert args.summary_json == "reports/eval_summary.json"


def test_parse_args_accepts_small_remote_eval_overrides() -> None:
    module = _load_run_eval_module()

    args = module.parse_args(
        [
            "--mode",
            "lora",
            "--adapter",
            "outputs/custom-adapter",
            "--max-samples",
            "20",
            "--max-new-tokens",
            "32",
        ]
    )

    assert args.mode == "lora"
    assert args.adapter == "outputs/custom-adapter"
    assert args.max_samples == 20
    assert args.max_new_tokens == 32
