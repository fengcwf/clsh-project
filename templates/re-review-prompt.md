# Scoped Re-Review Prompt

> 修复后的范围审查。只检查 fix 是否解决了 findings，不重新审查整个任务。
> **Superpowers v6.2.0 实证**："New findings on untouched code go to the ledger, not the loop."

---

## 输入

- **原始 findings**: {original_findings}
- **修复 diff**: {fix_diff_summary}
- **修复文件列表**: {fixed_files}

---

## 审查清单

对每个原始 finding：

1. **是否已修复？** — 读 fix diff，确认该 finding 对应的代码变更
2. **修复是否正确？** — 修复本身是否引入新问题
3. **是否有副作用？** — fix diff 中是否有超出 finding 范围的变更

---

## 输出格式

```
Re-Review Verdict: ALL_ADDRESSED / FINDINGS_OPEN

对每个 finding:
- Finding 1: [描述] → ADDRESSED / NOT_ADDRESSED
  证据: [具体代码位置或 diff 行]

新发现（如有，仅限 fix 引入的副作用）:
- [描述] → 记录到 ledger，不进入当前 fix 循环

结论: [一句话总结]
```

---

## 规则

- **禁止审查未修改的文件** — 只看 fix diff
- **禁止提出新 findings** — 新发现记录到 ledger，不进入当前循环
- **禁止扩大审查范围** — 只检查原始 findings 是否解决
