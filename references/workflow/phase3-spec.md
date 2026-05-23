# clsh-project — Phase 3+4: 设计文档与自检

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 3: 写设计文档 + Constitution

**目标：** 将需求和选定方案转化为详细的技术设计文档。

### 文件位置

```
wiki/projects/<项目名>/
├── overview.md
├── source-of-truth/
│   ├── constitution.md
│   └── <capability>.md
└── changes/
    └── YYYY-MM-DD-<变更名>/
        ├── proposal.md
        ├── conversation.md
        ├── spikes/          ← Phase 2.5 产出
        └── tasks.md
```

### 创建 Constitution（Phase 3 必做）

Constitution 是项目级的"宪法"，定义 AI worker 必须遵守的技术约束。

**轻量版（小项目）：**
```markdown
---
title: "[项目名] 项目约束"
date: YYYY-MM-DD
type: constitution
project: "[项目名]"
---

# [项目名] 项目约束

- **技术栈：** [一句话描述]
- **代码规范：** [关键规则]
- **架构：** [核心约束]
- **禁止：** [最重要的 2-3 条]
```

**完整版模板：** 见 `references/templates/constitution-template.md`

### 🎨 设计发散（UI 项目可选，借鉴 gstack /design-shotgun）

**适用条件：** 项目有前端 UI 且设计方向未确定（Phase 1 无明确视觉参考）。

**时机：** Constitution 创建后、Phase 4 自检前。

**流程：**
1. 灵犀用 `skill_view('sketch')` 加载 throwaway mockup skill
2. 生成 **2-3 个设计变体**的 HTML mockup（不需要完美，快速迭代）
   - 变体 A：保守方案（符合行业惯例）
   - 变体 B：大胆方案（差异化设计）
   - 变体 C（可选）：混合方案
3. 每个变体控制在单文件 HTML（<30KB），可直接浏览器打开
4. 截图后发给大佬选择方向
5. 大佬选择后，将设计方向写入 constitution.md 的 UI 约束章节

**不做此步骤的情况：**
- 大佬已提供明确设计参考（"类似 Linear"）
- 纯后端/API 项目
- 大佬说"简单做一下"

---

## Phase 4: 设计文档自检 + 大佬 Review

### ⛔ 流程合规检查

1. Phase 1 是否完成？
2. Phase 2 是否完成？
3. Phase 2.5（如触发）是否完成？
4. Phase 3 是否完成？
5. 是否有跳步？
6. 代码是否已提前编写？

**如果以上任何一项为 NO → 停止，补全缺失的 Phase。**

### 文档质量自检

1. **Placeholder 扫描** — 有无 "TBD"、"TODO"、"implement later"？
2. **内部一致性** — 各章节是否矛盾？架构与功能描述是否匹配？
3. **范围检查** — 是否过大需要拆分？
4. **歧义检查** — 是否有需求可被两种解读？
5. **需求覆盖** — Phase 1 的每个需求是否都有对应设计？
6. **Type Consistency** — 跨章节的类型/接口/命名是否一致？

### 大佬 Review Gate

自检通过后，向大佬确认：

> "设计文档已写入 `wiki/projects/<项目名>/changes/<变更名>/`，请 review。确认无误后我开始写实现计划。"

**等待大佬确认后才进入 Phase 5。**

### 🔍 自动路径检查（Q1 改进 — 2026-05-19）

**每次写入文件后，必须执行路径验证：**

```bash
# 写入文件后立即验证
ls -la <声明路径>
# 确认文件存在且大小 > 0
```

**Phase 3 写入验证清单：**
- [ ] `proposal.md` 已写入 `wiki/projects/<项目名>/changes/<变更名>/` → `ls` 验证
- [ ] `constitution.md` 已写入 `wiki/projects/<项目名>/source-of-truth/` → `ls` 验证
- [ ] 文件大小 > 0（非空文件）

**Phase 6 产出物验证清单：**
- [ ] 代码文件已写入声明的绝对路径 → `ls` 验证
- [ ] 测试文件已写入 → `ls` 验证
- [ ] 产出物路径使用绝对路径（禁止相对路径）

**⛔ 路径错误 = 流程违规，必须记 ERRORS.md**

> ⚠️ **教训（2026-05-15）：** write_file 使用相对路径，文件落到 skill references/ 目录而不是 wiki/projects/ 目录。写入后未 `ls` 验证，导致虚假汇报。
