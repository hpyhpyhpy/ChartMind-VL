# ChartMind-VL 本地脚手架设计说明

## 目标

本阶段在 Codex 本地完成不消耗 GPU 算力的项目框架，为后续 Claude Code 在 AutoDL 远程环境中执行训练 smoke test 做准备。

本阶段范围采用“训练前脚手架”：

- 配置文件与配置加载。
- AutoDL 环境检查脚本。
- ChartQA 样本规范化。
- Qwen2.5-VL chat prompt 格式化。
- 针对配置、数据结构和 prompt 的本地单元测试。

本阶段不加载 `Qwen/Qwen2.5-VL-7B-Instruct` 大模型，不下载完整数据集，不运行训练。

## 架构

项目采用轻量 Python 包结构：`src/chartvqa/` 保存可复用逻辑，`scripts/` 保存命令行入口，`configs/` 保存实验配置，`tests/` 保存本地可运行测试。

本阶段先建立训练链路前半段：

1. `configs/qwen25vl_chartqa.yaml` 描述模型、数据、LoRA、训练、评估和输出路径。
2. `src/chartvqa/config.py` 负责读取 YAML 并校验必要顶层字段。
3. `src/chartvqa/data.py` 定义 `ChartQASample`，并把 ChartQA 原始样本规范成统一字段。
4. `src/chartvqa/prompting.py` 把规范样本转换成 Qwen2.5-VL 可用的 chat messages。
5. `scripts/cloud_setup_autodl.sh` 提供远程环境检查和依赖安装入口。

## 设计边界

- 配置校验只做第一阶段需要的轻量校验，不引入复杂配置系统。
- 数据加载函数支持 HuggingFace Datasets，但测试不依赖网络。
- prompt 输出保持为通用 messages 结构，后续训练 collator 再调用 processor 的 chat template。
- 本地测试只覆盖纯 Python 逻辑，不触发模型下载和 GPU 调用。
- `.claude/` 等 Claude Code 专属配置不纳入本阶段修改。

## 成功标准

- 本地可以运行配置、数据和 prompt 相关单元测试。
- 配置文件包含第一阶段 smoke training 所需关键字段。
- ChartQA 原始样本可以被规范化为 `image`、`question`、`answer`、`question_type`。
- prompt messages 中包含 system、user image/text、assistant answer。
- 项目状态和实习面试资料同步更新。
