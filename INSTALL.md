# Installation Guide

This skill works with any AI assistant that supports custom skills/prompts and subagent delegation. Choose your platform below.

---

## Prerequisites

- An AI assistant that supports:
  - Custom skill/prompt loading
  - Subagent/task delegation (spawning specialized workers)
  - File system access (reading/writing project documents)
  - Multi-turn conversation with context persistence

---

## Platform-Specific Installation

### Generic / Any Platform

1. Clone the repository:
   ```bash
   git clone https://github.com/clsh/spec-driven-project.git
   cd spec-driven-project
   ```

2. Copy `SKILL.md` to your assistant's skill/prompt directory.

3. Copy the `templates/` directory alongside the skill.

4. Copy the `references/` directory alongside the skill (optional but recommended).

5. Start a conversation and say: *"I want to build a [X] system"*

### File Layout After Installation

```
your-assistant-skills/
└── spec-driven-project/
    ├── SKILL.md              # Main workflow (required)
    ├── templates/            # Document templates (required)
    │   ├── conversation-template.md
    │   ├── product-md-template.md
    │   ├── context-template.md
    │   ├── tech-md-template.md
    │   ├── adr-template.md
    │   ├── constitution-template.md
    │   ├── proposal-template.md
    │   ├── tasks-md-template.md
    │   ├── phase-confirmations.md
    │   ├── scout-research-goal.md
    │   ├── validation-report-template.md
    │   ├── phase6-dispatch-template.md
    │   ├── completion-summary-template.md
    │   ├── retrospective-template.md
    │   └── handoff-template.md
    └── references/           # Pitfalls, workflow docs (optional)
        ├── pitfalls/common.md
        ├── workflow/overview.md
        ├── workflow/phase-review.md
        └── anti-rationalization-patterns.md
```

---

## Verification

After installation, verify by asking your assistant:

> "I want to build a simple todo app"

The assistant should:
1. ✅ Set up a project directory structure
2. ✅ Ask you questions using the 5-Dimension framework
3. ✅ NOT immediately start writing code
4. ✅ Document your requirements before proceeding

If the assistant immediately starts coding, the skill isn't loaded correctly.

---

## Usage Tips

### Starting a New Project
Just describe what you want to build. The workflow activates automatically for multi-step projects.

### Continuing a Project
Reference the project name: *"Continue working on the todo-app project"*

### Reviewing an Existing Project
Say: *"Review the todo-app project"* — enters Review Mode (skips early phases).

### Skipping the Workflow
If you genuinely want something simple, say: *"Just do it simply"* — this bypasses the workflow for single-step tasks.

---

## Customization

### Adjusting Phase Rigidity
Edit `SKILL.md` phase gates. For example, to make Phase 2.5 optional, remove its trigger condition.

### Adding Custom Templates
Add `.md` files to `templates/` and reference them in `SKILL.md`.

### Modifying Roles
Edit the Roles table in `SKILL.md` to add project-specific roles.

### Changing Directory Structure
Edit the Directory Structure section in `SKILL.md`. Run `bash scripts/setup.sh` to validate.

---

## Uninstallation

Delete the skill directory:
```bash
rm -rf your-assistant-skills/spec-driven-project
```

Project directories created under `projects/` are independent and should be managed separately.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Assistant ignores the workflow | Ensure SKILL.md is in the active skill/prompt directory |
| Templates not found | Verify `templates/` is alongside SKILL.md |
| Assistant writes code directly | Check the Anti-Rationalization Guard table is loaded |
| Phases are being skipped | Review the Orchestrator Behavioral Rules section |

---

## What Gets Installed

| Component | Size | Required |
|-----------|------|----------|
| SKILL.md | ~24KB | ✅ Yes |
| templates/ (15 files) | ~12KB | ✅ Yes |
| references/ (4 files) | ~38KB | ⚡ Recommended |
| scripts/ | ~3KB | ❌ Optional |

Total: ~77KB. No runtime dependencies, no external services, no API keys.
