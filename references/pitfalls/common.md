# Common Pitfalls — 完整词典

> clsh-project 流程中的常见错误、触发条件、验证方法。
> 各 Phase 高频 pitfalls 已内嵌到对应 workflow 文件末尾，此文件是完整词典。

---

---

> **⚠️ Pitfalls #1-#50 已归档到 `archive/old-pitfalls-1-50.md`**
> 
> 这些早期 pitfall 现已被 Gate (G0-G7) 和 Convention (C0-C8) 规则层覆盖。
> 历史归档保留供参考。

---

## Pitfall #51: 灵犀做代码推理（置信度 0.9，3 次触发）

灵犀是协调者，不是 coder。**正确做法（Way C）：** 灵犀只指定文件路径和问题现象，worker 自己读代码、自己推理根因、自己修复。

## Pitfall #52: worker 修复后跳过 tester 验证（置信度 0.9，2 次触发）

worker 修复后灵犀直接汇报完成，没有让 tester 浏览器验证。修复速度 ≠ 修复质量。

## Pitfall #53: Vue 响应式（略）

## Pitfall #54: Workspace UI 暗色主题（略）

## Pitfall #55: 新增子模块必须先读 AGENTS.md（略）

## Pitfall #56: Kanban worker 写入错误路径（2026-05-27 教训）

worker 可能读取现有文件确定"自然"位置，忽略 constitution 指定的目标路径。task body 中必须显式写明**绝对输出路径**。

## Pitfall #57: worker 首轮输出功能不全 + 二轮补全模式

首轮后 grep 验证关键功能；缺失时二轮用精确 bullet-point 需求补全。

## Pitfall #58: Fastify 双静态根配置

需要同时服务 `src/public/` 和 `src/projects/*/public/` 时，注册两次 fastifyStatic。

## Pitfall #59: CodeWhale 部分编辑导致文件损坏（2026-05-28 教训）

超时时可能已对同一文件做了多次部分 patch，导致括号嵌套错乱。超时后直接 `write_file` 重写整个文件，不要逐行修补。

## Pitfall #60: Vue3 CDN 组件解构完整性

新建组件时，默认解构 `const { ref, computed, watch, onMounted, onUnmounted, h, defineComponent } = Vue;`

## Pitfall #61: 灵犀做代码推理再告诉 worker 怎么改（置信度 0.9，5 轮触发，2026-06-04 再犯）

kanban task body 只给**目标 + 现象 + 文件路径 + 约束 + 验收标准**。❌ 不该给具体代码改动（如"将 z-index 从 10 改为 100"、"添加 download_url: url"）。✅ 该给现象描述（如"播放条遮住了平台下拉框"、"下载 API 返回假成功"）。**2026-06-04 再犯案例：** Round 7 task body 写了"将 .md-search-bar 的 z-index 从 10 改为 100"、"ID 改为 `${item.song_name}_${item.source}_${item.ext}_${item.bitrate}`"。大佬纠正："不是应该给目标和问题coder，让他自己分析操作吗"。**根因：** 灵犀看到"简单 bug"就忍不住给具体修复方案，认为这样更快。但 Way C 的价值在于 worker 自己读代码推理，可能发现更好的方案或更多问题。

## Pitfall #62: API 一致性（略）

## Pitfall #63: Fastify 禁止 execSync（略）

## Pitfall #64: 知识复利（略）

## Pitfall #65: 子 agent 并行写共享文件（略）

## Pitfall #66: Skill 删除连带（略）

## Pitfall #67: 跳过 Phase 3 设计发散直接手写 HTML（2026-05-29 教训）

UI 项目禁止灵犀手写 CSS，必须用 Open Design tokens。

## Pitfall #68: delegate_task 并行覆盖文件（略）

## Pitfall #69: Skill 删除连带 scripts（略）

## Pitfall #70: Phase 1 需求澄清顺序（略）

## Pitfall #71: Phase 8 每轮必须主动记录测试结果（2026-06-03 强化）

每轮 Phase 8 反馈的**第一件事**是写 conversation.md，不需要大佬提醒。文档写入是门禁条件。

## Pitfall #72: Phase 8 禁止灵犀分析根因再告诉 worker

kanban task body 只给现象+文件路径，让 worker 自己分析。

## Pitfall #73: 外部 API 集成必须先查 OpenAPI spec

不要假设端点路径。

## Pitfall #74: GET vs POST handler 不匹配

端到端调试时，第一步验证"请求是否到达了 handler"。

## Pitfall #75: Kanban 评论在任务完成后不生效（2026-06-05 教训）

