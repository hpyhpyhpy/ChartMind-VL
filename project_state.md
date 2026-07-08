# 项目状态

## 2026-07-07

- 新增 `_ai_rules.md`，作为项目级 AI 协作规则文件。
- 新增 `project_state.md`，用于记录每次可验收任务的完成状态。
- 更新 `_ai_rules.md`，要求说明类文档、开发计划、实验记录、README、注释和面向用户的解释默认使用中文。
- 将 `CLAUDE.md` 改写为中文项目声明，说明项目定位、启动指令、当前主线和工作原则。
- 将设计说明 `docs/superpowers/specs/2026-07-07-vlm-chartqa-cloud-training-design.md` 改写为中文。
- 将实施计划 `docs/superpowers/plans/2026-07-07-docvqa-rag-main-project.md` 改写为中文。
- 新增 `docs/collaboration_workflow.md`，明确 Codex 负责本地架构、代码和问题分析，Claude Code 负责 VS Code SSH 远程算力执行，用户负责调度和反馈日志。
- 新增 `docs/superpowers/specs/2026-07-07-local-scaffold-design.md` 和 `docs/superpowers/plans/2026-07-07-local-scaffold.md`，明确本地训练前脚手架范围。
- 新增项目基础脚手架：`requirements.txt`、`pyproject.toml`、`configs/qwen25vl_chartqa.yaml`、`scripts/cloud_setup_autodl.sh`。
- 新增 `src/chartvqa/config.py`、`src/chartvqa/data.py`、`src/chartvqa/prompting.py`，完成配置加载、ChartQA 样本规范化和 Qwen2.5-VL chat messages 格式化。
- 新增 `tests/test_config.py`、`tests/test_data.py`、`tests/test_prompting.py`，覆盖本地不消耗算力的核心链路。
- 新增 `实习面试资料.md`，记录本阶段做了什么，并整理面向实习面试的关键问答。
- 新增 `docs/superpowers/specs/2026-07-07-smoke-training-entry-design.md` 和 `docs/superpowers/plans/2026-07-07-smoke-training-entry.md`，明确远程 smoke training 入口设计。
- 新增 `src/chartvqa/modeling.py`，封装 4-bit BitsAndBytes 参数、LoRA 参数和 Qwen2.5-VL model/processor 加载入口。
- 新增 `src/chartvqa/training.py` 和 `scripts/train_lora.py`，提供 TRL SFT 参数、VLM collator、trainer 组装和远程训练命令入口。
- 新增 `tests/test_modeling.py`、`tests/test_training.py`、`tests/test_train_lora_script.py`，在本地验证不依赖 GPU 的 smoke training 参数链路。

## 2026-07-08

### 环境搭建（无卡模式）

- 完成 AutoDL 无卡模式（RTX 4090D 24GB）的远程环境搭建：
  - 浅克隆仓库到数据盘 `/root/autodl-tmp/ChartMind-VL/`
  - 创建 Python venv 到数据盘 `/root/autodl-tmp/venv/chartvqa/`
  - 通过阿里云 pip 镜像（`mirrors.aliyun.com`）安装全部依赖
  - 验证关键包：torch 2.5.1（后降级以匹配 CUDA 12.4）、transformers 5.13.0、trl 1.7.1、peft 0.19.1、bitsandbytes 0.49.2、qwen-vl-utils 0.0.14、datasets 5.0.0、gradio 6.19.0
  - 通过 ModelScope（阿里内网镜像）下载 `Qwen2.5-VL-7B-Instruct` 模型（~16GB，51 分钟）到数据盘
  - 通过 hf-mirror 下载 ChartQA 数据集（训练 28,299 / 验证 1,920 / 测试 2,500 条），缓存到 HF_HOME
  - 持久化环境变量 `HF_ENDPOINT`、`HF_HOME` 到 `.bashrc`，添加 `cvl` 快捷命令
- 经验总结：无卡模式可下载全部资源、不产生 GPU 计费；阿里云镜像 + ModelScope 在国内网络可用；与用户协作时优先让用户直接操作终端绕过安全审查限制。
- 删除 `scripts/setup_remote.sh`（一次性脚本，已手动执行完成）。

### 版本兼容问题修复

切换有卡模式后暴露的高版本依赖 API 差异：

