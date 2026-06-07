# Common Pitfalls — 完整词典

> clsh-project 流程中的常见错误、触发条件、验证方法。
> 各 Phase 高频 pitfalls 已内嵌到对应 workflow 文件末尾，此文件是完整词典。

---

## Pitfall #87: 确认模板未加载（LLM 记忆依赖）

**触发条件：** Phase 结束输出确认请求时，SKILL.md 有铁律 #18 的文字但 LLM 没有加载 `phase-confirmation-template.md`

**根因：** 铁律 #18 写"必须使用模板"，但触发加载模板这一步依赖 LLM 自觉。LLM 加载了 SKILL.md（含规则文字）就认为"已知道规则"，没有实际加载模板文件。这违反了 LLM 能力无关性原则。

**解决方案（2026-06-07 确立）：** 模板内嵌到 SKILL.md 各 Phase 节中（方案 B）。LLM 加载 SKILL.md 时自动看到模板内容，不需要额外加载步骤。

**验证方法：** 检查 SKILL.md 各 Phase 节是否有内嵌的确认模板（含 `[CODE]` 占位符）

**教训：** "写了规则" ≠ "规则会被执行"。如果规则的执行依赖 LLM 记忆触发，就必须把触发条件变成机械的（内嵌到加载路径中）。
## 角色分离（铁律，置信度 0.9）

1. **禁止灵犀直接写代码** — 即使"很快能做完"也必须派 agent | 验证：检查是否有灵犀的 write_file/patch 操作 | 触发：任何代码修改任务
2. **禁止 Phase 8 "顺手修了"** — 大佬反馈问题必须走完整反馈循环 | 验证：检查 Phase 8 是否有 conversation.md + diagnosis.md | 触发：大佬说"这个有问题"/"帮我改"
3. **角色分离违规** — worker 卡住时不能自己动手，创建 fix 卡或 escalate | 验证：检查灵犀是否在 worker blocked 后直接写代码 | 触发：worker kanban_block
4. **Phase 8 必须走角色分离** — 小修复用 kanban（非 delegate_task），大修复更要用 kanban | 验证：检查 Phase 8 是否用了 delegate_task 替代 kanban | 触发：Phase 8 修复任务
5. **delegate_task 不是 kanban 的替代品（2026-05-24 教训）。** 用户要求走 kanban 时，不得用 `delegate_task` 替代。**判断规则：** clsh-project 流程或用户明确要求 kanban → 必须用 kanban。只有纯推理子任务（代码审查、调试分析、对比）才用 delegate_task。 | 验证：检查用户是否明确要求 kanban | 触发：用户说"用 kanban"/"走流程"

## 流程完整性（置信度 0.5-0.7）

6. **方向变化不回 Phase 1** — 核心定位变化必须回 Phase 1，不能回 Phase 3
7. **跳过 Phase 2.5 Spike** — 有技术不确定性的方案必须先验证
8. **Phase 5 缺少 Self-Review** — tasks.md 写完后必须 4 项自检
9. **Phase 6 不做 Spec-Code 同步** — 每个 Task 完成后更新 proposal.md
10. **Phase 7 归档不完整** — 必须检查 overview.md + completion-summary + retrospective + Phase 8 归档
55. **UI 设计跳过 Open Design 知识包加载（2026-05-29 教训）** — Phase 3 设计发散必须先读取 `/opt/open-design/design-systems/<name>/tokens.css` + `DESIGN.md` + `craft/*.md`，再渲染变体。直接手写 HTML = 跳步 = 效果差 = 返工。详见 `references/pitfalls/ui-design-open-design-enforcement.md` | 验证：检查 HTML 模板是否引用了 tokens.css 的变量 | 触发：任何 UI 项目 Phase 3

## 质量保障（置信度 0.5-0.9）

