# ChartMind-VL 实施计划

> **给后续执行者的要求：** 按任务逐项执行。每完成一个可验收任务，需要更新 `project_state.md` 并提交一次 git commit。任务勾选使用 `- [ ]` 格式维护进度。

**目标：** 构建一个可写入简历、可演示、可评估的多模态问答与微调项目。项目面向企业图表、报表和业务文档截图，主路线为 Qwen2.5-VL + ChartQA + LoRA/QLoRA，并使用 AutoDL 单卡 4090 作为训练环境。

**架构：** 第一阶段采用现代 VLM 微调流程：图表/报表图片 + 问题 -> Qwen2.5-VL prompt 格式化 -> zero-shot baseline -> 4-bit QLoRA 训练 -> 验证集评估 -> badcase 分析 -> Gradio Demo。OCR/RAG 保留为后续处理长报表 PDF 的扩展，不作为第一阶段核心。

**技术栈：** Python 3.10/3.11、AutoDL RTX 4090、Qwen2.5-VL-7B-Instruct、ChartQA、HuggingFace Datasets、Transformers、PEFT、TRL、bitsandbytes、Gradio、pandas、pytest，可选 TensorBoard 或 Weights & Biases。

## 全局约束

- 项目定位：AI 应用工程候选人的多模态图表/报表理解、VLM 微调、评估和后续偏好优化项目。
- 短期目标：云端 GPU 可用后，用 2-3 天做出可运行、可解释、可展示的训练和推理 MVP。
- 主项目：面向企业图表、报表、数据看板和业务文档截图的多模态 VQA 系统。
- MVP 优先级：云端训练 smoke run > zero-shot baseline > LoRA 微调 > 评估 > badcase 分析 > Gradio Demo > reward reranking / DPO / GRPO-style 探索。
- 简历表达：必须写成基于公开 notebook 和公开数据集的二次实现、改造和评估，不伪装成完全原创。
- 避免方向：不要把项目做成纯后端 CRUD，也不要只停留在 notebook 复现。
- Demo 要求：支持图片上传或样例选择、自然语言问题、base-vs-LoRA 模型选择、生成答案、可选参考答案展示。
- 评估要求：包含 exact match、token F1、numeric accuracy、人工准确率、错误分类、zero-shot vs LoRA 对比。
- 云端约束：训练在国内云平台完成，优先 AutoDL 单卡 RTX 4090 24GB，使用 SSH、JupyterLab 和 `tmux`。

---

## 推荐仓库结构

- `README.md`：项目概览、快速开始、云端训练指南、架构图、Demo 截图、评估摘要、简历 bullet。
- `requirements.txt`：MVP 所需依赖。
- `configs/qwen25vl_chartqa.yaml`：模型、数据集、LoRA、量化、训练和评估配置。
- `data/samples/`：少量公开图表/报表样例；如果许可不适合提交，则只保留下载说明。
- `data/eval/chartqa_eval_sample.csv`：导出的评估样例，包含问题、答案、图片 id 和问题类型。
- `src/chartvqa/config.py`：配置加载。
- `src/chartvqa/data.py`：加载 ChartQA，并规范化图像-问题-答案样本。
- `src/chartvqa/prompting.py`：将样本转换为 Qwen2.5-VL chat 格式。
- `src/chartvqa/modeling.py`：加载基础模型、processor、量化配置和 LoRA adapter。
- `src/chartvqa/training.py`：训练流程封装。
- `src/chartvqa/evaluation.py`：计算 EM、token F1、numeric accuracy 和错误字段。
- `src/chartvqa/inference.py`：对单张图片和问题执行 base 或 LoRA 推理。
- `app.py`：Gradio Demo。
- `scripts/cloud_setup_autodl.sh`：AutoDL 环境准备脚本和检查命令。
- `scripts/train_lora.py`：启动 QLoRA 微调。
- `scripts/run_eval.py`：执行 zero-shot 和 LoRA 评估，并导出报告。
- `reports/eval_results.csv`：评估结果。
- `reports/badcase_analysis.md`：人工 badcase 分析。
- `reports/experiments.md`：LoRA rank、学习率、数据比例等实验记录。
- `tests/`：prompt 格式、指标归一化、数值匹配和配置加载测试。

## 里程碑 0：项目决策与云端准备，半天

**交付物：** 确认 Qwen2.5-VL + ChartQA LoRA 路线，并准备 AutoDL 训练环境。

已确认选择：

- 数据方向：先做 ChartQA，后续扩展 DocVQA 或业务报表截图。
- MVP 解析方式：VLM-first，不以 OCR-first 为第一阶段主线。
- 基础模型：`Qwen/Qwen2.5-VL-7B-Instruct`。
- 微调方式：4-bit QLoRA + PEFT。
- 云平台：AutoDL 国内 GPU 实例，单卡 RTX 4090 24GB。
- Demo 框架：Gradio。
- 评估规模：先用 100-300 条 held-out 样本做自动指标，再人工检查 20-30 条。

