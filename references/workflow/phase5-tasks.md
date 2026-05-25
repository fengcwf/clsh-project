# clsh-project — Phase 5: 实现计划

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 5: 写实现计划

**文件位置：** `wiki/projects/<项目名>/changes/YYYY-MM-DD-<变更名>/tasks.md`

**参考：** `plan` skill（前身 writing-plans）

### ⛔ 文件大小控制（不可违反）

**tasks.md 单文件不得超过 3000 字。** 超过时必须拆分：

```
tasks.md          ← 汇总版（依赖图 + 任务索引 + Self-Review）
tasks-slice1.md   ← Slice 1 详细任务（~2000字）
tasks-slice2.md   ← Slice 2 详细任务（~2000字）
tasks-slice3.md   ← Slice 3 详细任务（~2000字）
tasks-slice4.md   ← Slice 4 详细任务（~2000字）
```

**拆分规则：**
1. tasks.md 写汇总：依赖图 + 每个 Slice 的简要描述 + 任务索引 + Self-Review
2. 每个 slice 文件写该 Slice 的完整任务（含代码片段）
3. 每个文件控制在 2000-3000 字
4. 分多次 write_file 写入，每次写一个文件
5. 写入后必须 `ls` 验证文件存在且大小 > 0

**⛔ 禁止：** 一次性 write_file 写入 >5000 字的内容（会被截断导致文件损坏）

### 关键原则
- **每个任务 = 一个 kanban 卡**
- **任务粒度：2-5 分钟**（一个任务 = 一个动作：写测试/运行/实现/提交）
- **包含完整代码片段**（可复制粘贴到文件中）
- **包含精确文件路径**（`exact/path/to/file.py:123-145`）
- **包含验证步骤**（精确命令 + 预期输出）
- **标注依赖关系**（哪些任务必须等别的任务完成）
- **标注完整的测试代码**（不是"写个测试"，而是实际测试代码）

### ⛔ Superpowers v5 — No Placeholders

以下写法 = **计划缺陷**，必须修复：

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| "TBD"、"TODO"、"稍后实现" | 写实际代码 |
| "添加错误处理" | 写具体的 try/catch 代码 |
| "类似 Task 3" | 复制实际代码（开发者可能跳读） |
| "写测试覆盖上述" | 写实际测试代码 |
| "填充详情" | 直接写详情 |

### ⛔ Superpowers v5 — Type Consistency

写完全部任务后，检查跨任务一致性：
- Task 3 定义的函数签名，Task 5/7 调用时是否匹配？
- 类型定义（interface/type/class）前后是否一致？
- 命名风格是否统一？

### Superpowers v5 — Self-Review

写完全部任务后执行：
1. **Spec Coverage** — 逐条扫描 spec 需求，确认每个需求都有对应任务。列出遗漏。
2. **Placeholder Scan** — 搜索 No Placeholders 表中的模式，全部修复。
3. **Type Consistency** — 跨任务检查签名一致性。
4. **File Isolation** — 是否有任务修改了相同的文件？（如果有，确认顺序和依赖关系已标注）

### 📋 文件依赖图

在 tasks.md 开头标注任务间依赖，确保无冲突的并行执行：

```
# [功能名] 实现计划

## 依赖图
Task 1: 创建数据模型（无依赖）
Task 2: 创建 API 层（依赖 Task 1）
Task 3: 创建 UI 组件（依赖 Task 2）
Task 4: 集成测试（依赖 Task 1, 2, 3）

依赖图:
Task 1 → Task 2 → Task 3
  ↓              ↓
  └──── Task 4 ←─┘

可并行: 无（线性依赖）
```

**规则：**
- 有依赖的任务必须等父任务完成
- 无依赖的任务可并行派发
- 修改同一文件的任务必须串行，且依赖关系明确

### 📋 垂直切片策略（incremental-build）

**参考：** `incremental-build` skill

将功能拆分为可独立交付的端到端切片，每个切片完成后系统处于可工作状态。

### 📋 Vertical Slice + HITL/AFK 分类

