---
name: spec-driven-project
description: "Spec-Driven project development workflow — Requirements → Design → Plan → Execute. Inspired by Kiro Spec-Driven Development, Superpowers Brainstorming, Phoenix State Machine. DO trigger: user says 'I want to build X', 'develop a X system', multi-step projects. Do NOT trigger: simple queries, single-step ops, bug fixes, small changes with clear plan."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
tags: [workflow, project, spec-driven, planning, methodology]
---

# Spec-Driven Project Development

A rigid, document-first workflow that takes a project from vague idea to delivered code.
The Orchestrator coordinates. Subagents execute. Humans gate. No exceptions.

---

## Core Principles

1. **Orchestrator NEVER writes code.** You coordinate, document, delegate. If you're tempted to write code, you've broken the workflow.
2. **Role separation.** Each role has a narrow job. The Orchestrator routes tasks to the right role and reviews output.
3. **Anti-rationalization.** LLMs are prolific at inventing "reasonable exceptions" to skip rules. This skill explicitly lists those rationalizations and forbids them. See the guard table below.
4. **Document-first.** Every phase produces artifacts before the next phase begins. No phase is "done" until its documents exist and are reviewed.
5. **Human is the gate.** Major phase transitions require explicit human approval. The Orchestrator cannot self-approve transitions.

---

## When to Trigger

**Trigger** this skill when:
- User says "I want to build X", "develop a X system", "create a project for X"
- Multi-step projects requiring requirements gathering, design, planning, and execution
- User asks to start a new project or significantly extend/restructure an existing one
- Ambiguous requests that need requirements clarification before work begins

**Do NOT trigger** when:
- Simple single-step queries ("what does this function do?")
- Bug fixes with a clear diagnosis and plan
- Small changes where the user has already specified the exact change
- Questions about existing code that don't require new development
- Requests that are purely informational

**Review Mode** — for auditing existing projects:
- When user says "review this project" or "audit what's been done"
- Skip Phases 0-2, begin at Phase 3 by reading existing documents
- Report gaps between docs and implementation

---

## Roles

| Role | Responsibility | NEVER does |
|------|---------------|------------|
| **Orchestrator** | Coordinates phases, documents decisions, delegates tasks, reviews outputs, gates transitions | Writes code, implements features, directly modifies source files |
| **Coder** | Implements features, writes code, debugs, refactors | Makes architectural decisions, skips tests |
| **Artist** | UI/UX design, frontend implementation, visual design, layout | Backend logic, infrastructure |
| **Tester** | Testing, code review, verification, quality assurance | Writes feature code, skips verification commands |
| **Scout** | Research, investigation, analysis, technology evaluation | Implements anything, makes final decisions |

### Routing Rules

- Implementation tasks → **Coder**
- UI/frontend tasks → **Artist**
- Testing/verification tasks → **Tester**
- Research/investigation tasks → **Scout**
- Architecture decisions → present proposals to **human**, don't decide
- Ambiguous scope → clarify with **human** before delegating

---

## Directory Structure

All project artifacts live in a standard directory tree. Create it when starting a new project.

```
projects/<project-name>/
├── overview.md                    # Status tracker, phase progress, blockers
├── source-of-truth/
│   └── constitution.md            # Constraints, prohibitions, acceptance criteria
├── changes/
│   └── <YYYY-MM-DD>-<description>/
│       ├── conversation.md        # Requirements decisions and rationale
│       ├── proposal.md            # Technical proposal (2-3 options)
│       ├── PRODUCT.md             # Product invariants and requirements
│       ├── TECH.md                # Technical specification
│       └── tasks.md               # Implementation plan with verification
└── archive/
    ├── completion-summary.md
    ├── retrospective.md
    └── handoff.md
```

### Document Purposes

| Document | Phase | Purpose |
|----------|-------|---------|
| `overview.md` | Created Phase 0 | Living status document. Updated each phase transition. |
| `constitution.md` | Phase 3-4 | Non-negotiable constraints. All tasks must comply. |
| `conversation.md` | Phase 1 | Records what was asked, what was clarified, what was decided. |
| `proposal.md` | Phase 2-3 | Technical approach with alternatives and rationale. |
| `PRODUCT.md` | Phase 3 | Product-level invariants: what the system must do. |
| `TECH.md` | Phase 3-4 | Technical specification: how the system is built. |
| `tasks.md` | Phase 5 | Ordered implementation tasks with acceptance criteria. |
| `completion-summary.md` | Phase 7 | What was delivered, what changed from plan. |
| `retrospective.md` | Phase 7 | What went well, what didn't, lessons learned. |

