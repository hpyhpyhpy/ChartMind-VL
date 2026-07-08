# ChartMind-VL Base vs LoRA 评估设计说明

## 目标

Smoke test 已经在 AutoDL RTX 4090D 上跑通，本阶段补齐 base model zero-shot 与 LoRA adapter 的对比评估入口。

本阶段在 Codex 本地完成：

- 评估指标函数。
- 推理封装。
- 评估脚本入口。
- 本地单元测试。

真实模型推理仍交给远端 AutoDL 执行。

## 架构

新增 `src/chartvqa/evaluation.py`：

- 文本归一化。
- Exact Match。
- Token F1。
- Numeric Accuracy。
- 单条预测打分和整体汇总。

新增 `src/chartvqa/inference.py`：

- 加载 base model 和 processor。
- 可选加载 LoRA adapter。
- 对单个 ChartQA 样本生成答案。

新增 `scripts/run_eval.py`：

- 读取配置和 ChartQA split。
- 支持 `base`、`lora`、`both` 三种评估模式。
- 输出逐样本 CSV 和指标 summary JSON。

## 输出文件

默认输出：

- `reports/eval_results.csv`
- `reports/eval_summary.json`

CSV 字段包括：

- `mode`
- `index`
- `question`
- `answer`
- `prediction`
- `question_type`
- `exact_match`
- `token_f1`
- `numeric_accuracy`

JSON 汇总包括每种模式的样本数和平均指标。

## 成功标准

- 本地测试覆盖指标和脚本参数解析。
- 本地测试不加载大模型、不访问网络。
- 远端可执行以下命令：

```bash
python scripts/run_eval.py --config configs/qwen25vl_chartqa.yaml --mode both --adapter outputs/qwen25vl-chartqa-smoke --max-samples 20
```

该命令用于第一轮小样本 base vs LoRA 对比，不追求最终指标，只验证评估链路和输出格式。
