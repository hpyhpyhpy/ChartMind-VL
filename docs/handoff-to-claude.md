# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 11:50

## 本次任务

请在远端 AutoDL RTX 4090D 环境执行 **ChartQA 1% 数据完整 1 epoch LoRA 训练**，训练完成后运行 base vs LoRA 评估。

背景：

- 20 steps smoke training 已跑通。
- base vs smoke LoRA 的 20 条评估也已跑通。
- smoke adapter 指标与 base 完全一致，原因是训练步数太少，符合预期。
- 下一步需要让 LoRA 真正训练完整 1 epoch，再做对比。

## Codex 已完成的本地改动

- 新增正式小规模训练配置：`configs/qwen25vl_chartqa_lora_1epoch.yaml`。
- 配置使用 `train[:1%]`、`num_train_epochs: 1`、`max_steps: -1`，不再使用 smoke test 的 20 steps 截断。
- 正式 adapter 输出目录：`outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增测试：`tests/test_formal_training_config.py`。
- 更新 `project_state.md`、`实习面试资料.md` 和本交接文档。

## 远端执行前提

远端已有环境：

- 仓库路径：`/root/autodl-tmp/ChartMind-VL/`
- venv：`/root/autodl-tmp/venv/chartvqa/`
- 快速进入命令：`cvl`
- LoRA adapter：`outputs/qwen25vl-chartqa-smoke/`
- Qwen2.5-VL 模型已缓存到数据盘。

注意：

- 远端 `model.id` 需要指向本地模型缓存路径，不要强行改回 HuggingFace 模型名。
- 非交互式 SSH 不一定加载 `.bashrc`，如需直接远程命令执行，请显式设置 `HF_ENDPOINT`、`HF_HOME`、`LANG`、`LC_ALL`。

## 请执行的命令

进入项目环境：

```bash
cvl
```

确认最新代码已同步后，先跑配置相关测试：

```bash
pytest tests/test_config.py tests/test_formal_training_config.py tests/test_training.py -v
```

执行完整 1 epoch LoRA 训练：

```bash
python scripts/train_lora.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --skip-initial-eval
```

训练完成后执行 100 条样本 base vs LoRA 评估：

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 100 \
  --max-new-tokens 64 \
  --output-csv reports/eval_lora_1epoch_results.csv \
  --summary-json reports/eval_lora_1epoch_summary.json
```

## 预期产物

请确认以下文件生成：

- `outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors`
- `outputs/qwen25vl-chartqa-lora-1epoch/adapter_config.json`
- `reports/eval_lora_1epoch_results.csv`
- `reports/eval_lora_1epoch_summary.json`

请将以下信息交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- 训练耗时。
- 训练 loss 关键日志或最后几行日志。
- adapter 文件大小。
- `reports/eval_lora_1epoch_summary.json` 内容。
- `reports/eval_lora_1epoch_results.csv` 前 5 行。
- GPU 峰值显存或大致显存占用。
- base 与 LoRA 是否都完成了 100 条样本推理。

## 可能风险

- 完整 1 epoch 比 smoke test 更久，建议在 `tmux` 中执行。
- 如果训练 OOM，优先把 `max_pixels` 降低到 `501760`，再重试。
- 如果评估 `both` 模式 OOM，可先分别运行：

```bash
python scripts/run_eval.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --mode base --max-samples 100
python scripts/run_eval.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --mode lora --adapter outputs/qwen25vl-chartqa-lora-1epoch --max-samples 100
```

- 如果 `model.id` 路径报错，请检查远端配置是否仍指向本地模型缓存路径。
- 如果 LoRA 加载失败，请检查 `outputs/qwen25vl-chartqa-lora-1epoch/adapter_config.json` 和 `adapter_model.safetensors` 是否存在。
