---
title: Anti-Rationalization Guard 重构 — 4 轮模型旋转分析
date: 2026-06-23
tags: [anti-rationalization, model-rotation, workflow-optimization]
trigger: "致远OA数据导入项目跳过 clsh-project 流程，Guard 被当成合理跳步理由清单"
models: [mimo, deepseek-r1, claude-sonnet, gemini-2.5-pro]
---

# Anti-Rationalization Guard 失效分析与重构

## 失效事件

**任务**: 致远OA数据导入 — review 代码 + 修改唯一字段逻辑（8 个文件改动）

**实际行为**: 读代码 → 问 1 个确认问题 → 直接改代码。跳过 Phase 0-8 全部流程。

**自我合理化过程**:
1. 看到"review 代码 + 调整功能" → 自动判断为"小改动"
2. 引用 Anti-Rationalization Guard 里的条目 → **确认**自己的跳步判断
3. 方向反了：Guard 应该**拦截**这些想法，我却用它来**确认**跳步

## 根因分析

| 维度 | 当前实现 | 需要的实现 |
|------|---------|-----------|
| 触发方式 | LLM 自觉去查（被动） | 想法产生时拦截（主动） |
| 存在形式 | SKILL.md 中间的一张表格 | Iron Laws（ALL CAPS 命令信号） |
| 语气 | 描述性（"不是跳过规则的理由"） | 命令性（"STOP — 你在合理化"） |
| 压力测试 | 从未测试 | Triple-Pressure 场景验证 |

## 4 轮模型旋转

| 轮次 | 模型 | 角色 | 核心贡献 |
|------|------|------|---------|
| R1 | mimo | 分析师 | 失效根因：被动→需要主动 |
| R2 | DeepSeek R1 | 设计师 | 5 层重构方案（~200 行） |
| R3 | Claude Sonnet | 批判者 | 7 条挑战，建议精简到 ~65 行 |
| R4 | Gemini 2.5 Pro | 综合者 | 最终方案 ~88 行 |

## R3 关键批判

1. **过度工程化** — 34 条规则稀释注意力。LLM 在 15 条以内遵守率最高
2. **正则检测不可行** — LLM 合理化表达无限多样，正则只能捕获冰山一角
3. **Iron Law > 用户指令** — 会制造 UX 摩擦。应定位为"高于 LLM 自判，不高于用户显式指令"
4. **Session 注入不可行** — clsh-project 是按需加载 skill，不是 session 启动加载。改用 memories/
5. **与 gate 脚本重叠** — Iron Laws 应明确定位为 prompt 级 fallback
6. **更简单替代** — 3 Iron Laws + 6 Red Flags + memories = ~65 行，80% 效果

**核心洞察**:
> "Round 2 失败的根本原因不是'规则不够多'，而是'规则太被动'。解法应该是让规则无处不在，而不是让规则更多。"

## 最终方案（已写入 SKILL.md）

- 3 Iron Laws（ALL CAPS，gate 脚本的 prompt 级 fallback）
- 6 Red Flags（命令性语气，想法产生时拦截）
- 用户覆盖协议（区分"用户书面指令"和"LLM 语气解读"）
- RF-6 反向合理化防护（拦截"用 Guard 表确认跳步"）
- memories/ 注入（替代不可行的 session 启动注入）
- 架构定位表（Guard 是 L3，gate 脚本是 L1）

## 方法论沉淀：4 轮模型旋转

适用场景：复杂方法论/架构决策，需要多视角审视

| 轮次 | 角色 | 模型选择建议 |
|------|------|------------|
| R1 | 分析师 | 当前主模型 — 基础分析 |
| R2 | 设计师 | 推理能力强的模型（DeepSeek R1, o3）— 出完整方案 |
| R3 | 批判者 | 不同模型族（Claude, Gemini）— 挑战假设 |
| R4 | 综合者 | 综合能力强的模型（Gemini Pro, Claude）— 收敛 |

关键：R3 必须用不同模型族，避免同模型系统性盲区。
