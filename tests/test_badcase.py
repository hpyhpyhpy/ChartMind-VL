from chartvqa.badcase import analyze_badcases, classify_pair, describe_error_type


def test_classify_pair_finds_lora_improvement() -> None:
    base = {"exact_match": 0.0, "token_f1": 0.2, "numeric_accuracy": 0.0}
    lora = {"exact_match": 1.0, "token_f1": 1.0, "numeric_accuracy": 1.0}

    assert classify_pair(base, lora) == "lora_improved"


def test_classify_pair_finds_lora_regression() -> None:
    base = {"exact_match": 1.0, "token_f1": 1.0, "numeric_accuracy": 1.0}
    lora = {"exact_match": 0.0, "token_f1": 0.0, "numeric_accuracy": 0.0}

    assert classify_pair(base, lora) == "lora_regressed"


def test_describe_error_type_prioritizes_numeric_errors() -> None:
    row = {
        "answer": "12.5",
        "prediction": "13.1",
        "exact_match": 0.0,
        "token_f1": 0.0,
        "numeric_accuracy": 0.0,
    }

    assert describe_error_type(row) == "数值错误"


def test_analyze_badcases_groups_base_and_lora_rows_by_index() -> None:
    rows = [
        {
            "mode": "base",
            "index": "0",
            "question": "What is the value?",
            "answer": "42",
            "prediction": "40",
            "exact_match": "0.0",
            "token_f1": "0.0",
            "numeric_accuracy": "0.0",
        },
        {
            "mode": "lora",
            "index": "0",
            "question": "What is the value?",
            "answer": "42",
            "prediction": "42",
            "exact_match": "1.0",
            "token_f1": "1.0",
            "numeric_accuracy": "1.0",
        },
    ]

    result = analyze_badcases(rows)

    assert result["summary"]["lora_improved"] == 1
    assert result["cases"][0]["case_type"] == "lora_improved"
    assert result["cases"][0]["base_prediction"] == "40"
    assert result["cases"][0]["lora_prediction"] == "42"
