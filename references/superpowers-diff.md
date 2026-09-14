# Superpowers vs clsh-project-mimo 逐步对比

> Superpowers = obra/superpowers 工作流（brainstorming → worktrees → writing-plans → SDD/executing-plans → TDD → review → finish）。  
> clsh-project-mimo = 本 skill（路径分类 + Obsidian 容器 + 机械 gate + actor 角色）。

## 端到端映射

| 步骤 | Superpowers | clsh-project-mimo | 差异 | 优化空间 |
|------|-------------|-------------------|------|----------|
| 1 入口 | 自动看到「在建功能」就 brainstorm | 触发短语 / 分类 | SP 靠 hook/描述自动；clsh 靠 description | 已够 |
| 2 分类 | Spike / Bounded / Architectural | 同左 | **同源** | 保持 |
| 3 探索上下文 | 读文件/提交 | + **wiki vault** + **phase0-scan.py** | clsh 更强（知识库） | 保持 scan |
| 4 外部调研 | 无强制 web | **IL-7 探索证据 + scout**（P0） | clsh 更硬 | 保持 |
| 5 澄清 | 一次一问（bounded/arch） | 一次一问 + 维度 ≥3 + 假确认过滤 | clsh gate 更机械 | 可对齐 SP「过大多系统先拆分」 |
| 6 方案 | 2-3 approaches + 推荐 | 同 + proposal.md 方案表 + vault | 接近 | — |
| 7 审批门 | 设计批准硬门 | Phase2 status:approved + 用户批准 | **同强度** | — |
| 8 规格文档 | `docs/superpowers/specs/YYYY-MM-DD-*.md` | `raw/projects/<p>/changes/<slug>/proposal.md` | 路径不同 | vault 更佳 |
| 9 计划 | writing-plans：2-5 分钟步、完整代码、无占位 | tasks.md 同要求 + gate3 拦 TBD | clsh 有脚本 | SP 有 Global Constraints 头——已部分采用 |
| 10 worktree | using-git-worktrees 默认隔离 | 鼓励 feature branch，**不强制 worktree** | SP 更硬 | **可选**：Phase4 默认 worktree |
| 11 执行 | subagent-driven：brief+report+review package | 同结构（briefs/reports/reviews） | **几乎同构** | — |
| 12 角色 | 通用 implementer/reviewer | 可选 **clsh-coder/artist/tester/reviewer/scout** | clsh 角色更细 | 依赖安装 agents/ |
| 13 修复环 | 5 轮 + 模型升级 + scoped re-review | workflow `maxFix` 默认 2 + 升档 ultra + findings 覆盖 | SP 环更长 | 可把 maxFix 提到 5 |
| 14 TDD | 铁律先测后码 | 同铁律 | **同** | — |
| 15 ledger | SDD ledger 防 compact | ledger.md 同 | **同** | — |
| 16 终审 | whole-branch review 最强模型 | Phase5 整分支审查 | **同** | — |
| 17 收尾 | finishing-a-development-branch 选项 | Phase6 归档进 Obsidian + overview | clsh 知识沉淀更强 | SP 的 merge/PR 选项可并入 Phase6 |
| 18 复利 | 基本无跨项目库 | wiki/solutions Phase6 可选写入 | clsh 胜 | 保持只读日常 |

## 反模式对照（两边都防）

| 反模式 | Superpowers | clsh-project-mimo |
|--------|-------------|-------------------|
| 太简单不审批 | Red flags 表 | Anti-Rationalization 表 |
| 先写码 | TDD iron law | 同 + gate |
| 自我放行 | 独立 reviewer | actor reviewer + 不自判 |
| 占位计划 | No Placeholders | gate3 正则 |
| compact 丢进度 | ledger | ledger + vault |

## 仍有优化空间的点（按 ROI）

| 优先级 | 项 | 建议 |
|--------|----|------|
| P1 | Worktree 默认隔离 | Phase4 Setup：若 git 仓库则建议 `git worktree` / feature branch，禁止直接 main |
| P1 | 修复环轮次 | 3→5，与 SP 对齐；R4+ 强制 fresh implementer |
| P1 | Plan 头 Global Constraints | tasks.md 强制「## Global constraints」节（gate3 可查） |
| P2 | 完成选项 | Phase6 询问 merge / PR / keep，不只归档文档 |
| P2 | Visual companion | 仅 UI 重设计时用；非核心 |
| P2 | worktree skill 内嵌说明 | 简短步骤写进 phases.md |
| P3 | 批量同形小任务 | SP：同形小改可合并一个 dispatch——已可在实践中用，可写进 SKILL |

## 结论

- **计划→子代理执行→双轴审查→ledger** 与 Superpowers SDD **同构**。  
- **相对 SP 强点**：Obsidian 项目容器、机械 gate 脚本、wiki 复利、角色化 agents。  
- **相对 SP 弱点**：无默认 worktree、修复环更短、无 finishing 分支工作流细化。  
- **相对 Hermes**：无 kanban 物理 bot 与 gate-enforcer；用 actor/session-chat/自定义 agent 近似。
