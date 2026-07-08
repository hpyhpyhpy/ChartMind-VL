from chartvqa.config import load_config
from chartvqa.training import build_sft_config_kwargs


def test_formal_training_config_builds_one_epoch_sft_kwargs() -> None:
    config = load_config("configs/qwen25vl_chartqa_lora_1epoch.yaml")

    kwargs = build_sft_config_kwargs(config)

    assert kwargs["output_dir"] == "outputs/qwen25vl-chartqa-lora-1epoch"
    assert kwargs["num_train_epochs"] == 1
    assert kwargs["max_steps"] == -1
    assert kwargs["eval_strategy"] == "no"
    assert kwargs["save_strategy"] == "epoch"
    assert kwargs["bf16"] is True
    assert kwargs["save_only_model"] is True
