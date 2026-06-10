# Pitfall #145: Phase 4 gate 脚本检查 tasks.md 导致预期 FAIL

## 日期
2026-06-10

## 问题
`gate-phase4.py` 调用 `phase4-mechanical-check.py`，后者检查 `changes/*/tasks.md` 是否存在、关键词是否完整、行数是否超限。但 tasks.md 是 Phase 5 产出，Phase 4 时尚不存在。

## 根因
gate-phase4.py 是一个"全量检查"脚本，设计时假设所有文档都已存在。但 Phase 4 的实际流程是：先自检 Phase 0-3 产出物 → 大佬确认 → 进入 Phase 5 写 tasks.md → 再跑 gate-phase4.py 生成确认码。

## 处理方式
1. Phase 4 自检时：跑 `phase4-mechanical-check.py`（底层检查），tasks.md 的 FAIL 为预期行为，不影响 Phase 4 判定
2. Phase 5 完成后：跑 `gate-phase4.py` 生成确认码（此时 tasks.md 已存在）
3. 不能因为 tasks.md FAIL 就认为 Phase 4 自检失败

## 影响
Phase 4 gate 脚本的 PASS/FAIL 判定需要人工判断 tasks.md 是否为预期缺失。
