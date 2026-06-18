---
version: 1.0.0
description: "Hermes Agent L4 Loop Native 原语 — /goal、/subgoal、kanban --goal 模式。clsh-project Phase 8 可用的 harness 原生循环能力。"
created: 2026-06-18
---

# Hermes L4 Loop Native Features

> 来源：Hermes 官方文档 + GitHub commits 调研（2026-06-18）
> 关联：[[从 skill 到 loop native：我理解的 Loop Engineering]] 分析

## 核心发现

Hermes 已有多个 L4 级原语，clsh-project 未充分利用。

## `/goal` — Ralph Loop

```
/goal Fix every failing test in tests/hermes_cli/
```

**机制：**
- Loop state：目标 + 子目标持久化在 `SessionDB.state_meta`，跨 /resume 存活
- Judge model：每 turn 结束后辅助模型判断 `{done: bool, reason: string}`
- Auto-continue：未完成自动继续，同一 session 内循环
- Turn budget：默认 20 轮，`goals.max_turns` 可配
- Fail-open：judge 出错 → continue，不阻塞

**对照 Loop Engineering 三问：**
- 流程：while not done → continue（代码控制）✅
- Loop state：goal + subgoals 持久化 ✅
- 算子：judge model（软规则）✅

## `/subgoal` — HITL 语法

```
/subgoal Add a regression test for the bug you just patched
/subgoal                            # 列出当前子目标
/subgoal remove 2                   # 删除第 2 条
/subgoal clear                      # 清空
```

**机制：**
- 追加验收标准到活跃 goal，不重置 loop
- judge prompt 重写，必须满足所有 subgoal 才算 done
- 持久化在 SessionDB.state_meta

## Kanban `--goal` 模式

**commit `0cd7d54b0`**: `feat(kanban): goal_mode cards run workers in a /goal loop`

```bash
hermes kanban create --goal --goal-max-turns 30 "Fix auth bug"
```

**机制：**
- kanban card 的 worker 被包裹在 /goal loop 中
- judge 检查 worker response vs card title+body
- worker 在同一 session 持续工作直到 judge 说 done
- 超时 → card 进入 blocked 状态（人工介入）
- 不是静默退出，是显式阻断

## clsh-project 应用

### Phase 8 反馈循环替代方案

| 现在（脚本驱动） | 可用（/goal 原生） |
|----------------|------------------|
| gate-phase8.py 手动检查 bugfix 进度 | `/goal "修复 XX bug"` + judge 自动判断 |
| hash 码防止跳步 | `/goal` turn budget + judge 持续检查 |
| 手动循环（send → verify → retry） | `/goal` auto-continue |
| 确认码替代验收标准 | `/subgoal` 原生验收标准管理 |

### 硬规则 vs 软规则分工

| 检查类型 | 用什么 | 原因 |
|---------|--------|------|
| 文件存在性、关键词、行数 | gate 脚本 | 机器判断，不可用 LLM 替代 |
| "bug 修好了吗"、"功能实现了吗" | /goal + judge | LLM 判断，不应该用脚本模拟 |
| 验收标准追加 | /subgoal | HITL 语法，用户控制 |

**核心洞察：gate 脚本（硬规则）+ /goal（软规则 loop）= 完整的 L4 组合，不是替代关系。**

## 禁止行为

- 禁止用 /goal 替代 gate 脚本的文件存在性检查 — 硬规则必须用脚本
- 禁止用脚本模拟 /goal 的 LLM 判断 — 软规则应该用 judge model
- 禁止不设 turn budget 就用 /goal — 必须有上限防止无限循环

## 参考链接

- `/goal` 文档：https://hermes-agent.nousresearch.com/docs/user-guide/features/goals
- Kanban `--goal` commit：`0cd7d54b0`
- Loop Engineering 分析：`raw/01-articles/Loop Engineering 分析：文章验证 + clsh-project 定位.md`
