# {项目名} — 领域语言

{一两句话描述项目是什么、为什么需要统一术语。}

## 语言

**{术语1}:**
{一两句定义 — "是什么"而非"做什么"}
_Avoid_: {同义词/容易混淆的词}

**{术语2}:**
{一两句定义}
_Avoid_: {同义词}

## 关系

- **{术语A}** 包含多个 **{术语B}**
- **{术语C}** 引用 **{术语D}**（通过 ID）

## 标志的歧义

- {术语X} 曾被用来指代 Y 和 Z — 已明确：{术语X} = Y，{术语X2} = Z

---

## 使用规则

1. **每个项目维护一份 context.md** — Phase 1 需求澄清时自然积累
2. **只收录项目特有术语** — 通用编程概念（timeout、error type）不收录
3. **一词一义** — 多个词指同一概念时，选最好的一个，其他列为 "Avoid"
4. **定义"是什么"** — 一两句话，不是功能描述
5. **标注关系** — 术语间的包含、引用、依赖关系
6. **发现歧义立即记录** — Phase 1 中发现术语冲突时，当场解决并记录

## 文件位置

`raw/projects/<项目名>/source-of-truth/context.md`

## 与其他文档的关系

- **conversation.md** — 记录需求 Q&A，引用 context.md 术语
- **proposal.md** — 设计文档使用 context.md 术语，保持一致
- **constitution.md** — 技术约束，不重复 context.md 内容
- **ADR** — 架构决策，引用 context.md 中的领域概念

---

*来源：Matt Pocock /grill-with-docs 的 CONTEXT-FORMAT.md*
