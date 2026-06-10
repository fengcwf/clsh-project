# 审查→整改项目交接模式

## 模式描述

当 Review 项目产出审查报告后，需要新建一个 Remediation 项目来执行整改。审查报告的 P0-P3 优先级直接映射为整改项目的轮次。

## 交接流程

1. **审查项目 Phase 7 完成** → 产出 `CODE-REVIEW-*.md`
2. **整改项目 Phase 1** → 审查报告作为需求输入（不需要重新调研）
3. **整改项目 Phase 2** → 按 P0→P1→P2 分批（方案 A：按优先级）
4. **整改项目 Phase 3** → proposal.md 引用审查报告的具体发现编号
5. **整改项目 Phase 5** → tasks.md 的每个 Task 对应审查报告的一项发现

## 整改项目 tasks.md 结构

```markdown
### Round 1: P0 安全修复（N 项 + 1 验证）

**Task 1** | 角色：coder | skills: ...
对应审查报告 §2.5 #1。行动：...。验收：...

**Task N** | 角色：tester | skills: ...
Round 1 验证：N 项 P0 修复全部生效，无回归

### Round 2: P1 改进（N 项 + 1 验证）
...
```

**关键**：每个轮次最后必须有一个 tester 验证卡。**验证卡必须依赖对应轮次的所有实现卡**，否则 tester 会在实现完成前执行验证，产生无意义的 FAIL 结果：

```python
# Round 1: 实现卡 T1-T6，验证卡 T7
for t_impl in [t1, t2, t3, t4, t5, t6]:
    hermes kanban link t_impl t7  # T7 依赖所有实现卡

# Round 2: 实现卡 T8-T13，验证卡 T14
for t_impl in [t8, t9, t10, t11, t12, t13]:
    hermes kanban link t_impl t14
```

**不设依赖的结果（2026-06-10 教训）：** T7/T14/T19 全部在实现卡之前执行 → 验证全部 FAIL → kanban 标记 "done"（tester 完成了验证动作，只是结果是 FAIL）→ 灵犀看到 19/19 done 就宣布完成 → 被用户纠正。

**铁律：Phase 6 完成后、进入 Phase 7 前，灵犀必须独立 review 实际产出（不信任 kanban "done" 状态）。**

## 审查报告 → 整改 Task 映射示例

| 审查报告发现 | 整改 Task | 角色 |
|-------------|----------|------|
| §2.5 #1: 硬编码 SESSION_SECRET | Task 1: 删除 tmp 脚本 | coder |
| §2.5 #2: .env 备份含密钥 | Task 2: 删除 .env.bak | coder |
| §2.5 #3: GraphQL 注入 | Task 3: 修 docker.mjs | coder |
| §2.5 #4: Math.random OTP | Task 4: 改 crypto.randomInt | coder |
| ... | ... | ... |
| Round 1 全部 | Task N: Round 1 验证 | tester |
