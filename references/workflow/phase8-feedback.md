# clsh-project — Phase 8: 反馈循环

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 8: 反馈循环（大佬测试后）

**触发条件：** 大佬测试后反馈问题

### ⛔ Phase 8 执行规范（不可违反）

#### 1. 必须用 delegate_task 派发修复任务

**Phase 8 修复 = Phase 6 执行，必须角色分离。**

| 修复类型 | 必须派给 | 工具集 |
|---------|---------|--------|
| 后端 API 修复 | coder | terminal, file |
| 前端逻辑修复 | coder | terminal, file |
| UI/CSS 修复 | artist | terminal, file |
| **测试验证** | **tester** | **terminal, file, web, browser** |

**⛔ 禁止灵犀直接改代码。** 即使"很快能做完"也必须派 delegate_task。

#### 2. Tester 必须使用浏览器工具

**tester 的 toolsets 必须包含 `web` 和 `browser`（或 `computer_use`）。**

tester 验证时：
- **必须用浏览器访问页面**，不能用 curl/API 替代
- 浏览器工具：`mcp_mp_browse_webpage` 或 `browser` toolset
- 验证内容：页面渲染、交互功能、CSS 样式、响应式布局
- 如果浏览器工具不可用，向大佬报告，不要降级为 curl 测试

**tester 派发模板：**
```
toolsets: ["terminal", "file", "web", "browser"]
```

#### 3. 每轮必须归档 wiki

**每轮 Phase 8 修复完成后，必须创建变更目录并归档：**

```
wiki/projects/<项目名>/changes/round<N>-feedback/
├── conversation.md    ← 大佬反馈的问题列表
├── diagnosis.md       ← diagnose 6 阶段记录
├── fixes.md           ← 每个问题的修复方案 + 派发记录
└── test-report.md     ← tester 验证报告
```

**全部修复完成后，归档到 archive/：**
```
wiki/projects/<project>/changes/archive/round<N>-feedback/
```

**⛔ 禁止只在对话中修复，不写 wiki 记录。**

#### 4. 大修复用 kanban，小修复用 delegate_task

| 场景 | 方式 |
|------|------|
| ≤3 个简单修复 | delegate_task 直接派发 |
| >3 个修复 或 需要追踪 | kanban 创建卡 + delegate_task |
| 跨 session 的大修复 | kanban（状态持久化） |

**kanban 创建规范：**
```bash
# 创建修复卡
hermes kanban create "[项目名] Round<N>: <问题简述>" \
  --assignee coder/artist \
  --body "问题描述 + 验收标准" \
  --json

# 创建 review 卡（依赖修复卡）
hermes kanban create "[项目名] Review: <问题简述>" \
  --assignee tester \
  --body "验证步骤 + PASS/FAIL 标准" \
  --parent <修复卡ID> \
  --json
```

### ⚠️ 上下文溢出防护（2026-05-21 教训，2026-05-21 强化）

**Phase 8 大量 bug 修复时，必须控制节奏。两次中断 = 必须更激进地控制上下文：**

#### 核心原则：每轮最多修 3-4 个 bug（不是 5-6 个）

1. **每轮最多修 3-4 个 bug** — 超过 4 个时必须分批，每批修完先重启测试
2. **后端和前端分开修** — 先修后端（通常少），再修前端
3. **Agent 反复超时后向大佬报告** — 不要全部 fallback 到灵犀直接改代码（违反角色分离 + 上下文爆炸）
4. **每批修完后写 checkpoint** — 记录已修复项，防止 session 断开后丢失进度
5. **修完一批先 `pm2 restart` + 基础测试** — 确确无回归再继续下批

#### 上下文节省策略（每次修复必做）

6. **用 `execute_code` 批量读代码** — 不要在主对话中逐个 read_file，用 execute_code 一次读多个文件并输出关键片段
7. **每个 bug 只读相关代码片段** — 不加载整个文件，用 offset/limit 或 grep 定位
8. **修一个验证一个** — 不要一次性修改所有文件再验证
9. **长输出写入 /tmp/ 而非主对话** — 测试结果、日志等写入文件，只在对话中放结论
10. **进度写入 checkpoint 文件** — `/tmp/<project>-round<N>-checkpoint.md`，记录已修/待修/阻塞项

#### 中断恢复协议

当 session 因上下文过大中断后重启：
1. 读取 `/tmp/<project>-round<N>-checkpoint.md` 恢复进度
2. 如果 checkpoint 不存在，从项目文档 `changes/` 目录恢复
3. **从上次中断的 bug 继续，不重做已完成的修复**
4. 向大佬确认恢复的上下文是否正确

### ⚠️ Diagnose 6 阶段循环

**参考：** `diagnose` skill

每个阶段有明确入口/出口条件。不满足出口条件不能进入下一阶段。

