# Pitfall #139: C8 --skill 注入必须存在于 assignee profile

**触发条件**：kanban 卡创建后 worker 连续 crash，日志显示 `Error: Unknown skill(s): XXX`

**根因**：`hermes kanban create --skill <name>` 注入的 skill 必须存在于 assignee profile 的 skills 目录。default profile 有但 tester/coder profile 没有的 skill 会导致 worker 启动失败。

**诊断**：
```bash
# 查看 crash 原因
hermes kanban log <task-id> 2>&1 | tail -5
# 输出: Error: Unknown skill(s): code-review-and-quality

# 检查 skill 是否在 assignee profile
ls /root/.hermes/profiles/<assignee>/skills/<category>/<skill-name>/
```

**修复**：
```bash
# 从 default profile 复制到 assignee profile
cp -r /root/.hermes/skills/<category>/<skill-name> \
      /root/.hermes/profiles/<assignee>/skills/<category>/

# 重新激活 blocked 卡
hermes kanban unblock <task-id>
```

**预防**：kanban create 前检查 skill 存在性：
```bash
# 验证命令（在 create 前跑）
for skill in code-review-and-quality systematic-debugging; do
  if [ ! -d "/root/.hermes/profiles/tester/skills/*/$skill" ]; then
    echo "MISSING: $skill in tester profile"
  fi
done
```

**常见 skill 映射**（2026-06-10 确认）：
| 角色 | --skill 参数 | default profile | tester profile | coder profile |
|------|-------------|-----------------|----------------|---------------|
| tester | code-review-and-quality | ✅ | ❌ 需复制 | — |
| tester | systematic-debugging | ✅ | ✅ | — |
| coder | test-driven-development | ✅ | — | ❌ 需复制 |
| coder | incremental-implementation | ✅ | — | ❌ 需复制 |

**铁律**：`hermes kanban create --skill` 前必须确认 skill 存在于 assignee profile。blocked 卡必须先修根因再 unblock。
