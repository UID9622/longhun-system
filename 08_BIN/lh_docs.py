#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""龍魂 · 对外文档一体化引擎 v2.0（lh docs）

DNA: #龍芯⚡️2026-09-05-lh-docs-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

lh docs <check|sync|version|stats|feedback|weekly|audit|feedback-form> [--json] [--audit] [--all] [--days N]
  check         体检 12_DOCS 与系统一致性 · 不一致 🟡 自动标记 · exit 1
  sync          同步交付文档版本行 + 重生成命令总表（调 lh doc-sync）
  version       打印 docs_version（v5.2.0 与系统主干联动）
  stats         统计文档站最近 7 天访问（鲲鹏 nginx 日志 → MD 表格 · --days N 调窗口）
  feedback      汇总耻辱墙中与文档相关反馈 · 按 docs/question/suggestion/bug 分类 · --all 扫全量
  weekly        周报生成（访问统计+反馈+待处理 → ~/.longhun/docs_feedback_weekly.md + 反馈报告_<日期>.md · 自动 GPG 签）
  audit         文档站三色审计（内容一致性/首页DNA/页面GPG/未授权改动 → 耻辱墙 docs_audit + 归档日志）
  feedback-form 生成耻辱墙反馈表单链接（指向 shame_report.yml 模板 · 供文档站底部接入）
  check --audit  在体检基础上追加文档站审计
