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

## Way C 派发模式

灵犀不做代码推理，只指定路径和问题：

```python
delegate_task(
    goal="修复 XXX 功能",
    acp_command="/usr/local/bin/codewhale",
    toolsets=["file", "terminal"],
    context="""
问题描述：[大佬反馈的现象]

相关文件路径：
- 代码位置：/opt/Workspace/src/projects/<项目>/
- wiki 项目文档：/mnt/unraid_data/Obsidian/wiki/projects/<项目>/changes/<变更名>/

请先读取相关代码和文档，自己分析根因并修复。
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