11. **agent 自判完成（置信度 0.9）** — 必须通过 CHECKPOINT 客观验证 | 验证：检查 checkpoint 是否有客观证据（exit code/截图/ls 输出）| 触发：agent 说"已完成"/"done"/"fixed"
12. **Auto-Fix 无限循环** — 2 轮后必须 escalate 给大佬
13. **Placeholder 污染 tasks.md** — TBD/TODO/similar to N = 计划缺陷
14. **写入文件后不验证路径** — write_file 后必须 `ls` 确认
15. **UI 项目跳过 Browser QA（置信度 0.9）** — tester 必须用浏览器截图验证 | 验证：检查 tester 是否有浏览器工具调用记录 | 触发：任何有 UI 的项目
16. **Pre-Commit 自检缺失** — agent context 必须包含安全自检清单，不依赖 agent 自觉
17. **设计发散跳过** — UI 项目且无明确设计参考时，Phase 3 应触发设计发散，不能直接画页面
18. **飞书发送 HTML 文件路径** — 飞书无法打开 HTML 文件。必须用 chromium-browser 截图后发送 PNG 图片（MEDIA: 前缀）
19. **chromium 截图路径 /tmp** — snap 版 chromium 受 AppArmor 限制，无法写入 /tmp。截图路径用 /root/mockups/ 等非受限目录
20. **AGENTS.md 参考其他项目** — AGENTS.md 应基于本项目自身架构（architecture.md），不能照搬其他项目的文档结构

## 执行纪律

