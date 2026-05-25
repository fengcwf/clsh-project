# SOUL.md 行为约束：Karpathy + Superpowers 融合方案

> 来源：2026-05-25 Workspace Phase 8 反馈循环中的系统性分析
> 用途：改进 agent SOUL.md 的行为约束强度

## 问题

SOUL.md 行为规则（如"数据说话"、"先理解再动手"）是**抽象原则**，LLM 可以宽松解释。
KANBAN_GUIDANCE 是通用协议，没有 review 专用门禁。
Task body 的具体指令总是赢过抽象原则（recency + specificity bias）。

## 三方对比

| 方案 | 管什么 | 策略 |
|------|--------|------|
| **Karpathy Skills** | 入口端 | 目标转换：模糊→可验证 |
| **Superpowers** | 出口端 | 交付门禁：没证据不许声称完成 |
| **Hermes 现状** | 通用协议 | 软约束，无 review 门禁 |

## Karpathy 4 原则

1. **Think Before Coding** — 不假设，不隐藏困惑，列出权衡
2. **Simplicity First** — 最少代码解决问题，不投机
3. **Surgical Changes** — 只改必须改的，清理自己的孤儿
4. **Goal-Driven Execution** — 定义成功标准，循环直到验证

**关键洞察：** "Strong success criteria let you loop independently."

**目标转换表：**
```
"Fix the bug"     → 写复现测试 → FAILS → 修复 → PASSES
"Add validation"  → 写无效输入测试 → 使通过
"Refactor X"      → 确保测试前后都通过
```

## Superpowers verification-before-completion

**5 步门禁函数：**
```
BEFORE 声称完成/修复/通过：
1. IDENTIFY: 什么命令能证明？
2. RUN: 执行完整命令（新鲜的）
3. READ: 完整输出 + exit code
4. VERIFY: 输出确认声明？
5. ONLY THEN: 带证据汇报
跳过任何一步 = 撒谎，不是验证
```

**Rationalization Prevention（防辩解表）：**
| 借口 | 现实 |
|------|------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Code looks correct" | Code ≠ running system |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |

## 应用到 SOUL.md

每个 agent 的 SOUL.md 补强三板斧：

1. **交付门禁** — 5 步验证函数（来自 Superpowers）
2. **目标转换** — 收到模糊任务自动转为可验证目标（来自 Karpathy）
3. **防辩解表** — 借口 vs 现实（来自 Superpowers）

### Coder 专用
- 收到 "修复 X" → 必须先找到精确根因 → 写复现测试 → 修复 → 验证
- 不允许在跑验证之前说"应该可以了"

### Tester 专用
- Review Gate 步骤 5 从"读代码"改为"执行验证（不可跳过）"
- 没有验证证据的 PASS = 违规
- UI 项目必须截图

### Scout 专用
- 每个结论 2+ 独立来源
- 没有来源证据的结论 = 编造

### Worker 专用
- 跑完 ≠ 成功，检查 exit code
- 检查产出物存在

### Artist 专用
- 截图修改前/后对比
- 没有截图对比的 UI 完成 = 违规

## Hermes Issue

已提交 feature request 草稿：
`wiki/syntheses/2026-05-25-hermes-issue-soul-md-behavioral-enforcement.md`

建议在 KANBAN_GUIDANCE 中加 review 专用门禁，或在 kanban_complete() 工具层加 metadata 验证检查。

## 参考

- https://github.com/multica-ai/andrej-karpathy-skills — Karpathy CLAUDE.md
- https://github.com/obra/superpowers/skills/verification-before-completion — Superpowers 门禁
- https://github.com/NousResearch/hermes-agent/issues/19351 — KANBAN_GUIDANCE 身份覆盖修复
