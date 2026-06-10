# Gate Enforcer Plugin — 真机械确认码门禁

**日期**: 2026-06-10
**状态**: ✅ 已实现（2026-06-10）
**根因**: workspace-remediation 项目 Phase 4/5 同时绕过检查
**实现计划**: `/mnt/unraid_data/Obsidian/raw/projects/workspace-remediation/changes/2026-06-10-remediation/gate-enforcer-implementation-plan.md`
**最终报告**: `/mnt/unraid_data/Obsidian/raw/projects/workspace-remediation/changes/2026-06-10-remediation/gate-enforcer-final-report.md`

---

## Phase Gate 分类（哪些 Phase 需要 Gate 脚本）

| Phase | 码来源 | Gate 类型 | 需要 Gate 脚本？ |
|-------|--------|----------|----------------|
| Phase 1 | 灵犀生成码，大佬输入 | 人是 Gate（大佬看内容才输入码） | ❌ |
| Phase 2 | 同上 | 同上 | ❌ |
| Phase 3 | 同上 | 同上 | ❌ |
| Phase 4 | 灵犀生成码，大佬输入 | LLM 是 Gate（可跳过检查直接给码） | ✅ gate-phase4.py |
| Phase 5 | 灵犀 review 后给码 | LLM 是 Gate（可不 review 就给码） | ✅ gate-phase5.py |
| Phase 6 | 灵犀 review tester 报告后给码 | LLM 是 Gate（可不 review 就给码） | ✅ gate-phase6.py |
| Phase 8 | 灵犀生成码，大佬输入 | LLM 是 Gate（可跳过检查直接给码） | ✅ gate-phase8.py |

**关键区分**：Phase 1-3 的 Gate 是**人**，LLM 无法伪造人的输入。Phase 4/5/6/8 的 Gate 是**灵犀**，灵犀可以跳过。

---

## 拦截机制

### Hook 签名（Hermes pre_tool_call）

```python
def enforce_gate(*, tool_name, args, **kwargs):
    # tool_name: "terminal" | "write_file" | "patch" | ...
    # args: dict（terminal 时 args["command"] 是命令字符串）
    # 返回 None = 放行，{"action": "block", "message": "..."} = 阻断
```

### 拦截规则

| 命令 | 拦截？ | 原因 |
|------|--------|------|
| `python3 -c "import secrets,string; ..."` | ✅ | 码生成模式 |
| `python3 ~/.hermes/scripts/gate-phase4.py /path/` | ❌ | gate 脚本本身 |
| `python3 ~/.hermes/scripts/phase4-mechanical-check.py /path/` | ❌ | 底层检查脚本 |
| `python3 -c "print('hello')"` | ❌ | 不匹配码生成模式 |
| `ls /path/` | ❌ | 普通命令 |

### 匹配模式

```python
CODE_GEN_PATTERNS = [
    re.compile(r"import\s+secrets.*import\s+string", re.DOTALL),
    re.compile(r"secrets\.choice.*ascii_uppercase", re.DOTALL),
    re.compile(r"string\.ascii_uppercase.*string\.digits", re.DOTALL),
]
GATE_SCRIPT_PATTERNS = [
    re.compile(r"gate-phase\d+\.py"),
    re.compile(r"phase4-mechanical-check\.py"),
]
```

---

## 完整执行流程

```
灵犀说"Phase 4 自检完成"
    ↓
灵犀调 terminal: python3 -c "import secrets,string; ..."
    ↓
pre_tool_call hook 触发
    ↓
(a) 匹配码生成模式？ YES
(b) ~/.hermes/gate-state/phase4-passed 存在？ NO
    ↓
BLOCK → "请先运行 gate-phase4.py"
    ↓
灵犀调 terminal: python3 ~/.hermes/scripts/gate-phase4.py <项目目录>
    ↓
hook: 匹配 gate 脚本？ YES → 放行
    ↓
gate-phase4.py:
  - 跑 phase4-mechanical-check.py 的所有检查
  - PASS → 生成码 + 写标记文件 + 输出 JSON
  - FAIL → 输出 JSON 错误报告，不出码
    ↓
灵犀再调 terminal: python3 -c "import secrets,string; ..."
    ↓
hook: 标记文件存在 → 放行 → 码生成成功
```

---

## 标记文件格式

路径：`~/.hermes/gate-state/phase4-passed`

```json
{
    "phase": "phase4",
    "project": "/mnt/unraid_data/Obsidian/raw/projects/<项目>",
    "code": "A3B7K9",
    "timestamp": 1718012345.67
}
```

---

## Gate 脚本清单

| 脚本 | 检查内容 | 标记文件 |
|------|---------|---------|
| gate-phase4.py | 文件存在性 + 关键词 + 行数 + 实现细节规范 | phase4-passed |
| gate-phase5.py | tasks.md skills 字段 + 角色标注 + 验收标准 + 行数 | phase5-passed |
| gate-phase6.py | tester 报告存在 + PASS/FAIL 判定 + 验证证据 | phase6-passed |
| gate-phase8.py | Phase 8 文档检查 | phase8-passed |

---

## 防作弊分析

| LLM 作弊手段 | 是否被阻断 | 原因 |
|-------------|-----------|------|
| 跳过脚本直接 `python3 -c` 编码 | ✅ 阻断 | hook 拦截 terminal code-gen |
| 用 `write_file` 直接写标记文件 | ⚠️ 可扩展 | 当前不拦截，可加规则 |
| 在回复文本中直接写 "确认码是 ABC123" | ❌ 不阻断 | hook 只能拦截工具调用 |
| 运行 gate 脚本但篡改输出 | ✅ 阻断 | 标记文件由脚本写入 |

