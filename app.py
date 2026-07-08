from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from chartvqa.config import load_config
from chartvqa.inference import answer_chart, load_inference_model


MODE_BASE = "Base"
MODE_LORA = "LoRA"
DEFAULT_CONFIG = "configs/qwen25vl_chartqa_lora_1epoch.yaml"
DEFAULT_ADAPTER = "outputs/qwen25vl-chartqa-lora-1epoch"

_MODEL_CACHE: dict[tuple[str, str | None], tuple[Any, Any]] = {}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch ChartMind-VL Gradio demo.")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help="Path to YAML config.",
    )
    parser.add_argument(
        "--adapter",
        default=DEFAULT_ADAPTER,
        help="LoRA adapter path.",
    )
    parser.add_argument(
        "--server-name",
        default="0.0.0.0",
        help="Gradio server host.",
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=7860,
        help="Gradio server port.",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Enable Gradio public sharing link.",
    )
    return parser.parse_args(argv)


def resolve_adapter_path(mode: str, adapter_path: str) -> str | None:
    return adapter_path if mode == MODE_LORA else None


def _load_cached_model(
    config_path: str,
    adapter_path: str | None,
) -> tuple[Any, Any]:
    cache_key = (config_path, adapter_path)
    if cache_key not in _MODEL_CACHE:
        config = load_config(config_path)
        _MODEL_CACHE[cache_key] = load_inference_model(config, adapter_path)
    return _MODEL_CACHE[cache_key]


def answer_uploaded_chart(
    image: Any,
    question: str,
    mode: str,
    config_path: str,
    adapter_path: str,
    max_new_tokens: int,
) -> str:
    if image is None:
        return "请先上传一张图表或报表截图。"
    if not question or not question.strip():
        return "请输入一个问题。"

    resolved_adapter = resolve_adapter_path(mode, adapter_path)
    model, processor = _load_cached_model(config_path, resolved_adapter)
    return answer_chart(
        {
            "image": image,
            "question": question.strip(),
            "answer": "",
        },
        model,
        processor,
        max_new_tokens=max_new_tokens,
    )


def build_demo(config_path: str, adapter_path: str):
    import gradio as gr

    with gr.Blocks(title="ChartMind-VL") as demo:
        gr.Markdown("# ChartMind-VL")
        with gr.Row():
            image = gr.Image(type="pil", label="图表 / 报表截图")
            with gr.Column():
                question = gr.Textbox(
                    label="问题",
                    placeholder="例如：Which category has the highest value?",
                    lines=3,
                )
                mode = gr.Radio(
                    choices=[MODE_BASE, MODE_LORA],
                    value=MODE_LORA,
                    label="模型",
                )
                max_new_tokens = gr.Slider(
                    minimum=8,
                    maximum=128,
                    value=64,
                    step=8,
                    label="最大生成 token 数",
                )
                submit = gr.Button("生成回答", variant="primary")
        answer = gr.Textbox(label="模型回答", lines=5)

        submit.click(
            fn=answer_uploaded_chart,
            inputs=[
                image,
                question,
                mode,
                gr.State(config_path),
                gr.State(adapter_path),
                max_new_tokens,
            ],
            outputs=answer,
        )

    return demo


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    demo = build_demo(args.config, args.adapter)
    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        share=args.share,
    )


if __name__ == "__main__":
    main()
