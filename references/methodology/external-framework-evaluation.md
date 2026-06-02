# 外部框架评估方法论 — LLM 依赖度测试

> 日期：2026-06-02
> 来源：Claude Code Harness + Superpowers v5.1.0 对比分析
> 用途：评估外部工具/方法论是否适合引入 clsh-project

---

## 一、LLM 依赖度测试（第一过滤器）

评估任何外部机制前，先回答一个问题：

> **这个机制在 LLM 能力下降 50% 时，是静默失败还是显式阻断？**

| 结果 | 行动 |
|------|------|
| 静默失败（产出变差但不报错） | ❌ 不得用于流程控制 |
| 显式阻断（报错/超时/escalate） | ⚠️ 可考虑，需加机械兜底 |
| 不依赖 LLM 判断 | ✅ 可直接采用 |

### 常见 LLM 依赖模式（高风险）

| 模式 | 为什么依赖 LLM | 机械替代 |
|------|---------------|---------|
| Inline self-review | LLM 自评自己写的代码 → 漏检 | 独立 tester agent |
| "只 flag 阻断级问题" | 需要 LLM 区分严重性 | 硬编码轮次上限 |
| Plateau detection | 需要 LLM 判断"是否有进展" | 固定轮次 + escalate |
| Multi-perspective debate | 多个 LLM 视角，本质还是 LLM 判断 | 预定义 checklist |
| "简单任务 inline review" | 需要 LLM 判断任务复杂度 | 所有任务统一 tester |

---

## 二、三源对比框架

对比多个外部框架时，用以下结构：

### Step 1: 机制拆解

每个框架拆成独立机制（不是整体评价），列出：
- 机制名称
- 输入/输出
- 依赖（LLM / 代码 / 人工）
- 失败模式

### Step 2: 映射到现有流程

| 外部机制 | clsh-project 现有等价 | 差距分析 |
|---------|---------------------|---------|
| 有等价 → | 不需要引入 | 记录映射关系 |
| 无等价但可借鉴 → | 分析是否值得引入 | 用 LLM 依赖度测试 |
| 无等价且 LLM 依赖 → | 不引入，找机械替代 | 记录但不采纳 |

### Step 3: 判断力归属

每个候选机制必须明确标注：
- 🤖 机械判断 — 代码/脚本可做
- 👤 人工判断 — 需要大佬确认
- 🧠 LLM 判断 — 依赖模型能力

**引入原则：** 🤖 > 👤 > 🧠。🧠 类机制需要大佬明确确认才能引入。

---

## 三、案例：Harness + Superpowers + clsh-project 三方对比（2026-06-02）

### 背景
- **Harness：** 2.5k ⭐，Plan→Work→Review→Ship，Team Debate 多视角 review
- **Superpowers v5.1.0：** 砍掉 subagent review（~25min→~30s inline），提高 review 门槛
- **clsh-project v5.12.0：** Phase 1-8，独立 tester，2 轮 Auto-Fix 上限

### 评估结果

| 外部机制 | LLM 依赖度 | 判断力归属 | 决策 |
|---------|-----------|-----------|------|
| Spec Delta / Skip Reason | 🟡 中 | 🧠 LLM 判断"是否漂移" | ⬇️ 降级观察（方案注入已前置解决） |
| Plateau Detection | 🔴 高 | 🧠 LLM 判断"是否有进展" | ❌ 不采纳（用硬编码轮次替代） |
| Team Debate 多视角 Review | 🔴 高 | 🧠 多个 LLM 视角 | ❌ 不采纳（用 checklist 替代） |
| Sprint Contract JSON | 🟢 低 | 🤖 机械 | ❌ 不采纳（task body 注入已够用） |
| Auto 模式选择 | 🟢 低 | 🤖 按数量规则 | ⏳ P2 择机采纳 |
| Session Launch Guidance | 🟢 低 | 🤖 格式化输出 | ✅ P1 采纳 |
| Inline Self-Review | 🔴 高 | 🧠 LLM 自评 | ❌ 不采纳（保留独立 tester） |

### 核心结论

Harness 和 Superpowers 的优化方向是"让更强的 LLM 做更多判断"（效率优先）。
clsh-project 的方向是"让流程不依赖 LLM 判断"（可靠性优先）。
两者不矛盾，服务不同风险偏好。

---

## 四、决策记录模板

评估外部框架后，记录到 `raw/projects/<项目>/docs/adr/`：

```markdown
# ADR-NNN: 引入/不引入 [机制名]

## 状态
[已采纳 / 观察中 / 已拒绝]

## 背景
[外部框架名 + 机制描述]

## LLM 依赖度测试结果
[静默失败 / 显式阻断 / 不依赖]

## 判断力归属
[🤖 / 👤 / 🧠]

## 决策
[引入 / 不引入 / 条件引入]

## 理由
[为什么这么决定]
```
