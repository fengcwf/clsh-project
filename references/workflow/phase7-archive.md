# clsh-project — Phase 7: 完成归档与流程复盘

> 本文件是 clsh-project skill 的详细参考。SKILL.md 中有摘要和链接。

---

## Phase 7: 完成归档 + 流程复盘

### ⛔ wiki 归档检查清单（必做，不可跳过）

Phase 7 归档时，必须确认以下文件已写入 wiki：

**项目文档：**
- [ ] `wiki/projects/<项目名>/overview.md` → 更新 status 为 `done`
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/completion-summary.md` → 完成摘要
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/retrospective.md` → 流程复盘
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/conversation.md` → 需求对话
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/proposal.md` → 设计提案
- [ ] `wiki/projects/<项目名>/changes/archive/<变更名>/tasks.md` → 实现计划
- [ ] `wiki/projects/<项目名>/source-of-truth/constitution.md` → 项目约束

**Phase 8 各轮归档（每轮必须）：**
- [ ] `wiki/projects/<项目名>/changes/archive/round<N>-feedback/conversation.md` → 测试反馈记录
- [ ] `wiki/projects/<项目名>/changes/archive/round<N>-feedback/fixes.md` → 修复方案记录

**⛔ 如果 Phase 8 已完成多轮测试，必须将每轮的 feedback 目录归档到 archive/，不能只保留在 changes/ 下。**

### 归档步骤

1. 更新提案状态 → `status: done`
2. 归档所有变更 → `changes/<变更名>/` → `changes/archive/`
3. 归档 Phase 8 每轮 feedback → `changes/round<N>-feedback/` → `changes/archive/round<N>-feedback/`
4. 更新 Source of Truth
5. 写入完成摘要 + 流程复盘
6. 同步 wiki + GitHub（见 `clsh-content/references/integration/github-sync-guide.md`）
7. **🔬 运行蒸馏评估**（加载 `project-wrap-up` skill）：
   - 执行 eval.json 5 项 binary 评估（30 秒）
   - 对 FAIL 项做故障分类（FLOW/AGENT/TOOL/KNOWLEDGE）
   - 结果 append 到 learnings.md
   - 触发条件满足时（learnings ≥10 条 或 eval ≤2/5）执行深度蒸馏
8. 向大佬汇报（含 eval 结果和蒸馏发现）
9. `ls` 验证所有归档文件存在且大小 > 0

### ⛔ 流程合规复盘（必做）

1. 是否有跳步？
2. 是否有提前编码？
3. 是否有自测自验？
4. 文档是否前置？
5. Security Scan 是否执行？
6. Auto-Fix 是否超过 2 轮？
7. 改进措施

**复盘结果写入** `retrospective.md`