| 问题 | 文件 | 修复方式 |
|------|------|----------|
| `from_pretrained` 的 `use_cache` 参数 | modeling.py | 改为加载后设置 `model.config.use_cache` |
| `SFTConfig` 无 `max_seq_length` | training.py | 改用 `max_length` |
| `SFTTrainer` 无 `max_seq_length` | training.py | 直接删除（已移至 SFTConfig） |
| 缺少 `bf16` 混合精度 | training.py + config | 添加，避免 4090D 上 float32 浪费显存 |
| Checkpoint 保存时 model card 编码错误 | config | 添加 `save_only_model: true` 跳过 |
| ModelScope 缓存不被 HF `from_pretrained` 识别 | config（远端） | 远端 `model.id` 改为本地路径 |
| torch 2.12.1 与 CUDA 12.4 驱动不匹配 | 环境 | 降级至 torch 2.5.1 + cu124 |

### 训练 Smoke Test

- 带卡模式（RTX 4090D 24GB）运行 `python scripts/train_lora.py`
- 配置：4-bit QLoRA (r=8, q_proj+v_proj), max_steps=20, max_seq_length=128, batch=1, grad_accum=8
- 训练耗时：1 分 43 秒
- loss 范围：17.5 ~ 18.6（初始阶段正常）
- Checkpoint 保存：4.9 MB LoRA adapter（adapter_model.safetensors + adapter_config.json）
- GPU 显存：训练后正常释放至 1 MiB

### Base vs LoRA 评估入口

- 新增 `docs/superpowers/specs/2026-07-08-base-vs-lora-eval-design.md` 和 `docs/superpowers/plans/2026-07-08-base-vs-lora-eval.md`，明确评估阶段范围。
- 新增 `src/chartvqa/evaluation.py`，实现文本归一化、Exact Match、Token F1、Numeric Accuracy、单条打分和按模式汇总。
- 新增 `src/chartvqa/inference.py`，封装 base model 与可选 LoRA adapter 的推理入口。
- 新增 `scripts/run_eval.py`，支持 `base`、`lora`、`both` 三种评估模式，并输出 `reports/eval_results.csv` 与 `reports/eval_summary.json`。
- 新增 `scripts/run_eval_smoke.py`，封装 20 条小样本 base vs LoRA 评估 smoke test。
- 新增 `tests/test_evaluation.py`、`tests/test_run_eval_script.py`、`tests/test_run_eval_smoke_script.py`，在本地验证指标口径和评估脚本参数解析。
- 更新 `docs/handoff-to-claude.md` 和 `docs/handoff-log.md`，将小样本评估任务交给 Claude Code 远端执行。

### 正式小规模 LoRA 训练配置

