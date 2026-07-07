# Enterprise Chart and Report VQA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a resume-ready multimodal question answering and fine-tuning project for enterprise charts, reports, and business document screenshots, using Qwen2.5-VL + ChartQA + LoRA/QLoRA as the main route and AutoDL 4090 as the training environment.

**Architecture:** Start with a modern VLM fine-tuning pipeline: chart/report image + question -> Qwen2.5-VL prompt formatting -> zero-shot baseline -> 4-bit QLoRA training -> held-out evaluation -> badcase analysis -> Gradio demo. Keep OCR/RAG as a later extension for report PDFs and long business documents, not the first-stage core.

**Tech Stack:** Python 3.10/3.11, AutoDL RTX 4090, Qwen2.5-VL-7B-Instruct, ChartQA, HuggingFace Datasets, Transformers, PEFT, TRL, bitsandbytes, Gradio, pandas, pytest, optional TensorBoard or Weights & Biases.

## Global Constraints

- Positioning: AI application engineering, focused on multimodal report/chart understanding, VLM fine-tuning, evaluation, and later preference optimization.
- Short-term target: produce a runnable, explainable, resume-ready training and inference MVP in 2-3 days after cloud GPU is available.
- Main project: multimodal VQA system for enterprise charts, reports, dashboards, and business document screenshots.
- MVP priority: cloud training smoke run > zero-shot baseline > LoRA fine-tuning > evaluation > badcase analysis > Gradio demo > reward reranking / DPO / GRPO-like exploration.
- Resume wording: describe the work as open-source reproduction plus secondary implementation and evaluation, not as a fully original system.
- Avoid: turning the project into a pure backend CRUD system.
- Demo requirement: support image upload or sample selection, natural language question, base-vs-LoRA model choice, generated answer, and sample answer comparison where labels exist.
- Evaluation requirement: include exact match, token F1, numeric accuracy, manual accuracy, hallucination/error categories, and zero-shot vs LoRA comparison.
- Cloud constraint: training runs on a domestic GPU platform, preferably AutoDL with one RTX 4090 24GB, using SSH/JupyterLab/tmux.

---

## Recommended Repository Structure

- `README.md`: project overview, quickstart, cloud training guide, architecture diagram, demo screenshots, evaluation summary, resume bullets.
- `requirements.txt`: minimal runtime dependencies for MVP.
- `configs/qwen25vl_chartqa.yaml`: model, dataset, LoRA, quantization, training, and evaluation settings.
- `data/samples/`: small public sample chart/report images committed only if licensing allows; otherwise keep download instructions.
- `data/eval/chartqa_eval_sample.csv`: small exported evaluation slice with question, answer, image id, and question type.
- `src/chartvqa/config.py`: typed configuration loader.
- `src/chartvqa/data.py`: load ChartQA and format image-question-answer samples.
- `src/chartvqa/prompting.py`: convert samples into Qwen2.5-VL chat format.
- `src/chartvqa/modeling.py`: load base model, processor, quantization, and LoRA adapter.
- `src/chartvqa/training.py`: reusable training entry points.
- `src/chartvqa/evaluation.py`: compute EM, token F1, numeric accuracy, and error fields.
- `src/chartvqa/inference.py`: run base or LoRA inference on one image/question pair.
- `app.py`: Gradio demo.
- `scripts/cloud_setup_autodl.sh`: AutoDL environment setup notes as executable shell steps.
- `scripts/train_lora.py`: run QLoRA fine-tuning.
- `scripts/run_eval.py`: run zero-shot and LoRA evaluation and export reports.
- `reports/eval_results.csv`: generated evaluation output.
- `reports/badcase_analysis.md`: manual badcase summary.
- `reports/experiments.md`: experiment table for LoRA ranks, learning rates, and data fractions.
- `tests/`: unit tests for prompt formatting, metric normalization, numeric matching, and config loading.

## Milestone 0: Project Decision and Cloud Setup, Half Day

**Deliverable:** confirm the Qwen2.5-VL + ChartQA LoRA route and prepare AutoDL for training.

Approved choice:

- Dataset direction: ChartQA first, DocVQA/report screenshots later.
- MVP parser: VLM-first, not OCR-first.
- Base model: `Qwen/Qwen2.5-VL-7B-Instruct`.
- Fine-tuning: 4-bit QLoRA with PEFT.
- Cloud platform: AutoDL domestic GPU instance, one RTX 4090 24GB.
- Demo framework: Gradio.
- Evaluation size: first 100-300 held-out examples for automated metrics, plus 20-30 manually inspected examples.