决策标准：

- baseline 必须能在单卡 4090 上跑通 smoke training。
- 数据集必须包含图片-问题-答案三元组。
- 第一轮训练必须小规模、可复现，再逐步扩大。
- 项目必须能包装成真实的企业图表/报表问答场景。

检查清单：

- [ ] 在 `README.md` 记录参考 notebook、数据集、模型和场景选择。
- [ ] 创建 AutoDL RTX 4090 24GB 实例，启用 PyTorch 镜像、JupyterLab 和 SSH。
- [ ] 在云端配置 HuggingFace 和 Kaggle token，不提交任何密钥。
- [ ] 运行最小 CUDA 检查命令，确认 `torch` 可以识别 GPU 和显存。
- [ ] 创建 `tmux` 会话，验证 SSH 断开后任务仍可继续运行。

## 里程碑 1：训练 MVP，第 1 天

**交付物：** 云端命令可以跑通一次 Qwen2.5-VL + ChartQA QLoRA smoke training。

### 任务 1：项目脚手架

**文件：**

- 创建：`requirements.txt`
- 创建：`configs/qwen25vl_chartqa.yaml`
- 创建：`src/chartvqa/config.py`
- 创建：`tests/test_config.py`
- 创建：`scripts/cloud_setup_autodl.sh`

**接口：**

- 产出：`load_config(path: str = "configs/qwen25vl_chartqa.yaml") -> dict`

步骤：

- [ ] 添加最小依赖：`torch`、`transformers`、`datasets`、`accelerate`、`peft`、`trl`、`bitsandbytes`、`qwen-vl-utils`、`gradio`、`pydantic`、`pyyaml`、`pillow`、`pandas`、`numpy`、`pytest`、`evaluate`、`scikit-learn`。
- [ ] 在 `configs/qwen25vl_chartqa.yaml` 中写入模型 id、数据集 id、数据切片、LoRA rank、LoRA alpha、学习率、batch size、梯度累积、最大序列长度、输出目录和评估设置。
- [ ] 在 `scripts/cloud_setup_autodl.sh` 中加入环境检查、依赖安装、CUDA 检查和缓存目录设置。
- [ ] 编写配置测试，确认 YAML 中包含必要字段。
- [ ] 实现 `load_config`。
- [ ] 运行 `pytest tests/test_config.py -v`。
- [ ] 提交：`chore: bootstrap chartvqa cloud project`。

### 任务 2：ChartQA 数据格式化

**文件：**

- 创建：`src/chartvqa/data.py`
- 创建：`src/chartvqa/prompting.py`
- 创建：`tests/test_prompting.py`

**接口：**

- 产出：`load_chartqa_splits(config: dict) -> tuple`
- 产出：`format_chat_sample(sample: dict, system_message: str) -> list[dict]`
- 产出：`ChartQASample(image, question: str, answer: str, question_type: str | None)`

步骤：

- [ ] 使用可配置切片加载 `HuggingFaceM4/ChartQA`，例如 `train[:1%]`、`val[:1%]`、`test[:1%]`。
- [ ] 将每条样本规范化为 image、query、answer 字段。
- [ ] 将样本转换为 Qwen2.5-VL chat messages，包含 system、user image/question 和 assistant answer。
- [ ] 测试格式化结果中包含一个 image 项和一个 text question 项。
- [ ] 运行 `pytest tests/test_prompting.py -v`。
- [ ] 提交：`feat: format chartqa for qwen vl`。

### 任务 3：模型与 LoRA 加载

**文件：**

- 创建：`src/chartvqa/modeling.py`
- 创建：`tests/test_lora_config.py`

**接口：**

- 产出：`build_bnb_config(config: dict)`
- 产出：`build_lora_config(config: dict)`
- 产出：`load_model_and_processor(config: dict, train: bool = False)`

步骤：

- [ ] 实现 4-bit BitsAndBytes 配置：NF4、double quantization、可用时使用 bf16 compute。
- [ ] 实现第一组 LoRA 配置：`r=8`、`lora_alpha=16`、`lora_dropout=0.1`，target modules 为 `q_proj` 和 `v_proj`。
- [ ] 训练模式下关闭 cache，并启用 gradient checkpointing。
- [ ] 编写测试，只检查配置构造，不加载完整模型。
- [ ] 提交：`feat: add qwen vl lora loading`。

### 任务 4：Smoke Training 脚本

**文件：**

- 创建：`src/chartvqa/training.py`
- 创建：`scripts/train_lora.py`

**接口：**

- 产出：`build_trainer(config: dict)`
- 产出命令：`python scripts/train_lora.py --config configs/qwen25vl_chartqa.yaml --max-steps 1`

