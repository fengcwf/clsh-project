---
title: "v6.2.0→v6.3.0 审计记录"
date: 2026-06-22
tags: [audit-record, v6.3.0, model-rotation]
---

# v6.2.0→v6.3.0 审计记录

## 审计背景

4 轮模型循环审查 clsh-project v6.2.0 的工作流逻辑和模板。

## 发现并修复的 10 项问题

### P0（阻断级）

1. **phase-confirmations.md Phase 编号完全脱节** — 模板描述旧版实现流程（Phase 0-4），SKILL.md 是 Kiro spec-driven 流程（Phase 0-8）。重写对齐。
2. **gate-phase1.py 不存在** — SKILL.md 引用了不存在的脚本。Phase 1（最关键的需求阶段）无机械门禁。新建脚本。
3. **Task 格式三方冲突** — SKILL.md 用 `###`，template 用 `##`，gate-phase5.py 只匹配 `##`。统一为 `##` + gate 支持 `#{2,3}`。
4. **verify_marker() 死代码 + 无 TTL** — HMAC 签名写入但从未验证。新增 `verify_marker_with_expiry()` + GATE_SECRET + TTL。

### P1

5. **缺少 proposal.md 模板** — Phase 3 产出物无结构引导。新建模板。
6. **Phase 1 追问无停止条件** — 5 维度 × 3 层级 = 15+ 轮无上限。新增 3 个停止条件。

### P2

7. **gate-phase2/3 缺目录存在性检查** — 传入不存在目录会抛异常。添加 `Path.is_dir()` + `gu.output_result()`。
8. **gate-phase5 中文 regex 不匹配** — `SKILL_ANNOTATION_PATTERNS` 只匹配英文。添加 `需要技能|技能`。
9. **gate-phase7 归档检查缺失** — Phase 7 的 9 步归档无 gate 保护。新增 `check_archive_docs()`。
10. **SKILL.md Gate 表不一致** — G1 改为 Phase 1 预检，G5 添加 TTL 描述。

## R2 发现但 R3/R4 降级的问题

| 问题 | R2 评级 | 最终评级 | 说明 |
|------|---------|---------|------|
| verify_marker 无调用者 | Critical | P3 | 死代码无安全影响 |
| GATE_SECRET 不验证 | Critical | P3 | defense-in-depth |
| Gate 间无状态链 | Critical | P2 | 文件依赖已间接保护 |

## 关键教训

1. **phase-confirmations.md 是最易过时的模板** — 流程变更时必须同步更新
2. **gate 脚本的关键词 regex 需要定期审计** — 过宽的 regex（如 `design`）等于没有检查
3. **R2 对抗审查的"Critical"需要 R3/R4 交叉验证** — 同模型审查有系统性夸大倾向
4. **Gate 脚本代码风格需统一** — gate-phase2/3 缺少目录检查是因为新增时间不同

## 评分变化

v6.2.0: 6.95/10 → v6.3.0: 8.5/10（+1.55）
