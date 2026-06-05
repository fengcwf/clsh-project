# Learnings

> clsh-project 执行经验持久化。每次项目执行前读取，执行中/后追加。
> 总量控制在 50 条以内。条目格式：`- [日期] 内容。来源: 项目名`

## 流程教训

- [2026-05-24] Wave 1-3 用 delegate_task 替代 kanban 是流程违规。原因：灵犀判断"效果一样"，忽略了 kanban 的持久化/依赖链/通知/审计能力。修正：任何 ≥3 工具调用的任务必须走 kanban。来源: workspace-mvp
- [2026-05-24] 建卡后被动等通知不可靠。hermes kanban create CLI 不自动订阅通知（#19479 上游故意不修）。修正：用 kcreate 脚本（建卡+自动订阅）+ kwait 轮询。来源: workspace-mvp
- [2026-05-24] Phase 3/5 如果不产出文件，后续 Phase 7 评估会判 FAIL。修正：Phase 3 必须输出 tasks.md，Phase 5 必须输出详细 task slice 文件。来源: workspace-mvp
- [2026-05-24] .env 生成密码 hash 也是"写代码"，应派给 coder。灵犀不该碰任何代码/配置生成。来源: workspace-mvp
- [2026-05-24] kanban create CLI 的 --parent 参数可能不生效（parents=[]）。建卡后必须用 klink 手动补链并验证。来源: workspace-mvp
- [2026-05-24] 禁止声称"没有 kanban 功能"。Hermes 有完整 kanban 系统，应先 hermes kanban --help 确认。违反铁律第1条。来源: workspace-mvp

## 技术陷阱

- [2026-05-24] @fastify/session 的 cookie.name 默认是 'sessionId'，前端 fetch 需要 credentials:'include'。来源: workspace-mvp
- [2026-05-24] bcrypt 在 npm 上安装需要代理（HTTPS_PROXY），否则超时。pnpm + npmmirror 更可靠。来源: workspace-mvp
- [2026-05-24] dotenv 的 config() 读 .env 是相对于 CWD，不是相对于脚本路径。必须 cd 到项目根目录再 node。来源: workspace-mvp

## 工具链

- [2026-05-24] kanban 通知依赖 gateway notifier watcher + notify-subscribe 订阅。两者缺一不可。来源: workspace-mvp
- [2026-05-24] chromium --headless 截图写到 CWD 的 screenshot.png，不是 --screenshot 指定路径。来源: workspace-mvp
- [2026-05-24] hermes kanban show 输出包在 {"task": {...}} 里，不是直接返回 task 对象。来源: workspace-mvp

## UI 设计

- [2026-05-24] 路径 A 需要 Step 4.5 生成结构化 prompt 给 artist（RTCF+v0 组合模板），不能只说"做个页面"。来源: workspace-mvp
- [2026-05-24] popular-web-designs（54 套品牌模板）在 .Archive 但内容完整，可补充 Open Design token。来源: workspace-mvp
- [2026-05-24] Halo 博客可用 Open Design typography 统一文章样式，公众号/小红书只能优化封面。来源: workspace-mvp

## 待验证假设

- [2026-05-24] dispatch_interval_seconds 降到 15s 能加快派发吗？需对比测试。来源: workspace-mvp
- [2026-05-24] kwait 30s 轮询间隔够吗？会不会错过快速完成的任务？来源: workspace-mvp
