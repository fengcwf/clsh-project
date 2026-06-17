# 常见陷阱清单 — Spec-Driven Development

> 本文件汇总实际使用中遇到的高频错误。每个陷阱包含：现象、根因、修复方法、预防措施。
> 按流程阶段排序，阶段号对应 8 阶段模型（P1-P8）。

---

## Phase 1: Scout & Requirements

### Pitfall #1: 跳过 Scout 直接开干
**Phase:** 1
**现象:** 收到需求后直接写 proposal，没有做任何技术调研
**根因:** LLM 倾向于立即生成"有用"的输出，跳过看似低效的研究阶段
**修复:** 回退到 Phase 1，用 3 个不同搜索策略收集技术约束
**预防:** Phase 1 checkpoint 必须有 `tech-constraints.md` 文件且至少 3 条约束

### Pitfall #2: Scout 产出复制粘贴搜索结果
**Phase:** 1
**现象:** tech-constraints.md 充满未消化的网页摘录，没有提炼为可操作的约束
**根因:** 没有要求"基于调研形成决策建议"
**修复:** 每条约束必须包含：约束描述 + 影响范围 + 推荐方案
**预防:** 模板中强制包含 3 个子字段

### Pitfall #3: Requirements 过于模糊，无法验证
**Phase:** 1
**现象:** 需求文档包含"应该支持多种方式"这类模糊描述
**根因:** 将讨论摘要直接作为验收标准
**修复:** 每条需求必须可测试：输入 → 预期输出
**预防:** 使用 GIVEN-WHEN-THEN 格式重写每条需求

### Pitfall #4: 遗漏非功能性需求
**Phase:** 1
**现象:** 只记录功能需求，性能/安全/兼容性需求缺失
**根因:** LLM 关注"做什么"而忽略"在什么约束下做"
**修复:** 补充约束清单（性能、安全、兼容、运维）
**预防:** 需求模板包含非功能性需求分区且标记为必填

### Pitfall #5: 不读现有代码就定义需求
**Phase:** 1
**现象:** 定义的功能与现有架构冲突，后续阶段全部返工
**根因:** 假设白板开发，忽略已有代码库约束
**修复:** 在 scout 阶段必须列出依赖的现有文件和接口
**预防:** tech-constraints 必须包含 `existing-code-dependencies` 小节

---

## Phase 2: Proposal

### Pitfall #6: Proposal 包含实现细节而非设计决策
**Phase:** 2
**现象:** proposal 中写"用 Express.js + SQLite"，没有说明为什么不用 Flask
**根因:** LLM 默认输出最熟悉的方案，不进行方案比较
**修复:** 每个技术选择必须附带 2-3 个替代方案及排除理由
**预防:** proposal 模板强制包含"技术选型理由"和"替代方案排除记录"

### Pitfall #7: Proposal 没有 scope 边界
**Phase:** 2
**现象:** 没有明确说"本项目不包含 X"，后续阶段不断膨胀
**根因:** LLM 倾向于"有用的全覆盖"，不愿意说"不"
**修复:** 补充 `out-of-scope` 小节，明确排除项
**预防:** proposal 模板中 `out-of-scope` 为必填项

### Pitfall #8: 架构图无法验证
**Phase:** 2
**现象:** 画了漂亮的架构图但模块间接口未定义
**根因:** 图是给人看的，LLM 不会自动验证图的一致性
**修复:** 每条箭头必须对应一个已定义的接口/数据流
**预防:** 架构图评审清单：每个箭头 = 1 个接口 = 1 个模块归属

### Pitfall #9: Proposal 过度设计
**Phase:** 2
**现象:** 为简单 CRUD 引入微服务、消息队列、CQRS
**根因:** LLM 学习了大量"最佳实践"但缺乏 context 判断
**修复:** 在 proposal 中增加"复杂度预算"约束
**预防:** 限制 proposal 中组件数量不超过功能数量的 1.5 倍

### Pitfall #10: 未记录已知风险
**Phase:** 2
**现象:** 项目进行到一半才发现依赖的 API 有速率限制
**根因:** Scout 阶段的风险没有传递到 proposal
**修复:** proposal 必须包含 risk register（至少 3 项）
**预防:** risk register 模板字段：风险描述 + 影响 + 概率 + 缓解方案

---

## Phase 3: Constitution

### Pitfall #11: Constitution 没有可测试的验收标准
**Phase:** 3
**现象:** 宪法写了"代码质量应良好"但没有定义"良好"是什么
**根因:** 将主观标准作为约束
**修复:** 每条标准必须可量化（测试覆盖率 > 80%、Lint 零错误、单文件 < 300 行）
**预防:** constitution 模板中验收标准为必填且必须是可执行的

