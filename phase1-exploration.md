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

- **正常停止**：同时满足以下两个条件：
  1. LLM 连续提出 ≥3 个新问题，用户都回答"没有了"/"足够了"/"确认"
  2. conversation.md 中已有 ≥5 轮讨论记录
- **安全阀**：硬上限 15 轮 → 暂停，请求人工介入
- **⛔ LLM 不得主动建议进入下一阶段** — 只追问，不推进
- **⛔ "继续"不是确认** — 用户回复"继续"/"没问题"/"好的"不算材料足够，必须是明确回答 LLM 的具体问题

### 追问强制规则

每轮 LLM 必须：
1. 从不同角度提出 ≥1 个新问题（功能/边界/异常/性能/安全/兼容性）
2. 问题必须具体（"导入失败时如何处理？"✅ "还有什么问题吗？"❌）
3. 如果用户回答了所有问题，LLM 必须再找新角度提问
4. 只有用户明确说"没有了"/"足够了"/"确认进入下一阶段"才可停止

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