21. **超时后提交半成品** — 子 agent 超时后 git stash/revert
22. **Phase 8 上下文溢出** — 每轮最多修 3-4 个 bug，用 execute_code 批量读代码
23. **Bugfix Spec 不列出调用点** — Spec 说"修复 X 功能"但没列出所有函数/端点 → coder 只修一处漏其他。**正例：** Spec 列出 `createShare()`, `listShares()`, `findShareByPath()` 三个函数都需要传 baseUrl → coder 全部改完。**反例：** Spec 只说"修复 URL"→ coder 改了 createShare，漏了 listShares
24. **Fastify 获取端口用 req.server.config.port** — Fastify 没有这个属性。正确方式：`req.headers.host`（包含 host:port）或 `req.hostname`（仅 host）
25. **代码分散在多个目录（2026-05-24 教训，2026-05-25 强化）** — 集成项目代码应集中在项目文件夹（如 `/opt/Workspace/src/projects/obsidian/`），不要分散在旧目录。**前端组件同理：** agent 修改代码时可能在 `src/public/views/` 和 `src/projects/<项目>/public/` 各留一份。**判断哪个是活跃副本：** 查 `app.mjs` 的 import 路径。清理时删孤儿副本，import 路径指向项目目录。
26. **UI 状态管理条件判断错误（2026-05-24 教训）** — 条件判断导致元素一闪而过。**修复：** 分离"显示条件"和"操作条件"
27. **通过 agent CLI 间接调自己** — Open Design 的 agent 调 hermes CLI = 冗余。直接读设计系统 tokens.css 渲染 HTML 即可
28. **等外部 API 生成效果图** — Stitch API 长 prompt 通过代理容易超时。用 Open Design tokens 本地渲染更快更稳定
29. **CSS backdrop-filter 创建 containing block（2026-05-25 教训）** — `backdrop-filter: blur()` 根据 CSS 规范创建新 containing block，导致 `position: fixed` 子元素相对该元素而非视口。修复：移除 backdrop-filter，改用 `background: rgba()`。详见 `code-principles` skill 的 `references/css-pitfalls.md`。
30. **清理重复文件前验证引用（2026-05-25 教训）** — 移动文件后删除旧副本前，必须验证没有 import/引用指向旧路径。
31. **调研报告写入 raw/projects/（2026-05-25 教训，第 3 次）** — 分析报告 → `wiki/syntheses/`。只有有 Phase 流程的项目才进 `raw/projects/`。
32. **frontmatter 版本号不更新** — 每次 patch SKILL.md 必须同步更新 frontmatter `version` 字段。
33. **CSS `backdrop-filter` 创建 containing block（2026-05-25 教训）** — 给元素加 `backdrop-filter: blur()` 会让该元素成为 `position:fixed` 子元素的 containing block，导致 fixed 定位相对于该元素而非视口。**修复：** 移除 backdrop-filter 改用不创建 CB 的半透明背景，或将弹出元素用 Teleport 渲染到 `document.body`。
34. **tester 只读代码判 PASS（2026-05-25 教训）** — tester 读了修改后的文件就 `kanban_complete(summary="approved")`，没有用浏览器实际验证任何 UI 效果。**根因：** review 卡 body 没有强制浏览器截图。**规则：** UI 项目的 tester review spec 必须包含 `必须用浏览器工具实际访问页面，截图验证每个验收标准`。
35. **tester 修改 .env 文件（2026-05-26 教训）** — tester 在验证过程中尝试登录，发现密码不对后直接修改 `.env` 文件重置密码 hash。**修复：** tester SOUL.md 已添加"⛔ 绝对禁止修改 .env/config.yaml"规则。
36. **手动改 .env 密码 hash 格式错误（2026-05-26 教训）** — 大佬手动将 `.env` 中 `ADMIN_PASSWORD_HASH` 改为 MD5 格式，但代码用 `bcrypt.compare()` 验证，需要 bcrypt 格式。
37. **Context File Pattern 执行残留（2026-05-26 教训）** — kanban task 的 bugfix spec 文件写到了项目根目录，没有归档到 `raw/projects/<项目>/changes/` 下。
38. **Kanban worker 执行 Way C（2026-06-03 更新）** — coder/artist 通过 kanban 派发，task body 只给目标+路径+约束，不做代码推理。详见 Phase 6 Kanban 派发执行器。
39. **灵犀做代码推理（置信度 0.9，3 次触发）** — 灵犀是协调者，不是 coder。**正确做法（Way C）：** 灵犀只指定文件路径和问题现象，worker 自己读代码、自己推理根因、自己修复。
40. **worker 修复后跳过 tester 验证（置信度 0.9，2 次触发）** — worker 修复后灵犀直接汇报完成，没有让 tester 浏览器验证。修复速度 ≠ 修复质量。
41-43. （Vue 响应式 / Workspace UI 暗色主题 / 新增子模块必须先读 AGENTS.md — 略）
44. **Kanban worker 写入错误路径（2026-05-27 教训）** — worker 可能读取现有文件确定"自然"位置，忽略 constitution 指定的目标路径。task body 中必须显式写明**绝对输出路径**。
45. **worker 首轮输出功能不全 + 二轮补全模式** — 首轮后 grep 验证关键功能；缺失时二轮用精确 bullet-point 需求补全。
46. **Fastify 双静态根配置** — 需要同时服务 `src/public/` 和 `src/projects/*/public/` 时，注册两次 fastifyStatic。
47. **CodeWhale 部分编辑导致文件损坏（2026-05-28 教训）** — 超时时可能已对同一文件做了多次部分 patch，导致括号嵌套错乱。超时后直接 `write_file` 重写整个文件，不要逐行修补。
48. **Vue3 CDN 组件解构完整性** — 新建组件时，默认解构 `const { ref, computed, watch, onMounted, onUnmounted, h, defineComponent } = Vue;`
49. **灵犀做代码推理再告诉 worker 怎么改（置信度 0.9，5 轮触发，2026-06-04 再犯）** — kanban task body 只给**目标 + 现象 + 文件路径 + 约束 + 验收标准**。❌ 不该给具体代码改动（如"将 z-index 从 10 改为 100"、"添加 download_url: url"）。✅ 该给现象描述（如"播放条遮住了平台下拉框"、"下载 API 返回假成功"）。**2026-06-04 再犯案例：** Round 7 task body 写了"将 .md-search-bar 的 z-index 从 10 改为 100"、"ID 改为 `${item.song_name}_${item.source}_${item.ext}_${item.bitrate}`"。大佬纠正："不是应该给目标和问题coder，让他自己分析操作吗"。**根因：** 灵犀看到"简单 bug"就忍不住给具体修复方案，认为这样更快。但 Way C 的价值在于 worker 自己读代码推理，可能发现更好的方案或更多问题。
50-54. （API 一致性 / Fastify 禁止 execSync / 知识复利 / 子 agent 并行写共享文件 / Skill 删除连带 — 略）
55. **跳过 Phase 3 设计发散直接手写 HTML（2026-05-29 教训）** — UI 项目禁止灵犀手写 CSS，必须用 Open Design tokens。
56-58. （delegate_task 并行覆盖文件 / Skill 删除连带 scripts / Phase 1 需求澄清顺序 — 略）
59. **Phase 8 每轮必须主动记录测试结果（2026-06-03 强化）** — 每轮 Phase 8 反馈的**第一件事**是写 conversation.md，不需要大佬提醒。文档写入是门禁条件。
60. **Phase 8 禁止灵犀分析根因再告诉 worker** — kanban task body 只给现象+文件路径，让 worker 自己分析。
61. **外部 API 集成必须先查 OpenAPI spec** — 不要假设端点路径。
62. **GET vs POST handler 不匹配** — 端到端调试时，第一步验证"请求是否到达了 handler"。
63. **Kanban 评论在任务完成后不生效（2026-06-05 教训）** — 任务 done 后追加的 `hermes kanban comment` 不会触发 worker 重新执行。需求变更时必须创建新卡或在当前 session 自己修复。 | 验证：检查任务状态是否为 done | 触发：任务完成后需要追加需求
63. **task body 列举太多参考文件导致 worker 迭代耗尽** — 灵犀先读参考文件 → 写自包含 SPEC 文件 → worker 只读 SPEC。
64. **SQLite Schema 不兼容导致迁移失败** — 修改表 schema 时，必须检测旧 schema 并处理。
65. **跳过 Phase 6 tester review 直接上线** — 代码完成后必须走 tester 验证流程。
66-67. （fetch credentials / 自构造 URL — 略）
68. **知识复利的关键是注入不是记录** — 设计重心是"注入机制"，不是"记录机制"。
69. **路径迁移必须全系统扫描** — 路径迁移后必须全系统 grep。
70. **Node.js fetch() 在某些网络环境挂起** — 改用 `http.request()` 替代。
71-72. （MoviePilot REST vs MCP / 诊断代理问题先确认目标服务 — 略）
73. **Phase 8 文档规范执行不力（2026-06-03 教训，4 轮）** — 文档写入是门禁条件，不是"做完再补"。
74. **CodeWhale 声称已修复但实际未改（2026-06-03 教训）** — CodeWhale summary 列了 12 项修复，但实际只改了部分代码。返回后必须 `grep -c` 验证关键功能是否实际存在。
75. **不要分析根因再派 worker（2026-06-03 大佬纠正）** — 大佬反馈 bug 时，灵犀只做：(1) 记录现象 (2) 指定文件路径 (3) 创建 kanban 卡让 worker 分析。
76. **execFileSync 在循环中对 N 个文件调用 = 性能灾难（2026-06-03 教训）** — 批量操作禁止在循环中同步启动子进程。改为按需检查或批量脚本。
77. **Kanban 派发 fire-and-forget（2026-06-03 教训）** — 派发任务后不做追踪，任务完成 ~1.5 小时无人知晓，依赖卡 blocked 无人解除。**铁律：派发 ≠ 结束。** 派发后必须设追踪机制（cron 轮询/session 内等待/notify_on_complete），完成后三件事：(1) 验证产出物 (2) 解除依赖 (3) 通知大佬。详见 Phase 6 "派发后追踪协议"。
78. **Tester 卡迭代预算耗尽（2026-06-03 教训，2026-06-07 再犯）** — 一个 tester 卡覆盖所有功能，迭代预算耗尽未完成。**大佬原话（2026-06-07）：**"我记得以前让你派活检查需要拆开每个功能点，而不是让一个 tester 检查全部"。**铁律：** tester 卡和 coder 卡一样拆分 — 每卡只验证一个功能点（≤5min，≤30 迭代）。5 个验证点 → 5 张 tester 卡。一个卡卡住 = 全部卡住。详见 Phase 6 "Tester 卡优化"。
79. **Tester 完成无 summary 无通知（2026-06-04 教训）** — tester 卡标记 done 但 summary 为空，灵犀不知情。**根因：** task body 没要求写 summary → worker 认为"验证通过就完事了"。**规则：** (1) task body 必须要求 worker 在 kanban_complete 时写 summary（验证了什么、结果、截图路径）(2) 灵犀必须主动轮询 kanban 状态，不能等通知 (3) 完成后必须自己跑 5 步验证，不信任 worker 的 summary。
80. **Way C 连续违规 — 灵犀忍不住给具体修复方案（2026-06-04 教训，同一 session 两次）** — Round 6 灵犀直接改代码（角色分离违规），Round 7 task body 写了具体代码改动（Way C 违规）。**根因相同：** 看到"简单 bug"就认为"给具体方案更快"。**大佬两次纠正：** "修复是不是没有派活，都是你自己干了" + "不是应该给目标和问题coder，让他自己分析操作吗"。**铁律：** 无论改动多小，task body 只给现象+文件路径。worker 自己读代码的价值 > 节省的 30 秒。
81. **Kanban create 后忘记 notify-subscribe（2026-06-04 教训）** — create 后没有调 notify-subscribe，kanban_notify_subs 表为空 → worker 完成无通知 → 灵犀不知情。**铁律：** 每次 kanban create 后必须立即 `hermes kanban notify-subscribe <task_id> --platform feishu --chat-id oc_22cb909a35e6a74c62cc0d4d170b19c3`。已写入 phase6-execution.md Step 3.2。与 #77 区别：#77 是不追踪状态；#81 是技术层没建通知订阅。
82. **Worker kanban_complete 不写 summary** — task_runs 有详细结果但 tasks.result 为空。**规则：** task body 必须要求 `kanban_complete(summary=...")`；灵犀必须主动查 task_runs 或 poll 状态，不能只依赖通知。
83. **先问用户再查 skill/memory（2026-06-04 教训）** — 大佬说"代理信息应该在 clsh-project 里有记载，为什么需要问我"。代理 `192.168.0.41:7890` 已记录在 `proxy-workarounds` skill 中，但灵犀没查就问用户。**铁律：** 查找优先级 = (1) 查相关 skill → (2) 查 memory → (3) 查 wiki/Obsidian → (4) 最后才问用户。用户已提供的信息不应重复询问。**触发信号：** 需要环境配置、凭据、端口、路径等信息时。

