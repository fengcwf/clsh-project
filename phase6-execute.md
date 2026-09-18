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
2. **skill 注入**：派发时必须注入 skills（coder→TDD+incremental+ponytail, artist→frontend+ponytail, tester→review+debug, reviewer→code-review+ponytail-review）
3. **通知指令注入**：task body 必须包含"完成后通知"指令
4. **tester 独立验证**：tester-report.md 必须存在且含 PASS/FAIL + 证据
5. **视觉保真（存在 DESIGN.md 时强制）**：tester 任务必须包含浏览器截图 + vision 工具对比
   `visual/final.png` 定稿图与 DESIGN.md token（色彩/字体/间距/断点），偏差按严重度记 FAIL/Nit
6. **Ponytail 边界规则**（skill 注入配套，见下方小节）：YAGNI 阶梯只对实现方式生效，不对需求本身生效

### Ponytail 边界规则（skill 注入配套）

> ponytail 的 YAGNI 阶梯（"这需要存在吗"）**只对实现方式生效，不对需求本身生效**。
> Phase 1-3 已定稿需求（PRODUCT.md/TECH.md），Phase 6 coder 无权砍需求。

- coder 认为某需求/功能可砍 → ledger 记录 + notify-main-session 提出，**不得自行删除需求范围**
- 需求变更必须回 Phase 1-3 走流程（与 IL-3 对称：协调者不写代码，coder 不改需求）
- ponytail 红线与本流程天然契合：验收标准中的验证/错误处理/安全项不许"懒"，非平凡逻辑必留可运行检查（tester 实测的证据来源）
- ponytail 阶梯前提：先读完任务和受影响代码、端到端 trace 之后再爬阶梯——阶梯缩短方案，永不缩短阅读，防止 ponytail 变成跳步借口
- reviewer 用 ponytail-review 审查过度工程：输出 `L<line>: <tag> <what>. <replacement>.` + `net: -<N> lines possible`，审查发现随 reviewer 报告归档
- Phase 8/长期维护可跑 ponytail-debt：收割代码库 `ponytail:` 注释标记成 ledger，防止"简化项"永久烂尾

### 标准派发流程

```
协调者读 tasks.md
  ↓
保存主 session ID（save-main-session-id.py）
  ↓
读取 .cp-init.json（基础设施已在 init 阶段创建并验证，Phase 6 不再创建）
  hermes kanban boards switch <board>   # board 名来自 .cp-init.json
  ↓
创建 ledger.md（从模板初始化）
  ↓
对每个任务：
  1. 更新 ledger: Task N: in-progress
  2. 生成 task-N-brief.md（从 tasks.md 提取）
  3. kanban_create(title, assignee, body, skills=[...])
     # coder: [test-driven-development, incremental-implementation, ponytail]
     # reviewer: [code-review-and-quality, ponytail-review]
     # artist: [frontend-design, ponytail]
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

## 验证时间预算（防过度验证）

> **流程完成度 > 单点验证深度。** 验证是手段，交付是目的。

- 每个 Task 的验证时间有预算：单 Task 验证不得超过总执行时间的 20%。超出即停止，将"未验证的边界"记入 tester-report.md 的 Known Gaps，继续下一个 Task。
- 禁止的无预算行为：与外部真实服务/二进制做大规模 golden 对比（>10 组）、大文件压测（>10MB）、性能基准测量——除非 tasks.md 的验收标准明确要求。
- 验证优先级：① 验收标准逐条覆盖（必须）→ ② 错误路径冒烟（应做）→ ③ 边界/兼容/性能深测（有预算才做）。
- 判断标准：如果验证活动不能改变某个验收标准的 PASS/FAIL 判定，它就是超预算的。

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

> 所有 profile 已配置 `browser.backend: browser-use`（Playwright 模式），无需单独启用 `web` toolset。
> 所有使用 `coding` 的 profile 已配置 `agent.coding_context: focus`（自动剥离非编码工具）。
> `coding` 工具集（focus 模式）包含：terminal、file、code_execution、vision、browser、web（search/extract）、skills、todo、memory、session_search、clarify、delegate。
> focus 模式自动剥离：image_gen、tts、cronjob、kanban、computer_use、homeassistant。

- coder: `['coding']` — 全套编码工具
- tester: `['file', 'browser', 'vision', 'skills', 'todo', 'code_execution', 'memory', 'session_search', 'clarify']`（**无 terminal，防止修改代码**）
- artist: `['coding', 'image_gen']` — 编码工具 + 图片生成
- scout: `['coding', 'memory', 'session_search']` — 调研 + 记忆
- reviewer: `['coding', 'memory', 'session_search']` — 审查 + 记忆
- worker: `['coding']` — 通用编码工具

## 子 agent 派发模板路径

- 派发记录模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/dispatch-record-template.md`
- 测试报告模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tester-report-template.md`
- 任务简报模板：`/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/task-brief-template.md`
- Ledger 模板：`templates/ledger-template.md`
- Scoped Re-Review 模板：`templates/re-review-prompt.md`

```bash
python3 scripts/gate-phase6.py <项目目录>
```
