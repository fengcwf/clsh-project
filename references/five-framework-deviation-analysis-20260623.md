# 五框架对比分析 + clsh-project 架构修正

**日期**: 2026-06-23

## 核心发现

clsh-project 是唯一把流程控制放在 prompt 中的框架。其他 5 个框架都用非 prompt 机制。

| 框架 | 防偏离机制 |
|------|-----------|
| Superpowers | 短流程 + 自包含（每 skill ≤400 行，5-10 条教训） |
| GStack | 角色隔离（一次一个角色，天然限制行动范围） |
| Spec Kit | 可执行规范（spec 直接生成代码，LLM 无判断空间） |
| OpenSpec | 文件即状态（`ls` 就知道当前 Phase） |
| Ralph Loop | 客观信号（测试通过是唯一出口，不让 AI 自评） |

## Phase 0-1 偏离根因

SKILL.md 440 行，LLM 读到 Phase 0 时脑子里装着 Phase 1-8 → 注意力分散 → 跳过 gate。

不是"规则放错位置"（规则确实在文件中），而是"规则堆在了一个太长的文件里"。

## 2026-05-22 决策修正

原决策："不拆分 — 保持单体 skill（Phase 是连续流程，拆分增加切换开销）"

已证明错误。Superpowers 的 14 个 skill 方案更稳定。

## 修正方案

拆分为 1 主 skill（~100 行红线）+ 9 Phase 子 skill（各 50-80 行）。切换机制复用现有 gate 脚本。

完整报告：/mnt/unraid_data/Obsidian/raw/projects/clsh-project/five-framework-deviation-analysis-20260623.md
