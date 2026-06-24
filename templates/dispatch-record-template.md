# dispatch-record.md — 任务派发记录

> Phase 6 必须产出。记录每个任务的派发方式、skill 注入、工具约束。

---

## 派发总览

| 指标 | 值 |
|------|-----|
| 任务总数 | [N] |
| 派发方式 | kanban / delegate_task |
| 执行 Level | A / B / C |
| tester 独立验证 | ✅ / ❌ |

---

## 任务派发明细

### Task 1: [标题]

- **角色**: coder / artist / tester
- **派发方式**: `delegate_task(...)` / `kanban create ...`
- **toolsets**: `['browser', 'vision', 'file', 'skills']`
- **注入 skills**: test-driven-development, incremental-implementation
- **派发时间**: [HH:MM]
- **完成时间**: [HH:MM]
- **状态**: ✅ 已完成 / ❌ 失败 / 🔄 进行中

---

### Task 2: [标题]

<!-- 按需复制上述模板 -->

---

## Skill 注入记录

| 任务 | 角色 | 注入的 Skills |
|------|------|---------------|
| Task 1 | coder | test-driven-development, incremental-implementation |
| Task 2 | artist | frontend-ui-engineering, popular-web-designs |
| Task 3 | tester | test-driven-development |

---

## Toolset 约束记录

| 任务 | 角色 | toolsets | 含 terminal? |
|------|------|----------|-------------|
| Task 1 | coder | terminal, file, skills | ✅ 允许 |
| Task 2 | artist | browser, vision, file, skills | ❌ 不含 |
| Task 3 | tester | browser, vision, file, skills | ❌ 不含 |

> ⚠️ tester 和 artist 的 toolsets 不得包含 terminal（防止 curl 绕过测试约束）

---

## Coordinator Review 记录

- **review 时间**: [HH:MM]
- **tester 报告**: [PASS/FAIL]
- **review 结论**: [通过/打回重测]
- **review 依据**: [简述验证了什么]