## Kanban 运维（2026-06-07 新增）

84. **Profile toolset 缺失导致 worker 静默失败（2026-06-07 教训）** — tester/worker profile 的 `config.yaml` 中 `toolsets` 缺少必要工具时，worker 启动后 60s 内退出，kanban 报 `protocol violation`（rc=0 但没调 kanban_complete）。**实测案例：** tester 缺少 `browser` + `vision` → 连续 4 个浏览器验证任务全部 1 分钟 crash。**排查路径：** protocol violation → 对比能正常工作的 profile 的 toolsets。**铁律：** 派发前验证 assignee profile 的 toolsets。UI 验证 → `browser` + `vision`；代码 → `terminal` + `file`。详见 `references/pitfalls/kanban-ops-lessons.md`。
85. **Kanban watchdog 脚本参数错误（2026-06-07 教训）** — `hermes kanban list --status in_progress` 无效（状态名是 `running`）；`hermes cronjob` 不存在（正确命令 `hermes cron`）。两个 bug 导致 watchdog 静默退出。详见 `references/pitfalls/kanban-ops-lessons.md`。
86. **凭据写入 task body 后必须 curl 验证（2026-06-07 教训）** — Workspace 密码 `clsh666.`（末尾有句号），写入 kanban 评论时漏掉句号 → 3 个 tester 全部认证失败。**铁律：** 凭据写入 task body 后用 curl 验证一次。

