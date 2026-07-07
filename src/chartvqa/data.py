from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ChartQASample:
    image: Any
    question: str
    answer: str
    question_type: str | None = None


def _first_present(raw: Mapping[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in raw and raw[key] is not None:
            return raw[key]
    raise KeyError(f"Missing any of fields: {', '.join(keys)}")


def _stringify_answer(answer: Any) -> str:
    if isinstance(answer, list | tuple):
        if not answer:
            return ""
        return str(answer[0])
    return str(answer)


def normalize_chartqa_sample(raw: Mapping[str, Any]) -> ChartQASample:
    image = _first_present(raw, ("image", "img", "image_path"))
    question = _first_present(raw, ("query", "question"))
    answer = _first_present(raw, ("label", "answer", "answers"))
    question_type = raw.get("type") or raw.get("question_type")

    return ChartQASample(
        image=image,
        question=str(question),
        answer=_stringify_answer(answer),
        question_type=str(question_type) if question_type is not None else None,
    )


def load_chartqa_splits(config: Mapping[str, Any]) -> dict[str, Any]:
    from datasets import load_dataset

    dataset_config = config["dataset"]
    dataset_id = dataset_config["id"]

    return {
        "train": load_dataset(dataset_id, split=dataset_config["train_split"]),
        "validation": load_dataset(dataset_id, split=dataset_config["validation_split"]),
        "test": load_dataset(dataset_id, split=dataset_config["test_split"]),
    }
