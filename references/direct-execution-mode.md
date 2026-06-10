# Phase 6 Direct Execution Mode

> 当 clsh-project Phase 6 以 subagent/test 模式运行时，跳过 kanban 派发，直接写代码。

## 触发条件

- 用户明确说"test mode"或"skip confirmation gates"
- 作为 subagent 被调用（无 kanban 环境）
- 用户要求"直接执行每个 Task"

## 与 Kanban 模式的区别

| 维度 | Kanban 模式（标准） | 直接执行模式（Test） |
|------|---------------------|---------------------|
| 派发方式 | `hermes kanban create --skill` | 直接 `write_file` |
| 角色隔离 | coder/artist/tester 独立 worker | 单 agent 执行所有角色 |
| Skills 注入 | kanban `--skill` 参数 | agent 自行加载 |
| 验证 | 独立 tester 卡 | agent 自检 checkpoint |
| 状态追踪 | kanban DB + dispatcher | 手动文件系统验证 |

## 执行模式

### 依赖顺序执行
```
Wave 1: Task 1 (无依赖)
Wave 2: Task 2, Task 10 (依赖 T1)
Wave 3: Task 3, Task 11 (依赖 T2)
Wave 4: Task 4, Task 5, Task 12 (依赖 T3)
Wave 5: Task 6, Task 13 (依赖 T4/T5)
Wave 6: Task 7, Task 9, Task 14, Task 15 (依赖 T3/T4)
Wave 7: Task 8, Task 16 (依赖全部后端)
```

### 每个 Task 的执行步骤
1. 读取 tasks.md 中该 Task 的定义（角色、文件、功能、验收标准）
2. 读取 proposal.md 和 constitution.md 中相关设计约束
3. 用 `write_file` 产出代码文件到目标路径
4. 自检：文件是否创建、是否符合验收标准
5. 输出简短 CHECKPOINT

### 产出物汇总
- 所有文件写入 `/tmp/<project-name>/`
- 执行完毕后输出完整文件清单（按 Task 分组）
- 更新 `overview.md` 标记 Phase 6 完成

## Pitfall: 代码生成质量

直接执行模式下，所有角色的代码由同一 agent 生成，需注意：
- **Prisma schema 必须完整** — 所有被路由引用的模型必须在 schema 中定义（如 Enrollment）
- **路由注册必须汇总** — 所有路由文件创建后，必须更新 `src/index.ts` 注册全部路由
- **变量名拼写** — 批量生成代码时容易出现截断或拼写错误（如 `MINIO_SECRET_KEY` 被截断）
- **测试文件必须可独立运行** — 集成测试需 mock 或使用 Fastify `inject()`
