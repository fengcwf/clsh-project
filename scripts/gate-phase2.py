#!/usr/bin/env python3
"""
gate-phase2.py - Phase 2 Quality Gate

Validates that TECH.md exists and contains meaningful technical design content.
This gate runs after Phase 2 (方案设计与技术验证).

Required files:
  - TECH.md : technical design document

Checks performed:
  1. TECH.md must exist (in changes/*/ or project root)
  2. TECH.md must have >= 10 non-blank lines
  3. TECH.md must contain architecture/design keywords
  4. TECH.md must contain at least 2 approach/option keywords (2-3 方案)
  5. UI 类项目（PRODUCT.md 命中 UI 关键词，无 .cp-visual-skip）:
     DESIGN.md（>=10 行 + 色彩/字体/间距 token）+ visual/final 定稿图必须存在

Usage:
    python gate-phase2.py <project_dir>

Output: JSON to stdout, exit 0 on PASS, 1 on FAIL.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_utils as gu

REQUIRED_DOCS = {
    "TECH.md": [
        r"(?:architecture|design|stack|component|implementation|架构|技术选型|方案)",
        r"(?:option|alternative|trade.?off|方案[ABCD]|备选|权衡|对比)",
    ],
}

MIN_NONBLANK_LINES = 10
GATE_NAME = "phase2"

# --- Phase 2.5 视觉 Spike checks (UI 类项目, v9.5) ---
UI_TRIGGER_PATTERN = r"(?:仪表盘|Dashboard|Gridstack|前端页面|界面|Tab|页面|UI)"
VISUAL_SKIP_MARKER = ".cp-visual-skip"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def check_document(project_dir: str, filename: str,
                   keyword_patterns: list[str]) -> list[str]:
    """Check a single document. Returns list of error strings (empty = pass)."""
    errors = []
    fpath = gu.find_file_in_changes(project_dir, [filename])
    if fpath is None:
        errors.append(f"{filename}: NOT FOUND")
        return errors

    text = fpath.read_text(encoding="utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < MIN_NONBLANK_LINES:
        errors.append(f"{filename}: only {len(lines)} non-blank lines "
                      f"(need >= {MIN_NONBLANK_LINES})")

    for pat in keyword_patterns:
        if not re.search(pat, text, re.IGNORECASE):
            errors.append(f"{filename}: missing keyword pattern {pat}")

    return errors


def check_visual_deliverables(project_dir: str) -> list[str]:
    """UI 类项目必须有 DESIGN.md + 定稿参考图（Phase 2.5 视觉 Spike）。"""
    errors = []
    proj = Path(project_dir)

    # 机械判断是否 UI 类项目：PRODUCT.md 命中 UI 关键词
    product = gu.find_file_in_changes(project_dir, ["PRODUCT.md"])
    if product is None:
        return []  # PRODUCT.md 缺失由 gate-phase1 负责
    text = product.read_text(encoding="utf-8", errors="replace")
    if not re.search(UI_TRIGGER_PATTERN, text, re.IGNORECASE):
        return []  # 非 UI 类项目，不要求

    # 显式跳过标记（文件内需写明原因）
    if (proj / VISUAL_SKIP_MARKER).exists():
        return []

    # DESIGN.md 必须存在且 token 化
    design = gu.find_file_in_changes(project_dir, ["DESIGN.md"])
    if design is None:
        errors.append(
            "DESIGN.md: NOT FOUND — PRODUCT.md 命中 UI 关键词，UI 类项目必须执行 "
            "Phase 2.5 视觉 Spike（候选参考图→用户定稿→DESIGN.md token）。"
            "非 UI 项目请在项目根创建 .cp-visual-skip 并写明原因。"
        )
    else:
        dtext = design.read_text(encoding="utf-8", errors="replace")
        dlines = [l for l in dtext.splitlines() if l.strip()]
        if len(dlines) < 10:
            errors.append(
                f"DESIGN.md: only {len(dlines)} non-blank lines (need >= 10)")
        for pat, name in [(r"(?:色彩|颜色|color)", "色彩 token"),
                          (r"(?:字体|font)", "字体 token"),
                          (r"(?:间距|spacing)", "间距 token")]:
            if not re.search(pat, dtext, re.IGNORECASE):
                errors.append(f"DESIGN.md: missing {name} — pattern {pat}")

    # 定稿参考图：changes/**/visual/final.<img>
    changes_dir = proj / "changes"
    finals = []
    if changes_dir.exists():
        finals = [
            p for p in changes_dir.rglob("*")
            if p.is_file()
            and "visual" in p.parts
            and p.name.startswith("final.")
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ]
    if not finals:
        errors.append(
            "visual/final image: NOT FOUND — 定稿参考图必须存在 "
            "(changes/<日期>/visual/final.png|jpg|webp，候选图经用户定稿后复制为 final.*)")

    return errors


def run_gate(project_dir: str) -> None:
    """Run Phase 2 gate checks."""
    all_errors = []

    for filename, patterns in REQUIRED_DOCS.items():
        all_errors.extend(check_document(project_dir, filename, patterns))

    # Phase 2.5 视觉 Spike（UI 类项目）
    all_errors.extend(check_visual_deliverables(project_dir))

    if not all_errors:
        code = gu.generate_code(project_dir, GATE_NAME)
        gu.write_pending(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, True, code=code, pending=True)
    else:
        gu.output_result(GATE_NAME, False, errors=all_errors)


def main() -> None:
    if len(sys.argv) < 2:
        gu.output_result(GATE_NAME, False,
                         errors=["Usage: gate-phase2.py <project_dir> [--verify CODE]"])

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        gu.output_result(GATE_NAME, False,
                         errors=[f"Project directory not found: {project_dir}"])

    # --verify subcommand: confirm code and write marker
    if len(sys.argv) >= 4 and sys.argv[2] == "--verify":
        code = sys.argv[3]
        ok, msg, _ = gu.verify_and_write_marker(GATE_NAME, project_dir, code)
        gu.output_result(GATE_NAME, ok, errors=[msg] if not ok else None,
                         code=code if ok else None)
        return

    run_gate(project_dir)


if __name__ == "__main__":
    main()
