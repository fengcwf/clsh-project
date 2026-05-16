# GitHub 同步指南 — clsh-project skill

## 仓库信息

- **仓库**: `fengcwf/clsh-project`（私有）
- **地址**: https://github.com/fengcwf/clsh-project
- **本地路径**: `/root/.hermes/skills/productivity/clsh-project/`
- **Token**: 存储在 `/root/.hermes/.env` 的 `GITHUB_TOKEN`

## 同步命令

```bash
# 日常更新（在 clsh-project 目录执行）
cd /root/.hermes/skills/productivity/clsh-project
git add .
git commit -m "<message>"
git push origin main
```

## 注意事项

- **只同步 clsh-project 目录**：git 仓库在 `clsh-project/` 下，不包含其他 skill
- Token 从 `/root/.hermes/.env` 读取：`grep GITHUB_TOKEN /root/.hermes/.env | cut -d= -f2`
- 不要在 commit message 中包含 token
- 同步范围：`SKILL.md` + `README.md` + `references/` 目录
