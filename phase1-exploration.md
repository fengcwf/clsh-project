---
phase: 1
name: "需求澄清（缺口驱动探索追问）"
gate_script: "gate-phase1.py"
output_files: ["PRODUCT.md", "conversation.md"]
---

# Phase 1: 需求澄清（缺口驱动探索追问）

## 前置依赖

- Phase 0 的 `phase0-research.md`（必须存在）

## 执行步骤

基于 Phase 0 的 phase0-research.md 中的信息缺口，探索+追问交替进行。

### 执行节奏

```
Round 1-3:  探索缺口（web_search/竞品/技术调研）→ 追问确认
Round 4-6:  针对回答中的新缺口 → 定向探索 → 追问补充
Round 7+:   纯追问澄清（不再探索，信息已充分）
```

### 每轮工作流

1. **read_file phase0-research.md** — 注入信息缺口清单
2. **探索**（前 3 轮必须）：web_search / 竞品分析 / Obsidian 相关文档深度阅读
3. **追问**：基于探索结果，从不同角度追问用户
4. **持久化**：追问记录写入 conversation.md

### 停止条件

- **正常停止**：用户主动确认"材料足够" / 连续 3 轮无新信息
- **安全阀**：硬上限 15 轮 → 暂停，请求人工介入
- **⛔ LLM 不得主动建议进入下一阶段** — 只追问，不推进

### 范围蔓延拦截

用户提出新功能想法 → 记录到 backlog.md → 不纳入当前阶段

## 铁律

- IL-7: **Round 1-3 必须使用探索工具**（web_search/grep/browser）— 纯问答不算
- IL-8: **每轮必须 read_file phase0-research.md** — 确保缺口清单在 context 中
- IL-9: **停止条件由用户控制** — LLM 不得主动建议"可以进入 Phase 2"

## 产出

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/product-md-template.md`

```bash
python3 scripts/gate-phase1.py <项目目录>
```
