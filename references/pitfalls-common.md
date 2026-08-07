# clsh-project 常见陷阱清单

version: "1.5"
updated: 2026-08-07

## 1. 角色分离（5 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 1 | Coordinator 做代码推理 | 只说目标和验收条件，禁止在 task body 写实现方案 | Critical |
| 2 | 跳过 Tester 角色 | 代码必须经独立 Tester 验证，Coordinator 不得自我放行 | Critical |
| 3 | 直接写任务内容 | Coordinator 写 task spec，不写代码、不跑命令 | High |
| 4 | 自己判断 C7 合格 | C7 由 Tester 产出报告，Coordinator 只读取并决策 | Critical |
| 5 | 向 task body 注入分析 | task body 只含目标和约束，分析内容放 reference files | Medium |

## 2. 流程合规（8 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 6 | 跳过 Phase | 每个 Phase 必须产出对应产出物才能进入下一阶段 | Critical |
| 7 | 直接跳到写代码 | 必须先完成 Phase 1-3（定义/研究/设计） | Critical |
| 8 | 不运行 gate 脚本 | Phase 门禁必须由脚本自动判断，禁止手动通过 | Critical |
| 9 | 手动生成确认码 | 确认码必须由 gate 脚本生成，禁止编造 | Critical |
| 10 | 跳过 Scout 研究 | Phase 2 必须运行 scout 生成技术摘要 | High |
| 11 | Phase 入口不重读 SKILL.md | 每次进入新 Phase 必须重新阅读对应阶段说明 | High |
| 12 | 复用旧确认码 | 确认码一次性使用，每次 gate 检查必须重新生成 | Critical |
| 13 | 跳过 Phase 3 设计 | 技术方案必须有独立设计文档，不得边做边想 | High |

## 3. 执行质量（8 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 14 | Fire-and-forget 派发 | 发出任务后必须等待结果，监控超时 | High |
| 15 | task body 塞太多参考文件 | task body ≤ 3 行，详细信息放 reference files | Medium |
| 16 | 声称修复但不验证 | 必须运行验证脚本/测试，展示通过输出 | Critical |
| 17 | 验证前不重启服务 | 代码改动后必须重启服务再跑验证 | High |
| 18 | Phase 8 文档不达标 | 交付文档必须包含摘要、文件列表、运行方式 | High |
| 19 | Tester 超时处理 | 超时必须记录并升级，不可静默跳过 | High |
| 20 | Way C 违规 | Tester 给出具体代码方案而非验收目标 | Critical |
| 21 | 忘记 notify-subscribe | 任务完成后必须通知并订阅后续更新 | Medium |

## 4. 文档管理（5 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 22 | 写入错误路径 | 写入前确认目标路径在 project-root 下 | High |
| 23 | 写入后不验证 | 写文件后必须 `ls` 确认文件存在 | High |
| 24 | 模板双副本 | 模板只保留一个位置，禁止同时维护两份 | Medium |
| 25 | 归档路径错误 | 归档必须移入 archive/，不得留在原位 | High |
| 26 | 文档写入作为门禁条件 | gate 脚本检查文档存在性，Coordinator 不得自定义规则 | High |

## 5. LLM 行为模式（4 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 27 | 先问用户再查 skill/memory | 本地信息优先，查完再向用户确认 | High |
| 28 | 合理化例外 | 遇到规则冲突时必须遵守规则，不可找理由绕过 | Critical |
| 29 | 反向合理化 | 引用 Guard 表格来确认跳步判断 = 合理化。Guard 是拦截器不是确认清单 | Critical |
| 30 | 假设项目类型不适配 | 每个项目都走完整流程，不跳过任何阶段 | High |

## 6. /goal 与迭代控制（4 条）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 31 | Phase 1-6 用 /goal | /goal 只适用于 Phase 8 反馈循环和 fix 卡 | Critical |
| 32 | /goal judge 替代 tester | judge 只判断迭代是否收敛，tester 必须独立验证 | Critical |
| 33 | /goal 绕过 gate 脚本 | /subgoal 必须嵌入 gate-phase8 文档检查 | High |
| 34 | 实现卡用 --goal | 实现卡单 shot 足够，--goal 只适合 fix 修复卡 | High |

