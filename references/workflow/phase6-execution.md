# clsh-project — Phase 6: Ralph Loop 分发执行

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 6: Ralph Loop 分发执行

### ⚠️ 角色分配规则（不可违反）

| 任务类型 | 必须派给 | 灵犀能做吗 | 设计规范来源 |
|---------|---------|-----------|------------|
| 后端 API | coder | ❌ | constitution.md |
| 前端逻辑 | coder | ❌ | constitution.md |
| UI 模板 | artist | ❌ | **OD 设计系统 DESIGN.md** + constitution.md |
| CSS 样式 | artist | ❌ | **OD 设计系统 DESIGN.md** + popular-web-designs |
| 测试验证 | tester | ❌ | constitution.md |
| 文档编写 | 灵犀 | ✅ | — |
| 协调汇报 | 灵犀 | ✅ | — |

**🎨 UI/样式任务设计规范注入（artist 派活必做）：**

当任务类型为 UI 模板或 CSS 样式时，delegate_task 的 context 必须包含：
1. 从 `/opt/open-design/design-systems/` 选取匹配的设计系统 DESIGN.md 摘要
2. 项目 constitution.md 中的 UI 相关约束
3. 如有 Phase 1 Visual Companion 产出的设计方向，附上参考

**选取设计系统的规则：**
- 项目有明确品牌参考 → 直接用对应设计系统（如"类似 Linear" → Linear DESIGN.md）
- 项目无明确参考 → 根据项目类型选择：
  - 管理后台/Dashboard → Material Design 或 Ant Design
  - 落地页/营销页 → Stripe 或 Vercel
  - 内容平台/博客 → Notion 或 Medium
  - 移动端优先 → Apple HIG 或 Tailwind UI

### ⚠️ 5 步验证函数（Superpowers 移植，2026-05-29）

**核心原则：没证据不许声称完成。**

```
BEFORE 声称任务完成/修复成功/测试通过：
  Step 1: IDENTIFY — 什么命令/证据能证明声明成立？
  Step 2: RUN — 执行验证命令（新鲜的，不复用之前的输出）
  Step 3: READ — 完整读取输出 + exit code
  Step 4: VERIFY — 输出是否符合预期？（逐条对照验收标准）
  Step 5: REPORT — 带证据汇报。跳过任何一步 = 违规
```

**⛔ 防辩解表：**

| 借口 | 现实 | 正确做法 |
|------|------|---------|
| "CodeWhale 说改好了" | CodeWhale ≠ 功能验证 | 跑验证命令 |
| "代码看起来对" | 代码 ≠ 运行中的系统 | 浏览器/curl 实际验证 |
| "之前测试过了" | 之前的测试 ≠ 当前的代码 | 重新执行验证 |
| "应该可以了" | 应该 ≠ 验证过 | 走完 5 步 |
| "这次改动很小" | 小改动也会引入回归 | 跑回归测试 |
| "agent 自己验证过了" | 自己验自己 = 不独立 | 灵犀独立验证或派 tester |

**集成位置：** Step 4 (灵犀验证 checkpoint) 和 Step 7 (Tester 验证) 必须走 5 步验证函数。

详见 `references/methodology/verification-and-ratchet.md` §一、§二。

### ⚠️ Ralph Loop 执行模式（核心）

**参考：** `references/methodology/ralph-loop-analysis.md`

**核心原则：**
- 灵犀是循环编排者，agent 是单步执行器
- 每轮通过 CHECKPOINT 客观验证，不依赖 agent 自判
- 失败反馈注入重试，最多 2 轮后 escalate 给大佬
- 文件系统 + git 作为记忆层（不是 agent 的上下文）

每个 Task 必须按以下状态机执行：

