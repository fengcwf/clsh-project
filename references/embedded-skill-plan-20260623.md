# clsh-project 内嵌 skill 拆分方案

**日期**: 2026-06-23
**状态**: 待实施

## 背景

SKILL.md 440 行（v7.0），4 轮审查结论：偏离根因是插件 Layer 3 从未实现（已修复），拆分有利于长期维护。

## 方案

不创建独立 skill。Phase 内容拆到 `references/phases/`，主 SKILL.md 按需加载。

```
clsh-project/
├── SKILL.md              (~120行, 永久注入)
├── references/phases/
│   ├── phase0.md ~ phase8.md  (各 30-60行)
├── references/           (不变)
├── templates/            (不变)
└── scripts/              (不变)
```

## 加载机制

- 主 SKILL.md：自动注入（红线+路由表）
- Phase 文件：gate-workflow.py 返回 current_phase → LLM 调用 `skill_view(file_path='references/phases/phaseN.md')`

## 主 SKILL.md 保留（~120行）

YAML frontmatter + 概述 + 边界定义 + Iron Laws(3条) + 触发条件 + gate-workflow.py 路由 + Phase 路由表 + 门禁总览 + 参考索引

## 各 Phase 文件（30-60行）

步骤 + 产出物 + Common Mistakes(5-10条) + 出口 gate

## 迁移

~1.5 小时。Convention/Pitfall 分散到各 Phase Common Mistakes。Iron Laws 留主 SKILL.md。
