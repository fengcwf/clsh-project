---
phase: 4
name: "机械自检"
gate_script: "gate-phase4.py"
output_files: []
---

# Phase 4: 机械自检

## 前置依赖

- Phase 0-3 的全部产出文件

## 执行步骤

1. 运行 `gate-phase4.py <项目目录>` → 获取检查结果
2. 根据错误修复对应文件：
   - `Missing file` → 检查文件是否在 changes/*/ 或 project root
   - `too short` → 补充内容到 ≥5 非空行
   - `missing required content` → 补充关键词（见下方清单）
3. 重新运行 `gate-phase4.py` 直到 PASS

## 关键词清单

| 文件 | 必须包含 |
|------|---------|
| overview.md | goal/purpose/scope/目标/范围 |
| conversation.md | requirement/user.story/需求/用户 |
| proposal.md | approach/option/方案/选型 |
| constitution.md | constraint/must.not/约束/禁止 |
| PRODUCT.md | goal/requirement/用户故事 |
| TECH.md | architecture/design/架构/技术选型 |

## 验收标准

- gate-phase4.py 返回 PASS + 确认码

```bash
python3 scripts/gate-phase4.py <项目目录>
```
