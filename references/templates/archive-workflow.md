# Phase 7 归档操作手册（2026-05-21 实战版）

## 触发条件

项目 Phase 8 测试全部通过，大佬确认项目完成时触发。

## 归档步骤（按顺序执行）

### 1. 更新 overview.md 状态

```markdown
status: done  # 从 active 改为 done
updated: YYYY-MM-DD  # 更新日期
```

在进度表中将所有 Phase 标记为 ✅ 完成。

### 2. 创建最终 completion-summary.md

**位置：** `raw/projects/<项目名>/changes/archive/<变更名>/completion-summary.md`

**内容模板：**

```markdown
# <项目名> — 项目完成摘要

> **项目：** <项目名>
> **完成日期：** YYYY-MM-DD
> **状态：** ✅ 全部完成（Phase 1-8）
> **GitHub：** <repo-url>（私有/公有）

## 项目概述
<一句话描述>

## 技术方案
- **后端：** <技术栈>
- **前端：** <技术栈>
- **部署：** <部署方式>
- **代码位置：** <绝对路径>

## 实现功能
| 功能 | 状态 | 说明 |
|------|------|------|
| ... | ✅ | ... |

## 性能指标
| 指标 | 值 |
|------|-----|
| ... | ... |

## 代码结构
<树形结构>

## 测试覆盖
- **N 轮 Phase 8 测试**，累计修复 N+ 个问题
- 每轮均有 tester 验证（除已记 ERRORS.md 的轮次）

## 已知限制
1. ...
2. ...

## 后续优化（低优先级）
- [ ] ...
```

### 3. 创建 retrospective.md

**位置：** `raw/projects/<项目名>/changes/archive/<变更名>/retrospective.md`

**必含章节：**
1. 流程合规总览（表格）
2. 流程违规记录（每轮违规详细说明）
3. 角色分离执行情况（每轮表格）
4. 技术决策回顾
5. 教训总结
6. 项目指标
7. 改进建议

### 4. 归档变更目录

```bash
# 将 changes/ 下的变更目录复制到 archive/
cd raw/projects/<项目名>
mkdir -p changes/archive/<变更名>
cp -r changes/<变更名>/* changes/archive/<变更名>/
```

### 5. 同步 GitHub

```bash
cd <项目代码目录>
git add -A
git commit -m "feat: <项目名> 完成归档

- Phase 1-8 全部完成
- N 轮测试修复 N+ 问题
- 完整流程复盘"
git push origin main
```

### 6. 更新 memory

将项目进度条目替换为精简摘要：

```
<YYYY-MM-DD>: <项目名> 项目完成归档。<N>天周期，Phase 1-8全完成，<N>轮测试修复<N>+问题。服务: <部署信息>。GitHub: <repo>(私有)已推送。关键教训: <核心教训>。路径: <代码路径>。状态: ✅完成。
```

**注意：** memory 容量 2200 字符。如果占用率 >85%，先删除过时条目再添加。

## 归档检查清单

- [ ] overview.md → status: done
- [ ] completion-summary.md 已写入 archive/
- [ ] retrospective.md 已写入 archive/
- [ ] 所有变更目录已复制到 archive/
- [ ] GitHub 已推送
- [ ] memory 已更新
- [ ] 服务运行正常（pm2 status / curl health）
