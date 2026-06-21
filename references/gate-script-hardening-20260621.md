# Gate 脚本加固记录 (2026-06-21)

## 背景

9 轮 review（mimo + DeepSeek 双模型）发现 gate 脚本存在安全和质量问题。以下为已实施的加固措施。

## 已实施加固

### 1. 确认码熵增强 (gate_utils.py)

| 项目 | 加固前 | 加固后 |
|------|--------|--------|
| 码长度 | 6 位 hex (24-bit) | 10 位 hex (40-bit) |
| 碰撞概率 | 1/16M | 1/1T |

### 2. Marker HMAC 签名 (gate_utils.py)

- 使用机器绑定密钥 (`platform.node() + os.getuid()`) 派生 HMAC-SHA256
- 签名覆盖 marker 全部字段（排除 hmac 自身）
- 新增 `verify_marker()` 函数用于验证
- 防止 marker 文件被伪造或跨机器复用

### 3. Slug 碰撞修复 (gate_utils.py)

| 项目 | 加固前 | 加固后 |
|------|--------|--------|
| 算法 | `re.sub(r"[^a-zA-Z0-9_-]", "_", path)` | `sha256(path)[:16]` |
| 碰撞风险 | `/a_b/c` ↔ `/a/b/c` 可能碰撞 | 不同路径必定不同 slug |

### 4. Review 报告质量门禁 (gate-phase7.py)

新增两个 FAIL 级检查（非 WARN）：

- **Severity 标签**：报告必须包含 Critical/Major/Minor/Suggestion 至少 1 个
- **Evidence 引用**：报告必须包含 `[file:line]` 格式引用 ≥3 个

MIN_DIMENSIONS 从 3 提升到 5。

**设计决策：** 使用 FAIL 而非 WARN，因为 R4 DeepSeek 魔鬼代言人指出"alert fatigue"——WARN 会被忽略。如果 severity+evidence 重要到要检查，就不应该是 WARN。

### 5. 关键词语义化 (gate-phase4.py)

| 文件 | 加固前 | 加固后 |
|------|--------|--------|
| overview.md | `\w{4,}` | `(?:goal\|purpose\|scope\|background\|目标\|范围\|背景)` |
| conversation.md | `\w{4,}` | `(?:requirement\|user.story\|need\|需求\|用户\|场景)` |
| proposal.md | `\w{4,}` | `(?:approach\|option\|trade.off\|方案\|选型\|权衡)` |
| constitution.md | `\w{4,}` | `(?:constraint\|must.not\|forbidden\|验收\|约束\|禁止)` |

支持中英文双语关键词。

### 6. Coverage Summary 输出 (gate-phase5.py)

gate-phase5.py 的 JSON 输出新增 `meta.coverage` 字段：

```json
{
  "gate": "phase5",
  "passed": true,
  "meta": {
    "coverage": {
      "total_stories": 8,
      "covered": 7,
      "uncovered": ["US-3"]
    }
  }
}
```

`output_result()` 函数新增 `meta` 参数支持。

## 未实施但记录的发现

### R5 Critical 发现（待处理）

| 问题 | 严重性 | 状态 |
|------|--------|------|
| Phase 1-3 无 gate 脚本 | HIGH | 未实施（改动范围大） |
| Gate 间无状态链验证 | HIGH | 未实施（所有 gate 脚本需改） |
| 确认码无 TTL 过期机制 | MEDIUM | 未实施 |
| Phase 6 PASS 检测误匹配 | HIGH | 未实施 |

### R2 架构发现

- G1/Pitfall#8/#7 三重规则重复
- C7/Pitfall#4/禁止行为表三重重复
- Phase 8 无硬性迭代上限
