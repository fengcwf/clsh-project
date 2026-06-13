# Pitfall: Skill-Local 文件未迁移到 Vault

## 日期
2026-06-13

## 问题
darwin 优化 + clsh-project 日常迭代过程中，在 skill-local `references/` 目录创建了 15 个文件 + 1 个 template，从未迁移到 Vault。SKILL.md 参考文件表用裸文件名（依赖"路径前缀"声明），但实际上这些文件只存在于 skill-local，Vault 中无副本。

## 根因
1. skill_manage(action='write_file') 默认写入 skill-local，不会自动同步到 Vault
2. darwin 优化循环在临时目录操作，完成后只覆盖 skill-local，不迁移 Vault
3. SKILL.md 的"路径前缀"声明掩盖了路径不匹配问题（看起来一致但实际不一致）

## 修复
1. `cp skill-local/*.md Vault/references/` 迁移所有文件
2. `rm skill-local/*.md` 清空 skill-local（Vault 是唯一真相源）
3. SKILL.md 参考文件表改为绝对 Vault 路径（不用裸文件名 + 前缀声明）

## 防御规则
- **skill_manage(action='write_file') 后必须 grep SKILL.md 检查是否有对应 Vault 路径引用**
- **参考文件表必须用绝对路径，禁止裸文件名 + 路径前缀声明**
- **每次 skill 更新后检查 skill-local references/ 是否有应迁移的文件**

## 影响
15 个 references + 1 个 template + 13 个 pitfalls + 2 个 workflow = 31 个文件迁移
