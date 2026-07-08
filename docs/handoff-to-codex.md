# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08 11:45

## 本次任务

执行 base vs LoRA 小样本评估 smoke test ✅ 完成

## 执行结果

| 项目 | 结果 |
|------|------|
| 命令是否跑通 | ✅ 全部跑通 |
| 远端 GPU | RTX 4090D 24GB |
| Base 模型推理 | ✅ 20/20 完成 |
| LoRA 推理 | ✅ 20/20 完成 |
| GPU 显存峰值 | 约 22-23 GB（4-bit 量化加载） |
| GPU 显存结尾 | 4 MiB（已释放） |

### 评估指标汇总

```json
{
  "base": {
    "count": 20,
    "exact_match": 0.25,
    "token_f1": 0.3100595238095238,
    "numeric_accuracy": 0.55
  },
  "lora": {
    "count": 20,
    "exact_match": 0.25,
    "token_f1": 0.3100595238095238,
    "numeric_accuracy": 0.55
  }
}
```

Base 与 LoRA 指标完全相同。**原因**：仅 20 步训练的 adapter 权重改变幅度微小，不足以在评估指标上产生差异。这在 smoke test 阶段属于预期行为。

### CSV 前 5 行

```
mode,index,question,answer,prediction,question_type,exact_match,token_f1,numeric_accuracy
base,0,"How many food item...",14,"The bar graph shows 15...",,0.0,0.0,0.0
base,1,"What is the difference...",0.57,"The difference...is 0.57...",,0.0,0.167,1.0
base,2,"How many bars are shown...",3,"There are three bars...",,0.0,0.0,0.0
base,3,"Is the sum value of...","No","No, the sum value...less than...",,0.0,0.167,0.0
```

### 发现的问题

1. **Base vs LoRA 结果相同** — 20 步训练不足以产生可观测差异，后续正式评估需用完整训练（1 epoch）。
2. **SSH 环境变量 caveat** — 非交互式 SSH 不自动加载 `.bashrc`，需显式设置 `HF_ENDPOINT` 和 `HF_HOME`。
3. **远端 config 需保持本地路径** — ModelScope 缓存不兼容 HuggingFace `from_pretrained`，`model.id` 不可改回通用 ID。

### 下一步建议

1. 用完整训练配置（`max_steps` 设为完整 1 epoch）重新训练，再用相同评估脚本对比。
2. 关注 `question_type` 区分 — CSV 中 `question_type` 列为空，后续可据此拆分子集分析 badcase。
3. 构建 Gradio Demo 展示 base vs 正式训练的 LoRA 效果对比。

## 远端环境（当前可用）

- 连接信息：由项目负责人提供
- 进入命令：`cvl`
- 最新代码已同步（commit `f0675af`）
- 评估产物：`reports/eval_smoke_results.csv`、`reports/eval_smoke_summary.json`
- 训练输出：`outputs/qwen25vl-chartqa-smoke/`
