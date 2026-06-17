# Workflow Overview — Spec-Driven Development

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Spec-Driven Development                       │
│                      8-Phase Workflow                            │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────┐
  │  START   │
  └────┬─────┘
       │
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 1: Scout & Requirements                                │
  │ ─────────────────────────────                                │
  │  Input:  User request / problem statement                    │
  │  Action: Research tech constraints, existing code, deps      │
  │  Output: requirements.md, tech-constraints.md                │
  │  Gate:   requirements.md 有 ≥5 条可测试需求                   │
  └────┬─────────────────────────────────────────────────────────┘
       │ requirements.md ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 2: Proposal                                            │
  │ ──────────────────                                           │
  │  Input:  requirements.md, tech-constraints.md                │
  │  Action: Design architecture, tech choices, scope            │
  │  Output: proposal.md, architecture.md                        │
  │  Gate:   proposal 包含 out-of-scope + 风险登记               │
  └────┬─────────────────────────────────────────────────────────┘
       │ proposal.md ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 3: Constitution                                        │
  │ ────────────────────                                         │
  │  Input:  proposal.md, architecture.md                        │
  │  Action: Define MUST/SHOULD 约束 + 验收标准                  │
  │  Output: constitution.md                                     │
  │  Gate:   每条 MUST 约束有可执行验证命令                       │
  └────┬─────────────────────────────────────────────────────────┘
       │ constitution.md ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 4: Analysis                                            │
  │ ──────────────────                                           │
  │  Input:  All Phase 1-3 outputs + existing codebase           │
  │  Action: Analyze impact, identify changes, security review   │
  │  Output: analysis.md (findings with file refs + action items)│
  │  Gate:   每条 finding 有 [file:line] 证据引用                 │
  └────┬─────────────────────────────────────────────────────────┘
       │ analysis.md ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 5: Task Planning                                       │
  │ ─────────────────────                                        │
  │  Input:  analysis.md, proposal.md, constitution.md           │
  │  Action: Create executable task list                         │
  │  Output: tasks.md (每个任务有 role/scope/verify/out-of-scope)│
  │  Gate:   每个任务 ≤1 文件, ≤100 行, 有 verify 命令           │
  │  ★ Gate: tasks.md 必须经过 C7 review 才能执行                │
  └────┬─────────────────────────────────────────────────────────┘
       │ tasks.md ✓ + C7 ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 6: Execution                                           │
  │ ───────────────────                                          │
  │  Input:  tasks.md + context from Phases 1-5                  │
  │  Action: Delegate tasks to appropriate roles                 │
  │  Output: 实际代码/文档改动 + verification evidence           │
  │  Gate:   每个任务有 verification output + diff evidence      │
  │  Loop:   task → execute → verify → next task                 │
  └────┬─────────────────────────────────────────────────────────┘
       │ All tasks verified ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 7: Review                                              │
  │ ──────────────                                               │
  │  Input:  All Phase 6 outputs (entire project)                │
  │  Action: Independent review (not self-review!)               │
  │  Output: review-report.md (severity + evidence + recommendation)│
  │  Gate:   0 critical findings, 0 unresolved majors            │
  └────┬─────────────────────────────────────────────────────────┘
       │ review-report.md ✓
       ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Phase 8: Finalize & Archive                                  │
  │ ────────────────────────                                     │
  │  Input:  All outputs, review report, user feedback           │
  │  Action: Final report, archive to projects/<name>/           │
  │  Output: final-report.md, projects/<name>/                   │
  │  Gate:   final-report 生成 + archive 完成                     │
  └────┬─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────┐
  │   DONE   │
  └──────────┘
