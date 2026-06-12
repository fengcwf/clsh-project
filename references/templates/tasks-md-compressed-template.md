# tasks.md Compressed Template (≤80 lines)

> Standard format for 16-task projects. Each task = 2 lines (header + pipe-separated details).
> Budget: headers+dep-graph ~8 lines + 16x2=32 lines + self-review 3 lines = ~43 lines.

## Template

```
# {project} Implementation Plan

## Phase 4 Self-Check
- [x] proposal.md + constitution.md written; mechanical check passed; boss confirmed execution

## Dependency Graph
T1->T2||T3||T10; T2->T4->T5; T3->T6->T7->T8->T9; T10->T11->T12->T13->T14->T15->T16

### T1: {title} | role: coder | skills: test-driven-development, incremental-implementation
file: {path} | func: {one-liner} | accept: GIVEN...WHEN...THEN...; GIVEN...WHEN...THEN... | out-of-scope: {one-liner}

### T2: {title} | role: artist | skills: popular-web-designs, frontend-ui-engineering
file: {path} | func: {one-liner} | accept: GIVEN...WHEN...THEN... | out-of-scope: {one-liner}

### T3: {title} | role: tester | skills: code-review-and-quality, systematic-debugging
file: {path} | func: {one-liner} | accept: GIVEN...WHEN...THEN... | out-of-scope: {one-liner}

## Self-Review
- Spec Coverage: PASS (INV-1->T1, INV-2->T2, ...)
- Placeholder Scan: PASS | Type Consistency: PASS | File Isolation: PASS
```

## Role-Skills Mapping
| Role | Skills |
|------|--------|
| coder | test-driven-development, incremental-implementation |
| artist | popular-web-designs, frontend-ui-engineering |
| tester | code-review-and-quality, systematic-debugging |

## Compression Techniques
1. Remove `- ` bullet indentation, write `field: value` directly
2. Merge 4 fields into one line with ` | ` separator
3. Multiple acceptance criteria with `; ACCEPT` (no line break)
4. Task numbers as `T1` not `Task 1`
5. Phase 4 confirmation as single line
6. Self-Review compressed to 2 lines