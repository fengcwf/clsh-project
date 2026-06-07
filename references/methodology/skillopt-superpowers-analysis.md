# SkillOpt × Superpowers v5.1.0 × clsh-project 三方对比分析

> 调研时间：2026-06-07
> 目的：分析 SkillOpt 和 Superpowers 对 clsh-project 的优化价值，识别 P0-P2 问题点

---

## 一、框架概览

| 维度 | SkillOpt | Superpowers v5.1.0 | clsh-project v5.23.0 |
|------|----------|-------------------|----------------------|
| **定位** | Skill 文档的自动优化器 | 编码 agent 的完整方法论框架 | 需求驱动的项目开发工作流 |
| **核心机制** | 5 步训练循环（Rollout→Reflect→Edit→Gate→Memory） | 14 个 composable skills + TDD for Skills | 8 Phase 门禁 + 角色分离 + Ralph Loop |
| **优化目标** | 任务性能分数（量化） | 流程纪律（规则） | 流程门禁 + 角色分离 |
| **Skill 演进方式** | 自动训练循环 | 手动 + TDD for Skills | 手动 + Darwin rubric |
| **验证机制** | held-out validation score（自动、量化） | 5 步验证 + 防借口表（规则强） | 5 步验证 + Backpressure Gates（规则+强制） |
| **适用场景** | 有明确 benchmark 的任务 | 编码项目 | 多类型项目（web/内容/运维） |
| **Stars/成熟度** | 新发布（2026.05） | 219K stars, v5.1.0 | 私有，v5.23.0 |

---

## 二、SkillOpt 核心机制

### 2.1 训练循环

```
Rollout（执行任务记录轨迹）
  → Reflect（分析成败 minibatch）
  → Edit（结构化 add/delete/replace 操作）
  → Gate（验证门控：只在验证集严格提升时才接受）
  → Memory（拒绝编辑缓冲 + 慢更新 + 元技能）
```

### 2.2 关键控制机制

| 机制 | 作用 | Ablation 效果 |
|------|------|--------------|
| 文本学习率预算（lr=4） | 限制每次编辑量，防止破坏性重写 | +2.7 分 |
| 拒绝编辑缓冲（rejected edit buffer） | 记录被拒绝的编辑方向，避免重复 | +3.4 分 |
| 验证门控（held-out gating） | 编辑只在验证集提升时才接受 | 核心机制 |
| 慢更新 + 元技能 | 更长horizon的反馈 | +7.5 分 |

### 2.3 结果

- 6 benchmark × 7 模型 × 3 harness = 52 个评估单元，全部最佳或并列最佳
- GPT-5.5 上平均 +23.5 分
- 优化后的 skill 文档（300-2000 tokens）可跨模型/harness 迁移

---

## 三、Superpowers v5.1.0 关键机制

### 3.1 writing-skills: TDD for Skills

```
NO SKILL WITHOUT A FAILING TEST FIRST

RED:   创建压力场景 → 无 skill 时 agent 违反 → 记录违规行为
GREEN: 写最小 skill → 有 skill 时 agent 遵守
REFACTOR: 发现新借口 → 堵漏 → 重测
```

### 3.2 verification-before-completion: 防借口机制

```
Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

| 借口                 | 现实                   |
|---------------------|-----------------------|
| "Should work now"   | RUN the verification  |
| "I'm confident"     | Confidence ≠ evidence |
| "Just this once"    | No exceptions         |
| "Agent said success"| Verify independently  |
```

### 3.3 v5.1.0 关键变更

- Review Loop: subagent review → inline self-review（30s vs 25min）
- No Placeholders 强化
- Code Review 合并到单文件
- SDD 不再每 3 任务暂停

---

## 四、clsh-project 现有机制

### 4.1 已有的强项

| 机制 | 来源 | 状态 |
|------|------|------|
| 5 步验证函数 | Superpowers 移植 | ✅ 完整 |
| Backpressure Gates Layer 1-2 | 四框架分析 | ✅ 已实施 |
| 防辩解表（Phase 6/8） | Superpowers 借鉴 | ✅ 已内嵌 |
| 维度关联簇研究 | 花叔 40 次实验 | ✅ 独有 |
| Darwin 9 维 rubric | SkillLens 论文 | ✅ 完整 |
| 执行审计 | Phase 7 集成 | ✅ 已自动化 |

### 4.2 关键差距

| 差距 | 来源 | 影响 |
|------|------|------|
| 无 TDD for Skills 流程 | Superpowers + SkillOpt | 改 skill 不知道是否变好 |
| 无拒绝编辑缓冲 | SkillOpt | 无"被拒绝修改"记录 |
| 无量化门控 | SkillOpt | Darwin rubric 是手动评估 |
| 教训外置（非内嵌） | Superpowers | 读 Phase 时看不到常见错误 |

---

## 五、P0-P2 深度分析

### 🔴 P0：验证门控

