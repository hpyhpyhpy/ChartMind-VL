# ChartMind-VL 实验记录

## 实验 1：Smoke Training

- 日期：2026-07-08
- 数据：ChartQA `train[:1%]`
- 模型：`Qwen/Qwen2.5-VL-7B-Instruct`
- 方法：4-bit QLoRA
- LoRA：`r=8`，`alpha=16`，target modules 为 `q_proj`、`v_proj`
- 训练：20 steps
- 输出：`outputs/qwen25vl-chartqa-smoke/`
- 结果：训练链路跑通，adapter 约 4.9 MB。

### 评估

- 评估样本：20 条
- Base 与 LoRA 指标相同。
- 结论：20 steps 只用于验证链路，不足以产生可观测效果差异。

## 实验 2：ChartQA 1% 数据 1 Epoch LoRA

- 日期：2026-07-08
- 数据：ChartQA `train[:1%]`，约 283 条训练样本
- 训练步数：36 steps
- 训练耗时：3 分 02 秒
- 最终 loss：约 17.86
- 输出：`outputs/qwen25vl-chartqa-lora-1epoch/`
- Adapter 大小：约 4.9 MB
- GPU：AutoDL RTX 4090D 24GB
- 显存峰值：约 23 GB

### 评估

评估数据来自 `test[:1%]`，共 25 条样本。原计划评估 100 条，但 `test[:1%]` 实际只有 25 条。

| 指标 | Base | LoRA | 变化 |
|------|------|------|------|
| Exact Match | 0.20 | 0.24 | +0.04 |
| Token F1 | 0.28 | 0.33 | +0.05 |
| Numeric Accuracy | 0.48 | 0.52 | +0.04 |

### 结论

1 epoch LoRA 在三项指标上均超过 Base，说明训练已经产生有效学习信号。当前样本数仍小，不能作为最终效果结论，但足以证明项目已从“链路验证”进入“效果验证”阶段。

### 后续观察

- `test[:1%]` 只有 25 条，如需 100 条评估，需将评估 split 改为 `test[:4%]` 或更大。
- `max_seq_length=128` 偏短，可能限制回答学习效果，后续可尝试 256 或 512。
- 下一步应基于逐样本 CSV 做 badcase 分析，找出 LoRA 答对但 Base 答错、两者都错、LoRA 退化的样本。
