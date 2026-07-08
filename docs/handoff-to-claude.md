# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 13:12

## 本次任务

请在远端 AutoDL RTX 4090D 环境复用已训练好的 1 epoch LoRA adapter，扩大评估样本量，验证 LoRA 相对 Base 的提升是否更稳定。

背景：

- 第一阶段最小闭环已经完成：训练 smoke test、1 epoch LoRA、base vs LoRA 评估、badcase 分析、Gradio Demo 均已跑通。
- 当前已知指标来自 `test[:1%]`，实际只有 25 条样本：
  - EM：0.20 -> 0.24
  - F1：0.28 -> 0.33
  - Numeric Accuracy：0.48 -> 0.52
- 25 条样本可以证明链路和学习信号，但不足以作为更稳的实验结论。
- Codex 已新增 `README.md`，并更新 `project_state.md` 与 `实习面试资料.md`，把第一阶段成果整理为展示材料。

## Codex 已完成的本地改动

- 新增 `README.md`，整理项目定位、训练结果、评估指标、badcase、Demo、AutoDL 命令、当前限制和后续计划。
- 更新 `project_state.md`，记录 Gradio Demo 远端验证结果和 README 展示文档。
- 更新 `实习面试资料.md`，补充 Demo 验证和 README 阶段的面试问答。
- 本地验证通过：
  - `pytest -v`：33 passed
  - `python -m compileall -q app.py src scripts tests`：通过

## 远端执行前提

远端已有环境：

- 仓库路径：`/root/autodl-tmp/ChartMind-VL/`
- venv：`/root/autodl-tmp/venv/chartvqa/`
- 快速进入命令：`cvl`
- LoRA adapter：`outputs/qwen25vl-chartqa-lora-1epoch/`
- Qwen2.5-VL 模型已缓存到数据盘。

注意：

- 本次不需要重新训练，只做扩大评估。
- 远端 `configs/qwen25vl_chartqa_lora_1epoch.yaml` 的 `model.id` 仍需保持本地模型路径：

```text
/root/autodl-tmp/.cache/huggingface/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master/
```

## 请执行的命令

进入项目环境：

```bash
cvl
```

确认 adapter 存在：

```bash
ls -lh outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors
```

建议先跑 100 条样本评估。如果耗时和显存可接受，再跑 250 条。

### 100 条评估

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 100 \
  --max-new-tokens 64 \
  --output-csv reports/eval_lora_1epoch_100_results.csv \
  --summary-json reports/eval_lora_1epoch_100_summary.json
```

### 可选：250 条评估

如果 100 条评估顺利完成，且单次运行成本可接受，请继续执行：

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 250 \
  --max-new-tokens 64 \
  --output-csv reports/eval_lora_1epoch_250_results.csv \
  --summary-json reports/eval_lora_1epoch_250_summary.json
```

## 预期产物

- `reports/eval_lora_1epoch_100_results.csv`
- `reports/eval_lora_1epoch_100_summary.json`
- 可选：
  - `reports/eval_lora_1epoch_250_results.csv`
  - `reports/eval_lora_1epoch_250_summary.json`

## 请交回 Codex

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- 每轮评估耗时。
- `reports/eval_lora_1epoch_100_summary.json` 内容。
- 如果执行了 250 条，也请给出 `reports/eval_lora_1epoch_250_summary.json` 内容。
- `reports/eval_lora_1epoch_100_results.csv` 前 5 行。
- base 与 LoRA 是否都完成指定样本数推理。
- GPU 峰值显存或大致显存占用。

## 判断标准

- 如果 100 条或 250 条上 LoRA 仍优于 Base，说明 1 epoch LoRA 的收益比 25 条结果更可信。
- 如果提升消失或反转，也不是失败，说明 25 条样本存在波动；下一步应优先做更细 badcase 分析，而不是直接扩大训练。
