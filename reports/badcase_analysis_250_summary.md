# 250 条评估 Badcase 摘要

> 本摘要基于 Claude Code 远端生成的 `reports/badcase_analysis_250.md` 交接结果整理。完整逐样本报告位于远端 AutoDL 环境。

## 汇总

| 类型 | 数量 | 占比 |
|------|------|------|
| LoRA 改进 | 6 | 2.4% |
| LoRA 退化 | 1 | 0.4% |
| 两者都对 | 113 | 45.2% |
| 两者都错 | 130 | 52.0% |

## 代表样本

### 样本 24：回答格式改进

- 问题：`Is the percentage value of "STEM" segment 52?`
- 标准答案：`Yes`
- Base：`Yes, the percentage value of the "STEM" segment is 52%.`
- LoRA：`Yes.`
- 观察：Base 回答内容正确但偏长，LoRA 更贴近 ChartQA 的短答案风格。

### 样本 73：数值改进

- 问题：`What is the average of the smallest gray bar and largest light blue bar?`
- 标准答案：`21.5`
- Base：计算过程不完整，未给出最终数值。
- LoRA：`21.5%`
- 观察：LoRA 在该样本上不仅改善格式，也给出了正确数值。

### 样本 235：数值改进

- 问题：`Find the two smallest values in the given chart and add them?`
- 标准答案：`3.2`
- Base：`1.6 + 1.8 = 3.4`
- LoRA：`3.2`
- 观察：Base 出现数值计算错误，LoRA 给出正确答案。

### 样本 244：问答能力改进

- 问题：`How many colors are used in the Graph?`
- 标准答案：`1`
- Base：`The graph uses one color, which is a shade of blue...`
- LoRA：`1 color is used in the graph.`
- 观察：LoRA 输出更接近标准答案的核心信息。

### 样本 142：LoRA 退化

- 问题：`Is the median of green graph from 2002 to 2006 greater than smallest value of orange graph?`
- 标准答案：`No`
- Base：`No.`
- LoRA：`No. The median of the green graph...is approximately 31%, which is not greater...`
- 观察：Base 已经给出完美短答案，LoRA 变啰嗦后从精确匹配退化为部分匹配。

## 结论

250 条 badcase 分析说明，当前 1% 数据 1 epoch LoRA 的收益主要来自两类：

- 答案格式更贴近 ChartQA 短答案风格。
- 少量数值问题从错误变为正确。

同时，LoRA 退化只有 1 条，说明当前 adapter 的风险较低。但两者都错仍有 130 条，占 52.0%，主要问题仍集中在数值读取、数值计算和复杂图表推理上。

因此，下一阶段如果继续优化，不应只追求 Demo 中更好看的单例，而应优先围绕数值错误做训练数据扩展、序列长度调整和 badcase 类型统计。
