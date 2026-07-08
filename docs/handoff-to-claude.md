# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 13:41

## 本次任务

请在远端 AutoDL RTX 4090D 环境基于 250 条评估结果生成更完整的 badcase 报告，并回传关键统计和代表样本。

背景：

- 1 epoch LoRA 已完成。
- 100 条评估有小幅波动，250 条评估中 LoRA 三项指标均超过 Base：
  - Exact Match：0.208 -> 0.224
  - Token F1：0.296 -> 0.315
  - Numeric Accuracy：0.456 -> 0.476
- 现在需要解释 250 条结果中 LoRA 到底在哪些样本上改进、在哪些样本上退化。

## Codex 已完成的本地改动

- 更新 `README.md`，将当前主要结果从 25 条评估升级为 250 条评估口径。
- 更新 `reports/experiments.md`，新增“实验 3：扩大评估样本量”。
- 更新 `project_state.md`，记录 100 条和 250 条评估结果。
- 更新 `实习面试资料.md`，新增“阶段 8：扩大评估样本量”的复盘和面试问答。

## 远端执行前提

远端已有产物：

- `reports/eval_lora_1epoch_250_results.csv`
- `reports/eval_lora_1epoch_250_summary.json`
- `outputs/qwen25vl-chartqa-lora-1epoch/`

注意：

- 本次不需要重新训练。
- 本次不需要重新跑评估，除非 250 条 CSV 文件缺失。
- 只需要读取已有 CSV 并生成 badcase 报告。

## 请执行的命令

进入项目环境：

```bash
cvl
```

生成 250 条 badcase 报告：

```bash
python scripts/analyze_badcases.py \
  --input-csv reports/eval_lora_1epoch_250_results.csv \
  --output-md reports/badcase_analysis_250.md \
  --max-cases 40
```

查看报告开头：

```bash
sed -n '1,220p' reports/badcase_analysis_250.md
```

## 请交回 Codex

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/badcase_analysis_250.md` 的汇总表。
- LoRA 改进、LoRA 退化、两者都对、两者都错的数量。
- 至少 3 个 LoRA 改进样本，包含问题、标准答案、Base 回答、LoRA 回答。
- 至少 3 个 LoRA 退化样本，如果没有退化样本请说明。
- 你观察到的主要错误类型，例如数值错误、部分匹配、答案格式不一致等。

## 判断标准

- 如果 LoRA 改进样本主要是答案格式更短、更贴近标准答案，说明当前训练更多学到了 ChartQA 答案风格。
- 如果 LoRA 对数值类问题也有明显改进，说明 adapter 不只是改了输出格式，还可能改善了图表问答能力。
- 如果退化样本不少，下一步需要谨慎扩大训练，优先看退化集中在哪些题型。
