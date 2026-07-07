from chartvqa.config import load_config
from chartvqa.modeling import build_bnb_config_kwargs, build_lora_config_kwargs


def test_build_lora_config_kwargs_uses_chartqa_smoke_defaults() -> None:
    config = load_config("configs/qwen25vl_chartqa.yaml")

    kwargs = build_lora_config_kwargs(config)

    assert kwargs == {
        "r": 8,
        "lora_alpha": 16,
        "lora_dropout": 0.1,
        "bias": "none",
        "target_modules": ["q_proj", "v_proj"],
        "task_type": "CAUSAL_LM",
    }


def test_build_bnb_config_kwargs_uses_nf4_double_quantization() -> None:
    config = load_config("configs/qwen25vl_chartqa.yaml")

    kwargs = build_bnb_config_kwargs(config)

    assert kwargs == {
        "load_in_4bit": True,
        "bnb_4bit_use_double_quant": True,
        "bnb_4bit_quant_type": "nf4",
        "bnb_4bit_compute_dtype": "bfloat16",
    }