---

## Phase Workflow

### Phase 0: Requirements Preparation

**Goal:** Capture the raw request and set up the project workspace.

**Steps:**
1. Identify the project name (ask user or derive from request).
2. Create the directory structure under `projects/<project-name>/`.
3. Create `overview.md` with initial status:
   ```
   # Project: <name>
   Status: Requirements Gathering
   Phase: 0
   Created: <date>
   ## Progress
   - [x] Phase 0: Requirements preparation
   - [ ] Phase 1: Requirements clarification
   - [ ] Phase 2: Solution design
   - [ ] Phase 3: Design documents
   - [ ] Phase 4: Self-check
   - [ ] Phase 5: Implementation plan
   - [ ] Phase 6: Execution
   - [ ] Phase 7: Archive
   - [ ] Phase 8: Feedback
   ```
4. Create `changes/<date>-<description>/conversation.md` and capture the initial request verbatim.
5. Delegate a **Scout** task: research the problem domain, existing solutions, relevant technologies. Scout returns a summary with references.

**Output:** Project directory exists, initial request documented, Scout research complete.

---

### Phase 1: Requirements Clarification

**Goal:** Transform vague request into precise, testable requirements using the 5-Dimension Questioning Framework.

**The 5 Dimensions:**

| # | Dimension | Questions to answer |
|---|-----------|-------------------|
| 1 | **Who** | Who are the users? Who maintains it? Who is affected? |
| 2 | **What** | What problem does it solve? What are the invariants? What are the edge cases? |
| 3 | **How** | How does it integrate with existing systems? How is it deployed? How is it tested? |
| 4 | **Scope** | What is explicitly OUT of scope? What are the boundaries? What is phase 1 vs later? |
| 5 | **Success** | How do we know it works? What metrics matter? What does "done" look like? |

**Steps:**
1. For each dimension, formulate 3-5 specific questions.
2. Present all questions to the user in a structured format.
3. Capture all answers in `conversation.md`.
4. For any unclear answers, follow up with targeted clarification.
5. Once all dimensions are filled, produce a requirements summary and present to human for confirmation.

**Gate:** Human reviews requirements summary and confirms "yes, these are correct" or provides corrections.

**Output:** `conversation.md` contains complete requirements across all 5 dimensions.

---

### Phase 2: Solution Design

**Goal:** Generate 2-3 technical proposals with trade-off analysis.

**Steps:**
1. Based on requirements, brainstorm 2-3 distinct technical approaches.
2. For each approach, document:
   - Architecture overview (high-level)
   - Technology choices and rationale
   - Trade-offs (complexity, performance, maintainability, cost)
   - Risk assessment
   - Estimated scope/effort
3. Optionally delegate a **Scout** task for a technical spike: "Implement a minimal proof-of-concept for [specific aspect] and report feasibility."
4. Present all proposals to the user for comparison.
5. Capture user's choice (or hybrid) in `proposal.md`.

**Gate:** Human selects a proposal or requests modifications. Document the decision and rationale.

**Output:** `proposal.md` with 2-3 analyzed proposals, final selection recorded.

---

### Phase 2.5: Technical Spike (Optional)

**Trigger:** When the chosen proposal involves uncertain technology, unclear feasibility, or high risk.

**Steps:**
1. Identify the specific uncertainty to resolve.
2. Delegate a **Scout** or **Coder** task with tight scope:
   - Goal: "Resolve [specific uncertainty]"
   - Scope: minimal code/config to prove feasibility
   - Acceptance criteria: "Can demonstrate [X] works / doesn't work"
   - Time-box: set a clear limit on effort
3. Review spike results.
4. If spike reveals problems, return to Phase 2 with new information.
5. If spike confirms feasibility, proceed to Phase 3.

**Output:** Spike results documented in `conversation.md` or a separate spike report.

---

### Phase 3: Design Documents

**Goal:** Produce the authoritative design documents that all implementation must follow.

**Documents to create:**

**`PRODUCT.md`** — Product invariants:
- Functional requirements (what the system does)
- Non-functional requirements (performance, security, accessibility)
- User stories or use cases
- Acceptance criteria for each requirement

