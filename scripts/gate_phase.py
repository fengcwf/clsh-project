#!/usr/bin/env python3
"""Mechanical phase gate for clsh-project-mimo (Obsidian vault layout).

Usage:
  python gate_phase.py <project_dir> <change_slug> <phase> [--code-project PATH]

  project_dir   : \\192.168.0.123\\data\\Obsidian\\raw\\projects\\<project>
  change_slug   : e.g. 2026-09-09-notes-sync
  phase         : 0..6
  --code-project: optional code repo (Phase 4/5 checks pipeline-result + role agents)

Phases:
  0 research   — phase0-data.json + overview + >=10 questions + exploration evidence
  1 clarify    — changes/<slug>/conversation.md + research/scout evidence
  2 design     — changes/<slug>/proposal.md (approaches + goals + test)
  3 plan       — changes/<slug>/tasks.md (concrete, no placeholders)
  4 execute    — ledger + (optional) code proj agents + pipeline GREEN/NEEDS_HUMAN
  5 verify     — ledger complete/ruling + pipeline results not silent-fail
  6 archive    — changes/archive/<slug>/completion-summary.md

Exit 0 = PASS (prints confirm code), 1 = BLOCKED.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

MIN_BODY_LINES = 5
CHANGE_DIR = "changes"
ARCHIVE_DIR = "changes/archive"

REQUIRED_FILENAMES = {
    0: ["overview.md"],
    1: ["conversation.md"],
    2: ["proposal.md"],
    3: ["tasks.md"],
    4: ["ledger.md"],
    5: ["ledger.md"],
    6: ["completion-summary.md"],
}

CONTENT_PATTERNS = {
    0: {
        "overview.md": [
            r"概述|overview|purpose|goal|目标",
            r"status|状态",
            r"open.?question|待确认|开放问题|constraint|约束",
        ],
    },
    1: {
        "conversation.md": [
            r"requirement|需求|用户|question|问题|？|\?",
            r"确认|approve|enough|足够|确认进入",
        ],
    },
    2: {
        "proposal.md": [
            r"goal|目的|目标|概述",
            r"方案|approach|architecture|架构",
            r"非目标|non-?goal|不在范围|out of scope|范围外",
            r"test|测试|验证|风险",
        ],
    },
    3: {
        "tasks.md": [
            r"Task\s*\d+|任务\s*\d+",
            r"files?|文件|Create:|Modify:|测试|Test:",
            r"- \[ \]",
        ],
    },
    4: {
        "ledger.md": [r"Task|任务|plan|phase3|tasks\.md"],
    },
    5: {
        "ledger.md": [r"complete|完成|Ruling|裁决|parked|deferred"],
    },
    6: {
        "completion-summary.md": [
            r"summary|摘要|总结|shipped|交付|完成",
            r"retrospective|复盘|回顾|遗留|open item|下一步",
        ],
    },
}

PHASE1_EXTRA = {
    "min_substantive": 3,
    "fake_confirm": re.compile(r"^(继续|好的|没问题|ok|okay)\s*$", re.I),
}

PLACEHOLDER_RE = re.compile(
    r"\bTBD\b|\bTODO\b|similar to Task|handle edge cases\s*$|适当处理|待补充|待完善",
    re.I | re.M,
)


def fail(msg: str) -> None:
    print(f"BLOCKED: {msg}")


def ok(phase: int, project_dir: Path, change: str, checked: list[str]) -> None:
    raw = f"{phase}|{project_dir}|{change}|{'|'.join(checked)}"
    code = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]
    print(f"PASS phase={phase} change={change} confirm_code={code}")
    print(f"  checked: {', '.join(checked)}")
    state_path = project_dir / CHANGE_DIR / change / "gate-state.json"
    if phase == 6:
        state_path = project_dir / ARCHIVE_DIR / change / "gate-state.json"
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {}
        if state_path.is_file():
            payload = json.loads(state_path.read_text(encoding="utf-8"))
        payload[str(phase)] = {
            "change": change,
            "checked": checked,
            "confirm_code": code,
        }
        state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  state: {state_path}")
    except OSError as exc:
        print(f"  warn: could not write gate-state ({exc})")


def body_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if lines and lines[0].strip() == "---":
        rest: list[str] = []
        in_fm = True
        for ln in lines[1:]:
            if in_fm and ln.strip() == "---":
                in_fm = False
                continue
            if not in_fm:
                rest.append(ln)
        lines = rest or lines
    return lines


def check_phase1_conversation(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    questions = [ln for ln in text.splitlines() if "?" in ln or "？" in ln or re.search(r"Q\d|问题\s*\d", ln)]
    if len(questions) < 3:
        errors.append(f"phase1 needs >=3 questions (found {len(questions)})")
    answers = [
        ln
        for ln in text.splitlines()
        if ln.strip()
        and not ln.strip().startswith(("#", "-", "|", ">"))
        and len(ln.strip()) >= 12
        and not PHASE1_EXTRA["fake_confirm"].match(ln.strip())
    ]
    if len(answers) < PHASE1_EXTRA["min_substantive"]:
        errors.append(
            f"phase1 needs >={PHASE1_EXTRA['min_substantive']} substantive answer lines (found {len(answers)})"
        )
    return errors


def check_phase0_open_questions(project_dir: Path) -> list[str]:
    errors: list[str] = []
    candidates = [
        project_dir / "overview.md",
        project_dir / CHANGE_DIR / "phase0-research.md",
    ]
    changes = project_dir / CHANGE_DIR
    if changes.is_dir():
        for d in sorted(changes.iterdir()):
            if d.is_dir() and not d.name.startswith("archive"):
                candidates.append(d / "phase0-research.md")
    blob = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in candidates if p.is_file()
    )
    if not re.search(r"open.?question|待确认|开放问题|constraint|约束", blob, re.I):
        errors.append(
            "phase0 needs open questions/constraints in overview.md or a phase0-research.md"
        )
    # >= 10 numbered structured questions across >= 3 dims (clsh IL-NEW)
    numbered = re.findall(
        r"(?:^|\n)\s*(?:[-*]\s*)?(\d+)[.)、]\s*(?:\[([^\]]+)\])?\s*([^\n]{8,})",
        blob,
    )
    if len(numbered) < 10:
        errors.append(
            f"phase0 needs >=10 numbered structured questions (found {len(numbered)}) "
            f"format: '1. [功能] ...?'"
        )
    dims = {m for m in re.findall(r"\[(功能|技术|边界|约束|异常|性能|安全|调研)\]", blob)}
    if len(dims) < 3:
        errors.append(
            f"phase0 questions must cover >=3 dims among 功能/技术/边界/约束/异常/安全 (found {sorted(dims) or 'none'})"
        )
    return errors


def check_phase0_scan_json(project_dir: Path) -> list[str]:
    """IL-4: mechanical scan must exist before Phase 1."""
    errors: list[str] = []
    scan = project_dir / "phase0-data.json"
    changes = project_dir / CHANGE_DIR
    alt = []
    if changes.is_dir():
        for d in sorted(changes.iterdir()):
            if d.is_dir() and not d.name.startswith("archive"):
                alt.append(d / "phase0-data.json")
    path = scan if scan.is_file() else next((p for p in alt if p.is_file()), None)
    if path is None:
        errors.append(
            "missing phase0-data.json — run scripts/phase0_scan.py <project_dir> first (IL-4)"
        )
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"phase0-data.json invalid JSON: {exc}")
        return errors
    for key in ("project_dir", "tech_stack", "seed_open_questions"):
        if key not in data:
            errors.append(f"phase0-data.json missing key: {key}")
    return errors


def check_phase0_cites_scan(project_dir: Path) -> list[str]:
    """IL-6: research must reference the scan JSON — anti-hallucination."""
    errors: list[str] = []
    candidates = [project_dir / "overview.md"]
    changes = project_dir / CHANGE_DIR
    if changes.is_dir():
        for d in sorted(changes.iterdir()):
            if d.is_dir() and not d.name.startswith("archive"):
                candidates.append(d / "phase0-research.md")
                candidates.append(d / "research-evidence.md")
    blob = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in candidates if p.is_file()
    )
    if not blob.strip():
        return ["phase0: no overview/research file to check scan citation"]
    if not re.search(r"phase0-data\.json|tech_stack|seed_open_questions", blob, re.I):
        errors.append(
            "phase0 research/overview must cite phase0-data.json (tech_stack / structure) — do not invent stack"
        )
    return errors


def check_exploration_evidence(path: Path, min_refs: int = 2) -> list[str]:
    """Phase 0/1: external/wiki research evidence required (clsh IL-7 spirit)."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    has_header = re.search(r"探索证据|Exploration Evidence|调研记录|Scout", text, re.I)
    urls = re.findall(r"https?://\S+", text)
    wiki_refs = re.findall(r"wiki/[\w./-]+|raw/projects/[\w./-]+|INDEX\.md|hot\.md|solutions/", text)
    tools = re.findall(r"websearch|webfetch|browser|playwright|actor explore|scout", text, re.I)
    if not has_header:
        errors.append(
            f"{path.name}: missing '## 探索证据' / Exploration Evidence section (IL-7)"
        )
    if len(urls) + len(wiki_refs) < min_refs and not tools:
        errors.append(
            f"{path.name}: needs >= {min_refs} source refs (URL or wiki path) or explicit tool trail "
            f"(found urls={len(urls)} wiki={len(wiki_refs)})"
        )
    return errors


