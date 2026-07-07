# ChartMind-VL 云端训练设计说明

## 目标

本项目要构建一个可写入简历、可演示、可解释的多模态 AI 应用项目，核心场景是 **企业图表、报表和业务看板截图问答**。

主技术路线是使用 **Qwen2.5-VL + ChartQA + LoRA/QLoRA**，并在 **AutoDL 单卡 RTX 4090** 云端环境中完成训练和评估。

项目需要证明候选人具备现代 VLM 微调项目的完整工程能力：数据格式转换、LoRA 训练、评估指标设计、badcase 分析、Demo 包装，以及后续扩展到 reward reranking / DPO / GRPO-style 优化的能力。

## 项目定位

项目不再狭义定位为票据问答或发票 OCR，而是定位为：

**面向企业图表、报表和业务文档截图的多模态问答系统。**

这个方向更贴近当前实际需求。很多企业 AI 产品都需要读取 BI 看板、财务报表、运营图表、市场分析图和业务截图，并用自然语言回答问题。它仍然属于文档智能和多模态应用方向，但比传统 OCR 字段抽取更贴近当前 VLM 落地场景。

## 主技术路线

第一阶段推荐路线：

- 基础模型：`Qwen/Qwen2.5-VL-7B-Instruct`
- 数据集：`HuggingFaceM4/ChartQA`
- 微调方法：4-bit QLoRA + PEFT
- 训练库：`transformers`、`peft`、`trl`、`bitsandbytes`
- 算力环境：AutoDL 单卡 RTX 4090 24GB
- Demo：使用 Gradio 加载 base model 或 LoRA adapter 进行推理
- 评估：对比 zero-shot baseline 与 LoRA adapter 在 ChartQA 验证集上的表现

已拉取的 Kaggle 参考 notebook：

- `research/kaggle_candidates/qwen25vl-chartqa/finetuning-qwen2-5vl-on-chartqa.ipynb`

## 为什么选择这条路线

相比 DocVQA + LLaVA：

- Qwen2.5-VL 更新，更贴近当前多模态应用和微调岗位的技术栈。
- 参考 notebook 已经包含 LoRA、TRL、bitsandbytes 和小规模 ChartQA 训练流程。
- ChartQA 可以自然包装成企业图表、报表和数据看板问答场景。
- 后续仍然可以加入 DocVQA 或业务报表截图样例，证明任务不局限于图表 benchmark。

相比 SROIE + LayoutLM：

- 项目叙事更偏现代 VLM 适配，而不是经典 OCR 或 token classification。
- 输出是自然语言问答，更容易做 Demo 和面试讲解。
- LoRA、badcase 分析、reward reranking 和 DPO 数据构造都更自然。

## 云端工作流

采用 **本地管理代码 + 云端训练评估** 的工作流。

本地机器负责：

- 维护 Git 仓库。
- 将 Kaggle 参考 notebook 整理成可复用脚本。
- 编写配置、评估脚本、README、实验记录和 badcase 文档。
- 在代码稳定后推送到 GitHub。

AutoDL 4090 实例负责：

- 克隆 GitHub 仓库。
- 配置 HuggingFace 和 Kaggle 凭据。
- 下载模型和数据集。
- 先跑 smoke training。
- 再跑小规模 LoRA 实验。
- 保存 LoRA adapter、训练日志、评估结果和 Demo 截图。

推荐云端工具：

- SSH：远程命令行操作。
- JupyterLab：查看数据和快速调试 notebook。
- `tmux`：保护长时间训练任务，避免 SSH 断开后训练中止。
- TensorBoard 或 Weights & Biases：记录实验曲线。
- HuggingFace 镜像或缓存目录：缓解国内模型下载不稳定问题。

## 第一阶段训练范围

第一阶段必须保持小而稳：

- 使用 ChartQA 的 1% 到 5% 数据做初始实验。
- 先训练 1 个 epoch。
- `batch_size` 先设为 1。
- 使用梯度累积。
- 使用 4-bit 量化。
- 第一组 LoRA 参数使用 `r=8`。

只有在 smoke training 成功后，才扩大实验范围：

- 增加训练样本比例。
- 对比 LoRA rank：`r=8`、`r=16`，必要时再尝试 `r=32`。
- 对比学习率。
- 对比 prompt 格式。
- 系统整理评估结果和 badcase。

## 评估设计

第一轮评估对比：

- Qwen2.5-VL base model zero-shot。
- Qwen2.5-VL + LoRA adapter。

评估指标：

- Exact Match：适合短答案。
- Token F1：适合部分匹配。
- Numeric Accuracy：判断图表数值回答是否正确。
- 人工准确率：抽样检查模型回答是否真的可接受。
- Badcase 分类：分析错误来源，而不是只给一个总分。

推荐 badcase 分类：

- 图表类型理解错误。
- 坐标轴或图例读取错误。
- 数值尺度错误。
- 多步比较错误。
- 输出格式不符合答案要求。
- 编造不存在的数值或结论。

## Demo 范围

第一版 Demo 使用 Gradio 即可，不需要复杂后端。

Demo 需要支持：

- 上传或选择图表/报表图片。
- 输入自然语言问题。
- 展示模型回答。
- 对样例数据展示参考答案。
- 切换 base model 和 LoRA adapter。
- 保存可用于 README 和面试展示的输出截图。

## 后续扩展

当 Qwen2.5-VL + ChartQA LoRA baseline 稳定后，再做增强：

1. 加入少量 DocVQA 或业务报表截图样例，证明项目不局限于 ChartQA。
2. 从模型输出和人工判断中构造偏好数据。
3. 实现基于规则奖励的多候选答案 reranking。
4. 将 chosen/rejected 样本整理成 DPO 数据。
5. 将 GRPO-style 优化作为长期探索，不作为第一阶段承诺。

## 简历项目名

推荐英文名：

**ChartMind-VL**

推荐中文名：

**面向企业图表与报表的多模态问答微调系统**

## 简历描述

基于 Qwen2.5-VL 与公开 ChartQA 数据集二次实现面向企业图表、报表和业务看板的多模态问答系统，完成数据格式转换、4-bit QLoRA 微调、zero-shot 与 LoRA adapter 对比评估、数值问答 badcase 分析和 Gradio Demo 展示，并探索基于多候选答案的 reward reranking 与 DPO 数据构造。

## 明确不做的事

- 在真正实现和评估前，不声称已经完成 GRPO 训练。
- 第一周不投入复杂后端开发。
- 不把项目只包装成票据 OCR。
- smoke training 和评估脚本跑通前，不扩大训练数据规模。
- 不只依赖主观 Demo 案例，必须保留可量化评估结果。

## 已确认决策

用户已在 2026-07-07 确认以下方向：

- 使用国内云平台，优先 AutoDL。
- 任务不必限定为票据问答。
- 项目应优先贴近当前实际需求和 VLM 微调价值。
- 接受 Qwen2.5-VL + ChartQA LoRA + AutoDL 作为主路线。