任务 done 后追加的 `hermes kanban comment` 不会触发 worker 重新执行。需求变更时必须创建新卡或在当前 session 自己修复。 | 验证：检查任务状态是否为 done | 触发：任务完成后需要追加需求

## Pitfall #76: task body 列举太多参考文件导致 worker 迭代耗尽

灵犀先读参考文件 → 写自包含 SPEC 文件 → worker 只读 SPEC。

## Pitfall #77: SQLite Schema 不兼容导致迁移失败

修改表 schema 时，必须检测旧 schema 并处理。

## Pitfall #78: 跳过 Phase 6 tester review 直接上线

代码完成后必须走 tester 验证流程。

## Pitfall #79: fetch credentials（略）

## Pitfall #80: 自构造 URL（略）

## Pitfall #81: 知识复利的关键是注入不是记录

设计重心是"注入机制"，不是"记录机制"。

## Pitfall #82: 路径迁移必须全系统扫描

路径迁移后必须全系统 grep。

## Pitfall #83: Node.js fetch() 在某些网络环境挂起

改用 `http.request()` 替代。

## Pitfall #84: MoviePilot REST vs MCP（略）

## Pitfall #85: 诊断代理问题先确认目标服务（略）

## Pitfall #86: Phase 8 文档规范执行不力（2026-06-03 教训，4 轮）

文档写入是门禁条件，不是"做完再补"。

## Pitfall #87: CodeWhale 声称已修复但实际未改（2026-06-03 教训）

CodeWhale summary 列了 12 项修复，但实际只改了部分代码。返回后必须 `grep -c` 验证关键功能是否实际存在。

## Pitfall #88: 不要分析根因再派 worker（2026-06-03 大佬纠正）

大佬反馈 bug 时，灵犀只做：(1) 记录现象 (2) 指定文件路径 (3) 创建 kanban 卡让 worker 分析。

## Pitfall #89: execFileSync 在循环中对 N 个文件调用 = 性能灾难（2026-06-03 教训）

批量操作禁止在循环中同步启动子进程。改为按需检查或批量脚本。

## Pitfall #90: Kanban 派发 fire-and-forget（2026-06-03 教训）

派发任务后不做追踪，任务完成 ~1.5 小时无人知晓，依赖卡 blocked 无人解除。**铁律：派发 ≠ 结束。** 派发后必须设追踪机制（cron 轮询/session 内等待/notify_on_complete），完成后三件事：(1) 验证产出物 (2) 解除依赖 (3) 通知大佬。详见 Phase 6 "派发后追踪协议"。

## Pitfall #91: Tester 卡迭代预算耗尽（2026-06-03 教训，2026-06-07 再犯）

一个 tester 卡覆盖所有功能，迭代预算耗尽未完成。**大佬原话（2026-06-07）：**"我记得以前让你派活检查需要拆开每个功能点，而不是让一个 tester 检查全部"。**铁律：** tester 卡和 coder 卡一样拆分 — 每卡只验证一个功能点（≤5min，≤30 迭代）。5 个验证点 → 5 张 tester 卡。一个卡卡住 = 全部卡住。详见 Phase 6 "Tester 卡优化"。

## Pitfall #92: Tester 完成无 summary 无通知（2026-06-04 教训）

tester 卡标记 done 但 summary 为空，灵犀不知情。**根因：** task body 没要求写 summary → worker 认为"验证通过就完事了"。**规则：** (1) task body 必须要求 worker 在 kanban_complete 时写 summary（验证了什么、结果、截图路径）(2) 灵犀必须主动轮询 kanban 状态，不能等通知 (3) 完成后必须自己跑 5 步验证，不信任 worker 的 summary。

## Pitfall #93: Way C 连续违规 — 灵犀忍不住给具体修复方案（2026-06-04 教训，同一 session 两次）

Round 6 灵犀直接改代码（角色分离违规），Round 7 task body 写了具体代码改动（Way C 违规）。**根因相同：** 看到"简单 bug"就认为"给具体方案更快"。**大佬两次纠正：** "修复是不是没有派活，都是你自己干了" + "不是应该给目标和问题coder，让他自己分析操作吗"。**铁律：** 无论改动多小，task body 只给现象+文件路径。worker 自己读代码的价值 > 节省的 30 秒。

## Pitfall #94: Kanban create 后忘记 notify-subscribe（2026-06-04 教训）