def _read_json(path: Path):
    """Read JSON tolerating UTF-8 BOM (PowerShell Set-Content -Encoding utf8)."""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return json.loads(text)


def check_code_project_phase4(code_proj: Path, change_dir: Path) -> list[str]:
    """P0/P1: role agents installed + pipeline results not silently broken."""
    errors: list[str] = []
    if not code_proj.is_dir():
        return [f"code project not found: {code_proj}"]

    coder_agent = code_proj / ".mimocode" / "agent" / "clsh-coder.md"
    if not coder_agent.is_file():
        errors.append(
            f"missing {coder_agent} — run scripts/bootstrap_roles.py {code_proj} "
            f"or degrade to agentType=general with role contract in prompt"
        )

    report_dir = code_proj / ".clsh" / "reports"
    if not report_dir.is_dir():
        # not fatal before first task, but note for execute progress
        return errors

    results = sorted(report_dir.glob("task-*-pipeline-result.json"))
    ledger = change_dir / "ledger.md"
    ledger_text = ledger.read_text(encoding="utf-8", errors="replace") if ledger.is_file() else ""

    for rp in results:
        try:
            data = _read_json(rp)
        except json.JSONDecodeError as exc:
            errors.append(f"{rp.name}: invalid JSON ({exc})")
            continue
        status = str(data.get("status", ""))
        task_n = data.get("taskN", rp.stem)
        if status not in {"GREEN", "NEEDS_HUMAN"}:
            errors.append(f"{rp.name}: illegal status {status!r} (want GREEN|NEEDS_HUMAN)")
        if status == "NEEDS_HUMAN":
            # must be recorded in ledger so it is not silently forgotten
            n = re.escape(str(task_n))
            if not re.search(
                rf"NEEDS_HUMAN|Task\s*{n}\s*:\s*(blocked|NEEDS_HUMAN)",
                ledger_text,
                re.I,
            ):
                errors.append(
                    f"{rp.name}: NEEDS_HUMAN not reflected in ledger.md — dual-write required"
                )
        if status == "GREEN":
            # if ledger claims this task complete, fine; if ledger has open findings only, warn via error
            if re.search(rf"Task\s*{re.escape(str(task_n))}\s*:\s*blocked", ledger_text, re.I):
                errors.append(f"{rp.name}: GREEN but ledger marks Task {task_n} blocked")
    return errors


