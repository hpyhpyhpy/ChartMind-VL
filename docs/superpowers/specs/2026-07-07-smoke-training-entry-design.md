# ChartMind-VL Smoke Training 入口设计说明

## 目标

本阶段补齐从本地训练前脚手架到远程 1-step smoke training 的中间层，让 Claude Code 可以在 AutoDL 上用标准命令验证模型加载、数据读取、LoRA 注入和 adapter 保存。

本阶段本地仍不消耗 GPU：

- 本地测试只覆盖配置参数构造、命令行参数和轻量数据处理。
- 不在本地加载 `Qwen/Qwen2.5-VL-7B-Instruct`。
- 不在本地下载 ChartQA。
- 不在本地运行训练。

## 架构

新增 `src/chartvqa/modeling.py`：

- 构造 BitsAndBytes 4-bit 量化参数。
- 构造 LoRA 参数。
- 在远程依赖存在时加载 Qwen2.5-VL model 和 processor。
- 训练模式下关闭 cache，并启用 gradient checkpointing。

新增 `src/chartvqa/training.py`：

- 构造 TRL `SFTConfig` 参数。
- 将 ChartQA split 转成 chat messages。
- 创建 VLM data collator。
- 组装 `SFTTrainer` 并执行训练保存。

新增 `scripts/train_lora.py`：

- 提供远程 smoke test 标准入口。
- 支持 `--config`、`--max-steps`、`--skip-initial-eval`。
- 默认读取 `configs/qwen25vl_chartqa.yaml`。

## 参考来源

本阶段继续参考公开 Kaggle notebook：

- `research/kaggle_candidates/qwen25vl-chartqa/finetuning-qwen2-5vl-on-chartqa.ipynb`

保留的关键思路：

- 使用 `Qwen/Qwen2.5-VL-7B-Instruct`。
- 使用 `HuggingFaceM4/ChartQA`。
- 使用 4-bit NF4 量化。
- 使用 LoRA target modules：`q_proj`、`v_proj`。
- 使用 TRL `SFTTrainer` 和自定义 VLM collator。

工程化改造：

- 将 notebook 中散落的参数集中到 YAML。
- 将模型配置、训练配置和 collator 拆成独立模块。
- 本地测试不依赖大模型和 GPU。
- 远程执行使用脚本化命令，而不是手动运行 notebook cell。

## 成功标准

- 本地单元测试可以验证 LoRA、量化和 SFT 参数构造。
- 本地单元测试可以验证训练命令参数解析。
- 远程可执行命令固定为：

```bash
python scripts/train_lora.py --config configs/qwen25vl_chartqa.yaml --max-steps 1
```

- 训练成功后 adapter 保存到配置中的 `training.output_dir`。
