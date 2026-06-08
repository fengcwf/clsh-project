# Darwin + ECC 自进化方法论

> 日期：2026-05-29
> 来源：darwin-skill v2.0 + ECC + SkillLens/SkillOpt 论文 + 花叔 40 次优化实验

---

## 核心概念：Skill = 可训练的外部状态

来自 SkillOpt 论文（微软 2026-05-22）：

| 概念 | 神经网络训练 | Skill 优化 |
|------|------------|-----------|
| 被优化的权重 | 模型参数 | SKILL.md 文本 |
| 训练器 | 反向传播 | LLM 分析弱维度，提出修改 |
| Loss 函数 | 交叉熵 | 9 维 rubric 评分 |
| 验证集 | held-out 数据 | test-prompts.json |
| 优化器 | SGD/Adam | git commit / git revert（棘轮） |
| 学习率 | η | 每轮只改一个维度 |
| 早停 | val loss 不降 | 连续 2 轮 Δ < 1 分 |

---

## 9 维 Rubric（Darwin v2.0 + SkillLens）

| # | 维度 | 权重 | 评分标准 | 来源 |
|---|------|------|---------|------|
| 1 | Frontmatter 质量 | 7 | name/description 含做什么+何时用+触发词 | Darwin |
| 2 | 工作流清晰度 | 12 | 步骤有序号、每步有明确输入/输出 | Darwin |
| 3 | **失败模式编码** | **12** | **必须写"如果 X 失败 → Y"；只写正向流程扣 ≥3 分** | SkillLens |
| 4 | 检查点设计 | 6 | 关键决策前有 🔴 CHECKPOINT / 🛑 STOP | Darwin |
| 5 | **可执行具体性** | **17** | **禁止"建议/可以考虑/根据情况/灵活把握"；≥3 处扣 ≥3 分** | SkillLens |
| 6 | 资源整合度 | 4 | references/ 路径可达 | Darwin |
| 7 | 整体架构 | 12 | 不冗余不遗漏、无 AI 腔废话 | Darwin |
| 8 | **实测表现** | **23** | **用 test-prompts 跑一遍看输出质量** | Darwin |
| 9 | 反例与黑名单 | 6 | 有"不要做什么"清单 + 高风险行动黑名单 | SkillLens |

**总分 100。Dim5（17 分）和 Dim8（23 分）权重最高。**

---

## 维度关联簇（花叔 40 次实验发现）

> 改一个维度时，关联维度会意外提升。实测：改 Failure Modes → Workflow 也从 7.5 涨到 9.0。

| 簇 | 包含维度 | 优化策略 |
|----|---------|---------|
| **结构簇** | Dim2 + Dim3 + Dim4 | 改簇内最低的，其他会跟着涨 |
| **具体性簇** | Dim5 + Dim9 | 加具体操作步骤时，反例也会变具体 |
| **效果簇** | Dim8 | 独立——必须跑 test-prompts |

**优化顺序：先结构簇 → 再具体性簇 → 最后效果簇。**

---

## LLM 评估的局限性

| 发现 | 数据 | 来源 |
|------|------|------|
| 单 LLM 评委准确率 | 46.4%（接近随机） | SkillLens |
| 加 meta-skill 维度后 | 73.8% | SkillLens |
| 多评委独立审查 | 更高 | darwin-skill v2.0 |

**根本问题：** 评委虽然独立于改进者，但底层模型相同，共享偏差。
**解决方案：** human-in-the-loop 是最后安全网。

---

## ECC 执行验证（我们的独有价值）

Darwin 只优化 SKILL.md 文本质量，不评估执行效果。我们的执行审计器补了这个缺口。

| 组件 | 做什么 | 不依赖 LLM |
|------|--------|-----------|
| 执行审计器 | grep session 日志检查合规率 | ✅ 确定性 |
| Pitfall 触发计数 | 统计规则被触发次数 | ✅ 确定性 |
| 模式匹配表 | 症状→原因→检查方法 | ✅ 查表 |
| pass@k 指标 | 流程合规率/修复轮次/验证通过率 | ✅ 计数 |

**两层互补：**
- Darwin 层 → LLM 驱动 → 优化 SKILL.md 写得好不好
- ECC 层 → 代码驱动 → 验证 SKILL.md 被执行时效果好不好

---

## 反模式黑名单（花叔 40 次实验 + SkillLens）

| # | 反模式 | 后果 |
|---|--------|------|
| 1 | 同一个 LLM 又改又评 | 准确率 46.4% |
| 2 | git reset --hard 当回滚 | 丢失历史 |
| 3 | 为凑分堆冗余规则 | 膨胀但不好用 |
| 4 | 跳过 test-prompts 直接评分 | Dim8 失真 |
| 5 | 一轮改多个维度 | 变量不可控 |
| 6 | 干跑比例 > 30% | Dim8 不可信 |
| 7 | 静默跳过异常 | 问题积累 |
| 8 | 忽视维度关联簇 | 优化策略失误 |

---

## 棘轮机制

**文本棘轮（Darwin）：** 编辑 SKILL.md → 独立评委打分 → 分高 keep / 分低 revert
**执行棘轮（ECC）：** 项目完成 → 执行审计 → 合规率升/降

---

## 参考来源

- darwin-skill v2.0: https://github.com/alchaincyf/darwin-skill
- SkillLens: https://arxiv.org/abs/2605.23899
- SkillOpt: https://arxiv.org/abs/2605.23904
- ECC: https://github.com/affaan-m/ECC
- 花叔文章: https://mp.weixin.qq.com/s/54pkSBImnc9mhEdOPf7EZw
