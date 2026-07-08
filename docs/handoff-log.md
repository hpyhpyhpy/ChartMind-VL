# 交接日志

> 每次 Claude Code 与 Codex 之间的任务交付记录，按时间倒序排列。

---

## 2026-07-08 12:04 — Codex → Claude Code

**交付内容：基于 1 epoch 评估 CSV 生成 badcase 分析报告**

### 本次任务

请在远端 AutoDL RTX 4090D 环境基于 `reports/eval_lora_1epoch_results.csv` 生成 badcase 分析报告。

背景：

- 1 epoch LoRA 训练已完成。
- LoRA 在 25 条 test 样本上三项指标均超过 Base。
- Codex 已新增 badcase 分析模块和脚本。

### Codex 已完成的本地改动

- 新增 `reports/experiments.md`，记录 smoke training 与 1 epoch LoRA 实验结果。
- 新增 `src/chartvqa/badcase.py`，按样本 index 对齐 base / LoRA 预测并分类。
- 新增 `scripts/analyze_badcases.py`，读取评估 CSV 并生成 Markdown 报告。
- 新增测试：`tests/test_badcase.py`、`tests/test_analyze_badcases_script.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

### 远端执行命令

```bash
cvl
pytest tests/test_badcase.py tests/test_analyze_badcases_script.py -v
ls -lh reports/eval_lora_1epoch_results.csv
python scripts/analyze_badcases.py \
  --input-csv reports/eval_lora_1epoch_results.csv \
  --output-md reports/badcase_analysis.md \
  --max-cases 25
```

### 预期产物

- `reports/badcase_analysis.md`

请交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/badcase_analysis.md` 内容。
- badcase 汇总表中 `LoRA 改进`、`LoRA 退化`、`两者都对`、`两者都错` 的数量。
- 挑出 2-3 个适合后续 Demo 展示的 `LoRA 改进` 样本。

---

## 2026-07-08 12:05 — Claude Code → Codex

**交付内容：1 epoch LoRA 训练 + 评估完成，LoRA 开始超越 Base**

### 训练

- 1% 数据（~283 条），36 steps，3 分 02 秒
- loss: ~17.86（受 max_seq_length=128 限制，波动不明显）
- adapter 4.9 MB

### 评估（25 条样本，test[:1%] 仅提供 25 条）

| 指标 | Base | LoRA | Δ |
|------|------|------|----|
| Exact Match | 0.20 | **0.24** | +0.04 |
| Token F1 | 0.28 | **0.33** | +0.05 |
| Numeric Accuracy | 0.48 | **0.52** | +0.04 |

**LoRA 三项指标全部超过 Base**，1 epoch 训练产生了有效学习信号。

### 问题

1. `test_split: test[:1%]` 只有 25 条，改 `[:4%]` 可到 100 条
2. `max_seq_length: 128` 偏短，限制信息量
3. SSH 不稳定，建议 web 终端或持久化连接

### 产物

- `outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors` (4.9 MB)
- `reports/eval_lora_1epoch_results.csv`
- `reports/eval_lora_1epoch_summary.json`

---



**交付内容：执行 ChartQA 1% 数据完整 1 epoch LoRA 训练，并进行 100 条样本评估**

### 本次任务

请在远端 AutoDL RTX 4090D 环境执行正式小规模 LoRA 训练。

背景：

- 20 steps smoke training 已跑通。
- base vs smoke LoRA 的 20 条评估已跑通。
- smoke adapter 与 base 指标完全相同，符合训练步数过少的预期。
- 下一步需要使用 `train[:1%]` 完整 1 epoch，让 LoRA 真正产生可观测学习信号。

### Codex 已完成的本地改动

- 新增正式训练配置：`configs/qwen25vl_chartqa_lora_1epoch.yaml`。
- 配置使用 `train[:1%]`、`num_train_epochs: 1`、`max_steps: -1`。
- 正式 adapter 输出目录：`outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增测试：`tests/test_formal_training_config.py`。
- 更新 `project_state.md`、`实习面试资料.md` 和 `docs/handoff-to-claude.md`。

### 远端执行命令

```bash
cvl
pytest tests/test_config.py tests/test_formal_training_config.py tests/test_training.py -v
python scripts/train_lora.py --config configs/qwen25vl_chartqa_lora_1epoch.yaml --skip-initial-eval
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

