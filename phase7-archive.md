---
phase: 7
name: "归档复盘"
gate_script: "gate-phase7.py"
output_files: ["completion-summary.md", "retrospective.md", "handoff.md"]
---

# Phase 7: 归档复盘

## 前置依赖

- Phase 6 的 tester-report.md（PASS）

## 执行步骤

生成三份归档文档，归档到 changes/archive/：

1. `changes/archive/completion-summary.md` — 项目完成总结
2. `changes/archive/retrospective.md` — 复盘报告
3. `changes/archive/handoff.md` — 交接文档

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/overview-template.md`

## 验收标准

- 三份文件全部存在
- gate-phase7.py 返回 PASS

```bash
python3 scripts/gate-phase7.py <项目目录>
```
