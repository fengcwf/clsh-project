# Review Mode Lessons — workspace-review 复盘

## 定量对比：delegate_task vs kanban+skills

| 维度 | delegate_task 版 | kanban+skills 版 | 提升 |
|------|-----------------|-----------------|------|
| 卡 1 发现数（代码质量） | 7 | 13 | +86% |
| 卡 3 发现数（安全） | 7 | 20 | +186% |
| file:line 覆盖 | 部分 | 全面 | 显著 |
| 攻击向量分析 | 无 | 有 | 显著 |
| 产出物持久化 | 仅 2/5 卡有文件 | 5/5 卡有输出 | 显著 |

## 10 条教训

### #1: C8 skills 注入必须真实执行（不是写在文档里）

事后补 tasks.md 的 `skills:` 字段不算合规。Skills 必须在 kanban worker 启动时注入到环境中。

### #2: delegate_task 不能替代 kanban

delegate_task 绕过了 skill 注入，导致审查质量下降 40-186%。Review 项目也必须走 kanban。

### #3: C7 review 不能自判

灵犀不能自己打勾通过 C7。必须加载 doubt-driven-development skill + 外部验证（spawn reviewer 或大佬确认）。

### #4: Phase 4 机械检查不可跳过

即使项目是 Review Mode，也必须通过 `phase4-mechanical-check.py`。目录结构必须是标准格式（changes/ + source-of-truth/）。

### #5: 审查范围必须覆盖整个项目目录

不只是 src/，还要覆盖根目录脚本、config/、scripts/、ecosystem.config.cjs、package.json。

### #6: worker skills 必须存在于 assignee profile

创建 kanban 卡前必须检查 skill 是否在 worker profile 的 `.skills_prompt_snapshot.json` 中。不存在 → copy + snapshot update → 再 create card。

### #7: 审查卡 body 必须要求文件产出

不加 "将完整报告写入 /tmp/workspace-review-{task_id}.md" → worker 只写截断的 kanban summary，无法恢复。

### #8: tester 验证必须带证据

tester 不能只说 "PASS"，必须附验证命令输出。Review 项目的 tester 卡 body 要写具体的验证命令。

### #9: worker 产出物必须在灵犀 review 前持久化

kanban summary 被截断（卡 4 仅 2,539 字符，卡 5 仅 183 字符）。读取 kanban comment 需要 SQL 查询 DB。

### #10: 整改项目 = 新项目，需要独立 clsh-project 流程

审查报告作为需求输入，但不能直接在审查项目上改。新建 workspace-remediation 项目，走完整 Phase 1-7。
