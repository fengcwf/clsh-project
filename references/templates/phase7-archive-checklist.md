# Phase 7 归档参考

详细的归档操作手册见：`references/templates/archive-workflow.md`

## 快速检查清单

1. 更新 overview.md → status: done
2. 创建 completion-summary.md（位置：archive/<变更名>/）
3. 创建 retrospective.md（位置：archive/<变更名>/）
4. 归档变更目录（changes/<变更名>/ → archive/<变更名>/）
5. 同步 GitHub（git add -A → commit → push）
6. 更新 memory（精简摘要，注意 2200 字符上限）
7. **🔬 蒸馏评估**（加载 `project-wrap-up` skill）
   - eval.json 5 项 binary 评估 → 结果 append learnings.md
   - FAIL 项做故障分类（FLOW/AGENT/TOOL/KNOWLEDGE）
   - 条件触发深度蒸馏（learnings ≥10 或 eval ≤2/5）
8. 验证服务运行正常
