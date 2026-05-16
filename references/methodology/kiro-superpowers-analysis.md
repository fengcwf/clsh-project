# Kiro & Superpowers & Phoenix 工作流分析

## 来源
- **Kiro** (AWS): https://github.com/kirodotdev/Kiro — Spec-Driven Development IDE
- **Superpowers** (obra): https://github.com/obra/superpowers — Agentic Skills Framework
- **Phoenix** (Lucasmantou): https://github.com/Lucasmantou/phoenix-immortal — AI Agent 完整架构设计
- **DeepSeek/MiMo/Qwen 研究**: raw/02-papers/ 4篇研究笔记

## Kiro 的核心流程
1. **Requirements** → `requirements.md` (EARS notation, user stories with acceptance criteria)
2. **Design** → `design.md` (technical architecture, component design)
3. **Tasks** → `tasks.md` (discrete implementation steps)
4. **Execution** → dependency graph analysis + wave-based parallel execution

**特点：** 三阶段线性推进，每阶段有文件产出，任务支持并行执行。审批门禁不可跳过。

## Superpowers 的核心流程
1. **Brainstorming** → Explore context → Ask questions (one at a time) → Propose 2-3 approaches → Present design sections → Write design doc → Spec self-review → User review gate
2. **Writing Plans** → Bite-sized tasks (2-5 min each), exact file paths, complete code, TDD
3. **Subagent-Driven Development** → Fresh subagent per task + two-stage review (spec compliance → code quality)
4. **Finishing** → Final integration review → merge/PR

**特点：** 渐进式提问（一次一个），设计文档有 self-review + user review 双重门禁，执行阶段每个任务独立 subagent + 双重 review。

## Phoenix 的核心架构
1. **Executor 执行管道**：8 阶段流水线（TaskDecomposer → PreApprover → MicroCompact → CreditMonitor → API调用 → DeepCompact → ResponseCache → ParallelExecutor）
2. **自愈系统**：抗体库 + 错误处理器 + 进化引擎
3. **熔断机制**：连续 3 次失败 → 熔断 → 冷却 → 恢复
4. **状态持久化**：工作流状态持久到磁盘，断电重启自动续上

**特点：** 分层解耦，每层职责明确。流程控制权在代码，不在 LLM。

## 共同理念
- 需求 → 设计 → 计划 → 执行，不能跳步
- 文档是锚点，防止进度丢失和跑偏
- 分阶段审批，每阶段需用户确认
- 任务应该是 bite-sized
- **流程控制权在代码，不在 LLM**（Phoenix/DeepSeek/MiMo/Qwen 共同结论）

## clsh-project 的选择

| 维度 | 采用自 | 说明 |
|------|--------|------|
| 需求澄清 | Superpowers | 一次一个问题，多选优先 |
| 方案对比 | Superpowers | 2-3 方案 + 推荐理由 |
| 设计文档 | Kiro | 结构化模板，含需求摘要 |
| 自检清单 | Superpowers | placeholder/一致性/范围/歧义/覆盖 |
| 实现计划 | Superpowers | bite-sized，精确文件路径 |
| 执行方式 | Hermes Kanban + Phoenix 状态机 | 状态机执行模式 + checkpoint 机制 |
| Review Gate | Superpowers + Phoenix | spec compliance + code quality + checkpoint 验证 |
| 反馈循环 | Phoenix 自愈系统 | Bug 修复 / 体验优化 / 新需求三条路径 |

## 关键认知

> "LLM 不会'遵守规则'，只会'预测下一个 token'。要让 Agent 严格按流程执行，必须把'要求'转化为可计算的状态流转+验证阻断+上下文锚定，而非依赖 Prompt 的语气强度。" — Qwen 研究

> "永远不要靠'告诉'Agent 来保证流程，要靠'限制'Agent 能做到的事来保证。" — DeepSeek 研究

> "把流程控制权交给代码，把 LLM 降级为单步执行器，是解决 skill 执行跑偏的最可靠架构模式。" — MiMo 研究

## 完整分析报告
- `wiki/syntheses/2026-05-12-00-41-kiro-superpowers-workflow-analysis.md`
- `wiki/syntheses/2026-05-15-clsh-project-optimization-v2.3.0.md`
- `references/agent-skill-execution-research.md`
