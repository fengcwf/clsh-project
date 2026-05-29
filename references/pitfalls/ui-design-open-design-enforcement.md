# UI 设计必须加载 Open Design 知识包

**日期：** 2026-05-29
**触发：** MoviePilot HTML 模板设计
**严重度：** 流程违规（Phase 3 跳步）

## 问题

Phase 3 设计发散要求加载 Open Design 知识包（tokens.css + DESIGN.md + craft/*.md），但灵犀直接手写了 HTML，没有加载任何设计系统文件。

结果：
- 用户评价"效果一般"
- 自定义的颜色/间距/排版不如成熟设计系统
- 后续返工（用 Open Design 重做 3 个变体）

## 正确流程（Phase 3 设计发散）

1. **读取 Open Design tokens：** `/opt/open-design/design-systems/<name>/tokens.css` → `:root {}` 块
2. **读取 DESIGN.md：** 9 节设计规范（颜色/字体/布局/组件/动效/反模式）
3. **读取 craft 标准：** `anti-ai-slop.md`（禁用 emoji 做图标、禁默认 indigo、accent 最多 2 次/屏）
4. **读取 state-coverage.md：** 5 个必须状态（Loading / Empty / Error / Populated / Edge）
5. **渲染 2-3 个变体：** 每个变体用不同设计系统
6. **发链接给用户选择：** 优先交互原型（nginx :8088 或 Fastify 静态文件）

## 设计系统选择表

| 用户偏好 | 设计系统 | 路径 |
|---------|---------|------|
| 极简白底 | `apple/` | `/opt/open-design/design-systems/apple/` |
| 图片主导 | `airbnb/` | `/opt/open-design/design-systems/airbnb/` |
| 毛玻璃 | `glassmorphism/` | `/opt/open-design/design-systems/glassmorphism/` |
| 企业级 | `ant/` | `/opt/open-design/design-systems/ant/` |
| 暗色面板 | `dashboard/` | `/opt/open-design/design-systems/dashboard/` |
| 优雅专业 | `stripe/` | `/opt/open-design/design-systems/stripe/` |

## Anti-AI-slop 检查清单

- [ ] 不用 emoji 做图标（用 SVG monoline + currentColor）
- [ ] 不用默认 Tailwind indigo（#6366f1, #4f46e5 等）
- [ ] var(--accent) 最多出现 2 次/屏
- [ ] 不用圆角卡片+彩色左边框（AI dashboard 标志性形状）
- [ ] 不用外部占位图 CDN（unsplash, placehold.co）
- [ ] 不用填充文字（lorem ipsum, feature one/two/three）
