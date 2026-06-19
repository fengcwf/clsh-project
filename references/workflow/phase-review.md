# Phase 7: Review Mode — Detailed Flow

## Overview

Review 是独立的质量验证阶段。Reviewer 必须：
- **独立于实现者**（不是同一个角色）
- **覆盖整个项目**（不仅是 src/）
- **使用标准格式**（severity + evidence + recommendation）

---

## 7-Step Review Process

```
Step 1: Prepare     → 收集所有 Phase 6 产出
Step 2: Scope       → 确定审查范围（整个项目）
Step 3: Audit       → 按 4 个维度逐一审查
Step 4: Classify    → 每个发现标注严重级别
Step 5: Recommend   → 每个发现给出修复建议
Step 6: Verify Fix  → 如有修复，验证修复后的状态
Step 7: Report      → 生成标准格式的 review report
```

### Step 1: Prepare — 收集产出

```
必须读取的文件：
  - tasks.md（所有任务描述）
  - 每个任务的 verification evidence
  - 每个任务的 diff 记录
  - constitution.md（验收标准）
  - proposal.md（设计意图）
  - analysis.md（分析发现）
```

### Step 2: Scope — 确定范围

**Review scope 必须覆盖整个项目，不仅仅是 src/：**

| 目录 | 检查内容 |
|-----|---------|
| `src/` | 代码质量、安全性、架构一致性 |
| `tests/` | 测试覆盖率、测试有效性、边界条件 |
| `config/` | 配置安全性、环境变量管理 |
| `docs/` | 文档准确性、与代码一致性 |
| `scripts/` | 脚本安全性、错误处理 |
| `.` (root) | README、package.json、.env 等 |

**Review scope 禁止事项：**
- ❌ 不能只审查 `src/` 而忽略其他目录
- ❌ 不能跳过测试文件
- ❌ 不能忽略配置文件中的安全问题
- ❌ 不能假设"没改动的文件不需要审查"

### Step 3: Audit — 4 维度审查

详见下方 "Audit Dimensions" 章节。

### Step 4: Classify — 严重级别

| 级别 | 定义 | 处理要求 |
|-----|------|---------|
| **Critical** | 阻断性问题：安全漏洞、数据丢失、系统崩溃 | 必须修复才能继续 |
| **Major** | 重要问题：功能缺陷、性能严重退化 | 应该修复，记录在案 |
| **Minor** | 次要问题：代码风格、小的优化 | 建议修复，不阻断 |
| **Suggestion** | 改进建议：更好的实现方式 | 可选，记录在案 |

### Step 5: Recommend — 修复建议

每个 finding 必须包含可执行的建议：

```
Finding: SQL injection in user.py:45
Recommendation: 使用 parameterized query：
  - 旧: cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
  + 新: cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
```

### Step 6: Verify Fix — 验证修复

对所有 critical 和 major 发现：
1. 记录修复前状态
2. 修复后重新检查
3. 验证修复没有引入新问题
4. 更新 finding 状态为 "resolved" 或 "open"

### Step 7: Report — 生成报告

使用标准输出格式（见下方）。

---

## Audit Dimensions

### 1. Spec Compliance（规格合规）

检查实现是否符合 constitution.md 中的约束。

| 检查项 | 方法 |
|-------|------|
| MUST 约束全部满足 | 逐条验证 constitution.md |
| 未添加未授权的依赖 | 对比 proposal.md 的依赖列表 |
| 未违反架构决策 | 检查 architecture.md 的组件边界 |
| 未超出 scope | 对比 tasks.md 的 scope 定义 |

### 2. Code Quality（代码质量）

| 检查项 | 方法 |
|-------|------|
| 无 Lint 错误 | 执行 `npm run lint` 或等效命令 |
| 单文件 < 300 行 | 统计每个文件行数 |
| 函数 < 50 行 | 统计每个函数行数 |
| 无重复代码 | grep 相似函数名和模式 |
| 有意义的命名 | 检查变量/函数命名一致性 |
| 错误处理完整 | 检查 try/catch、error 回调 |

### 3. Security（安全）

| 检查项 | 方法 |
|-------|------|
| 无 SQL 注入 | 检查所有数据库查询 |
| 无 XSS 漏洞 | 检查所有用户输入处理 |
| 无硬编码密钥 | grep `key=`, `secret=`, `password=` |
| 输入验证 | 检查所有 API 端点 |
| 依赖安全性 | `npm audit` 或等效 |
| 权限检查 | 检查认证/授权逻辑 |

### 4. Architecture（架构）

| 检查项 | 方法 |
|-------|------|
| 模块边界清晰 | 检查 import 关系图 |
| 依赖方向正确 | 不允许循环依赖 |
| 接口一致性 | 检查 API 返回格式 |
| 配置外置 | 检查硬编码的配置值 |
| 日志/监控 | 检查关键操作是否有日志 |

