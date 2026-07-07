# Local Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建 ChartMind-VL 不消耗 GPU 的本地训练前脚手架。

**Architecture:** 使用 `src/chartvqa/` 承载配置、数据和 prompt 的可复用逻辑；使用 `configs/`、`scripts/`、`tests/` 分别承载实验配置、远程环境入口和本地验证。测试使用纯 Python 样本，避免网络、模型下载和 GPU 依赖。

**Tech Stack:** Python 3.10/3.11、PyYAML、pytest、HuggingFace Datasets、Qwen2.5-VL chat messages、AutoDL RTX 4090 远程执行。

## Global Constraints

- 说明类文档、开发计划、实验记录、README、注释和面向用户的解释默认使用中文。
- 本阶段不加载大模型、不下载完整数据集、不运行训练。
- Claude Code 专属配置默认忽略，不纳入提交。
- 每完成可验收任务，需要更新 `project_state.md` 并提交一次 git commit。
- 本阶段完成后更新 `实习面试资料.md`。

---

### Task 1: 配置与 AutoDL 脚手架

**Files:**
- Create: `requirements.txt`
- Create: `configs/qwen25vl_chartqa.yaml`
- Create: `src/chartvqa/__init__.py`
- Create: `src/chartvqa/config.py`
- Create: `tests/test_config.py`
- Create: `scripts/cloud_setup_autodl.sh`

**Interfaces:**
- Produces: `load_config(path: str | Path = "configs/qwen25vl_chartqa.yaml") -> dict[str, Any]`

- [ ] 写配置加载失败测试，验证缺少文件会抛出 `FileNotFoundError`。
- [ ] 写配置字段测试，验证默认 YAML 包含 `model`、`dataset`、`lora`、`training`、`evaluation`、`output`。
- [ ] 运行 `pytest tests/test_config.py -v`，确认测试因模块缺失失败。
- [ ] 创建依赖、YAML、包入口、配置加载模块和 AutoDL 脚本。
- [ ] 运行 `pytest tests/test_config.py -v`，确认通过。

### Task 2: ChartQA 数据规范化

**Files:**
- Create: `src/chartvqa/data.py`
- Create: `tests/test_data.py`

**Interfaces:**
- Produces: `ChartQASample`
- Produces: `normalize_chartqa_sample(raw: Mapping[str, Any]) -> ChartQASample`
- Produces: `load_chartqa_splits(config: Mapping[str, Any]) -> dict[str, Any]`

- [ ] 写样本规范化测试，覆盖 `query`/`label` 字段。
- [ ] 写字段兼容测试，覆盖 `question`/`answer` 字段。
- [ ] 运行 `pytest tests/test_data.py -v`，确认测试因模块缺失失败。
- [ ] 实现 `ChartQASample`、`normalize_chartqa_sample` 和 `load_chartqa_splits`。
- [ ] 运行 `pytest tests/test_data.py -v`，确认通过。

### Task 3: Qwen2.5-VL Prompt 格式化

**Files:**
- Create: `src/chartvqa/prompting.py`
- Create: `tests/test_prompting.py`

**Interfaces:**
- Produces: `DEFAULT_SYSTEM_MESSAGE: str`
- Produces: `format_chat_sample(sample: ChartQASample | Mapping[str, Any], system_message: str = DEFAULT_SYSTEM_MESSAGE) -> list[dict[str, Any]]`

- [ ] 写 prompt 结构测试，验证 messages 包含 system、user、assistant 三轮。
- [ ] 写 user content 测试，验证同时包含 image 和 text 两种内容。
- [ ] 运行 `pytest tests/test_prompting.py -v`，确认测试因模块缺失失败。
- [ ] 实现 prompt 格式化逻辑。
- [ ] 运行 `pytest tests/test_prompting.py -v`，确认通过。

### Task 4: 阶段文档与验收

**Files:**
- Modify: `project_state.md`
- Create: `实习面试资料.md`

**Interfaces:**
- Produces: 面向复习的阶段总结和面试问答。

- [ ] 更新 `project_state.md`，记录本地训练前脚手架完成状态。
- [ ] 新建或更新 `实习面试资料.md`，用大白话说明本阶段做了什么。
- [ ] 在 `实习面试资料.md` 中补充本阶段关键技术面试问答。
- [ ] 运行全部本地测试：`pytest -v`。
- [ ] 提交本阶段相关文件。