Decision criteria:

- The baseline must run a smoke training job on one 4090.
- The dataset must contain image-question-answer triples.
- The first training run must be small and reproducible before scaling.
- The project must be easy to package as a current business scenario.

Checkpoint:

- [ ] Record selected Kaggle reference notebook, dataset, model, and scenario in `README.md`.
- [ ] Create AutoDL instance with RTX 4090 24GB, PyTorch image, JupyterLab, and SSH.
- [ ] Configure HuggingFace and Kaggle tokens on the cloud instance without committing secrets.
- [ ] Run a minimal command that imports `torch`, checks CUDA, and prints GPU memory.
- [ ] Start a `tmux` session and verify a dummy long-running process survives SSH disconnect.

## Milestone 1: Training MVP, Day 1

**Deliverable:** cloud command can run one Qwen2.5-VL + ChartQA QLoRA smoke training job.

### Task 1: Bootstrap Project

**Files:**
- Create: `requirements.txt`
- Create: `configs/qwen25vl_chartqa.yaml`
- Create: `src/chartvqa/config.py`
- Create: `tests/test_config.py`
- Create: `scripts/cloud_setup_autodl.sh`

**Interfaces:**
- Produces: `load_config(path: str = "configs/qwen25vl_chartqa.yaml") -> dict`
- Consumes: none

Steps:

- [ ] Create minimal dependencies: `torch`, `transformers`, `datasets`, `accelerate`, `peft`, `trl`, `bitsandbytes`, `qwen-vl-utils`, `gradio`, `pydantic`, `pyyaml`, `pillow`, `pandas`, `numpy`, `pytest`, `evaluate`, `scikit-learn`.
- [ ] Add `configs/qwen25vl_chartqa.yaml` with model id, dataset id, data split fractions, LoRA rank, LoRA alpha, learning rate, batch size, gradient accumulation, max sequence length, output dir, and eval settings.
- [ ] Add `scripts/cloud_setup_autodl.sh` with environment checks, package installation, CUDA check, and cache directory setup.
- [ ] Write a config test that loads the YAML and asserts required keys exist.
- [ ] Implement `load_config`.
- [ ] Run `pytest tests/test_config.py -v`.
- [ ] Commit with message `chore: bootstrap chartvqa cloud project`.

### Task 2: ChartQA Data Formatting

**Files:**
- Create: `src/chartvqa/data.py`
- Create: `src/chartvqa/prompting.py`
- Create: `tests/test_prompting.py`

**Interfaces:**
- Produces: `load_chartqa_splits(config: dict) -> tuple`
- Produces: `format_chat_sample(sample: dict, system_message: str) -> list[dict]`
- Produces: `ChartQASample(image, question: str, answer: str, question_type: str | None)`

Steps:

- [ ] Load `HuggingFaceM4/ChartQA` with configurable split slices such as `train[:1%]`, `val[:1%]`, and `test[:1%]`.
- [ ] Normalize each sample into image, query, and answer fields.
- [ ] Format each sample into Qwen2.5-VL chat messages with system, user image/question, and assistant answer.
- [ ] Test that formatted messages contain one image item and one text question item.
- [ ] Run `pytest tests/test_prompting.py -v`.
- [ ] Commit with message `feat: format chartqa for qwen vl`.

### Task 3: Model and LoRA Loading

**Files:**
- Create: `src/chartvqa/modeling.py`
- Create: `tests/test_lora_config.py`

**Interfaces:**
- Produces: `build_bnb_config(config: dict)`
- Produces: `build_lora_config(config: dict)`
- Produces: `load_model_and_processor(config: dict, train: bool = False)`

Steps:

- [ ] Implement 4-bit BitsAndBytes config: NF4, double quantization, bf16 compute where available.
- [ ] Implement LoRA config with first baseline `r=8`, `lora_alpha=16`, `lora_dropout=0.1`, target modules `q_proj` and `v_proj`.
- [ ] Ensure training mode disables cache and enables gradient checkpointing.
- [ ] Test config construction without loading the full model.
- [ ] Commit with message `feat: add qwen vl lora loading`.

### Task 4: Smoke Training Script

**Files:**
- Create: `src/chartvqa/training.py`
- Create: `scripts/train_lora.py`

**Interfaces:**
- Produces: `build_trainer(config: dict)`
- Produces: CLI command `python scripts/train_lora.py --config configs/qwen25vl_chartqa.yaml --max-steps 1`

Steps:

- [ ] Convert the reference Kaggle notebook training logic into a script.
- [ ] Implement a collator that applies Qwen2.5-VL chat template and masks padding labels.
- [ ] Run one-step training first with `--max-steps 1`.
- [ ] Save adapter output under `outputs/qwen25vl-chartqa-smoke`.
- [ ] Record GPU memory usage and wall-clock time in `reports/experiments.md`.
- [ ] Commit with message `feat: add qwen chartqa smoke training`.

## Milestone 2: Evaluation and Demo, Day 2

**Deliverable:** compare base model and LoRA adapter on held-out examples, then show results in a small Gradio demo.

### Task 5: Evaluation Metrics

**Files:**
- Create: `src/chartvqa/evaluation.py`
- Create: `scripts/run_eval.py`
- Create: `tests/test_evaluation.py`

**Interfaces:**
- Produces: `exact_match(prediction: str, answer: str) -> float`
- Produces: `token_f1(prediction: str, answer: str) -> float`
- Produces: `numeric_match(prediction: str, answer: str) -> float`
- Produces: CLI command `python scripts/run_eval.py --adapter outputs/qwen25vl-chartqa-smoke`

Steps:

- [ ] Test exact match with normalized case and whitespace.
- [ ] Test token F1 for partial answers.
- [ ] Test numeric matching with commas, percent signs, and simple decimals.
- [ ] Implement base model evaluation on a small held-out slice.
- [ ] Implement LoRA adapter evaluation on the same slice.
- [ ] Export `reports/eval_results.csv`.
- [ ] Commit with message `feat: evaluate chartqa answers`.

### Task 6: Gradio Demo

**Files:**
- Create: `src/chartvqa/inference.py`
- Create: `app.py`

**Interfaces:**
- Produces: `answer_chart(image, question: str, adapter_path: str | None, config: dict) -> str`

Steps:

- [ ] Build a Gradio UI with chart/report image upload and question input.
- [ ] Add a mode selector: base model or LoRA adapter.
- [ ] Display generated answer and optional reference answer for sample cases.
- [ ] Test with at least 5 ChartQA examples.
- [ ] Save demo screenshots under `reports/screenshots/`.
- [ ] Commit with message `feat: add chartvqa gradio demo`.

### Task 7: Initial README

**Files:**
- Create or modify: `README.md`

Steps:

- [ ] Add project positioning: open-source reproduction plus Qwen2.5-VL LoRA secondary implementation.
- [ ] Add architecture: chart/report image -> VLM prompt -> base inference -> LoRA training -> evaluation -> demo.
- [ ] Add AutoDL quickstart commands.
- [ ] Add sample input/output screenshots.
- [ ] Add current limitations.
- [ ] Add short resume bullets using restrained wording.
- [ ] Commit with message `docs: add initial project readme`.

### Task 8: Success and Failure Case Log

**Files:**
- Create: `reports/case_studies.md`

Steps:

- [ ] Record 5 successful chart/report QA examples.
- [ ] Record 5 failed chart/report QA examples.
- [ ] For each failure, label one primary cause: chart type misunderstanding, wrong axis or legend, numeric scale error, multi-step comparison error, answer format mismatch, hallucinated value.
- [ ] Add one screenshot or copied output per case where useful.
- [ ] Commit with message `docs: add qa case studies`.

## Milestone 3: LoRA Experiments, Day 3 to Day 7

**Deliverable:** a comparison table that can be discussed in interviews.

### Task 9: Controlled LoRA Runs

**Files:**
- Modify: `configs/qwen25vl_chartqa.yaml`
- Modify: `scripts/train_lora.py`
- Modify: `reports/experiments.md`

Experiment grid:

- data fraction: `1%`, `3%`, optionally `5%`
- LoRA rank: `8`, `16`
- learning rate: `2e-5`, optionally `1e-4`
- max epochs: `1`

Steps:

- [ ] Run the smoke configuration first.
- [ ] Run at least two real LoRA configurations.
- [ ] Record dataset size, trainable parameters, GPU memory, training time, eval loss, EM, token F1, and numeric accuracy.
- [ ] Save adapters under separate output directories.
- [ ] Add a compact experiment table.
- [ ] Commit with message `exp: compare chartqa lora settings`.

### Task 10: Badcase Analysis

**Files:**
- Create: `reports/badcase_analysis.md`
- Modify: `README.md`

Steps:

- [ ] Group failed cases into chart type misunderstanding, wrong axis or legend, numeric scale error, multi-step comparison error, answer format mismatch, hallucinated value.
- [ ] Include one representative example for each observed group.
- [ ] Add practical next-step fixes for the top 2 failure categories.
- [ ] Summarize the badcase distribution in README.
- [ ] Commit with message `docs: add chartqa badcase analysis`.

## Milestone 4: Scenario Expansion, Day 7 to Day 14

**Deliverable:** make the project feel like an enterprise report assistant, not only a benchmark notebook.

### Task 11: Report Screenshot Samples

**Files:**
- Create: `data/samples/README.md`
- Modify: `app.py`
- Modify: `reports/case_studies.md`

Steps:

- [ ] Add 5-10 public or self-created business chart/report screenshots with licensing notes.
- [ ] Write natural-language questions for each sample.
- [ ] Run base and LoRA inference on these samples.
- [ ] Record where ChartQA fine-tuning helps and where it does not transfer.
- [ ] Commit with message `data: add report screenshot samples`.

### Task 12: Optional OCR/RAG Extension

**Files:**
- Create: `src/chartvqa/rag.py`
- Create: `reports/rag_extension.md`

Steps:

- [ ] Keep this optional unless the VLM fine-tuning route is already stable.
- [ ] For long report PDFs, extract text with OCR or PDF text extraction.
- [ ] Retrieve relevant report text snippets as auxiliary context.
- [ ] Compare VLM-only answer vs VLM plus retrieved context on a few samples.
- [ ] Commit with message `exp: explore report rag extension`.

## Milestone 5: Preference Optimization, Week 3+

**Deliverable:** start with reward reranking and DPO data construction, not a premature GRPO claim.

Scope:

- Generate multiple candidate answers for the same chart question.
- Score candidates using answer match, numeric consistency, format compliance, and hallucination penalty.
- Create chosen/rejected pairs.
- Train or simulate a DPO-style preference step only after the data quality is checked.
- Treat GRPO-style optimization as long-term exploration.

Files:

- `src/chartvqa/reranking.py`
- `tests/test_reranking.py`
- `data/preference/chartqa_preferences.jsonl`
- `reports/reward_reranking.md`

Resume-safe wording:

- "Designed rule-based reward functions for multi-candidate answer reranking, combining answer matching, numeric consistency, and format compliance to reduce unsupported chart answers."

Avoid wording:

- "Used GRPO to significantly improve model reasoning ability."

## Execution Schedule

### 2-3 Day Resume-Ready Version After GPU Is Ready

- Day 1 morning: AutoDL setup, repo clone, token configuration, CUDA/package check.
- Day 1 afternoon: convert Kaggle notebook to scripts and run one-step smoke training.
- Day 2 morning: run base-model evaluation and LoRA smoke adapter evaluation.
- Day 2 afternoon: build Gradio demo and README screenshots.
- Day 3: run at least one real LoRA configuration, write evaluation table and case studies.

### 7-14 Day Stronger Version

- Days 4-5: LoRA rank/data-fraction comparison.
- Days 6-7: badcase analysis and demo polish.
- Days 8-10: report screenshot generalization samples.
- Days 11-14: reward reranking prototype, architecture docs, interview notes, resume variants.

## Definition of Done

MVP is done when:

- AutoDL setup is documented and reproducible.
- One-step Qwen2.5-VL ChartQA QLoRA training succeeds.
- At least one real LoRA run completes.
- Base vs LoRA evaluation exists in `reports/eval_results.csv`.
- Gradio demo can answer questions for sample chart/report images.
- `reports/case_studies.md` contains at least 5 successful and 5 failed cases.
- README includes scenario, training route, evaluation results, screenshots, limitations, and restrained resume bullets.

Strong version is done when:

- At least 3 LoRA configurations have been compared.
- Report screenshot transfer cases are included.
- Badcase analysis explains numeric and chart-structure failures.
- Reward reranking or preference-data construction is prototyped.
- Interview notes cover the 3-minute, 8-minute, and 20-minute project explanations.

## Self-Review

- Spec coverage: the plan now covers the user's revised preference for a current-demand scenario, VLM fine-tuning, AutoDL cloud training, evaluation, badcase analysis, and later DPO/GRPO-style exploration.
- Scope control: OCR/RAG is moved to an optional extension; first-stage work stays centered on Qwen2.5-VL + ChartQA LoRA.
- Resume safety: wording explicitly says open-source reproduction plus secondary implementation and avoids exaggerated GRPO claims.
- Risk coverage: the plan keeps the project centered on VLM adaptation, measurable evaluation, and practical scenario packaging rather than backend CRUD.
