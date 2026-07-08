# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 12:22

## 本次任务

请在远端 AutoDL RTX 4090D 环境启动并验证 **ChartMind-VL Gradio Demo**。

背景：

- 1 epoch LoRA 训练已完成，LoRA 在 25 条样本上三项指标均超过 Base。
- 修复后的 badcase 报告已生成。
- Codex 已新增 `app.py`，提供上传图片、输入问题、选择 Base/LoRA 并生成回答的 Demo 入口。

## Codex 已完成的本地改动

- 新增 `app.py`，支持上传图片、输入问题、选择 Base/LoRA 并生成回答。
- Demo 默认配置：`configs/qwen25vl_chartqa_lora_1epoch.yaml`。
- Demo 默认 adapter：`outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增 `tests/test_app.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

## 远端执行前提

远端已有环境：

- 仓库路径：`/root/autodl-tmp/ChartMind-VL/`
- venv：`/root/autodl-tmp/venv/chartvqa/`
- 快速进入命令：`cvl`
- LoRA adapter：`outputs/qwen25vl-chartqa-lora-1epoch/`
- Qwen2.5-VL 模型已缓存到数据盘。
- Gradio 已安装在远端环境中。

注意：

- 本次只验证 Demo 启动和基础交互，不需要重新训练。
- 如果远端还没有同步最新代码，请先同步 `app.py` 和 `tests/test_app.py`。
- 远端 `configs/qwen25vl_chartqa_lora_1epoch.yaml` 的 `model.id` 仍需保持本地模型路径。

## 请执行的命令

进入项目环境：

```bash
cvl
```

确认最新代码已同步后，先跑 Demo 相关测试：

```bash
pytest tests/test_app.py -v
```

确认 adapter 存在：

```bash
ls -lh outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors
```

启动 Demo：

```bash
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 7860
```

## 预期结果

请确认 Gradio Demo 可以访问，并至少完成一次页面加载。

请将以下信息交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- Demo 本地或公网访问地址。
- 页面是否能正常打开。
- Base 模式是否能加载并回答。
- LoRA 模式是否能加载并回答。
- 推理时 GPU 峰值显存或大致显存占用。
- 如能手动测试，请用样本 24 的问题验证 LoRA 是否输出更简洁的 `Yes.` 风格回答。

## 可能风险

- Demo 首次点击会加载模型，可能比较慢。
- Base 与 LoRA 两种模式分别加载模型，显存可能接近 22-23 GB。如 OOM，可只测 LoRA 模式，或重启进程后单独测 Base。
- 如果 `model.id` 路径报错，请检查远端配置是否仍指向本地模型缓存路径。

```bash
python app.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --adapter outputs/qwen25vl-chartqa-lora-1epoch
```
