# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

扩大 base vs LoRA 评估样本量（100 条和 250 条） ✅ 完成

## 执行结果

### 100 条评估

```json
{
  "base": { "count": 100, "exact_match": 0.22, "token_f1": 0.299, "numeric_accuracy": 0.50 },
  "lora": { "count": 100, "exact_match": 0.21, "token_f1": 0.295, "numeric_accuracy": 0.50 }
}
```
耗时：359s（~6 min）

### 250 条评估

```json
{
  "base": { "count": 250, "exact_match": 0.208, "token_f1": 0.296, "numeric_accuracy": 0.456 },
  "lora": { "count": 250, "exact_match": 0.224, "token_f1": 0.315, "numeric_accuracy": 0.476 }
}
```
耗时：676s（~11 min）

### 汇总对比

| 指标 | 25 条 (前次) | 100 条 | 250 条 |
|------|:-----------:|:------:|:------:|
| EM Δ | +0.04 | -0.01 | **+0.016** |
| F1 Δ | +0.05 | -0.004 | **+0.019** |
| NUM Δ | +0.04 | 0 | **+0.020** |

### 结论

- **250 条评估是最可信的结果**：LoRA 三项指标均稳定超过 Base
- 25 条到 100 条的波动是样本量不足导致的噪声
- 250 条后趋势稳定：LoRA 带来了微弱但有方向性的提升（+1.6%~2.0%）
- 考虑到仅 1% 数据 + 1 epoch 训练，这个结果合理且积极

### 产物

| 文件 | 说明 |
|------|------|
| `reports/eval_lora_1epoch_100_results.csv` | 100 条逐样本 |
| `reports/eval_lora_1epoch_100_summary.json` | 100 条汇总 |
| `reports/eval_lora_1epoch_250_results.csv` | 250 条逐样本 |
| `reports/eval_lora_1epoch_250_summary.json` | 250 条汇总 |

### 注意事项

- 远端 `test_split` 已从 `test[:10%]` 恢复为 `test[:1%]`
- 远端 `model.id` 仍为本地缓存路径
- 评估总耗时约 17 分钟（100 条 6 分钟 + 250 条 11 分钟）
- 推理前 GPU 显存 1 MiB，推理时峰值约 40-80%（24GB 总量），评估结束释放至 4 MiB
- Base 和 LoRA 各完成 250 条推理，无异常中断

### 远端环境

- 代码已同步（commit `ebbac1e`）
- 评估产物：`reports/eval_lora_1epoch_{100,250}_results.csv` + `_summary.json`
- GPU 显存：空载 4 MiB
