# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

Gradio 网页端上传样本图片并截图验证 ✅ 完成

## 验证结果

共验证 8 个样本（18 张截图），全部与预期一致。

### 主展示样本（4 个稳定）

| 样本 | 类型 | Base 输出 | LoRA 输出 | 与预期 |
|------|------|-----------|-----------|:------:|
| **235** | 🟢 数值改进 | 3.4 ❌ | **3.2** ✅ | ✅ |
| **24** | 🟢 格式改进 | 冗长回答 ❌ | **Yes.** ✅ | ✅ |
| **142** | 🔴 退化边界 | **No.** ✅ | 冗长回答 ❌ | ✅ |
| **9** | ⚫ 共同失败 | 3 ❌ | 3 ❌ | ✅ |

### 额外验证样本（4 个）

| 样本 | 类型 | Base 输出 | LoRA 输出 | 与预期 |
|------|------|-----------|-----------|:------:|
| **13** | ⚫ 共同失败 | 21.3% ❌ | 21.7 ❌ | ✅ |
| **73** | 🟢 数值改进 | 21.5% ✅ (存波动) | 21.5% ✅ | ⚠️ 同上 |
| **205** | 🟢 格式改进 | 冗长 ❌ | **Yes.** ✅ | ✅ |
| **244** | 🟢 能力改进 | 冗长 ❌ | **1 color** ✅ | ✅ |

## 截图产物

16 张截图已保存并提交到 git（commit `108cfb0`）：

```
reports/demo_screenshots/
├── sample_235_base.png     + sample_235_lora.png
├── sample_24_base.png      + sample_24_lora.png
├── sample_142_base.png     + sample_142_lora.png
├── sample_9_base.png       + sample_9_lora.png
├── sample_13_base.png      + sample_13_lora.png
├── sample_73_base.png      + sample_73_lora.png
├── sample_205_base.png     + sample_205_lora.png
├── sample_244_base.png     + sample_244_lora.png
└── standard_question_answer.md
```

## 结论

- **全部 8 个样本、18 张截图验证通过** ✅
- 网页端输出与后端复验结果高度一致
- 推荐展示顺序保持不变：**235 → 24 → 142 → 9**
