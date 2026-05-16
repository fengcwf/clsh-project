# Lucky API 格式变化记录

## 2026-05-15 发现

Lucky 反向代理 API 返回格式已从旧版 `{ruleList: [...]}` 变为新版 `{msg, ret, data}`。

## 新旧格式对比

### 旧格式（已废弃）
```json
{
  "ruleList": [
    {
      "ProxyList": [
        {
          "Remark": "服务名",
          "Domains": ["example.com"],
          "Locations": ["http://192.168.0.100:8080"],
          "Enable": true
        }
      ]
    }
  ]
}
```

### 新格式（当前）
```json
{
  "msg": "success",
  "ret": 0,
  "data": {
    "ruleList": [...]
  }
}
```

### 错误响应
```json
{
  "msg": "login invalid",
  "ret": -1
}
```

## 兼容写法

```php
$web = lucky_api('webservice/rules');
$web_rules = [];

// 新格式：{msg, ret, data: {ruleList: [...]}}
if ($web && isset($web['ret']) && $web['ret'] === 0 && !empty($web['data'])) {
    if (isset($web['data']['ruleList'])) {
        $web_rules = $web['data']['ruleList'];
    } elseif (is_array($web['data'])) {
        $web_rules = $web['data'];
    }
}

// 兼容旧格式（直接 ruleList）
if ($web && !empty($web['ruleList'])) {
    $web_rules = $web['ruleList'];
}
```

## 注意事项

- Token 过期时返回 `{"msg":"login invalid","ret":-1}`，不是 HTTP 错误
- 需要在应用层检查 `ret` 字段判断是否成功
- Token 存储在 `/opt/Workstation/.env` 的 `LUCKY_API_TOKEN` 字段
- 读取 Token 必须用 `parse_ini_file()`，不能用 `getenv()`
