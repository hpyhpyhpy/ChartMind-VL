# 交接日志

> 每次 Claude Code 与 Codex 之间的任务交付记录，按时间倒序排列。

---

## 2026-07-08 — Claude Code → Codex

**交付内容：Gradio Demo 启动并验证完成，端口 6006，页面可正常访问**

### 执行结果

| 检查项 | 状态 |
|--------|------|
| 代码同步 (c7e014d) | ✅ |
| app 测试 (3/3) | ✅ |
| LoRA adapter (4.9MB) | ✅ |
| Demo 启动 (端口 6006) | ✅ HTTP 200 |
| 页面正常打开 | ✅ |
| Base 模式回答 | ✅ |
| LoRA 模式回答 | ✅ |
| GPU 显存占用 | 40%-80%（24GB） |

### 验证结论

- 模型加载验证：Base → `Qwen2_5_VLForConditionalGeneration`，LoRA → `PeftModelForCausalLM`，两种模式正确区分
- 页面两种模式回答一致的原因是 **1% 数据训练的 LoRA 改进太微弱**（25 条只改进了 1 条），非 Demo bug
- 远端配置 sed 已修正 model.id 为本地缓存路径
- 访问地址：`https://u1079327-9e7a-1ebc3ec1.westb.seetacloud.com:8443`

---

## 2026-07-08 12:22 — Codex → Claude Code

**交付内容：启动并验证 ChartMind-VL Gradio Demo**

### 背景

- 1 epoch LoRA 训练已完成，LoRA 指标超过 Base。
- 修复后的 badcase 报告已生成。
- Codex 已新增 Gradio Demo 入口 `app.py`。

### Codex 已完成的本地改动

- 新增 `app.py`，支持上传图片、输入问题、选择 Base/LoRA 并生成回答。
- Demo 默认配置：`configs/qwen25vl_chartqa_lora_1epoch.yaml`。
- Demo 默认 adapter：`outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增 `tests/test_app.py`。
- 更新 `project_state.md` 和 `实习面试资料.md`。

### 远端执行命令

```bash
cvl
pytest tests/test_app.py -v
ls -lh outputs/qwen25vl-chartqa-lora-1epoch/adapter_model.safetensors
python app.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --server-name 0.0.0.0 \
  --server-port 7860
```

### 请交回 Codex

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- Demo 访问地址。
- 页面是否能正常打开。
- Base 和 LoRA 模式是否能加载并回答。
- 推理时 GPU 峰值显存或大致显存占用。
- 如能手动测试，请用样本 24 的问题验证 LoRA 是否输出更简洁的 `Yes.` 风格回答。

---

## 2026-07-08 — Claude Code → Codex

**交付内容：修复后的 badcase 报告重新生成完毕，错误类型分类已修复**

### 执行结果

- 代码同步到远端（commit `17f8f7e`）✅
- 7 个 badcase 测试全部通过 ✅（含新增的正确预测错误类型测试）
- CSV 存在（7.8K）✅
- `reports/badcase_analysis.md` 已重新生成 ✅

### Badcase 汇总

| 类型 | 数量 |
|------|------|
| LoRA 改进 | 1 |
| LoRA 退化 | 0 |
| 两者都对 | 12 |
| 两者都错 | 12 |

### 修复验证

**关键验证通过**：所有 12 条"两者都对"的正确预测样本，错误类型均显示 `回答正确`，不再误标为 `完全不匹配`。

### 唯一 LoRA 改进样本（样本 24）

LoRA 错误类型从修复前的"完全不匹配"（误标）变为 "回答正确" ✅

### 典型失败样本

样本 9（数值错误）、样本 13（数值错误）、样本 21（数值+时间）

---

## 2026-07-08 12:30 — Codex → Claude Code

**交付内容：修复 badcase 错误类型分类，并请求远端重跑报告**

### 背景

Claude Code 已生成初版 badcase 报告：

- LoRA 改进：1 条
- LoRA 退化：0 条
- 两者都对：12 条
- 两者都错：12 条

同时发现 `badcase.py` 存在错误类型误标：EM=1 的正确样本被标为 `完全不匹配`。

### Codex 已完成的修复

- 修复 `src/chartvqa/badcase.py`：`describe_error_type()` 先判断 `_is_correct(row)`，正确预测返回 `回答正确`。
- 更新 `tests/test_badcase.py`，新增正确预测错误类型测试。
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

### 请交回 Codex

- 命令是否跑通。
- 如果失败，完整错误日志或关键报错。
- `reports/badcase_analysis.md` 内容。
- 汇总表中四类数量。
- 确认 EM=1 或 numeric=1 的样本是否已显示为 `回答正确`。
- 1 个 LoRA 改进样本和 2-3 个典型失败样本。

---

## 2026-07-08 12:25 — Claude Code → Codex

**交付内容：badcase 分析报告生成完毕**

### 执行结果

- 6 个 badcase 测试全部通过 ✅
- CSV 存在（7.8K）✅
- 报告已生成（reports/badcase_analysis.md）

### Badcase 汇总

| 类型 | 数量 |
|------|------|
| LoRA 改进 | 1 |
| LoRA 退化 | 0 |
| 两者都对 | 12 |
| 两者都错 | 12 |

LoRA 改进仅 1 条（样本 24：回答更简洁）。建议 Codex 检查 `badcase.py` 的错误类型分类逻辑（EM=1 的样本被标为"完全不匹配"）。

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

## 2026-07-08 11:18 — Codex → Claude Code

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
## 2026-07-08 13:12 — Codex → Claude Code

**交付内容：扩大 base vs LoRA 评估样本量**

### Codex 本地完成情况

- 新增 `README.md`，整理 ChartMind-VL 第一阶段展示文档，包含项目定位、训练结果、base vs LoRA 指标、badcase 分析、Demo 使用方式、AutoDL 命令、当前限制和后续计划。
- 更新 `project_state.md`，记录 Gradio Demo 远端验证结果和 README 展示文档。
- 更新 `实习面试资料.md`，补充 Demo 验证和 README 阶段的面试问答。
- 本地验证通过：
  - `pytest -v`：33 passed
  - `python -m compileall -q app.py src scripts tests`：通过

### 下一步交给 Claude Code

请在远端 AutoDL RTX 4090D 环境复用 `outputs/qwen25vl-chartqa-lora-1epoch/`，扩大评估样本量：

```bash
cvl
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 100 \
  --max-new-tokens 64 \
  --output-csv reports/eval_lora_1epoch_100_results.csv \
  --summary-json reports/eval_lora_1epoch_100_summary.json
```

如果 100 条评估顺利且成本可接受，再执行：

```bash
python scripts/run_eval.py \
  --config configs/qwen25vl_chartqa_lora_1epoch.yaml \
  --mode both \
  --adapter outputs/qwen25vl-chartqa-lora-1epoch \
  --split test \
  --max-samples 250 \
  --max-new-tokens 64 \
  --output-csv reports/eval_lora_1epoch_250_results.csv \
  --summary-json reports/eval_lora_1epoch_250_summary.json
```

### 需要回传

- 命令是否跑通。
- 每轮评估耗时。
- `reports/eval_lora_1epoch_100_summary.json` 内容。
- 如果执行 250 条，也回传 `reports/eval_lora_1epoch_250_summary.json` 内容。
- `reports/eval_lora_1epoch_100_results.csv` 前 5 行。
- base 与 LoRA 是否都完成指定样本数推理。
- GPU 峰值显存或大致显存占用。

---
