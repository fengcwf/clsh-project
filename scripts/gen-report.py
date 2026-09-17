#!/usr/bin/env python3
"""
gen-report.py — clsh-project HTML 总体报告生成器（纯机械，stdlib only）

原则：
  - 报告是生成物（derived artifact）：永不手改，唯一修改方式是重新生成。
  - 报告内容 100% 来自项目目录中的 md/json 文件，不编造内容（文档烂则报告烂）。
  - 零 LLM 参与；生成失败不阻塞 clsh-project 流程（gate-workflow.py hook 吞异常）。
  - ⛔ CSS 必须对齐 workspace-development 设计系统 token（Light Glassmorphism）：
    --bg/--surface/--text/--text-secondary/--accent/--border/--shadow，
    禁止自创色值、禁止暗色主题。改 CSS 前先对照该 skill 的"设计系统速查"。

Usage:
    python3 gen-report.py <project_dir> [<project_dir> ...]  # 生成单项目报告 + 更新索引
    python3 gen-report.py --index                            # 仅从 registry 重建 index.html

Output:
    $CP_REPORT_DIR/projects/<slug>.html   单项目报告
    $CP_REPORT_DIR/index.html             多项目索引（卡片墙）
    $CP_REPORT_DIR/projects.json          registry（索引数据源）

Exit codes: 0 成功, 1 参数错误
"""

import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path(os.environ.get("CP_REPORT_DIR", "/opt/workdata/cp-reports"))
RAW_PROJECTS_ROOT = Path(os.environ.get(
    "CP_RAW_PROJECTS_ROOT", "/mnt/unraid_data/Obsidian/raw/projects"))

# 模板期望的文档清单（label, glob 相对项目目录, 必需?）
EXPECTED_DOCS = [
    ("overview.md", ["overview.md"]),
    ("ledger.md", ["ledger.md"]),
    ("tasks.md", ["tasks.md"]),
    ("PRODUCT.md", ["PRODUCT.md", "changes/*/PRODUCT.md"]),
    ("TECH.md", ["TECH.md", "changes/*/TECH.md"]),
    ("constitution.md", ["constitution.md", "changes/*/constitution.md", "source-of-truth/constitution.md"]),
    ("proposal.md", ["proposal.md", "changes/*/proposal.md"]),
    ("conversation.md", ["conversation.md", "changes/*/conversation.md"]),
    ("phase0-data.json", ["phase0-data.json", "changes/*/phase0-data.json"]),
    ("phase0-research.md", ["phase0-research.md", "changes/*/phase0-research.md"]),
    ("retrospective.md", ["retrospective.md", "changes/*/retrospective.md"]),
    ("completion-summary.md", ["completion-summary.md", "changes/*/completion-summary.md"]),
    ("handoff.md", ["handoff.md", "changes/*/handoff.md"]),
    ("briefs/ (Task Brief)", ["briefs/*.md"]),
    ("reviews/ (审查记录)", ["reviews/*.md"]),
    ("research/ (调研)", ["research/*.md"]),
]

PHASE_NAMES = {
    -1: "init", 0: "内化+扫描", 1: "需求澄清", 2: "方案设计", 3: "设计文档",
    4: "机械自检", 5: "实现计划", 6: "分发执行", 7: "归档复盘", 8: "反馈循环",
}

RAG_LABEL = {"green": "🟢 正常", "amber": "🟡 进行中", "red": "🔴 异常", "gray": "⚪ 未启动"}


# ---------------------------------------------------------------- utilities

def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def glob_files(root: Path, pattern: str) -> list[Path]:
    return sorted((p for p in root.glob(pattern) if p.is_file()),
                  key=lambda p: p.stat().st_mtime, reverse=True)


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Tolerant: no frontmatter → ({}, text)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        kv = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
        if kv:
            meta[kv.group(1)] = kv.group(2).strip().strip('"')
    return meta, text[m.end():]


def split_sections(md_text: str) -> list[tuple[str, str]]:
    """Split markdown body into [(heading, content), ...] on ## headings."""
    sections, current, buf = [], "(前言)", []
    for line in md_text.splitlines():
        if line.startswith("## "):
            sections.append((current, "\n".join(buf).strip()))
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    sections.append((current, "\n".join(buf).strip()))
    return [(h, c) for h, c in sections if c or h != "(前言)"]


