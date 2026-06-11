# clsh-project 流程总览

## 流程图

```
Phase 1: 需求澄清（调研循环 + 机械确认码）→ conversation.md
    ↓ [大佬确认码]
Phase 2: 提出 2-3 个方案 + 推荐理由 → 大佬选择
    ↓ [大佬确认码]
Phase 2.5: Technical Spike（可选）
    ↓ [VALIDATED]
Phase 3: 设计文档 → proposal.md + constitution.md
    ↓ [大佬确认码]
Phase 4: 自检 + 大佬确认
    ↓ [大佬确认码]
Phase 5: 实现计划 → 派 coder 写 tasks.md → 灵犀 review → [大佬确认码]
    ↓
Phase 6: Ralph Loop 分发执行（coder/artist/tester）
    ↓ [tester 通过] → 灵犀 review tester 报告 → [大佬确认码]
Phase 7: 归档 + 流程复盘
    ↓
Phase 8: 反馈循环 → 回到 Phase 1 或 Phase 6
```

## Session Launch Guidance

| 完成 Phase | 下一步 | 建议 |
|-----------|--------|------|
| Phase 1-5 | `/clsh-project 继续 <项目名>` | 当前 session 继续 |
| Phase 6 | `/clsh-project 继续 <项目名>` | 3+ Task 建议新 session |
| Phase 7 | 等待大佬测试反馈 | — |
| Phase 8 | `/clsh-project 继续 <项目名>` | 每轮修复建议新 session |

## 项目暂存

大佬说"先存 wiki，不做"时：写 overview.md（状态 `planning`）+ proposal.md → 向大佬确认 → **不进入 Phase 2+**。
