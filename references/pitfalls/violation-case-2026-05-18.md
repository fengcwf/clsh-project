# 流程违规案例：Phase 6 Kanban 状态同步 + 角色分离

> 记录时间：2026-05-18
> 项目：halo-blog-agent

## 事件描述

Phase 6 Ralph Loop 执行过程中，出现两类流程违规：

### 违规 1：角色分离

**现象**：Task 8（定时任务配置）派给 worker 后，worker 进程崩溃/超时，Kanban 状态停留在 running。灵犀等待 2 分钟后直接创建了 3 个 cron 任务。

**根因**：worker 无超时机制，灵犀在等待过长后自行介入执行。

**正确做法**：
1. 创建 fix 卡派给另一个 worker
2. 或 escalate 给大佬
3. 即使"看起来很小"也不能自己动手

**教训**：效率不是跳过角色分离的理由。

### 违规 2：Kanban 状态同步

**现象**：Task 3 (Halo 发布适配器) 和 Task 7 (去AI味模块) 的 coder 完成了工作（产出物存在）但未正确调用 `kanban_complete`，导致状态停留在 running/blocked。

**根因**：子 agent 在完成工作后可能崩溃或未正确标记。

**正确做法**：
1. 灵犀等待 5 分钟后检查 running 状态的卡
2. 用 `ls` 检查产出物是否存在
3. 产出物存在则手动 `hermes kanban complete <id>` 标记完成
4. 不等 dispatcher 通知，主动推进流程

## 改进措施

1. **超时机制**：coder 10 分钟，worker 5 分钟，tester 5 分钟
2. **Review 卡自动创建**：灵犀在验证 checkpoint 后立即创建 Review 卡
3. **产出物预检**：agent 开始工作前先创建产出物目录，灵犀可通过 `ls` 判断是否在工作
