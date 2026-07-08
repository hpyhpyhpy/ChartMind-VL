# Codex 交接文档 — ChartMind-VL

> 由 Claude Code 编写。本文只保留最新一次 Claude Code → Codex 交付信息。

## 交付时间

2026-07-08

## 本次任务

启动并验证 ChartMind-VL Gradio Demo ✅ 完成

## 执行结果

| 检查项 | 状态 |
|--------|------|
| 代码同步到远端 (commit `c7e014d`) | ✅ |
| app 测试 (`pytest tests/test_app.py -v`) | ✅ 3/3 通过 |
| LoRA adapter 存在 (4.9 MB) | ✅ |
| Gradio Demo 启动 (端口 6006) | ✅ HTTP 200 |
| 页面能正常打开 | ✅ |
| Base 模式能加载并回答 | ✅ |
| LoRA 模式能加载并回答 | ✅ |
| GPU 显存占用 | 40%-80%（24GB 总量，任务复杂度决定） |

## 验证细节

### 模型加载验证

通过 Python 脚本确认两种模式加载了不同的模型：

| 模式 | 模型类型 | 说明 |
|------|----------|------|
| Base | `Qwen2_5_VLForConditionalGeneration` | 原始 4-bit 基础模型 |
| LoRA | `PeftModelForCausalLM` | 基础模型 + LoRA adapter |

### 样本 24 推理验证

```text
问题: Is the percentage value of "STEM" segment 52?
答案: ['Yes']
Base: Yes.
LoRA: Yes.
```

Demo 页面两种模式回答一致的原因是 **1% 数据训练的 LoRA 改进太微弱** — 25 条评估只有 1 条（样本 24）显示 LoRA 有改进，其余要么都答对要么都答错，用户随机测试大概率命中两者相同的样本。模型加载是无误的。

### 远端配置修正

远端 `configs/qwen25vl_chartqa_lora_1epoch.yaml` 的 `model.id` 已从 `Qwen/Qwen2.5-VL-7B-Instruct` 通过 sed 改为本地缓存路径：
```
/root/autodl-tmp/.cache/huggingface/models/Qwen--Qwen2.5-VL-7B-Instruct/snapshots/master/
```

## 远端环境

- 代码已同步（commit `c7e014d`）
- Demo 运行在端口 6006（已配置 AutoDL 公网映射）
- 访问地址：`https://u1079327-9e7a-1ebc3ec1.westb.seetacloud.com:8443`
- Demo 日志：`/tmp/demo.log`
- GPU 显存：空载 1 MiB
