# 违规案例：Phase 8 第一轮修复 — 灵犀直接写代码（2026-05-20）

## 事件

Obsidian Workbench Phase 8 第一轮修复中，大佬提出 6 个测试反馈问题，灵犀直接自己修改了所有前端和后端代码（app.mjs, style.css, notes.mjs, share.mjs, backlinks.mjs, indexer.mjs, server.mjs），未派 coder/artist/tester。

## 根因

灵犀判断"修复小、代码量少"，以效率为由跳过了角色分离铁律。

## 后果

1. 违反了 clsh-project 铁律第 4 条"角色分离"
2. 被大佬指出"刚刚的测试结果修复都是你去做的，还是让coder、artist、tester去做"
3. 需要第二轮重新按角色分离执行，浪费了时间

## 教训

- **Phase 8 反馈修复 = Phase 6 执行**，必须走角色分离
- **"小修复"不是借口** — 即使只改一行也必须派 agent
- **灵犀的价值是协调、验证、汇报**，不是写代码
- **效率不是跳过角色分离的理由**（第 N 次强调）

## 正确做法

| 修复类型 | 应派 agent |
|---------|-----------|
| 后端 API 修复 | coder |
| 前端 JS 逻辑修复 | artist |
| CSS 样式修复 | artist |
| 测试验证 | tester |
| 灵犀职责 | 协调、验证 checkpoint、汇报 |

## 对比：第二轮正确执行

第二轮（追加 3 个问题 + 前 6 个问题的 UI 风格修复）：
- coder：后端 API（findShareByPath + /embed/* 路由 + CORS）
- artist-1：UI 风格重做（style.css + index.html）
- artist-2：app.mjs 功能修复（问题 1-6）
- artist-3：app.mjs 新增功能（TOC + iframe）
- tester：全量测试 9/9 PASS

结果：9/9 通过，无回归问题。