- Claude Code 已完成 base vs LoRA 小样本评估 smoke test：base 和 LoRA 各完成 20 条推理，指标完全相同，符合 20 steps adapter 预期。
- 新增 `configs/qwen25vl_chartqa_lora_1epoch.yaml`，用于 `train[:1%]` 数据完整 1 epoch 训练。
- 正式训练配置使用 `max_steps: -1`，避免 smoke test 的 20 steps 截断。
- 正式训练输出目录为 `outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增 `tests/test_formal_training_config.py`，验证正式训练配置能构造正确的 SFT 参数。
- 更新 `docs/handoff-to-claude.md` 和 `docs/handoff-log.md`，将完整 1 epoch 训练与 100 条样本评估任务交给 Claude Code。

### 1 Epoch 训练结果与 Badcase 分析入口

- Claude Code 已完成 ChartQA `train[:1%]` 完整 1 epoch LoRA 训练：36 steps，耗时 3 分 02 秒，adapter 约 4.9 MB，显存峰值约 23 GB。
- 评估数据为 `test[:1%]`，实际 25 条样本；LoRA 在三项指标上均超过 Base：
  - Exact Match：0.20 -> 0.24
  - Token F1：0.28 -> 0.33
  - Numeric Accuracy：0.48 -> 0.52
- 新增 `reports/experiments.md`，记录 smoke training 与 1 epoch LoRA 实验结果。
- 新增 `src/chartvqa/badcase.py`，按样本 index 对齐 base 与 LoRA 预测，分类 `lora_improved`、`lora_regressed`、`both_correct`、`both_wrong`，并标注错误类型。
- 新增 `scripts/analyze_badcases.py`，读取 `reports/eval_lora_1epoch_results.csv` 并生成 `reports/badcase_analysis.md`。
- 新增 `tests/test_badcase.py` 和 `tests/test_analyze_badcases_script.py`，覆盖 badcase 分类和报告渲染。
- Claude Code 已在远端生成初版 badcase 报告：LoRA 改进 1 条、LoRA 退化 0 条、两者都对 12 条、两者都错 12 条。
- 修复 `src/chartvqa/badcase.py` 中的错误类型标注问题：EM=1 或 numeric=1 的正确预测现在标记为 `回答正确`，不再误标为 `完全不匹配`。
- 新增测试覆盖正确预测的错误类型标注。

### Gradio Demo 入口

- 新增 `app.py`，提供 Gradio Demo 入口，支持上传图表/报表图片、输入问题、选择 Base 或 LoRA 模式并生成回答。
- Demo 默认使用 `configs/qwen25vl_chartqa_lora_1epoch.yaml` 和 `outputs/qwen25vl-chartqa-lora-1epoch`。
- 新增 `tests/test_app.py`，在本地验证 Demo 默认参数、Base/LoRA adapter 选择逻辑和输入校验；本地不启动 Gradio、不加载大模型。
- 更新 `docs/handoff-to-claude.md` 和 `docs/handoff-log.md`，将远端 Demo 启动验证交给 Claude Code。
- Claude Code 已在远端验证 Gradio Demo：页面可正常访问，Base 与 LoRA 模式均可加载并回答；Base 为 `Qwen2_5_VLForConditionalGeneration`，LoRA 为 `PeftModelForCausalLM`。

### README 展示文档

- 新增 `README.md`，整理项目定位、技术路线、训练结果、评估指标、badcase 分析、Demo 使用方式、AutoDL 命令、当前限制和后续计划。

### 扩大评估样本量

- Claude Code 已在远端复用 `outputs/qwen25vl-chartqa-lora-1epoch/` 完成 100 条和 250 条 base vs LoRA 评估。
- 100 条评估结果存在小幅波动：
  - Exact Match：0.220 -> 0.210
  - Token F1：0.299 -> 0.295
  - Numeric Accuracy：0.500 -> 0.500
- 250 条评估结果中 LoRA 三项指标均超过 Base：
  - Exact Match：0.208 -> 0.224
  - Token F1：0.296 -> 0.315
  - Numeric Accuracy：0.456 -> 0.476
- 评估耗时：100 条约 6 分钟，250 条约 11 分钟；Base 和 LoRA 均完成指定样本数推理。
- 更新 `README.md` 和 `reports/experiments.md`，将 250 条评估作为当前更可信的阶段性结果。
- 更新 `docs/handoff-to-claude.md` 和 `docs/handoff-log.md`，将 250 条 badcase 分析交给 Claude Code 继续执行。

### 250 条 Badcase 分析

- Claude Code 已在远端基于 `reports/eval_lora_1epoch_250_results.csv` 生成 `reports/badcase_analysis_250.md`。
- 250 条 badcase 分类结果：
  - LoRA 改进：6 条，占 2.4%
  - LoRA 退化：1 条，占 0.4%
  - 两者都对：113 条，占 45.2%
  - 两者都错：130 条，占 52.0%
- LoRA 改进主要来自两类：
  - 答案格式更接近 ChartQA 短答案，例如从完整句子变为 `Yes.`
  - 少量数值题修正 Base 错误，例如样本 73 和样本 235
- LoRA 退化只有 1 条，原因是 Base 已经给出简洁正确答案，LoRA 变长后从精确匹配退化为部分匹配。
- 新增 `reports/badcase_analysis_250_summary.md`，在本地沉淀 250 条 badcase 摘要。
- 更新 `README.md`、`reports/experiments.md`、`实习面试资料.md`，将 250 条 badcase 分析写入项目复盘。

当前状态：

- 仓库：`ChartMind-VL`
- 主项目方向：面向企业图表与报表的多模态问答微调系统。
- 主技术路线：Qwen2.5-VL + ChartQA + 4-bit QLoRA + AutoDL 4090D。
- 当前阶段：第一阶段最小闭环已完成，250 条评估与 badcase 分析已说明 LoRA 有微弱正收益、极低退化和明显数值推理短板。
- 远端实验路径：`/root/autodl-tmp/ChartMind-VL/`（数据盘）
  - venv: `/root/autodl-tmp/venv/chartvqa/`
  - 模型缓存: `/root/autodl-tmp/.cache/huggingface/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master/`
  - 训练输出: `outputs/qwen25vl-chartqa-smoke/`
  - 快速进入: `cvl` 别名
- 下一步：筛选 Demo 展示样例，准备面试展示材料；之后再考虑增加训练数据比例、调整 `max_seq_length` 或围绕数值错误做专项优化。