```
Task 开始
  ↓
Step 1: agent 读取任务描述 + constitution
  ↓
Step 2: agent 执行任务（TDD：先写失败测试 → 实现 → 通过测试）
  ↓
Step 3: 输出 CHECKPOINT（产出物自检）
  ↓
Step 4: 灵犀验证 checkpoint
  ├─ FAIL → 返回 Step 2（重试），最多 2 轮 → 仍 FAIL → 派 fix agent
  └─ PASS ↓
  ↓
Step 5: Security Scan（安全扫描）
  硬编码密钥、SQL 注入、shell 注入、eval/pickle、路径遍历
  ├─ 有问题 → 派 fix agent → 重新 Step 5（最多 2 轮）
  └─ PASS ↓
  ↓
Step 6: Quality Review（代码质量）
  命名、DRY、错误处理、测试覆盖
  ├─ 有问题 → 派 fix agent → 重新 Step 6（最多 2 轮）
  └─ PASS ↓
  ↓
Step 7: Tester 验证（功能测试 + 回归测试）
  ├─ 有 UI 的项目 → 必须走浏览器自动化 QA（见下方 §Browser QA）
  └─ 纯后端项目 → 传统 tester 验证即可
  ↓
Step 8: CHECKPOINT: PASS → 标记 Task 完成 → 进入下一 Task
  ↓
Step 9: Spec-Code 同步（Kiro — 必做）

### ⚠️ Blocked 状态处理协议（必须遵守）

**核心规则：`blocked ≠ done`，blocked 状态不触发依赖引擎 promote 子任务。**

```
worker 遇到问题无法继续
  ↓
Step B1: worker 调用 kanban_block(reason="具体阻塞原因")
Step B2: worker 调用 kanban_comment(body="完整上下文 + 已尝试的方案")
  ↓
Step B3: 灵犀收到通知后介入
  ├─ 产出物已完成 → hermes kanban complete <id>（标记 done，依赖引擎继续）
  ├─ 产出物部分完成 → hermes kanban complete <id> + 创建新卡处理剩余工作
  └─ 产出物不可用 → hermes kanban complete <id> + 创建 fix 卡（parents=[原卡]）
  ↓
Step B4: 创建 fix 卡（如需要）
  → assignee = 原 worker 或另一个 coder（不是灵犀自己）
  → parents = [原实现卡]（必须等原卡 done 后 fix 卡才 promoted）
  → body 包含：具体问题描述 + B2 的 comment 上下文
```

**⛔ 禁止：**
- worker 调用 `kanban_block()` 后，灵犀不 complete 原卡就直接创建 fix 子卡
  → 结果：fix 卡永远卡在 todo（parent 未 done）
- worker 遇到问题直接 `kanban_complete(summary="...")` 假装完成
  → 结果：产出物缺失但状态为 done，后续步骤踩坑
  检查 proposal.md 中的设计是否与实际代码一致：
  - 读取 proposal.md 中该 Task 对应的设计描述
  - 对比实际代码实现
  - 如有偏差 → 更新 proposal.md（不是"后面再补"）
  - 更新内容：接口变更、架构调整、新增/删除的功能点
```

**Checkpoint 格式（每个 Task 完成后必须输出）：**

```
CHECKPOINT: <任务名称>
产出物: <文件路径/内容摘要>
自检: <是否满足验收标准>
状态: PASS / FAIL
如 FAIL: <具体问题描述>
```

**🔬 微蒸馏（checkpoint 后必做，10 秒）：**
回答三个问题，有任何"是"就 append 到 `~/.hermes/skills/productivity/project-wrap-up/learnings.md`（每 Task 最多 1 条，可操作措辞，格式：`- [日期 Task N] 内容`）：
- 这个 Task 有什么出乎意料的？
- 如果重来一次，会怎么做不同？
- 有没有发现新的陷阱/模式？
三个都是"没有"→ 跳过。

**⚠️ Checkpoint 输出截断规则（Q2 改进 #4）：**
- Checkpoint 输出限制在 **200 字以内**
- 编译日志、测试输出等长文本 → 写入 `/tmp/<project>-<task>.log`，Checkpoint 只写文件路径
- 禁止将完整编译输出/测试日志直接输出到上下文
- 原因：一个 Task 的往返可能消耗 2000-5000 token，截断可节省 50-80%

### 🌐 Browser QA（UI 项目必做，借鉴 gstack /qa）

**适用条件：** 项目有前端 UI（Web 页面、管理后台、落地页等）。

**Tester 执行流程：**
1. 启动项目 dev server（如果尚未运行）
2. 用 `mcp_mp_browse_webpage` 打开目标页面
3. 按验收标准逐项操作：
   - 页面加载无报错（检查 console）
   - 核心交互可点击/可输入
   - 表单提交有反馈
   - 响应式布局在不同宽度下正常
   - 无明显视觉错位/溢出
4. 截图关键状态作为测试证据
5. 发现 bug → 记录到 fix 卡（含截图 + 复现步骤）

**与传统 tester 的区别：**
- 传统 tester：读代码 + 运行命令检查 → 可能遗漏 UI 层问题
- Browser QA：真实浏览器操作 → 能发现渲染/交互/布局问题

