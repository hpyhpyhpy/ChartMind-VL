from typing import Any, Mapping

from chartvqa.data import ChartQASample, normalize_chartqa_sample


DEFAULT_SYSTEM_MESSAGE = (
    "You are ChartMind-VL, a visual question answering assistant for business "
    "charts, reports, and dashboards. Answer accurately and keep the answer concise."
)


def _as_chartqa_sample(sample: ChartQASample | Mapping[str, Any]) -> ChartQASample:
    if isinstance(sample, ChartQASample):
        return sample
    return normalize_chartqa_sample(sample)


def format_chat_sample(
    sample: ChartQASample | Mapping[str, Any],
    system_message: str = DEFAULT_SYSTEM_MESSAGE,
) -> list[dict[str, Any]]:
    normalized = _as_chartqa_sample(sample)

    return [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": [
                {"type": "image", "image": normalized.image},
                {"type": "text", "text": normalized.question},
            ],
        },
        {
            "role": "assistant",
            "content": normalized.answer,
        },
    ]
