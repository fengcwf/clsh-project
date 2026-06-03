# Common Pitfalls — 完整版

> 本文件是 clsh-project SKILL.md Common Pitfalls 的完整版（含历史案例细节）。SKILL.md 中保留精简摘要（规则+验证+触发）。

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
49. **灵犀做代码推理再告诉 worker 怎么改（置信度 0.9，3 轮触发）** — kanban task body 只给**目标 + 参考文件 + 约束 + 验收标准**。❌ 不该给具体 CSS 代码、详细实现步骤。✅ 该给概念性目标。
50-54. （API 一致性 / Fastify 禁止 execSync / 知识复利 / 子 agent 并行写共享文件 / Skill 删除连带 — 略）
55. **跳过 Phase 3 设计发散直接手写 HTML（2026-05-29 教训）** — UI 项目禁止灵犀手写 CSS，必须用 Open Design tokens。
56-58. （delegate_task 并行覆盖文件 / Skill 删除连带 scripts / Phase 1 需求澄清顺序 — 略）
59. **Phase 8 每轮必须主动记录测试结果（2026-06-03 强化）** — 每轮 Phase 8 反馈的**第一件事**是写 conversation.md，不需要大佬提醒。文档写入是门禁条件。
60. **Phase 8 禁止灵犀分析根因再告诉 worker** — kanban task body 只给现象+文件路径，让 worker 自己分析。
61. **外部 API 集成必须先查 OpenAPI spec** — 不要假设端点路径。
62. **GET vs POST handler 不匹配** — 端到端调试时，第一步验证"请求是否到达了 handler"。
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
78. **Tester 卡迭代预算耗尽（2026-06-03 教训）** — 一个 tester 卡覆盖所有功能（平台分类+封面+元数据+回归），迭代预算 90 耗尽 12 轮未完成。**根因：** Review Checklist 太重（4 大类 10+ 项）+ 浏览器验证与代码审查混在一起。**铁律：** tester 卡和 coder 卡一样拆分 — 每卡只验证一个功能点（≤30 迭代）。灵犀做机械预检（语法/grep/curl），tester 只做浏览器验证。详见 Phase 6 "Tester 卡优化"。
