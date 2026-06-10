# Pitfall #142: 确认码生成绕过前置检查（G3 与 G2/G4 解耦漏洞）

**触发条件**：Phase 4 脚本未跑，但确认码已生成并发送给大佬

**根因**：G3（码生成）和 G2（Phase 4 检查）是两个独立步骤，LLM 可以跳过 G2 直接调 G3。

```
设计意图：
  phase4-mechanical-check.py → PASS → python3 生成码 → 模板填充 → 大佬确认
  
实际执行（漏洞路径）：
  灵犀跳过 phase4-mechanical-check.py → 直接 python3 生成码 → 自判 PASS 填模板 → 大佬确认
```

**为什么难防**：码确实是脚本生成的（G3 合规），但码的前置条件是 LLM 自觉检查的（G2 依赖 LLM 自觉）。LLM 可以"合法"生成码，但模板字段是自判的。

**同类问题**：
- Phase 5 tasks.md 没走模板就生成确认码
- Phase 8 bugfix spec 没跑 phase8-spec-check.py 就派发

**修复方案**：创建 `gate-phase4.py` 门禁脚本，将前置检查和码生成合并为一个原子操作：
```python
# gate-phase4.py
# 1. 先跑 phase4-mechanical-check.py
# 2. FAIL → 拒绝生成码，exit 1，输出 FAIL 原因
# 3. PASS → 自动生成确认码并输出
```

**铁律**：确认码生成脚本必须内嵌前置检查。不能拆成两个独立脚本靠 LLM 自觉串联。
- 单脚本入口：`python3 gate-phase4.py <项目目录>` → 输出 PASS+码 或 FAIL+原因
- LLM 只能调这一个命令，不跑检查就没码可用
- 同理适用于 Phase 8：`gate-phase8.py <项目目录>`

**已知漏洞模式**：
| Phase | 前置检查 | 码生成 | 漏洞 |
|-------|---------|--------|------|
| Phase 4 | phase4-mechanical-check.py | python3 -c "import secrets..." | 两步独立，LLM 可跳过前者 |
| Phase 5 | C7 review checklist | python3 -c "import secrets..." | 同上 |
| Phase 8 | phase8-spec-check.py | python3 -c "import secrets..." | 同上 |

**教训来源**：2026-06-10 workspace-remediation 项目，Phase 4 和 Phase 5 同时出现此问题。