### Pitfall #12: Constitution 与 Proposal 矛盾
**Phase:** 3
**现象:** constitution 禁止使用全局变量，但 proposal 设计了状态管理器
**根因:** 没有对照 proposal 逐条校验
**修复:** constitution 完成后运行 proposal-conformance 检查
**预防:** constitution 模板包含"引用 proposal 决策"小节

### Pitfall #13: Constitution 过于严格导致无法执行
**Phase:** 3
**现象:** 要求 100% 测试覆盖率但项目只有 2 天
**根因:** 没有根据项目规模调整约束
**修复:** constitution 应有分级：MUST（必须）和 SHOULD（建议）
**预防:** 模板包含约束分级标签，MUST 项不超过 10 条

### Pitfall #14: Constitution 缺少违反后果
**Phase:** 3
**现象:** 约束写了但没有说违反了怎么办
**根因:** 约束没有 enforcement 机制
**修复:** 每条 MUST 约束必须有验证命令或检查方式
**预防:** constitution 模板包含"验证方式"字段

---

## Phase 4: Analysis

### Pitfall #15: Orchestrator 做分析而非记录
**Phase:** 4
**现象:** orchestrator 自己分析代码结构，跳过读取现有文件
**根因:** LLM 倾向于基于记忆生成，而非基于证据生成
**修复:** 分析报告中的每条结论必须引用具体文件和行号
**预防:** analysis 模板要求 `[file:line]` 格式的证据引用

### Pitfall #16: Analysis 不读前序阶段产出
**Phase:** 4
**现象:** analysis 忽略 proposal 的架构决策，重新做一遍选型
**根因:** 没有将前序文件作为分析的必要输入
**修复:** analysis 开头必须有一个"前序决策摘要"小节
**预防:** 模板强制包含 dependency-links 指向 proposal/constitution

### Pitfall #17: Analysis 产出不具体
**Phase:** 4
**现象:** 分析报告写了"需要重构用户模块"但没说怎么重构
**根因:** 缺乏可操作性，停留在"发现"阶段
**修复:** 每个发现必须包含：具体文件 + 具体改动 + 影响范围
**预防:** analysis 模板的每个 finding 必须包含 action-item

### Pitfall #18: 分析遗漏安全风险
**Phase:** 4
**现象:** 没有检查 SQL 注入、XSS、敏感信息泄露
**根因:** 安全不是 LLM 的默认关注点
**修复:** analysis 必须包含 security-checklist 子节
**预防:** 模板中 security-review 为必填项

---

## Phase 5: Task Planning

### Pitfall #19: Tasks.md 缺少 role 标签
**Phase:** 5
**现象:** 任务描述了做什么但没说谁来做（architect/coder/tester/reviewer）
**根因:** 模板中 role 字段不是必填
**修复:** 为每个任务补充 `[role: coder]` 标签
**预防:** tasks.md 模板中 role 为必填字段

### Pitfall #20: 任务太大（>1 文件, >100 行）
**Phase:** 5
**现象:** 一个任务要求"实现整个用户系统"
**根因:** LLM 不会主动拆分大任务
**修复:** 拆分为多个子任务，每个任务 <= 1 个文件 <= 100 行
**预防:** 模板验证：每个任务必须有 `scope` 字段且文件数 <= 1

### Pitfall #21: 任务没有 scope exclusions
**Phase:** 5
**现象:** 任务标题模糊，cooder 自由发挥超出范围
**根因:** 没有明确说"这个任务不做什么"
**修复:** 每个任务添加 `out-of-scope: 不修改 X, 不涉及 Y`
**预防:** tasks.md 模板的每个 task 必须有 `out-of-scope` 字段

### Pitfall #22: 任务缺少验证命令
**Phase:** 5
**现象:** 任务描述了代码改动但没有说如何验证成功
**根因:** 没有要求任务包含 verification
**修复:** 每个任务添加 `verify: npm test && npm run lint`
**预防:** tasks.md 模板中 verify 命令为必填

### Pitfall #23: 任务之间依赖关系不清晰
**Phase:** 5
**现象:** 多个任务并行执行但需要同一个共享资源
**根因:** 没有显式标注依赖
**修复:** 用 `depends_on: [task-1, task-2]` 显式标注
**预防:** 模板包含依赖图自动生成

### Pitfall #24: 合并多个 bug 为一个修复任务
**Phase:** 5
**现象:** 一个 fix 任务里塞了 3 个不相关的 bug 修复
**根因:** 图省事，认为"都是修复"
**修复:** 每个 bug 单独建任务，有独立的验证命令
**预防:** 模板规则：一个任务只修一个 bug

