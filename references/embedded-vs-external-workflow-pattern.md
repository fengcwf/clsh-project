# Embedded vs External Workflow Steps — Architectural Pattern

> Established: 2026-06-10 | From: skill injection review session

## Core Insight

**Critical workflow steps must be embedded in SKILL.md, not referenced as external files.**

External file references (`📋 详细流程: /path/to/file.md`) are **information annotations**, not **execution instructions**. LLMs treat them as "reference material available" rather than "must read this file before proceeding." This causes steps to be skipped.

## The Pattern

### Phase 1-4: Embedded (No External File Dependency)

Phase 1-4 summaries in SKILL.md contain enough information for 灵犀 to execute without reading external files. External files exist for detail but are optional.

**Result:** Steps are never skipped. Process is reliable.

### Phase 5-6: External (File-Dependent)

Phase 5-6 originally referenced external templates/workflows for critical information (skill injection mapping, dispatch checklist). 灵犀 would sometimes skip reading these files.

**Result:** Steps were skipped. 98% of kanban tasks had no skill injection (1.9% usage rate).

## The Fix

**Embed the minimum viable information directly in SKILL.md. Keep external files for detail.**

| Information Type | Where It Goes | Example |
|-----------------|---------------|---------|
| Skill injection mapping | SKILL.md (embedded) | `coder → test-driven-development, systematic-debugging` |
| Dispatch checklist | SKILL.md (embedded) | Phase 6 checklist with ⛔ marks |
| Task format with skills field | SKILL.md (embedded) | `### Task N: 标题 | 角色：coder | skills: ...` |
| Detailed dispatch workflow | External file (optional read) | `phase6-execution.md` (617 lines) |
| Wave strategy, Browser QA | External file (optional read) | `phase6-execution.md` |

## Confirmation Code Gates: Output vs Process

**Confirmation code gates check Phase OUTPUT, not execution PROCESS.**

```
Phase 5: coder writes tasks.md → 灵犀 reviews → [confirmation code]
                                                    ↑ Gate is HERE
Phase 6: 灵犀 dispatches tasks → workers execute → tester verifies → [confirmation code]
                                                                      ↑ Gate is HERE
```

灵犀 can skip reading templates → dispatch cards → produce output → generate code → gate passes. Output exists, but process was incomplete.

**Phase 1-4 don't have this problem** because critical info is embedded in SKILL.md summary.

**Phase 5-6 fix:** Embed checklist + mapping directly. The checklist IS the process enforcement.

## Template Single-Copy Rule

**Templates exist only in raw/ Vault. Skill-local does not store copies.**

Reason: Dual copies (raw/ + skill-local/) caused sync issues. Single copy + absolute paths eliminates this.

SKILL.md references templates via absolute paths. 灵犀 uses `read_file()` on demand for optional detail.

## Anti-Pattern: "Just Make LLM Read the File"

```
❌ "Add a ⛔ instruction to read the external file"
   → Still depends on LLM following the instruction
   → Still has execution cost (extra tool call + tokens)

✅ "Embed the critical 10 lines directly in SKILL.md"
   → Zero extra steps
   → Always visible when skill is loaded
```

## When to Use External Files

| Use External When | Embed When |
|-------------------|------------|
| Detail is optional (reference material) | Step is critical (must not be skipped) |
| Content is >50 lines | Content is <20 lines |
| Content changes frequently | Content is stable |
| Multiple skills reference same file | Content is specific to this skill |

## Harness Comparison

[revfactory/harness](https://github.com/revfactory/harness) (Claude Code meta-skill) solves this differently:

- Agent definition files (`.claude/agents/builder.md`) embed skill references
- When agent is invoked, skills auto-load (framework-guaranteed)
- Progressive Disclosure: 100 words metadata → <500 lines SKILL.md → unlimited references

clsh-project uses orchestrator-driven injection (more flexible, same role can get different skills per task). The embedded checklist compensates for the lack of framework-level guarantee.