步骤：

- [ ] 将 Kaggle 参考 notebook 中的训练逻辑整理为脚本。
- [ ] 实现 collator，应用 Qwen2.5-VL chat template，并正确 mask padding labels。
- [ ] 先运行 `--max-steps 1`。
- [ ] 将 adapter 保存到 `outputs/qwen25vl-chartqa-smoke`。
- [ ] 在 `reports/experiments.md` 记录显存占用和运行时间。
- [ ] 提交：`feat: add qwen chartqa smoke training`。

## 里程碑 2：评估与 Demo，第 2 天

**交付物：** 在 held-out 样本上对比 base model 和 LoRA adapter，并用 Gradio 展示效果。

### 任务 5：评估指标

**文件：**

- 创建：`src/chartvqa/evaluation.py`
- 创建：`scripts/run_eval.py`
- 创建：`tests/test_evaluation.py`

**接口：**

- 产出：`exact_match(prediction: str, answer: str) -> float`
- 产出：`token_f1(prediction: str, answer: str) -> float`
- 产出：`numeric_match(prediction: str, answer: str) -> float`
- 产出命令：`python scripts/run_eval.py --adapter outputs/qwen25vl-chartqa-smoke`

步骤：

- [ ] 测试 exact match，处理大小写和空白字符归一化。
- [ ] 测试 token F1，支持部分匹配。
- [ ] 测试 numeric matching，处理逗号、百分号和简单小数。
- [ ] 实现 base model 在小规模 held-out 样本上的评估。
- [ ] 实现 LoRA adapter 在相同样本上的评估。
- [ ] 导出 `reports/eval_results.csv`。
- [ ] 提交：`feat: evaluate chartqa answers`。

### 任务 6：Gradio Demo

**文件：**

- 创建：`src/chartvqa/inference.py`
- 创建：`app.py`

**接口：**

- 产出：`answer_chart(image, question: str, adapter_path: str | None, config: dict) -> str`

步骤：

- [ ] 构建 Gradio UI，支持图表/报表图片上传和问题输入。
- [ ] 添加模式选择：base model 或 LoRA adapter。
- [ ] 展示模型答案，并在样例模式下展示参考答案。
- [ ] 至少用 5 条 ChartQA 样例测试。
- [ ] 将 Demo 截图保存到 `reports/screenshots/`。
- [ ] 提交：`feat: add chartvqa gradio demo`。

### 任务 7：初版 README

**文件：**

- 创建或修改：`README.md`

步骤：

- [ ] 写明项目定位：基于公开 notebook 和 Qwen2.5-VL LoRA 的二次实现。
- [ ] 写明架构：图表/报表图片 -> VLM prompt -> base inference -> LoRA training -> evaluation -> demo。
- [ ] 添加 AutoDL 快速开始命令。
- [ ] 添加样例输入输出截图。
- [ ] 添加当前限制。
- [ ] 添加克制、真实的简历 bullet。
- [ ] 提交：`docs: add initial project readme`。

### 任务 8：成功与失败案例记录

**文件：**

- 创建：`reports/case_studies.md`

步骤：

- [ ] 记录 5 个成功的图表/报表问答案例。
- [ ] 记录 5 个失败的图表/报表问答案例。
- [ ] 每个失败案例标注一个主要原因：图表类型理解错误、坐标轴或图例读取错误、数值尺度错误、多步比较错误、答案格式错误、编造数值。
- [ ] 对关键案例附截图或复制输出。
- [ ] 提交：`docs: add qa case studies`。

## 里程碑 3：LoRA 实验，第 3 天到第 7 天

**交付物：** 一张可用于面试讲解的 LoRA 实验对比表。

### 任务 9：受控 LoRA 对比实验

**文件：**

- 修改：`configs/qwen25vl_chartqa.yaml`
- 修改：`scripts/train_lora.py`
- 修改：`reports/experiments.md`

实验网格：

- 数据比例：`1%`、`3%`，可选 `5%`
- LoRA rank：`8`、`16`
- 学习率：`2e-5`，可选 `1e-4`
- 训练轮数：`1`

步骤：

- [ ] 先运行 smoke 配置。
- [ ] 至少运行两组正式 LoRA 配置。
- [ ] 记录数据量、可训练参数量、显存、训练时间、eval loss、EM、token F1 和 numeric accuracy。
- [ ] 将不同 adapter 保存到独立输出目录。
- [ ] 在 `reports/experiments.md` 中整理对比表。
- [ ] 提交：`exp: compare chartqa lora settings`。

### 任务 10：Badcase 分析

**文件：**

- 创建：`reports/badcase_analysis.md`
- 修改：`README.md`

步骤：

