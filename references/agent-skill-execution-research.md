# Agent Skill 执行跑偏问题 — 研究笔记

> 来源：raw/02-papers/ 4篇研究 + raw/01-articles/Phoenix不死鸟
> 整理时间：2026-05-15

## 核心问题

为什么 Agent 执行 Skill 时会跑偏？如何从架构层面锁死流程？

## 跑偏根因（4篇研究共同结论）

| 原因 | DeepSeek | MiMo | Qwen | Phoenix |
|------|----------|------|------|---------|
| 上下文窗口侵蚀（早期指令被稀释） | ✅ | ✅ | ✅ | — |
| LLM 主动性偏差（"走捷径"） | ✅ | ✅ | ✅ | — |
| Skill 缺少状态机/边界定义 | ✅ | ✅ | ✅ | ✅ |
| 框架 Re-planning 机制干扰 | — | ✅ | ✅ | — |
| 工具返回结果"诱惑"偏离 | — | ✅ | — | — |
| 自然语言指令的隐式歧义 | — | ✅ | ✅ | — |

## 解决方案（按实施强度排序）

### 方案1：黑箱封装（最可靠）
将整个严格流程写成不可分割的代码函数，Agent 只调一次，内部全控制。

### 方案2：外部编排层（推荐）
用代码控制流程，LLM 只负责每一步的具体执行。流程控制权在代码，不在 LLM。

```python
class SkillOrchestrator:
    def run(self):
        for i, step in enumerate(self.steps):
            result = self.agent.execute(instruction=step.instruction)
            if not step.validate(result):
                result = self.agent.execute(instruction=f"验证失败，请修正：{step.validation_criteria}")
```

### 方案3：可验证的状态机
每个步骤有明确的 checkpoint、验证条件、失败阻断。

```
Task 开始 → agent 执行 → 输出 CHECKPOINT → 验证 → PASS/FAIL
```

### 方案4：上下文重注入
每 N 轮对话后重新注入关键约束，防止指令被稀释。

### 方案5：结构化输出约束
强制模型输出结构化 JSON，让偏离行为可检测、可拦截。

## Phoenix 不死鸟架构借鉴

### Executor 执行管道（8阶段）
```
TaskDecomposer → PreApprover → MicroCompact → CreditMonitor → API调用 → DeepCompact → ResponseCache → ParallelExecutor
```

### 自愈系统
- **抗体库**：预定义错误处理规则集，犯过的错误不会再犯
- **错误处理器**：10步系统化排查法
- **进化引擎**：分析成功/失败案例，自动生成新规则

### 熔断机制
连续 3 次失败 → 熔断（open）→ 60秒冷却 → 半开（half-open）→ 成功 → 恢复（closed）

### 状态持久化
工作流状态持久到磁盘，断电重启自动续上。

## 对 clsh-project 的具体改进

1. **Checkpoint 机制**：每个 Task 完成后必须输出 CHECKPOINT
2. **灵犀验证环节**：agent 完成 → 灵犀验证 checkpoint → tester 验证 → 完成
3. **状态机执行模式**：流程控制权在灵犀（代码），不在 agent（LLM）
4. **Phase 8 反馈循环**：大佬测试反馈 → 记录 → 派 agent → tester 验证
5. **角色分离**：后端→coder，前端→coder，UI→artist，测试→tester，灵犀只协调

## 关键认知

> "LLM 不会'遵守规则'，只会'预测下一个 token'。要让 Agent 严格按流程执行，必须把'要求'转化为可计算的状态流转+验证阻断+上下文锚定，而非依赖 Prompt 的语气强度。" — Qwen 研究

> "永远不要靠'告诉'Agent 来保证流程，要靠'限制'Agent 能做到的事来保证。" — DeepSeek 研究

> "把流程控制权交给代码，把 LLM 降级为单步执行器，是解决 skill 执行跑偏的最可靠架构模式。" — MiMo 研究

## 参考链接
- `raw/02-papers/deepseek-agent-skill.md` — DeepSeek 分析
- `raw/02-papers/mimo-agent-skill.md` — MiMo 分析
- `raw/02-papers/qwen-agent-skill.md` — Qwen 分析
- `raw/01-articles/Phoenix不死鸟.md` — Phoenix 完整架构
