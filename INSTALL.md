# 安装指南 / Installation Guide

## 前置条件 / Prerequisites

| 依赖 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.8+ | 门禁脚本运行环境 |
| Hermes Agent | — | AI Agent 运行平台（delegate_task 支持） |
| Git | — | 克隆仓库 |

## 步骤 1：环境自检 / Step 1: Environment Check

```bash
cd ~/.hermes/skills/clsh-project
python3 scripts/env-check.py
```

输出示例：
```
============================================================
  clsh-project Environment Check
============================================================

  ✅ python3                    (v3.11.x)
  ✅ terminal
  ✅ file_ops
  ✅ hermes_agent
  ⚠️  kanban                     → Falls back to delegate_task
  ❌ obsidian_vault              → Optional. Falls back to local docs/
  ❌ gate_enforcer_plugin        → Optional. Physical block on gate fail.

  Capability Level: B — Standard capability
```

**根据输出的能力等级，决定后续配置。**

## 步骤 2：配置 config.json / Step 2: Configure

```bash
cp config.example.json config.json
```

编辑 `config.json`，根据 env-check 结果调整：

| 配置项 | 说明 | Level A/B/C 适配 |
|--------|------|-----------------|
| `project_docs_dir` | 项目文档存储路径 | 所有等级 |
| `level` | 能力等级（`auto`/`A`/`B`/`C`） | `auto` 推荐 |
| `confirm_code_method` | 确认码生成方式（`hash`） | 所有等级 |
| `features.kanban` | kanban 路径（如有） | Level A |
| `features.gate_enforcer_plugin` | 启用物理阻断 | Level A |

## 步骤 3：设置项目文档目录 / Step 3: Project Docs Directory

```bash
# 根据 config.json 中 project_docs_dir 创建目录
mkdir -p project-docs
```

确认目录可写：
```bash
touch project-docs/.test && rm project-docs/.test && echo "✅ OK"
```

## 步骤 4：验证门禁脚本 / Step 4: Verify Gate Scripts

```bash
# 测试 gate_utils.py
python3 -c "from scripts.gate_utils import *; print('✅ gate_utils loaded')"

# 测试各 gate 脚本语法
python3 -m py_compile scripts/gate-phase4.py
python3 -m py_compile scripts/gate-phase5.py
python3 -m py_compile scripts/gate-phase6.py
python3 -m py_compile scripts/gate-phase7.py
python3 -m py_compile scripts/gate-phase8.py

echo "✅ All gate scripts compile OK"
```

## 能力等级详情 / Capability Level Details

### Level A — 完整 / Full
- **依赖：** kanban + gate-enforcer plugin
- **功能：** 全功能任务派发（含 skill 注入）+ 机械门禁 + 物理阻断（代码生成被门禁拦截）
- **场景：** 生产环境，完整开发团队

### Level B — 标准 / Standard
- **依赖：** delegate_task（Hermes Agent）
- **功能：** 核心流程完整（子任务派发 + 机械门禁），无物理阻断
- **场景：** 日常开发，个人项目

### Level C — 轻量 / Lite
- **依赖：** 仅 prompt 约束
- **功能：** 退化为 Superpowers 级防偏离，无脚本门禁
- **场景：** 快速原型，轻量需求

## 故障排除 / Troubleshooting

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `env-check.py` 报 `UNAVAILABLE` | 缺少 Python 3.8+ 或 Hermes | 安装 Python 3.8+，确认 Hermes 可用 |
| `gate-phase4.py` 报错 | 目录结构不符合预期 | 按 Phase 顺序执行，确保文档先于代码 |
| `config.json` 读取失败 | JSON 格式错误 | 用 `python3 -m json.tool config.json` 验证 |
| 门禁脚本 `PASS` 但流程异常 | 确认码未正确输入 | 每次都跑 gate 脚本获取新码，不复用旧码 |
| Level 降级 | kanban/gate-enforcer 缺失 | 检查 `~/.hermes/config.yaml` 配置 |

## 下一步 / Next Steps

安装完成后，通过以下方式触发工作流：

1. 在 Hermes 中发送 `/clsh-project` 或 `/cp`
2. 说「我要做一个 XXX」
3. 按 Phase 顺序执行，每阶段用门禁脚本验证
