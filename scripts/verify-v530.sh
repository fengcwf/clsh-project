#!/bin/bash
# clsh-project v5.30.0 验证脚本
echo "=== SKILL.md 行数 ==="
wc -l /root/.hermes/skills/productivity/clsh-project/SKILL.md

echo ""
echo "=== 确认码模板 ==="
grep -c "🔑" /root/.hermes/skills/productivity/clsh-project/SKILL.md

echo ""
echo "=== 新增 reference 文件 ==="
for f in \
  references/methodology/context-engineering-integration.md \
  references/integration/external-skill-sources.md \
  references/pitfalls/confirmation-code-template-enforcement.md; do
  path="/root/.hermes/skills/productivity/clsh-project/$f"
  if [ -f "$path" ]; then
    echo "✅ $f ($(wc -l < "$path") lines)"
  else
    echo "❌ $f MISSING"
  fi
done

echo ""
echo "=== Worker AGENTS.md ==="
for p in coder worker artist tester; do
  echo "$p: $(wc -l < /root/.hermes/profiles/$p/AGENTS.md) lines"
done

echo ""
echo "=== 已安装外部 skill ==="
hermes skills list 2>/dev/null | grep -E "zoom-out|handoff|improve-arch|taste-skill|taste-brand|doubt|security-hard|code-simpl|frontend-ui"
