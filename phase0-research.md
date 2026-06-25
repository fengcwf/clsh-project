---
phase: 0
name: "内化历史教训 + 机械扫描"
gate_script: "gate-phase0.py"
output_files: ["phase0-data.json", "phase0-research.md"]
---

# Phase 0: 内化历史教训 + 机械扫描

## 执行步骤

两步执行（先机械后 LLM）：

### Step 0: 机械扫描（零 LLM 依赖）

```bash
python3 scripts/phase0-scan.py <项目目录>
```

输出 `phase0-data.json`（项目结构/技术栈/Obsidian 匹配/历史教训），**LLM 不参与此步骤**。

### Step 1: LLM 分析（基于 JSON 数据）

读取 `phase0-data.json` → 分析信息缺口 → 写 `phase0-research.md`。

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase0-research-template.md`

```bash
python3 scripts/gate-phase0.py <项目目录>
```

## 铁律

- IL-4: **必须先运行 phase0-scan.py** — 无 phase0-data.json 不得进入 Phase 1
- IL-5: **必须写 phase0-research.md** — 无调研摘要不得进入 Phase 1
- IL-6: **phase0-research.md 必须引用 phase0-data.json 数据** — 不得编造

## 验收标准

- `phase0-data.json` 存在且非空
- `phase0-research.md` 存在且包含信息缺口清单
- gate-phase0.py 返回 PASS
