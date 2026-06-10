# Pitfall #144: Unblock 卡片前未修复根因

## 场景

Kanban 卡 `t_c654446e`（artist，T16 CSS 变量化）连续 crash 4 次，报 `Unknown skill(s): popular-web-designs`。灵犀 unblock 后 worker 再 crash 2 次才最终成功（共 6 次 crash）。

## 时间线

| 时间 | 事件 | 说明 |
|------|------|------|
| 11:29 | 创建 | skills: popular-web-designs, frontend-ui-engineering |
| 11:30 | crash #1-2 | skill 解析失败，gave_up |
| 11:45 | unblock | 灵犀复制 skill 到 creative/ 目录后 unblock |
| 11:46 | crash #3-4 | **仍然失败** — bundled_manifest hash 不匹配 |
| 11:47 | 再次 gave_up | |
| 12:15 | 删除冲突副本 + 再次 unblock | 修复根因 |
| 12:16 | 成功执行 | |

## 根因

`popular-web-designs` 在 artist profile 存在两份副本（`creative/` 和 `software-development/`），bundled_manifest hash 与两个文件都不匹配。灵犀第一次修复只是复制了一份到 `creative/`（增加了第 3 份），没有删除冲突的 `software-development/` 副本。

## 铁律

**unblock 前必须确认根因已修复，否则只是浪费 crash 次数。**

```
1. 读 crash log → 定位根因
2. 修复根因（不是绕过）
3. 验证修复（ls/grep/手动测试）
4. 然后 unblock
```

**反模式：** 看到 crash → unblock → 期望"这次能行"

## 验证清单

unblock 前自问：
- [ ] crash 的根因是什么？（读 log，不是猜）
- [ ] 根因已修复？（有文件/配置变更证据）
- [ ] 修复已验证？（不是"应该可以了"）

## 关联

- Pitfall #143: Kanban Done ≠ Verified（同一批 crash）
- kanban-orchestrator: worker crash 诊断模式
