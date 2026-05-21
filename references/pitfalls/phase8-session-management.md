# Phase 8 大量 Bug 修复的 Session 管理

## 问题
Phase 8（大佬测试反馈）可能一次反馈 10+ 个 bug。如果全部在一个 session 中修复：
1. 上下文 token 耗尽 → session 断开
2. Agent 超时后 fallback 到灵犀自修 → 违反角色分离
3. 修完一批后服务状态不确定 → 下一批可能踩坑

## 最佳实践

### 分批策略
- **每批 5-6 个 bug**，按优先级排序
- **后端 bug 先修**（通常少，且影响前端测试）
- **前端 bug 分组**：CSS/布局一组，JS 交互一组，新功能一组
- 每批修完 → `pm2 restart` + 基础健康检查 → 确认无回归

### Agent 超时处理
1. 第一次超时 → 缩小任务范围重试
2. 第二次超时 → 向大佬报告瓶颈，建议分批
3. 不要 fallback 到全量自修 → 违反角色分离 + 上下文爆炸

### Checkpoint 机制
每批修完后输出：
```
CHECKPOINT: Phase 8 批次 N
已修复: [列表]
待修复: [列表]
服务状态: OK/FAIL
```

### Session 断开恢复
1. 读 wiki/projects/<项目名>/overview.md 确认进度
2. 读 last checkpoint 确认已修复项
3. 从下一个未修复项继续

## 案例：Obsidian Workbench 第五轮（2026-05-21）
- 13 个 bug，全部灵犀直接修
- 后端 1 个 + 前端 12 个
- Agent 3 次超时后 fallback
- Session 在修复第 11 个 bug 后断开
- 正确做法：分 3 批（后端 1 个 + 前端 6 个 + 前端 6 个）
