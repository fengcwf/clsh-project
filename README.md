# clsh-project — 需求驱动项目开发工作流

## 概述

当大佬提出新的项目或功能需求时，**不直接写代码**，而是走完整的 需求→设计→计划→执行 流程。

**核心理念（来自 Kiro + Superpowers + Phoenix + Ralph Loop）：**
- 需求不能跳到编码 — 必须经过需求澄清 → 设计 → 计划
- 文档是锚点 — 需求和设计必须写成文档，防止进度丢失和跑偏
- 分阶段审批 — 每个阶段需要大佬确认后才进入下一阶段
- 状态机执行 — 流程控制权在代码，不在 LLM
- Ralph Loop 原则 — 灵犀是循环编排者，agent 是单步执行器

## 何时触发

以下任一条件满足时主动触发：
1. 大佬发送 `/clsh-project` 或 `/project`
2. 大佬说"我要做一个 XXX"、"开发一个 XXX 系统"、"实现 XXX 功能"
3. 大佬提出的需求明显是多步骤项目

**不触发的情况：** 简单查询、单步操作、修复 bug（用 systematic-debugging）

## 流程总览

```
大佬: "我要做一个 XXX 系统"
           ↓
Phase 1: 需求澄清（一次一个问题，多选优先；UI项目可选 Visual Companion）
           ↓ [大佬确认需求]
Phase 2: 提出 2-3 个方案 + 推荐理由
           ↓ [大佬确认方案]
Phase 2.5: Technical Spike（可选，技术不确定时）
           ↓ [VALIDATED]
Phase 3: 写设计文档 + Constitution
           ↓ [大佬确认设计]
Phase 4: 设计文档自检（含流程合规检查） + 大佬确认
           ↓ [大佬确认进入执行]
Phase 5: 写实现计划（bite-sized + TDD + No Placeholders + Type Consistency）
           ↓
Phase 6: Ralph Loop 分发执行（coder/artist/tester + Security Scan + Auto-Fix）
           ↓ [tester 通过]
Phase 7: 完成归档 + 流程复盘
           ↓
Phase 8: 反馈循环（大佬测试后，diagnose 6 阶段）→ 回到 Phase 1 或 Phase 6
```

**⛔ 关键：每个 ↓ 处必须有明确的大佬确认，才能进入下一阶段。**

## 各 Phase 详解

### Phase 1: 需求澄清
- **调研前置**：提问前默认调研类似项目/行业方案，输出调研摘要（3-5 条关键发现 + 2-3 条项目启示）写入 `conversation.md`
- **一次只问一个问题**，多选题优先
- **先理解目的，再讨论细节**
- **Visual Companion**（UI/视觉项目专用）：可启动本地 HTML 页面展示设计方案

### Phase 2: 方案设计
- 提出 2-3 个方案，每个说清楚优缺点和工作量
- **技术不确定性检查**：有不确定时必须进入 Phase 2.5

### Phase 2.5: Technical Spike（可选）
- 在写设计文档前验证技术可行性
- 分解为 2-5 个可行性问题 → 快速原型 → 裁决（VALIDATED/PARTIAL/INVALIDATED）

### Phase 3: 写设计文档 + Constitution
- 产出：`proposal.md` + `constitution.md`
- Constitution 是项目级"宪法"，定义 AI worker 必须遵守的技术约束

### Phase 4: 设计文档自检 + 大佬 Review
- 流程合规检查（6 项）+ 文档质量自检（6 项）
- 自检通过后向大佬确认

### Phase 5: 写实现计划
- **No Placeholders**：禁止 TBD/TODO/"类似 Task N"
- **Type Consistency**：跨任务签名一致
- **文件依赖图**：标注任务间依赖
- **垂直切片策略**：3 种切片方式（垂直/契约优先/风险优先）
- **Self-Review**：写完计划后 fresh eyes 检查

### Phase 6: Ralph Loop 分发执行
- **状态机 8 步**：agent 执行 → CHECKPOINT → 灵犀验证 → Security Scan → Quality Review → Tester
- **Auto-Fix Loop**：最多 2 轮，2 轮后 escalate 给大佬
- **角色分离**：后端→coder，UI→artist，测试→tester，灵犀只协调