**来源：** Matt Pocock /to-issues

每个任务必须是**端到端的薄切片**（schema → API → UI → tests），不是水平层。

**⛔ 反模式：**
- "Task 1: 创建数据库表"（水平切片，无法独立验证）
- "Task 2: 写 API 接口"（依赖 Task 1 的表，但没有 UI 无法演示）

**✅ 正确：**
- "Task 1: 创建任务功能（DB + API + 基础 UI + 测试）" — 完成后可独立演示

**任务分类（每个 Task 标注）：**

| 类型 | 含义 | 示例 |
|------|------|------|
| **HITL** | Human-In-The-Loop，需要大佬参与 | 架构决策、设计审核、业务规则确认 |
| **AFK** | Away From Keyboard，可全自动执行 | 写代码、跑测试、部署验证 |

**规则：**
- 优先设计 AFK 任务，减少大佬等待
- HITL 任务必须明确标注需要大佬做什么
- AFK 任务的验收标准必须是客观可验证的（测试通过、文件存在、命令输出匹配）

**三种切片策略：**

| 策略 | 适用场景 | 示例 |
|------|---------|------|
| **垂直切片**（推荐） | 完整功能路径 | 切片1: 创建任务(DB+API+UI) → 切片2: 列表任务 → 切片3: 编辑任务 |
| **契约优先** | 前后端并行开发 | 切片0: API契约 → 切片1a: 后端 + 切片1b: 前端(并行) → 切片2: 集成 |
| **风险优先** | 技术不确定性高 | 切片1: 验证最风险的技术点 → 切片2: 核心功能 → 切片3: 增强功能 |

**垂直切片模板：**
```
Slice 1: 创建任务（DB + API + 基础UI）
  验证: 测试通过，用户可通过 UI 创建任务
Slice 2: 列表任务（查询 + API + UI）
  验证: 测试通过，用户可看到任务列表
Slice 3: 编辑任务（更新 + API + UI）
  验证: 测试通过，用户可修改任务
Slice 4: 删除任务（删除 + API + 确认UI）
  验证: 测试通过，完整 CRUD
```

**切片原则：**
- 每个切片 = 一个可独立验证的端到端功能
- 切片完成后**立即 commit**，不攒到最后
- 未完成的功能用**功能标志**隐藏（`FEATURE_NEW_UI=false`）
- 每个切片可独立回滚（`git revert`）

### 🔍 Phase 5 Self-Review（Superpowers v5 — 必做）

写完全部 tasks.md 后，执行以下自检，**全部通过才能进入 Phase 6**：

**1. Spec Coverage（需求覆盖）**
- 逐条扫描 Phase 1 conversation.md 中的每个需求
- 确认每个需求都有对应的 Task
- 遗漏 → 补充 Task，不能"后面再说"

**2. Placeholder Scan（占位符扫描）**
搜索 tasks.md 中的以下模式，**全部修复**：
| ❌ 错误模式 | ✅ 修复方式 |
|------------|------------|
| `TBD`、`TODO`、`稍后实现` | 写实际代码 |
| `添加错误处理` | 写具体的 try/catch |
| `类似 Task N` | 复制实际代码 |
| `写测试覆盖上述` | 写实际测试代码 |
| `填充详情` | 直接写详情 |

**3. Type Consistency（类型一致性）**
- Task 3 定义的函数签名，Task 5/7 调用时是否匹配？
- 类型定义（interface/type/class）前后是否一致？
- 命名风格是否统一？

**4. File Isolation（文件隔离）**
- 是否有多个 Task 修改同一文件？
- 如果有，确认顺序和依赖关系已标注

**Self-Review 结果写入 tasks.md 末尾：**
```markdown
## Self-Review 结果
- Spec Coverage: ✅/❌ (N 个需求全部覆盖 / 遗漏: xxx)
- Placeholder Scan: ✅/❌ (无占位符 / 发现: xxx)
- Type Consistency: ✅/❌
- File Isolation: ✅/❌
```
