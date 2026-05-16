# Ralph Loop 调研笔记 — 与 clsh-project 的融合

> 调研时间：2026-05-16
> 来源：Vercel Labs ralph-loop-agent、Geoffrey Huntley 原始方法论、Boris Cherny (Anthropic)、Decoding AI、Agent Factory

## 核心概念

**Ralph Loop**（全称 Ralph Wiggum Loop）是一种自主迭代循环模式：

```
while (true):
  agent 执行任务
  verifyCompletion()
  如果未完成 → 注入反馈 → 重试
  如果完成 → 退出
```

**核心洞察：** "Ralph is a Bash loop." — Geoffrey Huntley

## 三种失败模式及对策

| 失败模式 | 表现 | Ralph 对策 |
|---------|------|-----------|
| **Context Rot** | 长会话积累垃圾，丢失原始规范 | 每轮 fresh context + 重新加载 spec |
| **Premature Exit** | agent 看到进度就宣布完成 | 外部客观信号（测试/checker） |
| **Single-Pass Fragility** | 一次失败不可恢复 | 迭代直到验证通过 |

## 两种实现

### A. Stop Hook 模式（Claude Code 插件）
- 拦截 agent 退出信号
- 检查 completion promise（如 "All tests passing"）
- 未达成则 reinject 提示
- **缺点**：长会话 context 溢出

### B. Bash 循环模式（推荐）
```bash
while true; do
  cat PROMPT.md | claude  # 每次 fresh context
  if grep -q "DONE" output.txt; then break; fi
done
```
- 每次迭代全新 agent 实例
- 文件系统 + git 作为记忆层
- **彻底解决 context rot**

## 与 clsh-project Phase 6 的映射

| Ralph Loop | clsh-project Phase 6 |
|-----------|---------------------|
| Agent 执行 | coder/artist subagent |
| verifyCompletion | 灵犀验证 CHECKPOINT |
| 反馈注入重试 | FAIL → 返回 Step 2（max 2轮） |
| completion promise | CHECKPOINT: PASS |
| Bash 循环编排 | 灵犀（代码）编排 LLM |
| 测试作为客观信号 | tester 卡 + 安全扫描 |

## 关键原则

1. **流程控制权在代码，不在 LLM** — 灵犀是循环编排者，agent 是单步执行器
2. **客观验证，不自判** — 用测试/checker 作为完成信号，不让 agent 自评
3. **Fresh context 每轮** — 避免 context rot 导致质量下降
4. **文件系统 + git 是记忆层** — 不依赖 agent 上下文记忆
5. **安全边界** — max-iterations + 不可逆操作前人工确认

## 生产案例

- OpenAI Codex 团队：100 万行代码 / 1500 个 PR，零人工代码
- Geoffrey Huntley：14 小时自主 React v16→v19 迁移
- Anthropic：Boris Cherny 官方推广

## 安全警告

> "These loops are safe when repo-contained and the toolchain acts as the judge. They get dangerous with irreversible side effects outside the repo."

**Rule:** 如果循环可能破坏共享状态（数据库、生产环境、基础设施），每轮计划必须人工审查。

## 参考链接

- https://github.com/vercel-labs/ralph-loop-agent
- https://github.com/fstandhartinger/ralph-wiggum
- https://www.decodingai.com/p/ralph-loops
- https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/ralph-wiggum-loop
