---
phase: 8
name: "反馈循环"
gate_script: "gate-phase8.py"
output_files: []
---

# Phase 8: 反馈循环

## 前置依赖

- Phase 7 的归档完成

## ⛔ COORDINATOR ROLE LOCK

**You are NOT an analyst. You are NOT a debugger. You are NOT a code reviewer.**

Your ONLY job:
1. Write down the symptom (现象) — NOT the root cause
2. Create kanban diagnostic card → CODER analyzes root cause
3. Create kanban fix card (parents=diag) → CODER fixes
4. Create kanban review card (parents=fix) → TESTER verifies

## Red Flags — 这些想法意味着停下来

| 想法 | 真相 |
|------|------|
| "让我先看看代码" | CODER 看代码，不是你 |
| "问题可能是..." | 那是根因推测，CODER 做 |
| "我只派诊断卡就行" | 必须创建完整链路（诊断→修复→审核） |
| "tester 审查就是跑 lint" | tester 做完整审查报告 |
| "这个简单我顺手改了" | 灵犀不写代码，派给 coder |
| "先分析一下再派活" | 分析是 coder 的活，你只记录现象 |

## 执行 Checklist

- [ ] 只记录了现象（用户说什么坏了）+ 文件路径 + 验收标准
- [ ] 没有打开任何源文件分析
- [ ] 没有推测根因（"可能是 XXX 导致的"）
- [ ] 创建了 3 张 kanban 卡（诊断→修复→审核）
- [ ] 修复卡有 parents=诊断卡
- [ ] 审核卡有 parents=修复卡
- [ ] 每张卡注入了对应 skill

## 执行步骤

协调者只记录现象+文件+验收标准，coder/artist 自己分析根因+执行。

| 方式 | 适用场景 |
|------|---------|
| 标准模式 | Gateway、简单 bug → fix 卡 + tester 验证 |
| /goal 模式 | CLI/TUI、复杂 bug → judge + gate-phase8 |
| kanban --goal | Gateway fix 卡 → worker 自动迭代 |

**⛔ /goal 限制：** judge 不能替代 tester（C3）| 不能绕过 gate-phase8 | Phase 1-6 禁用

```bash
python3 scripts/gate-phase8.py <项目目录>
```