create 后没有调 notify-subscribe，kanban_notify_subs 表为空 → worker 完成无通知 → 灵犀不知情。**铁律：** 每次 kanban create 后必须立即 `hermes kanban notify-subscribe <task_id> --platform feishu --chat-id oc_22cb909a35e6a74c62cc0d4d170b19c3`。已写入 phase6-execution.md Step 3.2。与 #77 区别：#77 是不追踪状态；#81 是技术层没建通知订阅。

## Pitfall #95: Worker kanban_complete 不写 summary

task_runs 有详细结果但 tasks.result 为空。**规则：** task body 必须要求 `kanban_complete(summary=...")`；灵犀必须主动查 task_runs 或 poll 状态，不能只依赖通知。

## Pitfall #96: 先问用户再查 skill/memory（2026-06-04 教训）

大佬说"代理信息应该在 clsh-project 里有记载，为什么需要问我"。代理 `192.168.0.41:7890` 已记录在 `proxy-workarounds` skill 中，但灵犀没查就问用户。**铁律：** 查找优先级 = (1) 查相关 skill → (2) 查 memory → (3) 查 wiki/Obsidian → (4) 最后才问用户。用户已提供的信息不应重复询问。**触发信号：** 需要环境配置、凭据、端口、路径等信息时。**Workspace 凭据速查：** admin / clsh666.（末尾有句号），详见 #86。

## Pitfall #97: 跳过 tester 验证直接派 coder（2026-06-07）

- **场景：** 工业区迁移直接派 coder，没先派 tester 验证旧模块结构
- **根因：** "调研阶段已经读过代码" 不等于 "独立 tester 验证过"
- **正确流程：** Phase 6 Wave 0 先派 tester 验证（确认旧模块结构+新工作台架构），再派 coder

## Pitfall #98: Phase 8 tester 超时 → 灵犀直接验证（2026-06-08）

**触发条件：** Phase 8 UI 修复后派 tester kanban 卡做浏览器验证，tester 连续 timeout（迭代预算 90/90 耗尽）。

**根因：** 浏览器自动化（登录→导航→截图→分析）每步消耗迭代，多验证点任务容易超限。

**规则：** Phase 8 UI 验证优先级：
1. **灵犀直接验证**（推荐）— 自己做 `node -c` 语法检查 + 浏览器登录 + `browser_vision` 截图 + DOM 检查
2. **拆分 tester 卡** — 每卡 ≤2 个验证点
3. **语法检查先行** — `node -c` 排除明显错误再做浏览器验证

**铁律：** 不依赖 tester kanban 卡做完整浏览器验证。tester 适合代码 review，不适合多步骤浏览器交互。

## Pitfall #99: 代码修改后必须重启服务再验证（2026-06-08）

**触发条件：** coder 报告修复完成，灵犀直接浏览器验证发现功能不工作。

**根因：** pm2 进程还在运行旧代码。Node.js ESM 模块有缓存，修改文件后不重启 = 新代码不生效。

**规则：** coder 完成代码修改 → 灵犀验证前**必须先重启服务**（`pm2 restart workspace`）→ 再做浏览器验证。跳过重启 = 验证无效。
- **教训：** delegate_task 的结论是 self-reported，需要独立 tester 验证

## Pitfall #100: Coder 声称"已在之前实现"但功能不工作（2026-06-08 教训）

**场景：** Phase 8 BUG-4 右键菜单修复任务，coder 完成后 summary 写"已在之前的实现中完整完成，验证所有 6 条验收标准全部通过"。灵犀浏览器验证发现右键菜单根本不弹出。

**根因：** ContextMenu 组件代码存在（defineComponent + 渲染逻辑 + CSS），但 `onMounted` 中事件监听器添加失败（gridEl.value 为 null）。Coder 只检查了"代码是否存在"，没有检查"运行时是否工作"。

**与 #74 的区别：** #74 是 CodeWhale summary 列了多项修复但实际只改了部分代码（声称修复但未改）。#111 是代码确实存在，但运行时有 bug 导致不工作（声称实现但有缺陷）。

**铁律：** Coder 声称"已实现/已修复/已有功能"时，灵犀必须独立验证（浏览器截图 + 实际交互），不信任 coder 的 self-report。验证步骤：
1. `node -c` 语法检查
2. `grep` 确认关键代码路径存在
3. 浏览器实际操作验证功能是否工作（不是只看代码是否存在）
4. 如果 tester 已 blocked/gave_up，灵犀自己用 browser 工具验证（降级策略 3，见 #110）

**触发信号：** Coder summary 包含"已在之前实现""完整完成""所有验收标准通过"但没有附带浏览器截图或 curl 输出等客观证据。