**⛔ Browser QA 不能替代单元测试。** 两者互补：单元测试覆盖逻辑，Browser QA 覆盖集成。

### 🛡️ Pre-Commit 安全自检（借鉴 gstack /careful）

**时机：** 每个 Task 执行过程中，agent 提交代码前必须完成以下自检。

**自检清单（agent 在 context 中收到，不依赖 agent 自觉）：**

```
## Pre-Commit 安全自检（提交前必做）
- [ ] 无硬编码密钥/token/password（grep 检查）
- [ ] 无 eval()、exec()、pickle.loads() 等危险调用
- [ ] SQL 查询使用参数化（非字符串拼接）
- [ ] 用户输入有验证/转义（防 XSS/注入）
- [ ] 文件路径操作无目录遍历风险
- [ ] 无 console.log/print 泄露敏感信息
- [ ] 依赖版本固定（无 ^ 或 > 范围）
```

**与 Phase 6 Step 5 Security Scan 的区别：**
- Pre-Commit 自检：agent 在开发过程中自行检查（左移，更早发现）
- Security Scan：灵犀在 checkpoint 后集中审查（兜底，不依赖 agent）

**两者都做，不互相替代。** Pre-Commit 减少 Security Scan 的返工率。

### 任务派发流程

**⚠️ CodeWhale ACP 派发铁律（Way C）：**

灵犀只给**目标 + 参考文件 + 约束 + 验收标准**，不做代码推理。CodeWhale 自己读代码、分析问题、决定方案。

❌ 灵犀不应该给：具体 CSS 代码、详细实现步骤、"删 18 处 !important"、"用作用域提升优先级"
✅ 灵犀应该给："大佬说按钮丑，重做 UI。参考 style.css 和 CronMonitor.mjs。浅色毛玻璃主题。"

详见 `references/integration/codewhale-acp-integration.md` §Way C 派发模式。

```
对于计划中的每个 Task:
  1. 读取 constitution.md
  2. 根据任务类型选择 agent（coder/artist/tester）
  3. kanban_create 创建实现卡（绝对路径 + 验收标准 + 不在范围内）
  3.1. ⛔ task body 必须注入 proposal 相关章节（代码示例 + 文件路径 + 禁止事项），不能只写一句话描述。coder 只看 body，不读 wiki 文档。
  4. dispatcher 自动派发 ready 状态的卡
  5. worker 执行任务
  6. worker 完成后输出 CHECKPOINT（产出物自检）
  7. 灵犀验证 checkpoint（产出物 ls 验证）
     ├─ FAIL → 返回 Step 5（重试），最多 2 轮 → 仍 FAIL → 创建 fix 卡
     └─ PASS ↓
  8. kanban_create 创建 review 卡（assignee=tester, parents=[实现卡]）
     ⚠️ Review 卡必须在 Step 7 验证 PASS 后才能创建
  9. dispatcher 自动派发 review 卡
  10. tester 执行 Security Scan + Quality Review
  11. PASS → 标记 Task 完成
  12. FAIL → 创建 fix 卡（不是实现者本人）→ 重新 review（max 2轮）
  13. 全部 Task 完成 → Final Integration Review
```

**Review 卡创建规范：**
```bash
hermes kanban create "[项目名] Review: <任务名>" \
  --assignee tester \
  --body "...审查维度...\
PASS/FAIL 输出要求..." \
  --parent <实现卡ID> \
  --json
```
- Review 卡依赖实现卡（parents），实现卡完成后自动 promoted → ready
- Review 卡 body 必须包含：审查维度 + PASS/FAIL 输出格式 + 上下文（实现卡ID）
- **UI 项目：** Review 卡 body 必须包含「Browser QA 检查清单」（见上方 §Browser QA）

**Wave 并行派发策略（Kiro Specs 模式）：**

基于依赖图将任务分层（Wave），同层任务并行，跨层串行：

```
依赖图分层:
Wave 1: Task 1, Task 2 (无依赖)         ← 同时创建，dispatcher 并行执行
Wave 2: Task 3 (依赖 T1), Task 4 (依赖 T2) ← T1/T2 完成后自动 promoted
Wave 3: Task 5 (依赖 T3, T4)             ← T3/T4 完成后自动 promoted
```