87. **MiMo API 429 限流 — 并行派发秒炸（2026-06-07 教训）** — 4 个 tester 并行 dispatch → 4 个 MiMo API key 同时请求 → 全部 429 → `max_retries_exhausted` → 60s 内 crash（protocol violation）。**现象：** PID alive 但心跳 3+分钟停止，request dump 中 `429 Too many requests`。**铁律：** MiMo API 环境下**串行派发**（`dispatch --max 1`），间隔 ≥90s。**排查路径：** heartbeat 停止 → ps 确认 → 查 request dump → 429 → kill → archive → 串行重试。**正例：** 串行 2 张 10 分钟内 PASS。

88. **浏览器截图验证耗尽 API 迭代预算（2026-06-07 教训）** — tester 做浏览器登录+screenshot+vision 分析，单任务消耗大量 API 调用，叠加并行 = 立刻 429。**规则：** (1) UI 验证优先用代码检查（grep/node --check）替代浏览器截图 (2) 必须浏览器验证时，串行 dispatch 一张一张来 (3) task body 明确告诉 tester 可用命令行替代浏览器。

91. **`hermes cron resume` 对不存在的 cron 静默成功（2026-06-07 教训）** — `hermes cron resume 1d04104d3ca9` 报 "Resumed job: kanban-watchdog" 但该 cron 从未存在。后续 `hermes cron show` 返回 exit code 2（not found）。**铁律：** resume/create cron 后必须 `hermes cron list` 验证实际存在。参考 ID 不可信，必须从 list 输出中确认。