## Pitfall #101: pm2 重启后才能看到代码变更（2026-06-08 教训）

**场景：** Coder 修改了 app.mjs 和 style.css，灵犀第一次浏览器验证右键菜单失败，直到 `pm2 restart workspace` 后才看到新代码。

**规则：** pm2 管理的 Node.js 服务，server 端代码（routes、plugins、middleware）变更后必须 `pm2 restart <app>` 生效。纯前端静态文件（app.mjs、style.css）由 fastify-static 从磁盘实时读取，理论上不需要重启，但安全做法：一律重启。

**铁律：** Coder 完成代码修改后，灵犀浏览器验证前必须先 `pm2 restart <app>`。在 Phase 8 降级验证流程（#110）中，pm2 restart 是第 0 步（在 browser_navigate 之前）。

---

### 分类: Kanban 运维

## Pitfall #102: Kanban task body 含反引号导致 shell 解析失败（2026-06-08 教训）

**场景：** `hermes kanban create` 的 `--body` 参数包含反引号（代码块标记），shell 将反引号内的内容当作命令执行，导致 `eval: 行 83: 寻找匹配的 ``' 时遇到了未预期的 EOF`。

**根因：** bash 将反引号 `` ` `` 解释为命令替换（command substitution），`--body "## code: python3 `import re`"` 中的 `` `import re` `` 被 shell 尝试执行。

**修复方案：** 将 task body 写入临时文件，用 `$(cat /tmp/body.md)` 传递：
```bash
# ✅ 正确：body 写文件后读取
cat > /tmp/task-body.md << 'BODYEOF'
## Task
代码块标记：反引号x3
BODYEOF
hermes kanban create "title" --assignee coder --body "$(cat /tmp/task-body.md)" --json

