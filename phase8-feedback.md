---
phase: 8
name: "反馈循环"
gate_script: "gate-phase8.py"
output_files: []
---

# Phase 8: 反馈循环

## 前置依赖

- Phase 7 的归档完成

## 执行步骤

协调者只记录现象+文件+验收标准，coder/artist 自己分析根因+执行。

| 方式 | 适用场景 |
|------|---------|
| 标准模式 | Gateway、简单 bug → fix 卡 + tester 验证 |
| /goal 模式 | CLI/TUI、复杂 bug → judge + gate-phase8 |
| kanban --goal | Gateway fix 卡 → worker 自动迭代 |

**⛔ /goal 限制：** judge 不能替代 tester（C3）| 不能绕过 gate-phase8 | Phase 1-6 禁用

```bash
python3 scripts/gate-phase8.py <项目目录>
```
