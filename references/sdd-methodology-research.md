# SDD（Spec-Driven Development）方法论研究

> 来源：邵猛 @shao__meng 推文 (2026-06-12)
> 参考：warpdotdev/common-skills

## 核心理念

**Agent 出错往往是需求理解偏差。** 解决办法是把规格当作 PR 的一部分，让队友和 Agent 都能对照同一份文档。

## 规格分两层

| 层级 | 文件 | 内容 | 受众 |
|------|------|------|------|
| 产品规格 | PRODUCT.md | 做什么 — 用户视角、用户故事、可验证的产品不变量 | 产品/用户/Agent |
| 技术规格 | TECH.md | 怎么做 — 架构思路、改哪些文件、实现时要注意什么 | 开发/Agent |

**存放位置：** `specs/<issue>/` 目录（clsh-project 适配为 `changes/<日期>-<描述>/`）

## 三个 Skills

| # | Skill | 产出 | 核心价值 |
|---|-------|------|---------|
| 1 | `/write-product-spec` | PRODUCT.md | 定义「无论什么情况都必须成立」的不变量 |
| 2 | `/write-tech-spec` | TECH.md | 给 Agent 的「施工图纸」 |
| 3 | `/validate-changes-match-specs` | 校验报告 | 实现后对照 spec 自查 |

## 五步流程

1. 写产品规格（/write-product-spec）
2. 写技术规格（/write-tech-spec）
3. 让 Agent 按规格实现
4. 规格一致性校验（/validate-changes-match-specs）
5. 用计算机操作做端到端验证

## 关键洞察

### Spec as Code
规格不是独立文档，而是代码的一部分。Reviewer 看代码时自然看到 spec，Agent 实现时有明确参照。

### 不变量驱动
产品不变量（Invariants）是「无论什么情况都必须成立」的规则：
- 可测试 — 可以直接转测试用例
- 可验证 — 计算机操作可以检查
- 稳定 — 用户故事可能变，但不变量相对稳定
- 无歧义 — "必须成立"没有模糊空间

### 一致性校验显式化
`/validate-changes-match-specs` 是独立步骤，不依赖人工 Review 发现所有偏移。

## 与 clsh-project 的对比

| 维度 | SDD | clsh-project |
|------|-----|--------------|
| 规格与代码关联 | 随 PR 提交，自然关联 | 独立管理在 raw/projects/ |
| Review 可见性 | 自然看到 spec | 需要额外步骤关联 |
| 偏移发现时机 | Review 阶段 | 实现后才发现 |
| 真机械门禁 | ❌ 无 | ✅ Gate Enforcer Plugin |
| 进程隔离 | ❌ 无 | ✅ C7 Fresh-Context Reviewer |
| 多维度调研 | ❌ 无 | ✅ 5 维度覆盖安全/合规 |
| 不变量驱动 | ⭐⭐⭐ 核心理念 | ⭐ 需要借鉴 |

## 整合方向

> 用 SDD 的"规格即代码"理念，结合 clsh-project 的"真机械门禁"机制，打造更强大的防偏移体系。
