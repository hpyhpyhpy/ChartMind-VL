# Smoke Training Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 AutoDL 远程 1-step Qwen2.5-VL + ChartQA QLoRA smoke training 提供标准脚本入口。

**Architecture:** `modeling.py` 负责模型、量化和 LoRA；`training.py` 负责 SFT 参数、数据 collator 和 trainer 组装；`scripts/train_lora.py` 负责命令行入口。本地测试只验证纯 Python 参数和接口，不加载大模型。

**Tech Stack:** Python 3.10/3.11、Transformers、PEFT、TRL、BitsAndBytes、HuggingFace Datasets、Qwen2.5-VL、pytest。

## Global Constraints

- 本地不加载大模型、不下载完整数据集、不运行训练。
- 远程 smoke test 命令必须固定且可复制。
- Claude Code 专属配置默认忽略，不纳入提交。
- 每完成可验收任务，需要更新 `project_state.md` 并提交一次 git commit。
- 本阶段完成后更新 `实习面试资料.md`。

---

### Task 1: 模型与 LoRA 配置构造

**Files:**
- Create: `src/chartvqa/modeling.py`
- Create: `tests/test_modeling.py`
- Modify: `configs/qwen25vl_chartqa.yaml`

**Interfaces:**
- Produces: `build_bnb_config_kwargs(config: Mapping[str, Any]) -> dict[str, Any]`
- Produces: `build_lora_config_kwargs(config: Mapping[str, Any]) -> dict[str, Any]`
- Produces: `build_bnb_config(config: Mapping[str, Any]) -> Any`
- Produces: `build_lora_config(config: Mapping[str, Any]) -> Any`
- Produces: `load_model_and_processor(config: Mapping[str, Any], train: bool = False) -> tuple[Any, Any]`

- [ ] 写 LoRA kwargs 测试。
- [ ] 写 BitsAndBytes kwargs 测试。
- [ ] 运行 `pytest tests/test_modeling.py -v`，确认测试因模块缺失失败。
- [ ] 实现 `modeling.py`。
- [ ] 运行 `pytest tests/test_modeling.py -v`，确认通过。

### Task 2: 训练参数与 collator

**Files:**
- Create: `src/chartvqa/training.py`
- Create: `tests/test_training.py`
- Modify: `configs/qwen25vl_chartqa.yaml`

**Interfaces:**
- Produces: `build_sft_config_kwargs(config: Mapping[str, Any], max_steps: int | None = None) -> dict[str, Any]`
- Produces: `format_split_for_training(split: Iterable[Mapping[str, Any]]) -> list[list[dict[str, Any]]]`
- Produces: `create_vlm_collator(processor: Any) -> Callable[[list[list[dict[str, Any]]]], dict[str, Any]]`
- Produces: `build_trainer(config: Mapping[str, Any], max_steps: int | None = None) -> Any`
- Produces: `run_training(config: Mapping[str, Any], max_steps: int | None = None, skip_initial_eval: bool = False) -> None`

- [ ] 写 SFT kwargs 测试，确认 `max_steps` 可以覆盖配置。
- [ ] 写 split 格式化测试，确认 raw sample 会转为 chat messages。
- [ ] 运行 `pytest tests/test_training.py -v`，确认测试因模块缺失失败。
- [ ] 实现 `training.py`。
- [ ] 运行 `pytest tests/test_training.py -v`，确认通过。

### Task 3: 训练命令入口

**Files:**
- Create: `scripts/train_lora.py`
- Create: `tests/test_train_lora_script.py`

**Interfaces:**
- Produces: `parse_args(argv: list[str] | None = None) -> argparse.Namespace`
- Produces: `main(argv: list[str] | None = None) -> None`

- [ ] 写命令行参数解析测试。
- [ ] 运行 `pytest tests/test_train_lora_script.py -v`，确认测试因脚本缺失失败。
- [ ] 实现 `scripts/train_lora.py`。
- [ ] 运行 `pytest tests/test_train_lora_script.py -v`，确认通过。

### Task 4: 阶段文档与验收

**Files:**
- Modify: `project_state.md`
- Modify: `实习面试资料.md`

**Interfaces:**
- Produces: 面向复习的 smoke training 入口阶段总结和面试问答。

- [ ] 更新 `project_state.md`。
- [ ] 更新 `实习面试资料.md`。
- [ ] 运行 `pytest -v`。
- [ ] 提交本阶段相关文件。
