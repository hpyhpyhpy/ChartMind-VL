import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("scripts/analyze_badcases.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("analyze_badcases", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_args_uses_lora_1epoch_defaults() -> None:
    module = _load_module()

    args = module.parse_args([])

    assert args.input_csv == "reports/eval_lora_1epoch_results.csv"
    assert args.output_md == "reports/badcase_analysis.md"
    assert args.max_cases == 20


def test_render_markdown_includes_summary_and_cases() -> None:
    module = _load_module()
    analysis = {
        "summary": {"lora_improved": 1},
        "cases": [
            {
                "index": "0",
                "case_type": "lora_improved",
                "question": "What is the value?",
                "answer": "42",
                "base_prediction": "40",
                "lora_prediction": "42",
                "base_error_type": "数值错误",
                "lora_error_type": "完全不匹配",
            }
        ],
    }

    markdown = module.render_markdown(analysis, max_cases=5)

    assert "LoRA 改进" in markdown
    assert "What is the value?" in markdown
    assert "base：40" in markdown
    assert "LoRA：42" in markdown
