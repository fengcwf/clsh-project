# CodeWhale ACP 集成参考

## 会话机制

### ACP 模式（delegate_task）

**每次调用都是全新会话，不保留上次对话。**

从 `delegate_tool.py` 源码：
```python
Each child gets:
  - A fresh conversation (no parent history)
  - Its own task_id (own terminal session, file ops cache)
```

**影响：** 连续修复多个 bug 时，每次都需要重新读取相同文件，token 浪费严重。

### CLI 模式（terminal 调用）

支持持续会话：
```bash
codewhale exec --continue "继续"      # 恢复最近 session
codewhale exec --resume <SESSION_ID>   # 恢复指定 session
codewhale fork <SESSION_ID>            # 分支线程
codewhale sessions                     # 列出所有 session
codewhale thread list                  # 管理线程元数据
```

**CLI 坏处：** 解析复杂（stdout）、错误处理弱（exit code）、超时管理难。

## Token 优化

用精简 context 摘要，不传完整文件：

```python
# ❌ 错误：传完整文件（~50K tokens）
context=read_file("ObsidianView.mjs")  # 736 行全部传入

# ✅ 正确：只传关键信息（~10K tokens）
context="""
问题：重命名不带 .md
相关文件：
- ObsidianView.mjs（第 418-455 行 renameItem 函数）
- plugin.mjs（第 118-125 行 rename API）
后端 API：PUT /api/obsidian/rename，期望 { oldPath, newPath }
"""
```

## Way C 派发模式（铁律）

灵犀不做代码推理，只指定**目标 + 路径 + 约束**。CodeWhale 自己读代码、分析问题、决定方案。

### ✅ 灵犀应该给的

| 要素 | 说明 | 示例 |
|------|------|------|
| 目标 | 大佬想要什么结果 | "大佬说按钮丑，重做 UI" |
| 参考文件 | CodeWhale 应该读的 | "读 style.css 确认设计系统" |
| 约束 | 不可违反的限制 | "浅色毛玻璃主题，不引入新依赖" |
| 验收标准 | 怎么算做完 | "node -c 通过 + 大佬觉得好看" |

### ❌ 灵犀不应该给的

| 不该给 | 原因 |
|--------|------|
| 具体 CSS 代码 | CodeWhale 可能有更好的方案 |
| "删除 18 处 !important" | 这是 CodeWhale 应该自己发现的 |
| "用作用域提升优先级" | 这是 CodeWhale 应该自己决定的 |
| 详细实现步骤 | 越详细越限制 CodeWhale 的创造力 |

### 反例（灵犀做代码推理 ❌）

```python
# ❌ 灵犀分析了 CSS，告诉 CodeWhale 怎么改
context="""
按钮丑的原因：18处 !important、和全局 style.css 冲突。
修复方案：
1. 删除 .svc-btn.green 中的 !important
2. 用 .um-card-actions 作用域提升优先级
3. 添加 @media (max-width: 768px) 断点
具体代码：...
"""
```

### 正例（给目标，CodeWhale 自己推理 ✅）

```python
# ✅ 灵犀只描述问题和目标
context="""
目标：大佬说 UI 丑，重做视觉效果。

参考文件：
- /opt/Workspace/src/public/style.css（全局设计系统）
- /opt/Workspace/src/projects/cron/public/CronMonitor.mjs（参考实现）

约束：浅色毛玻璃主题，不引入新依赖。

验收标准：
1. 按钮视觉效果和 CronMonitor 同等水平
2. PC/移动端自适应
3. node -c 语法通过
"""
```

```python
delegate_task(
    goal="重做上游监控 UI",
    acp_command="/usr/local/bin/codewhale",
    toolsets=["file", "terminal"],
    context="""
目标：大佬说 UI 丑，重做视觉效果。

参考文件：
- /opt/Workspace/src/public/style.css（全局设计系统）
- /opt/Workspace/src/projects/cron/public/CronMonitor.mjs（参考实现）
- /opt/Workspace/src/projects/upstream-monitor/public/UpstreamMonitor.mjs（当前 UI）

约束：
- 浅色毛玻璃主题（背景 #f0f2f5，卡片 rgba(255,255,255,0.65)）
- 不引入新 npm 依赖
- Vue3 CDN 组件，完整解构 API

验收标准：
1. 按钮有存在感（padding、hover 效果、分色）
2. PC/移动端自适应（3断点）
3. 检查记录支持筛选
4. node -c 语法通过
"""
)
```

## .deepseek/notes.md

- **CLI 模式：** 自动读取项目目录的 `.deepseek/notes.md`
- **ACP 模式：** 不会自动读取，需要在 context 中显式传递

## 已验证的文件系统访问范围

| 路径 | 读 | 写 |
|------|----|----|
| `/mnt/unraid_data/Obsidian/wiki/` | ✅ | - |
| `/opt/Workspace/src/` | ✅ | ✅ |
| `/tmp/` | ✅ | ✅ |

## 性能参考

| 场景 | 时间 | Token |
|------|------|-------|
| 3 个 bug 修复（Round 7） | 156s | ~1.4M input |
| 4 个 bug 修复（Round 9） | 88s | ~500K input |
| 单个 API 路由添加 | 27s | ~70K input |

## ⛔ CodeWhale 超时后灵犀自行分析（2026-06-01 教训）

**违规模式：** CodeWhale 超时/失败 → 灵犀"顺手"自己分析根因并修复 → 违反铁律第8条

**正确行为：**
1. CodeWhale 超时 → 拆分更小任务重新派发
2. 如果是网络类任务（curl 到外部服务），灵犀自己做网络测试确认可达性，再派 CodeWhale 做纯代码修改
3. 如果 CodeWhale 连续超时 → 汇报大佬请求决策

**绝对不允许：** 灵犀自己分析根因然后修复，即使"看起来只是简单诊断"

**这条规则在每个 Phase 的每个 Round 都必须遵守，不存在例外**

**区分：** 网络连通性测试（ping、curl 状态码）灵犀可以做（因为这是环境诊断，不是代码分析）。但"API 返回 404，根因是端点路径不对，应该改成 MCP 协议"这种分析必须由 CodeWhale 做。
