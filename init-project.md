---
phase: init
name: "项目基础设施初始化（目录确认 + project/board/bot 创建）"
gate_script: "gate-init.py"
output_files: [".cp-init.json"]
---

# Init: 项目基础设施初始化（Phase 0 之前，强制）

> **每次新项目必须执行。目录必须每次与用户确认，不得自行假定。**
> gate-workflow.py 检测到 `.cp-init.json` 缺失时会把流程拦回本步骤。

## 执行步骤

### Step 1: 与用户确认项目信息（⛔ 不可跳过）

向用户确认以下三项，**必须得到明确回复**：

1. **项目名称**（人类可读，如"医院预算系统"）
2. **slug**（小写字母/数字/连字符，如 `yusuan`）
3. **项目目录**（默认建议 `/opt/workdata/<slug>`，但每次必须问，用户可指定其他路径）

### Step 2: 创建项目目录

```bash
mkdir -p <项目目录>
```

若目录已存在且非空 → 停下，询问用户是复用还是换目录。

### Step 3: 创建 Hermes Project + Kanban Board

```bash
hermes kanban boards create <slug>        # 若 board 已存在则跳过
hermes kanban boards switch <slug>
hermes project create "<项目名称>" --slug <slug> --primary <项目目录> --board <slug> --use
```

### Step 4: 创建项目专用 Bot（5 个，按角色克隆）

> 教训（jixiao 项目）：kanban 派活必须用项目专用 bot，禁止派给全局 profile。

每个角色 bot 从对应模板 profile 克隆（模板即 skill 派活使用的 agent）：

```bash
hermes profile create <slug>-artist   --clone-from artist   --description "<项目名称> UI bot"
hermes profile create <slug>-coder    --clone-from coder    --description "<项目名称> 编码 bot"
hermes profile create <slug>-scout    --clone-from scout    --description "<项目名称> 调研 bot"
hermes profile create <slug>-tester   --clone-from tester   --description "<项目名称> 测试 bot"
hermes profile create <slug>-reviewer --clone-from reviewer --description "<项目名称> 审查 bot"
```

若某个 `<slug>-<role>` profile 已存在则跳过（幂等）。

### Step 5: 写初始化清单 `.cp-init.json`

写入 `<项目目录>/.cp-init.json`，字段必须完整：

```json
{
  "project_name": "<项目名称>",
  "slug": "<slug>",
  "directory": "<项目目录绝对路径>",
  "board": "<slug>",
  "bots": {
    "artist": "<slug>-artist",
    "coder": "<slug>-coder",
    "scout": "<slug>-scout",
    "tester": "<slug>-tester",
    "reviewer": "<slug>-reviewer"
  },
  "user_confirmed": true,
  "confirmed_at": "<ISO 时间戳，用户确认目录的时间>",
  "created_at": "<ISO 时间戳>"
}
```

### Step 6: 机械验收（gate-init.py）

```bash
python3 scripts/gate-init.py <项目目录>
```

gate-init.py 会用 hermes CLI 实际验证：board 存在、5 个 bot profile 存在、
project 已注册、`.cp-init.json` 字段完整。

- PASS → 向用户展示确认码，用户确认后运行 `gate-init.py <目录> --verify <CODE>`
- FAIL → 按 errors 修复后重跑，**不得带病进入 Phase 0**

## 铁律

- IL-INIT-1: **目录必须每次与用户确认** — 禁止静默使用默认值
- IL-INIT-2: **gate-init.py PASS + 用户确认码验证后才能进入 Phase 0**
- IL-INIT-3: **Phase 6 不再创建 project/board/bot** — 基础设施只在本步骤创建一次

## 验收标准

- `<项目目录>/.cp-init.json` 存在且 5 个 bot 字段完整
- `hermes kanban boards list` 包含本项目 board
- `hermes profile list` 包含 5 个 `<slug>-<role>` bot
- `hermes project list` 包含本项目且 primary 指向确认过的目录
- gate-init.py 返回 PASS 且 --verify 通过
