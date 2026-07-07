# 项目状态

## 2026-07-07

- 新增 `_ai_rules.md`，作为项目级 AI 协作规则文件。
- 新增 `project_state.md`，用于记录每次可验收任务的完成状态。
- 更新 `_ai_rules.md`，要求说明类文档、开发计划、实验记录、README、注释和面向用户的解释默认使用中文。
- 将 `CLAUDE.md` 改写为中文项目声明，说明项目定位、启动指令、当前主线和工作原则。
- 将设计说明 `docs/superpowers/specs/2026-07-07-vlm-chartqa-cloud-training-design.md` 改写为中文。
- 将实施计划 `docs/superpowers/plans/2026-07-07-docvqa-rag-main-project.md` 改写为中文。
- 新增 `docs/collaboration_workflow.md`，明确 Codex 负责本地架构、代码和问题分析，Claude Code 负责 VS Code SSH 远程算力执行，用户负责调度和反馈日志。

当前状态：

- 仓库：`ChartMind-VL`
- 主项目方向：面向企业图表与报表的多模态问答微调系统。
- 主技术路线：Qwen2.5-VL + ChartQA + 4-bit QLoRA + AutoDL 4090。
- 当前阶段：协作工作流已明确，下一步由 Codex 完成本地最小闭环脚手架，再交给 Claude Code 在 AutoDL 远程环境中验证。
