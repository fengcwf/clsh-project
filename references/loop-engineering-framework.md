---
version: 1.0.0
description: "Loop Engineering 框架 — 硬规则算子 vs 软规则算子分类，Hermes L4 原语对照，clsh-project 优化方向"
created: 2026-06-18
source: "骨汤鸡蛋面《从 skill 到 loop native》+ Hermes 官方文档调研"
---

# Loop Engineering 框架

## 核心主张

> **确定性交给代码，判断力交给被代码显式调用的模型。** — Boris Cherny

Loop Engineering 的本质：把结构从"模型每轮临场读"外部化成"代码钉死、模型绕不过"。

## 四级阶梯

| 级 | 形态 | 结构落在哪 | 跃迁点 |
|---|------|-----------|--------|
| L1 | skill | 流程 + 知识全在 md，模型每轮读 | md 越长指令遵循越差 |
| L2 | skill + 独立 agent | 同上，隔离上下文 | 提升指令遵循，一点并发 |
| L3 | plugin | 硬规则 → hook，软规则 → agent()/assert()；流程仍分散 | 硬规则外部化，但无统一 loop state |
| L4 | loop native | loop state / 流程 / 软硬算子 / HITL 全是一等公民 | harness 原生支持 loop |

## 算子分类（对 clsh-project 至关重要）

| 算子类型 | 性质 | clsh-project 对应 | 可被 /goal 替代？ |
|---------|------|------------------|----------------|
| **数据算子** | 只读 IO | Scout 调研、web_search | ❌ |
| **硬规则算子** | 确定性机判 | gate-phase*.py（文件存在性、关键词、行数） | ❌ 不可替代 |
| **软规则算子** | LLM 判断 | /goal judge（bug 修好了吗、功能实现了吗） | 本身就是 /goal |

**关键洞察：gate 脚本（硬规则）和 /goal（软规则）是互补关系，不是替代关系。**

- 硬规则检查"文件存在吗、关键词对吗"→ 机器判断，不能用 /goal 替代
- 软规则检查"bug 修好了吗、还有问题吗"→ LLM 判断，不应该用脚本模拟

## Hermes 已有的 L4 原语

| 原语 | 功能 | 对应文章概念 |
|------|------|------------|
| `/goal` | Ralph Loop，judge 每 turn 判断 DONE/CONTINUE | loop state + 软规则算子 |
| `/subgoal` | 追加验收标准到活跃 goal | HITL 语法 |
| kanban `--goal` | worker 被包裹在 /goal loop 中 | loop operator |
| `delegate_task(background=true)` | 异步子 agent | agent() 原语 |
| `pre/post_tool_call` hook | 插件钩子 | L3 hook |

## clsh-project 的阶梯定位

| 阶梯 | 特征 | clsh-project 现状 |
|------|------|------------------|
| L1 | 流程全在 md | Phase 1-3 是 L1 |
| L2 | 隔离上下文 | kanban worker 独立 profile ✅ |
| L3 | 硬规则进 hook | Gate 脚本 + hash 码（脚本硬编码，非 hook） |
| **L4** | loop state + 流程 + HITL | **✅ /goal + /subgoal + kanban --goal 已有但未充分利用** |

## /goal 适用性（按场景）

| 场景 | 适合？ | 原因 |
|------|:---:|------|
| Phase 1-6 完整流程 | ❌ | 终止权在人（确认码），单次任务 |
| **Phase 8 反馈循环** | **✅** | 多轮迭代，LLM 判断"还有 bug 吗" |
| **fix 修复卡** | **✅** | 迭代直到收敛，节省来回开销 |
| Review Mode 修复 | ✅ | 同 Phase 8 结构 |
| coder 实现卡 | ❌ | 单 shot 足够 + C3 独立测试冲突 |
| tester 验证卡 | ⚠️ | 仅测试本身需调试时 |
| Scout 调研 | ⚠️ | 当前 delegate_task 够用 |

## 软规则硬化路径

Loop Engineering 的复利：**loop 越成熟，软规则承担的即兴判断越少。**

```
今天：/goal judge 判断"bug 修好了吗"（软规则）
  ↓ 沉淀
明天：gate-phase8.py 脚本检查"测试全部 PASS"（硬规则）
  ↓ 沉淀
后天：CI/CD pipeline 自动跑测试（完全自动化）
```

clsh-project 的 gate 脚本就是这个"软→硬"过程的产物。

## 参考

- 原文: `raw/01-articles/从 skill 到 loop native：我理解的 Loop Engineering.md`
- 分析报告: `raw/01-articles/Loop Engineering 分析：文章验证 + clsh-project 定位.md`
- /goal 适用性: `raw/projects/clsh-project/references/goal-mode-analysis.md`（v2.0）
- Hermes /goal 文档: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals
- kanban --goal commit: `0cd7d54b0`
