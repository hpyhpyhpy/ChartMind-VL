from chartvqa.data import ChartQASample, normalize_chartqa_sample


def test_normalize_chartqa_sample_reads_query_and_label_fields() -> None:
    raw = {
        "image": "chart.png",
        "query": "What is the highest value?",
        "label": "42",
        "type": "human",
    }

    sample = normalize_chartqa_sample(raw)

    assert sample == ChartQASample(
        image="chart.png",
        question="What is the highest value?",
        answer="42",
        question_type="human",
    )


def test_normalize_chartqa_sample_accepts_question_and_answer_fields() -> None:
    raw = {
        "image": "chart.png",
        "question": "Which bar is largest?",
        "answer": ["North"],
        "question_type": "comparison",
    }

    sample = normalize_chartqa_sample(raw)

    assert sample.question == "Which bar is largest?"
    assert sample.answer == "North"
    assert sample.question_type == "comparison"
