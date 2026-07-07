# ChartMind-VL 协作工作流规范

## 目标

本文档用于约定 ChartMind-VL 项目中 Codex、Claude Code 与用户之间的协作边界，避免本地代码建设、远程训练执行和问题分析混在一起。

当前阶段的核心目标是先完成一个可运行、可评估、可展示的最小闭环：

- 基于 `Qwen/Qwen2.5-VL-7B-Instruct`。
- 使用 `HuggingFaceM4/ChartQA` 数据集。
- 采用 4-bit QLoRA 微调。
- 在 AutoDL 单卡 RTX 4090 24GB 环境中完成 smoke test、训练、评估和 Demo 验证。

## 角色分工

### Codex

Codex 负责所有可以在本地提前完成的确定性工作，重点是项目架构、代码基础和问题分析。

Codex 的主要职责：

- 设计项目目录结构和模块边界。
- 编写数据转换、训练、评估、Demo 等代码入口。
- 编写和维护配置文件、运行说明、实验记录模板。
- 根据远程训练日志分析问题原因。
- 修改本地代码并提交可验收变更。
- 维护 `project_state.md`，记录已完成任务和下一步状态。

Codex 默认不负责：

- 直接占用远程 GPU 运行训练。
- 操作 Claude Code 的专属配置。
- 提交 `.claude/` 等 Claude Code 本地配置文件。

### Claude Code

Claude Code 负责通过 VS Code SSH 操作远程算力环境，执行需要 GPU 或远程环境的任务。

Claude Code 的主要职责：

- 在 AutoDL 或同类远程机器上准备运行环境。
- 安装依赖、下载模型和数据集。
- 执行 smoke test、训练、评估和 Gradio Demo。
- 收集并反馈真实日志、报错、显存占用和结果文件。
- 按 Codex 提供的命令或说明在远程环境中验证代码。

Claude Code 的配置文件属于它自己的独立配置。除非用户明确要求，Codex 在提交时应忽略 Claude Code 相关本地配置。

### 用户

用户负责在 Codex 和 Claude Code 之间进行调度，并决定阶段目标。

用户的主要职责：

- 决定当前优先任务。
- 将 Codex 产出的代码和说明同步到远程执行环境。
- 将 Claude Code 远程执行得到的日志、报错和实验结果反馈给 Codex。
- 判断某个阶段是否已经达到可验收标准。

## 推荐协作流程

### 1. 本地准备

Codex 先在本地完成可以提前准备的内容：

- 项目脚手架。
- 数据格式转换脚本。
- 训练 smoke test 入口。
- base vs LoRA 评估入口。
- badcase 分析入口。
- Demo 入口。
- AutoDL 运行说明。
- 实验记录模板。

完成后，Codex 更新 `project_state.md` 并提交一次 git commit。

### 2. 远程执行

用户让 Claude Code 在远程机器上执行对应步骤：

- 拉取或同步最新代码。
- 按文档准备环境。
- 运行指定命令。
- 保存日志、结果文件和关键指标。

远程执行阶段优先验证最小闭环，不优先追求完整训练效果。

### 3. 结果反馈

如果远程执行成功，用户将关键结果反馈给 Codex，用于更新实验记录和下一步计划。

如果远程执行失败，用户将以下信息反馈给 Codex：

- 执行的命令。
- 完整错误日志或关键错误片段。
- Python、CUDA、PyTorch、transformers、peft、bitsandbytes 等关键版本。
- GPU 型号、显存占用和 batch size 等运行参数。
- 失败发生在数据加载、模型加载、训练、评估还是 Demo 阶段。

### 4. 本地修复

Codex 根据远程事实判断问题类型：

- 代码逻辑问题：本地修改代码。
- 数据格式问题：调整转换脚本或数据校验。
- 显存问题：调整 LoRA、量化、batch size、gradient accumulation、max pixels 等配置。
- 依赖问题：更新环境说明或版本约束。
- 平台问题：给出远程操作建议。

修复完成后，Codex 更新文档或代码、更新 `project_state.md`，并提交一次 git commit。

### 5. 再次远程验证

用户再次让 Claude Code 在远程机器上验证 Codex 的修复。

这个循环持续到 smoke test、训练、评估和 Demo 都能形成可展示闭环。

## 交接格式

为了减少来回沟通成本，建议远程执行问题按以下格式反馈给 Codex。

```text
阶段：
执行环境：
执行命令：
期望结果：
实际结果：
关键日志：
显存/资源情况：
已尝试操作：
希望 Codex 判断的问题：
```

示例：

```text
阶段：训练 smoke test
执行环境：AutoDL RTX 4090 24GB，Python 3.10，CUDA 12.1
执行命令：python scripts/train_lora.py --config configs/train_smoke.yaml
期望结果：跑通 20 steps 并保存 LoRA adapter
实际结果：模型加载后 OOM
关键日志：CUDA out of memory ...
显存/资源情况：加载模型后已占用约 22GB
已尝试操作：batch size 从 2 改为 1，仍失败
希望 Codex 判断的问题：是否需要调整 max_pixels、量化配置或模型加载方式
```

## 提交与配置约定

- 每完成一个可验收任务，Codex 必须更新 `project_state.md`。
- 每完成一个可验收任务，Codex 必须进行一次 git commit。
- Codex 提交时只纳入当前任务相关文件。
- `.claude/` 下的本地配置默认不纳入提交。
- Claude Code 专属配置与 Codex 专属配置相互独立，互不覆盖。
- 如果某个文件既可能是项目文档，又可能是工具专属配置，提交前需要由用户确认。

## 当前推荐执行顺序

1. Codex 完成本地最小闭环脚手架。
2. Claude Code 在 AutoDL 上验证环境安装和 smoke test。
3. Codex 根据 smoke test 结果修复代码和配置。
4. Claude Code 执行 base vs LoRA 评估。
5. Codex 整理 badcase、实验记录和简历表述材料。
6. Claude Code 验证 Gradio Demo 可远程运行。
