# Pitfall #143: Kanban "Done" ≠ Work Verified

## 场景

Phase 6 执行完毕后，灵犀看到 kanban 所有卡片状态为 `done`，直接宣布"全部完成"进入 Phase 7。

## 问题

Kanban `done` 状态只代表 worker 进程正常退出（`kanban_complete()` 被调用），不代表：
- 代码变更正确
- 验收标准全部满足
- tester 验证在实现之后执行

本次具体表现：
1. T7/T14/T19 tester 验证卡与实现卡并行派发（无 `parents` 依赖）
2. tester 在实现完成前执行验证 → 全部 FAIL
3. kanban 标记 tester "done"（完成了验证动作，只是结果是 FAIL）
4. 灵犀看到 19/19 done → 宣布完成 → 被用户纠正

## 铁律

**Phase 6 结束后、Phase 7 之前，灵犀必须执行独立的产出 review：**

1. 逐项 `grep`/`cat` 验证每条验收标准
2. 对比 before/after 差异
3. 检查 tester 验证报告的实际内容（PASS 还是 FAIL）
4. 如果 tester FAIL，分析原因（是实现问题还是 timing 问题）

## 验证模板

```bash
# 验证每项整改
for task in T1 T2 T3 ...; do
  echo "=== $task ==="
  # 执行验收标准中的验证命令
  grep -r "预期关键词" /opt/project/src/ | wc -l
  cat /path/to/modified/file | head -20
done
```

## 关联

- Pitfall #141: 审查→整改项目交接模式（含 tester 依赖链要求）
- kanban-orchestrator skill: "Done ≠ Verified" pitfall
