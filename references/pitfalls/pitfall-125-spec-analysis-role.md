# Pitfall #125: Phase 8 Spec 灵犀做分析

**Added:** 2026-06-09
**Severity:** HIGH (导致多轮修复)

## Rule
Phase 8 bugfix spec 中，灵犀只做记录（现象/文件/验收标准），不做分析（根因/技术方案/设计方向假设）。coder/artist 自己读代码分析。设计方向无明确指令时填"待确认"，脚本拦截后先问大佬。

## Anti-pattern
灵犀收到"卡片背景不对" → 自己假设用浅色主题 → 写 var(--surface-solid) → coder 照做 → 大佬要暗色毛玻璃 → Round 4 重修。

## Correct Pattern
灵犀收到"卡片背景不对" → 记录原文 → 设计方向填"待确认" → 问大佬"要什么风格？" → 大佬确认后更新 spec → 派 coder。

## Reference
- 铁律 #21
- references/phase8-spec-precision-learnings.md
