# Demo 展示样例

> 基于 250 条评估 badcase 分析整理，用于 Gradio Demo 的推荐展示样本。
> 图片路径: reports/demo_cases/sample_{index}.png

---

## 1. 样本 235 — LoRA 数值改进（首选推荐 ⭐）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_235.png |
| 问题 | Find the two smallest values in the given chart and add them? |
| 标准答案 | 3.2 |
| Base 回答 | 1.6 + 1.8 = 3.4 ❌ |
| LoRA 回答 | 3.2 ✅ |
| 展示用途 | **数值改进** |
| 一句话话术 | Base 模型能识别数值但加法计算错误，LoRA 准确地找到了两个最小值并正确求和，展示了微调对数值推理的改善。 |

---

## 2. 样本 73 — LoRA 数值改进（候选，存在生成波动）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_73.png |
| 问题 | What is the average of the smallest gray bar and largest light blue bar? |
| 标准答案 | 21.5 |
| Base 回答 | 计算过程不完整，未给出最终数值 ❌ |
| LoRA 回答 | (1% + 42%) / 2 = 21.5% ✅ |
| 展示用途 | **数值改进** |
| 一句话话术 | CSV 中 LoRA 给出正确数值而 Base 回答中断；后端复验时 Base 和 LoRA 都答对，说明该样例存在生成波动，更适合作为候选补充而非主展示样例。 |

---

## 3. 样本 24 — LoRA 答案格式改进

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_24.png |
| 问题 | Is the percentage value of "STEM" segment 52? |
| 标准答案 | Yes |
| Base 回答 | Yes, the percentage value of the "STEM" segment is 52%. ❌（冗长，Non-EM） |
| LoRA 回答 | Yes. ✅（精确匹配） |
| 展示用途 | **答案格式改进** |
| 一句话话术 | LoRA 学会了 ChartQA 简洁的 Yes/No 回答风格，而 Base 倾向于输出冗长解释导致格式不匹配。 |

---

## 4. 样本 205 — LoRA 答案格式改进

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_205.png |
| 问题 | Is the median value of all the bars greater than 30? |
| 标准答案 | Yes |
| Base 回答 | Yes, the median value of all the bars is greater than 30. ❌ |
| LoRA 回答 | Yes. ✅ |
| 展示用途 | **答案格式改进** |
| 一句话话术 | 同样是 Yes/No 判断，LoRA 输出简洁精确，说明微调后模型更适应测评指标的评分规则。 |

---

## 5. 样本 244 — LoRA 能力改进（推荐补充）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_244.png |
| 问题 | How many colors are used in the Graph? |
| 标准答案 | 1 |
| Base 回答 | The graph uses one color, which is a shade of blue... ❌（语义正确但格式不匹配） |
| LoRA 回答 | 1 color is used in the graph. ✅（数值正确 + 格式匹配） |
| 展示用途 | **格式+数值混合改进** |
| 一句话话术 | LoRA 不仅给出正确数值，还保持了合理的自然语言格式，兼顾了指标和可读性。 |

---

## 6. 样本 142 — LoRA 退化（模型边界 ⚠️）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_142.png |
| 问题 | Is the median of green graph from 2002 to 2006 greater than smallest value of orange graph? |
| 标准答案 | No |
| Base 回答 | No. ✅（精确匹配） |
| LoRA 回答 | No. The median...is approximately 31%... ❌（语义正确但啰嗦） |
| 展示用途 | **退化边界** — LoRA 反而学会了过度解释 |
| 一句话话术 | 微调并非完美：LoRA 在某些 Base 已精确回答的样本上反而变啰嗦，导致精确匹配下降。 |

---

## 7. 样本 9 — 共同失败（模型边界）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_9.png |
| 问题 | How many more people felt inspired frequently than depressed frequently? |
| 标准答案 | 0.03 |
| Base 回答 | 3 ❌ |
| LoRA 回答 | 3 ❌ |
| 展示用途 | **共同失败** — 数值理解不足 |
| 一句话话术 | Base 和 LoRA 都答 3，标准答案是 0.03——模型不理解百分比差值需要归一化。这是当前微调方法尚未攻克的核心挑战。 |

---

## 8. 样本 13 — 共同失败（模型边界）

| 字段 | 内容 |
|------|------|
| 图片 | reports/demo_cases/sample_13.png |
| 问题 | What's the average of all the values in the green bars (round to one decimal)? |
| 标准答案 | 21.6 |
| Base 回答 | 21.3% ❌ |
| LoRA 回答 | 21.7 ❌ |
| 展示用途 | **共同失败** — 数值精度问题 |
| 一句话话术 | Base 和 LoRA 在平均值计算上都有偏差（21.3 vs 21.6 vs 21.7），说明仅有 1% 数据训练的 LoRA 在复杂数值推理上改善有限。 |

---

## 后端等价验证结果

Claude Code 已通过 Python 脚本直接调用 Demo 后端推理逻辑，对推荐样例进行复验。验证结果如下：

| 样本 | 预期类型 | 复验结果 | 是否适合主展示 |
|------|----------|----------|----------------|
| 235 | 数值改进 | Base 输出 `3.4`，LoRA 输出 `3.2` | 是 |
| 24 | 格式改进 | Base 输出冗长回答，LoRA 输出 `Yes.` | 是 |
| 142 | 退化边界 | Base 输出 `No.`，LoRA 输出较长解释 | 是 |
| 73 | 数值改进 | Base 和 LoRA 本次都答对 `21.5%` | 候选，存在波动 |
| 9 | 共同失败 | Base 和 LoRA 都输出 `3`，标准答案为 `0.03` | 是 |

注意：以上为后端等价验证，不是网页端上传图片后的截图验证。

## 推荐 Demo 展示顺序

推荐正式展示 **4 个稳定样本**，按以下顺序：

1. **样本 235** — LoRA 数值改进最强案例，加法算对了（Base 错了）
2. **样本 24** — 最简洁的格式改进对比（LoRA "Yes." vs Base 冗长）
3. **样本 142** — 诚实地展示 LoRA 也有退化（Base 更好）
4. **样本 9** — 诚实地展示共同局限性（0.03 vs 3）

样本 73 可以作为候选补充，但不建议作为主展示样例，因为后端复验时 Base 也答对了。这个顺序从 "LoRA 有进步" -> "也有局限" -> "我们清楚问题在哪"，呈现一个平衡、可信的展示叙事。

## 数据来源

- 评估数据：reports/eval_lora_1epoch_250_results.csv
- Badcase 分析：reports/badcase_analysis_250.md
- 图片目录：reports/demo_cases/
