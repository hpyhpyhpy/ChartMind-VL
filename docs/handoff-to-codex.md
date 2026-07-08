# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

基于 250 条 badcase 整理 Gradio Demo 展示样例 ✅ 完成

## 执行结果

| 检查项 | 状态 |
|--------|------|
| 导出样本图片 | ✅ 8 张 (reports/demo_cases/) |
| 生成 reports/demo_cases.md | ✅ 136 行，8 个样例 |

## 导出的样本图片

| 文件 | 大小 |
|------|------|
| reports/demo_cases/sample_24.png | 25K |
| reports/demo_cases/sample_73.png | 105K |
| reports/demo_cases/sample_205.png | 46K |
| reports/demo_cases/sample_235.png | 61K |
| reports/demo_cases/sample_244.png | 40K |
| reports/demo_cases/sample_142.png | 23K |
| reports/demo_cases/sample_9.png | 79K |
| reports/demo_cases/sample_13.png | 36K |

## 推荐 Demo 展示顺序（5 个样本）

| 顺序 | Index | 类型 | 一句话话术 |
|------|-------|------|-----------|
| 1 | **235** | 🟢 数值改进 | Base 加法算错（1.6+1.8=3.4），LoRA 算出 3.2 正确 |
| 2 | **24** | 🟢 格式改进 | LoRA 简洁 "Yes." vs Base 冗长 |
| 3 | **73** | 🟢 数值改进 | LoRA 完整计算 21.5，Base 回答中断 |
| 4 | **142** | 🔴 退化边界 | Base 完美 "No."，LoRA 变啰嗦 |
| 5 | **9** | ⚫ 共同失败 | 百分比差值问题，都答 3 而非 0.03 |

展示叙事："LoRA 有进步 → 也有局限 → 我们清楚问题在哪"

## 图片路径说明

远端路径：
- Markdown: `/root/autodl-tmp/ChartMind-VL/reports/demo_cases.md`
- 图片: `/root/autodl-tmp/ChartMind-VL/reports/demo_cases/sample_*.png`

如需在 Gradio Demo 中使用，图片路径需相对于 Demo 运行目录。
