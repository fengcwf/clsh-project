# 被拒绝的 Skill 编辑记录

> 记录 SKILL.md/pitfalls/workflow 修改尝试被 TDD for Skills Gate 拒绝的编辑方向。
> 目的：防止"改回去再改回来"的循环，提供负面反馈。
>
> 借鉴来源：SkillOpt rejected edit buffer（+3.4 分 ablation）
>
> 格式：每次记录编辑内容、验证结果、原因分析。

## 记录模板

```markdown
### [日期] 编辑描述

- **目标文件**: SKILL.md / references/pitfalls/common.md / references/workflow/phaseX.md
- **修改内容**: 具体改了什么
- **验证方式**: test-prompts 执行结果
- **Gate 结果**: ❌ REJECTED / ⚠️ NO CHANGE
- **原因分析**: 为什么这次修改没有提升或导致回退
- **后续处理**: 回滚 / 记录但不接受 / 调整后重试
```

## 被拒绝的编辑

> 2026-06-07 初始化。以下为预测性的高风险编辑方向（基于 clsh-project 历史教训）。

### 预测性风险编辑（待验证）

| 编辑方向 | 风险等级 | 原因 | 状态 |
|---------|---------|------|------|
| 删除 Phase 2.5（简化流程） | 🔴 高 | 技术验证环节缺失会导致 Phase 6 返工 | 待验证 |
| 合并 Phase 3+4（加速） | 🔴 高 | 自检和设计确认混在一起质量下降 | 待验证 |
| 取消独立 tester（改 inline review） | 🔴 高 | Superpowers v5.0.6 做了但 clsh-project 选择保留独立 tester | 已有教训 |
| 删除 Phase 8 diagnose 6 阶段（简化） | 🟡 中 | 跳过 Stage 1-2 直接修 = 瞎猜 | 待验证 |
| 减少 pitfalls 数量（精简到 50 条以下） | 🟡 中 | 可能丢失低频但重要的教训 | 待验证 |
| 增加 Phase 数量（拆分 Phase 6 为 6a/6b/6c） | 🟡 中 | 流程复杂度增加，用户感知更差 | 待验证 |

## 为什么记录这个

1. **防止循环优化** — 改了 A 发现不好，改回去；过几个月又想改 A
2. **提供负面反馈** — 教训记录的是"什么出了问题"，这里记录的是"什么修改没用"
3. **与 TDD for Skills 配合** — Gate 拒绝的编辑自动记录到这里
4. **指导未来优化** — 高风险编辑方向需要更谨慎的验证
