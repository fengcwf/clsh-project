---
phase: 8
name: "优化循环"
gate_script: "gate-phase8.py"
output_files: ["ledger.md"]
---

# Phase 8: Optimization Loop（优化循环）

> 从 Superpowers + Ralph Loop + MoA 分析提炼的优化循环模式。
> 核心：Fresh Context + One Thing + Two-Phase + Circuit Breaker + Skill Anchoring

## 前置依赖

- Phase 7 的归档完成（或 Phase 6 的任务执行完成）

## ⚡ Skill 锚定（强制）

**每次处理反馈时，协调者必须声明：**

```
"我正在使用 clsh-project 的优化循环处理反馈。
 反馈类型: [UI/逻辑/需求/性能/确认]。
 路由: Phase 6 [角色] / Phase 1-3 / Phase 7。"
```

⛔ 禁止：不声明直接处理 | ad-hoc 修改 | 跳过路由 | 在主会话中直接执行代码

## ⛔ COORDINATOR ROLE LOCK

**You are NOT an analyst. You are NOT a debugger. You are NOT a code reviewer.**

Your ONLY job:
1. 声明 skill 锚定
2. 判断反馈类型 → 查路由表
3. 记录现象（不分析根因）
4. 派发任务（delegate_task，fresh context）
5. 验证结果（tester）
6. 更新 ledger

## 铁律

- OL-1: **ONE THING PER ITERATION** — 每轮优化只处理一个反馈
- OL-2: **FRESH CONTEXT** — 每个任务必须 delegate_task，不允许在主会话直接执行
- OL-3: **TWO-PHASE** — 先 gap analysis（只读不改），再 implementation
- OL-4: **CIRCUIT BREAKER** — 全局 optimization round 上限
- OL-5: **SKILL ANCHORING** — 每次处理反馈必须声明

## 反馈路由表

| 反馈类型 | 路由目标 | 执行方式 | 示例 |
|---------|---------|---------|------|
| UI/样式 | Phase 6 artist | delegate_task + task brief | "按钮颜色不对" |
| 逻辑 bug | Phase 6 coder | delegate_task + task brief | "计算结果有误" |
| 需求变更 | Phase 1-3 重走 | gate 脚本重置 + 全流程 | "加一个新功能" |
| 性能问题 | Phase 6 coder | delegate_task + task brief | "页面加载太慢" |
| 用户确认 | Phase 7 归档 | gate-phase7 | "可以了" |

## 执行流程

### Phase 8a: Gap Analysis（只读不改）

收到反馈后，协调者**只分析不执行**：

1. 声明 skill 锚定
2. 判断反馈类型 → 查路由表
3. 读取 ledger.md，确认当前 optimization round
4. 如果是逻辑/UI/性能问题：
   - 读取相关文件（只读，不修改）
   - 记录现象 + 文件路径 + 验收标准
   - 生成 task brief
5. 如果是需求变更：
   - 记录变更内容
   - 重置 gate-workflow 到 Phase 1
6. 如果是用户确认：
   - 进入 Phase 7 归档

⛔ Phase 8a 禁止：修改代码 | 运行命令 | 分析根因

### Phase 8b: Implementation（Fresh Context）

Gap Analysis 完成后，协调者派发任务：

1. **Fresh Context**: 必须用 `delegate_task`（新子 agent）
   - 不允许在主会话中直接执行代码
   - 子 agent 拿到 task brief + 验收标准
2. **One Thing**: 每轮只派发一个任务
3. **Review**: 子 agent 完成后，派 tester 验证
4. **Update Ledger**: 记录结果到 ledger.md

### Fix Loop（复用 v9.2 机制）

tester FAIL 时，进入 Fix Loop：
- R=1-3: resume implementer（fresh context）
- R=4: fresh implementer + 模型升级
- R=5: controller 裁决

## ⛔ 电路断路器（Circuit Breaker）

> Ralph 实证: "Layer your circuit breakers. Max iterations, per-iteration timeout, stuck detection."

| 断路器 | 阈值 | 触发动作 |
|--------|------|---------|
| **max_rounds** | 10 | 停止优化循环，报告用户 |
| **timeout_per_round** | 15min | 跳过当前 round，记录到 ledger |
| **stuck_detection** | 同一问题 3 轮未解决 | 升级到 controller 裁决 |
| **token_budget** | 按项目配置 | 停止并报告消耗 |

### Stuck Detection

如果同一个 finding 连续 3 轮未解决：
1. 停止自动派发
2. 协调者做 controller 裁决：
   - **escalate**: 需要人工介入
   - **workaround**: 记录到 ledger，标记为 known issue
   - **abort**: 放弃该优化，继续下一个反馈

## Ledger 扩展

ledger.md 新增两个段：

### Optimization Rounds

```
## Optimization Rounds
Round 1: 逻辑 bug → Phase 6 coder → complete (commits a1b2c3d)
Round 2: UI 问题 → Phase 6 artist → fix-round-2 (1 finding open)
Round 3: 需求变更 → Phase 1-3 重走 → in-progress
```

### Learnings（来自 Ralph 的 progress.txt 模式）

```
## Learnings
- [2026-08-07] 发现 XXX 模块的 YYY 函数有边界问题，已修复
- [2026-08-07] ZZZ 配置需要在重启后生效，不是实时的
```

## Red Flags — 这些想法意味着停下来

| 想法 | 真相 |
|------|------|
| "这个反馈简单，我直接改" | delegate_task，fresh context |
| "让我先看看代码分析一下" | Phase 8a 只读不改，分析是 coder 的活 |
| "一轮处理两个反馈效率更高" | One Thing Per Iteration，Ralph 铁律 |
| "已经跑了 8 轮了，再试一轮" | Circuit Breaker 触发，报告用户 |
| "这个 finding 上轮没解决，继续试" | 3 轮 stuck → controller 裁决 |
| "我不需要声明 skill 锚定" | 你在合理化跳步，立即停止 |

## 执行 Checklist

- [ ] 声明了 skill 锚定（反馈类型 + 路由目标）
- [ ] 只处理了一个反馈（One Thing）
- [ ] 用了 delegate_task（Fresh Context）
- [ ] 更新了 ledger.md（Optimization Round + Learnings）
- [ ] 没有在主会话直接执行代码
- [ ] 检查了 Circuit Breaker 状态

```bash
python3 scripts/gate-phase8.py <项目目录>
```
