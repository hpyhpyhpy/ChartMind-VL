from collections.abc import Callable, Iterable
from typing import Any, Mapping

from chartvqa.data import load_chartqa_splits
from chartvqa.modeling import build_lora_config, load_model_and_processor
from chartvqa.prompting import format_chat_sample


def build_sft_config_kwargs(
    config: Mapping[str, Any],
    max_steps: int | None = None,
) -> dict[str, Any]:
    training_config = config["training"]
    resolved_max_steps = (
        int(max_steps) if max_steps is not None else int(training_config["max_steps"])
    )

    return {
        "output_dir": training_config["output_dir"],
        "num_train_epochs": int(training_config["num_train_epochs"]),
        "per_device_train_batch_size": int(
            training_config["per_device_train_batch_size"]
        ),
        "per_device_eval_batch_size": int(training_config["per_device_eval_batch_size"]),
        "gradient_accumulation_steps": int(
            training_config["gradient_accumulation_steps"]
        ),
        "gradient_checkpointing": bool(training_config["gradient_checkpointing"]),
        "learning_rate": float(training_config["learning_rate"]),
        "logging_steps": int(training_config["logging_steps"]),
        "eval_steps": int(training_config["eval_steps"]),
        "save_steps": int(training_config["save_steps"]),
        "eval_strategy": training_config["eval_strategy"],
        "save_strategy": training_config["save_strategy"],
        "max_steps": resolved_max_steps,
        "max_seq_length": int(training_config["max_seq_length"]),
        "max_grad_norm": float(training_config["max_grad_norm"]),
        "warmup_steps": int(training_config["warmup_steps"]),
        "load_best_model_at_end": bool(training_config["load_best_model_at_end"]),
        "remove_unused_columns": bool(training_config["remove_unused_columns"]),
        "optim": training_config["optim"],
        "dataset_kwargs": {"skip_prepare_dataset": True},
    }


def format_split_for_training(
    split: Iterable[Mapping[str, Any]],
) -> list[list[dict[str, Any]]]:
    return [format_chat_sample(sample) for sample in split]


def _extract_images(messages: list[dict[str, Any]]) -> list[Any]:
    images: list[Any] = []
    for message in messages:
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if isinstance(item, dict) and item.get("type") == "image":
                images.append(item["image"])
    return images


def create_vlm_collator(processor: Any) -> Callable[[list[list[dict[str, Any]]]], dict[str, Any]]:
    def collate_fn(examples: list[list[dict[str, Any]]]) -> dict[str, Any]:
        texts = [
            processor.apply_chat_template(
                example,
                tokenize=False,
                add_generation_prompt=False,
            )
            for example in examples
        ]
        image_inputs = [_extract_images(example) for example in examples]
        image_inputs = [images[0] if len(images) == 1 else images for images in image_inputs]

        batch = processor(
            text=texts,
            images=image_inputs,
            return_tensors="pt",
            padding=True,
        )
        labels = batch["input_ids"].clone()
        pad_token_id = processor.tokenizer.pad_token_id
        labels[labels == pad_token_id] = -100
        batch["labels"] = labels
        return batch

    return collate_fn


def build_trainer(
    config: Mapping[str, Any],
    max_steps: int | None = None,
) -> Any:
    from trl import SFTConfig, SFTTrainer

    splits = load_chartqa_splits(config)
    train_dataset = format_split_for_training(splits["train"])
    eval_dataset = format_split_for_training(splits["validation"])
    model, processor = load_model_and_processor(config, train=True)
    training_args = SFTConfig(**build_sft_config_kwargs(config, max_steps=max_steps))

    return SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=create_vlm_collator(processor),
        peft_config=build_lora_config(config),
        processing_class=processor,
    )


def run_training(
    config: Mapping[str, Any],
    max_steps: int | None = None,
    skip_initial_eval: bool = False,
) -> None:
    trainer = build_trainer(config, max_steps=max_steps)

    if not skip_initial_eval:
        print("== Initial evaluation ==")
        print(trainer.evaluate())

    print("== Training ==")
    trainer.train()

    print(f"== Saving adapter to {trainer.args.output_dir} ==")
    trainer.save_model(trainer.args.output_dir)
