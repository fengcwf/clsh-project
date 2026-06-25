---
phase: 2
name: "方案设计"
gate_script: "gate-phase2.py"
output_files: ["TECH.md"]
---

# Phase 2: 方案设计

## 前置依赖

- Phase 1 的 `PRODUCT.md`（必须存在）

## 执行步骤

1. 基于 PRODUCT.md 设计 2-3 个技术方案
2. 生成 TECH.md（架构决策 + 文件变更范围 + 实现注意事项）
3. TECH.md 必须包含方案对比表格
4. Phase 2.5: 技术 Spike（如有需要）

## 产出

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tech-md-template.md`

```bash
python3 scripts/gate-phase2.py <项目目录>
```