```
Stage 1: 建循环（Build the Loop）
  入口：大佬反馈了 bug/异常
  操作：固化复现命令（单命令 pass/fail）
  出口：有一键复现命令，输出明确 pass/fail 信号
  ↓
Stage 2: 复现（Reproduce）
  入口：复现命令已建立
  操作：运行 3 次确认稳定性
  出口：稳定复现 或 确认非确定性（统计复现率）
  ↓
Stage 3: 假设（Hypothesize）
  入口：问题已稳定复现
  操作：读完整错误 → 查 git log → 追踪数据流 → 形成具体假设
  出口："我认为 X 是 root cause，因为 Y，如果做 Z 应能观察到 W"
  ↓
Stage 4: 插桩（Instrument）
  入口：有具体假设
  操作：选最快反馈方法（类型检查<1s → 单测1-5s → 断点5-30s → 集成测试）
  出口：有证据支持或否定假设
  ↓
Stage 5: 修复（Fix）
  入口：证据确认 root cause
  操作：先写回归测试（FAIL → 修复 → PASS → 全量测试无回归）
  出口：回归测试通过，全量套件无回归
  Rule of Three：第3次修复失败 → 停止，质疑架构
  ↓
Stage 6: 复盘（Retrospect）
  入口：bug 已修复
  操作：为什么这个 bug 存在？防御措施？清理插桩？记录教训？
  出口：防御措施已添加/已评估不需要
```

**非确定性 bug 时**：Stage 2 → 统计复现（跑 N 次算失败率），Stage 4 → 用断言而非 print（失败立即停止，不被日志淹没）。

### 路径 A：Bug 修复

**Bugfix Spec 格式（Kiro 模式）：**

每个 bug 在 diagnose 前先写结构化 spec，确保诊断有锚点：

```markdown
## Bug Spec: {问题标题}

**当前行为**: {实际发生了什么}
**期望行为**: {应该发生什么}
**复现命令**: {单命令 pass/fail}
**影响范围**: {哪些功能/页面/API 受影响}

### Diagnose
- Stage 1 复现命令: `{命令}`
- Stage 2 复现稳定性: {N/N 次复现}
- Stage 3 根因假设: {X 是 root cause，因为 Y}
- Stage 4 验证证据: {支持/否定假设的证据}

### Fix
- 修改文件: {文件列表}
- **需要修改的函数/端点**: {列出所有调用点，不要只写"修复X功能"}
- 回归测试: {测试命令 + 结果}
- 防御措施: {已添加/已评估不需要}
```

> ⚠️ **教训（2026-05-24）：** Spec 说"修复 URL 生成"但没列出所有函数 → coder 只改了 `createShare()`，漏了 `listShares()` 和 `findShareByPath()`。**必须列出所有需要修改的函数/端点，不能只描述功能。**

**流程：**
```
大佬反馈 bug
  → 记录 conversation.md
  → 写 Bugfix Spec（当前行为/期望行为/复现命令/影响范围）
  → diagnose 6 阶段（Stage 1-6）
  → 创建修复任务 → 派 coder/artist
  → tester 验证 → 汇报
```

**与 diagnose 的关系：** Bugfix Spec 是 diagnose 的输入锚点。Stage 1-2 填充复现信息，Stage 3-4 填充根因和证据，Stage 5-6 填充修复和防御。

### 路径 B：体验优化
```
大佬反馈体验问题
  → 记录 conversation.md
  → 评估影响范围
  → 创建优化任务 → 派 artist
  → tester 验证 → 汇报
```

### 路径 C：需求变更
大佬提出新需求/方向变化
  → 判断变更级别：
     ├─ 功能追加（在现有方向上增加功能）
     │   → 能追加：更新 proposal.md，回到 Phase 3
     │   → 不能追加：新变更目录，从 Phase 1 开始
     │
     └─ 方向变化（核心定位/架构/目标用户变化）
         → ⛔ 禁止回到 Phase 3
         → 必须：新变更目录 + 从 Phase 1 开始
         → 必须：归档旧变更（status: superseded）
         → 必须：更新 overview.md 说明方向变化
         → 必须：更新 conversation.md 记录变更原因

> ⚠️ **教训（2026-05-19）：** 项目做到一半，大佬说"不做博客了，改做内容引擎"。灵犀直接在旧代码上修改，跳过 Phase 1-5，导致项目文档和实际代码不一致。**方向变化 = 必须回 Phase 1，不能回 Phase 3。**

### ⛔ 反馈循环红线
- **禁止"顺手修了"**
- **禁止跳过 tester**
- **禁止不记录就修**
- **禁止跳过 diagnose 的 Stage 1-2**（不复现就修 = 瞎猜）

> ⚠️ **教训（2026-05-15）：** 大佬说"测试有问题"，灵犀直接自己修复了，跳过了 Phase 8 的全部流程。
