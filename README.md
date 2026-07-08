# ChartMind-VL

面向企业图表、报表和业务看板截图的多模态问答与轻量微调项目。

本项目基于公开 Kaggle notebook 思路、`Qwen/Qwen2.5-VL-7B-Instruct` 和 `HuggingFaceM4/ChartQA` 数据集，完成从数据格式转换、4-bit QLoRA 微调、base vs LoRA 评估、badcase 分析到 Gradio Demo 展示的最小闭环。

## 项目定位

很多企业场景需要让模型理解 BI 看板、财务图表、运营报表和业务截图，并回答自然语言问题。ChartMind-VL 的目标不是做传统 OCR 字段抽取，而是展示现代 VLM 在图表/报表问答任务上的工程化微调流程。

第一阶段重点：

- 基础模型：`Qwen/Qwen2.5-VL-7B-Instruct`
- 数据集：`HuggingFaceM4/ChartQA`
- 微调方法：4-bit QLoRA
- 训练环境：AutoDL RTX 4090D 24GB
- Demo：Gradio

## 当前结果

### Smoke Training

- 数据：ChartQA `train[:1%]`
- 训练：20 steps
- 结果：训练链路跑通，adapter 约 4.9 MB
- 结论：用于验证模型加载、数据读取、LoRA 注入、反向传播和保存 adapter，不用于判断最终效果

### 1 Epoch LoRA

- 数据：ChartQA `train[:1%]`，约 283 条训练样本
- 训练：1 epoch，36 steps
- 耗时：3 分 02 秒
- Adapter：约 4.9 MB
- GPU：AutoDL RTX 4090D 24GB，峰值约 23 GB

初始评估数据为 `test[:1%]`，实际 25 条样本：

| 指标 | Base | LoRA | 变化 |
|------|------|------|------|
| Exact Match | 0.20 | 0.24 | +0.04 |
| Token F1 | 0.28 | 0.33 | +0.05 |
| Numeric Accuracy | 0.48 | 0.52 | +0.04 |

随后扩大到 100 条和 250 条评估样本：

| 评估样本 | EM 变化 | F1 变化 | Numeric 变化 | 观察 |
|----------|---------|---------|--------------|------|
| 25 条 | +0.040 | +0.050 | +0.040 | 样本较少，正向但不稳定 |
| 100 条 | -0.010 | -0.004 | 0.000 | 出现小幅波动 |
| 250 条 | +0.016 | +0.019 | +0.020 | 三项指标均超过 Base |

250 条评估结果：

| 指标 | Base | LoRA | 变化 |
|------|------|------|------|
| Exact Match | 0.208 | 0.224 | +0.016 |
| Token F1 | 0.296 | 0.315 | +0.019 |
| Numeric Accuracy | 0.456 | 0.476 | +0.020 |

结论：1 epoch LoRA 在 250 条评估中三项指标均超过 Base，说明训练产生了微弱但方向一致的学习信号。考虑到当前只使用 `train[:1%]` 和 1 epoch，这个结果更适合作为第一阶段闭环验证，而不是最终性能上限。

## Badcase 分析

远端基于 25 条评估样本生成 badcase 报告：

| 类型 | 数量 |
|------|------|
| LoRA 改进 | 1 |
| LoRA 退化 | 0 |
| 两者都对 | 12 |
| 两者都错 | 12 |

唯一 LoRA 改进样本：

- 问题：`Is the percentage value of "STEM" segment 52?`
- 标准答案：`Yes`
- Base：`Yes, the percentage value of the "STEM" segment is 52%.`
- LoRA：`Yes.`

这说明当前 LoRA 的可见收益主要体现在更接近 ChartQA 短答案风格。典型失败样本主要集中在百分比差值、平均值和时间点判断等数值推理问题。

## Demo

已新增 Gradio Demo：

```bash
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 7860
```

Demo 支持：

- 上传图表或报表截图
- 输入自然语言问题
- 切换 `Base` / `LoRA`
- 展示模型回答

远端验证结果：

- Gradio 页面可正常打开
- Base 模式可加载并回答
- LoRA 模式可加载并回答
- Base 使用 `Qwen2_5_VLForConditionalGeneration`
- LoRA 使用 `PeftModelForCausalLM`

## 目录结构

```text
configs/
  qwen25vl_chartqa.yaml
  qwen25vl_chartqa_lora_1epoch.yaml
src/chartvqa/
  config.py
  data.py
  prompting.py
  modeling.py
  training.py
  inference.py
  evaluation.py
  badcase.py
scripts/
  train_lora.py
  run_eval.py
  run_eval_smoke.py
  analyze_badcases.py
app.py
reports/
  experiments.md
  badcase_analysis.md
tests/
```

## 本地测试

本地测试不加载大模型、不下载数据集、不占用 GPU，主要验证配置、数据格式、prompt、指标、badcase 和脚本参数。

```bash
pytest -v
```

当前本地测试结果：

```text
33 passed
```

## AutoDL 运行流程

进入远端项目环境：

```bash
cvl
```

训练 smoke test：

```bash
python scripts/train_lora.py --config configs/qwen25vl_chartqa.yaml --max-steps 20 --skip-initial-eval
```

正式小规模训练：

```bash
python scripts/train_lora.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --skip-initial-eval
```

评估 base vs LoRA：

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

生成 badcase 报告：

```bash
python scripts/analyze_badcases.py \
  --input-csv reports/eval_lora_1epoch_results.csv \
  --output-md reports/badcase_analysis.md
```

启动 Demo：

```bash
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 7860
```

## 当前限制

- 目前只训练 ChartQA `train[:1%]`，数据量较小。
- 当前最大评估规模为 250 条样本，仍不是完整 test set。
- `max_seq_length=128` 偏短，可能限制图表问答中的复杂推理。
- LoRA 改进样本较少，Demo 中随机样本不一定能明显看到差异。

## 后续计划

- 基于 250 条评估结果生成更完整 badcase 报告，解释 LoRA 改进和退化样本。
- 尝试更长 `max_seq_length`，例如 256 或 512。
- 增加训练数据比例，如 `train[:3%]`。
- 对比 LoRA rank：`r=8`、`r=16`。
- 基于 badcase 构造更适合展示的 Demo 样例。

## 简历描述

基于 Qwen2.5-VL 与公开 ChartQA 数据集二次实现面向企业图表、报表和业务看板的多模态问答系统，完成数据格式转换、4-bit QLoRA 微调、base vs LoRA 对比评估、数值问答 badcase 分析和 Gradio Demo 展示，并在 AutoDL RTX 4090D 环境跑通训练与推理闭环。
