# Kanban 运维教训（2026-06-07）

## 1. Profile toolset 缺失导致 worker 静默失败

**现象：** kanban worker 启动后 60s 内退出，kanban 报 `protocol violation`（rc=0 但没调 kanban_complete）。

**根因排查路径：**
1. `hermes kanban runs <task_id>` → 看 outcome 是否为 `crashed`
2. 检查 error 信息：`worker exited cleanly (rc=0) without calling kanban_complete or kanban_block`
3. 对比能正常工作的 profile 的 toolsets：
   ```bash
   cat /root/.hermes/profiles/<profile>/config.yaml | grep -A10 "toolsets:"
   ```
4. 确认缺失的 toolset

**实测案例：**
- tester profile toolsets: `terminal, file, web, code_execution, skills, todo`
- artist profile toolsets: `terminal, file, browser, image_gen, vision, skills, todo`
- tester 缺少 `browser` + `vision` → 所有浏览器验证任务 1 分钟 crash
- 连续 4 个 tester 任务全部 failed，累计浪费 ~20 分钟 + 4 次迭代

**修复：**
```yaml
# /root/.hermes/profiles/<profile>/config.yaml
toolsets:
- terminal
- file
- browser    # UI 验证必须
- vision     # 截图分析必须
- web
- skills
- todo
```

**铁律：** 派发前验证 assignee profile 的 toolsets 是否覆盖任务需求。

| 任务类型 | 必需 toolsets |
|---------|-------------|
| UI 验证（浏览器截图） | browser, vision |
| 代码修改 | terminal, file |
| API 测试 | terminal, web |
| 文件操作 | file |

---

## 2. Kanban watchdog 脚本 bug

**Bug 1: `--status in_progress` 无效**
- kanban 状态名是 `running` 不是 `in_progress`
- `hermes kanban list --status in_progress` 返回空列表
- 脚本以为没有 running 任务 → 立即 `pause_self()`

**Bug 2: `hermes cronjob` 不存在**
- 正确命令是 `hermes cron`
- `pause_self()` 中调用 `hermes cronjob pause <id>` → 命令不存在
- 但 exit code 为 0（help 输出不报错）→ 脚本认为暂停成功

**组合效应：** 脚本每 5 分钟运行 → 查不到 running 任务 → 尝试暂停自身 → 暂停失败但 stdout 为空 → cron 报 "ok" → 用户以为 watchdog 在工作

**修复后脚本关键变更：**
```python
# 查询用 running 不是 in_progress
raw = run_cmd(["hermes", "kanban", "list", "--status", "running", "--json"])

# 暂停用 hermes cron 不是 hermes cronjob
run_cmd(["hermes", "cron", "pause", cron_id])

# 缓存 cron ID 避免每次查找
CRON_ID_FILE = os.path.join(SCRIPT_DIR, ".kanban-watchdog-cron-id")
```

---

## 3. 备份脚本超时

**现象：** `hermes-weekly-backup` cron 报 `Script timed out after 120s`

**根因：** rsync profiles 目录 2.4GB（含 kanban 临时工作区 `home/` `sessions/` `lsp/` `bin/` `logs/`）

**修复：** 排除 kanban 临时目录
```bash
rsync -a --quiet \
  --exclude='home/' \
  --exclude='sessions/' \
  --exclude='lsp/' \
  --exclude='bin/' \
  --exclude='logs/' \
  ~/.hermes/profiles/ "$BACKUP_DIR/hermes/profiles/"
```

**效果：** 2.4GB → 442MB 压缩包，120s → 60s

---

## 4. Kanban scratch workspace 是临时目录（2026-06-07 教训）

**现象：** kanban worker 任务标记 done，但产出文件丢失。

**根因：** kanban scratch workspace（`/root/.hermes/kanban/workspaces/<task_id>/`）是临时目录，任务完成后被清理。worker 写入 scratch 的代码文件不会持久化到实际项目目录。

**铁律：产出持久文件的任务不用 kanban scratch，用 delegate_task。**

| 任务类型 | 产出物 | 推荐执行器 |
|---------|--------|-----------|
| 代码生成（创建新文件） | 持久化源码文件 | **delegate_task** |
| 代码修改（patch 现有文件） | 修改现有文件 | kanban（workdir 指向项目目录） |
| 纯推理/分析 | 文本 summary | delegate_task |
| 测试验证 | 无文件产出 | kanban |

---

## 5. `max_in_progress_per_profile` 需要 gateway restart（2026-06-07 教训）

**现象：** 设置 `kanban.max_in_progress_per_profile: 1` 后，kanban daemon 仍然同时派发多个任务。

**根因：** `dispatch_in_gateway: true` → kanban daemon 运行在 gateway 进程内 → config 变更需要 gateway restart 才能生效。

**铁律：** 修改 kanban 相关 config 后必须重启 gateway。

---

## 6. delegate_task vs kanban 决策树（2026-06-07 总结）

```
任务需要产出持久文件？
├── YES → delegate_task（子 agent 直接写项目目录）
│   ├── 代码生成（新建文件）
│   ├── 大型重构（多文件修改）
│   └── 配置变更（修改 server.mjs 等）
└── NO → kanban
    ├── 测试验证（无文件产出）
    ├── 纯推理任务
    └── 修改现有文件（需 workdir）
```

---

## 7. `hermes cron resume` 对不存在的 cron 静默成功（2026-06-07 教训）

**现象：** `hermes cron resume 1d04104d3ca9` 报 "Resumed job: kanban-watchdog"，但 `hermes cron list` 中无此 cron。

**根因：** `hermes cron resume` 对不存在的 cron ID 不报错，输出 "Resumed" 但实际未创建任何任务。

**组合效应：**
1. 用户派活 → 灵犀调用 `hermes cron resume <id>` → 报 "Resumed" → 灵犀认为 watchdog 已启用
2. 实际 watchdog 不存在 → 任务完成时无通知 → 用户等了 20 分钟没收到消息
3. `hermes kanban notify-subscribe` 同样可能不持久化 → 订阅也丢失

**验证方法：**
```bash
# 派活后必须验证 watchdog 存在
hermes cron list | grep -i watchdog
# 如果不存在，创建新的
hermes cron create --name "kanban-watchdog" --schedule "*/5 * * * *" \
  --script kanban-watchdog.sh --no-agent
```

**铁律：** `hermes cron resume` 的输出不可信。必须 `hermes cron list | grep <name>` 验证实际存在。
