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

## 实验 3：扩大评估样本量

- 日期：2026-07-08
- 模型：`Qwen/Qwen2.5-VL-7B-Instruct`
- Adapter：`outputs/qwen25vl-chartqa-lora-1epoch/`
- 目标：验证 25 条样本上的 LoRA 提升是否能在更大评估样本上保持。

### 100 条评估

- 评估耗时：359 秒，约 6 分钟
- Base 和 LoRA 均完成 100 条推理

| 指标 | Base | LoRA | 变化 |
|------|------|------|------|
| Exact Match | 0.220 | 0.210 | -0.010 |
| Token F1 | 0.299 | 0.295 | -0.004 |
| Numeric Accuracy | 0.500 | 0.500 | 0.000 |

### 250 条评估

- 评估耗时：676 秒，约 11 分钟
- Base 和 LoRA 均完成 250 条推理
- 推理前 GPU 空载约 1 MiB，推理时显存占用约 40%-80%，评估结束释放至约 4 MiB

| 指标 | Base | LoRA | 变化 |
|------|------|------|------|
| Exact Match | 0.208 | 0.224 | +0.016 |
| Token F1 | 0.296 | 0.315 | +0.019 |
| Numeric Accuracy | 0.456 | 0.476 | +0.020 |

### 结论

100 条评估中 LoRA 略低于 Base，说明小样本下仍存在波动。250 条评估中 LoRA 在 EM、F1 和 Numeric Accuracy 三项指标上均超过 Base，说明 1 epoch LoRA 的收益虽然不大，但方向上更稳定。

这个结果比 25 条评估更可信，也更适合写入 README 和简历材料。不过它仍然不是最终性能结论，因为训练只用了 `train[:1%]`，评估也只覆盖了 250 条样本。

### 后续观察

- 基于 `reports/eval_lora_1epoch_250_results.csv` 重新生成 badcase 报告。
- 统计 LoRA 改进、退化、两者都对、两者都错的样本数量。
- 从 250 条结果中筛选更适合 Demo 展示的样例。

## 实验 4：250 条 Badcase 分析

- 日期：2026-07-08
- 输入：`reports/eval_lora_1epoch_250_results.csv`
- 远端完整报告：`reports/badcase_analysis_250.md`
- 本地摘要：`reports/badcase_analysis_250_summary.md`
- 目标：解释 250 条评估中 LoRA 的改进、退化和主要失败类型。

### 汇总

| 类型 | 数量 | 占比 |
|------|------|------|
| LoRA 改进 | 6 | 2.4% |
| LoRA 退化 | 1 | 0.4% |
| 两者都对 | 113 | 45.2% |
| 两者都错 | 130 | 52.0% |

### 代表样本

- 样本 24：Base 输出完整句子，LoRA 输出 `Yes.`，更贴近标准答案 `Yes`。
- 样本 73：Base 未给出最终数值，LoRA 输出 `21.5%`，匹配标准答案 `21.5`。
- 样本 235：Base 将两个最小值相加得到 `3.4`，LoRA 输出正确答案 `3.2`。
- 样本 142：Base 输出 `No.`，LoRA 输出较长解释，从精确匹配退化为部分匹配。

### 结论

250 条 badcase 分析说明，当前 LoRA 的收益主要来自回答格式更短、更贴近 ChartQA 标准答案，同时也修正了少量数值问题。退化样本只有 1 条，风险较低。

主要短板仍是数值类错误。两者都错共有 130 条，占 52.0%，说明 base 和 LoRA 在图表数值读取、数值计算和复杂比较问题上仍然存在共同不足。

### 后续观察

- 从 LoRA 改进样本中筛选 Demo 展示案例。
- 对两者都错的样本继续细分错误类型，判断优先调大 `max_seq_length`、增加训练数据还是调整 prompt。
- 下一轮训练前，优先围绕数值类 badcase 制定实验假设。
