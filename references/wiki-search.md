# Wiki 检索（只读优先）

Vault：`\\192.168.0.123\data\Obsidian`

## 铁律

- **Phase 0 / 开工前必须查 wiki**，避免重复造轮子。
- **日常执行只读 wiki**；唯一允许写 wiki 的步骤是 Phase 6 归档中沉淀 `reusability: cross-project` 的 solutions。
- 涉及 OA / 用友 / SQL / 客户 / 运维 的问题，不查 Obsidian 就回答 = 违规（与 vault AGENTS.md 一致）。

## 检索顺序（由快到慢）

1. **热缓存** `%WIKI%\hot.md` — ~500 字语义快照，项目状态与最近变更。
2. **索引** `%WIKI%\INDEX.md` — 页面列表 + 一行摘要；先 grep 关键词。
3. **方案库** `%WIKI%\solutions\` — 跨项目可复利方案；优先 `reusability: cross-project`。
4. **概念/实体** `%WIKI%\concepts\`、`%WIKI%\entities\`。
5. **参考** `%WIKI%\reference\`（ERRORS、LEARNINGS、tools、network…）。
6. **分析报告** `%WIKI%\syntheses\`。
7. **项目容器** `%VAULT%\raw\projects\<project>\overview.md`。
8. **领域资料** `%VAULT%\02-致远OA\`、`03-帆软报表\`、`04-用友\`、`08-unraid\`、`01-客户资料\`。
9. **全局 grep**（最后手段）。

## PowerShell 检索示例

```powershell
$vault = "\\192.168.0.123\data\Obsidian"
$wiki  = Join-Path $vault "wiki"

# 1) INDEX
Select-String -Path "$wiki\INDEX.md" -Pattern "笔记|sync|SQLite" -SimpleMatch

# 2) solutions 文件名/内容
Get-ChildItem "$wiki\solutions" -Filter *.md | Select-String -Pattern "timeout|obsidian" -List

# 3) concepts
Get-ChildItem "$wiki\concepts" -Filter *.md | Select-String -Pattern "loop|gate" -List

# 4) 定向目录
Get-ChildItem "$vault\08-unraid" -Recurse -Filter *.md | Select-String -Pattern "docker" -List

# 5) 全局（限 wiki，避免扫爆 raw）
Get-ChildItem $wiki -Recurse -Filter *.md | Select-String -Pattern "关键词" -List
```

## 答案引用规范

回复中引用 wiki 时给出：

1. 文件相对路径（如 `wiki/solutions/codewhale-network-timeout.md`）
2. 关键结论 1-3 句
3. 可选 wikilink：`[[solutions/codewhale-network-timeout|方案名]]`
4. 若 `confidence: low` 或 `contested: true`，必须向用户标注不确定性

## Frontmatter 速读

| 字段 | 含义 |
|------|------|
| type | concept / entity / solution / reference / summary |
| status | draft / active / archived |
| reusability | cross-project / project-specific / one-time |
| confidence | high / medium / low |
| contested | true 时内容有争议 |

## 与 clsh-project-mimo 的衔接

| 时机 | 动作 |
|------|------|
| Phase 0 Research | 读 hot + INDEX + solutions；把可复用方案记入 research |
| Phase 2 Design | 检查是否已有同类 solution，优先复用 |
| Phase 6 Archive | 将跨项目教训写入 `wiki/solutions/`（带 source_project） |

详细 schema 见 `%VAULT%\wiki\SCHEMA.md` 与 `%VAULT%\SCHEMA.md`。
