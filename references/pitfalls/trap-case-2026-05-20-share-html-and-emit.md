# 陷阱案例：share.html 风格遗漏 + Vue 组件 emit 参数陷阱（2026-05-20）

## 陷阱 1：share.html 风格遗漏

### 事件
UI 风格从紫色深色改为 Slate 灰蓝色浅色时，只更新了 Vue 组件（app.mjs + style.css），忘记了 share.html 是独立的静态 HTML 文件，导致分享页面仍然是旧风格。

### 根因
share.html 是独立 HTML 文件，不在 Vue 组件体系中，UI 风格更新时容易被遗忘。

### 教训
- **UI 风格更新时，必须检查所有 HTML 文件**，包括独立的静态页面
- 在 style.css 全局变量更新后，搜索所有 .html 文件中的硬编码颜色值

### 正确做法
```bash
grep -r "#7c5cfc\|#0f0f13\|#1e1e2e" /opt/*/src/public/*.html
```

---

## 陷阱 2：Vue 组件递归 emit 参数陷阱

### 事件
tree-item 组件递归调用时，子组件的 @contextmenu 写成了：
@contextmenu="emit('contextmenu', $event, $event)"
第二个参数应该是 item（当前节点数据），但写成了 $event（DOM 事件对象）。

### 教训
- 递归组件 emit 时，明确区分 DOM 事件和数据参数
- 写完组件后，检查所有 emit 调用的参数顺序和类型

### 正确写法
```html
<!-- 组件自身 div 上 -->
@contextmenu="emit('contextmenu', $event, item)"
<!-- 子组件递归调用时 -->
@contextmenu="emit('contextmenu', $event, child)"
```

---

## 陷阱 3：artist 并行写同一文件的协调

### 教训
- 多个 artist 写同一文件时，需要明确分工
- 最佳实践：按文件拆分，每个 artist 负责不同文件
- 如果必须写同一文件：串行执行，或明确指定各自修改的函数/区域
