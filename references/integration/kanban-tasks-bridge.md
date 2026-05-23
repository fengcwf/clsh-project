# Kanban → tasks.md Bridge 架构

## 问题

clsh-project Phase 6 派发 kanban 卡后，agent 完成任务只调用 `kanban_complete()`，不会自动回写 tasks.md 的 checkbox。导致：
- tasks.md 的 `- [ ]` 永远不变
- proposal.md 的 `status: implementing` 不会自动变 `done`
- Phase 7 归档需要手动触发

## 解决方案

### 标记约定

kanban 卡 body 末尾嵌入 HTML 注释标记：

```html
<!-- clsh-project: project=<项目名> change=<变更名> task=<任务编号> -->
```

**示例：**
```python
kanban_create(
    title="feat: 添加用户认证中间件",
    assignee="coder",
    body="""## 目标
实现 JWT 认证中间件

## 验收标准
- [ ] /api/* 无 token 返回 401

<!-- clsh-project: project=my-app change=2026-05-13-auth task=1 -->
""",
)
```

### Bridge 脚本

**路径：** `/opt/Workspace/scripts/obsidian/kanban-tasks-bridge.py`

**执行逻辑：**
1. 扫描 kanban DB 中 body 含 `clsh-project:` 的任务
2. 提取标记中的 `(project, change, task_num)`
3. 对 `done`/`archived` 状态的任务，找到对应的 `tasks.md`
4. 按 task_num 定位 `## Task N:` section，将 section 内所有 `- [ ]` → `- [x]`
5. 检查该 project/change 下所有标记任务是否全部 done
6. 全部 done → 更新 `proposal.md` frontmatter `status: done`

**关键设计决策：**

| 决策 | 选择 | 理由 |
|------|------|------|
| 标记位置 | kanban body（HTML 注释） | 不影响 worker 阅读任务描述 |
| 匹配策略 | section-level（`## Task N:` 下所有 checkbox） | 兼容 Step/子任务 checkbox |
| 触发方式 | Wiki Sync gate（每6h）| 不单独开 cron，复用已有流水线 |
| proposal 更新 | 全部 done 才触发 | 避免部分完成就标记 done |

### Checkbox 匹配策略（踩坑）

**初始方案（失败）：** 按行匹配含 task_num 的 `- [ ]` 行。
- 问题：tasks.md 中 "## Task 3:" 下的 checkbox 不含 "Task 3" 文字
- 结果：Task 1/2 匹配成功，Task 3 匹配失败

**最终方案（成功）：** 先用正则定位 `## Task N:` section（到下一个 `## ` 或 EOF），再批量替换 section 内所有 `- [ ]`。

```python
section_pattern = re.compile(
    rf'(##\s+Task\s*{task_num}\b.*?)(?=^## |\Z)',
    re.MULTILINE | re.DOTALL
)
```

### 手动运行

```bash
python3 /opt/Workspace/scripts/obsidian/kanban-tasks-bridge.py          # 执行
python3 /opt/Workspace/scripts/obsidian/kanban-tasks-bridge.py --status  # 查看状态
python3 /opt/Workspace/scripts/obsidian/kanban-tasks-bridge.py --dry-run # 预览
```

### 测试验证

端到端测试（2026-05-13）：
- 3 个 kanban 卡（2 done + 1 running）→ bridge 更新 2 个 section 的 checkbox ✅
- 第 3 个卡标记 done → bridge 更新剩余 checkbox + proposal.md status → done ✅
- tasks.md: 6/6 checked, 0 unchecked ✅
