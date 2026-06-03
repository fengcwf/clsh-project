# clsh-project 自进化机制

> 从 SKILL.md 迁出的自进化机制完整内容。SKILL.md 保留指针。

## 核心原则

### LLM 自评不可靠（2026-05-29 SkillLens 论文）

单 LLM 评委评估 skill 质量准确率仅 46.4%（接近随机）。加 meta-skill 维度后提升到 73.8%。**规则：** SKILL.md 评分必须用独立子 agent（不是灵犀自己），且每轮换新评委（避免锚定效应）。

### 维度关联簇（2026-05-29 花叔 40 次实验）

改一个评分维度时，关联维度会意外提升。Dim2/3/4 是结构簇（工作流清晰度/失败模式编码/检查点设计），Dim5/9 是具体性簇。**规则：** 优化时先改簇内最低维度，带动其他维度一起涨。不要一轮改多个维度。

### Skill 是可训练的外部状态（2026-05-29 SkillOpt 论文）

SKILL.md 不是"写完就完了"的静态文本，而是 LLM 的可训练外部状态（类似神经网络权重）。每次优化 = 一次训练步，必须通过验证（test-prompts）才能保留。**规则：** 修改 SKILL.md 前必须有验证机制（Darwin 棘轮或执行审计），不能凭感觉改。

### 执行审计应在归档时运行

执行审计器（`references/scripts/execution-audit.py`）应该在大佬说"归档"时触发（Phase 7 步骤 11），不需要 cron 定时。原因：审计需要完整的 session 数据，只有项目结束时才有。Phase 8 的修复轮次也是评分标准。

## Darwin 9 维 Rubric

详见 `references/methodology/darwin-ecc-evolution.md`。

**关键维度：**
- Dim5 可执行具体性（17 分，禁止模糊词）
- Dim3 失败模式编码（12 分，"如果 X 失败 → Y"）
- Dim8 实测表现（23 分，跑 test-prompts）

## 反模式黑名单

1. 用"文件是否存在""链接是否断"评估 SKILL.md 质量 = 文件卫生检查，对工作流进化没用
2. 评估 SKILL.md 质量时用 Darwin 9 维 rubric，不用文件结构检查脚本
3. ECC 证明确定性检查（grep session 日志 + exit code）比 LLM 判断可靠得多

## 执行审计触发

- **触发关键词：** "归档"/"wrap up"/"做完了吧"
- **执行位置：** Phase 7 步骤 11
- **审计脚本：** `references/scripts/execution-audit.py`