- [ ] 将失败案例分为：图表类型理解错误、坐标轴或图例读取错误、数值尺度错误、多步比较错误、答案格式错误、编造数值。
- [ ] 每个已观察到的类别提供一个代表案例。
- [ ] 为最主要的 2 类错误提出后续优化方案。
- [ ] 在 README 中总结 badcase 分布。
- [ ] 提交：`docs: add chartqa badcase analysis`。

## 里程碑 4：场景扩展，第 7 天到第 14 天

**交付物：** 让项目更像企业报表助手，而不是只停留在 benchmark notebook。

### 任务 11：报表截图样例

**文件：**

- 创建：`data/samples/README.md`
- 修改：`app.py`
- 修改：`reports/case_studies.md`

步骤：

- [ ] 加入 5-10 张公开或自制的业务图表/报表截图，并写明许可来源。
- [ ] 为每张样例编写自然语言问题。
- [ ] 对这些样例分别运行 base 和 LoRA 推理。
- [ ] 记录 ChartQA 微调在哪些场景有帮助，在哪些场景泛化不足。
- [ ] 提交：`data: add report screenshot samples`。

### 任务 12：可选 OCR/RAG 扩展

**文件：**

- 创建：`src/chartvqa/rag.py`
- 创建：`reports/rag_extension.md`

步骤：

- [ ] 只有在 VLM 微调主线稳定后再做此扩展。
- [ ] 对长报表 PDF 使用 OCR 或 PDF 文本抽取。
- [ ] 检索相关报表文本片段作为辅助上下文。
- [ ] 对少量样例比较 VLM-only 与 VLM + retrieved context 的效果。
- [ ] 提交：`exp: explore report rag extension`。

## 里程碑 5：偏好优化，第 3 周以后

**交付物：** 先做 reward reranking 和 DPO 数据构造，不提前承诺 GRPO。

范围：

- 对同一个图表问题生成多个候选答案。
- 使用答案匹配、数值一致性、格式合规性和幻觉惩罚打分。
- 构造 chosen/rejected 偏好样本。
- 只有在偏好数据质量确认后，再训练或模拟 DPO-style 优化。
- GRPO-style 优化作为长期探索。

文件：

- `src/chartvqa/reranking.py`
- `tests/test_reranking.py`
- `data/preference/chartqa_preferences.jsonl`
- `reports/reward_reranking.md`

简历安全表达：

- “设计规则奖励函数，对多候选回答进行 reward reranking，结合答案匹配、数值一致性和格式合规性降低无依据图表回答。”

避免表达：

- “使用 GRPO 显著提升模型推理能力。”

## 执行时间表

### GPU 准备后 2-3 天可展示版

- 第 1 天上午：AutoDL 环境准备、仓库克隆、token 配置、CUDA 和依赖检查。
- 第 1 天下午：将 Kaggle notebook 转为脚本，并跑通 one-step smoke training。
- 第 2 天上午：运行 base model 评估和 LoRA smoke adapter 评估。
- 第 2 天下午：构建 Gradio Demo 和 README 截图。
- 第 3 天：至少运行一组正式 LoRA 配置，整理评估表和案例分析。

### 7-14 天增强版

- 第 4-5 天：对比 LoRA rank 和数据比例。
- 第 6-7 天：整理 badcase 分析并打磨 Demo。
- 第 8-10 天：加入报表截图泛化样例。
- 第 11-14 天：实现 reward reranking 原型、补充架构文档、面试讲解稿和简历版本。

## 完成标准

MVP 完成标准：

- AutoDL 环境配置文档可复现。
- Qwen2.5-VL + ChartQA QLoRA one-step training 成功。
- 至少一组正式 LoRA 训练完成。
- `reports/eval_results.csv` 中有 base vs LoRA 评估结果。
- Gradio Demo 可以回答样例图表/报表问题。
- `reports/case_studies.md` 至少包含 5 个成功案例和 5 个失败案例。
- README 包含项目场景、训练路线、评估结果、截图、限制和克制的简历 bullet。

增强版完成标准：

- 至少比较 3 组 LoRA 配置。
- 加入报表截图迁移案例。
- Badcase 分析解释数值和图表结构类错误。
- 完成 reward reranking 或偏好数据构造原型。
- 面试笔记覆盖 3 分钟、8 分钟和 20 分钟项目讲解。

## 自检

- 覆盖范围：计划覆盖当前真实需求场景、VLM 微调、AutoDL 云端训练、评估、badcase 和后续 DPO/GRPO-style 探索。
- 范围控制：OCR/RAG 已降级为可选扩展，第一阶段聚焦 Qwen2.5-VL + ChartQA LoRA。
- 简历安全：明确采用公开 notebook 和公开数据集二次实现，不夸大 GRPO。
- 风险控制：项目重点放在 VLM 适配、可量化评估和实际场景包装，不滑向纯后端。