### Phase 7: 完成归档 + 流程复盘
- 更新提案状态、归档变更、更新 Source of Truth
- 流程合规复盘（7 项）写入 `retrospective.md`

### Phase 8: 反馈循环
- **Diagnose 6 阶段**：建循环 → 复现 → 假设 → 插桩 → 修复 → 复盘
- 3 条路径：Bug 修复 / 体验优化 / 新需求

## 流程门禁

| 门禁 | 检查内容 | 未通过 → |
|------|---------|---------|
| Phase 3→4 | proposal.md 已写入 + `ls` 验证 | 不允许写代码 |
| Phase 4→5 | 大佬明确回复"确认" | 不允许写 tasks.md |
| Phase 5→6 | tasks.md 已写入 + 每 Task 有验收标准 | 不允许创建 kanban 卡 |
| Phase 6 执行 | 代码任务必须有 tester 卡 | 不允许标记完成 |
| Phase 6 安全 | 每个 Task 必须通过 Security Scan | 不允许进入 Quality Review |
| Phase 6 修复 | Auto-Fix 最多 2 轮 | 2 轮后必须 escalate 给大佬 |
| Phase 6 测试 | 修复后必须 tester 验证 | 不允许汇报完成 |

## 快捷方式

- 大佬说"简单做一下" → 可跳过 Phase 2（方案对比），但 Phase 1 和 Phase 3 不能跳过
- Phase 2.5 Spike 是可选的，仅在技术不确定时触发

## Common Pitfalls

1. **灵犀直接写代码** — 即使"很快能做完"也必须派 agent
2. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证
3. **Phase 6 没有安全扫描** — 每个 Task 的 review 必须包含安全扫描
4. **tester 只做功能测试** — tester 应运行完整的 requesting-code-review 流水线
5. **攒到最后一起提交** — 每个 Task 后必须 commit
6. **Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环
7. **agent 自判完成** — 必须通过 CHECKPOINT 客观验证
8. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
9. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
10. **忽略 Type Consistency** — 跨任务的函数签名/类型必须一致

## Verification Checklist（每次使用此 skill 前）

- [ ] 确认不是简单查询/单步操作
- [ ] 确认 Phase 1-3 已完成且有文档产出
- [ ] 确认大佬已明确回复"确认"才进入下一 Phase
- [ ] 确认 tasks.md 中每个 Task 有验收标准 + 完整代码（无 TBD/TODO）
- [ ] 确认代码任务已派给 coder/artist，不是灵犀直接写
- [ ] 确认每个 Task 有 tester 卡
- [ ] 确认 Phase 6 有 Security Scan 步骤
- [ ] 确认 Phase 8 反馈走流程而非"顺手修了"
- [ ] 确认 Auto-Fix 不超过 2 轮后 escalate

## 参考文件

- `references/ralph-loop-analysis.md` — Ralph Loop 调研：原理 + 与 Phase 6 映射
- `references/superpowers-v5-changes.md` — Superpowers v5 关键变更及对 clsh-project 的影响
- `references/kiro-superpowers-analysis.md` — Kiro + Superpowers + Phoenix 工作流分析
- `references/agent-skill-execution-research.md` — Agent Skill 执行跑偏问题：根因分析 + 5种解决方案
- `references/constitution-template.md` — Constitution 模板
- `references/kanban-tasks-bridge.md` — Kanban bridge 说明
- `references/openspec-comparison.md` — OpenSpec 对比分析
- `references/violation-case-2026-05-15-self-coding.md` — 灵犀直接写代码违规案例
- `references/github-sync-guide.md` — GitHub 同步指南

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.5.0 | 2026-05-17 | Phase 1 新增"调研前置"环节：需求提问前默认调研类似项目/行业方案，输出调研摘要写入 conversation.md |
| v2.4.0 | 2026-05-16 | P0-P3 全面优化（Security Scan/Auto-Fix/Spike/Visual Companion 等） + git 仓库迁移到 clsh-project 目录 |
| v2.3.0 | 2026-05-15 | 铁律 8 条 + Phase 6 状态机 + Phase 8 反馈循环 |
| v2.2.0 | 2026-05-13 | Kanban bridge + tasks.md 回写 |
| v2.1.0 | 2026-05-12 | Constitution 模板 + Phase 4 自检 |
| v2.0.0 | 2026-05-11 | 初始版本 |
