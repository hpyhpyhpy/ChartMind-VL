from chartvqa.evaluation import (
    exact_match,
    numeric_match,
    score_prediction,
    summarize_scores,
    token_f1,
)


def test_exact_match_normalizes_case_punctuation_and_articles() -> None:
    assert exact_match("The Revenue, Growth!", "revenue growth") == 1.0


def test_token_f1_rewards_partial_overlap() -> None:
    assert token_f1("north region revenue", "north revenue") == 0.8


def test_numeric_match_handles_commas_percent_and_text() -> None:
    assert numeric_match("The answer is 1,200.0 dollars", "1200") == 1.0
    assert numeric_match("It increased by 12%", "12") == 1.0
    assert numeric_match("It increased by 13%", "12") == 0.0


def test_score_prediction_returns_all_metrics() -> None:
    scores = score_prediction("42", "42")

    assert scores == {
        "exact_match": 1.0,
        "token_f1": 1.0,
        "numeric_accuracy": 1.0,
    }


def test_summarize_scores_groups_by_mode() -> None:
    rows = [
        {"mode": "base", "exact_match": 1.0, "token_f1": 0.5, "numeric_accuracy": 1.0},
        {"mode": "base", "exact_match": 0.0, "token_f1": 0.5, "numeric_accuracy": 0.0},
        {"mode": "lora", "exact_match": 1.0, "token_f1": 1.0, "numeric_accuracy": 1.0},
    ]

    summary = summarize_scores(rows)

    assert summary["base"] == {
        "count": 2,
        "exact_match": 0.5,
        "token_f1": 0.5,
        "numeric_accuracy": 0.5,
    }
    assert summary["lora"]["count"] == 1
    assert summary["lora"]["exact_match"] == 1.0
