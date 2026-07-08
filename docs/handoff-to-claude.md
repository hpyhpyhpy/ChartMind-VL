# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 12:04

## 本次任务

请在远端 AutoDL RTX 4090D 环境基于最新评估 CSV 生成 **badcase 分析报告**。

背景：

- 1 epoch LoRA 训练已跑通，耗时 3 分 02 秒。
- LoRA 在 25 条 test 样本上三项指标均超过 Base。
- 评估结果已在远端 `reports/eval_lora_1epoch_results.csv`。
- Codex 已新增 badcase 分析脚本，需要 Claude Code 在远端用真实 CSV 生成报告。

## Codex 已完成的本地改动

- 新增 `reports/experiments.md`，记录 smoke training 与 1 epoch LoRA 实验结果。
- 新增 `src/chartvqa/badcase.py`，按样本 index 对齐 base / LoRA 预测并分类：
  - `lora_improved`
  - `lora_regressed`
  - `both_correct`
  - `both_wrong`
- 新增 `scripts/analyze_badcases.py`，读取评估 CSV 并生成 Markdown 报告。
- 新增测试：`tests/test_badcase.py`、`tests/test_analyze_badcases_script.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

## 远端执行前提

远端已有环境：

- 仓库路径：`/root/autodl-tmp/ChartMind-VL/`
- venv：`/root/autodl-tmp/venv/chartvqa/`
- 快速进入命令：`cvl`
- LoRA adapter：`outputs/qwen25vl-chartqa-lora-1epoch/`
- 评估 CSV：`reports/eval_lora_1epoch_results.csv`
- Qwen2.5-VL 模型已缓存到数据盘。

注意：

- 本次只生成 badcase 报告，不需要重新训练。
- 如果远端还没有同步最新代码，请先同步 Codex 本次新增的 `src/chartvqa/badcase.py` 和 `scripts/analyze_badcases.py`。

## 请执行的命令

进入项目环境：

```bash
cvl
```

确认最新代码已同步后，先跑 badcase 相关测试：

```bash
pytest tests/test_badcase.py tests/test_analyze_badcases_script.py -v
```

确认评估 CSV 存在：

```bash
ls -lh reports/eval_lora_1epoch_results.csv
```

生成 badcase 报告：

```bash
python scripts/analyze_badcases.py \
  --input-csv reports/eval_lora_1epoch_results.csv \
  --output-md reports/badcase_analysis.md \
  --max-cases 25
```

## 预期产物

请确认以下文件生成：

- `reports/badcase_analysis.md`

请将以下信息交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/badcase_analysis.md` 内容。
- badcase 汇总表中 `LoRA 改进`、`LoRA 退化`、`两者都对`、`两者都错` 的数量。
- 挑出 2-3 个适合后续 Demo 展示的 `LoRA 改进` 样本。

## 可能风险

- 如果报告中没有 `LoRA 改进` 样本，也请如实反馈。这可能是因为 25 条样本太少。
- 如果远端 CSV 只有 base 或只有 LoRA 行，说明评估文件不完整，需要重新运行评估脚本。

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 100 \
  --output-csv reports/eval_lora_1epoch_results.csv \
  --summary-json reports/eval_lora_1epoch_summary.json
```
