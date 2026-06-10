## Pitfall #137: Phase 模板 --skill 注入不一致（2026-06-10 教训）

**场景：** Phase 6 模板的 kanban create 命令有 --skill 参数，但 Phase 8 模板没有。灵犀按模板执行时，Phase 6 的 worker 加载了领域技能（test-driven-development 等），Phase 8 的 worker 没有。

**根因：** C8 规则（"kanban 派发必须注入 skills"）在 Phase 6 checklist 中内嵌了技能映射，但 Phase 8 反馈模板是独立编写的，没有同步 --skill。两个模板各自维护，没有交叉检查。

**数据：** 2026-06-09 审计发现 106 个 kanban 任务中仅 2 个带 --skill（1.9%）。Phase 8 反馈循环占了大量任务，但模板中 kanban create 命令完全没有 --skill。

**铁律：**
1. 任何包含 `hermes kanban create` 的模板，命令中必须有 `--skill` 参数
2. 新增/修改模板时，必须 grep 所有模板文件确认 --skill 一致性
3. 技能映射表（coder/tester/artist 对应哪些 skills）在 SKILL.md Phase 6 checklist 中定义，所有模板引用同一份

**验证：** `grep -c "\-\-skill" <template-file>` 应该 ≥ 2（coder + tester 各一次）

**修复（2026-06-10）：** Phase 8 feedback template + workflow 均已补充 --skill 注入。
