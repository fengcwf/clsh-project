# Pitfall #126: vision_analyze 超时导致 Kanban 任务卡死

**Added:** 2026-06-09
**Severity:** CRITICAL (34 分钟超时，任务永久卡死)

## Rule
coder profile 不得包含 `vision` toolset。设计规范必须用文字/CSS 精确值描述，不引用图片路径。task body 中引用图片 → worker 调 vision_analyze → MiMo API 超时 → 任务卡死 → 僵尸进程。

## Anti-pattern
task body 写"参考图: /root/.hermes/image_cache/img_xxx.jpg" → coder worker 加载时自动 vision_analyze → 34 分钟超时 → worker 重试 → 再次超时 → 永久卡死。

## Correct Pattern
设计规范用文字描述：颜色用 rgba 值，间距用 px 值，布局用文字描述。不引用图片。如需分析参考图，由 artist（有 vision）执行或灵犀在派发前提取数值。

## Verification
```bash
grep "vision" /root/.hermes/profiles/coder/config.yaml
# 应该无输出（vision 已移除）
```

## Reference
- Workspace 优化 R4-4/R4-5 超时案例
- references/phase8-spec-precision-learnings.md
