# Anti-Deviation Patterns — 8 框架调研

**日期**: 2026-06-10
**来源**: Superpowers、GSD、Ralph Loop、Kiro、gstack、Spec Kit、OpenSpec、Trellis

---

## 核心发现

**没有任何框架能纯靠 prompt 实现真机械防偏离。** 真正有效的机制都跳出 prompt：
1. 工具调用拦截（GSD PreToolUse、Hermes pre_tool_call）
2. 进程隔离（Ralph Loop 每次全新进程）
3. 不信任 review（Superpowers fresh-context reviewer）

---

## Tier 1: 真机械（LLM 绕不过）

| 框架 | 机制 | 原理 |
|------|------|------|
| GSD | PreToolUse hook | Claude Code hook 在工具调用前拦截，阻断工作流目录外的文件编辑 |
| GSD | 包合法性门禁 | 三层检查（research audit → plan checkpoint → execution stop），防止 AI 幻觉包 |
| Ralph Loop | bash 循环 + 进程隔离 | 每次迭代 `claude -p` 全新进程，零上下文继承。exit code 控制流程 |
| Ralph Loop | 反压机制 | test/lint/types 失败 = exit code 非零 = 阻断提交 |
| Kiro | userInput 工具 | IDE 级阻断：agent 必须暂停等待人确认 |
| Kiro | SMT 求解器 | LLM + 形式逻辑验证需求一致性（歧义检测、矛盾检测、完整性检查） |

---

## Tier 2: 结构性约束（减少偏离空间）

| 框架 | 机制 | 原理 |
|------|------|------|
| Superpowers | 上下文隔离 | 每个子 agent 零上下文启动，coordinator 必须粘贴完整任务文本 |
| Superpowers | 两阶段 review | Spec Compliance（你造对了吗？）→ Code Quality（你造好了吗？），串行不可跳过 |
| Superpowers | 不信任模型 | reviewer prompt 明确写"implementer 可能撒谎，你必须独立验证一切" |
| GSD | Command Routing Hub | 确定性路由层，6 值 errorKind 枚举，永不抛异常 |
| Trellis | verify sub-agent | 独立子 agent 跑 lint/tests，对比 spec 检查 diff |

---

## Tier 3: Prompt 约束（LLM 自觉遵守）

| 框架 | 机制 | 原理 |
|------|------|------|
| Superpowers | skill 自动触发 | 描述只写"何时用"，不写摘要（防 LLM 走捷径只看描述不读正文） |
| gstack | 角色人格 | CEO/EM/Engineer/QA/DevOps 六角色，每个角色约束响应空间 |
| Spec Kit | 模板约束 | 结构化 Markdown 模板强制输出格式 |
| OpenSpec | 轻量 spec 层 | proposal → specs → design → tasks，流式迭代 |

---

## 框架详情

### Superpowers (obra/superpowers, 223k stars)

**创建者**: Jesse Vincent (obra)
**核心理念**: "The workflow is the source of truth"

**防偏离机制**:
- Brainstorming gate: 必须先完成 brainstorming → spec → user approval 才能写代码
- Context isolation: 子 agent 零上下文，coordinator 粘贴完整任务文本
- 两阶段 review: Spec Compliance → Code Quality，串行
- 不信任模型: reviewer prompt 写"implementer 可能撒谎"
- Verification before completion: "没有新鲜验证证据不许声称完成"，含 24 条历史失败记忆
- Skill auto-trigger: 描述只写"何时用"，防 LLM 走捷径

### GSD (gsd-build/get-shit-done, 64k stars)

**创建者**: TÂCHES
**核心理念**: Tool-call boundary enforcement

**防偏离机制**:
- PreToolUse hook: Claude Code hook 阻断工作流目录外的文件编辑（真机械）
- 包合法性门禁: 三层检查防止 AI 幻觉包（slopsquatting）
- Command Routing Hub: 确定性路由，永不透明降级
- 新鲜上下文 per agent: 每个 spawned agent 200K token 干净窗口
- Drift-guard tests: 单一真相源由 anchored tests 强制

### Ralph Loop (Geoffrey Huntley)

**核心理念**: 进程隔离 + 反压

**防偏离机制**:
- bash 循环: 每次迭代 `claude -p` 全新进程，零上下文继承
- 反压机制: test/lint/types 失败 = exit code 非零 = 阻断提交
- 文件系统状态: `progress.txt` 外部化，无上下文污染
- 迭代上限: 防止无限循环

### Kiro (Amazon/AWS)

**核心理念**: Spec-driven + IDE-level enforcement

**防偏离机制**:
- userInput 工具: IDE 级阻断，agent 必须暂停等待人确认
- SMT 求解器: LLM + 形式逻辑验证需求一致性
- Spec 文件持久化: `.kiro/specs/` 提交到 Git
- System prompt 硬规则: "MUST NOT proceed without explicit user approval"

---

## clsh-project 映射

| 框架机制 | clsh-project 对应 | 当前状态 |
|---------|------------------|---------|
| GSD PreToolUse | Gate Enforcer Plugin | ✅ 已实现 |
| Superpowers 不信任模型 | C7 Fresh-Context Reviewer | ✅ 已实现 |
| Ralph Loop 进程隔离 | Phase 边界上下文重载 | ✅ 已实现 |
| GSD 包合法性门禁 | Anti-Rationalization Guard | ✅ 已实现 |
| Superpowers 验证前置 | 验证证据模板 | ✅ 已实现 |
| gstack 角色约束 | 灵犀禁止行为表 | ✅ 已实现 |

---

## 参考链接

- Superpowers: https://github.com/obra/superpowers
- GSD: https://github.com/gsd-build/get-shit-done
- Kiro: https://kiro.dev/docs
- Spec Kit: https://github.com/github/spec-kit
- OpenSpec: https://github.com/Fission-AI/OpenSpec
- Trellis: https://github.com/mindfold-ai/Trellis
- gstack: https://github.com/garrytan/gstack
