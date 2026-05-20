# clsh-project 技术陷阱 — 2026-05-20

## 陷阱 1：write_file 工具 "was modified" 报错

**场景：** 用 write_file 写入已被外部进程修改的文件（如 pm2 重启、其他 agent 写入）
**症状：** write_file 报错 "was modified since you last read it on disk"
**修复：** 改用 terminal `cat > file << 'EOF'` 方式写入
**预防：** 对于会被外部进程修改的文件，始终用 terminal 写入

## 陷阱 2：server.mjs import 路径与实际文件位置不匹配

**场景：** server.mjs 从 `./services/` 导入模块，但文件实际在 `./api/` 目录
**症状：** 服务器启动后 API 返回 404 或模块未找到
**修复：** 确保 server.mjs 的 import 路径与实际文件位置一致
**预防：** 创建新文件后，grep server.mjs 确认 import 路径正确

## 陷阱 3：前后端参数名不一致

**场景：** 前端发送 `expiresIn`，后端解构 `expiresAt`
**症状：** 分享创建成功但 expiresAt 为 null
**修复：** 统一参数名（前端发送什么，后端就解构什么）
**预防：** 写完 API 后立即 curl 测试，验证参数传递

## 陷阱 4：前端硬编码 localhost

**场景：** 前端 app.mjs 中分享链接写死 `http://localhost:3456`
**症状：** 用户访问时链接指向 localhost 而非服务器 IP
**修复：** 使用 `BASE_URL` 常量，从环境变量或配置读取
**预防：** 搜索代码中所有 `localhost` 引用，替换为配置变量

## 陷阱 5：share.html 静态文件 API 路径

**场景：** share.html 通过 fetch 调用 API，但 API 路由未注册
**症状：** 分享页面加载失败，显示 "分享链接已过期或不存在"
**修复：** 确保 `/api/shares/verify/:token` 路由在 server.mjs 中注册
**预防：** 写完 share.html 后，验证所有 fetch 调用的 API 路由存在

## 陷阱 6：write_file "was modified" 报错

**场景：** 用 write_file 写入已被外部进程修改的文件
**症状：** write_file 报错 "was modified since you last read it on disk"
**修复：** 改用 terminal `cat > file << 'EOF'` 方式写入
**预防：** 对于会被外部进程修改的文件，始终用 terminal 写入

## 陷阱 7：server.mjs import 路径与实际文件位置不匹配

**场景：** server.mjs 从 `./services/` 导入模块，但文件实际在 `./api/` 目录
**症状：** 服务器启动后 API 返回 404 或模块未找到
**修复：** 确保 server.mjs 的 import 路径与实际文件位置一致
**预防：** 创建新文件后，grep server.mjs 确认 import 路径正确

## 陷阱 8：前后端参数名不一致

**场景：** 前端发送 `expiresIn`，后端解构 `expiresAt`
**症状：** 分享创建成功但 expiresAt 为 null
**修复：** 统一参数名（前端发送什么，后端就解构什么）
**预防：** 写完 API 后立即 curl 测试，验证参数传递
