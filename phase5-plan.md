---
phase: 5
name: "实现计划"
gate_script: "gate-phase5.py"
output_files: ["tasks.md"]
---

# Phase 5: 实现计划

## 前置依赖

- Phase 3 的 `proposal.md` + `constitution.md`
- Phase 4 的 gate-phase4.py PASS

## 执行步骤

协调者派任务（body 含 proposal + constitution 路径），coder 自己写 tasks.md。

**⛔ 协调者只 review 格式，不改内容。**

- INV-* 全覆盖 | P0 故事必须有任务 | P1/P2 须在 tasks.md 或 TECH.md "范围外"显式排除

### 字段格式要求（gate-phase5.py 正则匹配）

每个 Task 块必须包含以下纯文本字段（**不能用 markdown 加粗 `**`**）：

```
- status: ⬜
- phase: Phase N
- role: 角色名
- skills: 技能列表
- depends: 依赖
- covers: US-*, INV-*
```

gate-phase5.py 正则：
- 技能: `(?:skill|skills|agent|需要技能|技能)\s*[:=]`
- 角色: `(?:role|assignee|owner|responsible|角色).*?[:]`
- 验收: `(?:acceptance|criteria|验收)`

**⚠️ `- **需要技能**: xxx` 不匹配！必须用 `- skills: xxx`。**

## 产出

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tasks-template.md`

```bash
python3 scripts/gate-phase5.py <项目目录>
```