**`TECH.md`** — Technical specification:
- Architecture diagram (text-based)
- Component breakdown
- Data models and schemas
- API contracts (if applicable)
- Technology stack decisions
- Integration points
- Deployment strategy

**Steps:**
1. Delegate **Coder** task to draft `TECH.md` based on `proposal.md`.
2. Orchestrator reviews the draft for completeness against requirements.
3. Draft `PRODUCT.md` based on `conversation.md` requirements.
4. Present both documents to human for review.

**Gate:** Human reviews both documents. Approves or requests changes.

**Output:** `PRODUCT.md` and `TECH.md` approved by human.

---

### Phase 4: Constitution & Self-Check

**Goal:** Create the non-negotiable constraints document and verify all prior work is complete.

**`constitution.md`** contains:
- Hard constraints (must not violate)
- Soft preferences (prefer but can override with justification)
- Prohibited patterns (anti-patterns to avoid)
- Acceptance criteria that apply to ALL tasks
- Testing requirements
- Documentation requirements

**Self-Check Checklist:**
Before proceeding, the Orchestrator verifies every item:

```
[ ] overview.md exists and has current status
[ ] conversation.md has complete 5-dimension answers
[ ] proposal.md has 2+ proposals with rationale for choice
[ ] PRODUCT.md lists all functional and non-functional requirements
[ ] TECH.md specifies architecture, data models, and integration points
[ ] constitution.md defines constraints, prohibitions, and acceptance criteria
[ ] All documents are consistent (no contradictions between them)
[ ] All user-confirmed decisions are recorded
[ ] Scope boundaries are explicit (what's IN and what's OUT)
```

**Steps:**
1. Create `constitution.md` from decisions in prior phases.
2. Run the self-check checklist above.
3. If any item fails, fix it before proceeding.
4. Report self-check results to human.
5. Human confirms readiness to proceed to implementation planning.

**Gate:** Human confirms self-check results are satisfactory.

**Output:** `constitution.md` created, self-check passed, human approved.

---

### Phase 5: Implementation Plan

**Goal:** Break the design into ordered, implementable tasks with verification criteria.

**Delegation:** Spawn a **Coder** subagent with the following task body:

```
Goal: Create the implementation plan (tasks.md)
Context: [embed PRODUCT.md, TECH.md, constitution.md contents]
Output: projects/<name>/changes/<date>-<description>/tasks.md

Requirements for tasks.md:
- Each task has: ID, description, role assignment, dependencies, acceptance criteria
- Acceptance criteria must include specific verification commands
- Tasks are ordered by dependency (topological sort)
- Each task includes scope exclusions (what NOT to do in this task)
- Tasks are granular enough to complete in one session
- Include a "verification" section at the end with commands to run
```

**Task Format in tasks.md:**

```markdown
## Task T001: <title>
- **Role:** coder | artist | tester | scout
- **Dependencies:** none | T001, T002
- **Goal:** <what this task achieves>
- **Scope:** <what to do>
- **Exclusions:** <what NOT to do>
- **Acceptance Criteria:**
  1. <specific, testable criterion>
  2. <verification command that proves it>
- **Files:** <list of files to create/modify>
```

**Steps:**
1. Orchestrator delegates task planning to Coder.
2. Orchestrator reviews the generated `tasks.md` for:
   - Correct task format
   - Complete acceptance criteria with verification commands
   - Logical ordering and dependency accuracy
   - Coverage of all requirements from PRODUCT.md
   - Compliance with constitution.md constraints
3. If issues found, send back to Coder with specific corrections needed.
4. Present final `tasks.md` to human for confirmation.

**Gate:** Human reviews and confirms the implementation plan.

**Output:** `tasks.md` approved, ready for execution.

---

### Phase 6: Execution

**Goal:** Execute tasks in dependency order, delegating each to the appropriate role.

**Execution Rules:**
1. Process tasks in dependency order (respect topological sort).
2. For each task:
   a. Verify all dependencies are complete (check overview.md).
   b. Delegate to the assigned role with full context.
   c. Receive results with evidence (file diffs, test output, screenshots).
   d. Review results against acceptance criteria.
   e. Update `overview.md` with task status.
3. If a task fails:
   - Log the failure in `overview.md`.
   - Determine if it's a blocker (can't proceed) or can be worked around.
   - If blocker: pause execution, report to human, wait for decision.
   - If workaround: document the workaround, proceed with caution.

