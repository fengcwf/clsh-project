# clsh-project 版本历史

> 完整版本历史。SKILL.md 只保留最近 3 版。

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.25.0 | 2026-06-07 | **Kanban scratch workspace + delegate_task 决策树**：新增 pitfalls #89（scratch workspace 产出文件丢失 → 代码生成用 delegate_task）、#90（`max_in_progress_per_profile` 需要 gateway restart）。更新 kanban-ops-lessons.md §4-6。同步更新 delegation-protocol 决策树。 |
| v5.24.0 | 2026-06-07 | **SkillOpt + Superpowers 三方对比分析**：分析 SkillOpt 训练循环和 Superpowers v5.1.0 TDD for Skills、Rationalization Prevention。实施：P0-B TDD for Skills，P1-B rejected-edits.md，P1-A pitfalls 内嵌到 7 个 Phase workflow 文件。 |
| v5.19.0 | 2026-06-04 | **Phase 8 强制机制 + Pitfall 强化**：新增 §3.1 Round Exit Checklist（文档写入门禁）。Phase 8 tester 卡 summary 要求模板。Pitfall #49 强化（5 轮触发案例）。Pitfall #79 新增（tester 无通知）。 |
| v5.15.0 | 2026-06-03 | **CodeWhale ACP → Kanban 派发回归**：Phase 6/8 的 coder/artist 角色从 CodeWhale ACP 改回 kanban 派发。Way C 铁律不变（给路径+目标，不做代码推理），派发方式从 delegate_task(acp_command) 改为 kanban create。15+ pitfalls 中的 CodeWhale 引用更新为 worker/kanban。 |
| v5.13.0 | 2026-06-02 | **LLM 能力无关性原则 + Harness/Superpowers 对比落地**：新增核心设计原则、Review Checklist 模板、Spec Delta 必填字段、Session Launch Guidance。 |
| v5.12.0 | 2026-06-02 | **知识复利系统 + Review skill 显式调用 + wiki-lint 适配**：wiki/projects/ 迁移至 raw/projects/，新增 wiki/solutions/ 跨项目方案库，Phase 0 新增跨项目知识注入。 |
| v5.11.0 | 2026-06-01 | **fetch credentials + URL 自构造陷阱**：新增 pitfall #64-65。 |
| v5.10.1 | 2026-06-01 | **GET handler 缺失 + CodWhale 网络超时**：新增 pitfall #62-63。 |
| v5.10.0 | 2026-05-31 | **Phase 8 测试记录 + Way C 铁律 + 外部 API 集成**：新增 pitfall #59-61。 |
| v5.9.0 | 2026-05-31 | **Skill 删除陷阱 + 需求澄清顺序**：新增 pitfall #57-58。 |
| v5.8.0 | 2026-05-29 | **自进化方法论落地**：Darwin 9 维 rubric + 维度关联簇 + ECC 执行验证。 |
| v5.7.0 | 2026-05-29 | **自进化方案 Layer 1+2 落地**：5 步验证函数 + 防辩解表 + 棘轮机制。 |
| v5.6.0 | 2026-05-29 | **Way C 派发铁律强化**：更新 codewhale-acp-integration.md 新增 Way C 详细规范。 |
| v5.5.3 | 2026-05-28 | **内容管理子模块模式 + CodeWhale 文件损坏 + Vue 解构**：新增 pitfall #47-50。 |
| v5.5.2 | 2026-05-27 | **Workspace 子模块模式 + CodeWhale 二轮补全**：新增 pitfall #43-46。 |
| v5.4.0 | 2026-05-27 | **CodeWhale ACP 集成**：Phase 6/8 的 coder/artist 角色使用 CodeWhale ACP 执行。 |
| v5.3.7 | 2026-05-26 | **.env hash 格式 + spec 残留清理**：新增 pitfall #36-37。 |
| v5.3.4 | 2026-05-25 | **Karpathy + Superpowers 行为约束融合**：诊断引擎模式 + 防辩解表。 |
| v5.3.3 | 2026-05-25 | **CSS containing block + tester 应付教训**：新增 pitfall #33-34。 |
| v5.3.2 | 2026-05-25 | **Phase 8 Wave 分批 + Pitfall #25 强化**。 |
| v5.3.1 | 2026-05-25 | **Review 修复**：Pitfalls 重新编号，新增 #29-30。 |
| v5.3.0 | 2026-05-25 | **Matt Pocock Skills 借鉴**：代码交叉验证、CONTEXT.md、ADR、Vertical Slice、Prototype、Handoff。 |
| v5.2.3 | 2026-05-24 | **Phase 8 派发方式纠正**：用户明确要求 kanban 派发，禁止 delegate_task 替代。 |
| v5.2.1 | 2026-05-24 | **设计工具链补充**：Stitch MCP + UI prompt 框架。 |
| v5.2.0 | 2026-05-24 | **设计工具链更新**：全面使用 Open Design tokens。 |
| v5.1.0 | 2026-05-23 | **gstack 借鉴落地**：Browser QA + Pre-Commit 安全自检。 |
| v5.0.0 | 2026-05-23 | **SKILL.md 瘦身**：Phase 详情拆分到 references/workflow/。 |
| v4.3.0 | 2026-05-23 | **蒸馏 v2 集成**：Phase 0 读取 learnings.md + Phase 6 微蒸馏 + Phase 7 条件触发深度蒸馏。 |
| v4.1.0 | 2026-05-22 | **上游优化集成**：Wave 并行派发 + Bugfix Spec 结构化格式。 |
| v4.0.0 | 2026-05-22 | **Pitfalls 大迁移 + 边界定义**：89→78 条，三类迁移。 |
| v3.8.0 | 2026-05-21 | Phase 6 与 Hermes Kanban 对齐。 |
| v3.7.0 | 2026-05-21 | References 架构重构。 |
