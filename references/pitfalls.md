# Pitfalls (condensed for MiMo Desktop)

Drawn from clsh-project historical pitfalls and Superpowers execution lessons.

## Process compliance

| Pitfall | Rule | Severity |
|---------|------|----------|
| Skip path classification | Always classify spike/bounded/architectural and announce it | Critical |
| Jump straight to code | Approval gate required even for "simple" work | Critical |
| Treat "继续" as design approval | Approval must reference the design content | Critical |
| Downgrade path mid-task | Complexity only ratchets up | High |
| Skip gate script | Mechanical gate, never LLM self-judgment | High |
| Reuse old confirm code | Script prints a fresh code each PASS | Medium |

## Clarification

| Pitfall | Rule | Severity |
|---------|------|----------|
| Batch multiple questions | One question per message | High |
| Abstract questions | Ask specific scenarios ("导入失败时用户看到什么？") | High |
| Absorb scope creep into current spec | Backlog it; keep current goal fixed | High |
| Skip dimension coverage | Cover ≥3 of 功能/异常/性能/安全/兼容 | Medium |

## Design & plan

| Pitfall | Rule | Severity |
|---------|------|----------|
| Placeholder plan steps | Concrete code and commands only | Critical |
| "Similar to Task N" | Repeat the code | High |
| Types/names drift across tasks | Self-review plan consistency | High |
| Plan without interfaces | Later tasks need produced signatures | Medium |

## Execution

| Pitfall | Rule | Severity |
|---------|------|----------|
| Paste full plan into dispatch | Brief file only | High |
| Paste session history into dispatch | Fresh subagent needs task + interfaces only | High |
| Controller implements | Main session coordinates; actor implements | Critical |
| Parallel Phase4 tasks on same files | Never; disjoint file sets or serial | Critical |
| GREEN pipeline without ledger dual-write | Always write ledger after pipeline result | Critical |
| Trust schema green_cmd without tester run | Independent tester must re-run tests | High |
| Hardcode model group that may not exist | Pass modelBase/modelUpgrade; omit upgrade if unknown | High |
| Skip bootstrap then wonder agentType fails | Phase4 check .mimocode/agent/clsh-coder.md | High |
| Skill upgrade without re-bootstrap | Re-run bootstrap_roles.py --force on active projects | Medium |
| Implementer self-review as the gate | Independent reviewer required | Critical |
| Fix loop without cap | Max 3 rounds, then adjudicate + ledger | Critical |
| Ignore ledger after compaction | Read ledger first; do not re-dispatch completed tasks | Critical |
| Fire-and-forget actor | Handle report status; NEEDS_CONTEXT/BLOCKED need response | High |
| Claim fix without evidence | Tests/commands + output in report | Critical |
| Parallel implementers on same files | Never parallel conflicting implementation | High |

## Docs

| Pitfall | Rule | Severity |
|---------|------|----------|
| Artifacts written to cwd instead of vault | All phase outputs under `raw/projects/<project>/changes/<slug>/` | Critical |
| Skip wiki consultation at Phase 0 | Read hot.md + INDEX.md + solutions first | Critical |
| Write/edit wiki outside Phase 6 archive | Daily flow is wiki-read-only | Critical |
| overview.md never updated after archive | Refresh status + change history table | High |
| Write without verifying existence | Read back or list after write | Medium |
| Dual template copies | Single source under skill `templates/` | Medium |
| Gate invoked without change_slug | Correct CLI: project_dir change_slug phase | High |

## LLM behavior

| Pitfall | Rule | Severity |
|---------|------|----------|
| Rationalize an exception | Guard table is a blocker, not a checklist | Critical |
| Cite Guard to confirm skipping | Citing it to skip = rationalizing | Critical |
| Ask user before checking local files/memory | Local first | High |
| Self-judge quality pass | Script + reviewer decide | Critical |