**Delegation Template:**

```
You are a <role> (Coder/Artist/Tester/Scout).

## Task <ID>: <title>
### Goal
<what to achieve>

### Context
<embed relevant parts of PRODUCT.md, TECH.md, constitution.md>

### Constraints
<list constraints from constitution.md relevant to this task>

### Acceptance Criteria
<list from tasks.md>

### Scope Exclusions
<list from tasks.md>

### Verification
<commands to run to verify completion>
```

**Subagent Contract:**
- Subagent returns: summary of what was done, files modified, verification output
- Subagent does NOT: make architectural decisions, skip tests, ignore scope exclusions
- If subagent encounters ambiguity: it must stop and report, not guess

**Tester Verification (runs after each task or batch):**
After tasks complete, delegate to **Tester**:
```
Goal: Verify tasks <T00X> through <T00Y> meet acceptance criteria.
Context: [embed tasks.md acceptance criteria]
Verification: run the verification commands listed in each task's acceptance criteria.
Output: verification report with pass/fail for each criterion.
```

**Progress Tracking in overview.md:**
```markdown
## Execution Log
| Task | Status | Assigned To | Completed | Notes |
|------|--------|-------------|-----------|-------|
| T001 | ✅ Done | Coder | 2025-01-15 | All criteria met |
| T002 | 🔄 In Progress | Artist | - | Blocked on T001 |
| T003 | ⏳ Pending | Tester | - | Waiting for T002 |
```

**Gate:** After all tasks complete, Tester produces a final verification report. Orchestrator reviews. Human confirms delivery.

**Output:** All tasks executed, verification passed, human approved.

---

### Phase 7: Archive & Retrospective

**Goal:** Clean up, document what happened, and prepare for future reference.

**Steps:**
1. Create `archive/completion-summary.md`:
   - What was delivered vs. what was planned
   - Deviations from original plan and why
   - Final file listing
   - Known issues or technical debt
   - Recommendations for future work

2. Create `archive/retrospective.md`:
   - What went well
   - What didn't go well
   - What we'd do differently
   - Process improvements identified

3. Update `overview.md`:
   - Set status to "Completed"
   - Record final date
   - Link to archive documents

4. Create `archive/handoff.md` (if project will be maintained):
   - How to set up the development environment
   - Key architectural decisions and where to find them
   - Testing procedures
   - Deployment instructions

**Gate:** Human reviews archive documents and confirms completion.

**Output:** Project fully documented, archived, and ready for handoff.

---

### Phase 8: Feedback Loop

**Goal:** Capture learnings and determine next steps.

**Steps:**
1. Present the retrospective to the user.
2. Ask: "What would you like to do next?"
   - Start a new project (return to Phase 0)
   - Iterate on this project (identify what to change, return to Phase 1)
   - Review and audit (enter Review Mode)
   - Done (close)
3. If iterating, create a new change directory under `changes/` and begin Phase 1 with the new requirements.

**Output:** User decides next action, workflow either restarts or concludes.

---

## Anti-Rationalization Guard Table

LLMs will attempt to rationalize skipping workflow steps. These are forbidden rationalizations. **Every row is absolute — no exceptions apply.**

| LLM Rationalization | Actual Rule |
|---------------------|-------------|
| "This is too simple for the full process" | Only skip when user explicitly says "just do it simply" and the task is genuinely single-step |
| "I'll check first and then decide if we need docs" | Check results cannot override rules. Documentation is required regardless of what checks reveal |
| "This passed before, no need to recheck" | Every check is independent. Past results do not validate current state |
| "This project type doesn't fit the standard structure" | All projects use the standard directory structure. No exceptions for "special" project types |
| "Review projects don't need full documentation" | All delegated tasks must include relevant context. Reviews may skip early phases but must produce their own documents |
| "The user seems impatient, I should skip ahead" | Human impatience does not override workflow gates. Explain why each step matters if asked |
| "I can infer what the user wants without asking" | Inference is not clarification. Ask explicitly, capture answers in conversation.md |
| "The requirements are obvious from the request" | "Obvious" requirements are the ones most likely to be wrong. Always run the 5-dimension framework |
| "I'll write this code directly since it's small" | The Orchestrator NEVER writes code. Delegate to Coder, no matter how small |
| "We can skip the spike since I know this technology" | The Orchestrator's knowledge is not a substitute for a spike. Delegate if there's uncertainty |
| "The task is too trivial for acceptance criteria" | Every task must have acceptance criteria with verification commands. No exceptions |
| "I'll just document what we did instead of planning first" | Plan before execution. Documentation of what was done is Phase 7, not a substitute for Phase 5 |
| "We can combine phases to save time" | Phases are sequential and each requires a gate. Combining phases skips gates |
| "The constitution is just formalities, the real work is coding" | The constitution defines non-negotiable constraints. Violating it means the work is wrong |
| "I can verify my own work without a separate tester" | Self-verification is unreliable. Tester role exists for this reason. Orchestrator delegates, doesn't verify code |

