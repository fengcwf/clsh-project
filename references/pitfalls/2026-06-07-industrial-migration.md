# 2026-06-07 工业区迁移教训

## #91: Vue3 模块 CSS 类未注册到 style.css（2026-06-07）

- **场景：** 工业区模块 IndustrialView.mjs 使用 66 个 CSS 类（`.ind-card`, `.ind-table`, `.ind-modal` 等），全部未在 style.css 定义，页面无样式
- **根因：** Vue3 h() render 的 `class: 'xxx'` 只设 HTML 属性，不自动注入 CSS
- **修复：** 在 style.css 末尾追加 ~280 行 CSS（毛玻璃设计系统）
- **规则：** 新模块使用 CSS 类时，必须同步在 style.css 中定义。派 coder 时 task body 必须包含此验收标准。
- **验证：** `curl -s http://localhost:8080/style.css | grep ".模块前缀-"` 应有结果

## #92: SQLite 迁移列名不匹配（2026-06-07）

- **场景：** 旧 buildings 表有 shareholder_ratio/shareholder_note/created_at/updated_at 列，新 building 表没有。迁移脚本用旧表列名 INSERT → `SQLITE_ERROR: table has no column named`
- **根因：** 迁移脚本 `SELECT *` 获取所有列，直接 INSERT 到新表，未过滤
- **修复：** PRAGMA table_info 对比新旧表，只 INSERT 新表存在的列，排除 id（自增）
- **规则：** 迁移前必须对比 schema，不能假设新旧表结构一致

## #93: delegate_task 浏览器验证超时（2026-06-07）

- **场景：** 派 tester 用浏览器截图验证 UI，600 秒超时未完成
- **根因：** 浏览器操作（登录→导航→截图→vision 分析）消耗大量 API 迭代
- **修复：** 代码验证优先（grep/node -c/curl），浏览器验证留给最关键的 UI 交互
- **规则：** 验证任务优先用代码，必须浏览器时串行单张派发
