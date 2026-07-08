# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08

## 本次任务

请在远端 AutoDL 环境基于 250 条 badcase 结果，准备一组适合 Gradio Demo 展示的样例素材。

背景：

- 250 条评估中 LoRA 三项指标均超过 Base：
  - Exact Match：0.208 -> 0.224
  - Token F1：0.296 -> 0.315
  - Numeric Accuracy：0.456 -> 0.476
- 250 条 badcase 分析结果：
  - LoRA 改进：6 条
  - LoRA 退化：1 条
  - 两者都对：113 条
  - 两者都错：130 条
- 当前需要把这些结果转成展示材料：哪些样本适合展示 LoRA 改进，哪些样本适合展示模型边界。

## Codex 已完成的本地改动

- 新增 `reports/badcase_analysis_250_summary.md`，整理 250 条 badcase 摘要。
- 更新 `README.md`，将 badcase 章节升级为 250 条分析口径。
- 更新 `reports/experiments.md`，新增“实验 4：250 条 Badcase 分析”。
- 更新 `project_state.md`，记录 250 条 badcase 结果。
- 更新 `实习面试资料.md`，新增“阶段 9：250 条 Badcase 分析”的复盘和面试问答。

## 远端执行前提

远端已有产物：

- `reports/eval_lora_1epoch_250_results.csv`
- `reports/badcase_analysis_250.md`
- `outputs/qwen25vl-chartqa-lora-1epoch/`
- Gradio Demo 已验证可运行。

## 请执行的任务

请从 250 条 badcase 结果中整理 Demo 展示样例，优先选择：

1. LoRA 数值改进样本：例如样本 73、235。
2. LoRA 答案格式改进样本：例如样本 24、205。
3. LoRA 退化样本：样本 142，用于说明模型边界。
4. 两者都错但有代表性的数值推理失败样本，选 2 条即可。

如果方便，请导出这些样本对应的图片到远端 `reports/demo_cases/`，并生成一个 Markdown 文件：

```text
reports/demo_cases.md
```

每个样例请包含：

- 样本 index
- 图片路径
- 问题
- 标准答案
- Base 回答
- LoRA 回答
- 展示用途：格式改进 / 数值改进 / 退化边界 / 共同失败
- 一句话讲解

## 可选验证

如果时间允许，请用 Gradio Demo 手动跑 2 个样本，确认页面上 Base/LoRA 输出与 CSV 记录一致或大体一致。

## 请交回 Codex

- 是否成功生成 `reports/demo_cases.md`。
- 是否导出样本图片；如果导出，请说明路径。
- 推荐用于 Demo 的 3-5 个样本 index。
- 每个推荐样本的一句话展示话术。
- 如果 Gradio 手动验证了样本，请说明结果。

## 判断标准

- Demo 样例不要只展示 LoRA 改进，也要保留至少 1 个边界样本。
- 展示话术要诚实：当前 LoRA 是小幅改进，不是全面超越。
- 优先选择能解释业务价值的样本，例如数值计算、颜色数量、Yes/No 判断。
