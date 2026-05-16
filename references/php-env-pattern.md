# PHP .env 读取模式

## 问题

PHP 的 `getenv()` 函数**读不到 `.env` 文件中的变量**，只能读取系统环境变量。

## 正确做法

```php
// ❌ 错误：getenv 读不到 .env 文件
define('LUCKY_TOKEN', getenv('LUCKY_API_TOKEN') ?: '');

// ✅ 正确：用 parse_ini_file 读取 .env 文件
function get_lucky_token() {
    $env_file = dirname(__FILE__) . '/.env';
    if (file_exists($env_file)) {
        $env = @parse_ini_file($env_file);
        if (!empty($env['LUCKY_API_TOKEN'])) return $env['LUCKY_API_TOKEN'];
    }
    return getenv('LUCKY_API_TOKEN') ?: '';
}
define('LUCKY_TOKEN', get_lucky_token());
```

## 注意

- `.env` 文件路径用 `dirname(__FILE__)` 确保是相对于当前 PHP 文件的路径
- 用 `@` 抑制 `parse_ini_file` 的警告（文件不存在时）
- 保留 `getenv()` 作为 fallback（某些环境可能通过系统环境变量注入）
