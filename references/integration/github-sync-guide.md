# GitHub 同步指南

## clsh-project 仓库

- **仓库**: `fengcwf/clsh-project`（私有）
- **地址**: https://github.com/fengcwf/clsh-project
- **本地路径**: `/root/.hermes/skills/productivity/clsh-project/`

## clsh-content 仓库

- **仓库**: `fengcwf/clsh-content`（私有）
- **地址**: https://github.com/fengcwf/clsh-content
- **本地路径**: `/root/.hermes/skills/productivity/clsh-content/`

## 同步命令

```bash
# clsh-project
cd /root/.hermes/skills/productivity/clsh-project
git add . && git commit -m "<message>" && git push origin main

# clsh-content
cd /root/.hermes/skills/productivity/clsh-content
git add . && git commit -m "<message>" && git push origin main
```

## 注意事项

- Token 从 `/root/.hermes/.env` 读取：`grep GITHUB_TOKEN /root/.hermes/.env | cut -d= -f2`
- 不要在 commit message 中包含 token
- 每个 skill 目录是独立的 git 仓库
