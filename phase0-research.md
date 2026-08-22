---
phase: 0
name: "内化历史教训 + 机械扫描 + 结构化问题清单"
gate_script: "gate-phase0.py"
output_files: ["phase0-data.json", "phase0-research.md"]
---

# Phase 0: 内化历史教训 + 机械扫描 + 结构化问题清单

## 执行步骤

两步执行（先机械后 LLM）：

### Step 0: 机械扫描（零 LLM 依赖）

```bash
python3 scripts/phase0-scan.py <项目目录>
```

输出 `phase0-data.json`（项目结构/技术栈/Obsidian 匹配/历史教训），**LLM 不参与此步骤**。

### Step 1: LLM 分析 + 结构化问题清单（基于 JSON 数据）

读取 `phase0-data.json` → 分析信息缺口 → 写 `phase0-research.md`。

📋 `/mnt/unraid_data/Obsidian/raw/projects/clsh-project/references/templates/phase0-research-template.md`

**⚠️ gate-phase0.py 新增检查（v2.0）：**
- `phase0-research.md` 必须包含 `## 待确认问题清单` 章节
- 必须有 **>= 10 个编号问题**（格式：`1. [维度] 问题描述?`）
- 问题必须覆盖 **>= 3 个维度**（功能/技术/边界/约束）
- 维度标签：`[功能]` `[技术]` `[边界]` `[约束]`

**问题生成策略（batch-grill-me 模式）：**
1. 从 phase0-data.json 的每个 section 提取盲区
2. 按 4 个维度分类生问题：
   - 功能/业务：用户角色、操作流程、场景覆盖
   - 技术/架构：框架选型、数据模型、部署方式
   - 边界/异常：错误处理、超时、数据异常
   - 约束/兼容：性能上限、安全要求、第三方依赖
3. 每个维度至少 2 个问题，总共 >= 10 个
4. 问题必须具体（"导入失败时如何处理？"✅ "还有什么问题吗？"❌）

```bash
python3 scripts/gate-phase0.py <项目目录>
```

## 铁律

- IL-4: **必须先运行 phase0-scan.py** — 无 phase0-data.json 不得进入 Phase 1
- IL-5: **必须写 phase0-research.md** — 无调研摘要不得进入 Phase 1
- IL-6: **phase0-research.md 必须引用 phase0-data.json 数据** — 不得编造
- IL-NEW: **phase0-research.md 必须包含 >= 10 个结构化问题** — 覆盖 >= 3 个维度

## 验收标准

- `phase0-data.json` 存在且非空
- `phase0-research.md` 存在且包含信息缺口清单
- `phase0-research.md` 包含 `## 待确认问题清单` 章节，>= 10 个编号问题
- 问题覆盖 >= 3 个维度（功能/技术/边界/约束）
- gate-phase0.py 返回 PASS
