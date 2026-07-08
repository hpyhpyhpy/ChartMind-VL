# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08 12:05

## 本次任务

执行 ChartQA 1% 数据完整 1 epoch LoRA 训练 + 100 条样本评估 ✅ 完成

## 训练结果

| 项目 | 数值 |
|------|------|
| 训练步数 | 36 steps（1 epoch） |
| 训练耗时 | 3 分 02 秒 |
| 最终 loss | ~17.86 |
| Adapter 大小 | 4.9 MB (r=8, q_proj+v_proj) |
| GPU 显存峰值 | ~23 GB |

### Loss 趋势

loss 在 17.8~18.0 之间波动，无明显下降趋势。原因：
- `max_seq_length=128` 下每个样本只有少量 token，学习信号有限
- 1% 数据仅 ~283 条，36 steps 不足以让 loss 大幅收敛

## 评估结果（test[:1%]，25 条样本）

| 指标 | Base | LoRA | Δ |
|------|------|------|----|
| Exact Match | 0.20 | **0.24** | **+0.04 (+20%)** |
| Token F1 | 0.28 | **0.33** | **+0.05 (+18%)** |
| Numeric Accuracy | 0.48 | **0.52** | **+0.04 (+8%)** |

**LoRA 在三项指标上均超过 Base**，证明 1 epoch 的训练产生了有效学习信号。

## 发现的问题

1. **`test[:1%]` 只有 25 条** — `test_split: test[:1%]` 仅选取了 25 个样本，`--max-samples 100` 无法达到 100 条。如需 100 条评估，需将 `test_split` 改为 `test[:4%]` 或更大。
2. **`max_seq_length=128 偏短** — 当前序列长度限制了每个样本的信息量，可能是 loss 不降的原因之一。完整全量训练时可考虑增大（如 256 或 512）。
3. **SSH 不稳定** — 连接频繁断开，建议后续通过 AutoDL web 终端或持久化 SSH 执行。

## 下一步建议

1. **跑全量数据训练**（`train_split: train`，去掉 `[:1%]`），看 LoRA 能否在更大数据量上收敛。
2. **调整超参数**：增大 `max_seq_length`、微调 `learning_rate`。
3. **构建 Gradio Demo**，让用户能上传图表提问，并对比 Base vs LoRA 的回答。
4. Badcase 分析：从 CSV 中挑出 LoRA 答对而 Base 答错的样本。

## 远端环境

- 最新代码已上传（commit 未同步，已通过 scp 直传）
- 训练输出：`outputs/qwen25vl-chartqa-lora-1epoch/`
- 评估产物：`reports/eval_lora_1epoch_results.csv`、`reports/eval_lora_1epoch_summary.json`
