# Phase 8 修复任务上下文管理指南（2026-05-21）

## 背景

Phase 8 反馈循环中，修复任务因上下文过大连续中断两次。根本原因：一轮修太多 bug + 在主对话中逐个读文件 + 无 checkpoint 保存进度。

## 核心规则

### 1. 每轮最多修 3-4 个 bug

**绝对上限：4 个 bug / 轮**

超过 4 个时必须分批：
- 第一批：修 3-4 个 → 重启测试 → 确认无回归
- 第二批：修 3-4 个 → 重启测试 → 确认无回归
- 依此类推

### 2. 用 execute_code 批量读代码

**禁止在主对话中逐个 read_file**

```python
# ✅ 正确：用 execute_code 一次读多个文件的关键片段
execute_code("""
from hermes_tools import read_file, terminal

# 读取相关代码片段（不加载整个文件）
files = [
    ('/opt/project/src/api/share.mjs', 50, 100),  # offset, limit
    ('/opt/project/src/public/app.mjs', 200, 250),
    ('/opt/project/src/public/style.css', 1, 50),
]

for path, offset, limit in files:
    result = read_file(path, offset=offset, limit=limit)
    print(f"\\n=== {path} (lines {offset}-{offset+limit}) ===")
    print(result['content'][:500])  # 只输出前500字符
""")
```

```python
# ❌ 错误：在主对话中逐个 read_file
# read_file('/opt/project/src/api/share.mjs')  # 加载整个文件
# read_file('/opt/project/src/public/app.mjs')  # 上下文膨胀
# read_file('/opt/project/src/public/style.css')  # 继续膨胀
```

### 3. 每个 bug 只读相关代码片段

用 grep 定位，用 read_file 的 offset/limit 只读相关行：

```bash
# 先 grep 定位
grep -n "createShare" /opt/project/src/api/share.mjs
# 输出: 45:  async createShare({ path }) {

# 只读相关行
read_file('/opt/project/src/api/share.mjs', offset=40, limit=20)
```

### 4. 修一个验证一个

**不要一次性修改所有文件再验证**

```
修 bug #1 → 测试 bug #1 → 通过 → 修 bug #2 → 测试 bug #2 → 通过 → ...
```

而不是：
```
修 bug #1, #2, #3, #4 → 一起测试 → 发现 #2 有回归 → 全部重来
```

### 5. 长输出写入 /tmp/

```python
# 测试结果写入文件
terminal("curl -s http://localhost:3456/api/tree/ | head -50 > /tmp/test-tree.txt")

# 只在对话中放结论
print("Tree API: ✅ 返回 16 项")
```

### 6. 进度写入 checkpoint 文件

每批修完后写 checkpoint：

```markdown
# /tmp/<project>-round<N>-checkpoint.md

## 已修复
- [x] Bug #1: TOC 点击无法跳转 → notes.mjs 添加 slugify
- [x] Bug #2: 文件夹无法展开 → folder.html 添加 expandFolder
- [x] Bug #3: 第三层路径失败 → share.mjs 添加 path 属性

## 待修复
- [ ] Bug #4: 右键菜单文本显示错误
- [ ] Bug #5: Toast 背景色看不清
- [ ] Bug #6: 项目文件需要迁移

## 阻塞项
- 无

## 下一步
- 修 Bug #4-#6（前端）
- pm2 restart
- 基础测试
```

## 中断恢复协议

当 session 因上下文过大中断后重启：

1. **读取 checkpoint**
   ```bash
   cat /tmp/<project>-round<N>-checkpoint.md
   ```

2. **如果 checkpoint 不存在**，从项目文档恢复
   ```bash
   cat /mnt/unraid_data/Obsidian/wiki/projects/<项目名>/changes/<变更名>/completion-summary.md
   ```

3. **从上次中断的 bug 继续**，不重做已完成的修复

4. **向大佬确认**恢复的上下文是否正确

## 上下文预算估算

| 操作 | Token 估算 | 说明 |
|------|-----------|------|
| read_file (500行) | ~2000 | 单个文件 |
| execute_code 批量读 (5个文件) | ~3000 | 一次搞定 |
| patch 修改 | ~500 | 单次修改 |
| 测试验证 | ~1000 | curl + 检查 |
| **单个 bug 修复** | **~2000-3000** | 读+改+验 |
| **4 个 bug 修复** | **~8000-12000** | 安全范围 |
| **10 个 bug 修复** | **~20000-30000** | ⚠️ 危险！ |

**安全阈值：单轮修复不超过 12000 token（约 4 个 bug）**

## 常见错误模式

### 错误 1: 一轮修太多

```
❌ 大佬反馈 13 个 bug → 灵犀一轮全修 → 上下文爆炸 → session 中断
✅ 大佬反馈 13 个 bug → 分 4 轮修（4+4+3+2）→ 每轮重启测试
```

### 错误 2: 在主对话中读完整文件

```
❌ read_file('app.mjs')  # 500行进上下文
❌ read_file('style.css')  # 300行进上下文
❌ read_file('share.mjs')  # 200行进上下文
# 上下文已膨胀 4000+ token

✅ execute_code("""
    # 只读相关片段
    app = read_file('app.mjs', offset=200, limit=50)
    css = read_file('style.css', offset=1, limit=30)
    share = read_file('share.mjs', offset=40, limit=20)
    print(app['content'][:200])
    print(css['content'][:200])
    print(share['content'][:200])
""")
# 上下文只增加 ~1000 token
```

### 错误 3: 没有 checkpoint

```
❌ 修了 5 个 bug → session 中断 → 重启后不知道修了哪些 → 重头来过
✅ 修了 5 个 bug → 写 checkpoint → session 中断 → 读 checkpoint → 继续第 6 个
```
