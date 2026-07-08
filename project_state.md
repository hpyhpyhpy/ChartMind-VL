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

当前状态：

- 仓库：`ChartMind-VL`
- 主项目方向：面向企业图表与报表的多模态问答微调系统。
- 主技术路线：Qwen2.5-VL + ChartQA + 4-bit QLoRA + AutoDL 4090D。
- 当前阶段：Smoke test 已完成，训练全链路已跑通。
- 远端实验路径：`/root/autodl-tmp/ChartMind-VL/`（数据盘）
  - venv: `/root/autodl-tmp/venv/chartvqa/`
  - 模型缓存: `/root/autodl-tmp/.cache/huggingface/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master/`
  - 训练输出: `outputs/qwen25vl-chartqa-smoke/`
  - 快速进入: `cvl` 别名
- 下一步：交给 Codex 进行 base vs LoRA 评估、badcase 分析、Gradio Demo。
