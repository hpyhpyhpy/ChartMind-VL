# VLM ChartQA Cloud Training Design

## Goal

Build a resume-ready multimodal AI application project around **enterprise report, chart, and dashboard question answering**, using **Qwen2.5-VL + ChartQA + LoRA/QLoRA** as the main training direction and **AutoDL 4090 cloud GPU** as the training environment.

The project should demonstrate that the candidate can handle a modern VLM fine-tuning workflow end to end: data formatting, LoRA training, evaluation, badcase analysis, demo packaging, and a credible path toward reward reranking / DPO / GRPO-style optimization.

## Positioning

The project is no longer narrowly framed as receipt or invoice question answering. The revised scenario is:

**A multimodal question answering system for enterprise charts, reports, and business document screenshots.**

This scenario is more current because many teams are building AI products that read BI dashboards, financial reports, operating reports, market research charts, and business screenshots. It still belongs to the broader document intelligence / multimodal application space, but it sounds less like a classic OCR task and more like a current VLM application.

## Main Technical Route

Recommended first route:

- Base model: `Qwen/Qwen2.5-VL-7B-Instruct`
- Dataset: `HuggingFaceM4/ChartQA`
- Fine-tuning method: 4-bit QLoRA with PEFT
- Training library: `transformers`, `peft`, `trl`, `bitsandbytes`
- Hardware: one rented RTX 4090 24GB on AutoDL
- Demo: Gradio inference demo using base model and LoRA adapter
- Evaluation: zero-shot baseline vs LoRA adapter on held-out ChartQA samples

The Kaggle notebook already pulled locally is the initial reference:

- `research/kaggle_candidates/qwen25vl-chartqa/finetuning-qwen2-5vl-on-chartqa.ipynb`

## Why This Route

Compared with DocVQA/LLaVA:

- Qwen2.5-VL is newer and more aligned with current VLM application work.
- The notebook already contains LoRA, TRL, bitsandbytes, and a small ChartQA training loop.
- ChartQA maps cleanly to real business scenarios: charts, dashboards, and report figures.
- The project can still be extended to DocVQA or report screenshots later.

Compared with SROIE/LayoutLM:

- The story is less classic OCR and more modern multimodal model adaptation.
- The output is natural-language question answering rather than only token-level field extraction.
- LoRA, badcase analysis, and later preference optimization fit more naturally.

## Cloud Workflow

The workflow should be **local project management + cloud training**.

Local machine:

- Maintain the codebase.
- Convert reference notebook into scripts.
- Write configs, evaluation scripts, README, and experiment notes.
- Push code to GitHub once the repo is initialized.

AutoDL 4090 instance:

- Clone the GitHub repo.
- Configure HuggingFace and Kaggle credentials.
- Download model and dataset.
- Run smoke training first.
- Run full small-scale LoRA experiments.
- Save LoRA adapter, logs, evaluation outputs, and demo screenshots.

Recommended cloud tools:

- SSH for remote command line.
- JupyterLab for visual data inspection and quick notebook debugging.
- `tmux` for long-running training sessions.
- TensorBoard or Weights & Biases for experiment tracking.
- HuggingFace mirror/cache settings where needed.

## Training Scope

Phase 1 should be deliberately small:

- Use 1 percent to 5 percent of ChartQA for initial experiments.
- Train for 1 epoch first.
- Keep batch size at 1.
- Use gradient accumulation.
- Use 4-bit quantization.
- Use LoRA rank `8` as the first baseline.

Only after the first training run succeeds should the project expand to:

- More samples.
- Rank comparison: `r=8`, `r=16`, possibly `r=32`.
- Learning rate comparison.
- Prompt format comparison.
- Evaluation and badcase analysis.

## Evaluation

The first evaluation should compare:

- Base Qwen2.5-VL zero-shot.
- Qwen2.5-VL with LoRA adapter.

Metrics:

- Exact match for short answers.
- Token-level F1 for partial matches.
- Numeric accuracy for chart values.
- Manual correctness for a small sampled subset.
- Badcase categories.

Badcase categories:

- Chart type misunderstanding.
- Wrong axis or legend reading.
- Numeric scale error.
- Multi-step comparison error.
- Answer format mismatch.
- Hallucinated value.

## Demo Scope

The first demo should support:

- Upload or select a chart/report image.
- Ask a natural-language question.
- Show the generated answer.
- Show the expected answer for sample cases when available.
- Show whether the model is using base or LoRA adapter.
- Save example outputs for README and interview discussion.

The demo does not need a complex backend. Gradio is enough.

## Later Extensions

After the Qwen2.5-VL + ChartQA LoRA baseline is stable:

1. Add a few DocVQA or report screenshot samples to show the scenario is not limited to charts.
2. Build a small preference dataset from model outputs and human labels.
3. Implement rule-based reward reranking for multiple generated answers.
4. Convert preference pairs into DPO data.
5. Treat GRPO-style optimization as a long-term exploration, not a first-stage promise.

## Resume-Safe Project Name

Recommended name:

**Enterprise Chart and Report VQA Fine-Tuning System**

Chinese name:

**面向企业图表与报表的多模态问答微调系统**

## Resume-Safe Description

基于 Qwen2.5-VL 与公开 ChartQA 数据集二次实现面向企业图表、报表和业务看板的多模态问答系统，完成数据格式转换、4-bit QLoRA 微调、zero-shot 与 LoRA adapter 对比评估、数值问答 badcase 分析和 Gradio Demo 展示，并探索基于多候选答案的 reward reranking 与 DPO 数据构造。

## Explicit Non-Goals

- Do not claim full GRPO training before it is actually implemented and evaluated.
- Do not spend the first week building a complex backend.
- Do not frame the project as only receipt OCR.
- Do not train on large data before the smoke run and evaluation script are working.
- Do not rely only on subjective demo examples; keep measurable evaluation output.

## Approval Status

The user approved the revised direction on 2026-07-07:

- Domestic cloud platform preferred.
- Project task does not have to be receipt QA.
- Current practical demand and VLM fine-tuning value are more important.
- Qwen2.5-VL + ChartQA LoRA on AutoDL is accepted as the main route.
