# Claude Code 交接文档 — ChartMind-VL

> 由 Codex 编写。本文只保留最新一次 Codex → Claude Code 交付信息。

## 交付时间

2026-07-08 11:18

## 本次任务

请在远端 AutoDL RTX 4090D 环境执行 **base model vs LoRA adapter 小样本评估 smoke test**。

本次不是继续训练，而是验证评估链路：

- base model zero-shot 可以推理。
- LoRA adapter 可以加载并推理。
- 两种模式使用同一批 ChartQA test 样本。
- 评估脚本可以输出逐样本 CSV 和汇总 JSON。

## Codex 已完成的本地改动

- 新增 `src/chartvqa/evaluation.py`：Exact Match、Token F1、Numeric Accuracy、单条打分与汇总。
- 新增 `src/chartvqa/inference.py`：base model / LoRA adapter 推理封装。
- 新增 `scripts/run_eval.py`：通用评估入口，支持 `base`、`lora`、`both`。
- 新增 `scripts/run_eval_smoke.py`：20 条小样本 base vs LoRA 评估 smoke 入口。
- 新增测试：`tests/test_evaluation.py`、`tests/test_run_eval_script.py`、`tests/test_run_eval_smoke_script.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

## 远端执行前提

远端已有环境：

- 仓库路径：`/root/autodl-tmp/ChartMind-VL/`
- venv：`/root/autodl-tmp/venv/chartvqa/`
- 快速进入命令：`cvl`
- LoRA adapter：`outputs/qwen25vl-chartqa-smoke/`
- Qwen2.5-VL 模型已缓存到数据盘。

注意：远端 `configs/qwen25vl_chartqa.yaml` 的 `model.id` 可能已被替换为本地模型路径。请保持远端可用配置，不要强行改回 HuggingFace 模型名。

## 请执行的命令

进入项目环境：

```bash
cvl
```

确认最新代码已同步后，先跑本地测试：

```bash
pytest tests/test_evaluation.py tests/test_run_eval_script.py tests/test_run_eval_smoke_script.py -v
```

执行小样本评估 smoke test：

```bash
python scripts/run_eval_smoke.py
```

等价于：

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-smoke \
  --split test \
  --max-samples 20 \
  --max-new-tokens 64 \
  --output-csv reports/eval_smoke_results.csv \
  --summary-json reports/eval_smoke_summary.json
```

## 预期产物

请确认以下文件生成：

- `reports/eval_smoke_results.csv`
- `reports/eval_smoke_summary.json`

请将以下信息交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/eval_smoke_summary.json` 内容。
- `reports/eval_smoke_results.csv` 前 5 行。
- GPU 峰值显存或大致显存占用。
- base 与 LoRA 是否都完成了 20 条样本推理。

## 可能风险

- `both` 模式会先加载 base，再加载 LoRA。脚本已在每个模式结束后释放模型并清理 CUDA cache，但如果仍 OOM，可先分别运行：

```bash
python scripts/run_eval.py --mode base --max-samples 20
python scripts/run_eval.py --mode lora --adapter outputs/qwen25vl-chartqa-smoke --max-samples 20
```

- 如果 `model.id` 路径报错，请检查远端配置是否仍指向本地模型缓存路径。
- 如果 LoRA 加载失败，请检查 `outputs/qwen25vl-chartqa-smoke/adapter_config.json` 和 `adapter_model.safetensors` 是否存在。
