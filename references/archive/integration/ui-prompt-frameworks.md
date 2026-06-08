# UI 设计 Prompt 框架

## 概述

三个主流 UI 设计 prompt 框架，用于 Phase 3 设计发散阶段生成高质量 prompt。

## 1. RTCF 框架（UXMagic）

| 层 | 作用 | 示例 |
|---|------|------|
| **R**ole | 锚定专业身份 | `"Act as a Senior Product Designer specialized in enterprise fintech."` |
| **T**ask | 明确目标 | `"Generate a responsive crypto trading dashboard."` |
| **C**ontext | 关键约束 | `"Dark Mode. High-frequency trader. Needs order book, execution history. Use Nexus design system tokens."` |
| **F**ormat | 输出格式 | `"Export as Figma Auto Layout. Separate Order Entry and Market Data modules."` |

### 关键洞察
- **Flow Mode**：设计体验流而不是单屏 → `Login → Dashboard → Error State`
- **Sectional Editing**：局部重生成而不是整屏重做
- **Design System Token**：必须量化到具体 token，否则 AI 会"漂移"

## 2. v0 三要素框架（Vercel）

```
Build [产品表面：组件、数据、操作].

Used by [谁],
in [什么场景],
to [做什么决策].

Constraints:
- 平台/设备
- 视觉调性
- 布局假设
```

### 完整示例
```
Build a support dashboard showing: open tickets count,
average response time, tickets by priority (high/medium/low),
agent performance list with current workload, recent ticket activity feed.

Used by support team leads (managing 5-10 agents),
on their phones while walking the floor,
to prevent agent burnout and maintain response-time SLAs.

Constraints:
Mobile-first, light theme, high contrast.
Color code by priority: red for urgent, yellow for medium, green for low.
Show agent status badges (busy/available).
Maximum 2 columns on mobile.
```

### 效果差异
好 prompt 比烂 prompt 快 30-40%，少 150 行代码，省 1.5 credits。

## 3. Stitch Prompt Guide（Google 官方）

### 核心原则
- **高层 vs 细节**：复杂 app 先高层再逐屏细化
- **用形容词定调性**：`"A vibrant and encouraging fitness tracking app."`
- **逐屏迭代，一次改一两处**
- **用 UI/UX 术语**：`navigation bar`、`call-to-action button`、`card layout`
- **精确引用元素**：`"primary button on sign-up form"`

## 4. DESIGN.md — Google 开源设计系统规范

2026 年 4 月开源，专为 AI Agent 读取设计系统而生。

### 9 个核心 Section
1. Brand & Style — 品牌调性、目标受众
2. Colors — 色彩体系 + 语义用法
3. Typography — 字体层级 + 中英文搭配
4. Layout & Spacing — 栅格 + 间距规范
5. Elevation & Depth — 阴影/层级
6. Components — 组件规范 + 状态
7. Icons & Imagery — 图标风格
8. Motion — 动效规范
9. Accessibility — 无障碍要求

### 相关资源
- [awesome-design-md](https://github.com/voltagent/awesome-design-md) — 知名品牌 DESIGN.md 合集
- [stitch-prompt](https://github.com/dalmaer/stitch-prompt) — CLI 模板工具

## 组合使用模板

```
Role: Act as a Senior Product Designer for [领域].

Task: Generate a [具体页面] for [产品描述].

Context:
- Target users: [用户画像 + 使用场景]
- Core modules: [核心功能模块]
- Design system: [颜色/字体/圆角/间距规范]
- Layout: [布局结构]
- Visual style: [参考产品 + 关键视觉特征]
- Animations: [动效要求]

Format:
- Device: [Desktop/Mobile]
- Grid: [栅格规范]
- Export: [HTML/CSS / Figma Auto Layout]
```