**派发流程：**
1. 按依赖图计算 Wave 层级（拓扑排序）
2. 创建所有卡（指定 `--parent`），初始 blocked 或无 parent 的直接 ready
3. dispatcher 自动派发 ready 卡，完成后 promote 子卡
4. Review 卡在 checkpoint 验证 PASS 后创建（不是同时创建）

**`hermes kanban swarm` 快速模式（可选）：**
```bash
hermes kanban swarm "项目目标" \
  --worker coder:"Task 1: 数据模型":skill1,skill2 \
  --worker coder:"Task 2: API 层":skill1 \
  --verifier tester \
  --synthesizer coder
```
适合：3+ 个独立任务 + 需要 verifier + 需要 synthesizer 汇总。

**进展监控：**
```bash
hermes kanban list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data:
    if '项目名' in t.get('title',''):
        print(f\"{t['id']} | {t['status']} | {t['title'][:60]}\")
"
```

### ⚡ Phase 6 超时机制（Q5 方案 C — 2026-05-19 实施）

**三层防护：子 agent 自带超时 + 产出物预检 + 灵犀 5 分钟轮询**

#### 第 1 层：子 agent 自带超时
派活时在 delegate_task 的 context 中写明：
```
## 超时规则
- 本任务必须在 N 分钟内完成（coder: 10分钟, worker: 5分钟, tester: 5分钟）
- 超时则输出 TIMEOUT 并退出，不要继续尝试
- 产出物写到 /tmp/<project>-<task>/ 目录
```

#### 第 2 层：产出物预检
- agent 开始工作前先创建产出物目录：`mkdir -p /tmp/<project>-<task>/`
- 灵犀通过 `ls /tmp/<project>-<task>/` 判断 agent 是否在工作
- **5 分钟内产出物目录无任何变化 → 判定为卡死**，不再等待

#### 第 3 层：灵犀 5 分钟轮询
Phase 6 执行过程中，灵犀每 5 分钟检查一次：
```bash
hermes kanban list --json | python3 -c "
import json, sys, time
data = json.load(sys.stdin)
now = time.time()
for t in data:
    if t['status'] == 'running' and '项目名' in t.get('title',''):
        started = t.get('started_at', 0)
        elapsed = (now - started) / 60
        print(f\"{t['id']} | {elapsed:.0f}min | {t['assignee']} | {t['title'][:50]}\")
"
```
- running 超过 5 分钟 → 检查产出物目录
- 产出物存在 → `hermes kanban complete <id>` 手动标记完成
- 产出物不存在 → 执行超时自动回滚（Phoenix）→ escalate 给大佬

#### Worker Heartbeat（长任务可选）
- 预计 >5 分钟的任务，worker 应每 2-3 分钟调用 `kanban_heartbeat(note="进度描述")`
- dispatcher 的 passive heartbeat 每 60s 检查 PID 是否存活（自动延长 claim）
- heartbeat 不能替代显式超时机制，只是辅助监控

#### 超时自动回滚（Phoenix — 2026-05-19 实施）

子 agent 超时/卡死后，灵犀执行以下回滚流程：

```bash
# 1. 检查未提交的改动
cd <项目目录>
git diff --stat
git status --short

# 2. 如果有未提交的改动 → stash（不直接提交半成品）
git stash save "auto-rollback: <task-name> timeout at $(date +%Y%m%d-%H%M)"

# 3. 如果有未 stash 的改动 → 记录到日志
echo "TIMEOUT_ROLLBACK: <task-name> | $(date) | $(git diff --stat)" >> /tmp/<project>-timeout.log

# 4. 通知大佬
# 发送飞书告警：任务超时 + 已自动回滚 + 需要人工介入
```

**回滚原则：**
- ⛔ 禁止直接提交半成品代码
- ✅ 未提交改动 → `git stash`，保留现场供大佬检查
- ✅ 已提交改动 → `git revert <commit>`，回滚到超时前状态
- ✅ 回滚后通知大佬，不自行重试

### ⛔ 执行红线

- **禁止灵犀直接写代码** — 即使"很快能做完"也必须派
- **禁止跳过 checkpoint** — 每个 Task 必须有产出物验证
- **禁止自己测自己写的代码**
- **禁止跳过 tester 卡**
- **禁止在 Phase 4 确认前开始编码**
- **禁止跳过 artist 做 UI**
- **禁止跳过 Security Scan** — 即使"代码很简单"
- **禁止 fix agent 超过 2 轮** — 2 轮后必须 escalate 给大佬
- **禁止 agent 自判完成** — 必须通过客观验证
