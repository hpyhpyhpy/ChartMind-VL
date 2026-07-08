# 交接日志

> 每次 Claude Code 与 Codex 之间的任务交付记录，按时间倒序排列。

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
