# 阶段确认模板 / Phase Confirmation Templates

> **重要规则**: 代码示例必须独占一行，前后用空行隔开。不要将代码嵌入段落文本中。
> **确认码**: 每个 Phase 结束时运行对应 gate 脚本，将生成的确认码替换 `[CODE]` 占位符。确认码必须独占一行。

---

## Phase 0+1: 需求准备与澄清确认

```
✅ Phase 0+1 完成确认

历史教训: [已读取/已匹配]
PRODUCT.md: [已完成] — 用户故事 [N] 个, 不变量 [N] 个
conversation.md: [已完成] — 需求澄清对话记录

gate-phase1 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 2 — 方案设计与技术验证
```

---

## Phase 2: 方案设计与技术验证确认

```
✅ Phase 2 完成确认

TECH.md: [已完成]
方案对比: [N] 个方案, 推荐方案: [方案名]
架构决策 ADR: [N] 个
文件变更范围: [N] 个文件

gate-phase2 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 3 — 设计文档
```

---

## Phase 3: 设计文档确认

```
✅ Phase 3 完成确认

proposal.md: [已完成] — 设计决策 [N] 项
constitution.md: [已完成] — 约束 [N] 条, 禁止操作 [N] 条

gate-phase3 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 4 — 机械检查
```

---

## Phase 4: 机械检查与流程合规确认

```
✅ Phase 4 完成确认

overview.md: [已检查]
conversation.md: [已检查]
proposal.md: [已检查]
constitution.md: [已检查]
PRODUCT.md: [已检查]
TECH.md: [已检查]

gate-phase4 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 5 — 实现计划
```

---

## Phase 5: 实现计划确认

```
✅ Phase 5 完成确认

tasks.md: [已完成]
任务总数: [N] 个 (coder: [N], tester: [N], artist: [N])
INV-* 覆盖: [N]/[N]
US-* 覆盖: P0 [N]/[N], P1 [N]/[N], P2 [N]/[N]

gate-phase5 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 6 — 分发执行
```

---

## Phase 6: 分发执行确认

```
✅ Phase 6 完成确认

代码任务: [N]/[N] 完成
测试任务: [N]/[N] 完成
tester 报告: [PASS/FAIL]
C7 fresh-context review: [PASS/FAIL]

gate-phase6 检查: [PASS/FAIL]
gate-phase7 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 7 — 完成归档
```

---

## Phase 7: 完成归档与流程复盘确认

```
✅ Phase 7 完成确认

completion-summary.md: [已完成]
retrospective.md: [已完成]
handoff.md: [已完成]
归档路径: changes/archive/

gate-phase7 检查: [PASS/FAIL]
确认码: [CODE]

下一步: 进入 Phase 8 — 反馈循环
```

---

## Phase 8: 反馈循环确认

```
✅ Phase 8 完成确认

bug 修复: [N]/[N] 已修复
conversation.md: [已更新]
diagnosis.md: [已完成]
bugfix-spec.md: [已完成]

gate-phase8 检查: [PASS/FAIL]
确认码: [CODE]

项目完成: [是/否]
```

---

## 代码独占行规则 / Code On Its Own Line Rule

在所有文档中，代码必须遵循以下格式：

**正确** ✅

运行以下命令来验证安装：

```bash
[command here]
```

安装成功后，你会看到：

```json
{"status": "ok"}
```

**错误** ❌

运行 `[command here]` 来验证安装，你会看到 `{"status": "ok"}`。

---

## 确认格式规范

1. 每个阶段确认使用代码块包裹
2. 状态标识使用 ✅ (完成) 或 ❌ (未完成)
3. 确认码 `[CODE]` 必须独占一行，由 gate 脚本生成后替换
4. 确认必须列出该 Phase 的核心产出物和门禁检查结果
