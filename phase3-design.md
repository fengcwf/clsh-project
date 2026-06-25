---
phase: 3
name: "设计文档"
gate_script: "gate-phase3.py"
output_files: ["proposal.md", "constitution.md"]
---

# Phase 3: 设计文档

## 前置依赖

- Phase 2 的 `TECH.md`（必须存在）

## 执行步骤

1. 基于 TECH.md 生成 proposal.md（设计决策，不写实现细节）
2. 生成 constitution.md（不可违反的约束）

**⛔ proposal 只写设计决策**，不写实现细节

## 产出

- proposal.md
- constitution.md（📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/constitution-template.md`）

```bash
python3 scripts/gate-phase3.py <项目目录>
```
