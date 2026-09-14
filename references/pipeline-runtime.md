# Phase 4 Pipeline Runtime（A″）

主会话 = coordinator + gate；workflow = 单 task 执行引擎。

## 时序

```text
Architectural → bootstrap_roles.py → Phase 0-3
Phase 4 per task:
  gate/ledger → brief → workflow clsh-task-pipeline
    coder → artist? → tester ⇄ (maxFix) → reviewer ⇄ (maxFix)
    → GREEN | NEEDS_HUMAN
  主会话同步报告到 Obsidian → ledger → 下一 task
Phase 5: 整分支审查（不在 pipeline 内）
```

## args 契约

| 字段 | 含义 | 默认 |
|------|------|------|
| taskN | 任务号 | 必填 |
| briefPath | brief 绝对/相对路径 | 必填 |
| reportDir | 报告目录 | `.clsh/reports` |
| needUI | 是否跑 artist | false |
| maxFix | 每阶段熔断轮次 | 2 |
| coderTimeoutMs | coder 超时 | 900000 |
| otherTimeoutMs | 其他角色超时 | 600000 |
| fromStage | 中断续跑起点 | coder |
| modelBase | 首轮 coder 模型组 | `standard` |
| modelUpgrade | 修复轮；null/省略=不传 model | 勿写死不存在的组名 |
| useRoleAgents | false → general + 角色契约 | true |

## 门禁核对（v2.3.0）

```powershell
# Phase 4
gate_phase.py <vault_project> <slug> 4 --code-project <code_proj>
# 检查: clsh-coder.md 存在; pipeline-result 仅 GREEN|NEEDS_HUMAN; NEEDS_HUMAN 须进 ledger

# Phase 5
gate_phase.py <vault_project> <slug> 5 --code-project <code_proj>
# 检查: 全部 task-*-pipeline-result.json == GREEN
```

角色安装自检：`scripts/check_agents.py <code_proj>`

## 卡死

| 信号 | 含义 |
|------|------|
| `agent()` → `null` | 超时/取消/失败（引擎 cancel，不永久挂死） |
| schema 字段缺失 | 交付不合格 |
| report 文件未落盘 | 伪交付 |
| 连续 maxAttempts null | 升档后仍失败 → NEEDS_HUMAN |

禁止：无限重试；主会话对 NEEDS_HUMAN 静默忽略。

## 循环

1. tester `verdict=FAIL` → findings JSON → 回 coder（UI-only 可 artist）
2. coder `fixed_finding_ids` 必须覆盖 Critical/Important open ids
3. reviewer Critical → 同上再进 coder fix
4. `round > maxFix` → NEEDS_HUMAN

## 报告位置

- 流水线权威：`<code>/.clsh/reports/task-N-*-report.json`
- 人读/gate：同步摘要到 Obsidian `changes/<slug>/reports/`
- 人读模板：skill `templates/reports/*.md`

## 降级 B

无 `clsh-*` agent 时：`actorType: general` + 在 prompt 粘贴角色契约与 JSON 字段要求；主会话手动串行 spawn/wait。

## 多项目

每个代码项目独立 bootstrap；`.clsh/` 与 `.mimocode/agent/` 不跨项目共用。
