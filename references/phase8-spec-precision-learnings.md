# Phase 8 Spec 精度优化 — 完整学习记录

> 来源：2026-06-09 Workspace 优化项目复盘
> 借鉴：Superpowers brainstorming/writing-plans + gstack /design-consultation + Ralph Loop backpressure

## 一、问题根因

### Round 3 Spec → Round 4 反馈的 Gap

| Bug | Round 3 Spec | Round 4 实际要 | Gap 类型 |
|-----|-------------|---------------|---------|
| 卡片背景 | `var(--surface-solid)` 浅色 | `rgba(25,25,25,0.65)` 暗色毛玻璃 | 设计假设错误 |
| 右键菜单 | 完整组件定义 | 代码不工作（timing） | 技术验证缺失 |
| 配置面板 | ASCII 布局图 | "太丑了" | 视觉精度不够 |
| z-index 遮挡 | `z-index: 1000` | Round 4 又报 | 验证不充分 |

### 三类根因

1. **设计假设不验证** — 灵犀看到"卡片背景不统一"→假设用工作台标准样式→实际用户要暗色毛玻璃
2. **技术实现不验证** — spec 描述了 WHAT，没验证实际能不能跑
3. **视觉描述不精确** — "Homarr 风格"无法传达视觉质量

## 二、框架对比

| 框架 | 机制 | clsh-project 对应 |
|------|------|-----------------|
| Superpowers brainstorming | spec 只写设计决策，不写代码 | Phase 3 proposal 只写设计决策 ✅ |
| Superpowers writing-plans | plan 写完整代码，每步都有 | Phase 5 派 coder 写 tasks ✅ |
| Superpowers spec-reviewer | 自动审查 Completeness/Spec Alignment/Decomposition/Buildability | C7 Buildability review ✅ |
| gstack /design-consultation | 设计决策必须过专家审查 | Phase 8 设计方向确认 ✅ |
| Ralph Loop backpressure | 无客观证据不允许标记完成 | G4 phase8-spec-check.py ✅ |

## 三、Superpowers Plan Review 四维检查

| 维度 | 检查内容 | clsh-project 落地 |
|------|---------|-----------------|
| **Completeness** | TODO/placeholder/不完整 task | C7 Buildability 检查 |
| **Spec Alignment** | plan 覆盖 spec 需求，无 scope creep | C7 Spec Coverage 检查 |
| **Task Decomposition** | task 边界清晰，步骤可执行 | C7 粒度检查（2-5分钟） |
| **Buildability** | 工程师能照做而不卡住 | C7 Buildability 检查 |

**校准原则：** 只标记会导致实现出问题的问题，不标记措辞/风格/锦上添花的建议。

## 四、落地产物

| 产物 | 路径 | 用途 |
|------|------|------|
| Bugfix spec 模板 | `raw/projects/clsh-project/templates/bugfix-spec-template.md` | Phase 8 结构化 spec |
| 门禁脚本 | `~/.hermes/scripts/phase8-spec-check.py` | 机械检查必填节 + 设计方向非"待确认" |
| C0 Convention | SKILL.md Layer 2 | 灵犀只记录不分析 |
| C7 Convention | SKILL.md Layer 2 | 流程合规 + Buildability review |
| G4 Gate | SKILL.md Layer 1 | Phase 8 spec 门禁 |

## 五、关键教训

1. **灵犀做决策 = 单点故障** — 灵犀假设浅色主题→coder 照做→用户不满意→多轮修复
2. **spec 不精确 ≠ spec 不详细** — Round 3 spec 很详细，但方向错了
3. **验证比 spec 更重要** — z-index 修了但没浏览器验证→Round 4 又报
4. **coder profile 不该有 vision** — task body 引用图片→vision_analyze 34 分钟超时
5. **模板强制 > LLM 自觉** — bugfix-spec-template 强制填设计方向，脚本拦截"待确认"
