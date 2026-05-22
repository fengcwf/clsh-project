# clsh-project — 需求驱动项目开发工作流

## 概述

当大佬提出新的项目或功能需求时，**不直接写代码**，而是走完整的 需求→设计→计划→执行 流程。

**核心理念（来自 Kiro + Superpowers + Phoenix + Ralph Loop）：**
- 需求不能跳到编码 — 必须经过需求澄清 → 设计 → 计划
- 文档是锚点 — 需求和设计必须写成文档，防止进度丢失和跑偏
- 分阶段审批 — 每个阶段需要大佬确认后才进入下一阶段
- 状态机执行 — 流程控制权在代码，不在 LLM
- Ralph Loop 原则 — 灵犀是循环编排者，agent 是单步执行器

## 边界定义

### 管什么
- 流程编排（Phase 1-8 门禁和流转）
- 角色分离（灵犀 ≠ coder）
- 质量保障（checkpoint + review + security scan）
- 文档管理（wiki/projects/ 结构）

### 不管什么
- 具体技术实现细节 → `wiki/projects/<项目>/references/pitfalls/`
- Hermes 工具链使用细节 → `references/integration/hermes-pitfalls.md`
- 调试方法论 → `diagnose` skill
- 代码质量规则 → `code-principles` skill

### 膨胀阈值
- SKILL.md: ≤ 900 行
- Common Pitfalls: ≤ 25 条（超出迁移）
- references/: ≤ 25 个文件（超出归档）

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

## 架构

```
clsh-project/
├── SKILL.md                              ← 主流程定义（~1140 行）
├── README.md                             ← 本文件
└── references/
    ├── methodology/                      ← 方法论研究（5 个文件）
    │   ├── kiro-superpowers-analysis.md
    │   ├── ralph-loop-analysis.md
    │   ├── superpowers-v5-changes.md
    │   ├── superpowers-architecture-analysis.md
    │   └── agent-skill-execution-research.md
    ├── templates/                        ← 流程模板（4 个文件）
    │   ├── constitution-template.md
    │   ├── archive-workflow.md
    │   ├── phase7-archive-checklist.md
    │   ├── phase8-checkpoint-template.md  ← ⭐ 修复进度持久化
    │   └── cloud-server-wireguard.md
    ├── integration/                      ← 工具链集成 + 陷阱（8 个文件）
    │   ├── hermes-pitfalls.md            ← ⭐ 工具链陷阱（从 Common Pitfalls 迁移）
    │   ├── kanban-tasks-bridge.md
    │   ├── hermes-plugin-hooks-reference.md
    │   ├── hermes-plugin-zero-token.md
    │   ├── hermes-slash-command-mechanism.md
    │   ├── halo-auth.md
    │   ├── halo-cli-auth.md
    │   └── reference-migration-pattern.md
    └── pitfalls/                         ← 流程违规案例（8 个文件）
        ├── violation-case-2026-05-15.md
        ├── violation-case-2026-05-18.md
        ├── violation-case-2026-05-20.md
        ├── phase8-context-management.md
        ├── phase8-session-management.md
        ├── phase8-frontend-debug-patterns.md
        ├── memory-tool-traps-2026-05-21.md
        └── technical-traps-2026-05-20.md
```

### 项目专属参考（wiki）

```
wiki/projects/<项目名>/
└── references/
    └── pitfalls/                         ← 技术陷阱（从 Common Pitfalls 迁移）
        ├── node-esm-traps.md             ← ESM/require/await 模块陷阱
        ├── frontend-css-traps.md         ← z-index/sticky/alpha CSS 陷阱
        ├── markdown-render-traps.md      ← 表格正则/Heading ID 渲染陷阱
        ├── server-ops-traps.md           ← 端口冲突/execSync/路由注册
        └── deployment-traps.md           ← Docker→pm2/环境路径差异
```

## 相关 Skills

| Skill | 关系 | 说明 |
|-------|------|------|
| `kanban-orchestrator` | Phase 6 执行 | 任务分解 + 派发 |
| `kanban-worker` | Phase 6 执行 | Worker 执行协议 |
| `subagent-driven-development` | Phase 6 执行 | 子 agent 派发模式 |
| `plan` | Phase 5 计划 | 实现计划编写 |
| `spike` | Phase 2.5 | 技术可行性验证 |
| `diagnose` | Phase 8 调试 | 6 阶段诊断循环 |
| `test-driven-development` | Phase 5-6 | TDD 流程 |
| `incremental-build` | Phase 5 | 垂直切片策略 |
| `requesting-code-review` | Phase 6 Review | 代码审查流水线 |
| `obsidian-operations` | 文档管理 | wiki 归档 |

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

## Common Pitfalls（精简版）

> 78 条教训已去重迁移。流程纪律保留在下方，技术陷阱→`wiki/projects/<项目>/references/pitfalls/`，工具链→`references/integration/hermes-pitfalls.md`。

### 角色分离（铁律）
1. **禁止灵犀直接写代码** — 即使"很快能做完"也必须派 agent
2. **禁止 Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环
3. **角色分离违规** — worker 卡住时不能自己动手，创建 fix 卡或 escalate
4. **Phase 8 必须走角色分离** — 小修复用 delegate_task，大修复用 kanban

### 流程完整性
5. **方向变化不回 Phase 1** — 核心定位变化必须回 Phase 1，不能回 Phase 3
6. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证
7. **Phase 5 缺少 Self-Review** — tasks.md 写完后必须 4 项自检
8. **Phase 6 不做 Spec-Code 同步** — 每个 Task 完成后更新 proposal.md
9. **Phase 7 归档不完整** — 必须检查 overview.md + completion-summary + retrospective + Phase 8 归档

### 质量保障
10. **agent 自判完成** — 必须通过 CHECKPOINT 客观验证
11. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
12. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
13. **写入文件后不验证路径** — write_file 后必须 `ls` 确认

### 执行纪律
14. **超时后提交半成品** — 子 agent 超时后 git stash/revert
15. **Phase 8 上下文溢出** — 每轮最多修 3-4 个 bug，用 execute_code 批量读代码

## 版本历史

| 版本 | 日期 | 变更 |
| v4.1.0 | 2026-05-22 | **上游优化集成**：Wave 并行派发 + Bugfix Spec + checkpoint 模板 |
| v4.0.0 | 2026-05-22 | **Pitfalls 大迁移 + 边界定义**：89→15 条精简，技术陷阱→wiki，工具链→hermes-pitfalls.md |
| v3.8.0 | 2026-05-21 | Phase 6 与 Kanban 对齐（Blocked 状态、Review 卡时机） |
| v3.7.0 | 2026-05-21 | References 架构重构（项目→wiki、跨项目→wiki/reference/） |

> 完整版本历史见 git log。