92. **`notify-subscribe` 发送文件内容而非文本摘要（2026-06-07 教训）** — kanban 任务完成后，notify-subscribe 通知机制把 coder 修改的文件内容（如 index.html）作为通知发送给用户。**根因：** 通知系统将 task result 中的文件变更作为附件发送。**规避：** 用 no_agent cron watchdog 脚本输出纯文本摘要，不依赖 notify-subscribe 的默认行为。

93. **CDN 库 API 版本不兼容（2026-06-07 教训）** — `marked` CDN 加载后 `marked(text)` 报 "marked is not a function"，因为 marked v5+ 顶层 API 改为 `marked.parse(text)`。**铁律：** 添加 CDN 库后必须在浏览器控制台验证 API 调用方式，不能假设 API 与旧版一致。coder 自己分析此类问题，灵犀不替 coder 判断根因。

94. **Kanban scratch workspace 产出文件丢失（2026-06-07 教训）** — kanban scratch workspace（`/root/.hermes/kanban/workspaces/<task_id>/`）是临时目录，任务完成后清理。worker 写入 scratch 的代码文件不会持久化到实际项目目录。**实测：** 12 个代码生成任务用 kanban 派发 → worker 成功完成 → scratch 清理 → 文件不存在。**铁律：** 产出持久文件的任务（代码生成、新建文件）用 `delegate_task`（子 agent 直接写项目目录）。kanban 只用于无文件产出的任务（测试验证、纯推理）或修改现有文件。详见 `references/pitfalls/kanban-ops-lessons.md` §4。

90. **`max_in_progress_per_profile` 需要 gateway restart（2026-06-07 教训）** — `dispatch_in_gateway: true` → kanban daemon 运行在 gateway 进程内 → config 变更需要 restart 生效。**现象：** 设置 `max_in_progress_per_profile: 1` 后 daemon 仍并行派发。**铁律：** 修改 kanban config 后必须 `hermes gateway restart`（从外部 shell，内部会报 `Refusing to restart`）。详见 `references/pitfalls/kanban-ops-lessons.md` §5。

### #87: Kanban 并发打爆 API（2026-06-07）
- **场景：** 12 个工业区任务同时派发给 coder，全部打爆 MiMo 429
- **根因：** `max_in_progress_per_profile: null`（无限制）+ `auto_decompose_per_tick: 3`（每 tick 3 个）+ gateway 未重启导致配置未生效
- **症状：** 所有任务 blocked（protocol violation — worker 429 后退出没调 kanban_complete）
- **修复：** `max_in_progress_per_profile: 1` + `auto_decompose_per_tick: 1` + `dispatch_stale_timeout_seconds: 600`
- **教训：** 任务必须顺序派发，不能并行。配置修改后必须重启 gateway。
- **验证：** `hermes config get kanban.max_in_progress_per_profile` 应返回 1

### #88: Watchdog 不检测 blocked 任务（2026-06-07）
- **场景：** 12 个任务全部 blocked，watchdog 看不到（只监控 running/ready），自暂停
- **根因：** watchdog 只检查 running 和 ready 状态，不检查 blocked
- **修复：** watchdog v2 新增 blocked 检测 + 自动 unblock 重试（最多 2 次）
- **教训：** watchdog 必须覆盖所有活跃状态（running + ready + blocked）

### #89: 跳过 tester 验证直接派 coder（2026-06-07）
- **场景：** 工业区迁移直接派 coder，没先派 tester 验证旧模块结构
- **根因：** "调研阶段已经读过代码" 不等于 "独立 tester 验证过"
- **正确流程：** Phase 6 Wave 0 先派 tester 验证（确认旧模块结构+新工作台架构），再派 coder
- **教训：** delegate_task 的结论是 self-reported，需要独立 tester 验证
