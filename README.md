# /clsh-project — 需求驱动项目开发工作流(通用版)

> **Spec-driven development workflow for AI agents — 从需求澄清到设计文档到实现计划到执行。**
> Inspired by Kiro Spec-Driven Development, Superpowers Brainstorming, Phoenix State Machine Execution.

## 📖 这是什么 / What is it?

clsh-project 是一个面向 AI Agent 的**需求驱动项目开发工作流**。当用户提出新项目或功能需求时，不直接写代码，而是走完整 需求→设计→计划→执行 流程，确保产出高质量、可追溯的软件。

## ✨ 核心特性 / Key Features

| 特性 | 说明 |
|------|------|
| **8 阶段工作流** | Phase 0-8，从需求澄清到反馈循环，每个阶段有明确产出物和门禁 |
| **机械门禁脚本** | `scripts/gate-phase*.py` 检查产出物存在性、关键词、格式，不依赖 LLM 判断力 |
| **反合理化护栏** | Anti-Rationalization Guard — 阻止 LLM 创造"合理例外"跳过规则 |
| **LLM 无关性设计** | 流程控制不依赖 LLM 能力，强 LLM 和弱 LLM 产出一致结果 |

## ⚡ 快速开始 / Quick Start

```bash
# 1. 克隆 / Clone
git clone <repo-url> ~/.hermes/skills/clsh-project

# 2. 环境自检 / Check environment
python3 ~/.hermes/skills/clsh-project/scripts/env-check.py

# 3. 配置 / Configure
cp ~/.hermes/skills/clsh-project/config.example.json ~/.hermes/skills/clsh-project/config.json
# 编辑 config.json，根据 env-check 输出调整配置
```

## 🏗️ 架构流程图 / Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 0+1: 需求准备与澄清                                       │
│  ↓ (PRODUCT.md + conversation.md)                              │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2+2.5: 方案设计与技术验证                                  │
│  ↓ (TECH.md)                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3+4: 设计文档与自检 ⛔ gate-phase4.py                    │
│  ↓ (proposal.md + constitution.md)                             │
├─────────────────────────────────────────────────────────────────┤
│  Phase 5: 实现计划 ⛔ gate-phase5.py                            │
│  ↓ (tasks.md)                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Phase 6: 分发执行 ⛔ gate-phase6.py + gate-phase7.py           │
│  ↓ (coder/artist 执行, tester 验证)                              │
├─────────────────────────────────────────────────────────────────┤
│  Phase 7: 完成归档与流程复盘                                      │
│  ↓ (completion-summary.md + retrospective.md)                  │
├─────────────────────────────────────────────────────────────────┤
│  Phase 8: 反馈循环 ⛔ gate-phase8.py                             │
│  (修改文档 + 验证)                                               │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 能力等级 / Capability Levels

| 等级 | 依赖 | 能力 |
|------|------|------|
| **Level A（完整）** | kanban + gate-enforcer | 全功能：任务派发 + 机械门禁 + 物理阻断 |
| **Level B（标准）** | delegate_task | 核心流程完整：子任务派发 + 机械门禁 |
| **Level C（轻量）** | 仅 prompt 约束 | 退化为 Superpowers 级防偏离 |

## 📊 与同类工具对比 / Comparison

| 特性 | clsh-project | Superpowers | Kiro |
|------|-------------|-------------|------|
| 需求→设计→计划→执行 | ✅ 8 阶段 | ✅ Brainstorming | ✅ Spec-driven |
| 机械门禁脚本 | ✅ gate-phase*.py | ❌ 依赖 LLM | ❌ 依赖 LLM |
| 反合理化护栏 | ✅ Anti-Rationalization Guard | ❌ 无 | ❌ 无 |
| LLM 无关性 | ✅ 脚本+硬编码 | ❌ | ❌ |
| 通用性 | ✅ 无平台依赖 | ⚠️ Obsidian | ⚠️ AWS |
| 3 层规则架构 | ✅ Gate+Convention+Pitfall | ❌ | ❌ |

## 📁 项目结构 / Structure

```
clsh-project/
├── SKILL.md              # 技能定义（流程规则+门禁+模板）
├── config.example.json   # 配置模板
├── scripts/
│   ├── env-check.py      # 环境自检脚本
│   ├── gate_utils.py     # 门禁工具函数
│   ├── gate-phase1.py    # Phase 1 门禁
│   ├── gate-phase4.py    # Phase 4 门禁（含码生成）
│   ├── gate-phase5.py    # Phase 5 门禁
│   ├── gate-phase6.py    # Phase 6 门禁
│   ├── gate-phase7.py    # Phase 7 门禁（review 报告）
│   └── gate-phase8.py    # Phase 8 门禁
├── templates/            # Phase 产出物模板
│   ├── product-md-template.md
│   ├── tech-md-template.md
│   ├── constitution-template.md
│   ├── tasks-template.md
│   └── phase-confirmations.md
└── references/
    └── pitfalls-common.md  # 高频教训 Top 10
```

## 📚 安装指南 / Installation

详细安装步骤请查看 [INSTALL.md](INSTALL.md)。

## 📄 许可证 / License

MIT License

---

**灵感来源 / Inspired by:** Kiro Spec-Driven Development · Superpowers Brainstorming · Phoenix State Machine Execution
