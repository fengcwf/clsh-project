# MiMo Desktop 多角色 / actor 能力对照（相对 Hermes bot mode）

## 结论速览

| 需求 | Hermes bot mode | MiMo Desktop 对应 | 可替代？ |
|------|-----------------|-------------------|----------|
| 持久角色（coder/artist/tester/reviewer/scout） | kanban worker + SOUL + skills + tools | **自定义 subagent** `.mimocode/agent/clsh-*.md`（本 skill `agents/` 模板） | **近似**：system prompt + skills + tool 策略可配；**无** kanban 物理派单 |
| 角色间直接互发消息 | bot A → bot B | **无原生 bot-to-bot**。主会话编排，或 `session-chat` 会话互聊（hop≤5） | **编排替代** |
| 项目专用长期 bot 会话 | 项目 kanban profile | `create_session` 建命名会话 + `talk_to_session` 持续对话 | **近似** |
| coder 完直接叫 artist | worker 链 | 主会话：coder 完成 → spawn artist（或 talk_to_session artist 会话） | **主 agent 中枢** |
| 完整 SOUL | `SOUL.md` 注入 | agent markdown **body = system prompt**（等价 soul） | **是** |
| 专用 skill 集 | skill 预载 | 子代理可加载 `~/.claude/skills` 中相关 skill；也可在 prompt 内点名 | **是（按需）** |
| 工具白名单 | toolsets | frontmatter `tool_allowlist` / workflow `tools: []` | **是** |
| 物理门禁 hook | gate-enforcer | **无**等价 pre_tool_call 插件（可用 evolve hooks 自建，复杂） | **否（默认）** |
| 多 agent 确定性流水线 | 手写 | `.mimocode/workflows/*.js` + `agent()` API | **更强**（可 pipeline） |

## 三种「子代理」别搞混

| 机制 | 生命周期 | 用户可见 | 适用 |
|------|----------|----------|------|
| **`actor` spawn/run** | 一次性任务级 | 否（后台） | 单任务实现/审查/调研 |
| **自定义 agent 文件** | 跨 spawn 可复用身份 | 否 | 角色化 prompt（coder 等） |
| **session-chat 会话** | 长期对话 | **是**（侧栏会话） | 项目常驻 bot、跨会话协作 |

`actor` 默认 `general`/`explore`；定义 `agents/clsh-coder.md` 后可用 `subagent_type: clsh-coder`（以 `mimo agent list` 实际名为准）。

## 推荐映射（clsh-project-mimo Phase 4 流水线）

```text
主会话 (coordinator)
  │ actor/spawn clsh-coder   → reports/task-N-report.md
  │ actor/spawn clsh-reviewer → brief + report + diff package
  │ （UI 任务）actor/spawn clsh-artist
  │ （Phase0/1）actor/spawn clsh-scout
  └ 仍由主会话写 ledger / 跑 gate / 向用户要审批
```

**不要**期望 coder 自动唤醒 artist——MiMo 必须 coordinator 串行/编排。

## 安装角色模板（项目级，推荐）

```powershell
$skill = "$env:USERPROFILE\.claude\skills\clsh-project-mimo\agents"
$projAgents = "<你的代码项目>\.mimocode\agent"
New-Item -ItemType Directory -Force -Path $projAgents | Out-Null
Copy-Item "$skill\clsh-*.md" $projAgents
# 新对话后: mimo agent list 或查看 @ 补全
```

全局安装：复制到 `~\.config\mimocode\agent\`。

## 与 session-chat 组合（更接近 Hermes「专用 bot」）

1. `create_session` name=`clsh-coder` purpose=`实现计划任务` workspace=项目路径  
2. 后续 `talk_to_session` contact=`clsh-coder` 投递 brief 路径  
3. tester/reviewer 同理；主会话仍跑 gate  
4. 限制：hop≤5；对方看不到你这边上下文，消息必须自包含  

适合「长期同一角色、多轮」；短任务用 actor 更省侧栏噪音。

## 本 skill 的选择

| 阶段 | 默认 | 可选升级 |
|------|------|----------|
| Phase 0/1 调研 | `actor` clsh-scout / explore | 复杂竞品 → websearch+browser |
| Phase 4 实现 | `actor` clsh-coder + clsh-reviewer | UI 加 clsh-artist |
| 长项目多变更 | 文件 ledger | 常驻 session 作 coder/tester |

## 诚实差距

1. **无** kanban 状态机与物理阻断门禁。  
2. **无** bot 自主互相呼叫——必须 coordinator 或 session-chat。  
3. Desktop 若未暴露 `subagent_type` 自定义名，则退回 `general` 并在 prompt 内粘贴角色契约（本 skill brief 已含契约摘要）。  
4. Skills 是否注入子代理取决于引擎配置；不确定时在 dispatch prompt 中显式要求遵守 TDD/审查规则。
