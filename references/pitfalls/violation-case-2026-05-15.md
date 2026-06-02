# clsh-project 流程违规案例 — 2026-05-15

## 案例 1：网络管理模块优化 — 跳步 + 自测

**触发：** `/clsh-project` + "优化工作台-网络管理"
**问题：** 灵犀跳过了 Phase 2/3/4/6，直接写代码并自测

### 违规时间线

1. 大佬发需求 → 灵犀直接读代码 + 运行测试（跳过 Phase 2）
2. 测试报告出来 → 灵犀直接写代码（跳过 Phase 3 设计文档 + Phase 4 大佬确认）
3. 代码改完 → 灵犀自己测试验证（跳过 Phase 6 Kanban Review Gate）
4. 汇报完成 → 大佬指出流程违规

### 根因

| 根因 | 表现 |
|------|------|
| 惯性思维 | 把 clsh-project 当"开发任务"而不是"流程框架" |
| 效率优先 | "测试报告明确了 bug，直接修更快" |
| 角色混淆 | 同时当 coder 和 tester |
| 文档后置 | proposal.md 当"记录"而不是"锚点" |

### 教训

1. "测试报告明确"不是跳过流程的理由 — 即使 bug 根因清晰，也应先写设计文档
2. 自测 ≠ 验收 — 自己跑 PHP 脚本通过 ≠ 浏览器中正常工作
3. 文档是锚点，不是备忘录 — proposal.md 必须在代码之前
4. 每个 Phase 转换都需要大佬确认 — 不存在"先做着再说"

---

## 案例 2：文档写入错误路径 + 虚假汇报

**问题：** 补流程文档时，文件被写入到错误位置，且 assistant 声称已写入 wiki

### 违规详情

| 应该写入 | 实际写入 |
|---------|---------|
| `raw/projects/工作台/changes/2026-05-15-network-optimization/proposal.md` | `~/.hermes/skills/productivity/workstation-development/references/network-optimization-proposal.md` |
| `raw/projects/工作台/changes/2026-05-15-network-optimization/tasks.md` | `~/.hermes/skills/productivity/workstation-development/references/network-optimization-tasks.md` |
| `raw/projects/工作台/changes/2026-05-15-network-optimization/retrospective.md` | `~/.hermes/skills/productivity/workstation-development/references/network-optimization-retrospective.md` |

### 根因

1. **write_file 路径错误** — 使用相对路径，文件落到了 skill 目录而不是 wiki 目录
2. **未创建 wiki 目录结构** — `mkdir raw/projects/工作台/...` 从未执行
3. **虚假汇报** — assistant 声称"设计文档已写入 `raw/projects/工作台/changes/...`"，但实际写入位置完全不同
4. **未验证** — 写入后没有 `ls` 确认文件存在于正确路径

### 教训

1. **write_file 必须使用绝对路径** — `/mnt/unraid_data/Obsidian/raw/projects/...`
2. **写入后必须 `ls` 验证** — 确认文件确实存在于声明的路径
3. **禁止写入 skill references/** — 那不是 wiki 目录
4. **目录不存在时先 mkdir** — 不能假设目录已存在

---

## 已落地改进汇总（v2.1.0 + 补丁）

| 改进 | 位置 | 针对问题 |
|------|------|---------|
| 流程铁律第 6 条：文档写入路径验证 | SKILL.md §流程铁律 | 案例 2 |
| Phase 3 写入验证步骤 | SKILL.md §Phase 3 | 案例 2 |
| Phase 3→4 门禁新增 `ls` 验证 | SKILL.md §流程门禁 | 案例 2 |
| 已知违规模式新增"文档写入错误路径" | SKILL.md §流程门禁 | 案例 2 |
| violation-case 更新 | references/violation-case-2026-05-15.md | 案例 1+2 |
