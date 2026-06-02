# Matt Pocock Skills — clsh-project 借鉴分析

**来源：** https://github.com/mattpocock/skills (103k ⭐, MIT)
**分析日期：** 2026-05-24
**分析文档：** `raw/projects/clsh-project-analysis-mattpocock-skills.md`

## 项目概述

Matt Pocock 的 Skills 是面向 Claude Code 的工程 skill 集合，核心理念来自《The Pragmatic Programmer》《Domain-Driven Design》《A Philosophy of Software Design》。强调小、可组合、基于工程基本功。

## 已采纳的模式

### 1. CONTEXT.md 共享领域语言
- **来源：** `grill-with-docs` skill
- **用途：** 项目术语表，减少歧义和 token 消耗
- **clsh-project 集成：** Phase 1 需求澄清时自然积累，模板见 `references/templates/context-template.md`
- **规则：** 只收录项目特有术语（不是通用编程概念），一词一义，列出要避免的同义词

### 2. ADR 架构决策记录
- **来源：** `grill-with-docs/ADR-FORMAT.md`
- **用途：** 记录难逆转的架构决策及原因
- **clsh-project 集成：** Phase 3 设计确认时，满足 3 条件才创建
- **创建条件：** (1) 难逆转 (2) 令人意外 (3) 有真实取舍
- **模板：** `references/templates/adr-template.md`

### 3. 代码交叉验证
- **来源：** `grill-with-docs` 的 "Cross-reference with code"
- **用途：** Phase 1 大佬描述现有行为时，必须检查代码验证
- **集成位置：** 流程铁律 #12

### 4. Vertical Slice 任务切分
- **来源：** `to-issues` skill
- **用途：** Phase 5 任务切分遵循端到端薄切片原则
- **关键概念：**
  - 每个 Task 是端到端的薄切片（schema → API → UI → tests），不是水平层
  - 完成后可独立验证/演示
  - HITL（需人工）vs AFK（可自动）分类
  - 宁可多切薄片，不要少切厚片

### 5. 可运行 Prototype（UI 设计发散升级）
- **来源：** `prototype` skill
- **用途：** Phase 2.5 / Phase 3 设计发散从截图升级到可运行原型
- **两条分支：**
  - 逻辑原型：终端 app 测试状态机/数据模型
  - UI 原型：多个变体同一路由切换，一条命令运行
- **规则：** 从第一天就标记为"一次性"，无持久化，做完就删或吸收
- **Token 分析：** 交互原型比截图方案省 token（一次生成 vs 每轮重新截图）

### 6. Module Depth 评估
- **来源：** `improve-codebase-architecture` skill
- **用途：** Phase 4 自检增加设计质量检查
- **关键概念：**
  - 删除测试：删掉模块后复杂度是消失（= 透传）还是扩散（= 有价值）？
  - 接口深度：核心模块的接口是否比实现简单得多？
  - 深模块 = 高杠杆（简单接口 + 丰富行为）

### 7. Handoff 文档
- **来源：** `handoff` skill
- **用途：** Phase 7 归档时生成 handoff.md，方便跨 session 续接
- **规则：** 引用已有文档不重复，脱敏处理，建议下次加载的 skills

## 未采纳的模式及原因

| 模式 | 原因 |
|------|------|
| Issue Tracker 集成 | clsh-project 用 Kanban 而非 GitHub Issues |
| Triage 状态机 | clsh-project 用 Kanban 状态 + Phase 门禁 |
| `/setup-matt-pocock-skills` | clsh-project 有自己的初始化流程 |
| `/caveman` 压缩模式 | Hermes 有独立的 token 优化机制 |

## 参考资料

- 原始分析文档：`raw/projects/clsh-project-analysis-mattpocock-skills.md`
- CONTEXT-FORMAT.md：https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md
- ADR-FORMAT.md：https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/ADR-FORMAT.md
- prototype skill：https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype
- to-issues skill：https://github.com/mattpocock/skills/tree/main/skills/engineering/to-issues
