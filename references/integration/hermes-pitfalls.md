# Hermes 工具链陷阱

> 从 clsh-project Common Pitfalls 迁移（2026-05-22）
> 原因：SKILL.md 膨胀，工具链细节不属于流程纪律

## Kanban

### blocked 状态不触发依赖引擎
worker 调用 kanban_block() 后，blocked ≠ done，依赖引擎不会 promote 子任务。灵犀必须先 complete 原卡再创建 fix 子卡（parents=[原卡]）。

### Review 卡必须在 checkpoint 验证后创建
不要同时创建实现卡和 Review 卡。灵犀验证 checkpoint PASS 后才创建 Review 卡。

### Kanban 状态同步问题
coder/worker 完成后可能未正确调用 kanban_complete。灵犀应 5 分钟后检查 running 状态的卡，用 ls 检查产出物，存在则手动 complete。

### Review 卡应由灵犀创建
实现卡完成后灵犀应主动创建 Review 卡，不依赖 agent 自判。

### notify-subscribe 命令可能返回空
hermes kanban notify-subscribe 可能返回空输出（exit code 1），不影响功能，跳过即可。

### Phase 6 Kanban 卡创建后状态为 running
dispatcher 自动将 ready 状态的卡标记为 running，正常行为不需要干预。

## delegate_task

### 超时根因
coder agent 超时常见根因：(1) 验证阶段同步 I/O 阻塞 (2) npm install 网络慢 (3) Docker Hub 超时。解决：任务描述中写"不要运行验证命令，只写文件"。

### 全部超时的应急方案
3+ 个 delegate_task 全部超时（600s）时不要重复派发。应急：灵犀直接 patch 前端文件 + 记录流程偏差 + tester 验证。预防：每个 agent 任务控制在 2-3 个文件修改。

### 多 agent 同时超时的根因
任务描述过于复杂、agent 启动开销大、网络延迟。解决：每个 ≤2-3 文件，不派验证命令，超时 2 次后转灵犀直接修改。

### Artist 大任务拆分模式
5+ 个前端变更时按职责拆分：CSS/样式、功能修复、新增功能。每个子任务控制在 5-8 分钟。

### Coder 任务描述精确性
coder 可能遗漏小字段。任务描述中明确列出每个函数的返回值格式，包括计算字段。

### 任务拆分防超时（用户偏好）
单个 agent 任务不超过 5 分钟。前端按职责拆分，后端按 API/模块拆分。

## Cron & 巡检

### 巡检报告写本地
cron prompt 必须指定 Obsidian 路径，不能只写 ~/.hermes/cron/output/。

### 公众号检查不走云主机
本地出口 IP 不在微信白名单中。必须 SSH 到云主机执行。

### 公众号 API 检查未走云主机 SSH
巡检脚本在本地调用 wechat-publish.cjs 会失败。修复：通过 SSH 到云主机执行。

## Gateway & 插件

### hook 只拦截特定前缀消息
pre_gateway_dispatch hook 只拦截配置的前缀。纯数字消息不经过插件直接进 LLM。要在 hook 中支持数字匹配，必须在 on_pre_dispatch 里显式处理。

### register_command 只对斜杠命令有效
register_command("/mp", handler) 只拦截 /mp 前缀。纯数字消息不是斜杠命令。这是唯一的零 token 路径。

### 飞书 Card 按钮不会发送消息
飞书 Interactive Card 按钮点击触发 card.action.trigger 回调，不会把 value 作为消息发送到对话。Hermes 飞书 adapter 转换为 /card 命令。

### 插件指令一次性化
插件执行完就结束，没有上下文保持。搜索完结果后用户想操作需重新发指令。应设计状态机或上下文保持机制。

### 调研时不要反复重启 gateway
每次重启中断 session 导致重复分析。调研阶段只读文档和搜索，不修改运行中的代码。

## 其他工具

### delegation-protocol 重复加载浪费 token
每次派活前读完整 delegation-protocol（3000+ 字）。解决：session 内缓存（只加载一次）+ 快速检查清单。

### MCP 重复调用归因错误
是工具映射问题不是项目问题。

### 大规模文件索引策略
14229 个文件全量扫描 >120s。必须用 grep 预过滤。SQLite FTS5 trigram 分词器对中文更友好。

### 图片生成方案调研
优先推荐免费 API 方案（Gemini、FLUX.2 Schnell、Seedream V4），不推荐付费方案或需本地 GPU 的方案。

### UI/UX Pro Max 使用模式
uipro init --ai all --force → python3 .cursor/skills/ui-ux-pro-max/scripts/search.py → 写入 design-system/MASTER.md。

### Phase 6 Checkpoint 输出过长
限制 200 字以内，长文本写入 /tmp/<project>-<task>.log。
