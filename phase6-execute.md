---
phase: 6
name: "分发执行"
gate_script: "gate-phase6.py"
output_files: ["tester-report.md", "ledger.md"]
---

# Phase 6: 分发执行

## 前置依赖

- Phase 5 的 `tasks.md`（必须存在）

## 执行步骤

**角色：** coder/artist → 执行 | tester → 验证。

### 执行协议（gate-phase6.py 检查）

1. **dispatch 方式**：conversation.md 必须记录派发证据（`delegate_task` 调用 或 `kanban create`）
2. **skill 注入**：派发时必须注入 skills（coder→TDD+incremental, artist→frontend, tester→review+debug）
3. **Level 适配**：Level A 用 kanban（首选）或 delegate_task，Level B 用 delegate_task，Level C 降级为 WARN
   - ⚠️ **L4 拦截降级**：delegate_task 被 gate-enforcer L4 拦截时（缺少 toolsets），必须改用 `hermes kanban create` 派活，不得自己写代码（IL-3）
4. **kanban 通知订阅**：kanban create 后必须调用 `hermes kanban notify-subscribe <task_id> --platform desktop --chat-id default --delivery-mode notify+wake`，确保任务完成通知回到当前会话
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

---

## 📒 Ledger 进度追踪（v9.2 新增）

> **Superpowers v6.2.0 实证**：没有 ledger 的 controller 在 compaction 后重 dispatch 了已完成的任务序列。

### 初始化

Phase 6 开始时，协调者创建 ledger 文件：

模板路径：`templates/ledger-template.md`

生成 `<项目目录>/ledger.md`，首行格式：
```
# Ledger — plan: <project_name>
```

### 更新规则

协调者在每个任务状态变化时更新 ledger：

```
Task 1: complete (commits a1b2c3d..d4e5f6a, review clean)
Task 2: fix-round-2 (2 findings open)
Task 3: blocked (依赖 Task 2)
```

### 恢复机制

compaction 后，协调者必须：
1. `read_file ledger.md` — 读取进度
2. 找到第一个非 `complete` 的任务 — 从此处继续
3. 不要重新 dispatch 已完成的任务

### 裁决记录

R=5 裁决时，记录到 ledger 的 "Fix 裁决记录" 段。

---

## 🔄 Fix Loop 升级机制（v9.2 新增）

> **Superpowers v6.2.0 实证**："Past the cap, rounds don't converge — the failure is structural."

### 升级阶梯

| Round | 行为 | 模型 |
|-------|------|------|
| R=1-3 | resume 同一个 implementer | 同原模型 |
| R=4 | fresh implementer（新 context） | 升级一档模型 |
| R=5 | controller 裁决每个 open finding | 最强模型 |

### R=1-3: Resume Implementer

tester FAIL 后，协调者：
1. 读取 tester-report.md 的 findings
2. 派发同一个 implementer（或 fresh implementer），附带 findings
3. implementer 修复后，运行 scoped re-review（见下）

### R=4: Fresh Implementer + 模型升级

R=3 仍未通过时：
1. 派发**全新** implementer（新 context，不继承之前的修复历史）
2. 使用更强模型
3. 附带所有历史 findings + 已尝试的修复

### R=5: Controller 裁决

R=4 仍未通过时，协调者**不再派发 implementer**：
1. 逐个审查 open findings
2. 对每个 finding 做出裁决：
   - **adjudicate**：finding 成立，必须修复（升级为 BLOCKED）
   - **park**：finding 不阻塞，记录到 ledger 后继续
   - **escalate**：需要人工介入
3. 裁决记录写入 ledger

### ⛔ 禁止

- 禁止 R>5 仍继续派发 implementer
- 禁止跳过 scoped re-review 直接判定 PASS
- 禁止在同一轮 fix 中修改未被 finding 指出的文件

---

## 🔍 Scoped Re-Review（v9.2 新增）

> **Superpowers v6.2.0 实证**："New findings on untouched code go to the ledger, not the loop."

### 触发时机

每次 fix round 结束后，必须运行 scoped re-review。

### 模板

路径：`templates/re-review-prompt.md`

### 流程

1. 协调者收集：原始 findings + fix diff + 修复文件列表
2. 派发 re-reviewer（可以是 tester 或独立 reviewer）
3. re-reviewer **只检查** fix 是否解决了原始 findings
4. 输出格式：
   ```
   Re-Review Verdict: ALL_ADDRESSED / FINDINGS_OPEN
   - Finding 1: ADDRESSED (evidence: src/foo.py:41)
   - Finding 2: NOT_ADDRESSED (未找到对应变更)
   ```

### 规则

- **禁止审查未修改的文件** — 只看 fix diff
- **禁止提出新 findings** — 新发现记录到 ledger，不进入当前循环
- **禁止扩大审查范围** — 只检查原始 findings 是否解决

---

### 优化后执行流程

```
协调者读 tasks.md
  ↓
创建 ledger.md（从模板初始化）
  ↓
对每个任务：
  1. 更新 ledger: Task N: in-progress
  2. 生成 task-N-brief.md（从 tasks.md 提取）
  3. 派 implementer（coder/artist），context 指向 brief
  4. implementer 完成后，生成 review-package.sh（git diff）
  5. 派 tester，context 指向 review-package.md
  6. tester 读 review-package.md，输出结构化 verdict
  7. PASS → 更新 ledger: complete → 下一个任务
  8. FAIL → 进入 Fix Loop:
     R=1-3: resume implementer + scoped re-review
     R=4: fresh implementer + 模型升级 + scoped re-review
     R=5: controller 裁决 → 记录到 ledger
```

---

## 子 agent 派发模板路径

- 派发记录模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/dispatch-record-template.md`
- 测试报告模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tester-report-template.md`
- 任务简报模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/task-brief-template.md`
- Ledger 模板：`templates/ledger-template.md`
- Scoped Re-Review 模板：`templates/re-review-prompt.md`

## 子 agent toolsets 要求

- coder: `['terminal', 'file', 'code_execution', 'skills', 'todo']`
- tester: `['file', 'browser', 'vision', 'web', 'skills', 'todo']`（**无 terminal**）
- artist: `['browser', 'vision', 'file', 'image_gen', 'skills', 'todo']`

```bash
python3 scripts/gate-phase6.py <项目目录>
```
