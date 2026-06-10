# tasks.md 紧凑格式（80 行限制）

## 问题

tasks.md 行数上限 80 行，但整改项目可能有 20+ 个 Task。每个 Task 如果写 5 行（标题+范围+行动+验收标准+空行），20 个 Task = 100+ 行，超限。

## 紧凑格式模板

每个 Task 只用 **2 行**（标题行 + 内容行）：

```markdown
**Task N** | 角色：coder | skills: test-driven-development, incremental-implementation
行动描述。验收：验证条件
```

不用空行分隔，不用 `###` 子标题，不用表格。

## 对比

### 标准格式（~5 行/Task）
```markdown
#### Task 1: 删除明文密钥脚本 | 角色：coder | skills: test-driven-development, incremental-implementation

**范围**: tmp_inject.cjs, tmp_sign.cjs, tmp_signall.cjs（根目录）
**行动**: 删除 3 个含硬编码 SESSION_SECRET 的文件
**验收标准**: `grep -r "18074d8f" /opt/Workspace/` 返回空
```

### 紧凑格式（~2 行/Task）
```markdown
**Task 1** | 角色：coder | skills: test-driven-development, incremental-implementation
删除明文密钥脚本：tmp_inject.cjs, tmp_sign.cjs, tmp_signall.cjs。验收：`grep -r "18074d8f" /opt/Workspace/` 空
```

## 适用场景

- Task 数量 > 10
- 每个 Task 改动范围明确（单文件或少量文件）
- 验收条件可以用一行表达

## 不适用

- Task 需要详细的多步操作说明
- Task 有复杂的依赖关系需要展开
- 验收条件需要多行描述
