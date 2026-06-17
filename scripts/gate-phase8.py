#!/usr/bin/env python3
"""
gate-phase8.py - Phase 8 Quality Gate

Validates that bugfix artifacts exist: conversation log, diagnosis,
and specification. This gate runs after the bugfix/fix phase.

Checks performed:
  1. Bugfix conversation file must exist
  2. Diagnosis document must exist with root cause analysis
  3. Bugfix spec must exist with fix plan and acceptance criteria
  4. No placeholder content in bugfix documents
  5. Minimum content requirements met

Usage:
    python gate-phase8.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

GATE_NAME = "phase8"

# Required bugfix artifacts and their validation patterns
BUGFIX_ARTIFACTS = {
    "conversation": {
        "filenames": [
            "bugfix-conversation.md",
            "fix-conversation.md",
            "conversation.md",
            "bugfix-log.md",
        ],
        "required_patterns": [
            r"(?:bug|issue|error|defect|fix|problem)",
        ],
        "description": "Bugfix conversation log",
    },
    "diagnosis": {
        "filenames": [
            "diagnosis.md",
            "root-cause.md",
            "bugfix-diagnosis.md",
            "analysis.md",
        ],
        "required_patterns": [
            r"(?:root\s+cause|diagnosis|analysis|cause|origin)",
        ],
        "description": "Bug diagnosis / root cause analysis",
    },
    "spec": {
        "filenames": [
            "bugfix-spec.md",
            "fix-spec.md",
            "bugfix-specification.md",
            "fix-plan.md",
        ],
        "required_patterns": [
            r"(?:fix|solution|patch|remediation|approach)",
        ],
        "description": "Bugfix specification / fix plan",
    },
}

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bTBD\b",
    r"<placeholder>",
    r"<fill in>",
    r"<add here>",
]

MIN_NONBLANK_LINES = 8


def check_bugfix_artifact(project_dir: str, artifact_key: str,
                          artifact_config: dict) -> list[str]:
    """Check a single bugfix artifact.

    Returns a list of error strings (empty = pass).
    """
    errors = []
    desc = artifact_config["description"]
    filenames = artifact_config["filenames"]

    # --- File existence ---
    filepath = gu.find_file_in_changes(project_dir, filenames)
    if filepath is None:
        errors.append(
            f"Missing {desc}. Looked for: {', '.join(filenames)}"
        )
        return errors

    content = filepath.read_text(encoding="utf-8", errors="replace")

    # --- Line count ---
    lines = [l for l in content.splitlines() if l.strip()]
    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(
            f"{filepath.name}: too short ({len(lines)} non-blank lines, "
            f"minimum {MIN_NONBLANK_LINES})"
        )

    # --- Content relevance ---
    content_lower = content.lower()
    patterns = artifact_config["required_patterns"]
    has_content = any(re.search(p, content_lower) for p in patterns)
    if not has_content:
        errors.append(
            f"{filepath.name}: missing expected content "
            f"({desc} should contain relevant keywords)"
        )

    # --- Placeholder check ---
    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, content)
        if match:
            errors.append(f"{filepath.name}: placeholder found: '{match.group()}'")

    return errors


def run_gate(project_dir: str) -> None:
    """Run the Phase 8 gate checks."""
    errors = []

    for artifact_key, artifact_config in BUGFIX_ARTIFACTS.items():
        errors.extend(
            check_bugfix_artifact(project_dir, artifact_key, artifact_config)
        )

    if not errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_marker(GATE_NAME, project_dir, code,
                        {"checked": list(BUGFIX_ARTIFACTS.keys())})
        gu.output_result(GATE_NAME, True, code=code)
    else:
        gu.output_result(GATE_NAME, False, errors=errors)


def main():
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase8.py <project_dir>"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    run_gate(project_dir)


if __name__ == "__main__":
    main()
