# OpenSpec 对比分析

## 概述

clsh-project v2.0 借鉴了 OpenSpec 的 Delta Spec 模式，但做了以下关键改进。

## 对比表

| 维度 | OpenSpec | clsh-project v2.0 |
|------|----------|-------------------|
| **项目隔离** | 扁平结构（单项目） | 项目级命名空间（多项目并行） |
| **执行方式** | 单 AI 线性执行 | Kanban + 5 worker 并行 |
| **Review** | 无内置 review | 强制 review gate（tester） |
| **依赖管理** | 无（线性列表） | Kanban parents 链 |
| **崩溃恢复** | 无（会话中断就没了） | SQLite 持久化（自动 reclaim） |
| **需求记录** | conversation.md | conversation.md（借鉴） |
| **增量规格** | Delta Spec | delta-specs/（借鉴） |
| **归档** | 自动归档到 archive/ | 归档 + SoT 合并（借鉴） |
| **Dashboard** | openspec view | kanban list + INDEX.md |

## 借鉴的概念

1. **Delta Spec 模式** — 只写变更部分，不重复已有信息
2. **Conversation 持久化** — 需求探索过程记录到文件
3. **Archive 机制** — 变更完成后归档，不删除
4. **Source of Truth** — 系统当前状态的规格，增量维护

## 不借鉴的部分

1. **单 AI 执行** — 保持多 agent 并行
2. **无 Review** — 保持强制 review gate
3. **扁平结构** — 改为项目级命名空间
4. **AI 主导需求** — 保持人主导、AI 辅助

## 与 OpenSpec 的映射

| OpenSpec 概念 | clsh-project 映射 |
|--------------|------------------|
| openspec/project.md | raw/projects/<project>/overview.md |
| openspec/specs/ | raw/projects/<project>/source-of-truth/ |
| openspec/changes/<name>/ | raw/projects/<project>/changes/<name>/ |
| openspec/changes/<name>/proposal.md | 同上 |
| openspec/changes/<name>/specs/ | raw/projects/<project>/changes/<name>/delta-specs/ |
| openspec/changes/<name>/tasks.md | 同上 |
| openspec/changes/<name>/conversation.md | 同上 |
| openspec/changes/archive/ | raw/projects/<project>/changes/archive/ |
| openspec view (dashboard) | kanban list + INDEX.md |

## 参考链接

- OpenSpec GitHub: https://github.com/Fission-AI/OpenSpec
- OpenSpec 详细分析: https://intent-driven.dev/knowledge/openspec/
- Hashrocket 对比: https://hashrocket.com/blog/posts/openspec-vs-spec-kit
- Martin Fowler SDD 分析: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
