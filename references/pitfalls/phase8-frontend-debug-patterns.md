# Phase 8 前端调试模式参考

## 上下文溢出防护

Phase 8 大量 bug 修复时的节奏控制：

1. **每轮最多 5-6 个 bug** — 超过 10 个时，分批处理
2. **后端和前端分开修** — 先修后端（通常少），再修前端
3. **每批修完先重启测试** — 确认无回归再继续下一批
4. **agent 超时后缩小任务** — 不要全量 fallback 到自修

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

```css
/* ❌ 这会导致子元素的 position:fixed 失效 */
.obs-layout {
  backdrop-filter: blur(16px);
}
.obs-ctx-menu {
  position: fixed; /* 相对于 .obs-layout，不是视口 */
}

/* ✅ 修复方案 1：不用 backdrop-filter */
.obs-layout {
  background: rgba(255,255,255,0.85); /* 半透明但不创建 CB */
}

/* ✅ 修复方案 2：用 Teleport 渲染弹出元素到 body */
/* Vue3: h(Teleport, { to: "body" }, [menuEl]) */
```

**同理会影响的 CSS 属性：** `transform`、`filter`、`will-change: transform`、`contain: layout` 等也会创建 containing block。

## CSS 重复定义导致样式冲突（2026-05-25）

多个文件或同一文件内出现同一个选择器的两次定义，后定义的覆盖前一个，导致部分样式丢失。

```css
/* line 779: 第一次定义（缺少 position） */
.obs-ctx-menu {
  background: white;
  border-radius: 10px;
}

/* line 1088: 第二次定义（有 position） */
.obs-ctx-menu {
  position: fixed;
  z-index: 100;
  background: white;
}
```

**修复：** 删除重复定义，保留完整的一个。用 `grep -c '选择器' 文件` 检查是否有重复。

## 仅读代码不等于 UI 验证（2026-05-25 教训）

**问题：** tester 读了修改后的源码文件，检查 CSS 属性和 JS 逻辑正确，就判定"全部 PASS"。但实际浏览器中效果完全不同（CSS 层叠、浏览器渲染差异、运行时状态等）。

**规则：** UI 项目的 review 必须包含浏览器实际验证，不能只做代码审查。
- ✅ 用浏览器打开页面 + 截图 + 交互测试
- ✅ 用 curl 验证 API 状态码
- ❌ 只读 .mjs/.css 文件就判 PASS
- ❌ 只检查"代码逻辑正确"不验证渲染效果
