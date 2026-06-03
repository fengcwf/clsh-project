# Phase 8 Mechanical Pre-Close Checklist

> 2026-06-03 新增：3 次 Phase 8 违规（不写记录/不测试就汇报）后确立的机械强制机制。

## 触发时机

每轮 Phase 8 修复完成后、向大佬汇报前，**必须执行**。

## 检查步骤

```bash
PROJECT="<项目名>"
ROUND="round<N>"
DIR="raw/projects/${PROJECT}/changes/${ROUND}-feedback"

# Step 1: 确认变更目录存在
[ -d "$DIR" ] || { echo "MISSING DIR: $DIR"; exit 1; }

# Step 2: 确认 4 个必写文件
MISSING=0
for f in conversation.md diagnosis.md fixes.md test-report.md; do
  if [ ! -f "$DIR/$f" ]; then
    echo "MISSING: $f"
    MISSING=$((MISSING + 1))
  fi
done

# Step 3: 确认 fixes.md 非空（有实际修复内容）
if [ -f "$DIR/fixes.md" ]; then
  LINES=$(wc -l < "$DIR/fixes.md")
  [ "$LINES" -lt 3 ] && echo "WARNING: fixes.md only $LINES lines"
fi

# Step 4: 确认 tester 验证记录
if [ -f "$DIR/test-report.md" ]; then
  grep -q "PASS\|FAIL\|浏览器" "$DIR/test-report.md" || echo "WARNING: test-report.md 缺少 PASS/FAIL/浏览器 验证记录"
fi

[ "$MISSING" -eq 0 ] && echo "✅ Phase 8 pre-close check PASSED" || echo "❌ $MISSING files MISSING — 不允许汇报完成"
```

## 文件内容要求

| 文件 | 最低内容 | 写入时机 |
|------|---------|---------|
| `conversation.md` | 大佬反馈的原始问题列表（逐条记录） | 收到反馈后立即 |
| `diagnosis.md` | Diagnose 6 阶段记录（Stage 1-6 每阶段结论） | 诊断完成后 |
| `fixes.md` | 每个问题的修复方案 + kanban 卡 ID + 修改的文件列表 | 修复完成后 |
| `test-report.md` | tester 验证结果（PASS/FAIL + 截图证据或浏览器验证描述） | tester 返回后 |

## 红线

- **缺少任一文件 = 不允许汇报"完成"**
- **conversation.md 不是在修完之后补写，而是收到反馈后立即写**
- **test-report.md 不能只有"已修复"，必须有验证方式和结果**