# ---------------------------------------------------------------- scanning

def get_gate_state(project_dir: Path) -> dict:
    """Read phase completion from .phaseN.complete markers + gate-state JSON."""
    completed: dict[int, str] = {}
    for n in range(0, 9):
        marker = project_dir / f".phase{n}.complete"
        if marker.is_file():
            completed[n] = fmt_ts(marker.stat().st_mtime)
    # gate-state markers (written by gate scripts via gate_utils)
    try:
        import hashlib
        slug = hashlib.sha256(str(project_dir).rstrip("/").encode()).hexdigest()[:16]
        gate_dir = Path.home() / ".hermes" / "gate-state" / slug
        for mf in sorted(gate_dir.glob("*.json")):
            try:
                data = json.loads(mf.read_text(encoding="utf-8"))
                phase = data.get("phase", "")
                num = phase if isinstance(phase, int) else (
                    int(phase.replace("phase", "")) if str(phase).startswith("phase") else None)
                if num is not None and 0 <= num <= 8:
                    completed.setdefault(num, data.get("timestamp", fmt_ts(mf.stat().st_mtime)))
            except (json.JSONDecodeError, ValueError, OSError):
                continue
    except Exception:
        pass
    return completed


def scan_project(project_dir: Path) -> dict:
    """Gather everything the report needs. Pure filesystem facts."""
    d = {"dir": str(project_dir), "exists": project_dir.is_dir()}
    if not d["exists"]:
        return d

    init_file = project_dir / ".cp-init.json"
    init = {}
    if init_file.is_file():
        try:
            init = json.loads(read_text(init_file))
        except json.JSONDecodeError:
            init = {}
    d["init"] = init
    d["name"] = init.get("project_name") or project_dir.name
    d["slug"] = init.get("slug") or project_dir.name

    all_files = [p for p in project_dir.rglob("*") if p.is_file()]
    d["file_count"] = len(all_files)
    d["last_modified"] = max((p.stat().st_mtime for p in all_files), default=0)

    # overview
    ov_path = project_dir / "overview.md"
    ov_meta, ov_body = parse_front_matter(read_text(ov_path))
    d["overview_meta"] = ov_meta
    d["overview_sections"] = split_sections(ov_body) if ov_body else []
    d["overview_size"] = ov_path.stat().st_size if ov_path.is_file() else 0

    # phase state
    completed = get_gate_state(project_dir)
    d["phases"] = {n: completed.get(n) for n in range(0, 9)}
    if not (project_dir / ".cp-init.json").is_file():
        d["current_phase"] = None
    else:
        missing = [n for n in range(0, 9) if n not in completed]
        d["current_phase"] = missing[0] if missing else 8

    # ledger
    d["ledger_sections"] = split_sections(read_text(project_dir / "ledger.md"))

    # tasks.md checkbox stats
    tasks_text = read_text(project_dir / "tasks.md", 500_000)
    d["tasks_done"] = len(re.findall(r"^- \[x\]", tasks_text, re.M | re.I))
    d["tasks_open"] = len(re.findall(r"^- \[ \]", tasks_text, re.M))
    d["tasks_total"] = d["tasks_done"] + d["tasks_open"]

    # ledger Task 状态统计（tasks.md 无 checkbox 时的回退数据源）
    ledger_all = re.sub(r"<!--.*?-->", "", read_text(project_dir / "ledger.md"), flags=re.S)
    statuses = re.findall(r"^Task\s+\d+[^:\n]*:\s*([\w-]+)", ledger_all, re.M)
    if d["tasks_total"]:
        d["eff_done"], d["eff_total"] = d["tasks_done"], d["tasks_total"]
    else:
        d["eff_total"] = len(statuses)
        d["eff_done"] = sum(1 for s in statuses if s.lower() == "complete")

    # doc completeness matrix
    matrix = []
    for label, patterns in EXPECTED_DOCS:
        hits = []
        for pat in patterns:
            hits += glob_files(project_dir, pat)
        hits = sorted(set(hits))
        matrix.append({
            "label": label,
            "present": bool(hits),
            "count": len(hits),
            "newest": fmt_ts(hits[0].stat().st_mtime) if hits else "",
        })
    d["matrix"] = matrix
    d["docs_present"] = sum(1 for m in matrix if m["present"])
    d["docs_total"] = len(matrix)

    # changes/ iterations
    iterations = []
    for cdir in sorted((project_dir / "changes").glob("*"), reverse=True) \
            if (project_dir / "changes").is_dir() else []:
        if cdir.is_dir():
            cfiles = sorted(cdir.rglob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
            iterations.append({
                "name": cdir.name,
                "mtime": max((p.stat().st_mtime for p in cfiles), default=cdir.stat().st_mtime),
                "files": [{"name": str(p.relative_to(cdir)), "size": p.stat().st_size} for p in cfiles if p.is_file()],
            })
    d["iterations"] = iterations

    # research / reviews / briefs / worker-sessions counts + lists
    for sub in ("research", "reviews", "briefs"):
        sdir = project_dir / sub
        d[sub] = [{"name": p.name, "mtime": p.stat().st_mtime, "size": p.stat().st_size}
                  for p in glob_files(sdir, "*.md")] if sdir.is_dir() else []
    ws_dir = project_dir / "worker-sessions"
    d["worker_sessions"] = len(glob_files(ws_dir, "**/*.md")) if ws_dir.is_dir() else 0

    # recent activity: top 15 files by mtime
    d["recent"] = sorted(all_files, key=lambda p: p.stat().st_mtime, reverse=True)[:15]

    # RAG (mechanical rules)
    ledger_text = read_text(project_dir / "ledger.md")
    # 剔除模板注释后再判定，防止注释里的示例状态词（blocked/escalated）误报
    ledger_body = re.sub(r"<!--.*?-->", "", ledger_text, flags=re.S)
    if d["current_phase"] is None:
        rag = "gray"
    elif re.search(r"\bblocked\b|escalated", ledger_body, re.I):
        rag = "red"
    elif 7 in completed and 8 in completed:
        rag = "green"
    else:
        rag = "amber"
    d["rag"] = rag
    return d


# ---------------------------------------------------------------- rendering

CSS = """
:root{--bg:#f0f2f5;--surface:rgba(255,255,255,.65);--surface-solid:#fff;
--text:#1a1a2e;--text-secondary:#666;--accent:#4f46e5;--accent-hover:#4338ca;
--border:rgba(0,0,0,.08);--shadow:0 4px 24px rgba(0,0,0,.06);
--green:#16a34a;--amber:#d97706;--red:#dc2626;--purple:#7c3aed;--gray:#9ca3af}
*{box-sizing:border-box;margin:0;padding:0}
body{font:14px/1.65 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
background:var(--bg);color:var(--text);padding:28px 16px}
.wrap{max-width:980px;margin:0 auto}
.card{background:var(--surface);backdrop-filter:blur(12px);border:1.5px solid var(--border);
border-radius:14px;padding:18px 22px;margin-bottom:16px;box-shadow:var(--shadow)}
h1{font-size:22px;font-weight:700}
h2{font-size:15px;font-weight:700;margin-bottom:10px;padding-bottom:6px;
border-bottom:1.5px solid var(--border)}
.muted{color:var(--text-secondary);font-size:12px}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;
font-weight:600;border:1.5px solid var(--border);background:var(--surface-solid)}
.b-green{color:var(--green)}.b-amber{color:var(--amber)}.b-red{color:var(--red)}.b-gray{color:var(--gray)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-top:12px}
.kpi{background:var(--surface-solid);border:1.5px solid var(--border);border-radius:10px;
padding:10px 12px;text-align:center}
.kpi .v{font-size:20px;font-weight:700}
.kpi .l{font-size:11px;color:var(--text-secondary)}
.phases{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.ph{flex:1;min-width:86px;border:1.5px solid var(--border);border-radius:8px;
padding:6px 8px;text-align:center;background:var(--surface-solid);font-size:11px}
.ph.done{border-color:var(--green);color:var(--green)}
.ph.cur{border-color:var(--accent);color:var(--accent);font-weight:700}
.ph .n{font-weight:700;font-size:13px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--border)}
th{color:var(--text-secondary);font-weight:600;font-size:12px}
.ok{color:var(--green);font-weight:700}.miss{color:var(--red);font-weight:700}
pre{white-space:pre-wrap;word-break:break-all;font:12px/1.6 ui-monospace,Menlo,Consolas,monospace;
background:var(--surface-solid);border:1.5px solid var(--border);border-radius:8px;padding:10px 12px}
.tl{border-left:2px solid var(--border);margin-left:8px;padding-left:16px}
.tl-item{margin-bottom:14px;position:relative}
.tl-item::before{content:"";position:absolute;left:-21px;top:6px;width:9px;height:9px;
border-radius:50%;background:var(--accent);border:2px solid var(--surface-solid)}
a{color:var(--accent);text-decoration:none}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:720px){.grid2{grid-template-columns:1fr}}
.footer{text-align:center;color:var(--text-secondary);font-size:11px;margin-top:20px}
.pill{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11px;
border:1px solid var(--border);background:var(--surface-solid);color:var(--text-secondary);margin-right:4px}
details{margin:6px 0;border:1px solid var(--border);border-radius:8px;padding:8px 12px;background:var(--surface-solid)}
summary{cursor:pointer;font-weight:600;font-size:13px}
ul{margin:4px 0 4px 18px}li{margin:2px 0}
code{background:rgba(0,0,0,.05);padding:1px 5px;border-radius:4px;font:12px ui-monospace,Menlo,monospace}
.navbar{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}
.navbar a{font-size:12px;padding:3px 10px;border:1.5px solid var(--border);border-radius:999px;
background:var(--surface-solid);color:var(--text)}
"""


def render_head(title: str) -> str:
    return (f"<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body><div class=\"wrap\">")


def render_foot(note: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (f"<div class=\"footer\">{esc(note)} · 生成时间 {now} · "
            f"gen-report.py v1（生成物，永不手改；重新生成即更新）</div></div></body></html>")


def render_phases(phases: dict, current) -> str:
    cells = []
    for n in range(0, 9):
        cls = "ph done" if phases.get(n) else ("ph cur" if n == current else "ph")
        when = phases.get(n)
        sub = f"<div class=\"muted\">{esc(when[:10] if when else PHASE_NAMES[n])}</div>"
        cells.append(f"<div class=\"{cls}\"><div class=\"n\">P{n}</div>{sub}</div>")
    return "<div class=\"phases\">" + "".join(cells) + "</div>"


def find_latest(root: Path, patterns: list[str]) -> Path | None:
    """按优先级/最新 mtime 找文档。"""
    hits = []
    for pat in patterns:
        hits += glob_files(root, pat)
    return hits[0] if hits else None


def render_md_lite(text: str) -> str:
    """轻量 markdown 渲染：粗体/行内代码/列表；表格保留为 pre（保证对齐）。"""
    out, in_list, in_pre = [], False, False
    for line in text.splitlines():
        s = esc(line)
        if s.startswith("|"):
            if not in_pre:
                out.append("<pre>")
                in_pre = True
            out.append(s + "\n")
            continue
        if in_pre:
            out.append("</pre>")
            in_pre = False
        m = re.match(r"^\s*[-*]\s+(.*)$", s)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            item = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", m.group(1))
            item = re.sub(r"`([^`]+)`", r"<code>\1</code>", item)
            out.append(f"<li>{item}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if s.startswith("#"):
            continue  # 章节标题由调用方渲染为 summary
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        out.append(f"<div>{s or '&nbsp;'}</div>")
    if in_list:
        out.append("</ul>")
    if in_pre:
        out.append("</pre>")
    return "".join(out)


def render_doc_card(card_id: str, title: str, path: Path | None,
                    per_sec: int = 900, max_secs: int = 14) -> str:
    """把一个 markdown 文档渲染为章节折叠卡片（内容区核心）。"""
    if not path or not path.is_file():
        return ""
    _, body = parse_front_matter(read_text(path))
    secs = split_sections(body)
    if not secs:
        return ""
    blocks = []
    for h, c in secs[:max_secs]:
        snippet = c[:per_sec] + ("…" if len(c) > per_sec else "")
        if not snippet.strip():
            continue
        blocks.append(f"<details><summary>{esc(h)}</summary>"
                      f"<div style=\"margin-top:8px\">{render_md_lite(snippet)}</div></details>")
    more = f"<div class=\"muted\">…共 {len(secs)} 章节，仅渲染前 {max_secs} 个</div>" if len(secs) > max_secs else ""
    return (f"<div class=\"card\" id=\"{esc(card_id)}\"><h2>{esc(title)} "
            f"<span class=\"muted\">{esc(path.name)} · {len(secs)} 章节</span></h2>"
            f"{''.join(blocks)}{more}</div>")


def render_reviews_summary(root: Path, reviews: list[dict]) -> str:
    """reviews/ 审查结论汇总：每份提取标题+结论行。"""
    if not reviews:
        return ""
    rows = []
    for f in reviews[:20]:
        txt = read_text(root / "reviews" / f["name"], 30_000)
        m = re.search(r"结论[:：]\s*\*{0,2}([^<\n*]+)", txt)
        concl = m.group(1).strip() if m else "—"
        rows.append(f"<tr><td>{esc(f['name'].removesuffix('.md'))}</td>"
                    f"<td>{esc(concl[:150])}</td>"
                    f"<td class=\"muted\">{fmt_ts(f['mtime'])}</td></tr>")
    more = f"<div class=\"muted\">共 {len(reviews)} 份，展示最近 20 份</div>" if len(reviews) > 20 else ""
    return (f"<div class=\"card\" id=\"sec-reviews\"><h2>审查结论汇总"
            f"<span class=\"muted\">reviews/ · {len(reviews)} 份</span></h2>"
            f"<table><tr><th>审查</th><th>结论</th><th>时间</th></tr>{''.join(rows)}</table>{more}</div>")


def render_project_html(d: dict) -> str:
    name, rag = d["name"], d["rag"]
    parts = [render_head(f"{name} — 项目报告")]

    # Header
    cur = d.get("current_phase")
    cur_label = "全部完成" if cur == 8 and d["phases"].get(8) else (
        f"Phase {cur} · {PHASE_NAMES.get(cur, '')}" if cur is not None else "未初始化")
    parts.append(f"""
<div class="card">
  <div class="row" style="justify-content:space-between">
    <div>
      <h1>{esc(name)}</h1>
      <div class="muted">{esc(d['dir'])} · slug: {esc(d['slug'])} · 文件 {d['file_count']} 个 ·
      最后活动 {fmt_ts(d['last_modified']) if d['last_modified'] else '-'}</div>
    </div>
    <span class="badge b-{rag}">{RAG_LABEL[rag]}</span>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="v">{esc(cur_label.split(' · ')[0])}</div><div class="l">当前阶段</div></div>
    <div class="kpi"><div class="v">{d['eff_done']}/{d['eff_total']}</div><div class="l">任务完成</div></div>
    <div class="kpi"><div class="v">{d['docs_present']}/{d['docs_total']}</div><div class="l">文档完整度</div></div>
    <div class="kpi"><div class="v">{len(d['iterations'])}</div><div class="l">迭代轮次</div></div>
    <div class="kpi"><div class="v">{len(d['reviews'])}</div><div class="l">审查记录</div></div>
    <div class="kpi"><div class="v">{d['worker_sessions']}</div><div class="l">Worker会话</div></div>
  </div>
  {render_phases(d['phases'], cur)}
</div>""")

    # Goal / overview sections
    if d["overview_sections"]:
        goal_secs = [s for s in d["overview_sections"]
                     if re.search(r"目标|goal|目的|purpose|简介|状态", s[0], re.I)][:4]
        body = "".join(
            f"<h2 style=\"border:none;margin:12px 0 4px;padding:0;font-size:13px;color:var(--text-secondary)\">{esc(h)}</h2>"
            f"<div style=\"white-space:pre-wrap\">{esc(c[:900])}</div>" for h, c in goal_secs)
        status = d["overview_meta"].get("status", "")
        parts.append(f"<div class=\"card\"><h2>目标摘要（源自 overview.md"
                     f"{' · ' + esc(status) if status else ''}）</h2>{body}</div>")

    # ---- 深度内容区：需求范围 / 实施方案 / 约束 / 调研 / 任务 / 审查（机械提取文档正文）----
    root = Path(d["dir"])
    deep_cards = [
        ("sec-product", "需求范围（用户故事 / 不变量 / 范围外）",
         ["PRODUCT.md", "changes/*/PRODUCT.md"], 1000, 14),
        ("sec-tech", "技术方案（方案对比 / 架构 / 核心设计 / 分期）",
         ["TECH.md", "changes/*/TECH.md"], 1000, 14),
        ("sec-proposal", "设计方案与决策（proposal.md）",
         ["proposal.md", "changes/*/proposal.md"], 900, 14),
        ("sec-constitution", "宪法约束（不变量 / 禁止操作 / 验收标准）",
         ["constitution.md", "changes/*/constitution.md", "source-of-truth/constitution.md"], 800, 12),
        ("sec-research", "调研结论（phase0 / research REPORT）",
         ["research/REPORT.md", "phase0-research.md", "changes/*/phase0-research.md"], 900, 12),
        ("sec-tasks", "任务计划（tasks.md 波次与任务）",
         ["tasks.md"], 500, 10),
    ]
    nav_html, deep_html = [], []
    for cid, title, patterns, per_sec, max_secs in deep_cards:
        p = find_latest(root, patterns)
        if p:
            nav_html.append(f"<a href=\"#{cid}\">{esc(title.split('（')[0])}</a>")
        deep_html.append(render_doc_card(cid, title, p, per_sec, max_secs))
    rev = render_reviews_summary(root, d.get("reviews", []))
    if rev:
        nav_html.append("<a href=\"#sec-reviews\">审查结论</a>")
    deep_html.append(rev)
    parts.append(f"<div class=\"navbar\" id=\"sec-nav\">{''.join(nav_html)}</div>")
    parts.append("".join(deep_html))

    # Doc completeness
    rows = "".join(
        f"<tr><td>{esc(m['label'])}</td>"
        f"<td class={'ok' if m['present'] else 'miss'}>{'✓ ' + str(m['count']) + ' 个' if m['present'] else '✗ 缺失'}</td>"
        f"<td class=\"muted\">{esc(m['newest'])}</td></tr>"
        for m in d["matrix"])
    parts.append(f"""
<div class="card"><h2>文档完整度矩阵（模板期望 vs 实际存在）</h2>
<table><tr><th>文档</th><th>状态</th><th>最新修改</th></tr>{rows}</table></div>""")

    # Ledger
    if d["ledger_sections"]:
        secs = "".join(
            f"<h2 style=\"border:none;margin:12px 0 4px;padding:0;font-size:13px;color:var(--text-secondary)\">{esc(h)}</h2>"
            f"<pre>{esc(c[:2500])}</pre>"
            for h, c in d["ledger_sections"][:8])
        parts.append(f"<div class=\"card\"><h2>Ledger（跨 compaction 进度追踪）</h2>{secs}</div>")

    # Changes timeline
    if d["iterations"]:
        items = []
        for it in d["iterations"]:
            flist = "".join(f"<span class=\"pill\">{esc(f['name'])}</span>" for f in it["files"][:12])
            more = f"<span class=\"pill\">+{len(it['files']) - 12} more</span>" if len(it["files"]) > 12 else ""
            items.append(f"<div class=\"tl-item\"><b>{esc(it['name'])}</b> "
                         f"<span class=\"muted\">{fmt_ts(it['mtime'])} · {len(it['files'])} 文件</span>"
                         f"<div style=\"margin-top:4px\">{flist}{more}</div></div>")
        parts.append(f"<div class=\"card\"><h2>迭代时间线（changes/）</h2>"
                     f"<div class=\"tl\">{''.join(items)}</div></div>")

    # research / reviews / briefs
    idx = []
    for sub, label, color in (("research", "调研 research/", "var(--purple)"),
                              ("reviews", "审查 reviews/", "var(--amber)"),
                              ("briefs", "任务简报 briefs/", "var(--accent)")):
        if d.get(sub):
            flist = "".join(
                f"<div>{esc(f['name'])} <span class=\"muted\">{fmt_ts(f['mtime'])}</span></div>"
                for f in d[sub][:14])
            idx.append(f"<div><h2 style=\"color:{color}\">{label}（{len(d[sub])}）</h2>{flist}</div>")
    if idx:
        parts.append(f"<div class=\"card\"><div class=\"grid2\">{''.join(idx)}</div></div>")

    # Recent activity
    rec = "".join(
        f"<tr><td>{esc(str(p.relative_to(d['dir'])))}</td>"
        f"<td class=\"muted\">{fmt_ts(p.stat().st_mtime)}</td>"
        f"<td class=\"muted\">{p.stat().st_size / 1024:.1f}K</td></tr>"
        for p in d["recent"])
    parts.append(f"<div class=\"card\"><h2>近期活动（最近 15 个文件）</h2>"
                 f"<table><tr><th>文件</th><th>修改时间</th><th>大小</th></tr>{rec}</table></div>")

    parts.append(render_foot("clsh-project 项目总体报告"))
    return "".join(parts)


def render_index_html(registry: list[dict]) -> str:
    parts = [render_head("clsh-project 项目总览")]
    cards = []
    for r in sorted(registry, key=lambda x: x.get("last_modified", 0), reverse=True):
        rag = r.get("rag", "gray")
        cur = r.get("current_phase")
        cur_l = f"P{cur} {PHASE_NAMES.get(cur, '')}" if cur is not None else "未初始化"
        cards.append(f"""
<div class="card" style="margin-bottom:12px">
  <div class="row" style="justify-content:space-between">
    <div><a href="projects/{esc(r['slug'])}.html"><b>{esc(r['name'])}</b></a>
      <div class="muted">{esc(r['dir'])} · 文件 {r.get('file_count', '?')} ·
      最后活动 {fmt_ts(r['last_modified']) if r.get('last_modified') else '-'}</div></div>
    <div class="row"><span class="badge">{esc(cur_l)}</span>
      <span class="badge b-{rag}">{RAG_LABEL[rag]}</span></div>
  </div>
</div>""")
    parts.append(f"<h1 style=\"margin-bottom:4px\">clsh-project 项目总览</h1>"
                 f"<div class=\"muted\" style=\"margin-bottom:16px\">{len(registry)} 个项目 · "
                 f"点击进入单项目报告</div>{''.join(cards)}")
    parts.append(render_foot("clsh-project 项目索引"))
    return "".join(parts)


# ---------------------------------------------------------------- main

def load_registry() -> list[dict]:
    f = REPORT_DIR / "projects.json"
    if f.is_file():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_registry(registry: list[dict]) -> None:
    (REPORT_DIR / "projects.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=1), encoding="utf-8")


def generate(project_dir: Path) -> Path:
    d = scan_project(project_dir)
    out_dir = REPORT_DIR / "projects"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{d['slug']}.html"
    out.write_text(render_project_html(d), encoding="utf-8")

    registry = [r for r in load_registry() if r.get("dir") != d["dir"]]
    registry.append({
        "dir": d["dir"], "slug": d["slug"], "name": d["name"], "rag": d["rag"],
        "current_phase": d.get("current_phase"), "file_count": d["file_count"],
        "last_modified": d["last_modified"],
    })
    save_registry(registry)
    (REPORT_DIR / "index.html").write_text(render_index_html(registry), encoding="utf-8")
    return out


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    args = sys.argv[1:]
    if not args:
        print("Usage: gen-report.py <project_dir> [...] | --index", file=sys.stderr)
        return 1
    if args == ["--index"]:
        (REPORT_DIR / "index.html").write_text(render_index_html(load_registry()), encoding="utf-8")
        print(str(REPORT_DIR / "index.html"))
        return 0
    for a in args:
        p = Path(a).expanduser().resolve()
        if not p.is_dir():
            print(f"skip (not a dir): {a}", file=sys.stderr)
            continue
        out = generate(p)
        print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