# ❌ 错误：body 直接内联（反引号会触发 shell 解析）
hermes kanban create "title" --assignee coder --body "## Task: 用反引号`code`标记" --json
```

**触发条件：** task body 中包含反引号（` `）、美元符号（$）、感叹号（!）等 shell 特殊字符。

**教训：** 复杂的 kanban task body（含代码示例、技术术语）一律先写文件再读取，不要直接内联到 shell 命令中。

## Pitfall #103: Profile toolset 缺失导致 worker 静默失败（2026-06-07 教训）

tester/worker profile 的 `config.yaml` 中 `toolsets` 缺少必要工具时，worker 启动后 60s 内退出，kanban 报 `protocol violation`（rc=0 但没调 kanban_complete）。**实测案例：** tester 缺少 `browser` + `vision` → 连续 4 个浏览器验证任务全部 1 分钟 crash。**排查路径：** protocol violation → 对比能正常工作的 profile 的 toolsets。**铁律：** 派发前验证 assignee profile 的 toolsets。UI 验证 → `browser` + `vision`；代码 → `terminal` + `file`。详见 `references/pitfalls/kanban-ops-lessons.md`。

## Pitfall #104: Kanban watchdog 脚本参数错误（2026-06-07 教训）

`hermes kanban list --status in_progress` 无效（状态名是 `running`）；`hermes cronjob` 不存在（正确命令 `hermes cron`）。两个 bug 导致 watchdog 静默退出。详见 `references/pitfalls/kanban-ops-lessons.md`。

## Pitfall #105: 凭据写入 task body 后必须 curl 验证（2026-06-07 教训）

Workspace 密码 `clsh666.`（末尾有句号），写入 kanban 评论时漏掉句号 → 3 个 tester 全部认证失败。**铁律：** 凭据写入 task body 后用 curl 验证一次。

## Pitfall #106: MiMo API 429 限流 — 并行派发秒炸（2026-06-07 教训）

4 个 tester 并行 dispatch → 4 个 MiMo API key 同时请求 → 全部 429 → `max_retries_exhausted` → 60s 内 crash（protocol violation）。**现象：** PID alive 但心跳 3+分钟停止，request dump 中 `429 Too many requests`。**铁律：** MiMo API 环境下**串行派发**（`dispatch --max 1`），间隔 ≥90s。**排查路径：** heartbeat 停止 → ps 确认 → 查 request dump → 429 → kill → archive → 串行重试。**正例：** 串行 2 张 10 分钟内 PASS。

## Pitfall #107: 浏览器截图验证耗尽 API 迭代预算（2026-06-07 教训）

tester 做浏览器登录+screenshot+vision 分析，单任务消耗大量 API 调用，叠加并行 = 立刻 429。**规则：** (1) UI 验证优先用代码检查（grep/node --check）替代浏览器截图 (2) 必须浏览器验证时，串行 dispatch 一张一张来 (3) task body 明确告诉 tester 可用命令行替代浏览器。

## Pitfall #108: `hermes cron resume` 对不存在的 cron 静默成功（2026-06-07 教训）

`hermes cron resume 1d04104d3ca9` 报 "Resumed job: kanban-watchdog" 但该 cron 从未存在。后续 `hermes cron show` 返回 exit code 2（not found）。**铁律：** resume/create cron 后必须 `hermes cron list` 验证实际存在。参考 ID 不可信，必须从 list 输出中确认。

## Pitfall #109: `notify-subscribe` 发送文件内容而非文本摘要（2026-06-07 教训）

kanban 任务完成后，notify-subscribe 通知机制把 coder 修改的文件内容（如 index.html）作为通知发送给用户。**根因：** 通知系统将 task result 中的文件变更作为附件发送。**规避：** 用 no_agent cron watchdog 脚本输出纯文本摘要，不依赖 notify-subscribe 的默认行为。

## Pitfall #110: CDN 库 API 版本不兼容（2026-06-07 教训）

`marked` CDN 加载后 `marked(text)` 报 "marked is not a function"，因为 marked v5+ 顶层 API 改为 `marked.parse(text)`。**铁律：** 添加 CDN 库后必须在浏览器控制台验证 API 调用方式，不能假设 API 与旧版一致。coder 自己分析此类问题，灵犀不替 coder 判断根因。

## Pitfall #111: Kanban scratch workspace 产出文件丢失（2026-06-07 教训）

kanban scratch workspace（`/root/.hermes/kanban/workspaces/<task_id>/`）是临时目录，任务完成后清理。worker 写入 scratch 的代码文件不会持久化到实际项目目录。**实测：** 12 个代码生成任务用 kanban 派发 → worker 成功完成 → scratch 清理 → 文件不存在。**铁律：** 产出持久文件的任务（代码生成、新建文件）用 `delegate_task`（子 agent 直接写项目目录）。kanban 只用于无文件产出的任务（测试验证、纯推理）或修改现有文件。详见 `references/pitfalls/kanban-ops-lessons.md` §4。

## Pitfall #112: `max_in_progress_per_profile` 需要 gateway restart（2026-06-07 教训）

`dispatch_in_gateway: true` → kanban daemon 运行在 gateway 进程内 → config 变更需要 restart 生效。**现象：** 设置 `max_in_progress_per_profile: 1` 后 daemon 仍并行派发。**铁律：** 修改 kanban config 后必须 `hermes gateway restart`（从外部 shell，内部会报 `Refusing to restart`）。详见 `references/pitfalls/kanban-ops-lessons.md` §5。

## Pitfall #113: Kanban 并发打爆 API（2026-06-07）

- **场景：** 12 个工业区任务同时派发给 coder，全部打爆 MiMo 429
- **根因：** `max_in_progress_per_profile: null`（无限制）+ `auto_decompose_per_tick: 3`（每 tick 3 个）+ gateway 未重启导致配置未生效
- **症状：** 所有任务 blocked（protocol violation — worker 429 后退出没调 kanban_complete）
- **修复：** `max_in_progress_per_profile: 1` + `auto_decompose_per_tick: 1` + `dispatch_stale_timeout_seconds: 600`
- **教训：** 任务必须顺序派发，不能并行。配置修改后必须重启 gateway。
- **验证：** `hermes config get kanban.max_in_progress_per_profile` 应返回 1

## Pitfall #114: Watchdog 不检测 blocked 任务（2026-06-07）

- **场景：** 12 个任务全部 blocked，watchdog 看不到（只监控 running/ready），自暂停
- **根因：** watchdog 只检查 running 和 ready 状态，不检查 blocked
- **修复：** watchdog v2 新增 blocked 检测 + 自动 unblock 重试（最多 2 次）
- **教训：** watchdog 必须覆盖所有活跃状态（running + ready + blocked）

## Pitfall #115: `hermes kanban show --json` 不输出干净 JSON（2026-06-08 教训）

- **场景：** E2E 测试脚本用 `hermes kanban show <id> --json` 获取任务状态，`json.loads()` 解析失败返回 None
- **根因：** CLI 的 `--json` 标志对 `show` 子命令不产生干净 JSON 输出（混合文本+JSON）
- **症状：** `kanban_show()` 返回 None → 脚本误判任务状态为 "unknown"
- **修复：** 用 regex 解析文本输出（`hermes kanban show <id>` 不带 `--json`）：`re.search(r'status:\s+(.+)', out)`
- **验证：** `hermes kanban show t_xxx 2>&1 | grep "status:"` 应返回状态
- **铁律：** 脚本中获取 kanban 任务状态时，用文本解析替代 JSON 解析

## Pitfall #116: Watchdog spec 与实现差距（2026-06-08 教训）

- **场景：** delegation-protocol 描述 watchdog v2 有 5 项功能（完成检测/超时告警/blocked 检测/自动暂停/状态持久化），实际脚本只实现 1 项
- **根因：** spec 在 2026-06-07 更新了 v2 功能描述，但脚本没有同步更新
- **修复：** 升级 watchdog v2（6/6 功能），设计决策"永远 active + 空闲静默"（不自动暂停，避免 LLM 依赖 resume）
- **验证：** `python3 ~/.hermes/scripts/clsh-e2e-watchdog-test.py` 应 14/15 PASS（唯一 FAIL 是 pitfall #91 上游问题）
- **铁律：** spec 更新后必须同步更新实现 + E2E 测试验证

## Pitfall #117: AGENTS.md 对 kanban worker 无效（2026-06-08 教训）

**问题：** 在 `~/.hermes/profiles/<name>/AGENTS.md` 写了 Context Engineering 规则，以为 kanban worker 会读取。实际上 worker 的 cwd 是 kanban workspace 目录（`/root/.hermes/kanban/workspaces/<task_id>/`），不是 profile 目录。AGENTS.md 加载逻辑是 `cwd / "AGENTS.md"` 向上遍历到 git root，profile 目录不在这个路径上。

**根因：** `_default_spawn()` 设置 `cwd=workspace`（kanban_db.py:6765），worker 子进程的 cwd 在 workspace，不在 profile home。

**正确注入路径：**
- **SOUL.md**（profile home）→ 始终加载（`get_hermes_home() / "SOUL.md"`）
- **task body** → 灵犀控制的 Context Engineering 五层架构
- **--skills** → kanban 自动预加载 `kanban-worker` + task.skills

**规则：** Worker 的"始终加载"规则放 SOUL.md，不放 AGENTS.md。

## Pitfall #118: Tester 浏览器验证迭代预算耗尽 — 降级策略（2026-06-08 教训）

**场景：** Phase 8 tester 任务要求浏览器登录 + 截图 + vision 分析验证 UI 修复。Run #159 耗尽 90/90 迭代后 timeout，自动重试 Run #160 再次耗尽 90/90，最终 `gave_up`（blocked）。

**根因：** 浏览器验证链路长（navigate → type credentials → click → wait → screenshot → vision analyze），单次验证消耗 15-20 迭代。3 个验证点 × 20 迭代 = 60，加上登录和页面加载 ≈ 90，刚好耗尽预算。

**与 #88 的区别：** #88 是并行派发导致 429 限流；#110 是单个 tester 任务自身迭代预算不足。

**降级策略（按优先级）：**
1. **代码级验证**（灵犀可自己做）：`node -c` 语法检查 + `grep` 关键修复点确认代码已落地
2. **拆分 tester 卡**（每卡 1 个验证点，≤30 迭代）：3 个验证点 → 3 张 tester 卡
3. **灵犀手动浏览器截图**（需登录凭据）：灵犀自己 browser_navigate + browser_vision，不走 kanban

**铁律：** tester 任务含浏览器验证时，task body 必须限制验证点数量（≤2 个/卡）。超过 2 个验证点 → 拆分。已知迭代预算 = 90，每个浏览器验证点 ≈ 20 迭代，安全上限 = 4 个验证点（留 10 迭代余量给登录）。

**本次处理（2026-06-08 实测）：** tester 两次 gave_up 后，灵犀执行降级策略 1+3：代码检查确认 3 个修复已落地（SearchCardInner 内联 SVG、.grid-stack-item-content 统一样式、dc-toolbar z-index:2），`node -c` 语法通过。然后灵犀自己用 browser_navigate + browser_type（密码 clsh666.，见 #86）+ browser_click + browser_vision 完成浏览器截图验证。总计 <5 分钟，比重新派 tester 快 10x。

**灵犀手动浏览器验证模式（fallback 优先级最高）：**
当 tester kanban 任务 blocked/gave_up 且验证点 ≤3 个时，灵犀直接用 browser 工具验证：
1. `browser_navigate` → 登录页
2. `browser_type` → 输入凭据（Workspace 密码见 #86：`clsh666.`）
3. `browser_click` → 登录
4. `browser_vision` → 截图验证每个修复点
5. 完成后 `hermes kanban complete <tester_id> --result "灵犀手动验证通过"`

**优势：** 无需等 kanban daemon 调度、无迭代预算限制、可精确控制验证步骤。
**限制：** 需要知道登录凭据（查 #86 或 memory）、验证点 ≤3 个（否则耗时过长）。

**⚠️ `node -c` 不适用于 CSS 文件（2026-06-08 教训）** — `node -c`（`--check`）只能检查 JavaScript 语法，对 .css 文件报 `ERR_UNKNOWN_FILE_EXTENSION`。Acceptance Criteria 中不应包含 `node -c *.css`。CSS 验证方式：(1) 浏览器渲染截图 (2) grep 检查关键属性是否存在。

---

### 分类: E2E 与机械门禁（2026-06-09）

## Pitfall #119: phase4-mechanical-check.py 路径尾部斜杠（2026-06-09）

运行 `phase4-mechanical-check.py` 时项目目录**不能带尾部 `/`**。带 `/` 导致 `glob.glob` 匹配失败，所有文件显示不存在 → 误判 FAIL。
```
❌ python3 phase4-mechanical-check.py /path/to/project/
✅ python3 phase4-mechanical-check.py /path/to/project
```

## Pitfall #120: constitution.md 需要"实现细节规范"节（2026-06-09）

`phase4-mechanical-check.py` 会检查 constitution.md 是否包含 `## 实现细节规范` 节标题，且内容需覆盖编码规范（utf-8/encoding）和错误处理规范（异常/错误响应）。只写技术栈+约束+禁止+验收 → FAIL。