数据: ~/.longhun/docs_feedback_weekly.md · ~/.longhun/audit/docs_audit.log
"""
import argparse
import ast
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LH_PY = ROOT / "08_BIN" / "lh.py"
USAGE_MD = ROOT / "12_DOCS" / "USAGE.md"
SITE_DIR = ROOT / "docs-site" / "docs"
HOME = Path.home()

sys.path.insert(0, str(ROOT / "08_BIN"))
from lh_doc_sync import DELIVERY_DOCS, DOCS_VERSION, bump_delivery_versions  # noqa: E402

# ── 任务3/4 常量（2026-09-05 焊入）─────────────────────────────
KUNPENG_IP = "119.13.90.27"
NGINX_LOG = "/var/log/nginx/access.log"
SHAME_JSON = HOME / ".longhun" / "shame_wall" / "shame_wall.json"
WEEKLY_MD = HOME / ".longhun" / "docs_feedback_weekly.md"
AUDIT_LOG = HOME / ".longhun" / "audit" / "docs_audit.log"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

HEAD_REQUIRED = ["DNA: ", "创建者: ", "归属名: ", "协议: "]
DNA_DATE_RE = re.compile(r"#龍(?:芯|帳)⚡️[^\n]*?(\d{4}-\d{2}-\d{2})")
VERSION_LINE_RE = re.compile(r"^> 文档版本:")
NGINX_RE = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d{3}) \S+ "([^"]*)"')
MONTH = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
# lh.py 特殊入口（非 SUB_DISPATCH 子命令但真实可跑）
LH_SPECIAL_ENTRIES = {"ask", "chat", "auto", "console", "dashboard", "health",
                      "engine", "audit", "push", "personas"}
PAGE_NAV = {"dependencies": "DEPENDENCIES", "install": "INSTALL", "quickstart": "QUICKSTART",
            "usage": "USAGE", "api-reference": "API_REFERENCE", "jsonrpc": "JSONRPC",
            "mcp-guide": "MCP_GUIDE", "notion-mcp-guide": "NOTION_MCP_GUIDE",
            "troubleshooting": "TROUBLESHOOTING"}


def _ssh(cmd: str, timeout: int = 25) -> str:
    try:
        p = subprocess.run(
            ["ssh", "-i", str(HOME / ".ssh" / "longhun_kunpeng_ed25519"),
             "-o", "ConnectTimeout=8", "-o", "StrictHostKeyChecking=no",
             f"root@{KUNPENG_IP}", cmd],
            capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:  # noqa: BLE001
        return ""


def _doc_date(p: Path):
    try:
        m = DNA_DATE_RE.search(p.read_text(encoding="utf-8", errors="ignore")[:900])
        return m.group(1) if m else None
    except Exception:  # noqa: BLE001
        return None


def _file_md5(p: Path) -> str:
    try:
        return hashlib.md5(p.read_bytes()).hexdigest()
    except Exception:  # noqa: BLE001
        return ""


def _extract_commands() -> set:
    """从 lh.py SUB_DISPATCH 提取真实命令集合（与 lh doc-sync 同解析口径）"""
    try:
        tree = ast.parse(LH_PY.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return set()
    out = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "SUB_DISPATCH":
                    val = node.value
                    if isinstance(val, ast.Dict):
                        for k in (val.keys or []):
                            if isinstance(k, ast.Constant):
                                out.add(str(k.value))
                    elif isinstance(val, ast.List):
                        for elt in (val.elts or []):
                            if isinstance(elt, ast.Tuple) and elt.elts and isinstance(elt.elts[0], ast.Constant):
                                out.add(str(elt.elts[0].value))
    return out


# ══════════════════ check（任务C v5.2.0 基础）══════════════════

def check_docs(json_out: bool = False) -> int:
    issues = []
    today = datetime.date.today().strftime("%Y-%m-%d")
    real_cmds = _extract_commands()

    for rel in DELIVERY_DOCS:
        p = ROOT / rel
        if not p.exists():
            issues.append((rel, "missing", "文档缺失"))
            continue
        head = p.read_text(encoding="utf-8", errors="ignore").split("\n")[:12]
        for hk in HEAD_REQUIRED:
            if not any(hk in line for line in head[:6]):
                issues.append((rel, "header", f"头部缺「{hk.rstrip(': ')}」"))
        if not Path(str(p) + ".asc").exists():
            issues.append((rel, "sign", "GPG 签名 .asc 缺失"))
        d = _doc_date(p)
        if d is None:
            issues.append((rel, "dna_date", "DNA 时间戳缺失"))
        elif d > today:
            issues.append((rel, "dna_date", f"DNA 时间戳指向未来日期 {d}"))
        ver = [line for line in head if VERSION_LINE_RE.match(line)]
        if not ver:
            issues.append((rel, "version", f"头部缺版本行 → 运行 lh docs sync（当前 {DOCS_VERSION}）"))
        elif DOCS_VERSION not in ver[0]:
            issues.append((rel, "version",
                           f"版本行 {ver[0].split(':', 1)[1].strip()} ≠ 系统 {DOCS_VERSION}"))

    if USAGE_MD.exists():
        doc_cmds = set(re.findall(r"`lh ([a-z][a-z0-9-]*)`", USAGE_MD.read_text(encoding="utf-8")))
        doc_only = sorted((doc_cmds - real_cmds) - LH_SPECIAL_ENTRIES)
        if doc_only:
            issues.append(("USAGE.md", "cmd", "文档提及但 lh.py 无此命令: " + ", ".join(doc_only)))

    if SITE_DIR.exists():
        for rel in DELIVERY_DOCS:
            name = Path(rel).name
            sp = SITE_DIR / name
            if not sp.exists():
                continue
            sd, td = _doc_date(sp), _doc_date(ROOT / rel)
            if td and sd and sd != td:
                issues.append((f"docs-site/docs/{name}", "site",
                               f"站点副本 DNA {sd} ≠ 源 {td} → 需重建/重部署站点"))

    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "check", "docs_version": DOCS_VERSION,
                          "consistent": not issues, "issue_count": len(issues),
                          "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if issues:
            print(f"🟡 待更新 {len(issues)} 项（docs_version={DOCS_VERSION}）:")
            for rel, kind, detail in issues:
                print(f"  🟡 {rel} [{kind}] {detail}")
        else:
            print(f"🟢 docs check 通过 · {len(DELIVERY_DOCS)} 份交付文档与系统全一致（docs_version={DOCS_VERSION}）")
    return 1 if issues else 0


def cmd_sync(json_out: bool = False) -> int:
    bumped = bump_delivery_versions()
    r = subprocess.run([sys.executable, str(ROOT / "08_BIN" / "lh_doc_sync.py")],
                       capture_output=True, text=True, timeout=120)
    info = {"tool": "lh-docs", "mode": "sync", "docs_version": DOCS_VERSION,
            "bumped": bumped, "doc_sync": r.stdout.strip()}
    if r.returncode != 0:
        info["doc_sync_error"] = r.stderr.strip()
    if json_out:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(f"🟢 lh docs sync 完成 · bumped {len(bumped)} 份 · doc-sync exit {r.returncode}")
        for b in bumped:
            print(f"  · {b}")
    return 0 if r.returncode == 0 else 1


def cmd_version(json_out: bool = False) -> int:
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "version", "docs_version": DOCS_VERSION}))
    else:
        print(DOCS_VERSION)
    return 0


# ══════════════════ stats（任务3 · nginx 访问统计）══════════════

def _collect_stats(days: int = 7):
    """拉鲲鹏 nginx 日志 → 统计。ssh 失败返回 None。"""
    raw = _ssh(f"grep '/docs/' {NGINX_LOG} 2>/dev/null")
    if not raw:
        return None
    today = datetime.date.today()
    rows = []  # (page, referer_host)
    for line in raw.splitlines():
        m = NGINX_RE.match(line)
        if not m:
            continue
        ip, ts, method, path, status, ref = m.groups()
        if method != "GET" or not path.startswith("/docs/"):
            continue
        if status not in ("200", "301", "302", "304"):
            continue
        # 静态资源与搜索索引不计入页面访问
        if re.search(r"\.(png|css|js|svg|ico|woff2?|ttf|jpg|jpeg|webp|map)$", path):
            continue
        if "/docs/search/" in path or path == "/docs/search":
            continue
        # 7 天窗口过滤
        try:
            t = datetime.datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z").date()
        except ValueError:
            continue
        if (today - t).days > days:
            continue
        page = path.rstrip("/") if path != "/docs/" else "/docs/"
        host = ""
        if ref and ref != "-":
            try:
                host = urllib.parse.urlsplit(ref).netloc or "(站内)"
            except Exception:  # noqa: BLE001
                host = "(未知)"
        rows.append((page, host))
    if not rows:
        return {"total": 0, "days": days, "top_pages": [], "sources": [], "daily": []}
    pages = {}
    for page, _ in rows:
        pages[page] = pages.get(page, 0) + 1
    sources = {}
    for _, host in rows:
        key = "直接访问" if not host else ("站内跳转" if host in ("uid9622.cn", "www.uid9622.cn", "(站内)")
                                        else "GitHub" if "github" in host else host)
        sources[key] = sources.get(key, 0) + 1
    return {"total": len(rows), "days": days,
            "top_pages": sorted(pages.items(), key=lambda x: -x[1])[:5],
            "sources": sorted(sources.items(), key=lambda x: -x[1]),
            "daily": len(rows)}


def cmd_stats(json_out: bool = False, days: int = 7) -> int:
    st = _collect_stats(days)
    if st is None:
        print("🟡 docs stats 失败：无法连接鲲鹏或 nginx 日志不可达（ssh root@119.13.90.27 检查）")
        return 1
    if st["total"] == 0:
        if json_out:
            print(json.dumps({"tool": "lh-docs", "mode": "stats", "days": days,
                              "total": 0, "message": "近 7 天无 /docs/ 页面访问"}))
        else:
            print(f"🟡 docs stats：近 {days} 天无 /docs/ 页面访问记录（日志 {NGINX_LOG}）")
        return 0
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "stats", "days": days,
                          "total": st["total"], "top_pages": st["top_pages"],
                          "sources": st["sources"]}, ensure_ascii=False, indent=2))
    else:
        print(f"🟢 docs stats · 近 {days} 天 /docs/ 页面访问统计")
        print(f"\n| 页面 | 访问量 |")
        print(f"|:---|---:|")
        for p, c in st["top_pages"]:
            print(f"| {p} | {c} |")
        print(f"\n| 来源渠道 | 次数 |")
        print(f"|:---|---:|")
        for s, c in st["sources"]:
            print(f"| {s} | {c} |")
        print(f"\n共 {st['total']} 次页面访问（排除静态资源）")
    return 0


# ══════════════════ feedback（任务3 · 耻辱墙反馈汇总）══════════

FEED_TAG_RE = [
    ("docs", re.compile(r"docs|文档|documentation", re.I)),
    ("question", re.compile(r"question|问|疑问|求助|help|how", re.I)),
    ("suggestion", re.compile(r"suggestion|建议|提个|想法|improve", re.I)),
    ("bug", re.compile(r"bug|故障|异常|错误|error|fail|坏", re.I)),
]


def _feed_tag(text: str) -> str:
    for tag, rx in FEED_TAG_RE:
        if rx.search(text):
            return tag
    return "other"


def _collect_feedback(days: int | None = 30):
    """读耻辱墙 → 文档相关反馈分类。days=None 扫全量；无文件/无记录返回空集。"""
    out = {"count": 0, "by_tag": {}, "items": []}
    if not SHAME_JSON.exists():
        return out
    try:
        d = json.loads(SHAME_JSON.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return out
    today = datetime.date.today()
    for rec in d.get("记录", []):
        if not isinstance(rec, dict):
            continue
        text = json.dumps(rec, ensure_ascii=False)
        # 只关注与文档站点/交付文档相关
        if not re.search(r"docs|文档|uid9622\.cn/docs|documentation", text, re.I):
            continue
        date_s = rec.get("date") or rec.get("time", "")[:10]
        if days is not None:
            try:
                if (today - datetime.date.fromisoformat(date_s)).days > days:
                    continue
            except Exception:  # noqa: BLE001
                pass
        tag = _feed_tag(text)
        out["by_tag"][tag] = out["by_tag"].get(tag, 0) + 1
        out["items"].append({"date": date_s, "tag": tag,
                             "title": str(rec.get("title") or rec.get("reason") or rec.get("type") or "")[:120]})
        out["count"] += 1
    return out


def cmd_feedback(json_out: bool = False, all_records: bool = False) -> int:
    fb = _collect_feedback(None if all_records else 30)
    window = "全量" if all_records else "近 30 天"
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "feedback", "window": window,
                          "count": fb["count"], "by_tag": fb["by_tag"], "items": fb["items"]},
                         ensure_ascii=False, indent=2))
    else:
        if fb["count"] == 0:
            print(f"🟢 docs feedback（{window}）：耻辱墙无文档相关反馈（记录保持 0）")
        else:
            print(f"🟡 docs feedback（{window}）· 文档相关反馈 {fb['count']} 条")
            print("\n| 分类 | 数量 |")
            print("|:---|---:|")
            for t in ["docs", "question", "suggestion", "bug", "other"]:
                if fb["by_tag"].get(t):
                    print(f"| {t} | {fb['by_tag'][t]} |")
            for it in fb["items"]:
                print(f"  · [{it['tag']}] {it['date']} {it['title']}")
    return 0


# ══════════════════ weekly（任务3 · 每周报告自动生成）══════════

def _build_weekly() -> str:
    now = datetime.datetime.now()
    st = _collect_stats(7)
    fb = _collect_feedback(30)
    L = []
    L.append("# 🐉 龍魂文档站 · 每周反馈报告")
    L.append(f"\n> 生成时间: {now.strftime('%Y-%m-%d %H:%M')} · 工具: lh docs weekly")
    L.append(f"> DNA: #龍芯⚡️{now.strftime('%Y-%m-%d')}-DOCS-WEEKLY-UID9622")
    L.append(f"> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n")
    L.append("## 一、访问统计（近 7 天）")
    if st is None:
        L.append("\n🟡 无法连接鲲鹏获取 nginx 日志。")
    elif st["total"] == 0:
        L.append("\n近 7 天无 /docs/ 页面访问。")
    else:
        L.append(f"\n共 **{st['total']}** 次页面访问。\n")
        L.append("| 页面 | 访问量 |")
        L.append("|:---|---:|")
        for p, c in st["top_pages"]:
            L.append(f"| `{p}` | {c} |")
        L.append("\n| 来源渠道 | 次数 |")
        L.append("|:---|---:|")
        for s, c in st["sources"]:
            L.append(f"| {s} | {c} |")
    L.append("\n## 二、反馈列表（耻辱墙 · 近 30 天文档相关）")
    if fb["count"] == 0:
        L.append("\n暂无文档相关反馈。")
    else:
        L.append(f"\n共 {fb['count']} 条。\n")
        L.append("| 日期 | 分类 | 标题 |")
        L.append("|:---|:---|:---|")
        for it in fb["items"]:
            L.append(f"| {it['date']} | {it['tag']} | {it['title']} |")
    L.append("\n## 三、待处理事项与迭代建议")
    todo = []
    q = fb["by_tag"].get("question", 0)
    if q >= 3:
        todo.append(f"🟡 有 {q} 个同类问题 → 考虑在文档站 FAQ/对应文档补充条目（3 人以上同问自动加 FAQ 规则触发）")
    if fb["by_tag"].get("bug", 0):
        todo.append(f"🟡 有 {fb['by_tag'].get('bug', 0)} 条 bug 反馈 → 先跑 `lh docs check` 排除文档与系统不一致，再人工核对")
    pages_low = ""
    if st and st["top_pages"] and st["total"] >= 5:
        low = [p for p, _ in st["top_pages"] if _ == 1]
        if low:
            todo.append(f"🟡 低访问页面 {low} → 考虑合并或优化入口")
    if not todo:
        todo.append("🟢 无待处理 · 持续观察一周")
    for t in todo:
        L.append(f"- {t}")
    L.append("\n> 本报告自动生成并 GPG 签名 · 数据：nginx access.log + 耻辱墙 · 引擎 `lh docs weekly`")
    return "\n".join(L)


def cmd_weekly(json_out: bool = False) -> int:
    """周报双落：docs_feedback_weekly.md（引擎常规名）+ 反馈报告_<日期>.md（任务A命名）"""
    md = _build_weekly()
    WEEKLY_MD.parent.mkdir(parents=True, exist_ok=True)
    report_md = HOME / ".longhun" / f"反馈报告_{datetime.date.today().strftime('%Y-%m-%d')}.md"
    WEEKLY_MD.write_text(md, encoding="utf-8")
    report_md.write_text(md, encoding="utf-8")
    # 自动 GPG 分离签名（复用 lh_gpg_sign 引擎）
    r = subprocess.run([sys.executable, str(ROOT / "08_BIN" / "lh_gpg_sign.py"),
                        "sign", "--force", str(WEEKLY_MD), str(report_md)],
                       capture_output=True, text=True, timeout=60)
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "weekly", "output": str(WEEKLY_MD),
                          "feedback_report": str(report_md),
                          "signed": r.returncode == 0}, ensure_ascii=False, indent=2))
    else:
        print(f"🟢 docs weekly 已生成 → {WEEKLY_MD}")
        print(f"🟢 反馈报告 → {report_md}" + ("（GPG 已签）" if r.returncode == 0 else "（签名失败）"))
    return 0


def cmd_feedback_form(json_out: bool = False) -> int:
    """生成耻辱墙反馈表单链接（指向 .github/ISSUE_TEMPLATE/shame_report.yml）"""
    base = "https://github.com/UID9622/longhun-system/issues/new"
    url = base + "?template=shame_report.yml&labels=docs-feedback&title=" + urllib.parse.quote("[文档反馈] ")
    md_block = (
        "💬 发现文档问题？请通过耻辱墙提交 → [耻辱墙反馈表单](" + url + ")\n"
        "   - 附上所在页面与 DNA 追溯码（页面底部），便于溯源修复\n"
        "   - 每 3 人以上同类反馈将自动进入 FAQ 建议（引擎 `lh docs weekly`）")
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "feedback-form",
                          "template": ".github/ISSUE_TEMPLATE/shame_report.yml",
                          "url": url, "markdown": md_block}, ensure_ascii=False, indent=2))
    else:
        print("💬 耻辱墙反馈表单（指向 shame_report.yml 模板）")
        print("链接: " + url)
        print("\n供文档站底部/扩散素材粘贴的 Markdown 片段:\n")
        print(md_block)
    return 0


# ══════════════════ audit（任务4 · 文档站三色审计）═════════════

def _append_shame(entry: dict):
    """耻辱墙 append-only（schema v1.1: version/生成时间/总记录数/记录）"""
    try:
        d = json.loads(SHAME_JSON.read_text(encoding="utf-8")) if SHAME_JSON.exists() else {
            "version": 1.1, "生成时间": datetime.datetime.now().isoformat(), "总记录数": 0, "记录": []}
        d.setdefault("记录", [])
        d["记录"].append(entry)
        d["总记录数"] = len(d["记录"])
        SHAME_JSON.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def _append_audit_log(line: str):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def audit_site(json_out: bool = False):
    """文档站三色审计。返回 (findings, color)。写入耻辱墙 docs_audit 事件 + 归档日志。"""
    findings = []  # (severity 0 ok / 1 warn / 2 bad, item, detail)
    today = datetime.date.today()
    # 1) 站点内容 vs 12_DOCS 源（一致性 · 仅比对站点实际收录的文档）
    for rel in DELIVERY_DOCS:
        src = ROOT / rel
        name = Path(rel).name
        sp = SITE_DIR / name
        if not sp.exists():
            continue  # 未收录站点的文档（30分钟指南/体系索引）不参与站点一致性
        if _file_md5(src) != _file_md5(sp):
            findings.append((1, f"site:{name}", "站点副本与 12_DOCS 源不一致 → 需 lh docs sync + 重建站点"))
    # 2) 首页 DNA 有效性
    home_src = SITE_DIR / "index.md"
    if home_src.exists():
        hd = _doc_date(home_src)
        if not hd:
            findings.append((1, "home:index.md", "首页缺 DNA 时间戳"))
        elif hd > today.strftime("%Y-%m-%d"):
            findings.append((2, "home:index.md", f"首页 DNA 时间戳指向未来 {hd}"))
        else:
            findings.append((0, "home:index.md", f"首页 DNA 有效（{hd}）"))
    # 3) 页面 GPG：源文档 .asc 存在 + 抽验签名
    for rel in DELIVERY_DOCS:
        src = ROOT / rel
        asc = Path(str(src) + ".asc")
        if not asc.exists():
            findings.append((2, f"sign:{Path(rel).name}", "源文档 .asc 缺失（GPG 未签）"))
    # 4) 未授权新增 md（站点目录内不属于导航的散文件）
    allowed = {Path(rel).name for rel in DELIVERY_DOCS} | {"index.md", "README.md"}
    try:
        for p in SITE_DIR.glob("*.md"):
            if p.name not in allowed and "assets" not in p.name:
                findings.append((2, f"stray:{p.name}", "站点目录出现未登记 .md → 疑似未授权修改"))
    except Exception:  # noqa: BLE001
        pass
    # 汇总
    bad = sum(1 for s, *_ in findings if s == 2)
    warn = sum(1 for s, *_ in findings if s == 1)
    color = "🟢" if not bad and not warn else ("🟡" if not bad else "🔴")
    now = datetime.datetime.now()
    entry = {"date": now.strftime("%Y-%m-%d"), "time": now.isoformat(),
             "type": "docs_audit", "color": color, "bad": bad, "warn": warn,
             "reason": f"文档站三色审计 {color}（bad={bad} warn={warn}）"}
    if bad or warn:
        _append_shame(entry)
    _append_audit_log(json.dumps({"ts": now.isoformat(), "color": color,
                                  "bad": bad, "warn": warn, "findings": findings},
                                 ensure_ascii=False))
    if json_out:
        print(json.dumps({"tool": "lh-docs", "mode": "audit", "color": color,
                          "bad": bad, "warn": warn, "findings": findings,
                          "logged": str(AUDIT_LOG)}, ensure_ascii=False, indent=2))
    else:
        print(f"{color} docs audit · bad={bad} warn={warn} · 归档 {AUDIT_LOG}")
        for sev, item, detail in findings:
            mark = {0: "✅", 1: "🟡", 2: "🔴"}[sev]
            print(f"  {mark} {item}: {detail}")
    return color


def cmd_audit(json_out: bool = False) -> int:
    color = audit_site(json_out)
    return 0 if color == "🟢" else 1


# ══════════════════ main ══════════════════

def main():
    ap = argparse.ArgumentParser(description="对外文档一体化引擎 (lh docs)")
    ap.add_argument("sub", nargs="?", default="check",
                    choices=["check", "sync", "version", "stats", "feedback", "weekly",
                             "audit", "feedback-form"])
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--audit", action="store_true", help="check 时追加文档站三色审计")
    ap.add_argument("--all", action="store_true", help="feedback 扫全量耻辱墙记录（默认近 30 天）")
    ap.add_argument("--days", type=int, default=7, help="stats 统计窗口天数（默认 7）")
    args = ap.parse_args()
    if args.sub == "check":
        code = check_docs(args.json)
        if args.audit:
            audit_site(args.json)
        sys.exit(code)
    if args.sub == "sync":
        sys.exit(cmd_sync(args.json))
    if args.sub == "version":
        sys.exit(cmd_version(args.json))
    if args.sub == "stats":
        sys.exit(cmd_stats(args.json, args.days))
    if args.sub == "feedback":
        sys.exit(cmd_feedback(args.json, args.all))
    if args.sub == "weekly":
        sys.exit(cmd_weekly(args.json))
    if args.sub == "feedback-form":
        sys.exit(cmd_feedback_form(args.json))
    sys.exit(cmd_audit(args.json))


if __name__ == "__main__":
    main()
