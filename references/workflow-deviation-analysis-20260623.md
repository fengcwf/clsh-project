# 插件偏离实测报告（精简版）

> 完整报告存 raw/projects/clsh-project/workflow-deviation-analysis-final-20260623.md

## 实测项目
Excel OA 数据导入工具增强（2026-06-23）

## 4 个插件失败根因

| # | 根因 | 插件位置 | 严重度 |
|---|------|---------|--------|
| 1 | Bootstrap 死锁 | 第 171-174 行 | P0 |
| 2 | delegate_task 盲区 | 第 210 行 | P0 |
| 3 | 路径匹配过窄 | 第 197 行 | P1 |
| 4 | 无 Phase 序列检查 | 全局 | P1 |

## 最小修复方案（+60 行）

### 修复 1: Bootstrap 死锁
GATE_DIR 存在即激活 Layer 2，用哨兵值标记 bootstrap 状态。

### 修复 2: delegate_task 拦截
无条件拦截 delegate_task/execute_code，Phase 3 完成前不允许。不依赖关键词匹配。

## 4 轮审查结论

| 原结论 | 修正后 |
|--------|--------|
| 三层架构是根因 | Bootstrap 死锁是 P0，三层架构是放大器 |
| 旧版更稳定 | 删除（幸存者偏差） |
| 关键词匹配拦截 | 改为无条件拦截 |
| 砍掉 Layer 2/3 | 保守精简（40→15） |
