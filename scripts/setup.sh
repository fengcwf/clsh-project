#!/bin/bash
# setup.sh — 初始化 Spec-Driven Development 工作空间
# 用法: bash scripts/setup.sh [project-name]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECTS_DIR="${PROJECT_ROOT}/projects"

echo "========================================"
echo "  Spec-Driven Development — Setup"
echo "========================================"
echo ""

# ── Step 1: 创建 projects/ 目录 ──
echo "[1/3] Creating projects/ directory..."
if [ ! -d "$PROJECTS_DIR" ]; then
    mkdir -p "$PROJECTS_DIR"
    echo "  ✓ Created: $PROJECTS_DIR"
else
    echo "  ✓ Already exists: $PROJECTS_DIR"
fi

# ── Step 2: 验证 skill 安装 ──
echo "[2/3] Validating skill installation..."

REQUIRED_FILES=(
    "references/pitfalls/common.md"
    "references/workflow/overview.md"
    "references/workflow/phase-review.md"
    "references/anti-rationalization-patterns.md"
    "scripts/setup.sh"
)

MISSING=0
for f in "${REQUIRED_FILES[@]}"; do
    if [ -f "${PROJECT_ROOT}/${f}" ]; then
        echo "  ✓ ${f}"
    else
        echo "  ✗ MISSING: ${f}"
        MISSING=1
    fi
done

if [ "$MISSING" -eq 1 ]; then
    echo ""
    echo "ERROR: Some required files are missing."
    echo "Please ensure the skill is properly installed."
    exit 1
fi

# ── Step 3: 打印使用说明 ──
echo "[3/3] Setup complete!"
echo ""
echo "========================================"
echo "  Usage Instructions"
echo "========================================"
echo ""
echo "  1. Start a new project:"
echo "     mkdir -p projects/<project-name>"
echo "     cd projects/<project-name>"
echo ""
echo "  2. Follow the 8-phase workflow:"
echo "     Phase 1: Scout & Requirements → requirements.md"
echo "     Phase 2: Proposal             → proposal.md"
echo "     Phase 3: Constitution         → constitution.md"
echo "     Phase 4: Analysis             → analysis.md"
echo "     Phase 5: Task Planning        → tasks.md"
echo "     Phase 6: Execution            → code + evidence"
echo "     Phase 7: Review               → review-report.md"
echo "     Phase 8: Finalize & Archive   → final-report.md"
echo ""
echo "  3. Reference materials:"
echo "     references/pitfalls/common.md              — 常见陷阱（50个）"
echo "     references/workflow/overview.md            — 流程概览"
echo "     references/workflow/phase-review.md        — Review 详细流程"
echo "     references/anti-rationalization-patterns.md — 反理性化模式"
echo ""
echo "========================================"
echo "  Ready to go!"
echo "========================================"

exit 0
