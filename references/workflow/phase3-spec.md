# clsh-project — Phase 3+4: 设计文档与自检

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 3: 写设计文档 + Constitution

**目标：** 将需求和选定方案转化为详细的技术设计文档。

### 文件位置

```
raw/projects/<项目名>/
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

### 🎨 设计发散（UI 项目必做）

**适用条件：** 项目有前端 UI 且设计方向未确定（Phase 1 无明确视觉参考）。

**时机：** Constitution 创建后、Phase 4 自检前。

**⛔ 不做此步骤的情况：**
- 大佬已提供明确设计参考（"类似 Linear"）
- 纯后端/API 项目
- 大佬说"简单做一下"

#### 流程

1. **获取设计参考**（二选一）：
   - 大佬提供参考图 → `vision_analyze` 提取设计参数（颜色、字体、间距、圆角）→ 匹配 Open Design 设计系统
   - 大佬无明确参考 → 根据项目类型推荐设计系统（见下方选择表）

2. **读取设计 tokens**：
   - 从 `/opt/open-design/design-systems/<name>/DESIGN.md` 获取语义 tokens
   - 从 `/opt/open-design/design-systems/<name>/tokens.css` 获取 CSS 变量
   - 将 tokens 注入 HTML mockup 的 `:root` 块

3. **读取 Open Design 知识包 → 本地渲染 2-3 个 HTML mockup 变体**
   - **⛔ 跳过此步骤 = 流程违规（2026-05-29 教训）** — 灵犀曾手写 HTML 颜色/间距，效果远差于 Open Design tokens。大佬确认："glass布局+配色，比你之前自己生成的好很多"。知识包加载是强制步骤，不是可选
   - **⛔ 禁止用 html-anything 通用模板做复杂 UI mockup** — 效果差、缺乏层次感、扁平化。html-anything 只适合封面图/卡片，不适合 Dashboard/管理后台等复杂 UI
   - **⛔ 禁止通过 Open Design API 调 hermes CLI**（自己调自己，浪费 token + 时间）
   - **✅ 读取完整知识包后直接渲染**（质量 70 分→90 分）：
     1. `tokens.css` — CSS 变量值
     2. `DESIGN.md` — 9 节设计规范（颜色/字体/布局/组件/动效/反模式）
     3. `SKILL.md` — 构建工作流 + 布局规则 + 自检清单
     4. `example.html` — 参考实现
     5. `craft/*.md` — 质量底线（anti-ai-slop / state-coverage / laws-of-ux）
   - 详细流程见 `references/pitfalls/ui-design-workflow.md`
   - 每个变体用不同设计系统（如 glassmorphism + linear-app + shadcn）
   - 每个变体控制在单文件 HTML（<30KB），自包含（inline CSS，用 var() 引用 tokens）
   - 灵犀直接渲染（不需要派 agent），除非需要复杂交互原型才派 artist

4. **展示给大佬选择（两种方式，优先交互原型）：**
   - **✅ 首选：交互原型** — 生成可切换变体的单文件 HTML（N 套 CSS + 切换 JS），放到 `/opt/Workspace/src/public/test/<项目名>/`，通过 Fastify 发链接：`https://wp.www.fengcwf.cn/test/<项目名>/<文件>.html`。大佬直接在浏览器切换变体对比，零额外 token。
   - **备选：截图** — 用 `chromium-browser --headless --screenshot` 截图发飞书（当大佬无法访问外网时）
   - ⛔ **禁止发送 HTML 文件路径** — 飞书无法直接打开 HTML
   - 截图命令：`chromium-browser --headless --disable-gpu --screenshot=/root/mockups/out.png --window-size=1440,900 --no-sandbox file:///path/to/mockup.html`
   - ⚠️ AppArmor 限制：snap 版 chromium 无法写入 /tmp，截图路径用 /root/mockups/

5. **大佬选择方向 + 修改意见** → 将设计方向写入 constitution.md 的 UI 约束章节

6. **记录设计 ADR（满足条件时）** — 如果选择的设计方向满足 ADR 三条件（难逆转 + 令人意外 + 有真实取舍），记录到 `raw/projects/<项目名>/docs/adr/`。模板：`references/templates/adr-template.md`

7. **如果大佬不满意** → 迭代修改 HTML mockup，重复 4-5

#### Open Design 设计系统选择表

| 大佬偏好/参考 | 设计系统 | 主色 | 风格 |
|-------------|---------|------|------|
| 类 AI UI Kit / Ant Design / 企业级 | `ant/` | `#1677FF` | 企业级、数据密集、专业 |
| 类 Linear / Notion / 极简 | `shadcn/` | `#000000` | 极简、黑白、大量留白 |
| 类 Vercel / 暗色仪表板 | `dashboard/` | `#0ea5e9` | 暗色分析面板、数据驱动 |
| 类 Stripe / 优雅 | `stripe/` | `#635bff` | 专业、优雅 |
| 类 Apple / 软质感 | `apple/` | 系统蓝 | 软质感、圆润 |
| 类 GitHub / 开发者 | `github/` | — | 开发者友好 |

**匹配方法：** 大佬发参考图 → vision_analyze 提取主色 → 在 tokens.css 中搜索最接近的设计系统。

#### 设计工具链（2026-05-24 更新）

| 工具 | 用途 | 适用场景 |
|------|------|---------|
| **Open Design** | **所有设计需求（首选）** | Dashboard、管理后台、产品原型、封面图、卡片。152 设计系统 + tokens 精确匹配 |
| **图片模型（Grok/Gemini）** | UI 效果图生成 | 高保真效果图、概念图。需 OpenRouter credits 或 Gemini API Key |
| popular-web-designs | 品牌风格参考 | 54 个知名品牌的 CSS 设计系统值 |

**⛔ html-anything 已移除（v6.0.0）** — 效果差、缺乏层次感，被 Open Design 完全替代。

**图片模型使用要点：**
- OpenRouter Grok Imagine：需购买 credits（free tier 无法调用图片模型，返回 402）
- Gemini：需代理访问（国内服务器无法直连 Google APIs），模型名 `gemini-2.5-flash-image`
- 截图仍然是主要的飞书展示方式（图片模型是补充，不是替代）
- 详见 `references/integration/image-generation-api-notes.md`

**与 clsh-content 设计工具链对齐：** 全部用 Open Design + 图片模型，无 html-anything。

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
7. **Module Depth（模块深度）** — 方案中的核心模块，如果删掉它，复杂度是消失（= 透传模块，可去掉）还是扩散到 N 个调用方（= 有价值）？核心模块的接口是否比实现简单得多？（来源：Matt Pocock /improve-codebase-architecture 的删除测试）
8. **术语一致性** — proposal.md 是否使用了 context.md 中定义的术语？有无自造新词？

### 大佬 Review Gate

自检通过后，向大佬确认：

> "设计文档已写入 `raw/projects/<项目名>/changes/<变更名>/`，请 review。确认无误后我开始写实现计划。"

**等待大佬确认后才进入 Phase 5。**

### 🔍 自动路径检查（Q1 改进 — 2026-05-19）

**每次写入文件后，必须执行路径验证：**

```bash
# 写入文件后立即验证
ls -la <声明路径>
# 确认文件存在且大小 > 0
```

**Phase 3 写入验证清单：**
- [ ] `proposal.md` 已写入 `raw/projects/<项目名>/changes/<变更名>/` → `ls` 验证
- [ ] `constitution.md` 已写入 `raw/projects/<项目名>/source-of-truth/` → `ls` 验证
- [ ] 文件大小 > 0（非空文件）

**Phase 6 产出物验证清单：**
- [ ] 代码文件已写入声明的绝对路径 → `ls` 验证
- [ ] 测试文件已写入 → `ls` 验证
- [ ] 产出物路径使用绝对路径（禁止相对路径）

**⛔ 路径错误 = 流程违规，必须记 ERRORS.md**

> ⚠️ **教训（2026-05-15）：** write_file 使用相对路径，文件落到 skill references/ 目录而不是 raw/projects/ 目录。写入后未 `ls` 验证，导致虚假汇报。
