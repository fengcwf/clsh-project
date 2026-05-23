# clsh-project — Phase 2+2.5: 方案设计与技术验证

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 2: 方案设计

**目标：** 提出多个技术方案，让大佬做选择题。

### 规则
- **提出 2-3 个方案** — 不要只给一个"推荐方案"
- **每个方案说清楚：** 优点、缺点、工作量估算
- **给出推荐理由**
- **用对比表格呈现**

### ⛔ 技术不确定性检查

如果方案中存在以下情况，**必须进入 Phase 2.5 Spike**，不可直接跳到 Phase 3：
- 使用从未在项目中用过的框架/协议/库
- 性能要求可能无法满足（需要基准测试验证）
- 多方案技术路线差异大，无法凭经验判断
- 依赖第三方服务的稳定性/兼容性未知

---

## Phase 2.5: Technical Spike（可选）

**目标：** 在写设计文档前验证技术可行性，降低设计返工风险。

**参考：** `spike` skill

### 何时触发（满足任一）
- Phase 2 的方案存在技术不确定性
- 新框架/新协议首次引入
- 性能/兼容性需要实际验证
- 大佬明确要求"先确认能不能做"

### 流程

```
1. 分解为 2-5 个独立可行性问题（Given/When/Then 格式）
2. 按风险排序，最高风险的 spike 先做
3. 每个 spike：研究 → 快速原型 → 裁决
4. 输出：VALIDATED / PARTIAL / INVALIDATED
5. 更新 Phase 2 方案
```

### 裁决格式

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked
- ...

### What didn't
- ...

### Surprises
- ...

### Recommendation for the real build
- ...
```

**文件位置：** `wiki/projects/<项目名>/changes/<变更名>/spikes/NNN-question/`

### ⛔ Spike 铁律
- **快速原型 ≠ 生产代码** — spike 代码写完就扔，不要"顺手合并"
- **每个 spike 独立目录** — 不互相干扰
- **有 PARTIAL 或 INVALIDATED 时** — 必须更新方案，不能假装没看到
