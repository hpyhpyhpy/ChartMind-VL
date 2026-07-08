# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 13:55

## 本次任务

请在远端 Gradio Demo 中手动验证推荐展示样例，确认页面实际输出与 `reports/demo_cases.md` 和评估 CSV 记录一致或大体一致。

背景：

- 你已基于 250 条 badcase 生成 `reports/demo_cases.md`。
- 你已导出 8 张图片到 `reports/demo_cases/`。
- 当前尚未进行 Gradio 页面手动验证。
- Codex 已将 Demo 样例结果写入 `README.md`、`reports/experiments.md`、`project_state.md` 和 `实习面试资料.md`，但明确标注为“尚未手动验证”。

## 请优先验证的样本

请至少验证 3 个样本：

| 样本 | 类型 | 期望观察 |
|------|------|----------|
| 235 | 数值改进 | Base 倾向算错，LoRA 应输出或接近 `3.2` |
| 24 | 格式改进 | LoRA 应比 Base 更接近 `Yes.` |
| 142 | 退化边界 | Base 应比 LoRA 更简洁、更接近 `No.` |

如果时间允许，再验证：

| 样本 | 类型 | 期望观察 |
|------|------|----------|
| 73 | 数值改进 | LoRA 应输出或接近 `21.5` |
| 9 | 共同失败 | Base 和 LoRA 都可能答 `3`，标准答案是 `0.03` |

## 建议操作

进入远端环境：

```bash
cvl
```

如果 Demo 没有运行，请启动：

```bash
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 6006
```

然后在 Gradio 页面中上传对应图片，例如：

```text
reports/demo_cases/sample_235.png
reports/demo_cases/sample_24.png
reports/demo_cases/sample_142.png
```

分别用 Base 和 LoRA 模式提问，记录页面输出。

## 请交回 Codex

- 手动验证了哪些样本 index。
- 每个样本的 Base 页面输出。
- 每个样本的 LoRA 页面输出。
- 是否与 `reports/demo_cases.md` 中记录一致或大体一致。
- 如果输出不同，请说明差异。
- Demo 页面是否仍可正常访问。
- 如方便，请保存截图路径或说明无法截图。

## 判断标准

- 只要输出与 CSV 记录大体一致，就可以将这些样例作为正式展示样例。
- 如果生成结果有随机波动，需要记录波动，并优先选择更稳定的样例。
- 如果某个推荐样例在页面上不稳定，就从 `reports/demo_cases.md` 里的其他样本替换。
