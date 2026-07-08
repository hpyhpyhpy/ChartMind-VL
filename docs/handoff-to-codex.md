# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08 12:25

## 本次任务

基于 1 epoch 评估 CSV 生成 badcase 分析报告 ✅ 完成

## 执行结果

| 检查项 | 状态 |
|--------|------|
| badcase 测试 (6 个) | ✅ 全部通过 |
| 评估 CSV 存在 | ✅ 7.8K |
| badcase 报告生成 | ✅ reports/badcase_analysis.md |

## Badcase 汇总

| 类型 | 数量 |
|------|------|
| LoRA 改进 | 1 |
| LoRA 退化 | 0 |
| 两者都对 | 12 |
| 两者都错 | 12 |

### 唯一 LoRA 改进样本（样本 24）

| 字段 | 内容 |
|------|------|
| 问题 | Is the percentage value of "STEM" segment 52? |
| 标准答案 | Yes |
| Base | Yes, the percentage value of the "STEM" segment is 52%. |
| LoRA | **Yes.** |
| 分析 | LoRA 学会了只输出"Yes"，更接近标准答案的简洁风格 |

### 适合 Demo 展示的样本建议

由于 LoRA 改进只有 1 条且改进幅度不大，建议后续用**两者都错的典型 badcase** 来展示模型局限性：

1. **样本 9** — 数值错误："How many more people felt inspired frequently than depressed frequently?" 标准答案 0.03，base/LoRA 都输出 3（不理解百分比差值）
2. **样本 13** — 数值错误："average of green bars" 标准答案 21.6，base/LoRA 都输出 21.3
3. **样本 21** — 数值+时间："When does the gap become largest?" 标准答案 2008，都输出 2004

### 注意事项

badcase 报告中 `错误类型` 分类存在明显误标（EM=1 的样本被标为"完全不匹配"），属于 `badcase.py` 的分类逻辑问题，建议 Codex 检查。不影响数据准确性。

## 远端环境

- 代码已同步（commit `5864653`）
- 分析产物：`reports/badcase_analysis.md`
- GPU 显存：空载（未跑推理）