## 7. gate 脚本交互（5 条，2026-06-23 新增）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 35 | gate 脚本中文本地化 | regex 模式必须同时匹配中英文关键词 | High |
| 36 | delegate_task 绕过 gate-enforcer | gate-enforcer 的 pre_tool_call hook 只监控父 agent 的工具调用，子 agent 的 patch/write_file 不在监控范围。Phase 1-3 未完成时 coordinator 禁止派修改型 delegate | Critical |
| 37 | gate 文件放错目录 | gate 脚本用 find_file_in_changes() 搜索，只搜 changes/*/ 和项目根目录。project-docs/ 不在搜索路径中。文档必须放 changes/<日期>-<话题>/ | High |
| 38 | gate-phase5 tasks.md 格式不匹配 | regex 期望独立行 `role:` 和 `skills:`（不带 ** 包裹）。用 **负责人角色**: 不匹配。每个 task 必须有 role:、skills:、验收标准: 三行 | High |
| 39 | gate-phase6 tester-report 缺证据 | tester-report.md 不能只有断言（PASS），必须包含实际命令输出作为证据（test results/logs/code blocks） | High |
| 40 | 跳过 Phase 1 五维度追问 | Phase 1 必须走完 5 维度框架（用户与场景/功能与流程/安全与威胁/合规与隐私/行业与技术），不能因为"需求明确"就跳过 | High |

## 8. Superpowers 6.0 优化相关（3 条，2026-07-15 新增）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 41 | 派 tester 前不生成 review package | Phase 6 协调者必须先运行 gen-review-package.sh，tester 只读 review-package.md | High |
| 42 | 派 implementer 时传完整 tasks.md | 必须生成 task-N-brief.md，implementer 只读 brief 文件 | High |
| 43 | tester 输出冗长 | tester-report 用简洁合同（双轴判定+证据+风险点），禁止完整审查报告 | Medium |

## 9. MoA 优化相关（5 条，2026-08-07 新增）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 44 | 跳过 ledger 创建 | Phase 6 开始时必须从 ledger-template.md 创建 ledger.md，gate-phase6 检查存在性 | Critical |
| 45 | compaction 后不读 ledger | compaction 后必须 read_file ledger.md 恢复进度，禁止重新 dispatch 已完成任务 | Critical |
| 46 | fix loop 无上限 | fix 循环最多 5 轮（R=1-5），R=5 必须 controller 裁决，禁止 R>5 继续派发 | Critical |
| 47 | scoped re-review 扩大范围 | re-review 只检查原始 findings 是否解决，禁止审查未修改文件或提出新 findings | High |
| 48 | re-review 发现当新 findings 处理 | re-review 中发现的未修改代码问题记录到 ledger，不进入当前 fix 循环 | Medium |

## 10. Phase 8 Optimization Loop（5 条，2026-08-07 新增）

| # | 陷阱 | 规则 | 严重度 |
|---|------|------|--------|
| 49 | Phase 8 ad-hoc 处理反馈 | 每次处理反馈必须声明 skill 锚定 + 查路由表，禁止直接修改 | Critical |
| 50 | 主会话直接执行代码 | Phase 8 每个任务必须 delegate_task（fresh context），不允许在主会话执行 | Critical |
| 51 | 一轮处理多个反馈 | One Thing Per Iteration——每轮只处理一个反馈（Ralph 铁律） | High |
| 52 | 跳过 Gap Analysis | Phase 8 必须先 8a（只读分析）再 8b（实现），禁止直接进入实现 | High |
| 53 | 超过 Circuit Breaker 阈值 | max_rounds=10, timeout=15min, stuck=3 轮。触发后必须停止并报告用户 | Critical |
