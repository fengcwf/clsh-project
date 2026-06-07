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

### TDD for Skills（2026-06-07 SkillOpt + Superpowers 借鉴）

**核心原则：修改 SKILL.md = 写代码，必须先写测试再改。**

借鉴来源：
- Superpowers writing-skills: "NO SKILL WITHOUT A FAILING TEST FIRST"
- SkillOpt: held-out validation gating（编辑只在验证集提升时才接受）

**流程：**

```
修改 SKILL.md 前：
  Step 1: BASELINE — 用当前 skill 执行 3-5 个代表性任务，记录 baseline 表现
  Step 2: IDENTIFY — 明确要改什么（哪个维度、哪个 Phase）
  Step 3: EDIT — 修改 SKILL.md（每次最多改 1 个维度）
  Step 4: VALIDATE — 用修改后的 skill 重新执行同样的任务
  Step 5: GATE — 新表现 ≥ baseline 才接受修改，否则回滚
```

**Test Prompts 存储：** `references/test-prompts/<skill-name>.md`

**Test Prompts 要求：**
- 每个 skill 至少 3 个 test prompts
- 覆盖该 skill 的核心场景（不是边界场景）
- 每个 prompt 有明确的 PASS/FAIL 标准
- prompt 本身要稳定（不随项目变化）

**Gate 规则：**
- 新表现 ≥ baseline → 接受修改
- 新表现 < baseline → 回滚修改，记录到 rejected-edits.md
- 新表现 = baseline（无变化）→ 记录但不接受（改了没用 = 浪费）

**例外：**
- 紧急修复（大佬要求立即改）→ 先改，后补 test-prompts 验证
- 纯格式调整（不改语义）→ 不需要 test-prompts
- 新增 pitfalls（不改现有规则）→ 不需要 test-prompts

**与 Darwin rubric 的关系：**
- Darwin rubric: SKILL.md 整体质量评估（每季度/大版本）
- TDD for Skills: 单次修改的验证（每次修改）
- 两者互补：TDD 保证每次改都是正向，Darwin 保证整体质量

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

### 执行审计触发

- **触发关键词：** "归档"/"wrap up"/"做完了吧"
- **执行位置：** Phase 7 步骤 11
- **审计脚本：** `references/scripts/execution-audit.py`

### 学习率预算（2026-06-07 SkillOpt 借鉴）

**核心原则：每次修改幅度要有限制，不能大改。**

借鉴来源：SkillOpt 文本学习率 lr=4（限制每次编辑操作数），ablation +2.7 分。

**硬规则：**

1. **每次 SKILL.md 修改最多改 1 个维度** — Darwin 9 维 rubric 的 9 个维度，每次只改最低的 1 个。改一个维度会带动关联维度一起涨（维度关联簇），但同时改多个维度会产生干扰。
2. **每次新增 pitfalls ≤ 3 条** — 批量添加 > 3 条时，拆成多次修改。每次修改后验证 SKILL.md 整体一致性。
3. **单次 workflow 修改不超过 1 个 Phase** — 不跨多个 Phase 同时改 workflow 文件。

**例外：**
- 大佬要求批量修改 → 可以一次改多个维度，但必须事后记录到 rejected-edits.md（如果验证失败）
- 新增 pitfalls 为紧急修复（大佬反馈的高频错误）→ 可以一次加 5 条，但必须是独立的新增，不改现有规则
- 归档/清理操作（不改语义）→ 不需要限制

**与膨胀阈值的关系：**
- 膨胀阈值控制总量（SKILL.md ≤900 行，common.md ≤80 条）
- 学习率预算控制单次修改幅度（每次 ≤1 维度，≤3 条 pitfalls）
- 两者互补：膨胀阈值是总量上限，学习率是每次增量
