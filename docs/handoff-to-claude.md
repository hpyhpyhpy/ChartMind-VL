# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08

## 本次任务

请在 Gradio 网页端上传推荐样例图片并保存截图，补齐最终展示材料。

背景：

- 你已通过 Python 脚本完成 Demo 后端等价验证。
- 4/5 样本与预期一致：235、24、142、9。
- 样本 73 出现生成波动：Base 本次也答对，因此不建议作为主展示样例。
- 当前还缺真正网页端上传图片的截图验证。

## 推荐截图样例

请优先截图以下 4 个稳定样本：

| 样本 | 类型 | 展示目的 |
|------|------|----------|
| 235 | 数值改进 | 展示 LoRA 修正 Base 加法错误 |
| 24 | 格式改进 | 展示 LoRA 更符合短答案格式 |
| 142 | 退化边界 | 展示 LoRA 并非总是更好 |
| 9 | 共同失败 | 展示当前数值/百分比短板 |

样本 73 可不截图，或作为候选补充截图，但请标记为“有波动”。

## 建议操作

进入远端环境：

```bash
cvl
```

如 Demo 未运行，启动：

```bash
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 6006
```

在网页端上传对应图片：

```text
reports/demo_cases/sample_235.png
reports/demo_cases/sample_24.png
reports/demo_cases/sample_142.png
reports/demo_cases/sample_9.png
```

分别切换 Base 和 LoRA 模式，记录页面输出并保存截图。

## 产物建议

请将截图保存到：

```text
reports/demo_screenshots/
```

建议命名：

```text
sample_235_base.png
sample_235_lora.png
sample_24_base.png
sample_24_lora.png
sample_142_base.png
sample_142_lora.png
sample_9_base.png
sample_9_lora.png
```

## 请交回 Codex

- 是否成功在网页端上传图片并推理。
- 每个样本的 Base 页面输出和 LoRA 页面输出。
- 截图是否保存，保存路径是什么。
- 是否有样本输出和后端等价验证不同。
- 如果网页端操作不方便，请说明原因。

## 判断标准

- 只要网页端输出与后端等价验证大体一致，就可以作为最终展示材料。
- 如果某个样例网页端输出不稳定，就不要放进主展示顺序。
