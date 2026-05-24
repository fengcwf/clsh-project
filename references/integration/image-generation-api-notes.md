# 图片生成 API 调用笔记

> 2026-05-24 实测数据。用于 clsh-project Phase 3 设计发散和 clsh-content 封面图生成。

## OpenRouter — Grok Imagine Image Quality

- **模型 ID**: `x-ai/grok-imagine-image-quality`
- **价格**: $0.05/张
- **能力**: 文本→图片，1K/2K 分辨率，多比例，文字渲染
- **API**: `POST https://openrouter.ai/api/v1/chat/completions`

### ⚠️ Free Tier 限制（2026-05-24 实测）

- **free tier 账户无法调用图片模型**，即使模型标注为 "free"
- 返回 `402 Insufficient credits`（账户从未购买 credits）
- `:free` 变体不存在（404）
- **需要购买 credits 才能使用**

### 调用格式

```json
{
  "model": "x-ai/grok-imagine-image-quality",
  "messages": [{"role": "user", "content": "prompt text"}],
  "modalities": ["image", "text"],
  "image_config": {"aspect_ratio": "16:9"}
}
```

注意：不加 `modalities` 参数也会返回 402（不是 400），说明该参数是必需的。

### 脚本位置

`/root/.hermes/skills/productivity/clsh-content/scripts/image-gen.cjs` — 默认模型。

---

## Google Gemini

- **图片模型**: `gemini-2.5-flash-image`（⚠️ 不是 `gemini-2.0-flash-exp`）
- **免费额度**: 500次/天（但可能被 quota 限制到 0）
- **API**: `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}`

### ⚠️ 国内网络访问

- **直连超时** — 服务器在国内无法访问 Google APIs（GFW）
- **需代理**: `http://192.168.0.41:7890`（家庭网络 HTTP 代理）
- curl 示例: `curl --proxy http://192.168.0.41:7890 ...`
- Python: `urllib.request.ProxyHandler({"https": "http://192.168.0.41:7890"})`
- ⚠️ Python urllib 代理设置比 curl 更严格，建议用 curl 或写 shell 脚本

### ⚠️ 模型名称

| 名称 | 状态 |
|------|------|
| `gemini-2.0-flash-exp` | ❌ 404 NOT_FOUND |
| `gemini-2.0-flash-preview-image-generation` | ❌ 不在列表中 |
| `imagen-3.0-generate-002` | ❌ 不在列表中 |
| `gemini-2.5-flash-image` | ✅ 正确名称 |
| `gemini-2.0-flash` | ❌ 不支持 IMAGE output（400） |

### 调用格式

```json
{
  "contents": [{"parts": [{"text": "prompt"}]}],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {"aspectRatio": "16:9"}
  }
}
```

响应中图片在 `candidates[0].content.parts[].inlineData.data`（base64）。

### Quota 限制

- free tier 可能被限到 0（`limit: 0`）
- 错误码: `429 RESOURCE_EXHAUSTED`
- retry delay 通常 45 秒
- 不同模型有独立 quota

---

## fal.ai（备选）

- **模型**: FLUX.2 Schnell, Seedream V4
- **需要**: `FAL_KEY` 环境变量
- **优势**: 不被 GFW 封锁
- **状态**: 未配置

---

## 截图替代方案（当前可用）

当图片模型不可用时，用 HTML mockup + chromium 截图：

```bash
chromium-browser --headless --disable-gpu --screenshot=/path/out.png \
  --window-size=1440,900 --no-sandbox file:///path/to/mockup.html
```

⚠️ AppArmor 限制：snap 版 chromium 无法写入 `/tmp`，改用 `/root/mockups/` 等路径。

发送到飞书：`send_message(target='feishu', message='描述\nMEDIA:/path/out.png')`