## Pitfall #121: proposal.md "技术方案"需在标题中（2026-06-09）

proposal.md 的 `# 标题` 必须包含"技术方案"（如 `# XXX 技术方案`），不能只在正文出现。机械检查对标题和正文都做子串匹配，但标题命中更可靠。

## Pitfall #122: Phase 0-1 调研门禁（2026-06-09 E2E 漂移检测发现）

conversation.md 必须包含三个结构化调研节：`## 调研发现`（行业实践）、`## 技术选型`（方案对比）、`## 质量规格`（安全/性能/可靠性/可观测性）。只复述需求就确认 = 流程违规。**根因链：** Phase 0-1 没调研 → constitution 缺质量规格 → 代码缺质量实现。调研门禁是最高 ROI 的修复——改一处，下游全部受益。

## Pitfall #123: constitution 必须有质量规格节（2026-06-09 E2E 漂移检测发现）

constitution.md 必须有安全/性能/可靠性/可观测性四个维度的质量规格。这些规格从 Phase 0-1 的"质量规格"节提取，不是凭空填写。constitution-template.md 已加入质量规格占位模板。

## Pitfall #124: Phase 6 task body 必须注入 constitution 质量约束（2026-06-09 E2E 漂移检测发现）

Phase 6 派发 task 时，body 必须注入 constitution 的"质量规格"节（安全/性能/可靠性/可观测性）。coder 只看 body，不读 wiki 文档。不注入 = 质量规格在传递链中丢失 = 流程违规。

