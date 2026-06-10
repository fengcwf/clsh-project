# 调研方法论对比 — 8 框架分析

> 来源：2026-06-10 E2E 测试复盘，分析"为什么工作流没有实现用户提出的 15 个问题点"
> 结论：11/15 项遗漏根因是调研模板缺维度

## 框架对比矩阵

| 框架 | 调研深度 | 安全覆盖 | 合规覆盖 | 用户体验 | 权限隔离 | 可测试性 |
|------|---------|---------|---------|---------|---------|---------|
| **Superpowers** | 中（动态追问） | ❌ | ❌ | ❌ | ❌ | 低 |
| **Spec Kit** | 高（澄清+分析） | ❌ | ❌ | ❌ | ❌ | 中 |
| **Kiro** | 高（用户故事） | ❌ | ❌ | ❌ | ❌ | **高** |
| **OpenSpec** | 低（轻量） | ❌ | ❌ | ❌ | ❌ | 低 |
| **Ralph Loop** | 中（PRD） | ❌ | ❌ | ❌ | ❌ | 中 |
| **GSD** | 中（元提示） | ❌ | ❌ | ❌ | ❌ | 低 |
| **Phoenix** | **极高（12步）** | **✅ 威胁建模** | **✅ RFC 2119** | ❌ | **✅ 租户隔离** | **高** |
| **Trellis** | 中（brainstorm） | ❌ | ❌ | ❌ | ❌ | 中 |
| **clsh-project** | 中（5维度） | ❌ | ❌ | ❌ | ❌ | 低 |

## 各框架调研方法论

### 1. Superpowers — 苏格拉底式提问
- `brainstorming` 技能，检测模糊需求自动激活
- 动态追问：Who/What/How/Constraints
- 不预设问题清单，根据回答追问

### 2. Spec Kit — 结构化澄清 + 一致性分析
- `/speckit.clarify` 结构化澄清 underspecified areas
- `/speckit.analyze` 跨工件一致性检查（spec ↔ plan ↔ tasks）
- 最强调"Constitution"（项目宪法）

### 3. Kiro — 用户故事 + 验收标准
- Requirements-First 或 Design-First 两种工作流
- 用户故事：`As a [role], I want [feature], so that [benefit]`
- 验收标准：`GIVEN [context] WHEN [action] THEN [result]`
- **最强调"可测试性"**，验收标准可直接转测试用例

### 4. OpenSpec — 轻量级 + 流迭代
- `/opsx:propose` 创建 proposal.md
- 核心理念：fluid not rigid / iterative not waterfall
- 无严格阶段门禁，随时可更新任何工件

### 5. Ralph Loop — PRD 技能 + 自主执行
- `/prd` 技能生成详细需求文档
- PRD 直接转 `prd.json` 驱动自主执行
- 调研→执行无缝衔接

### 6. GSD — 元提示 + 上下文工程
- "Your brain works faster than your keyboard"
- Brain dump → AI breaks into tasks → AI writes code
- 最强调"上下文工程"

### 7. Phoenix Security — 12-Role 安全规格系统
**12 步流程：**
1. Context Curation（上下文策展）
2. Scope Definition（范围定义）
3. Constraint Distillation（约束提炼）
4. Requirements Engineering（需求工程）
5. **Ambiguity Hunting（歧义狩猎）** ← 独特
6. **Threat Modeling（威胁建模）** ← 独特
7. API Contract Design（API 契约设计）
8. **Verification Mapping（验证映射）** ← 独特
9. Batch Planning（批量规划）
10. Final Gate Review（最终门禁审查）

**产出：** RFC 2119 需求、MITRE ATT&CK 威胁模型、租户隔离不变量、API 错误分类、验证矩阵

### 8. Trellis — 4-Phase Loop + 子代理
- `trellis-brainstorm` 技能写 `prd.md`
- 4-Phase：Plan → Implement → Verify → Finish
- **学习成果自动回流到 spec** ← 独特

## 关键发现

1. **只有 Phoenix 在调研阶段覆盖安全** — 威胁建模+验证映射
2. **只有 Kiro 强调"可测试性"** — GIVEN...WHEN...THEN 格式
3. **没有框架覆盖"数据隐私"** — 匿名化、删除权、合规条款
4. **没有框架覆盖"用户体验异常场景"** — 网络断开、加载失败、操作中断

## clsh-project 可借鉴点

| 框架 | 借鉴内容 | 优先级 |
|------|---------|--------|
| Phoenix | 威胁建模（攻击面识别+缓解措施） | P0 |
| Kiro | GIVEN...WHEN...THEN 验收标准格式 | P0 |
| Spec Kit | 跨工件一致性分析 | P1 |
| Trellis | 调研经验回流到模板 | P1 |
| Superpowers | 动态追问机制 | P2 |
