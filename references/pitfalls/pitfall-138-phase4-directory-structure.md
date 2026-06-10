# Pitfall #138: Phase 4 目录结构必须符合脚本预期

**触发条件**：Phase 4 机械检查 FAIL，报告"文件不存在"但文件实际在项目根目录

**根因**：`phase4-mechanical-check.py` 用 glob 模式查找文件：
- `changes/*/conversation.md`（不是根目录的 `conversation.md`）
- `changes/*/proposal.md`
- `changes/*/tasks.md`
- `source-of-truth/constitution.md`
- `overview.md`（根目录，这个没问题）

**错误示例**：
```
workspace-review/
├── overview.md          ← ✅ 脚本能找到
├── conversation.md      ← ❌ 脚本找不到（期望 changes/*/conversation.md）
├── proposal.md          ← ❌ 脚本找不到
├── tasks.md             ← ❌ 脚本找不到
└── constitution.md      ← ❌ 脚本找不到（期望 source-of-truth/constitution.md）
```

**正确结构**：
```
workspace-review/
├── overview.md
├── changes/
│   └── 2026-MM-DD-<topic>/
│       ├── conversation.md
│       ├── proposal.md
│       └── tasks.md
└── source-of-truth/
    └── constitution.md
```

**各文件必需关键词**（脚本检查）：
- overview.md: `状态`, `进度表`
- conversation.md: `需求`, `决策`
- proposal.md: `技术方案`, `不在范围内`
- constitution.md: `约束`, `禁止`, `验收标准`
- tasks.md: `验收标准`, `不在范围内`

**各文件行数上限**：
- overview.md: ≤60 行
- conversation.md: ≤60 行
- proposal.md: ≤70 行
- constitution.md: ≤60 行
- tasks.md: ≤80 行

**constitution.md 额外要求**（实现细节规范检查）：
必须包含 `## 实现细节规范` 节，且内容含"编码"关键词。否则：
```
❌ 实现细节节: 缺少实现细节规范节
❌ 编码规范
```

**铁律**：Phase 4 FAIL = 必须修复目录结构和关键词，不能以"项目类型不同"为由绕过。
