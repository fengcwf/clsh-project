# clsh-project Verification Checklist

> 从 SKILL.md 迁出的验证清单完整版。SKILL.md 保留指针。

## 流程合规

- [ ] 确认不是简单查询/单步操作（否则不应触发 clsh-project）
- [ ] 确认 Phase 1 已执行调研前置（调研摘要已写入 conversation.md 或大佬明确跳过）
- [ ] 确认 Phase 1-3 已完成且有文档产出（conversation.md / proposal.md / constitution.md）
- [ ] 确认 UI 项目 Phase 3 是否需要设计发散（2-3 mockup 变体，截图发飞书）
- [ ] 确认大佬已明确回复"确认"才进入下一 Phase
- [ ] 确认 tasks.md 中每个 Task 有验收标准 + 完整代码（无 TBD/TODO）
- [ ] 确认代码任务已派给 coder/artist，不是灵犀直接写
- [ ] 确认每个 Task 有 tester 卡
- [ ] 确认 Phase 6 Security Scan 已加载 `requesting-code-review` skill 执行
- [ ] 确认 Phase 6 Quality Review 已加载 `code-principles` skill 执行
- [ ] 确认 Phase 8 诊断已加载 `diagnose` skill 执行 6 阶段
- [ ] 确认 UI 项目 Phase 6 tester 卡包含 Browser QA 检查清单（必须含"截图验证"字样）
- [ ] 确认 agent 派发 context 包含 Pre-Commit 安全自检清单
- [ ] 确认 Phase 8 反馈走流程而非"顺手修了"
- [ ] 确认 Auto-Fix 不超过 2 轮后 escalate
- [ ] 确认每个 kanban task body 包含 proposal 相关章节 + constitution 约束 + 不在范围内声明
- [ ] 确认 Phase 1 中大佬描述现有行为时已代码交叉验证
- [ ] 确认满足条件的架构决策已记录为 ADR（raw/projects/<项目名>/docs/adr/）
- [ ] 确认新增子模块已读 AGENTS.md 并按其目录结构规范创建文件
- [ ] 确认每个 Task 的 checkpoint 包含 Spec Delta 字段
- [ ] 确认 review 卡 body 包含完整 Review Checklist 模板（5 维度逐项填写）
- [ ] 确认每个 Phase 完成后输出 Session Launch Guidance

## 验证合规（Layer 2）

- [ ] 确认声称"完成/修复/通过"前已走完 5 步验证函数（铁律 #14）
- [ ] 确认验证命令是新鲜执行的，不是复用之前的输出
- [ ] 确认 worker 修复后已走独立 tester 验证（不是只看 worker 的声明）
- [ ] 确认没有使用防辩解表中的借口跳过验证