### Pitfall #25: Phase 6 在 Phase 5 任务被审查前就开始执行
**Phase:** 5/6
**现象:** orchestrator 看到 tasks.md 写完就直接派发 coder
**根因:** 没有强制的 gate：tasks.md 必须先经过 reviewer
**修复:** tasks.md 完成后必须有 C7 review checkpoint
**预防:** 流程卡点：没有 reviewer 签字不能进入 Phase 6

---

## Phase 6: Execution

### Pitfall #26: 使用 delegate 但不嵌入上下文
**Phase:** 6
**现象:** 委派任务时只说"实现用户模块"，不提供 architecture.md 内容
**根因:** 假设 cooder 能读取所有文件
**修复:** delegate 时必须在 goal 中嵌入：文件路径 + 相关架构片段 + 接口定义
**预防:** delegate 模板包含 context-embedding 强制字段

### Pitfall #27: 接受 subagent 自报告成功
**Phase:** 6
**现象:** subagent 说"done"，orchestrator 就相信了
**根因:** 信任 subagent 的声明而非验证
**修复:** 必须检查 verification output、diff、test results
**预防:** 成功判定规则：只看证据，不看声明

### Pitfall #28: 不检查委派上下文是否被使用
**Phase:** 6
**现象:** 提供了 architecture.md 但 cooder 从没读过
**根因:** 没有验证机制检查 subagent 是否使用了提供的上下文
**修复:** 在 cooder 产出中检查是否引用了提供的文件
**预防:** 要求 cooder 在产出中包含 `[context-used]` 引用列表

### Pitfall #29: Cooder 实现超出任务范围
**Phase:** 6
**现象:** 任务要求改 model.py，cooder 顺手改了 view.py
**根因:** 没有明确限定修改范围
**修复:** 任务的 `scope` 字段必须列出允许修改的文件清单
**预防:** orchestrator 验证产出 diff 仅包含 scope 内文件

### Pitfall #30: 忽略 cooder 的编译/测试输出
**Phase:** 6
**现象:** cooder 的终端输出显示了 warning 但 orchestrator 没注意
**根因:** 没有要求检查 cooder 的全部终端输出
**修复:** 每次执行后必须读取 cooder 终端输出并提取 warning/error
**预防:** 终端输出自动扫描规则：任何 warning 必须记录

### Pitfall #31: 缺少 tester review（代码任务）
**Phase:** 6
**现象:** 代码任务完成后直接标记 done，跳过测试验证
**根因:** 测试被视为可选而非必须
**修复:** 所有 `[role: coder]` 任务必须附带 tester review
**预防:** 流程硬性要求：coder 任务 → tester 验证 → 才能 done

### Pitfall #32: 并行任务冲突
**Phase:** 6
**现象:** 两个 coder 同时修改同一个文件
**根因:** 没有文件锁或依赖检查
**修复:** 通过 depends_on 和 scope 字段控制串行
**预防:** orchestrator 在派发前检查 scope 重叠

---

## Phase 7: Review

### Pitfall #33: Self-review 代替独立 review
**Phase:** 7
**现象:** 实现者自己审查自己的代码
**根因:** 角色混淆，一个人做了 coder 和 reviewer
**修复:** reviewer 必须是不同角色，且未参与实现
**预防:** C7 review 必须由独立的 reviewer 角色执行

### Pitfall #34: Review 仅看 src/ 目录
**Phase:** 7
**现象:** review 只检查源代码，忽略配置、文档、测试
**根因:** "review = code review" 的狭义理解
**修复:** review scope 必须覆盖整个项目：src + config + docs + tests + scripts
**预防:** review checklist 包含所有目录类型

### Pitfall #35: Review 项目目录结构不符合标准
**Phase:** 7
**现象:** review 输出格式混乱，找不到 evidence、recommendation
**根因:** 没有使用标准 review 模板
**修复:** 每个 finding 必须有：severity + evidence + recommendation
**预防:** review 模板强制要求标准字段

### Pitfall #36: Review 只报告问题不给修复建议
**Phase:** 7
**现象:** "此处有安全风险"但没说怎么修
**根因:** review 只做发现不做推荐
**修复:** 每个 finding 必须包含 actionable recommendation
**预防:** 模板中 recommendation 为必填字段

### Pitfall #37: Review 发现未分类严重级别
**Phase:** 7
**现象:** 所有问题混在一起，无法区分 blocker vs minor
**根因:** 没有 severity 分级
**修复:** 每个 finding 必须标注 critical/major/minor/suggestion
**预防:** 模板包含 severity 枚举字段

