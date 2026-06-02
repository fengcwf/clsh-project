# Constitution 模板 — 项目级约束文件

## 概述

`constitution.md` 是项目级的"宪法"，定义 AI worker 必须遵守的技术约束、代码规范和架构要求。

**灵感来源：** Spec-Kit 的 CONSTITUTION.md + gstack 的角色约束

**文件位置：** `raw/projects/<项目名>/source-of-truth/constitution.md`

## 何时创建

- Phase 3（写设计文档）时，同步创建 constitution.md
- 旧项目迁移时，从现有代码/文档中提炼

## 模板

```markdown
---
title: "[项目名] 项目约束"
date: YYYY-MM-DD
type: constitution
project: "[项目名]"
---

# [项目名] 项目约束

## 技术栈

- **语言：** [如 Python 3.11, PHP 8.1, TypeScript 5.x]
- **框架：** [如 FastAPI, Laravel, Next.js]
- **数据库：** [如 PostgreSQL 16, MySQL 8, SQLite]
- **包管理：** [如 pip, composer, pnpm]
- **部署：** [如 Docker, systemd, nginx]

## 代码规范

### 命名规则
- [如：Python 用 snake_case，类名用 PascalCase]
- [如：数据库表名用复数形式 users, orders]

### 文件组织
- [如：路由文件在 src/routes/，服务层在 src/services/]
- [如：测试文件在 tests/ 目录，命名 test_*.py]

### 风格约束
- [如：使用 type hints]
- [如：行宽 120 字符]
- [如：禁止使用 any 类型（TypeScript）]

## 架构约束

### 分层规则
- [如：Controller 层不直接操作数据库，必须通过 Service 层]
- [如：业务逻辑不写在路由文件中]

### 依赖规则
- [如：禁止循环依赖]
- [如：外部 API 调用统一封装在 services/external/]

### 数据库规则
- [如：禁止直接写 SQL，使用 ORM]
- [如：所有表必须有 created_at, updated_at 字段]
- [如：迁移文件不可修改，只能新增]

## 禁止事项

- ❌ [如：禁止在生产代码中使用 print/console.log]
- ❌ [如：禁止硬编码密钥/密码]
- ❌ [如：禁止修改 migration 文件]

## 必须事项

- ✅ [如：所有 API 端点必须有错误处理]
- ✅ [如：所有新功能必须有测试]
- ✅ [如：数据库操作必须在事务中]

## 环境配置

- **开发端口：** [如：前端 3000，后端 8000]
- **环境变量：** [如：从 .env 文件读取，不要提交到 git]
- **代理：** [如：外网请求走 192.168.0.41:7890]

## 参考文档

- [链接到项目其他相关文档]
```

## 轻量版模板（小项目）

```markdown
---
title: "[项目名] 项目约束"
date: YYYY-MM-DD
type: constitution
project: "[项目名]"
---

# [项目名] 项目约束

- **技术栈：** [一句话描述]
- **代码规范：** [关键规则]
- **架构：** [核心约束]
- **禁止：** [最重要的 2-3 条]
```

## 从现有项目提炼

如果项目已有代码但没有 constitution，按以下步骤提炼：

1. **扫描代码结构** — 确定文件组织方式
2. **检查 package.json/requirements.txt** — 确定技术栈和依赖
3. **查看现有代码风格** — 命名规则、缩进、注释风格
4. **检查 .env 或配置文件** — 环境配置
5. **询问大佬** — 确认隐含的约束和偏好

## 与 SOUL.md 的关系

| 维度 | SOUL.md | constitution.md |
|------|---------|-----------------|
| **范围** | 全局（所有项目） | 单个项目 |
| **内容** | 行为风格、沟通偏好 | 技术约束、代码规范 |
| **加载** | 自动（Hermes 启动时） | 主动注入（clsh-project 流程） |
| **示例** | "结论在前，步骤在后" | "使用 snake_case，禁止 any" |
