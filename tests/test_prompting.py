from chartvqa.data import ChartQASample
from chartvqa.prompting import DEFAULT_SYSTEM_MESSAGE, format_chat_sample


def test_format_chat_sample_returns_system_user_and_assistant_messages() -> None:
    sample = ChartQASample(
        image="chart.png",
        question="What is the total revenue?",
        answer="$10M",
    )

    messages = format_chat_sample(sample)

    assert [message["role"] for message in messages] == [
        "system",
        "user",
        "assistant",
    ]
    assert messages[0]["content"] == DEFAULT_SYSTEM_MESSAGE
    assert messages[2]["content"] == "$10M"


def test_format_chat_sample_user_content_contains_image_and_text() -> None:
    sample = {
        "image": "chart.png",
        "question": "Which month is highest?",
        "answer": "March",
    }

    messages = format_chat_sample(sample)
    user_content = messages[1]["content"]

    assert user_content[0] == {"type": "image", "image": "chart.png"}
    assert user_content[1] == {"type": "text", "text": "Which month is highest?"}
