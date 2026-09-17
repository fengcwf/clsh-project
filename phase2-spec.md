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
5. Phase 2.5: 视觉 Spike（UI 类项目强制，gate-phase2.py 机械检查）

## Phase 2.5: 视觉 Spike（UI 类项目）

> **目的：** UI 决策在像素层面定稿，防止"文字决策→实现漂移"（Superpowers #1783 实证失败模式：
> 门禁全绿但交付 UI 与设计决策相反）。参考图 = 用户判断材料（用户判断→方案选择）；
> DESIGN.md = token 化的可传递约束，逐字进入 coder 的 task brief 与 constitution。

**触发条件（机械判断，非 LLM 裁量）：** PRODUCT.md 命中 UI 关键词
（仪表盘|Dashboard|Gridstack|前端页面|界面|Tab|页面|UI）。非 UI 项目在项目根放
`.cp-visual-skip`（文件内写一行原因）显式跳过。

**执行步骤：**

1. 调研视觉方向：竞品截图/设计系统（可用 `popular-web-designs` / `design-taste-frontend`）
2. 生成 2-3 张候选参考图（`ai-ui-design-generation` 或 `frontend-design`），存
   `changes/<日期>/visual/candidate-*.png`
3. 逐张给用户选择 → 用户选定 1 张 → 复制为 `changes/<日期>/visual/final.png`（定稿）
4. 产出 DESIGN.md（与 TECH.md 同目录）：色彩 token（主色/中性色/语义色 + hex 值）、
   字体/字号阶梯、间距阶梯、圆角/阴影、断点清单、定稿图引用路径
5. 定稿后需求变更 → 记录 backlog.md，禁止静默重新生成

**⛔ 铁律：参考图未定稿、DESIGN.md 未产出，不得进入 Phase 3。**
gate-phase2.py 机械检查 DESIGN.md（≥10 行 + 色彩/字体/间距 token）+ visual/final 定稿图。

## 产出

- TECH.md（必选）
- DESIGN.md + visual/final.png（UI 类项目必选，Phase 2.5）

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/tech-md-template.md`

```bash
python3 scripts/gate-phase2.py <项目目录>
```
