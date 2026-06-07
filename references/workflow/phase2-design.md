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

**文件位置：** `raw/projects/<项目名>/changes/<变更名>/spikes/NNN-question/`

### ⛔ Spike 铁律
- **快速原型 ≠ 生产代码** — spike 代码写完就扔，不要"顺手合并"
- **每个 spike 独立目录** — 不互相干扰
- **有 PARTIAL 或 INVALIDATED 时** — 必须更新方案，不能假装没看到

### 🎨 设计 Prototype（UI 项目专用）

**来源：** Matt Pocock /prototype skill

**与 Spike 的区别：**
- Spike = 验证"能不能做"（技术可行性）
- Prototype = 验证"该怎么做"（设计方向/交互逻辑）

**触发条件：** Phase 2 方案涉及 UI 设计方向选择，且大佬无明确视觉参考。

**两种分支：**

| 分支 | 回答的问题 | 产出 |
|------|----------|------|
| **逻辑原型** | "这个状态机/数据模型感觉对吗？" | 可交互的终端 app |
| **UI 原型** | "这个页面应该长什么样？" | 同一页面内 2-3 个可切换的设计变体 |

**UI 原型规则：**
1. **一个 HTML 文件 + N 套 CSS 变体 + 切换 JS** — 不是 N 个独立页面
2. **一条命令运行** — `python3 -m http.server` 或直接打开 HTML
3. **从第一天标记为"一次性"** — 完成后删除或吸收进正式代码
4. **无持久化** — 状态在内存中
5. **放测试目录** — `/opt/Workspace/test/<项目名>/`，nginx :8088 服务
6. **发链接给大佬** — `https://wptest.cwf.fengcwf.cn:10086/<项目名>/<文件>.html`

**与 Phase 3 设计发散的关系：**
- Phase 2.5 Prototype = 快速探索多个截然不同的方向（可能只用于内部讨论）
- Phase 3 设计发散 = 确定方向后的精细 mockup（发飞书给大佬选择）
- 如果 Phase 2.5 已产出 UI 原型且大佬确认方向，Phase 3 可直接基于原型细化

---

## ⛔ Common Pitfalls（Phase 2 高频）

> 从 pitfalls/common.md 提取的 Phase 2 高频教训，避免额外查文件。

### #7 跳过 Phase 2.5 Spike

**规则：** 方案中存在技术不确定性时，必须进入 Phase 2.5 Spike 验证，不可直接跳到 Phase 3。

**触发条件（满足任一）：**
- 使用从未在项目中用过的框架/协议/库
- 性能要求可能无法满足
- 多方案技术路线差异大，无法凭经验判断
- 依赖第三方服务的稳定性/兼容性未知

**反例：** 选了一个"看起来能行"的方案直接写设计文档 → Phase 6 发现技术不可行 → 全部返工。