---

## Review Scope Rules

### 必须覆盖的范围

```
review-project/
├── src/           ← 必须审查
├── tests/         ← 必须审查（包括测试质量本身）
├── config/        ← 必须审查（安全+配置管理）
├── docs/          ← 必须审查（与代码一致性）
├── scripts/       ← 必须审查（安全+错误处理）
├── package.json   ← 必须审查（依赖+脚本）
├── README.md      ← 必须审查（文档准确性）
├── .env.example   ← 必须审查（环境变量文档）
└── .gitignore     ← 可选审查
```

### 审查规则

1. **整个项目**：review 必须覆盖项目的所有目录
2. **不是仅 src/**：很多安全和配置问题在 src/ 之外
3. **包括测试质量**：测试本身也需要审查（是否有效、是否覆盖边界）
4. **配置安全**：检查 .env、config 等文件中的敏感信息
5. **文档一致性**：README 和 docs 是否与实际代码一致

---

## Review Project Directory Structure

Reviewer 产出的目录结构必须符合：

```
review-report.md           ← 主报告
├── summary                ← 概要
├── findings/              ← 所有发现
│   ├── critical.md        ← Critical 级别发现
│   ├── major.md           ← Major 级别发现
│   ├── minor.md           ← Minor 级别发现
│   └── suggestions.md     ← 改进建议
├── evidence/              ← 证据截图/输出
│   ├── lint-output.txt
│   ├── test-results.txt
│   └── security-scan.txt
└── verification/          ← 验证记录
    ├── before-fix.md
    └── after-fix.md
```

**简化模式**：如果项目较小，可以合并为单文件 `review-report.md`，但必须包含所有分区内容。

---

## Output Format

### review-report.md 标准格式

```markdown
# Review Report — [Project Name]

## Summary
- Review Date: YYYY-MM-DD
- Reviewer: [独立角色]
- Scope: [覆盖的目录列表]
- Total Findings: N (Critical: X, Major: Y, Minor: Z, Suggestion: W)

## Critical Findings
### [F-001] Title
**File:** path/to/file.py:45
**Severity:** Critical
**Description:** [具体描述问题]
**Evidence:** [代码片段、输出截图等]
**Recommendation:** [具体的修复建议，包含代码示例]

## Major Findings
### [F-002] Title
...

## Minor Findings
### [F-003] Title
...

## Suggestions
### [F-004] Title
...

## Verification Results
| Finding | Status | Verified By |
|---------|--------|------------|
| F-001 | Resolved | [日期] |
| F-002 | Open | — |

## Conclusion
[总体评估：是否可以继续到 Phase 8]
```

### Finding 必填字段

| 字段 | 必填 | 说明 |
|-----|------|------|
| ID | ✅ | F-001, F-002... |
| Title | ✅ | 简洁描述 |
| File | ✅ | 文件路径 + 行号 |
| Severity | ✅ | Critical/Major/Minor/Suggestion |
| Description | ✅ | 详细描述 |
| Evidence | ✅ | 代码片段或输出 |
| Recommendation | ✅ | 可执行的修复建议 |

---

## Review Checklist Template

```markdown
# Review Checklist — [Project]

## Spec Compliance
- [ ] All MUST constraints from constitution.md are satisfied
- [ ] No unauthorized dependencies added
- [ ] Architecture boundaries respected
- [ ] Scope from tasks.md not exceeded

## Code Quality
- [ ] Lint passes with 0 errors
- [ ] No file > 300 lines
- [ ] No function > 50 lines
- [ ] Error handling complete
- [ ] Meaningful variable/function names
- [ ] No dead code

## Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Dependencies audit clean
- [ ] Auth/authz checks in place

## Architecture
- [ ] No circular dependencies
- [ ] Module boundaries clear
- [ ] API response format consistent
- [ ] Configuration externalized
- [ ] Logging present at key points

## Documentation
- [ ] README accurate and complete
- [ ] API docs match implementation
- [ ] Comments explain "why" not "what"
- [ ] CHANGELOG updated

## Testing
- [ ] Tests exist for all new features
- [ ] Tests cover edge cases
- [ ] Tests are independent (no order dependency)
- [ ] Test output clean (no warnings)
```

---

## Common Review Mistakes

| 错误 | 后果 | 正确做法 |
|-----|------|---------|
| Self-review | 盲点、偏见 | 独立 reviewer |
| 只看 src/ | 配置安全漏洞逃逸 | 覆盖整个项目 |
| 不给建议 | 发现无法修复 | 每个 finding 有 recommendation |
| 不分级 | 无法优先处理 | 标注 severity |
| 不 re-verify | 修复引入新问题 | 修复后重新检查 |
| 用 LLM 做自动 review | 理性化跳过检查 | 人工复核关键发现 |