| 维度 | SkillOpt | Superpowers | clsh-project |
|------|----------|-------------|--------------|
| 核心机制 | validation score 严格门控 | 5 步验证 + 防借口表 | 5 步验证 + Backpressure Gates |
| 量化标准 | ✅ 数值评分 | ❌ 规则检查 | ❌ 规则检查 |
| 防借口机制 | ❌ 无（自动执行） | ✅ Rationalization Table | ✅ Phase 6/8 已有 |
| 自动回滚 | ✅ 验证失败自动回滚 | ❌ 依赖 agent 遵守 | ❌ 依赖 worker 遵守 |
| Skill 修改门控 | ✅ 编辑必须验证通过 | ✅ TDD for Skills | ❌ 无（改了就算） |

**差距分析：**
1. ✅ Phase 6/8 已有防辩解表（与 Superpowers 对齐）
2. ❌ 缺失 TDD for Skills → **已补齐（P0-B）**
3. ❌ 缺失量化门控 → 需要 test-prompts 机制（长期）

### 🟠 P1：拒绝编辑缓冲

| 维度 | SkillOpt | Superpowers | clsh-project |
|------|----------|-------------|--------------|
| 记录什么 | 被 Gate 拒绝的编辑方向 | Common Mistakes（内嵌各 skill） | pitfalls/common.md（83+ 条外置） |
| 查询方式 | 自动注入优化器 | 读 skill 时自动看到 | 需要额外查 pitfalls 文件 |
| 结构化 | ✅ 结构化 | 🟡 半结构化 | 🟡 半结构化 |

**差距分析：**
1. ✅ pitfalls 已有 83+ 条（比 Superpowers 更丰富）
2. ❌ 缺失"被拒绝的修改"记录 → **已补齐（P1-B）**
3. ❌ 教训外置 → 内嵌到各 Phase workflow 会增加 token 消耗 <10%，但命中率提升

### 🟡 P2：学习率预算

| 维度 | SkillOpt | Superpowers | clsh-project |
|------|----------|-------------|--------------|
| 控制方式 | lr=4 个编辑操作 | "Write minimal skill" | 膨胀阈值 + 维度关联簇 |
| 量化 | ✅ 编辑操作数限制 | ❌ 原则 | 🟡 有研究，无硬规则 |

**差距分析：**
1. ✅ 已有维度关联簇研究（SkillOpt 和 Superpowers 都没有）
2. ❌ 无硬规则 → 建议抛弃（P2 优先级低，现有膨胀阈值已够用）

---

## 六、LLM 能力无关性检查

**原则：** 流程控制不依赖 LLM 判断力。LLM 强时和 LLM 弱时，流程应产出一致的结果。

### 检查结果

| 优化 | 是否引入 LLM 依赖 | 判断 |
|------|-----------------|------|
| P0-A: 防辩解表 | ❌ 无（纯规则文本） | ✅ 安全 |
| P0-B: TDD for Skills | ⚠️ 有（Step 4 VALIDATE 需要 LLM 判断表现） | ⚠️ 需要注意 |
| P1-B: rejected-edits.md | ❌ 无（纯记录文件） | ✅ 安全 |

### P0-B 的 LLM 依赖分析

TDD for Skills 的 Step 4 VALIDATE 需要 LLM 判断"新表现是否 ≥ baseline"。

**缓解措施：**
1. test-prompts 有明确的 PASS/FAIL 标准（不是模糊的"好不好"）
2. Gate 规则是硬编码的（新 ≥ baseline → 接受，新 < baseline → 回滚）
3. 例外情况已定义（紧急修复、纯格式调整、新增 pitfalls）

**结论：** P0-B 引入了轻微的 LLM 依赖（判断 PASS/FAIL），但通过明确的标准和硬编码的 Gate 规则缓解。不会导致"LLM 弱时静默失败"。

---

## 七、实施总结

### 已完成

| 优化 | 动作 | 文件 |
|------|------|------|
| P0-A | Phase 6/8 已有防辩解表，无需新增 | — |
| P0-B | TDD for Skills 流程 | references/methodology/self-evolution-mechanism.md |
| P1-B | rejected-edits.md | references/pitfalls/rejected-edits.md |

### 待确认

| 优化 | 说明 | 需要 |
|------|------|------|
| P0-C | Backpressure Gates Layer 3（kanban complete 前校验） | 需要改 Hermes kanban 模块代码 |

### 抛弃

| 优化 | 原因 |
|------|------|
| P2 学习率预算 | 优先级低，现有膨胀阈值已够用 |

---

## 八、一句话总结

> **SkillOpt 证明了"验证可以自动"（validation gating + rejected buffer），Superpowers 证明了"规则可以很强"（Rationalization Prevention + TDD for Skills）。clsh-project 的 5 步验证函数与 Superpowers 对齐，TDD for Skills 已补齐，rejected-edits 已创建。核心差距从"缺机制"缩小到"缺量化"（test-prompts），这是长期优化目标。**
