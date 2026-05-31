# Phase 8 前端调试模式参考

## 上下文溢出防护

Phase 8 大量 bug 修复时的节奏控制：

1. **每轮最多 5-6 个 bug** — 超过 10 个时，分批处理
2. **后端和前端分开修** — 先修后端（通常少），再修前端
3. **每批修完先重启测试** — 确认无回归再继续下一批
4. **agent 超时后缩小任务** — 不要全量 fallback 到自修

## Token→Session 免登录架构（2026-05-31）

实现"点击链接免登录进入 embed 模式"的完整架构：

### 后端
```
POST /api/auto-login
  → 验证 token（Map 存储，24h 过期，一次性销毁）
  → 创建 session（request.session.user = { username, role: 'embed' }）
  → 返回 user 对象
```

### 前端（app.mjs onMounted）
```
1. 读 URL 参数: ?token=xxx&embed=moviepilot
2. 优先设置 embed.value（不等 auth）
3. 如果有 token → 调 POST /api/auto-login
4. 成功 → user.value = data.user, authChecked.value = true
5. 清理 URL 参数（replaceState）
6. 如果有 embed → activeProject = embed, loading = false（不等 loadProjects）
7. 渲染：embed 模式 → 全屏无侧边栏
```

### 关键 Pitfalls
- session cookie 必须 `sameSite: 'lax'`（允许从飞书等外部链接设置 cookie）
- auto-login 成功后必须立即设 `authChecked = true`（否则渲染函数卡在 loading spinner）
- 移除前端 Bearer token 依赖（已有 session cookie 认证）
- embed 模式不等 `loadProjects()`，直接设 `activeProject` 和 `loading=false`（避免阻塞渲染）

## Vue3 CDN 组件 Tab 状态管理（2026-05-31）

### 错误模式
```javascript
// ❌ onClick 只 dispatch event，不更新内部状态
const active = props.activeTab || 'recommend';
tabs.map(t => h('button', {
  onClick: () => window.dispatchEvent(new CustomEvent('tab', { detail: t.key }))
}))
// 结果：点击 tab 无反应，active 永远是 props 的值
```

### 正确模式
```javascript
// ✅ 创建内部 ref，onClick 直接更新
const VALID_TABS = ['recommend', 'search', 'download', 'subscribe'];
const activeTab = ref(
  VALID_TABS.includes(props.activeTab) ? props.activeTab : 'recommend'
);

tabs.map(t => h('button', {
  class: `mp-tab ${activeTab.value === t.key ? 'mp-tab--active' : ''}`,
  onClick: () => { activeTab.value = t.key; }
}))

// 渲染用内部 ref
const active = activeTab.value;
```

### 关键点
- 验证 props.activeTab 是否是有效 tab key，无效值 fallback 到默认
- 用 VALID_TABS 数组做验证，不要硬编码 if-else
- 内部 ref 优先于 props（props 只作初始值）

## Workspace 子模块 CSS 加载（2026-05-31）

子模块的 CSS 不会自动加载到 Workspace 主应用。

**规则：** 子模块的 CSS 必须在 `src/public/index.html` 的 `<head>` 中添加 `<link>` 引用。

```html
<!-- src/public/index.html -->
<link rel="stylesheet" href="/projects/moviepilot/public/tokens.css">
```

**验证：** 浏览器 F12 → Network → 检查 CSS 文件是否返回 200。

## ESM 变量遮蔽（2026-05-21）

```javascript
// ❌ 错误：参数 path 遮蔽 import 的 path 模块
export function createShare({ path }) {
  const fullPath = path.resolve(VAULT_PATH, path); // path 是参数不是模块！
}

// ✅ 正确：参数重命名
export function createShare({ path: sharePath }) {
  const fullPath = path.resolve(VAULT_PATH, sharePath); // path 是模块
}
```

## Markdown 表格正则（2026-05-21）

两步匹配策略：
1. 先匹配有 separator 的标准表格：`/(^\|.+\|\n\|[\s\-:|]+\|\n(?:\|.+\|\n?)*)/gm`
2. 再匹配无 separator 的连续 `|` 行：`/(^\|.+\|\n(?:\|.+\|\n?)+)/gm`
3. `buildTable` 函数用 `function` 声明（hoisting）避免定义顺序问题

## z-index 层级管理

| 层级 | z-index | 用途 |
|------|---------|------|
| Content | 0-100 | 普通内容 |
| Sidebar | 500 | 侧边栏 |
| Context menu | 1000 | 右键菜单 |
| Modal | 3000 | 弹窗 |
| Toast | 5000 | 提示消息（必须最高） |

Toast 需要 `pointer-events: none` 避免遮挡交互。

## TOC 在 flex 容器中悬浮

```css
.note-with-toc { display: flex; gap: 0; }
.note-article { flex: 1; min-width: 0; }
.toc-panel {
  position: sticky;
  top: 0;
  align-self: flex-start; /* 关键：sticky 在 flex item 上需要这个 */
  max-height: calc(100vh - 60px);
  overflow-y: auto;
}
```

## 响应式设计断点

| 断点 | 行为 |
|------|------|
| ≤1024px | TOC 隐藏 |
| ≤768px | Sidebar 变为可抽屉（transform: translateX(-100%)），添加 hamburger 按钮 |
| ≤480px | 搜索框隐藏，分享管理全宽，select 改为纵向布局 |

## 原生 select 卡顿

移动端 `<select>` 渲染选项多时卡顿。缓解：减少选项到 5 个以内，单位选择器用固定宽度。

## CSS `backdrop-filter` 创建 containing block（2026-05-25）

**问题：** 给元素加 `backdrop-filter: blur()` 后，该元素成为所有 `position:fixed` 子元素的 containing block。fixed 子元素不再相对于视口定位，而是相对于该元素。

**症状：** 弹出菜单用了 `position:fixed` + `e.clientX/clientY` 但位置偏移（相对于父容器而非鼠标位置）。

**同理会影响的 CSS 属性：** `transform`、`filter`、`will-change: transform`、`contain: layout` 等也会创建 containing block。

## CSS 重复定义导致样式冲突（2026-05-25）

多个文件或同一文件内出现同一个选择器的两次定义，后定义的覆盖前一个，导致部分样式丢失。

**修复：** 删除重复定义，保留完整的一个。用 `grep -c '选择器' 文件` 检查是否有重复。

## 仅读代码不等于 UI 验证（2026-05-25 教训）

**问题：** tester 读了修改后的源码文件，检查 CSS 属性和 JS 逻辑正确，就判定"全部 PASS"。但实际浏览器中效果完全不同。

**规则：** UI 项目的 review 必须包含浏览器实际验证，不能只做代码审查。
- ✅ 用浏览器打开页面 + 截图 + 交互测试
- ✅ 用 curl 验证 API 状态码
- ❌ 只读 .mjs/.css 文件就判 PASS
- ❌ 只检查"代码逻辑正确"不验证渲染效果
