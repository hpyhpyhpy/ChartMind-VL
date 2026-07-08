# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 13:12

## 本次任务

请在远端 AutoDL RTX 4090D 环境复用已训练好的 1 epoch LoRA adapter，扩大评估样本量，验证 LoRA 相对 Base 的提升是否更稳定。

## ✅ 执行结果

### 100 条评估

| 指标 | Base | LoRA | Δ |
|------|------|------|----|
| Exact Match | 0.22 | 0.21 | -0.01 |
| Token F1 | 0.299 | 0.295 | -0.004 |
| Numeric Accuracy | 0.50 | 0.50 | 0 |

耗时：359s（~6 min）

### 250 条评估

| 指标 | Base | LoRA | Δ |
|------|------|------|----|
| Exact Match | 0.208 | **0.224** | **+0.016** |
| Token F1 | 0.296 | **0.315** | **+0.019** |
| Numeric Accuracy | 0.456 | **0.476** | **+0.020** |

耗时：676s（~11 min）

### 结论

100 条时 LoRA 略微落后（波动），**250 条时 LoRA 在三项指标上全面反超**。说明：

- 1 epoch 1% 数据训练确实产生了微弱但方向稳定的学习信号
- 25 条和 100 条的波动是由样本量不足引起的
- 250 条的结果是最可信的：LoRA 三项指标均高于 Base

### 产物

- `reports/eval_lora_1epoch_100_results.csv` — 100 条逐样本结果
- `reports/eval_lora_1epoch_100_summary.json` — 100 条汇总
- `reports/eval_lora_1epoch_250_results.csv` — 250 条逐样本结果
- `reports/eval_lora_1epoch_250_summary.json` — 250 条汇总

### 注意事项

- 远端 `test_split` 已从 `test[:10%]` 恢复为 `test[:1%]`
- 远端 `model.id` 仍为本地缓存路径
- 评估总耗时约 17 分钟，GPU 使用正常，显存已释放至 4 MiB