def check_code_project_phase5(code_proj: Path) -> list[str]:
    errors: list[str] = []
    if not code_proj.is_dir():
        return [f"code project not found: {code_proj}"]
    report_dir = code_proj / ".clsh" / "reports"
    if not report_dir.is_dir():
        return ["missing .clsh/reports — no pipeline evidence for Phase 5"]
    results = list(report_dir.glob("task-*-pipeline-result.json"))
    if not results:
        errors.append("Phase 5: no task-*-pipeline-result.json found (execute evidence missing)")
        return errors
    bad = []
    for rp in results:
        try:
            data = _read_json(rp)
        except json.JSONDecodeError:
            bad.append(rp.name)
            continue
        if data.get("status") != "GREEN":
            bad.append(f"{rp.name}={data.get('status')}")
    if bad:
        errors.append(
            "Phase 5 requires all pipeline results GREEN before whole-branch review; "
            f"non-green: {', '.join(bad)}"
        )
    return errors


def resolve_change_dir(project_dir: Path, change: str, phase: int) -> Path:
    if phase == 6:
        return project_dir / ARCHIVE_DIR / change
    return project_dir / CHANGE_DIR / change


def main() -> int:
    argv = sys.argv[1:]
    code_proj: Path | None = None
    if "--code-project" in argv:
        i = argv.index("--code-project")
        if i + 1 >= len(argv):
            fail("--code-project requires a path")
            return 2
        code_proj = Path(argv[i + 1]).expanduser().resolve()
        argv = argv[:i] + argv[i + 2 :]
    if len(argv) != 3:
        print(__doc__.strip())
        return 2

    project_dir = Path(argv[0]).expanduser().resolve()
    change = argv[1].strip()
    phase_raw = argv[2]

    try:
        phase = int(phase_raw)
    except ValueError:
        fail(f"phase must be 0-6, got {phase_raw!r}")
        return 1

    if phase not in REQUIRED_FILENAMES:
        fail(f"unknown phase {phase} (valid: 0-6)")
        return 1

    if not project_dir.is_dir():
        fail(f"project dir not found: {project_dir}")
        return 1

    # Phase 0 may run before a formal change dir exists
    if phase == 0:
        checked: list[str] = []
        errors: list[str] = []
        overview = project_dir / "overview.md"
        if not overview.is_file():
            errors.append("missing raw/projects/<project>/overview.md")
        else:
            lines = body_lines(overview)
            if len(lines) < MIN_BODY_LINES:
                errors.append(f"overview.md too short ({len(lines)} lines, need >= {MIN_BODY_LINES})")
            else:
                blob = overview.read_text(encoding="utf-8", errors="replace")
                for pat in CONTENT_PATTERNS[0]["overview.md"]:
                    if not re.search(pat, blob, re.I | re.M):
                        errors.append(f"overview.md missing /{pat}/")
                checked.append("overview.md")
            errors.extend(check_phase0_open_questions(project_dir))
            errors.extend(check_phase0_scan_json(project_dir))
            errors.extend(check_phase0_cites_scan(project_dir))
            # exploration evidence: prefer research-evidence.md in change dirs
            ev_candidates: list[Path] = []
            changes = project_dir / CHANGE_DIR
            if changes.is_dir():
                for d in sorted(changes.iterdir()):
                    if d.is_dir() and not d.name.startswith("archive"):
                        ev_candidates.extend(
                            [d / "research-evidence.md", d / "scout-report.md", d / "phase0-research.md"]
                        )
            # fallback: change/phase0-research.md or a section inside overview
            ev_candidates.append(project_dir / CHANGE_DIR / "phase0-research.md")
            ev = next((p for p in ev_candidates if p.is_file()), None)
            if ev is not None:
                errors.extend(check_exploration_evidence(ev, min_refs=2))
            else:
                # last resort: overview may embed the evidence section
                errors.extend(check_exploration_evidence(overview, min_refs=2))
        if errors:
            for e in errors:
                fail(e)
            return 1
        ok(phase, project_dir, change or "-", checked)
        return 0

    change_dir = resolve_change_dir(project_dir, change, phase)
    if not change_dir.is_dir():
        fail(
            f"missing change dir: {change_dir}\n"
            f"  expected under {project_dir / CHANGE_DIR}"
        )
        return 1

    checked = []
    errors = []

    for fname in REQUIRED_FILENAMES[phase]:
        path = change_dir / fname
        if not path.is_file():
            rel = path.relative_to(project_dir) if path.is_relative_to(project_dir) else path
            errors.append(f"missing file: {rel}")
            continue
        lines = body_lines(path)
        if len(lines) < MIN_BODY_LINES:
            errors.append(f"{fname}: too short ({len(lines)} non-empty lines, need >= {MIN_BODY_LINES})")
            continue
        blob = path.read_text(encoding="utf-8", errors="replace")
        for pat in CONTENT_PATTERNS[phase].get(fname, []):
            if not re.search(pat, blob, re.I | re.M):
                errors.append(f"{fname}: missing required content matching /{pat}/")
        checked.append(fname)

    if phase == 1:
        path = change_dir / "conversation.md"
        if path.is_file():
            errors.extend(check_phase1_conversation(path))
        # Scout / exploration: required if any [技术]/[调研] question OR always evidence trail
        scout_files = [
            change_dir / "research-evidence.md",
            change_dir / "scout-report.md",
            change_dir / "phase0-research.md",
        ]
        scout = next((p for p in scout_files if p.is_file()), None)
        if scout is not None:
            errors.extend(check_exploration_evidence(scout, min_refs=1))
        else:
            errors.append(
                "phase1 needs research-evidence.md or scout-report.md (websearch/webfetch/browser trail) — IL-7"
            )

    if phase == 3:
        path = change_dir / "tasks.md"
        if path.is_file():
            for m in PLACEHOLDER_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
                errors.append(f"tasks.md contains placeholder: {m.group(0)!r}")

    if phase == 4:
        path = change_dir / "ledger.md"
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            if "tasks.md" not in text and "plan" not in text.lower() and "phase3" not in text:
                errors.append("ledger.md should name the plan/tasks.md path on the first lines")
        if code_proj is not None:
            errors.extend(check_code_project_phase4(code_proj, change_dir))
            if not errors:
                checked.append("pipeline+agents")

    if phase == 5 and code_proj is not None:
        errors.extend(check_code_project_phase5(code_proj))
        if not any("Phase 5 requires" in e or "missing" in e for e in errors):
            checked.append("pipeline-results")

    if errors:
        for e in errors:
            fail(e)
        return 1

    ok(phase, project_dir, change, checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