### Pitfall #38: Review 没有验证修复后的状态
**Phase:** 7
**现象:** reviewer 指出问题后直接结束，没验证是否真的修了
**根因:** 缺少 re-review 环节
**修复:** 修复后必须有 re-check 并更新 finding 状态
**预防:** review 流程包含 re-verify 步骤

---

## Phase 8: Finalize & Archive

### Pitfall #39: Phase 8 反馈缺少现象+文件+标准
**Phase:** 8
**现象:** 最终反馈写了"基本满意"但没说哪里好哪里不好
**根因:** 反馈粒度不够
**修复:** 每条反馈必须包含：具体现象 + 涉及文件 + 对应验收标准
**预防:** 反馈模板包含三要素必填字段

### Pitfall #40: 归档到错误目录
**Phase:** 8
**现象:** 项目文件散落在 root 目录而非 `projects/<name>/`
**根因:** 没有检查归档目标路径
**修复:** 移动所有文件到 projects/<project-name>/
**预防:** 归档脚本自动验证目标路径

### Pitfall #41: 归档后遗留临时文件
**Phase:** 8
**现象:** .bak、.tmp、node_modules 等被一起归档
**根因:** 归档时没有排除规则
**修复:** 归档前执行 clean：排除临时文件和依赖目录
**预防:** .archive-exclude 规则：*.bak, *.tmp, node_modules, .env.local

### Pitfall #42: 未生成最终报告就结束
**Phase:** 8
**现象:** 直接 archive 不生成 summary
**根因:** 认为 archive = 完成
**修复:** 先生成 final-report.md，再归档
**预防:** 流程卡点：没有 final-report 不能执行 archive

---

## Cross-Phase: General LLM Coordination Failures

### Pitfall #43: LLM 自动化跳过流程步骤
**Phase:** Any
**现象:** "Phase 2 没什么好做的，直接开始 Phase 3"
**根因:** LLM 理性化（rationalization）：用合理理由解释为什么跳步
**修复:** 回退到被跳过的步骤，执行该步骤的最小有效版本
**预防:** 每个 phase 必须有不可跳过的 checkpoint

### Pitfall #44: 在长 session 中上下文窗口耗尽
**Phase:** Any
**现象:** 早期阶段的决策在后期被遗忘
**根因:** 上下文窗口有限，长 session 丢失远端信息
**修复:** 关键决策写入文件而非依赖记忆
**预防:** 每个阶段产出独立文件，下一阶段通过文件获取上下文

### Pitfall #45: 子任务上下文污染
**Phase:** 6
**现象:** cooder 的局部上下文影响了全局决策
**根因:** subagent 无法区分全局和局部上下文
**修复:** 为每个 subagent 提供精简的、仅与任务相关的上下文
**预防:** delegate 时明确标注 [全局] vs [局部] 上下文

### Pitfall #46: 文件版本竞争
**Phase:** 6
**现象:** 多个 subagent 同时写同一个文件，后写覆盖先写
**根因:** 文件是共享状态，没有锁机制
**修复:** 通过任务编排确保互斥访问
**预防:** 每个任务的 scope 禁止访问其他任务的 scope 文件

### Pitfall #47: 错误传播但未终止
**Phase:** Any
**现象:** 一个任务失败了，但 orchestrator 忽略错误继续执行
**根因:** LLM 倾向于"继续前进"而非"停下处理"
**修复:** 任何 critical error 必须触发 pause 而非 skip
**预防:** 错误处理规则：critical = 暂停, major = 记录并继续, minor = 记录

### Pitfall #48: 生成的代码包含硬编码值
**Phase:** 6
**现象:** API key、URL、端口号直接写在代码里
**根因:** LLM 不会主动考虑配置管理
**修复:** 替换为环境变量或配置文件引用
**预防:** constitution 必须包含"禁止硬编码"规则

### Pitfall #49: 忽略已有测试
**Phase:** 6
**现象:** 实现了新功能但没有对应的测试
**根因:** 测试被视为"nice to have"
**修复:** 为每个新功能补充对应测试
**预防:** tasks.md 要求：每个 coder 任务附带 test-case 任务

### Pitfall #50: 不读项目其他部分就修改
**Phase:** 6
**现象:** 修改了一个函数但没有更新调用方
**根因:** 局部视角，缺乏全局理解
**修复:** 修改后 grep 所有调用点并更新
**预防:** 任务 scope 必须包含"受影响的调用点"分析
