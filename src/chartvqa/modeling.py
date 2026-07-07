from typing import Any, Mapping


def build_bnb_config_kwargs(config: Mapping[str, Any]) -> dict[str, Any]:
    model_config = config["model"]
    return {
        "load_in_4bit": bool(model_config.get("load_in_4bit", True)),
        "bnb_4bit_use_double_quant": bool(
            model_config.get("bnb_4bit_use_double_quant", True)
        ),
        "bnb_4bit_quant_type": str(model_config.get("bnb_4bit_quant_type", "nf4")),
        "bnb_4bit_compute_dtype": str(
            model_config.get("bnb_4bit_compute_dtype", model_config.get("torch_dtype", "bfloat16"))
        ),
    }


def build_lora_config_kwargs(config: Mapping[str, Any]) -> dict[str, Any]:
    lora_config = config["lora"]
    return {
        "r": int(lora_config["r"]),
        "lora_alpha": int(lora_config["alpha"]),
        "lora_dropout": float(lora_config["dropout"]),
        "bias": str(lora_config.get("bias", "none")),
        "target_modules": list(lora_config["target_modules"]),
        "task_type": str(lora_config.get("task_type", "CAUSAL_LM")),
    }


def _resolve_torch_dtype(dtype_name: str) -> Any:
    import torch

    dtype_map = {
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
        "float32": torch.float32,
    }
    if dtype_name not in dtype_map:
        raise ValueError(f"Unsupported torch dtype: {dtype_name}")
    return dtype_map[dtype_name]


def build_bnb_config(config: Mapping[str, Any]) -> Any:
    from transformers import BitsAndBytesConfig

    kwargs = build_bnb_config_kwargs(config)
    kwargs["bnb_4bit_compute_dtype"] = _resolve_torch_dtype(
        kwargs["bnb_4bit_compute_dtype"]
    )
    return BitsAndBytesConfig(**kwargs)


def build_lora_config(config: Mapping[str, Any]) -> Any:
    from peft import LoraConfig

    return LoraConfig(**build_lora_config_kwargs(config))


def load_model_and_processor(
    config: Mapping[str, Any],
    train: bool = False,
) -> tuple[Any, Any]:
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

    model_config = config["model"]
    model_id = model_config["id"]
    load_in_4bit = bool(model_config.get("load_in_4bit", True))

    model_kwargs: dict[str, Any] = {
        "device_map": "auto",
        "use_cache": not train,
    }
    if load_in_4bit:
        model_kwargs["quantization_config"] = build_bnb_config(config)
    else:
        model_kwargs["torch_dtype"] = _resolve_torch_dtype(
            str(model_config.get("torch_dtype", "bfloat16"))
        )

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_id,
        **model_kwargs,
    )
    processor_kwargs = {
        key: model_config[key]
        for key in ("min_pixels", "max_pixels")
        if model_config.get(key) is not None
    }
    processor = AutoProcessor.from_pretrained(model_id, **processor_kwargs)

    if hasattr(processor, "tokenizer"):
        processor.tokenizer.padding_side = "right"

    if train and bool(config["training"].get("gradient_checkpointing", True)):
        model.gradient_checkpointing_enable()

    return model, processor
