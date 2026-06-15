# Pitfall #156: Gate 脚本检查的文件必须是该 Phase 的产出物

**日期：** 2026-06-15
**严重性：** 高（导致门禁永远 FAIL）

## 问题

gate-phase4.py 检查了 tasks.md（关键词 `验收标准`/`不在范围内`，≤80 行），但 tasks.md 是 Phase 5 的产出物（由 coder 写）。Phase 4 跑时 tasks.md 不存在，门禁永远 FAIL。

## 根因

gate-phase4.py 在 PRODUCT.md/TECH.md 引入之前设计，当时 tasks.md 可能是 Phase 3 就预创建的。SDD 优化后 tasks.md 的创建时机推迟到 Phase 5，但 gate-phase4.py 没同步更新。

## 修复

- phase4-mechanical-check.py：移除 `changes/*/tasks.md`，新增 `changes/*/PRODUCT.md` + `changes/*/TECH.md`
- gate-phase5.py：新增 PRODUCT.md 不变量覆盖检查（INV-* 在 tasks.md 中有引用）

## 规则

**Gate 脚本检查的文件必须是该 Phase 的产出物。** 新增 Phase 产出物时，必须同步更新对应的 gate 脚本。跨 Phase 检查（如 Phase 4 检查 Phase 5 文件）会导致门禁逻辑错误。

## 验证方法

跑 `gate-phase4.py <项目目录>` 时，检查 JSON 输出中的文件列表是否都是 Phase 3 的产出物。如果出现 Phase 5 的文件（如 tasks.md），说明检查范围错误。
