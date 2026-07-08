from __future__ import annotations

from typing import Any, Mapping

from chartvqa.data import ChartQASample, normalize_chartqa_sample
from chartvqa.modeling import load_model_and_processor
from chartvqa.prompting import format_chat_sample


def load_inference_model(
    config: Mapping[str, Any],
    adapter_path: str | None = None,
) -> tuple[Any, Any]:
    model, processor = load_model_and_processor(config, train=False)

    if adapter_path:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter_path)
        model.eval()
    elif hasattr(model, "eval"):
        model.eval()

    return model, processor


def _extract_first_image(messages: list[dict[str, Any]]) -> Any:
    for message in messages:
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if isinstance(item, dict) and item.get("type") == "image":
                return item["image"]
    raise ValueError("No image found in chat messages")


def _model_device(model: Any) -> Any:
    if hasattr(model, "device"):
        return model.device
    try:
        return next(model.parameters()).device
    except StopIteration:
        return None


def answer_chart(
    sample: ChartQASample | Mapping[str, Any],
    model: Any,
    processor: Any,
    max_new_tokens: int = 64,
) -> str:
    normalized = sample if isinstance(sample, ChartQASample) else normalize_chartqa_sample(sample)
    messages = format_chat_sample(normalized)
    prompt_messages = messages[:2]
    prompt_text = processor.apply_chat_template(
        prompt_messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    image = _extract_first_image(prompt_messages)

    inputs = processor(
        text=[prompt_text],
        images=image,
        return_tensors="pt",
    )
    device = _model_device(model)
    if device is not None and hasattr(inputs, "to"):
        inputs = inputs.to(device)

    generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
    input_ids = inputs["input_ids"]
    trimmed_ids = [
        output_ids[len(source_ids):]
        for source_ids, output_ids in zip(input_ids, generated_ids, strict=True)
    ]
    decoded = processor.batch_decode(
        trimmed_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    return decoded[0].strip()