**唯一漏洞**：LLM 在文本回复中直接编码（不调工具）。
**补丁**：确认模板要求码必须伴随脚本 JSON 输出。大佬复制码时检查 JSON 是否存在。

---

## Plugin 代码

### plugin.yaml

```yaml
name: gate-enforcer
version: "1.0.0"
description: "pre_tool_call hook: 阻断未过门禁的确认码生成"
author: 灵犀
provides_hooks:
  - pre_tool_call
```

### \_\_init\_\_.py

```python
"""Gate Enforcer — pre_tool_call hook: 阻断未过门禁的确认码生成

参考 GSD PreToolUse hook 模式：
- 在工具调用前拦截（pre_tool_call）
- 检查前置条件（gate-state 标记文件）
- 不满足 → block，LLM 无法绕过
"""

import json, logging, os, re
from pathlib import Path

logger = logging.getLogger("plugins.gate-enforcer")

GATE_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "gate-state"

CODE_GEN_PATTERNS = [
    re.compile(r"import\s+secrets.*import\s+string", re.DOTALL),
    re.compile(r"secrets\.choice.*ascii_uppercase", re.DOTALL),
    re.compile(r"string\.ascii_uppercase.*string\.digits", re.DOTALL),
]

GATE_SCRIPT_PATTERNS = [
    re.compile(r"gate-phase\d+\.py"),
    re.compile(r"phase4-mechanical-check\.py"),
]


def register(ctx):
    ctx.register_hook("pre_tool_call", enforce_gate)
    logger.info("Gate Enforcer registered pre_tool_call hook")


def _is_code_gen_command(cmd: str) -> bool:
    for pattern in GATE_SCRIPT_PATTERNS:
        if pattern.search(cmd):
            return False
    for pattern in CODE_GEN_PATTERNS:
        if pattern.search(cmd):
            return True
    return False


def _has_gate_marker() -> bool:
    if not GATE_DIR.exists():
        return False
    return any(GATE_DIR.glob("*-passed"))


def enforce_gate(*, tool_name, args, **kwargs):
    if tool_name != "terminal":
        return None
    cmd = args.get("command", "") if isinstance(args, dict) else ""
    if not cmd or not _is_code_gen_command(cmd):
        return None
    if _has_gate_marker():
        return None
    logger.warning("Gate Enforcer: blocking code generation — no gate marker")
    return {
        "action": "block",
        "message": (
            "⛔ 确认码生成被阻断：未找到门禁通过记录。\n\n"
            "请先运行门禁脚本：\n"
            "  Phase 4: python3 ~/.hermes/scripts/gate-phase4.py <项目目录>\n"
            "  Phase 5: python3 ~/.hermes/scripts/gate-phase5.py <项目目录>\n"
            "  Phase 6: python3 ~/.hermes/scripts/gate-phase6.py <项目目录>\n"
            "  Phase 8: python3 ~/.hermes/scripts/gate-phase8.py <项目目录>\n\n"
            "门禁脚本会检查文档合规性，通过后自动生成确认码并写入标记文件。"
        )
    }
```

### config.yaml 注册

```yaml
plugins:
  enabled:
    - gate-enforcer
```

---

## Pitfall: Python importlib 用于连字符文件名

gate-phase4.py 需要导入 `phase4-mechanical-check.py`，但 Python 的 `import` 不支持连字符文件名。必须用 `importlib.util`：

```python
import importlib.util
spec = importlib.util.spec_from_file_location(
    "phase4_mechanical_check",
    Path(__file__).parent / "phase4-mechanical-check.py"
)
phase4_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase4_check)
run_checks = phase4_check.run_checks
```

**不要用** `sys.path.insert + import` — 连字符文件名无法作为 Python 模块名。

---

## 与其他防偏离机制的协同

| 机制 | 作用域 | 与 Gate Enforcer 的关系 |
|------|--------|----------------------|
| Gate Enforcer | Phase 4/5/6/8 码生成 | 核心：物理阻断 |
| Anti-Rationalization Guard | 所有 Phase | 辅助：防止 LLM 创造"合理例外" |
| Fresh-Context C7 Reviewer | Phase 5/6/8 review | 辅助：不信任执行者报告 |
| Phase 边界上下文重载 | 所有 Phase | 辅助：防上下文漂移 |
| 验证证据模板 | 所有确认码 | 辅助：要求附命令输出 |

---

## 测试结果（2026-06-10）

| 测试 | 结果 |
|------|------|
| gate-phase4.py（workspace-remediation） | ✅ PASS |
| gate-phase5.py（workspace-remediation） | ✅ PASS |
| gate-phase6.py（workspace-remediation） | ✅ 正确 FAIL（无 tester 报告） |
| gate-phase8.py（workspace-remediation） | ✅ 正确 FAIL（无 diagnosis.md） |
| Plugin hook 加载 | ✅ |
| Plugin 阻断测试（无标记） | ✅ block |
| Plugin 放行测试（有标记） | ✅ allow |
| Plugin 普通命令测试 | ✅ 不拦截 |

**⚠️ 需要重启网关才能生效。** Plugin 在 config.yaml 中注册后，需要 `hermes gateway restart` 才会加载。