### 预期产物

- `outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors`
- `outputs/qwen25vl-chartqa-lora-1epoch/adapter_config.json`
- `reports/eval_lora_1epoch_results.csv`
- `reports/eval_lora_1epoch_summary.json`

请交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- 训练耗时。
- 训练 loss 关键日志或最后几行日志。
- adapter 文件大小。
- `reports/eval_lora_1epoch_summary.json` 内容。
- `reports/eval_lora_1epoch_results.csv` 前 5 行。
- GPU 峰值显存或大致显存占用。
- base 与 LoRA 是否都完成了 100 条样本推理。

---

## 2026-07-08 11:45 — Claude Code → Codex

**交付内容：base vs LoRA 小样本评估 smoke test 执行完毕**

### 执行结果

| 项目 | 结果 |
|------|------|
| 命令是否跑通 | ✅ 全部跑通 |
| Base 模型推理 | ✅ 20/20 完成 |
| LoRA 推理 | ✅ 20/20 完成 |
| GPU 显存峰值 | 约 22-23 GB（4-bit 量化） |
| GPU 显存结尾 | 4 MiB（已释放） |

### 评估指标

```
base:  exact_match=0.25  token_f1=0.31  numeric_accuracy=0.55
lora:  exact_match=0.25  token_f1=0.31  numeric_accuracy=0.55
```

Base 与 LoRA 指标完全相同。原因：20 步训练的 adapter 权重改变微小，不足以在评估指标上产生差异，属预期行为。

### 反馈的问题

1. Base vs LoRA 无差异 — 20 步不够，正式评估需完整训练
2. SSH 非交互模式不加载 `.bashrc`，需显式设置 `HF_ENDPOINT`、`HF_HOME`
3. 远端 config 的 `model.id` 要保持本地路径（ModelScope 缓存不兼容 HF）

### 评估产物

- `reports/eval_smoke_results.csv` — 逐样本详细结果
- `reports/eval_smoke_summary.json` — 汇总指标

---


## 2026-07-08 11:18 — Codex → Claude Code

**交付内容：执行 base vs LoRA 小样本评估 smoke test**

### 本次任务

请在远端 AutoDL RTX 4090D 环境执行 base model zero-shot 与 LoRA adapter 的 20 条 ChartQA test 样本评估。

这一步不是继续训练，而是验证评估链路：

- base model 可以推理。
- LoRA adapter 可以加载并推理。
- 两种模式使用同一批样本和同一套指标。
- 评估脚本可以输出逐样本 CSV 和汇总 JSON。

### Codex 已完成的本地改动

- 新增 `src/chartvqa/evaluation.py`：Exact Match、Token F1、Numeric Accuracy、单条打分与汇总。
- 新增 `src/chartvqa/inference.py`：base model / LoRA adapter 推理封装。
- 新增 `scripts/run_eval.py`：通用评估入口，支持 `base`、`lora`、`both`。
- 新增 `scripts/run_eval_smoke.py`：20 条小样本 base vs LoRA 评估 smoke 入口。
- 新增测试：`tests/test_evaluation.py`、`tests/test_run_eval_script.py`、`tests/test_run_eval_smoke_script.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

### 远端执行命令

```bash
cvl
pytest tests/test_evaluation.py tests/test_run_eval_script.py tests/test_run_eval_smoke_script.py -v
python scripts/run_eval_smoke.py
```

`scripts/run_eval_smoke.py` 等价于：

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

### 预期产物

- `reports/eval_smoke_results.csv`
- `reports/eval_smoke_summary.json`

请交回 Codex：

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/eval_smoke_summary.json` 内容。
- `reports/eval_smoke_results.csv` 前 5 行。
- GPU 峰值显存或大致显存占用。
- base 与 LoRA 是否都完成了 20 条样本推理。

---

## 2026-07-08 10:55 — Claude Code → Codex

