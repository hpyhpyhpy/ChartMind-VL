# ChartMind-VL 项目声明

## 项目定位

ChartMind-VL 是一个面向企业图表、报表和业务看板截图的多模态问答与轻量微调项目。

项目主线是基于 `Qwen/Qwen2.5-VL-7B-Instruct` 和公开 `ChartQA` 数据集，完成从数据格式转换、4-bit QLoRA 微调、zero-shot 与 LoRA adapter 对比评估、badcase 分析到 Gradio Demo 展示的闭环。

## 启动指令

每次新对话开始时，请先读取 [_ai_rules.md](_ai_rules.md) 并严格遵守其中的规则。

## 当前主线

- 任务场景：企业图表、报表、数据看板截图问答。
- 基础模型：`Qwen/Qwen2.5-VL-7B-Instruct`。
- 数据集：`HuggingFaceM4/ChartQA`。
- 微调方法：4-bit QLoRA。
- 云端算力：国内平台，优先 AutoDL 单卡 RTX 4090 24GB。
- 第一阶段目标：跑通训练 smoke test、完成 base vs LoRA 评估、产出 Demo 和可写入简历的实验记录。

## 工作原则

- 先完成可运行、可评估、可展示的最小闭环，再做扩展。
- 不把项目包装成纯 OCR、纯后端或单纯 notebook 复现。
- LoRA 是第一阶段重点，reward reranking / DPO / GRPO-style 优化作为后续增强。
- 说明类文档、计划、实验记录、README、注释和面向用户的解释默认使用中文。
