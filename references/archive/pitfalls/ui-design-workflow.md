# UI 设计工作流（2026-05-24 更新）

> clsh-project Phase 3 设计发散的标准流程

## 三个阵营

| 阵营 | 工具 | 输出 | 适合场景 |
|------|------|------|---------|
| Camp 1: 生产应用构建 | v0、Lovable、Bolt.new | 可部署的完整应用 | 快速出 MVP |
| Camp 2: 概念/低保真 | Uizard、Galileo AI、Google Stitch | 图片/线框图 | 方向确认、视觉探索 |
| Camp 3: 工作区内设计 | Claude Design、Figma Make、Open Design | 代码内嵌的设计 | 无交接、设计即代码 |

## 我们的方案（Camp 3）

```
灵犀描述需求 + 视觉方向（文字）
    ↓
灵犀读取 Open Design 知识包（见下方）
    ↓
灵犀用 tokens + SKILL.md + Craft 规则 本地渲染 HTML mockup
    ↓ chromium-browser 截图 → 发飞书给大佬
大佬确认方向 + 修改意见
    ↓
灵犀迭代 HTML → 大佬确认最终版
coder 基于确认的 mockup 实现生产代码
```

## Open Design 知识包集成（核心流程）

**不是**让 Open Design 调 Hermes agent（套娃），**而是**灵犀直接读取知识包自己渲染。

### 知识包组成

| 文件 | 路径 | 作用 |
|------|------|------|
| `tokens.css` | `design-systems/<name>/tokens.css` | CSS 变量值 |
| `DESIGN.md` | `design-systems/<name>/DESIGN.md` | 9 节设计规范（颜色/字体/布局/组件/动效/反模式） |
| `SKILL.md` | `design-templates/<name>/SKILL.md` | 构建工作流 + 布局规则 + 自检清单 |
| `example.html` | `design-templates/<name>/example.html` | 参考实现 |
| `craft/*.md` | `craft/state-coverage.md` 等 | 质量底线（5 种状态、无障碍、UX 定律） |

### 知识包读取步骤

```bash
# 1. 选设计系统
cat /opt/open-design/design-systems/glassmorphism/tokens.css
cat /opt/open-design/design-systems/glassmorphism/DESIGN.md

# 2. 选 Skill
cat /opt/open-design/design-templates/dashboard/SKILL.md

# 3. 读参考实现
cat /opt/open-design/design-templates/dashboard/example.html

# 4. 读 Craft 规则（按需）
cat /opt/open-design/craft/state-coverage.md    # 5 种必写状态
cat /opt/open-design/craft/anti-ai-slop.md      # 反 AI 味规则
cat /opt/open-design/craft/laws-of-ux.md         # UX 定律
```

### 生成流程

1. 读完知识包 → 理解设计系统规则 + 构建工作流 + 质量底线
2. 结合项目需求（proposal.md）生成 HTML
3. 严格遵循：
   - DESIGN.md 的颜色/字体/间距（不发明新值）
   - SKILL.md 的布局规则（如 dashboard: sidebar 220-260px, KPI cards, inline SVG charts）
   - anti-ai-slop：不用默认 indigo、不用 emoji 做图标、accent 最多 2 处可见
   - state-coverage：至少展示 populated 状态
4. `chromium-browser --headless --screenshot` 截图
5. 发飞书给大佬确认

## 设计系统选择指南

| 场景 | 推荐设计系统 | 特点 |
|------|-------------|------|
| 管理后台 | `glassmorphism` | 磨砂玻璃、浅色、柔和霓虹 |
| 极简深色 | `linear-app` | 深黑底、紫色 accent、极致简洁 |
| 通用 SaaS | `shadcn` | 中性、干净、Tailwind 风格 |
| 品牌官网 | `stripe` | 精致渐变、专业感 |
| 科技感 | `glassmorphism` + Gleb Kuznetsov 风格改造 | 低饱和霓虹 + 浅色磨砂 |

## Prompt 框架（用于 Stitch / v0 / 任何 AI UI 工具）

### RTCF 框架
```
Role: Act as a Senior Product Designer specialized in [领域].
Task: Generate a [具体页面类型].
Context: [设计系统] + [用户场景] + [核心模块] + [视觉风格参考]
Format: Desktop 1440px, [字体], HTML/CSS output.
```

### v0 三要素
```
Build [产品表面：组件、数据、操作].
Used by [谁], in [什么场景], to [做什么决策].
Constraints: [平台] + [视觉调性] + [布局假设]
```

## 工具矩阵

| 需求 | 工具 | 输出 |
|------|------|------|
| 快速效果图 | Open Design tokens + Chromium 截图 | PNG |
| 完整原型 | Open Design Web UI + Hermes agent | HTML/PDF |
| 多风格探索 | 换设计系统重新渲染 | PNG |
| 设计系统规范 | Stitch DESIGN.md + 本地 tokens | DESIGN.md |
| AI 生成设计稿 | Google Stitch (MCP) | 设计系统 token + HTML |

## 注意事项

- **不用 emoji 做图标**（anti-ai-slop 规则 #3），用 SVG 线性图标
- **不用默认 indigo**（anti-ai-slop 规则 #1），用设计系统提供的 accent
- **accent 最多 2 处可见**（anti-ai-slop 规则）
- **chromium 截图路径用 /root/mockups/**（snap 版 AppArmor 限制 /tmp）
- **飞书不发 HTML 路径**，发 PNG 图片（MEDIA: 前缀）
