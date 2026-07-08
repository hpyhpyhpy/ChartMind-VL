# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

基于 250 条评估 CSV 生成 badcase 报告 ✅ 完成

## 执行结果

| 检查项 | 状态 |
|--------|------|
| CSV 存在 (87K, 500 行) | ✅ |
| badcase 报告生成 | ✅ reports/badcase_analysis_250.md (431 行, 40 个样本) |

## 汇总表

| 类型 | 数量 | 占比 |
|------|------|------|
| 🟢 LoRA 改进 | **6** | 2.4% |
| 🔴 LoRA 退化 | **1** | 0.4% |
| ⚪ 两者都对 | 113 | 45.2% |
| ⚫ 两者都错 | 130 | 52.0% |

## LoRA 改进样本（至少 3 个）

### 样本 24 — 回答格式改进
| 字段 | 内容 |
|------|------|
| 问题 | Is the percentage value of "STEM" segment 52? |
| 标准答案 | Yes |
| Base | Yes, the percentage value of the "STEM" segment is 52%. |
| LoRA | **Yes.** |
| 分析 | Base 冗长(部分匹配), LoRA 简洁(回答正确 ✅) |

### 样本 73 — 数值改进
| 字段 | 内容 |
|------|------|
| 问题 | What is the average of the smallest gray bar and largest light blue bar? |
| 标准答案 | 21.5 |
| Base | 计算过程不完整，未给出最终数值 (数值错误 ❌) |
| LoRA | **21.5%** (回答正确 ✅) |

### 样本 205 — 回答格式改进
| 字段 | 内容 |
|------|------|
| 问题 | Is the median value of all the bars greater than 30? |
| 标准答案 | Yes |
| Base | Yes, the median value of all the bars is greater than 30. |
| LoRA | **Yes.** |
| 分析 | 同样 Base 冗长→LoRA 简洁 ✅ |

### 样本 235 — 数值改进
| 字段 | 内容 |
|------|------|
| 问题 | Find the two smallest values in the given chart and add them? |
| 标准答案 | 3.2 |
| Base | 1.6 + 1.8 = **3.4** (数值错误 ❌) |
| LoRA | **3.2** (回答正确 ✅) |

### 样本 244 — 问答能力改进
| 字段 | 内容 |
|------|------|
| 问题 | How many colors are used in the Graph? |
| 标准答案 | 1 |
| Base | The graph uses one color, which is a shade of blue... (完全不匹配 ❌) |
| LoRA | **1 color is used in the graph.** (回答正确 ✅) |

## LoRA 退化样本

只有 1 条 **(样本 142)**：

| 字段 | 内容 |
|------|------|
| 问题 | Is the median of green graph from 2002 to 2006 greater than smallest value of orange graph? |
| 标准答案 | No |
| Base | **No.** (回答正确 ✅) |
| LoRA | No. The median of the green graph...is approximately 31%, which is not greater... (部分匹配 ❌) |

分析：Base 已完美回答"Answer"，LoRA 变啰嗦，从精确匹配退化为部分匹配。

## 主要错误类型观察

1. **数值错误占主导**："两者都错" 130 条中大部分是数值错误（占约 60-70%）— Base 和 LoRA 在图表数值理解上的不足高度一致
2. **回答格式改进是 LoRA 主要收益**：6 个改进样本中 4 个是基座输出了完整句子而 LoRA 学会了简洁风格
3. **LoRA 也修正了少量数值错误**：样本 73 和 235 显示 LoRA 不仅在格式上改进，在特定数值计算上也比 Base 更准
4. **退化极少**：仅 1 条退化（0.4%），且退化原因是 Base 已完美而 LoRA 变得啰嗦，并非答错

总体：1% 数据训练的 LoRA 在回答风格和少量数值上产生了积极但微弱的变化。

## 远端环境

- 代码已同步（commit `b065af4`）
- 产物：`reports/badcase_analysis_250.md`
