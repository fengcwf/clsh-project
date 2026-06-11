# 调研方法论对比研究 — 8 框架分析

> 日期: 2026-06-11 | 来源: E2E 在线教育平台 Review + 调研优化

## 背景

E2E 测试发现 clsh-project 的调研模板只覆盖"功能实现"和"技术选型"，导致 15 个问题点中 11 个被遗漏（安全/隐私/体验/权限）。研究 8 个框架的调研方法论，找到优化方向。

## 8 框架调研方法论

### Superpowers — 苏格拉底式追问
- `brainstorming` 技能，检测模糊需求自动激活
- 不预设问题清单，根据用户回答动态追问
- 追问维度：Who/What/How/Constraints

### Spec Kit — 结构化澄清 + 一致性分析
- `/speckit.clarify` 结构化澄清 underspecified areas
- `/speckit.analyze` 跨工件一致性检查（spec ↔ plan ↔ tasks）
- 最强调"Constitution"（项目宪法）

### Kiro — 用户故事 + 验收标准
- Requirements-First 或 Design-First 两种工作流
- 用户故事：`As a [role], I want [feature], so that [benefit]`
- 验收标准：`GIVEN [context] WHEN [action] THEN [result]`
- **最强调"可测试性"**

### OpenSpec — 轻量级 + 流迭代
- `fluid not rigid`、`iterative not waterfall`
- 无严格阶段门禁，随时可更新任何工件

### Ralph Loop — PRD 技能 + 自主执行
- `/prd` 技能生成详细需求文档
- PRD 直接转 `prd.json` 驱动自主执行

### GSD — 元提示 + 上下文工程
- "Your brain works faster than your keyboard"
- 自动管理上下文窗口

### Phoenix Security — 12-Role 安全规格系统
- **唯一在调研阶段覆盖安全的框架**
- 12 步流程：Context → Scope → Constraint → Requirements → **Ambiguity Hunting** → **Threat Modeling** → API Contract → **Verification Mapping** → Batch Planning → Final Gate
- 产出：RFC 2119 需求、MITRE ATT&CK 威胁模型、验证矩阵

### Trellis — 4-Phase Loop + 学习回流
- `trellis-brainstorm` 技能
- 学习成果自动回流到 `.trellis/spec/`

## 对比矩阵

| 框架 | 调研深度 | 安全覆盖 | 合规覆盖 | 用户体验 | 权限隔离 | 可测试性 |
|------|---------|---------|---------|---------|---------|---------|
| Superpowers | 中 | ❌ | ❌ | ❌ | ❌ | 低 |
| Spec Kit | 高 | ❌ | ❌ | ❌ | ❌ | 中 |
| Kiro | 高 | ❌ | ❌ | ❌ | ❌ | **高** |
| OpenSpec | 低 | ❌ | ❌ | ❌ | ❌ | 低 |
| Ralph Loop | 中 | ❌ | ❌ | ❌ | ❌ | 中 |
| GSD | 中 | ❌ | ❌ | ❌ | ❌ | 低 |
| Phoenix | **极高** | **✅** | **✅** | ❌ | **✅** | **高** |
| Trellis | 中 | ❌ | ❌ | ❌ | ❌ | 中 |

## clsh-project 借鉴

| 来源 | 借鉴内容 | 落地位置 |
|------|---------|---------|
| Superpowers | 苏格拉底式追问 | Phase 0-1 追问框架 |
| Kiro | GIVEN...WHEN...THEN | tasks.md 验收标准格式 |
| Phoenix | 威胁建模 + 验证矩阵 | Phase 0-1 安全维度 |
| Spec Kit | 跨工件一致性检查 | Phase 4 自检 |
| Trellis | 学习回流 | Phase 7 归档 |
