# clsh-project — 需求驱动项目开发工作流（通用版）

A rigid, document-first workflow that takes a project from vague idea to delivered code. Inspired by [Kiro](https://kiro.dev) Spec-Driven Development, [Superpowers](https://github.com/superpowers) Brainstorming, and [Phoenix](https://phoenixframework.org) State Machine patterns.

**The Orchestrator coordinates. Subagents execute. Humans gate. No exceptions.**

---

## What This Is

A methodology skill for AI assistants that enforces structured project development:

```
Phase 0+1: Requirements → 5-Dimension Questioning Framework
Phase 2:   Solution Design → 2-3 proposals with trade-offs
Phase 3:   Design Documents → PRODUCT.md + TECH.md
Phase 4:   Constitution → Non-negotiable constraints
Phase 5:   Implementation Plan → Ordered tasks with verification
Phase 6:   Execution → Delegated to role-specific subagents
Phase 7:   Archive → Completion + Retrospective
Phase 8:   Feedback Loop → Iterate or close
```

## Core Principles

1. **Orchestrator NEVER writes code** — coordinates, documents, delegates only
2. **Role separation** — Orchestrator, Coder, Artist, Tester, Scout each have narrow responsibilities
3. **Anti-rationalization** — Explicit guard table prevents LLMs from inventing "reasonable exceptions"
4. **Document-first** — Every phase produces artifacts before the next begins
5. **Human is the gate** — Major transitions require explicit human approval

## Quick Start

```bash
# Install the skill into your AI assistant
curl -sSL https://raw.githubusercontent.com/clsh/clsh-project/main/install.sh | bash

# Or clone manually
git clone https://github.com/clsh/clsh-project.git
cp -r clsh-project/SKILL.md ~/.your-assistant/skills/
cp -r clsh-project/templates ~/.your-assistant/skills/
```

Then ask your AI assistant: **"I want to build a [X] system"** — the workflow activates automatically.

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Repository Structure

```
clsh-project/
├── SKILL.md                          # Main workflow definition (~540 lines)
├── README.md                         # This file
├── INSTALL.md                        # Installation guide
├── LICENSE                           # MIT
├── install.sh                        # One-line installer
├── templates/                        # Document templates for each phase
│   ├── conversation-template.md      # Phase 1: Requirements log
│   ├── product-md-template.md        # Phase 1: Product invariants
│   ├── context-template.md           # Phase 1: Domain language table
│   ├── tech-md-template.md           # Phase 2: Technical spec
│   ├── adr-template.md               # Phase 2: Architecture Decision Record
│   ├── constitution-template.md      # Phase 3: Constraints
│   ├── proposal-template.md          # Phase 3: Technical proposal
│   ├── tasks-md-template.md          # Phase 5: Implementation plan
│   ├── phase-confirmations.md        # All phases: Transition confirmations
│   ├── scout-research-goal.md        # Scout delegation template
│   ├── validation-report-template.md # Phase 6: Tester verification
│   ├── phase6-dispatch-template.md   # Phase 6: Task dispatch checklist
│   ├── completion-summary-template.md# Phase 7: Archive
│   ├── retrospective-template.md     # Phase 7: Retrospective
│   └── handoff-template.md           # Phase 7: Handoff
├── references/
│   ├── pitfalls/common.md            # 50 hard-won pitfalls with fixes
│   ├── workflow/
│   │   ├── overview.md               # Flow diagram + phase transition rules
│   │   └── phase-review.md           # Review mode detailed process
│   └── anti-rationalization-patterns.md # Why LLMs skip rules + prevention
└── scripts/
    └── setup.sh                      # Project directory setup
```

## How It Works

### Roles

| Role | Does | Never Does |
|------|------|------------|
| **Orchestrator** | Coordinates, documents, delegates, reviews output | Writes code, implements features |
| **Coder** | Implements, debugs, refactors | Architectural decisions, skipping tests |
| **Artist** | UI/UX, frontend, visual design | Backend, infrastructure |
| **Tester** | Testing, code review, verification | Feature code |
| **Scout** | Research, investigation, analysis | Implementation, decisions |

### Phase Gates

Every phase transition has a gate:

| Transition | Gate |
|-----------|------|
| 0 → 1 | Project directory created |
| 1 → 2 | Human approves requirements |
| 2 → 3 | Human selects proposal |
| 3 → 4 | Human approves design docs |
| 4 → 5 | Human approves constitution |
| 5 → 6 | Human confirms task plan |
| 6 → 7 | Tester verification passed |
| 7 → 8 | Human confirms archive |
| 8 → done | Human decides to stop |

### Anti-Rationalization

The skill includes a guard table of 15 forbidden LLM rationalizations. Examples:

| LLM Says | Actually |
|----------|----------|
| "Too simple for the process" | Only skip when user explicitly says so |
| "I'll check first then decide" | Checks cannot override rules |
| "Passed before, no need to recheck" | Every check is independent |
| "I can verify my own work" | Self-verification is unreliable |

## Who Is This For?

- **Solo developers** who want structured AI-assisted project development
- **Teams** using AI assistants for code generation who need quality gates
- **Anyone** who's been burned by LLMs skipping steps and producing unreliable code

## Philosophy

> Plausibility is not correctness. Code that looks right isn't verified until proven.

This workflow exists because LLMs are excellent at producing plausible-looking output that's subtly wrong. The rigid pipeline, role separation, and human gates catch what LLM self-review misses.

## License

MIT — Use it, fork it, adapt it. Attribution appreciated but not required.

## Credits

- [Kiro](https://kiro.dev) — Spec-Driven Development concept
- [Superpowers](https://github.com/superpowers) — Brainstorming methodology and two-stage review
- [Phoenix Framework](https://phoenixframework.org) — State machine execution pattern
- [Ralph Loop](https://github.com) — Orchestrator/single-step executor separation