## Pitfall #125: "测试 X" 可能是新项目需求，不是操作指令（2026-06-09）

用户说"测试 clsh-project 购物车结算页，需求：商品列表+购物车+结算按钮+满减券+库存扣减"时，"测试"是项目类型（测试项目），不是"去测试现有代码"。**判断标准：** 如果消息包含"需求："后跟功能列表 → 这是新项目需求，走完整 Phase 1-7。**反例：** "帮我测试一下 XX 功能"、"跑一遍测试" → 才是测试现有代码。误判 = 浪费一个来回澄清。

## Pitfall #126: kanban task body 引用图片导致 vision_analyze 超时（2026-06-09）

task body 引用图片路径 → worker 调 `vision_analyze` → MiMo API 34 分钟超时 → 任务卡死。根因：coder/artist profile 的 toolsets 包含 `vision`，agent 看到图片路径就自动分析。**修复：** coder profile 不需要 vision，已移除。artist profile 保留但 task body 禁止写图片路径。**铁律：** task body 不引用任何图片文件路径，设计规范用精确 CSS 值或文字描述。

## Pitfall #127: Phase 8 spec 设计假设错误（2026-06-09）

Round 3 spec 假设用工作台标准浅色主题 `var(--surface-solid)`，用户实际要暗色毛玻璃 `rgba(25,25,25,0.65)`。根因：灵犀看到"卡片背景不统一"就假设用默认样式，没有向用户确认设计方向。**铁律：** 设计决策分流——有明确指令写精确值，有参考图提取数值，无指令无图→停下来问用户。详见 `references/templates/phase8-feedback-template.md`。

