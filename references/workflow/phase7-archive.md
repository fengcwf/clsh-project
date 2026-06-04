# clsh-project — Phase 7: 完成归档与流程复盘

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 7: 完成归档 + 流程复盘

### ⛔ wiki 归档检查清单（必做，不可跳过）

Phase 7 归档时，必须确认以下文件已写入 wiki。**注意：项目有两种归档结构**（见下方说明），根据实际结构选择对应路径。

**项目文档（两种结构通用）：**
- [ ] `raw/projects/<项目名>/overview.md` → 更新 status 为 `done`
- [ ] `raw/projects/<项目名>/source-of-truth/constitution.md` → 项目约束
- [ ] `raw/projects/<项目名>/changes/archive/completion-summary.md` → 完成摘要
- [ ] `raw/projects/<项目名>/changes/archive/retrospective.md` → 流程复盘
- [ ] `raw/projects/<项目名>/changes/archive/handoff.md` → 跨 session 续接文档

**设计文档（根据项目结构选择）：**

| 结构类型 | 设计文档位置 | Phase 8 反馈位置 |
|---------|------------|----------------|
| **变更型**（1 个设计目录） | `changes/archive/<变更名>/proposal.md` | `changes/archive/round<N>-feedback/` |
| **轮次型**（无独立设计目录） | `changes/archive/<变更名>/proposal.md`（同上） | `changes/archive/round<N>-feedback/` |

**Phase 8 各轮归档（每轮必须）：**
- [ ] `raw/projects/<项目名>/changes/archive/round<N>-feedback/conversation.md` → 测试反馈记录
- [ ] `raw/projects/<项目名>/changes/archive/round<N>-feedback/fixes.md` → 修复方案记录
- [ ] `raw/projects/<项目名>/changes/archive/round<N>-feedback/diagnosis.md` → 诊断记录（如有）
- [ ] `raw/projects/<项目名>/changes/archive/round<N>-feedback/test-report.md` → 测试报告（如有）

**⛔ 如果 Phase 8 已完成多轮测试，必须将每轮的 feedback 目录归档到 archive/，不能只保留在 changes/ 下。**

### 归档结构说明

**变更型（标准）：** 项目有 1 个 `changes/<日期>-<变更名>/` 目录（含 proposal/constitution/tasks），Phase 8 反馈在 `changes/round<N>-feedback/`。归档时 design 目录和 round 目录都移到 `archive/`。

**轮次型（Phase 8 密集）：** 项目经过多轮 Phase 8 反馈（≥5 轮），feedback 目录数量远多于设计目录。归档时所有 `changes/*` 统一移到 `changes/archive/`。completion-summary.md / retrospective.md / handoff.md 放在 `changes/archive/` 根目录（不嵌套在 `<变更名>/` 下）。

### 归档步骤

1. 更新提案状态 → `status: done`
2. 创建 `changes/archive/` + `source-of-truth/` 目录
3. 归档所有变更 → `mv changes/* changes/archive/`（一步到位，包括 design + round feedback + bugfix）
4. 更新 Source of Truth → `source-of-truth/constitution.md`
5. 写入 completion-summary.md + retrospective.md + handoff.md（放在 `changes/archive/`）
6. 清理项目测试残留（.pkl、musicdl_outputs/、__pycache__/ 等）
7. 同步 wiki + GitHub（见 `clsh-content/references/integration/github-sync-guide.md`）
8. **🔬 运行蒸馏评估**（加载 `project-wrap-up` skill）：
   - 执行 eval.json 8 项 binary 评估（30 秒）
   - 对 FAIL 项做故障分类（FLOW/AGENT/TOOL/KNOWLEDGE）
   - 结果 append 到 learnings.md
   - 触发条件满足时（learnings ≥10 条 或 eval ≤3/8）执行深度蒸馏
   - **同步到 raw/**：`python3 /opt/Workspace/scripts/obsidian/learnings-to-raw.py`（遵循 raw → ingest → wiki 架构）
9. 向大佬汇报（含 eval 结果和蒸馏发现）
10. **🔄 触发 Solutions Ingest**（知识复利编译）：
   - 检查 `raw/projects/<项目名>/` 下是否有新的 raw fix 记录（`.md` 文件，非 changes/ 目录）
   - 有新文件 → 按 `llm-wiki` skill 的 ingest 流程编译为 `wiki/solutions/` 页面：
     a. 读取 raw fix 记录内容
     b. LLM 判断 track（bug/knowledge）+ reusability（cross-project/project-specific）
     c. 搜索 `wiki/solutions/INDEX.md` 检查是否与已有方案重叠
     d. 重叠 → 更新现有方案；不重叠 → 创建新方案页面
     e. 更新 `wiki/solutions/INDEX.md` 索引
   - 无新文件 → 跳过
11. **📄 生成 Handoff 文档** — 归档时生成 `handoff.md`，方便跨 session 续接：
   - 当前项目状态摘要（已完成/待完成）
   - 建议下次 session 加载的 skills
   - 引用已有文档路径（不重复内容，避免 token 浪费）
   - 脱敏处理（删除密钥/token/密码）
   - **文件位置：** `raw/projects/<项目名>/changes/archive/handoff.md`（放在 archive 根目录，不嵌套在 `<变更名>/` 下）
   - **来源：** Matt Pocock /handoff skill
12. `ls` 验证所有归档文件存在且大小 > 0
13. **📊 运行执行审计**（Darwin + ECC 融合，2026-05-29）：
    - 运行 `references/scripts/execution-audit.py`（在 execute_code 中调用）
    - 输出合规报告：角色分离 / 验证执行 / tester 浏览器验证 / 修复轮次 / pitfall 触发
    - 合规率 < 75% → 写入 retrospective.md 的"改进措施"
    - pitfall 触发次数更新 → 影响下次执行时的置信度注入
    - **触发时机：大佬说"归档"时自动运行，不需要 cron 定时**
    - **⚠️ execute_code 不可用时的手动回退：** 读取各 round conversation.md 手动统计角色分离违规、验证合规、tester 浏览器验证、修复轮次，写入 retrospective.md。binary eval 同理——读 eval.json 逐条对照项目实际情况手动打分。

### ⛔ 流程合规复盘（必做）

1. 是否有跳步？
2. 是否有提前编码？
3. 是否有自测自验？
4. 文档是否前置？
5. Security Scan 是否执行？
6. Auto-Fix 是否超过 2 轮？
7. 改进措施

**复盘结果写入** `retrospective.md`
