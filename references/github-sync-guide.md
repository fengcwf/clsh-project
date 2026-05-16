# GitHub 同步指南 — clsh-project skill

## 仓库信息

- **仓库**: `fengcwf/clsh-project`（私有）
- **地址**: https://github.com/fengcwf/clsh-project
- **本地路径**: `/root/.hermes/skills/productivity/clsh-project/`
- **Token**: 存储在 `/root/.hermes/.env` 的 `GITHUB_TOKEN`

## 同步命令

```bash
# 首次推送（已执行）
cd /root/.hermes/skills/productivity
git init
git config user.name "灵犀"
git config user.email "lingxi@hermes"
git remote add origin https://<TOKEN>@github.com/fengcwf/clsh-project.git
git add clsh-project/
git commit -m "<message>"
git branch -M main
git push -u origin main

# 后续更新
cd /root/.hermes/skills/productivity
git add clsh-project/
git commit -m "<message>"
git push
```

## 注意事项

- Token 从 `/root/.hermes/.env` 读取：`grep GITHUB_TOKEN /root/.hermes/.env | cut -d= -f2`
- 不要在 commit message 中包含 token
- 同步范围：`clsh-project/` 目录（SKILL.md + references/）