```

---

## Phase Transition Rules

| 触发条件 | 当前 Phase → 下一 Phase | 前置条件 |
|---------|----------------------|---------|
| 需求收集完成 | P1 → P2 | requirements.md 存在且 ≥5 条可测试需求 |
| 技术方案确定 | P2 → P3 | proposal.md + architecture.md 完成 |
| 约束定义完成 | P3 → P4 | constitution.md 中 MUST 项有验证命令 |
| 分析完成 | P4 → P5 | analysis.md 每条 finding 有 evidence |
| 任务规划完成 | P5 → P6 | tasks.md 通过 C7 review |
| 所有任务执行完 | P6 → P7 | 每个任务有 verification evidence |
| 审查通过 | P7 → P8 | review-report 中 0 critical, 0 unresolved majors |
| 归档完成 | P8 → DONE | final-report + archive 完成 |

### 回退规则

| 触发条件 | 当前 Phase → 回退到 | 动作 |
|---------|-------------------|------|
| Review 发现设计缺陷 | P7 → P4 | 重新分析 + 重新规划 |
| 任务过大无法执行 | P6 → P5 | 重新拆分任务 |
| 架构选型错误 | P4 → P2 | 重新设计 |
| 需求变更 | Any → P1 | 重新收集需求 |
| subagent 执行失败 | P6 → P6 | 记录错误，调整任务重试 |

---

## Session Management

### 何时继续同一 Session

- Phase 1-3 产出完整且可读
- 项目上下文 < 50K tokens
- 没有中断或外部依赖等待
- 当前 phase 的工作 < 1 小时
- 用户确认"继续"

### 何时开新 Session

- 上下文已 > 70K tokens（需要清理）
- 上一个 phase 产出有歧义需要澄清
- 需要等待外部输入（API key、用户决策）
- 用户主动要求暂停
- 跨天或跨长时间段

### Session 切换 Checklist

1. 确保当前 phase 产出已保存到文件
2. 记录 session 号和完成的 phase 到 progress.md
3. 下一个 session 的第一步：读取 progress.md + 最新产出文件
4. 验证文件完整性（无截断、格式正确）

---

## Project Pausing & Stashing

### 临时暂停（同 session 内）

```
1. 保存当前 phase 的中间产出
2. 记录进度到 progress.md
3. 不执行任何归档
4. 恢复时直接读取 progress.md 继续
```

### 长期暂停（跨 session）

```
1. 确保当前 phase 产出完整（不允许 half-done）
2. 执行归档：projects/<name>/stashed/
3. 记录原因和恢复条件
4. 恢复时从 projects/<name>/stashed/ 恢复
5. 重新验证所有产出完整性
```

### 暂停禁止事项

- ❌ 不允许 phase 执行到一半就暂停（必须完成当前 phase）
- ❌ 不允许跳过 verification 就暂停
- ❌ 不允许在 subagent 执行中暂停

---

## Failure Modes

| 失败模式 | 症状 | 恢复策略 | 预防措施 |
|---------|------|---------|---------|
| **上下文窗口溢出** | 丢失早期 phase 决策 | 从文件重建上下文 | 每 phase 独立文件 |
| **Subagent 无声失败** | "done" 但无产出 | 检查 verification evidence | 成功判定 = 证据，非声明 |
| **任务膨胀** | 一个任务 >100 行 | 拆分任务 | 模板强制限制 |
| **角色混淆** | 同一角色做 coder+reviewer | 重新分配角色 | 流程硬性隔离 |
| **依赖冲突** | 多个任务改同一文件 | 串行化 + 重排 | scope 互斥检查 |
| **需求漂移** | scope 不断膨胀 | 回到 P1 重新定义 | constitution 约束 |
| **格式不一致** | 每次输出格式不同 | 使用标准模板 | 模板字段必填 |
| **遗漏安全检查** | 安全漏洞进入生产 | 回退到 P4 安全分析 | security checklist 必填 |
| **过早优化** | 项目未完成就开始优化 | 回到核心功能 | complexity budget |
| **文件丢失** | phase 产出被覆盖 | 从 git 恢复 | 每次写入前备份 |

---

## Key Metrics

| 指标 | 目标值 | 计算方式 |
|-----|-------|---------|
| 任务粒度 | ≤1 文件, ≤100 行 | tasks.md scope 统计 |
| 验证覆盖率 | 100% | 有 verify 命令的任务比例 |
| Review 独立性 | 100% | 不同角色执行 review |
| 回退次数 | ≤2 | 跨 session 统计 |
| Critical 发现修复率 | 100% | 修复的 critical / 总 critical |
