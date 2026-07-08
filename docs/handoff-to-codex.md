# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

使用修复后的 badcase 逻辑重新生成 badcase 分析报告 ✅ 完成

## 执行结果

| 检查项 | 状态 |
|--------|------|
| 代码同步到远端 (commit `17f8f7e`) | ✅ |
| badcase 测试 (7 个) | ✅ 全部通过 |
| 评估 CSV 存在 | ✅ 7.8K |
| badcase 报告重新生成 | ✅ reports/badcase_analysis.md |

## Badcase 汇总

| 类型 | 数量 |
|------|------|
| LoRA 改进 | 1 |
| LoRA 退化 | 0 |
| 两者都对 | 12 |
| 两者都错 | 12 |

### 错误类型修复验证

**关键验证通过**：所有 EM=1 或 numeric=1 的正确预测样本现在都显示 `回答正确`，不再误标为 `完全不匹配`。

验证样本（共 12 条"两者都对"的样本，错误类型均为 `回答正确`）：
- 样本 1：回答正确 ✅
- 样本 4：回答正确 ✅
- 样本 5：回答正确 ✅
- 样本 6：回答正确 ✅
- 样本 10：回答正确 ✅
- 样本 11：回答正确 ✅
- 样本 12：回答正确 ✅
- 样本 14：回答正确 ✅
- 样本 15：回答正确 ✅
- 样本 16：回答正确 ✅
- 样本 17：回答正确 ✅
- 样本 22：回答正确 ✅

### 唯一 LoRA 改进样本（样本 24）

| 字段 | 内容 |
|------|------|
| 问题 | Is the percentage value of "STEM" segment 52? |
| 标准答案 | Yes |
| Base | Yes, the percentage value of the "STEM" segment is 52%. |
| LoRA | **Yes.** |
| base 错误类型 | 部分匹配但不精确 |
| LoRA 错误类型 | **回答正确** ✅ |

修复前：LoRA 也被标为"完全不匹配"（误标）
修复后：LoRA 正确显示为"回答正确"

### 典型失败样本（供 Demo / README 展示）

1. **样本 9**（数值错误）— "How many more people felt inspired frequently than depressed frequently?" 标准答案 0.03，base/LoRA 都输出 3（不理解百分比差值原理）
2. **样本 13**（数值错误）— "average of green bars" 标准答案 21.6，都输出 21.3
3. **样本 21**（数值+时间）— "When does the gap become largest?" 标准答案 2008，都输出 2004

## 远端环境

- 代码已同步（commit `17f8f7e`）
- 分析产物：`reports/badcase_analysis.md`（已覆盖旧版）
- GPU 显存：空载（未跑推理）
