---
phase: 6
name: "分发执行（kanban + Bot 直接通知主 Session）"
gate_script: "gate-phase6.py"
output_files: ["tester-report.md", "ledger.md"]
---

# Phase 6: 分发执行（kanban + Bot 直接通知主 Session）

## 前置依赖

- Phase 5 的 `tasks.md`（必须存在）

## 核心机制

> **kanban 派活 → Bot worker 执行 → 完成后直接通知主 session LLM。**
> 
> Worker 通过 API Server 的 `/api/sessions/{id}/chat` 端点注入消息到主 session，
> 主 LLM 收到通知后决定下一步。不经过 kanban 通知系统。

## 执行步骤

**角色：** coder/artist → 执行 | tester → 验证。

### Phase 6.0: 保存主 Session ID

**每次 Phase 6 开始时必须执行：**

```bash
python3 /root/.hermes/scripts/save-main-session-id.py
```

这会将当前主 session ID 写入 `/tmp/hermes-main-session-id`，供 worker 通知使用。

### 执行协议（gate-phase6.py 检查）

1. **dispatch 方式**：必须使用 `kanban create`（Level A 首选）
2. **skill 注入**：派发时必须注入 skills（coder→TDD+incremental, artist→frontend, tester→review+debug）
3. **通知指令注入**：task body 必须包含"完成后通知"指令
4. **tester 独立验证**：tester-report.md 必须存在且含 PASS/FAIL + 证据

### 标准派发流程

```
协调者读 tasks.md
  ↓
保存主 session ID（save-main-session-id.py）
  ↓
创建 project + board（如果不存在）：
  hermes project create "<项目名>" --slug <slug> --primary <项目目录> --board <slug> --use
  hermes kanban boards switch <slug>
  ↓
创建 ledger.md（从模板初始化）
  ↓
对每个任务：
  1. 更新 ledger: Task N: in-progress
  2. 生成 task-N-brief.md（从 tasks.md 提取）
  3. kanban_create(title, assignee, body, skills=[...])
     body 必须包含通知指令（见下方模板）
  4. hermes kanban dispatch --max 1（立即派发，不等 60s tick）
  5. → 等待 worker 通知（自动，无需轮询）
  5. → 主 LLM 收到通知，读取结果
  6. PASS → 更新 ledger: complete → 下一个任务
  7. FAIL → 进入 Fix Loop
```

### Task Body 通知指令模板

**每个 kanban task 的 body 必须包含以下段落：**

```markdown
## 完成后通知
kanban_complete() 后，执行以下命令通知主 session：
python3 /root/.hermes/scripts/notify-main-session.py <task_id> "<summary>"
```

**完整 task body 示例：**

```markdown
## 目标
实现预算编制模块的前端页面

## 关键约束
- Vue3 + Element Plus
- 不修改现有 API

## 验收标准
- [ ] 页面能正常渲染 → 验证: `curl http://localhost:8090/budget`
- [ ] 表单提交成功 → 验证: 检查数据库记录

## 完成后通知
kanban_complete() 后，执行以下命令通知主 session：
python3 /root/.hermes/scripts/notify-main-session.py t_xxxxx "已完成预算编制前端页面"
```

### Worker 侧行为

Worker 完成任务后的标准流程：
1. `kanban_complete(summary="...", metadata={...})`
2. `terminal(command="python3 /root/.hermes/scripts/notify-main-session.py <task_id> '<summary>'")`
3. → 主 session LLM 收到消息 → 继续执行

---

## Superpowers 优化

### P1: 预生成 Review Package

**派 tester 前**，协调者必须先生成 review package：

```bash
bash scripts/gen-review-package.sh <项目目录> [base_ref] [head_ref]
```

**tester 只读 review-package.md，不跑 git 命令。**

### P3: Task Brief 文件化

**派 implementer 前**，协调者从 tasks.md 提取单个任务生成 brief：

模板路径：`templates/task-brief-template.md`

**implementer 只读 task-N-brief.md，不读完整 tasks.md。**

---

## Ledger 进度追踪

Phase 6 开始时，协调者创建 ledger 文件：

模板路径：`templates/ledger-template.md`

### 恢复机制

compaction 后，协调者必须：
1. `read_file ledger.md` — 读取进度
2. 找到第一个非 `complete` 的任务 — 从此处继续
3. 不要重新 dispatch 已完成的任务

---

## Fix Loop 升级机制

| Round | 行为 | 模型 |
|-------|------|------|
| R=1-3 | resume 同一个 implementer | 同原模型 |
| R=4 | fresh implementer（新 context） | 升级一档模型 |
| R=5 | controller 裁决每个 open finding | 最强模型 |

---

## Scoped Re-Review

每次 fix round 结束后，必须运行 scoped re-review。

路径：`templates/re-review-prompt.md`

---

## 子 agent toolsets 要求

- coder: `['terminal', 'file', 'code_execution', 'skills', 'todo']`
- tester: `['file', 'browser', 'vision', 'web', 'skills', 'todo']`（**无 terminal**）
- artist: `['browser', 'vision', 'file', 'image_gen', 'skills', 'todo']`

## 子 agent 派发模板路径

- 派发记录模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/dispatch-record-template.md`
- 测试报告模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tester-report-template.md`
- 任务简报模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/task-brief-template.md`
- Ledger 模板：`templates/ledger-template.md`
- Scoped Re-Review 模板：`templates/re-review-prompt.md`

```bash
python3 scripts/gate-phase6.py <项目目录>
```
