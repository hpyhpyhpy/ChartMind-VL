import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("app.py")


def _load_app_module():
    spec = importlib.util.spec_from_file_location("chartmind_app", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_args_uses_lora_1epoch_defaults() -> None:
    module = _load_app_module()

    args = module.parse_args([])

    assert args.config == "configs/qwen25vl_chartqa_lora_1epoch.yaml"
    assert args.adapter == "outputs/qwen25vl-chartqa-lora-1epoch"
    assert args.server_name == "0.0.0.0"
    assert args.server_port == 7860
    assert args.share is False


def test_resolve_adapter_path_only_for_lora_mode() -> None:
    module = _load_app_module()

    assert module.resolve_adapter_path("Base", "outputs/adapter") is None
    assert module.resolve_adapter_path("LoRA", "outputs/adapter") == "outputs/adapter"


def test_answer_uploaded_chart_validates_inputs_before_loading_model() -> None:
    module = _load_app_module()

    assert module.answer_uploaded_chart(None, "question", "Base", "config", "adapter", 8) == (
        "请先上传一张图表或报表截图。"
    )
    assert module.answer_uploaded_chart("image", "", "Base", "config", "adapter", 8) == (
        "请输入一个问题。"
    )
