# Skill 删除导致脚本丢失 — MoviePilot 案例

**日期：** 2026-05-31
**教训来源：** MoviePilot 项目优化

## 问题

`skill_manage(action='delete')` 会删除整个 skill 目录，包括 `scripts/`、`references/` 等子目录。如果脚本被其他组件（如插件）引用，删除 skill 会导致脚本丢失。

## 案例

### 背景
- MoviePilot 原有 skill：`~/.hermes/skills/media/moviepilot/`
- Skill 包含脚本：`scripts/mp_render.py`（HTML 渲染脚本）
- 新建插件：`~/.hermes/plugins/mp-command/`（调用 mp_render.py）

### 操作
1. 删除 moviepilot skill：`skill_manage(action='delete', name='moviepilot')`
2. 删除 wq skill：`skill_manage(action='delete', name='wq', absorbed_into='')`

### 结果
- 整个 `~/.hermes/skills/media/moviepilot/` 目录被删除
- `scripts/mp_render.py` 被一起删除
- mp-command 插件调用 mp_render.py 失败

### 修复
从记忆中重建 mp_render.py（142 行）

## 规则

1. **删除 skill 前检查脚本引用**
   ```bash
   # 检查是否有其他组件引用该 skill 的脚本
   grep -r "skills/media/moviepilot/scripts" ~/.hermes/plugins/
   grep -r "skills/media/moviepilot/scripts" ~/.hermes/skills/
   ```

2. **备份脚本再删除**
   ```bash
   # 备份脚本
   cp ~/.hermes/skills/media/moviepilot/scripts/mp_render.py /tmp/
   # 删除 skill
   skill_manage(action='delete', name='moviepilot')
   # 恢复脚本到新位置
   mkdir -p ~/.hermes/plugins/mp-command/scripts/
   mv /tmp/mp_render.py ~/.hermes/plugins/mp-command/scripts/
   ```

3. **absorbed_into 必须是 skill，不能是 plugin**
   ```python
   # ❌ 错误：absorbed_into 指向 plugin
   skill_manage(action='delete', name='moviepilot', absorbed_into='mp-command')
   # 报错：absorbed_into='mp-command' does not exist

   # ✅ 正确：absorbed_into 为空或指向已存在的 skill
   skill_manage(action='delete', name='moviepilot', absorbed_into='')
   ```

## 相关 Pitfall

- clsh-project #57：Skill 删除会连带删除 scripts/ 目录