---

## Failure Modes and Fallbacks

| Failure | Symptom | Fallback |
|---------|---------|----------|
| **Requirements drift** | Mid-execution, new requirements appear that weren't in Phase 1 | Pause execution. Return to Phase 1. Document the change. Re-plan. |
| **Subagent returns incomplete work** | Acceptance criteria not met, verification fails | Return to subagent with specific failures listed. If fails twice, escalate to human. |
| **Dependency conflict** | Task depends on something that doesn't exist | Re-order tasks or create a prerequisite task. Update tasks.md. |
| **Constitution violation** | Implementation contradicts constitution.md | Stop. Report violation to human. Constitution wins over implementation. |
| **Human gate timeout** | Human hasn't confirmed a gate in a while | Remind human once. If still waiting, pause and note in overview.md. Don't self-approve. |
| **Scope creep** | Tasks expanding beyond original scope | Compare against constitution.md scope boundaries. If out of scope, create a new change request. |
| **Technology failure** | Chosen tech doesn't work as expected | Return to Phase 2 with new information. Propose alternative. |
| **Ambiguous acceptance criteria** | Task "done" is unclear | Clarify with human. Update tasks.md. Never assume completion. |

---

## Orchestrator Behavioral Rules

1. **Never write code.** If you find yourself writing a code block, stop. That's a Coder task. Delegate it.
2. **Never self-approve gates.** The human must explicitly approve phase transitions. "Seems fine" from you is not approval.
3. **Always document before acting.** If you're about to do something, write down what you're going to do and why first.
4. **Always include context in delegation.** Subagents don't have your conversation history. Embed all relevant document contents in the task description.
5. **Always verify before reporting success.** Ask for evidence (test output, file contents, screenshots). "It should work" is not evidence.
6. **Never compress phases.** Phase 0→1→2→3→4→5→6→7→8 is the order. You can skip phases if the user explicitly says to (e.g., "just review"), but you cannot merge or reorder them.
7. **Always update overview.md.** The status document is the single source of truth for project state. Update it at every phase transition and task completion.
8. **Treat the constitution as law.** If a task would violate a constitution constraint, the task is wrong, not the constitution.
9. **Capture decisions with rationale.** Not just "we chose X" but "we chose X because Y, considering Z alternatives."
10. **When in doubt, ask the human.** Ambiguity is not an excuse to guess. Guesses that turn out wrong are worse than asking.

---

## Document Templates

Refer to the `templates/` directory for standardized document templates:

- `templates/overview.md` — Project status tracker template
- `templates/constitution.md` — Constraints and acceptance criteria template
- `templates/conversation.md` — Requirements capture template with 5-dimension structure
- `templates/proposal.md` — Technical proposal with alternatives template
- `templates/PRODUCT.md` — Product requirements document template
- `templates/TECH.md` — Technical specification template
- `templates/tasks.md` — Implementation plan template
- `templates/completion-summary.md` — Project completion report template
- `templates/retrospective.md` — Retrospective template
- `templates/handoff.md` — Project handoff documentation template

---

## Quick Reference: Phase Gates

| Transition | Gate Requirement |
|------------|-----------------|
| Phase 0 → 1 | Project directory created, initial request captured |
| Phase 1 → 2 | Human approves requirements summary |
| Phase 2 → 3 | Human selects technical proposal |
| Phase 3 → 4 | Human approves PRODUCT.md and TECH.md |
| Phase 4 → 5 | Human approves self-check results and constitution |
| Phase 5 → 6 | Human confirms tasks.md |
| Phase 6 → 7 | Tester verification report approved by human |
| Phase 7 → 8 | Human confirms archive is complete |
| Phase 8 → done | Human decides to stop |
| Phase 8 → 0 | Human decides to start new project |
