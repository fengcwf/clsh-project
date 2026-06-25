---
phase: 6
name: "分发执行"
gate_script: "gate-phase6.py"
output_files: ["tester-report.md"]
---

# Phase 6: 分发执行

## 前置依赖

- Phase 5 的 `tasks.md`（必须存在）

## 执行步骤

**角色：** coder/artist → 执行 | tester → 验证。

### 执行协议（gate-phase6.py 检查）

1. **dispatch 方式**：conversation.md 必须记录派发证据（`delegate_task` 调用 或 `kanban create`）
2. **skill 注入**：派发时必须注入 skills（coder→TDD+incremental, artist→frontend, tester→review+debug）
3. **Level 适配**：Level A 用 kanban/delegate_task，Level B 用 delegate_task，Level C 降级为 WARN
4. **tester 独立验证**：tester-report.md 必须存在且含 PASS/FAIL + 证据

### 子 agent 派发模板路径

- 派发记录模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/dispatch-record-template.md`
- 测试报告模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tester-report-template.md`

### 子 agent toolsets 要求

- coder: `['terminal', 'file', 'code_execution', 'skills', 'todo']`
- tester: `['file', 'browser', 'vision', 'web', 'skills', 'todo']`（**无 terminal**）
- artist: `['browser', 'vision', 'file', 'image_gen', 'skills', 'todo']`

```bash
python3 scripts/gate-phase6.py <项目目录>
```
