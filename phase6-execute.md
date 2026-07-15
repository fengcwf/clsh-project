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

---

## ⚡ Superpowers 6.0 优化（v9.1 新增）

### P1: 预生成 Review Package

**派 tester 前**，协调者必须先生成 review package：

```bash
bash scripts/gen-review-package.sh <项目目录> [base_ref] [head_ref]
```

生成 `<项目目录>/review-package.md`，包含：
- commit list
- files changed summary
- net diff with context（≤500 行截断）

**tester 只读 review-package.md，不跑 git 命令。**

派发 tester 时在 context 中指定：
```
review-package.md 路径: <项目目录>/review-package.md
请基于此文件审查，不要运行 git 命令。
```

### P3: Task Brief 文件化

**派 implementer 前**，协调者从 tasks.md 提取单个任务生成 brief：

模板路径：`templates/task-brief-template.md`

生成 `<项目目录>/task-N-brief.md`，包含：
- 任务信息（标题/角色/技能/依赖）
- 目标描述
- 约束条件
- 验收标准
- 参考文件

**implementer 只读 task-N-brief.md，不读完整 tasks.md。**

派发 implementer 时在 context 中指定：
```
task brief 路径: <项目目录>/task-N-brief.md
请基于此文件执行，不需要读取完整 tasks.md。
```

### 执行流程（优化后）

```
协调者读 tasks.md
  ↓
对每个任务：
  1. 生成 task-N-brief.md（从 tasks.md 提取）
  2. 派 implementer（coder/artist），context 指向 brief
  3. implementer 完成后，生成 review-package.sh（git diff）
  4. 派 tester，context 指向 review-package.md
  5. tester 读 review-package.md，输出结构化 verdict
  6. PASS → 下一个任务 | FAIL → 派 fixer
```

---

## 子 agent 派发模板路径

- 派发记录模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/dispatch-record-template.md`
- 测试报告模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tester-report-template.md`
- 任务简报模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/task-brief-template.md`

## 子 agent toolsets 要求

- coder: `['terminal', 'file', 'code_execution', 'skills', 'todo']`
- tester: `['file', 'browser', 'vision', 'web', 'skills', 'todo']`（**无 terminal**）
- artist: `['browser', 'vision', 'file', 'image_gen', 'skills', 'todo']`

```bash
python3 scripts/gate-phase6.py <项目目录>
```
