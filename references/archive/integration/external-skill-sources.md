# 外部 Skill 源分析与集成记录

> 2026-06-08 调研。三个外部 skill 仓库的评估、选择和集成方式。

## 集成决策树

```
外部 skill 评估
├── 与现有能力重叠？→ 跳过（已有 diagnose/tdd/systematic-debugging 等）
├── 通用原则可复用？→ 安装为独立 skill + clsh-project references
├── 只在特定 Phase 有用？→ 内嵌到对应 Phase 模板（不装独立 skill）
└── 核心理念可融入现有规则？→ 融入现有铁律（如 context-engineering → Way C）
```

**核心原则：** 不嵌入 clsh-project SKILL.md（避免膨胀），不装独立 skill 当只用一次的模板。

## Token 成本分析

| 方式 | 加载时机 | Token 成本 | 适用场景 |
|------|---------|-----------|---------|
| 独立 skill | `skill_view()` 显式调用 | 0（不调用）/ ~800（调用） | 低频使用、跨项目复用 |
| 内嵌 SKILL.md | 每次加载 clsh-project | +300-500（每次） | 高频、流程强绑定 |
| 模板内嵌 Phase | Phase 执行时 | +100-200（只注入模板） | 最轻量 |

**决策：** context-engineering 用"模板内嵌 Phase"（最轻量），其他用"独立 skill + references"。

## 已评估的源

### 1. Matt Pocock (mattpocock/skills) — 120k ⭐

10 个 engineering skill + 4 个 productivity skill。

**已安装（3 个）：**

| Skill | 集成点 | 价值 |
|-------|--------|------|
| `zoom-out` | 4 个 worker AGENTS.md | 遇不熟悉代码自动触发，极轻量（31 行） |
| `handoff` | Phase 7 | 会话交接文档压缩 |
| `improve-architecture` | Phase 4 + Review Mode | 深度模块评估 + 删除测试 + 接缝分析 |

**已吸收不安装（7 个）：** diagnose、tdd、prototype、grill-with-docs、grill-me、to-issues、to-prd → 我们已有对应能力。

**不适用（3 个）：** triage、setup-matt-pocock-skills（GitHub 专用）、write-a-skill（已有 hermes-agent-skill-authoring）。

### 2. Leonxlnx (taste-skill) — 36k ⭐

14 个 skill（10 个代码生成 + 4 个图片生成）。

**已安装（2 个）：**

| Skill | 集成点 | 价值 |
|-------|--------|------|
| `taste-skill` (design-taste-frontend) | artist 派发 --skills | Anti-Slop 前端设计框架，替代模板化 UI |
| `taste-brandkit` | artist 品牌设计 | 品牌素材方向 |

**关键配置：** `DESIGN_VARIANCE`/`MOTION_INTENSITY`/`VISUAL_DENSITY` 三个旋钮，按项目类型调。

### 3. Addy Osmani (addyosmani/agent-skills) — 48.9k ⭐

23 个 skill（22 个生命周期 + 1 个 meta）。

**已安装（4 个）：**

| Skill | 集成点 | 价值 |
|-------|--------|------|
| `doubt-driven-dev` | Phase 6 Security Scan | 对抗性审查（CLAIM→EXTRACT→DOUBT→RECONCILE） |
| `security-hardening` | Phase 6 Pre-Commit | OWASP Top 10 三层边界（Always Do/Ask First/Never Do） |
| `code-simplification` | Review Mode + Phase 6 Quality | Chesterton's Fence + Rule of 500 |
| `frontend-ui-engineering` | artist AGENTS.md | WCAG 2.1 AA + Anti-AI-Aesthetic |

**已融入不安装（1 个）：** context-engineering → 融入 Way C 铁律（五层架构模板）。

**已评估不安装（18 个）：** 与现有能力重叠或不适用。

## 集成模式总结

```
clsh-project SKILL.md (665 行)
├── Phase 4: improve-architecture（Module Depth）
├── Phase 6 Step 5: doubt-driven-dev + security-hardening
├── Phase 6 Step 6: code-simplification
├── Phase 6 Pre-Commit: security-hardening（OWASP）
├── Phase 6 artist: taste-skill + frontend-ui
├── Phase 7: handoff
└── Review Mode: improve-architecture + code-simplification

Worker AGENTS.md (4 profiles)
├── Selective Include + Trust Levels
├── zoom-out（自动触发）
└── artist 额外：frontend-ui + taste-skill
```