## Pitfall #128: Phase 8 spec 不列浏览器验证步骤（2026-06-09）

Round 3 spec 描述了 WHAT（ContextMenu 组件）但没要求"写完在浏览器里右键验证"。coder 按 spec 写了代码但 addEventListener 时机不对，没在浏览器里验证就标记完成。**铁律：** 每个 UI bug 的 spec 必须包含"浏览器验证步骤"（打开→操作→截图→对比）。无验证步骤 = spec 不合格。

## Pitfall #129: UI 任务派给 coder 而不是 artist（2026-06-09）

R4-4（卡片 UI 重设计）应派给 artist（加载 taste-skill），错派给 coder。根因：灵犀创建 kanban 任务时没按角色分配规则检查。**铁律：** UI/CSS/样式 → artist，代码逻辑 → coder。详见 `references/templates/phase8-feedback-template.md` 角色分配规则表。

## Pitfall #130: Phase 4 机械检查 tasks.md 时序陷阱（2026-06-09）

`phase4-mechanical-check.py` 会检查 tasks.md 是否存在，但 tasks.md 在 Phase 5 才创建。因此：
- Phase 4 结束时运行机械检查 → tasks.md 必定 FAIL（预期行为）
- 正确做法：Phase 5 完成 tasks.md 后再运行完整机械检查
- E2E 测试模式下，可在 Phase 5 后一次性验证全部 5 个文档

## Pitfall #131: E2E 测试模式（无大佬确认）（2026-06-09）

当 clsh-project 用于 E2E 测试或演示时（无真实大佬参与），可跳过确认门禁：
- Phase 1-4 的确认码门禁 → 跳过（需求已完整提供）
- Phase 6 的 delegate_task 派发 → 若工具不可用，灵犀可直接写代码（记录为角色分离违规）
- Phase 7 归档 → 正常执行
- **必须在 overview.md 或 retrospective.md 中标注"E2E 测试模式"**

**规则：** 飞书卡片中分割线一律用 `{"tag": "hr"}`，不用 `divider`。

### 分类: 机械执行器（2026-06-09 审计）

## Pitfall #137: Gate 规则无脚本 = LLM 自觉（2026-06-09）

**场景：** 铁律三层重构后，8 个 Gate 中只有 G2/G3/G4 有脚本。G5/G7 写了规则但无脚本执行，靠 LLM 自觉。结果：灵犀跳过 G7 5 步验证→用 worker 声明替代实际验证→大佬测试发现没修好。

**规则：** Gate 层规则必须有脚本。新增 Gate 规则时，先写脚本再写规则。脚本不存在 = 规则不存在。

## Pitfall #138: Security Scan 由灵犀执行 = 角色越界（2026-06-09）

**场景：** phase6-execution.md 写"灵犀在 checkpoint 后集中审查"。安全扫描本质上是代码分析，违反铁律 2。

**规则：** 灵犀不做任何需要读代码的审查。安全扫描、代码质量、性能分析全部由 tester 做。

## Pitfall #139: 确认码格式存在于多文件（2026-06-09）

**规则：** 飞书卡片中分割线一律用 `{"tag": "hr"}`，不用 `divider`。已升级）。phase8-feedback 两份文件被误判为新旧版本，实际内容完全不同。

**铁律：** 报告中所有行数/版本号必须在写入前重新验证（`wc -l` + `grep version`）。同名文件必须 `diff` 比较内容，不能只看修改时间。

**详细方法论：** `references/skill-audit-methodology.md`

## Pitfall #138: SKILL.md 瘦身后未验证行数（2026-06-09）

**铁律：** 每次 SKILL.md 编辑后必须 `wc -l` 验证 ≤ 350。超限 = 需要继续瘦身。

## Pitfall #139: Gate 规则无脚本 = LLM 自觉（2026-06-09 审计）

**规则：** Gate 层规则必须有脚本。新增 Gate 规则时，先写脚本再写规则。脚本不存在 = 规则不存在。

## Pitfall #140: Security Scan 由灵犀执行 = 角色越界（2026-06-09 审计）

**规则：** 灵犀不做任何需要读代码的审查。安全扫描、代码质量、性能分析全部由 tester 做。

## Pitfall #141: 确认码格式存在于多文件（2026-06-09 审计）

**规则：** 确认码格式变更时，必须全局 grep 所有引用点。
