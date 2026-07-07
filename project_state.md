# 项目状态

## 2026-07-07

- 新增 `_ai_rules.md`，作为项目级 AI 协作规则文件。
- 新增 `project_state.md`，用于记录每次可验收任务的完成状态。
- 更新 `_ai_rules.md`，要求说明类文档、开发计划、实验记录、README、注释和面向用户的解释默认使用中文。
- 将 `CLAUDE.md` 改写为中文项目声明，说明项目定位、启动指令、当前主线和工作原则。
- 将设计说明 `docs/superpowers/specs/2026-07-07-vlm-chartqa-cloud-training-design.md` 改写为中文。
- 将实施计划 `docs/superpowers/plans/2026-07-07-docvqa-rag-main-project.md` 改写为中文。
- 新增 `docs/collaboration_workflow.md`，明确 Codex 负责本地架构、代码和问题分析，Claude Code 负责 VS Code SSH 远程算力执行，用户负责调度和反馈日志。
- 新增 `docs/superpowers/specs/2026-07-07-local-scaffold-design.md` 和 `docs/superpowers/plans/2026-07-07-local-scaffold.md`，明确本地训练前脚手架范围。
- 新增项目基础脚手架：`requirements.txt`、`pyproject.toml`、`configs/qwen25vl_chartqa.yaml`、`scripts/cloud_setup_autodl.sh`。
- 新增 `src/chartvqa/config.py`、`src/chartvqa/data.py`、`src/chartvqa/prompting.py`，完成配置加载、ChartQA 样本规范化和 Qwen2.5-VL chat messages 格式化。
- 新增 `tests/test_config.py`、`tests/test_data.py`、`tests/test_prompting.py`，覆盖本地不消耗算力的核心链路。
- 新增 `实习面试资料.md`，记录本阶段做了什么，并整理面向实习面试的关键问答。

当前状态：

- 仓库：`ChartMind-VL`
- 主项目方向：面向企业图表与报表的多模态问答微调系统。
- 主技术路线：Qwen2.5-VL + ChartQA + 4-bit QLoRA + AutoDL 4090。
- 当前阶段：本地训练前脚手架已完成，下一步进入模型与 LoRA 加载、smoke training 脚本和远程 AutoDL 验证准备。
