# Base vs LoRA Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ChartMind-VL 增加 base model zero-shot 与 LoRA adapter 的评估入口。

**Architecture:** `evaluation.py` 负责纯指标；`inference.py` 负责模型加载和单样本生成；`scripts/run_eval.py` 负责远端批量评估和结果落盘。本地测试只覆盖纯 Python 逻辑。

**Tech Stack:** Python 3.10/3.11、Transformers、PEFT、Qwen2.5-VL、ChartQA、pytest、CSV、JSON。

## Global Constraints

- 本地不加载大模型、不下载数据集、不运行真实推理。
- 真实 base vs LoRA 评估在 AutoDL RTX 4090D 上执行。
- 输出默认保存到 `reports/eval_results.csv` 和 `reports/eval_summary.json`。
- 每完成可验收任务，需要更新 `project_state.md`。
- 本阶段完成后更新 `实习面试资料.md`。

---

### Task 1: 评估指标

**Files:**
- Create: `src/chartvqa/evaluation.py`
- Create: `tests/test_evaluation.py`

**Interfaces:**
- Produces: `normalize_answer(text: str) -> str`
- Produces: `exact_match(prediction: str, answer: str) -> float`
- Produces: `token_f1(prediction: str, answer: str) -> float`
- Produces: `numeric_match(prediction: str, answer: str) -> float`
- Produces: `score_prediction(prediction: str, answer: str) -> dict[str, float]`
- Produces: `summarize_scores(rows: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, float]]`

### Task 2: 推理封装

**Files:**
- Create: `src/chartvqa/inference.py`

**Interfaces:**
- Produces: `load_inference_model(config: Mapping[str, Any], adapter_path: str | None = None) -> tuple[Any, Any]`
- Produces: `answer_chart(sample: ChartQASample | Mapping[str, Any], model: Any, processor: Any, max_new_tokens: int = 64) -> str`

### Task 3: 评估脚本

**Files:**
- Create: `scripts/run_eval.py`
- Create: `tests/test_run_eval_script.py`

**Interfaces:**
- Produces: `parse_args(argv: list[str] | None = None) -> argparse.Namespace`
- Produces: `main(argv: list[str] | None = None) -> None`

### Task 4: 阶段文档与验收

**Files:**
- Modify: `project_state.md`
- Modify: `实习面试资料.md`

**Interfaces:**
- Produces: 阶段总结、远端运行命令和面试问答。
