# clsh-project — LLM Review 指南

> **⚠️ LLM 必读**：review clsh-project skill 或执行 clsh-project 流程前，必须先读本文档。
> 本文档描述了 SKILL.md 中不明显但关键的机制。

---

## 1. gate-enforcer 插件（八层机械门禁）

**位置：** `~/.hermes/plugins/gate-enforcer/`

**不是 SKILL.md 的规则，是代码级强制拦截。** LLM 无法绕过。

| Layer | 拦截什么 | 触发条件 |
|-------|---------|---------|
| L1 | 确认码伪造 | terminal 中出现 secrets.choice 模式 |
| L2 | 未跑 gate-workflow.py 就写项目文件 | write_file/patch/terminal 写操作 |
| L3 | Phase 乱序 + HMAC 验证 | gate-phaseN.py 的前置 Phase 未完成或 HMAC 无效 |
| L4 | delegate_task 缺少 toolsets 或含 terminal | clsh-project 项目中的 delegate_task 调用 |
| L5 | Phase 0 未完成就写 PRODUCT.md | write_file/patch 对 PRODUCT.md |
| L6 | Phase 加载拦截 | 必须先加载 Phase 指令才能执行操作 |
| L7 | GATE_DIR 写入拦截 | 直接 write_file/patch/terminal 写入 gate-state 目录 |
| L8 | 环境变量劫持 + execute_code 写入拦截 | 设置 GATE_SECRET/GATE_DIR/HERMES_HOME 或 execute_code 写 gate-state |

**关键：** Layer 2-8 只在存在 clsh-project 项目（gate-state 中有 phase marker）时激活。普通工作不受影响。

---

## 2. 两步确认码流程（v6.0 新增）

**gate-phaseN.py 现在分两步：**

```
步骤 1: python3 gate-phaseN.py <project_dir>
        → 检查通过 → 写 .pending 文件（含 code）→ 输出确认码
        → ⚠️ 不写 marker！gate-enforcer 会拦截后续 Phase。

步骤 2: python3 gate-phaseN.py <project_dir> --verify <code>
        → 验证码正确 → 写正式 marker（含 HMAC）→ 删除 .pending
        → ✅ gate-enforcer 放行后续 Phase。
```

**LLM 必须：**
1. 运行 gate-phaseN.py 获取确认码
2. 将确认码展示给用户
3. 等待用户回码
4. 运行 `gate-phaseN.py <dir> --verify <code>`
5. 确认 marker 写入成功

**禁止：**
- 直接 read_file .pending 文件获取码（虽然技术上可行，但违反流程设计）
- 不等用户确认就调用 --verify
- 跳过 --verify 直接进入下一 Phase

---

## 3. subagent 盲区

**已知设计缺陷（2026-06-23 记录，2026-07-01 L7/L8 部分修复）：**

- gate-enforcer 的 `pre_tool_call` hook 只监控当前进程的工具调用
- `delegate_task` 子 agent 在独立上下文中运行，其 `write_file`/`patch` 不受 L2 拦截
- **L4 可以拦截父 agent 的 delegate_task 调用**（检查 toolsets），但子 agent 内部的操作不受控
- **L7 拦截对 GATE_DIR 的直接写入**（包括 terminal/write_file/patch）
- **L8 拦截 execute_code 中的 gate-state 写入**

**缓解措施：**
- L4 强制 delegate_task 指定 toolsets（不含 terminal）
- L7 阻止对 gate-state 目录的直接文件写入
- L8 阻止通过 execute_code 绕过
- tester profile 已移除 terminal 和 code_execution（物理限制）
- gate-phase6 Check 6 验证 conversation.md 中 tester 的 toolsets

---

## 4. Phase 6 完整流程（不是只检查关键词）

**正确流程：**

```
tasks.md → kanban/delegate_task 派发 → coder 执行 → tester 验证 → coordinator review → Phase 7
```

**gate-phase6 检查 6 项：**
1. Dispatch evidence（conversation.md 中有派发证据）
2. Skill injection（注入了正确的 skills）
3. Level dispatch（符合 env Level A/B/C）
4. Tester report（tester-report.md 存在 + PASS/FAIL + 证据）
5. **Coordinator review**（灵犀 review 了 tester 结果）
6. **Toolset constraint**（tester 的 toolsets 不含 terminal）

---

## 5. Profile 工具隔离

| Profile | toolsets | 说明 |
|---------|----------|------|
| tester | file, browser, vision, web, skills, todo | **无 terminal、无 code_execution** |
| coder | terminal, file, code_execution, skills, todo | 无 vision（防超时） |
| artist | browser, vision, file, image_gen, skills, todo | 无 terminal |

**机制：** profile config.yaml 的 toolsets 是框架级限制。不在列表中的工具 schema 不发给 LLM，模型不知道这些工具存在。

---

## 6. HMAC 密钥管理（v6.0 新增）

- **新密钥**：首次运行时自动生成随机 32 字节密钥，持久化到 `~/.hermes/gate-state/.hmac_key`
- **旧密钥兼容**：验证时先尝试新密钥，再尝试旧密钥（hostname+uid）
- **GATE_SECRET 环境变量**：仍可覆盖（用于 CI/testing），但 L8 会阻止运行时修改
- **确认码**：8 位大写 hex（32-bit entropy）

---

## 7. 确认码格式

- **8 位大写 hex 字母+数字**（32-bit entropy，非安全用途）
- **TTL 30 分钟**（过期的码 marker HMAC 仍有效，视为"expired but valid"）
- 输出带 `📋 确认码（复制用）: XXXXXXXX` 格式，方便用户复制

---

## 8. 模板索引

| 模板 | 用途 | Phase |
|------|------|-------|
| product-md-template.md | 产品规格 | 1 |
| tech-md-template.md | 技术规格 | 2 |
| proposal-md-template.md | 设计提案 | 3 |
| constitution-template.md | 项目宪法 | 3 |
| tasks-template.md | 任务清单 | 5 |
| overview-template.md | 项目概览 | 4 |
| dispatch-record-template.md | 派发记录 | 6 |
| tester-report-template.md | 测试报告 | 6 |
| phase-confirmations.md | 确认格式 | 全部 |

---

## 9. 已知缺陷

| # | 缺陷 | 状态 |
|---|------|------|
| 1 | subagent 内部操作部分不受 gate-enforcer 拦截 | L7/L8 部分缓解 |
| 2 | gate-phase6 的检查是文本匹配，不验证 kanban DB 状态 | 待修复 |
| 3 | Phase 0-2 没有 scout 派发做技术调研 | 待实施 |
| 4 | delegation.default_toolsets 是死配置（已从代码移除） | 不可修复 |
