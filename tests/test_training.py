from chartvqa.config import load_config
from chartvqa.training import build_sft_config_kwargs, format_split_for_training


def test_build_sft_config_kwargs_allows_max_steps_override() -> None:
    config = load_config("configs/qwen25vl_chartqa.yaml")

    kwargs = build_sft_config_kwargs(config, max_steps=1)

    assert kwargs["output_dir"] == "outputs/qwen25vl-chartqa-smoke"
    assert kwargs["max_steps"] == 1
    assert kwargs["per_device_train_batch_size"] == 1
    assert kwargs["gradient_accumulation_steps"] == 8
    assert kwargs["dataset_kwargs"] == {"skip_prepare_dataset": True}
    assert kwargs["remove_unused_columns"] is False


def test_format_split_for_training_converts_raw_samples_to_messages() -> None:
    split = [
        {
            "image": "chart.png",
            "query": "What is the value?",
            "label": ["12"],
        }
    ]

    formatted = format_split_for_training(split)

    assert len(formatted) == 1
    assert [message["role"] for message in formatted[0]] == [
        "system",
        "user",
        "assistant",
    ]
    assert formatted[0][1]["content"][0] == {"type": "image", "image": "chart.png"}
    assert formatted[0][2]["content"] == "12"