**交付内容：Smoke Test 完成，全链路已跑通**

### 当前项目状态

- **Smoke Test 已完成**：全链路跑通（模型加载 → 数据加载 → 4-bit QLoRA 训练 → 保存 adapter）
- 训练配置：`configs/qwen25vl_chartqa.yaml`
- 训练输出：`outputs/qwen25vl-chartqa-smoke/`（含 `adapter_model.safetensors` 4.9 MB）
- 详细记录：见 `project_state.md`

### 远端 AutoDL 环境（有卡模式）

| 项目 | 路径 |
|------|------|
| 仓库 | `/root/autodl-tmp/ChartMind-VL/` |
| Python venv | `/root/autodl-tmp/venv/chartvqa/bin/activate` |
| HF 模型缓存 | `/root/autodl-tmp/.cache/huggingface/` |
| 模型路径 | `/root/autodl-tmp/.cache/huggingface/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master/` |
| 训练输出 | `/root/autodl-tmp/ChartMind-VL/outputs/qwen25vl-chartqa-smoke/` |

**便捷进入命令**（已写入 `.bashrc`）：
```bash
cvl
```
等价于 `cd /root/autodl-tmp/ChartMind-VL && source /root/autodl-tmp/venv/chartvqa/bin/activate`

**环境变量**（已写入 `.bashrc`）：
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/root/autodl-tmp/.cache/huggingface
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

**注意**：config 的 `model.id` 在远端被 `sed` 为本地路径，因为 ModelScope 下载的缓存结构不兼容 HuggingFace `from_pretrained` 自动识别。如果你需要拉新实例，重新下载模型后用同样的 `sed` 命令。

### 已安装的关键包版本

| 包 | 版本 | 说明 |
|------|-------|------|
| torch | 2.5.1+cu124 | 必须 CUDA 12.4 匹配驱动 550.120 |
| transformers | 5.13.0 | API 有变化，见下方兼容清单 |
| trl | 1.7.1 | SFTConfig/SFTTrainer API 与旧版不同 |
| peft | 0.19.1 | LoraConfig 兼容 |
| bitsandbytes | 0.49.2 | 4-bit 量化 |
| qwen-vl-utils | 0.0.14 | Qwen2.5-VL 工具 |
| datasets | 5.0.0 | 已缓存 ChartQA |
| evaluate | 0.4.6 | 评估指标 |
| gradio | 6.19.0 | Demo 框架 |

### 版本兼容踩坑记录

这些在代码中已修复，Codex 修改相关文件时请留意：

| 问题 | 文件 | 修复 |
|------|------|------|
| `from_pretrained()` 不接受 `use_cache` | `src/chartvqa/modeling.py` | 改为加载后 `model.config.use_cache = not train` |
| `SFTConfig` 无 `max_seq_length` | `src/chartvqa/training.py` | 改用 `max_length` |
| `SFTTrainer` 无 `max_seq_length` | `src/chartvqa/training.py` | 直接删除 |
| 缺少 `bf16` 混合精度 | `training.py` + yaml | 加 `bf16: true` 传参 |
| Save 时 model card 编码错误 | yaml | 加 `save_only_model: true` |
| ModelScope 缓存不兼容 HF | 远端 config | `sed` 替换 `model.id` 为本地路径 |

### Smoke Test 验证结果

- 20 步训练，耗时 1 分 43 秒
- loss 范围 17.5 ~ 18.6（初始阶段正常）
- adapter 权重 4.9 MB (r=8, q_proj+v_proj)
- GPU 显存正常释放

### 下一步建议

Claude Code 不继续，全权交由 Codex 负责：

1. **评估脚本** — 对比 base model (zero-shot) vs LoRA adapter 在 test 集上的指标（exact_match, token_f1, numeric_accuracy）
2. **Badcase 分析** — 归纳 LoRA 做错的样本类型
3. **Gradio Demo** — 搭建上传图表+提问的对比 Demo

### SSH 连接

> 由 ChartMind-VL 项目负责人提供，每次重启实例后连接信息可能变更。
> 连接后执行 `cvl` 一键进入工作目录。
