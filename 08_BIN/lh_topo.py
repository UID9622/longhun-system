#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·己卯·未时·䷟恒-TOPOLOGY-ENGINE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·知识图谱拓扑引擎 v1.0 — `lh topo`
# 把 Notion 知识库作为正式知识图谱节点接入系统，本地缓存可执行的审计结构。
#   lh topo list                     列出全部本地拓扑缓存 + 概况
#   lh topo verify 通心译             校验节点(资产+子图谱+笔记) DNA/链接/状态 → 全绿或缺口
#   lh topo sync 通心译 [--dry-run]   从 Notion API 拉最新行 → 更新本地缓存
#   lh topo sync 图谱 --source obsidian --dir <md目录>   本地 Obsidian 文档库源同步(v1.2)
#   lh topo sync 图谱 --source yuque --namespace <login/slug>   语雀 API 知识库源同步(v1.2)
#   lh topo subgraph 图谱 --name <库名> --db-id <id> [--meta '{json}']   注册关联库子图谱(v1.5)
#   lh topo obsidian scan [--dir <vault>] [--kw 词]   扫描本地 Obsidian 命中笔记(不落盘)
#   lh topo obsidian sync [--name 图谱名] [--dir <vault>] [--kw 词]   命中笔记注册为 Obsidian 镜像子图谱
#   lh topo cite <资产名>             返回资产完整引用格式（含 DNA+链接 · 引用溯源）
#   lh topo frameworks                列出龍魂引擎依赖的开源框架清单(M77 下近空)
# 缓存: docs/topology/<图谱名>_legion_topo.json · 校验: ~/.longhun/topo/{source}_verify.json
# 版本: v1.5 (2026-09-03 · 通心译深度拓扑: 顶层 subgraphs 子图谱层(关联库+Obsidian 镜像)
#       + iter_nodes 统一节点遍历(组资产+子图谱+内嵌笔记)→ stats/verify/root_hash/list/HTML 同步
#       + v1.4 sync --live · v1.3 register/node · v1.2 多数据源) · 零三方依赖（原生 urllib）

import argparse
import contextlib
import hashlib
import html as html_mod
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPO_DIR = ROOT / "docs" / "topology"
STATE_DIR = Path.home() / ".longhun"          # 跨引擎共享状态（lh_dh_dispatch 知识库）
DH_KB_STATE = STATE_DIR / "dh_kb_state.json"  # 数字人知识库加载状态（lh health 读取）
VERIFY_DIR = STATE_DIR / "topo"               # 各数据源同步校验结果落盘（v1.2·任务A）
DB_DIR = STATE_DIR / "db"                     # SQLite 持久化（任务C·生态补全 2026-09-03）
DB_PATH = DB_DIR / "topo.db"                  # 图谱版本历史库（append-only·支撑 diff）
SHAME_DB = STATE_DIR / "shame_wall" / "shame_wall.db"   # 归一审判官耻辱墙库（dashboard 读）
GROUP_ORDER = ["🎯 核心ASI层", "🤖 执行Agent层", "⚡ 技能库",
               "📚 文档库", "🏗️ 系统架构层", "🔧 工具层"]
NOTION_API = "https://api.notion.com/v1"
YUQUE_API = "https://www.yuque.com/api/v2"    # 语雀开放 API v2（X-Auth-Token·任务A）
# 本机代理会劫持 Notion 连接（socks5h）→ 强制直连
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


# ─────────────────────────── 通用 ───────────────────────────

def list_topos():
    if not TOPO_DIR.is_dir():
        return []
    return sorted(f for f in TOPO_DIR.iterdir() if f.is_file() and f.name.endswith("_topo.json"))


def _find_topo_file(keyword: str) -> tuple:
    """按关键词返回 (缓存文件 Path, 图谱 dict)；找不到 → 抛 SystemExit
    v1.2: 精确 topo_name 优先（镜像图谱 topo_name 如「通心译-obsidian」不会抢占主图谱）"""
    if not keyword:
        raise SystemExit("  ❌ 缺图谱名，例: lh topo verify 通心译")
    kw = keyword.strip()
    _cache = []
    for f in list_topos():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("topo_name") == kw:
            return f, data
        _cache.append((f, data))
    for f, data in _cache:                    # 第一轮精确未中 → 子串兜底（主图谱先行靠精确轮）
        if kw in data.get("topo_name", "") or kw in data.get("display", ""):
            return f, data
    raise SystemExit(f"  ❌ 未找到图谱「{keyword}」，可用 lh topo list 查看")


def find_topo(keyword: str) -> dict:
    """按关键词匹配缓存（topo_name/display 含 keyword）"""
    return _find_topo_file(keyword)[1]


def load_topo_data():
    """lh health 等外部模块共用：读全部拓扑缓存并聚合成统计"""
    out = {"loaded": False, "nodes": 0, "green": 0, "yellow": 0,
           "neutral": 0, "last_sync": "未同步", "topo": ""}
    if not TOPO_DIR.is_dir():
        return out
    for f in TOPO_DIR.iterdir():
        if not (f.is_file() and f.name.endswith("_topo.json")):
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        green = yellow = neutral = 0
        for g in data.get("groups", []):
            for a in g.get("assets", []):
                s = (a.get("status") or "").strip()
                if s.startswith("🟢"):
                    green += 1
                elif s.startswith("🟡"):
                    yellow += 1
                else:
                    neutral += 1
        total = green + yellow + neutral
        if out["nodes"] < total:   # 多图谱时取节点最多者为主
            out.update({"loaded": True, "nodes": total, "green": green,
                        "yellow": yellow, "neutral": neutral,
                        "last_sync": data.get("last_sync", "?"),
                        "topo": data.get("display", f.stem)})
    return out


def iter_nodes(data: dict):
    """统一节点遍历(v1.5·子图谱+内嵌资产):
    groups 资产 + subgraphs(子图谱=1 节点,其 assets 笔记逐条再算节点)。
    子图谱节点 schema 与 asset 兼容:name/dna/status/link + subgraph_meta/assets"""
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            yield g.get("name", ""), a
    for sg in data.get("subgraphs", []):
        sg_lab = f"🗄️ {sg.get('name', '子图谱')}"
        yield sg_lab, sg
        for a in sg.get("assets", []):
            yield f"{sg_lab}·笔记", a


def asset_stats(data: dict) -> tuple:
    green = yellow = neutral = 0
    for _g, n in iter_nodes(data):
        s = (n.get("status") or "").strip()
        if s.startswith("🟢"):
            green += 1
        elif s.startswith("🟡"):
            yellow += 1
        else:
            neutral += 1
    return green, yellow, neutral


# ─────────────────────────── 知识库 & 静态服务（v1.1·2026-09-02）───────────────────────────

def topo_root_hash(data: dict) -> str:
    """聚合根哈希(v1.5·含子图谱)：group|name|dna 排序拼接 → SHA-256 前 16 位（页脚主权锚点）"""
    lines = [f"{g}|{n.get('name')}|{n.get('dna')}" for g, n in iter_nodes(data)]
    return hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()[:16].upper()


def build_kb_index(data: dict) -> list:
    """构建数字人知识库内存索引：资产名 → {内容摘要, DNA, 层级(组), 链接}"""
    out = []
    for g, a in iter_nodes(data):
        out.append({
            "name": a.get("name", "?"),
            "group": g,
            "dna": a.get("dna", ""),
            "status": (a.get("status") or "").strip(),
            "link": a.get("link", ""),
            "summary": f"通心译总台资产 · {g} · {a.get('name')}",
        })
    return out


def load_kb_index(keyword: str = "通心译") -> dict:
    """知识库统一状态源：条目数/绿黄/最后同步/根哈希（lh topo kb-status / lh health / 数字人注入共用）"""
    f, data = _find_topo_file(keyword)
    green, yellow, neutral = asset_stats(data)
    return {"loaded": bool(data.get("groups")), "entries": len(build_kb_index(data)),
            "green": green, "yellow": yellow, "neutral": neutral,
            "topo": data.get("display", "?"), "last_sync": data.get("last_sync", "?"),
            "root_hash": topo_root_hash(data), "source": f"docs/topology/{f.name}"}


def _wallet_banner() -> str:
    """收款区块(可降级): 读 ~/.longhun/crypto.json 的 SOL 地址·二维码走 /donate.png 静态路由。
    无配置/无地址 → 返回空串,页面不出现收款区块(优雅降级·不显示假收款)。"""
    try:
        with open(os.path.expanduser("~/.longhun/crypto.json"), encoding="utf-8") as fh:
            cfg = json.loads(fh.read())
        addr = (cfg.get("networks", {}) or {}).get("solana", {}).get("address", "")
        if not addr:
            return ""
    except Exception:
        return ""
    esc = html_mod.escape
    return ('<div class="donate">'
            '<span class="dh">💛 支持龍魂 · 纯自愿 · 零黑箱 · 款项仅用于服务器与开发</span> '
            '<img src="/donate.png" alt="支持龍魂二维码" class="dq">'
            '<span class="da">SOL / USDC: <code>' + esc(addr) + '</code>'
            '<button type="button" onclick="navigator.clipboard.writeText(\'' + esc(addr) + '\')">复制</button>'
            '</span></div>')


def render_topo_html(keyword: str = "通心译") -> str:
    """生成人类可读拓扑页：6 组树形 + 19 节点（名称/ID/DNA/状态）+ 页脚主权声明与根哈希"""
    f, data = _find_topo_file(keyword)
    green, yellow, neutral = asset_stats(data)
    total = green + yellow + neutral
    rh = topo_root_hash(data)
    esc = html_mod.escape
    donate_html = _wallet_banner()

    groups_html = []
    for _gi, g in enumerate(data.get("groups", []), 1):
        rows = []
        for a in g.get("assets", []):
            st = (a.get("status") or "").strip()
            dot = "🟢" if st.startswith("🟢") else ("🟡" if st.startswith("🟡") else "⚪")
            name = esc(a.get("name", "?"))
            name_html = (f'<a href="{esc(a.get("link", ""))}" target="_blank">{name}</a>'
                         if a.get("link") else name)
            rows.append(
                f'<li class="asset">'
                f'<div class="row1"><span class="dot">{dot}</span> {name_html}'
                f'<span class="grp-tag">{esc(g.get("name", ""))}</span></div>'
                f'<div class="meta"><span class="k">ID</span><code>{esc(str(a.get("id", "")))}</code></div>'
                f'<div class="meta"><span class="k">DNA</span><code>{esc(str(a.get("dna", "")))}</code></div>'
                f'<div class="meta"><span class="k">状态</span><span class="st">{esc(st) or "未标注"}</span></div>'
                f'</li>')
        groups_html.append(
            f'<section class="grp"><h2>{esc(str(g.get("name", "")))}'
            f'<span class="cnt">{len(g.get("assets", []))}</span></h2>'
            f'<ul>{"".join(rows)}</ul></section>')

    sub_html = []
    for sg in data.get("subgraphs", []):
        meta = sg.get("subgraph_meta", {}) or {}
        st = (sg.get("status") or "").strip()
        dot = "🟢" if st.startswith("🟢") else ("🟡" if st.startswith("🟡") else "⚪")
        sg_name = esc(sg.get("name", "?"))
        sg_link = (f'<a href="{esc(sg.get("link", ""))}" target="_blank">{sg_name}</a>'
                   if sg.get("link") else sg_name)
        meta_html = "".join(
            f'<div class="meta"><span class="k">{k}</span><code>{esc(str(meta[k]))}</code></div>'
            for k in ("database_id", "row_count", "created", "edited") if meta.get(k))
        rows = (f'<li class="asset"><div class="row1"><span class="dot">{dot}</span> '
                f'{esc(str(sg.get("type", "notion-db")))}</div>'
                f'<div class="meta"><span class="k">DNA</span>'
                f'<code>{esc(str(sg.get("dna", "")))}</code></div>{meta_html}</li>')
        for na in sg.get("assets", []):
            nst = (na.get("status") or "").strip()
            ndot = "🟢" if nst.startswith("🟢") else ("🟡" if nst.startswith("🟡") else "⚪")
            nn = esc(na.get("name", "?"))
            nlink = (f'<a href="{esc(na.get("link", ""))}" target="_blank">{nn}</a>'
                     if na.get("link") else nn)
            rows += (f'<li class="asset"><div class="row1"><span class="dot">{ndot}</span> {nlink}'
                     f'<span class="grp-tag">笔记</span></div>'
                     f'<div class="meta"><span class="k">DNA</span>'
                     f'<code>{esc(str(na.get("dna", "")))}</code></div></li>')
        cnt = meta.get("row_count") or (len(sg.get("assets", [])) if sg.get("assets") else "")
        sub_html.append(
            f'<section class="grp subgrp"><h2>🗄️ 子图谱 · {sg_link}'
            f'{"<span class=cnt>" + esc(str(cnt)) + " 行</span>" if cnt else ""}</h2>'
            f'<ul>{rows}</ul></section>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(data.get('display', '通心译总台'))} · 拓扑开放页</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#0a0e17; color:#c9d1d9; font-family:-apple-system,'PingFang SC','Noto Sans SC',sans-serif; padding:24px; }}
.wrap {{ max-width:880px; margin:0 auto; }}
header {{ text-align:center; padding:28px 0 20px; border-bottom:2px solid #ffab00; margin-bottom:24px; }}
h1 {{ font-size:28px; color:#ffab00; letter-spacing:2px; }}
.sub {{ color:#8b949e; margin-top:8px; font-size:13px; }}
.chips {{ margin:14px 0; display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }}
.chip {{ background:#161b22; border:1px solid #30363d; border-radius:14px; padding:3px 12px; font-size:12px; color:#ffab00; }}
.grp {{ margin:14px 0; }}
.grp h2 {{ font-size:16px; color:#58a6ff; border-left:3px solid #58a6ff; padding-left:10px; margin-bottom:10px; }}
.grp .cnt {{ margin-left:8px; background:#161b22; color:#8b949e; border-radius:8px; padding:1px 8px; font-size:11px; }}
ul {{ list-style:none; }}
li.asset {{ background:#0d1117; border:1px solid #21262d; border-left:3px solid #30363d; border-radius:6px; padding:10px 12px; margin:8px 0; }}
li.asset:hover {{ border-left-color:#ffab00; }}
.row1 {{ font-size:14px; font-weight:600; color:#e6edf3; }}
.dot {{ margin-right:6px; }}
.grp-tag {{ font-size:10px; color:#8b949e; background:#161b22; padding:1px 8px; border-radius:8px; margin-left:8px; font-weight:400; }}
.meta {{ margin-top:4px; font-size:11px; color:#8b949e; }}
.meta .k {{ display:inline-block; min-width:30px; color:#484f58; }}
.meta code {{ background:#161b22; color:#7ee787; border-radius:4px; padding:1px 6px; font-size:11px; word-break:break-all; }}
.st {{ color:#ffab00; }}
footer {{ margin-top:28px; border-top:1px solid #21262d; padding:18px 0 8px; text-align:center; font-size:11px; color:#8b949e; line-height:1.9; }}
footer .sovereign {{ color:#ffab00; letter-spacing:1px; }}
footer .root {{ color:#7ee787; }}
.donate {{ margin:22px auto 6px; padding:14px 18px; border:1px dashed #ffab00; border-radius:10px;
           display:flex; gap:14px; align-items:center; justify-content:center; flex-wrap:wrap;
           background:#0d1117; text-align:left; }}
.donate .dh {{ color:#ffab00; font-size:12px; letter-spacing:1px; }}
.donate .dq {{ width:84px; height:84px; border-radius:6px; background:#fff; padding:3px; }}
.donate .da {{ color:#c9d1d9; font-size:12px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
.donate code {{ background:#161b22; color:#7ee787; border-radius:4px; padding:2px 8px; word-break:break-all; font-size:11px; }}
.donate button {{ background:#ffab00; color:#0a0e17; border:0; border-radius:6px; padding:3px 10px; cursor:pointer; font-size:12px; }}
.donate button:active {{ opacity:.7; }}
@media (max-width:600px) {{ body {{ padding:12px; }} h1 {{ font-size:20px; }} .donate {{ justify-content:flex-start; }} }}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>🕸️ {esc(data.get('display', '通心译总台'))}</h1>
  <div class="sub">龍魂知识图谱拓扑 · 节点 {total} · {len(data.get('groups', []))} 组 · {len(data.get("subgraphs", []))} 子图谱 · 归属 诸葛鑫 | UID9622 · 龍芯北辰</div>
  <div class="chips">
    <span class="chip">节点 {total}</span><span class="chip">🟢 {green}</span>
    <span class="chip">🟡 {yellow}</span><span class="chip">同步 {esc(str(data.get('last_sync', '?')))[:19]}</span>
    <span class="chip">根哈希 {rh}</span>
  </div>
</header>
{"".join(groups_html)}{"".join(sub_html)}
<footer>
  <div class="sovereign">🐉 龍魂 · 通心译军团 · 数字主权归 诸葛鑫 | UID9622 · 龍芯北辰</div>
  <div>协议: CC BY-NC-SA 4.0（核心思想层） · 工程实现: MulanPSL v2</div>
  <div>GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F</div>
  <div class="root">根哈希: {rh} · 缓存: docs/topology/{esc(f.name)} · 同步 {esc(str(data.get('last_sync', '?')))}</div>
</footer>
{donate_html}
</div>
</body>
</html>
"""


class TopoHandler(BaseHTTPRequestHandler):
    """静态拓扑页服务：GET / → HTML · GET /health → JSON（M77 零中间层·纯标准库）"""
    keyword = "通心译"

    def log_message(self, format, *args):   # 静默访问日志
        pass

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Longhun-Owner", "Zhuge-Xin-UID9622")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """v1.1 规范路径（2026-09-02·对外加固）:
        / → 默认图谱 HTML · /topo/<图谱名>/html → 指定图谱 HTML ·
        /topo/<图谱名> → 图谱 JSON 树 · /health → 存活 JSON · 其余 404"""
        path = urllib.parse.unquote(self.path).rstrip("/") or "/"
        if path == "/health":
            kb = load_kb_index(self.keyword)
            body = json.dumps({"status": "ok", "service": "lh-topo-serve",
                               "topo": kb["topo"], "entries": kb["entries"],
                               "root_hash": kb["root_hash"]}, ensure_ascii=False).encode("utf-8")
            return self._send(200, body, "application/json; charset=utf-8")
        hdir = find_holo_dir()
        if path in ("/holo", "/holo/"):
            if not hdir:
                return self._send(404, b"holo pages not deployed (10_PORTAL/holo)", "text/plain; charset=utf-8")
            return self._send(200, (hdir / "index.html").read_bytes(), "text/html; charset=utf-8")
        if path == "/holo/data":
            body = json.dumps(holo_data_json(), ensure_ascii=False).encode("utf-8")
            return self._send(200, body, "application/json; charset=utf-8")
        if path.startswith("/holo/vendor/"):
            if not hdir:
                return self._send(404, b"holo vendor missing", "text/plain; charset=utf-8")
            rel = path[len("/holo/"):]
            fp = (hdir / rel).resolve()
            if not str(fp).startswith(str(hdir.resolve())) or not fp.is_file():
                return self._send(404, b"holo vendor 404", "text/plain; charset=utf-8")
            _ctype = {"js": "application/javascript", "png": "image/png",
                      "css": "text/css; charset=utf-8", "jpg": "image/jpeg",
                      "svg": "image/svg+xml", "woff2": "font/woff2"}
            ctype = _ctype.get(fp.suffix.lstrip("."), "application/octet-stream")
            return self._send(200, fp.read_bytes(), ctype)
        if path.startswith("/holo"):
            return self._send(404, b"holo route: /holo /holo/data /holo/vendor/*", "text/plain; charset=utf-8")
        if path == "/dashboard":
            body = render_dashboard_html().encode("utf-8")
            return self._send(200, body, "text/html; charset=utf-8")
        if path == "/donate.png":   # 收款二维码静态路由(读 ~/.longhun/static/donate.png)
            qr = os.path.expanduser("~/.longhun/static/donate.png")
            if os.path.exists(qr):
                with open(qr, "rb") as _f:
                    return self._send(200, _f.read(), "image/png")
            return self._send(404, b"donate.png not configured", "text/plain; charset=utf-8")
        name = self.keyword
        is_json = False
        if path != "/":
            parts = path.split("/")
            is_html = len(parts) == 4 and parts[0] == "" and parts[1] == "topo" \
                and parts[3] == "html" and parts[2] != ""
            is_json = len(parts) == 3 and parts[0] == "" and parts[1] == "topo" \
                and parts[2] != "" and not parts[2].endswith(".html")
            if not (is_html or is_json):
                body = ("404 · lh-topo-serve (M77 零中间层)\n\n规范路径:\n"
                        "  /                      当前图谱 HTML 页\n"
                        "  /topo/<图谱名>/html    指定图谱 HTML 页\n"
                        "  /topo/<图谱名>         指定图谱 JSON 树\n"
                        "  /health                存活 JSON").encode()
                return self._send(404, body, "text/plain; charset=utf-8")
            name = parts[2]
        try:
            kb = load_kb_index(name)
            if is_json:
                body = json.dumps(kb, ensure_ascii=False, indent=2).encode()
                return self._send(200, body, "application/json; charset=utf-8")
            page = render_topo_html(name).encode()
            self._send(200, page, "text/html; charset=utf-8")
        except SystemExit as e:
            msg = f"404 · 图谱「{name}」本地缓存缺失，请先 lh topo sync {name}\n{e}".encode()
            self._send(404, msg, "text/plain; charset=utf-8")


# ─────────────────────── 统一看板 /dashboard（任务D·2026-09-03）───────────────────────

def _shame_wall_recent(limit: int = 10) -> list:
    """读归一审判官耻辱墙 SQLite 最近记录（容错·空则返回 []）"""
    if not SHAME_DB.is_file():
        return []
    try:
        conn = sqlite3.connect(str(SHAME_DB))
        rows = conn.execute(
            f"SELECT 源名称,源URL,指纹类型,置信度,审计色,发现时间,匹配内容 "
            f"FROM 剽窃记录 ORDER BY 发现时间 DESC LIMIT {int(limit)}").fetchall()
        conn.close()
        return [{"name": r[0], "url": r[1], "kind": r[2], "conf": r[3],
                 "color": r[4], "ts": r[5],
                 "match": (r[6] or "")[:80]} for r in rows]
    except Exception:   # noqa: BLE001
        return []


def _live_snapshots() -> list:
    """~/.longhun/topo/*.json 活体快照汇总（拓扑/serve 实时数据源）"""
    out = []
    if VERIFY_DIR.is_dir():
        for f in sorted(VERIFY_DIR.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            if d.get("schema") == "longhun-topo-live-v1":
                assets = d.get("assets", [])
                g = sum(1 for a in assets if "🟢" in str(a.get("status")))
                y = sum(1 for a in assets if "🟡" in str(a.get("status")))
                r = sum(1 for a in assets if "🔴" in str(a.get("status")))
                out.append({"name": d.get("topo_name", f.stem), "display": d.get("display"),
                            "nodes": len(assets), "green": g, "yellow": y, "red": r,
                            "live": d.get("live", {}), "last_sync": d.get("last_sync", "")})
    return out


def render_dashboard_html(refresh: int = 60) -> str:
    """统一看板: 全部图谱状态 + 耻辱墙最新 + 服务健康（60s 自动刷新·零三方依赖）"""
    graphs = []
    for f in sorted(TOPO_DIR.glob("*_legion_topo.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        assets = [a for g in d.get("groups", []) for a in g.get("assets", [])]
        graphs.append({"name": d.get("display", d.get("topo_name", f.stem)),
                       "file": f.name,
                       "nodes": len(assets),
                       "green": sum(1 for a in assets if "🟢" in str(a.get("status", ""))),
                       "yellow": sum(1 for a in assets if "🟡" in str(a.get("status", ""))),
                       "red": sum(1 for a in assets if "🔴" in str(a.get("status", ""))),
                       "sync": d.get("last_sync", "-")})
    live = _live_snapshots()
    shame = _shame_wall_recent(10)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    donate_html = _wallet_banner()
    # 服务健康探测（容器友好: 失败不计红·标注离线）
    import shutil as _sh
    import subprocess as _sp
    ollama_ok = bool(_sh.which("ollama"))
    ollama_live = "—"
    if ollama_ok:
        try:
            r = _sp.run(["ollama", "list"], capture_output=True, text=True, timeout=6)
            if r.returncode == 0:
                ollama_live = f"在线 · {len([x for x in r.stdout.splitlines()[1:] if x.strip()])} 模型"
            else:
                ollama_live = "未启动"
        except Exception:
            ollama_live = "不可达"
    import importlib.util as _iu
    py_ok = {
        "PyTorch": bool(_iu.find_spec("torch")),
        "Transformers": bool(_iu.find_spec("transformers")),
    }

    def _bar(g, y, r):
        return (f"<span class=stat style='color:#44ff88'>🟢{g}</span> "
                f"<span class=stat style='color:#ffab00'>🟡{y}</span> "
                f"<span class=stat style='color:#ff4444'>🔴{r}</span>")

    rows = "".join(
        f"<tr><td>{html_mod.escape(g['name'])}</td><td>{g['nodes']}</td>"
        f"<td>{_bar(g['green'], g['yellow'], g['red'])}</td>"
        f"<td style='color:#888'>{html_mod.escape(g['sync'])}</td></tr>"
        for g in graphs) or "<tr><td colspan=4 style='color:#888'>无图谱</td></tr>"
    live_rows = "".join(
        f"<tr><td>{html_mod.escape(snap['display'] or snap['name'])}</td><td>{snap['nodes']}</td>"
        f"<td>{_bar(snap['green'], snap['yellow'], snap['red'])}</td>"
        f"<td style='color:#888'>{html_mod.escape(snap.get('last_sync',''))}</td></tr>"
        for snap in live) or "<tr><td colspan=4 style='color:#888'>无活体快照（未跑 sync --live）</td></tr>"
    shame_rows = "".join(
        f"<tr><td style='color:{'#ff4444' if '🔴' in str(s['color']) else '#ffab00'}'>"
        f"{html_mod.escape(str(s['color']))}</td>"
        f"<td>{html_mod.escape(s['name'])}</td>"
        f"<td>{html_mod.escape(str(s['kind']))}</td>"
        f"<td style='color:#888'>{html_mod.escape(str(s['ts']))}</td>"
        f"<td style='color:#888;max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>"
        f"{html_mod.escape(str(s['match']))}</td></tr>"
        for s in shame) or "<tr><td colspan=5 style='color:#888'>耻辱墙 0 记录 · 清白</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="{int(refresh)}">
<title>🐉 龍魂统一看板 · UID9622</title>
<style>
body{{background:#0a0e17;color:#c0c0c0;font-family:'Courier New',monospace;padding:16px;}}
h1{{color:#00d4ff;letter-spacing:4px;font-size:20px}}
h2{{color:#ffab00;font-size:15px;border-bottom:1px solid #1a1a2e;padding-bottom:4px}}
table{{width:100%;border-collapse:collapse;margin:8px 0 20px;font-size:13px}}
th{{background:#1a1a2e;color:#00d4ff;padding:6px;text-align:left}}
td{{padding:6px;border-bottom:1px solid #10121f}}
.stat{{padding:2px 10px;border-radius:10px;font-size:12px;background:#1a1a2e}}
.health{{display:inline-block;padding:2px 10px;border-radius:10px;font-size:12px;margin:2px}}
.g{{background:#0f2a1a;color:#44ff88}}.y{{background:#2a210f;color:#ffab00}}
.r{{background:#2a0f0f;color:#ff4444}}.o{{background:#1a1a2e;color:#888}}
.donate{{margin:16px 0 4px;padding:10px 14px;border:1px dashed #ffab00;border-radius:8px;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;background:#0d111f}}
.donate .dh{{color:#ffab00;font-size:12px;letter-spacing:1px}}
.donate img{{width:72px;height:72px;border-radius:4px;background:#fff;padding:2px}}
.donate code{{color:#7ee787;word-break:break-all}}
.donate button{{background:#ffab00;color:#000;border:0;border-radius:4px;cursor:pointer;padding:2px 8px}}
.foot{{color:#555;font-size:11px;text-align:center;margin-top:24px}}
.box{{background:#0d111f;border:1px solid #1a1a2e;padding:8px 14px;margin:8px 0;border-radius:6px}}
</style></head><body>
<h1>🐉 龍魂统一看板 · 诸葛鑫 | UID9622 · 龍芯北辰</h1>
<div class=box><span style='color:#888'>自动刷新 {int(refresh)}s · 生成 {html_mod.escape(now)}</span></div>
<h2>🕸️ 全部图谱（docs/topology）</h2>
<table><tr><th>图谱</th><th>节点</th><th>三色</th><th>最后同步</th></tr>{rows}</table>
<h2>🔬 活体快照（sync --live 落盘 ~/.longhun/topo）</h2>
<table><tr><th>图谱</th><th>节点</th><th>三色</th><th>探测时间</th></tr>{live_rows}</table>
<h2>🏥 服务健康</h2>
<div>
<span class="health {'g' if ollama_live.startswith('在线') else 'o'}">Ollama · {html_mod.escape(str(ollama_live))}</span>
<span class="health {'g' if py_ok['PyTorch'] else 'o'}">PyTorch {'✓' if py_ok['PyTorch'] else '—'}</span>
<span class="health {'g' if py_ok['Transformers'] else 'o'}">Transformers {'✓' if py_ok['Transformers'] else '—'}</span>
<span class="health g">topo-serve · 本页在线</span>
<span class="health o">网关 API · 9622（容器内自检）</span>
</div>
<h2>🧱 耻辱墙 · 最近 {len(shame)} 条</h2>
<table><tr><th>色</th><th>源名称</th><th>指纹</th><th>发现时间</th><th>匹配</th></tr>{shame_rows}</table>
{donate_html}
<div class=foot>M77 零中间层 · 纯标准库 · 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2<br>
DNA: #龍芯⚡️2026-09-03-ECOSYSTEM-DASHBOARD-v1.0-UID9622</div>
</body></html>"""


# ─────────────────────── 全息可视化 /holo（2026-09-04 · Three.js+WebXR 多端）───────────────────────

_HOLO_TRIES = [
    ROOT / "10_PORTAL" / "holo",                      # 本地开发(10_PORTAL/holo/)
    Path(__file__).resolve().parent / "holo",         # 引擎同级(/apps/topo/holo/)
    Path("/apps/topo/holo"),                          # 鲲鹏部署目录兜底
]


def find_holo_dir():
    """定位全息页面静态目录(本地/引擎同级/鲲鹏) → 找不到 None"""
    for _p in _HOLO_TRIES:
        if (_p / "index.html").is_file():
            return _p
    return None


def holo_color(status: str) -> str:
    s = (status or "").strip()
    if s.startswith("🟢"):
        return "#22c55e"
    if s.startswith("🟡"):
        return "#eab308"
    if s.startswith("🔴"):
        return "#ef4444"
    return "#64748b"


def holo_data_json():
    """/holo/data 聚合: 23 节点+三色审计+耻辱墙+根哈希(前端 60s 轮询数据源)"""
    try:
        _f, data = _find_topo_file("通心译")
    except SystemExit:
        return {"error": "topo cache missing · lh topo sync 通心译"}
    green, yellow, neutral = asset_stats(data)
    nodes = []
    for g, n in iter_nodes(data):
        nodes.append({
            "name": n.get("name", "?"), "group": g,
            "dna": n.get("dna", ""), "status": (n.get("status") or "").strip(),
            "color": holo_color(n.get("status")),
        })
    shame = _shame_wall_recent(12)
    shame_red = len([1 for s in shame if "红" in str(s.get("color", ""))])
    return {
        "nodes": nodes,
        "audit": {"green": green, "yellow": yellow, "neutral": neutral,
                  "shame_red": shame_red, "total": len(nodes)},
        "shame": shame,
        "root_hash": topo_root_hash(data),
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
        "service": "lh-topo-serve /holo v1.0",
    }


def cmd_serve(port: int = 8762, host: str = "127.0.0.1", keyword: str = "通心译"):
    """lh topo serve --port 8762 — 独立静态服务（默认仅本机；对外显式 --host 0.0.0.0）"""
    TopoHandler.keyword = keyword
    srv = ThreadingHTTPServer((host, port), TopoHandler)
    kb = load_kb_index(keyword)
    print(f"\n  🕸️  拓扑开放服务 http://{host}:{port}/ · {kb['topo']}")
    print(f"     节点 {kb['entries']} · 🟢{kb['green']} · 🟡{kb['yellow']}"
          f" · 根哈希 {kb['root_hash']} · 同步 {kb['last_sync']}")
    print("     / 拓扑页 · /health 存活 · 零中间层(M77·纯标准库) · Ctrl+C 停止")
    print()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("  ⏹️  已停止")


def cmd_kb_status(keyword: str = "通心译", json_out: bool = False):
    """lh topo kb-status — 知识库加载状态（本地缓存即时构建 + 数字人 state 文件互补）"""
    s = load_kb_index(keyword)
    state = {}
    with contextlib.suppress(Exception):
        if DH_KB_STATE.exists():
            state = json.loads(DH_KB_STATE.read_text(encoding="utf-8"))
    if json_out:
        print(json.dumps({**s, "dh_loaded": bool(state.get("loaded")),
                          "dh_loaded_at": state.get("loaded_at", "")},
                         ensure_ascii=False, indent=2))
        return
    print(f"\n  🕸️  知识库状态 · {s['topo']}")
    print(f"     已加载 {s['entries']} 条资产 · 🟢{s['green']} · 🟡{s['yellow']}")
    print(f"     最后同步 {s['last_sync']} · 源 {s['source']}")
    if state.get("loaded"):
        print(f"     数字人接入: ✅ 已加载({state.get('loaded_at', '?')})")
    else:
        print("     数字人接入: ⏳ 未加载（lh dh 启动/调用时自动挂载）")
    print()


# ─────────────────────────── list ───────────────────────────

def cmd_list(keyword: str = ""):
    """lh topo list [图谱名] — 无参=总览全部图谱；带图谱名=该图谱全部组+节点明细（v1.3）"""
    files = list_topos()
    if not files:
        print("  🕸️  暂无拓扑缓存（docs/topology/）· 首次请用 lh topo sync 通心译")
        return
    detail = False
    if keyword.strip():
        f, _d = _find_topo_file(keyword)
        files, detail = [f], True
    print(f"\n  🕸️  龍魂知识图谱拓扑 · 本地缓存 {len(files)} 个")
    print("  " + "=" * 56)
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            print(f"  🔴 {f.name}（损坏）")
            continue
        green, yellow, neutral = asset_stats(d)
        print(f"  {d.get('display','?')}")
        print(f"     节点 {green+yellow+neutral} · 🟢{green} · 🟡{yellow}"
              f"{(' · ⚪'+str(neutral)) if neutral else ''}"
              f" · 同步 {d.get('last_sync','?')} · {f.relative_to(ROOT)}")
        if detail:
            for g in d.get("groups", []):
                if not g.get("assets"):
                    continue
                print(f"   📂 {g.get('name')}")
                for a in g.get("assets", []):
                    print(f"      · {a.get('name')}  [{a.get('type','?')}] {a.get('status','')}")
                    if a.get("dna"):
                        print(f"        DNA {a.get('dna')}")
                    if a.get("link"):
                        print(f"        链接 {a.get('link')}")
            for sg in d.get("subgraphs", []):
                meta = sg.get("subgraph_meta", {})
                print(f"   🗄️ [子图谱] {sg.get('name')}  [{sg.get('type','?')}] {sg.get('status','')}")
                if sg.get("dna"):
                    print(f"        DNA {sg.get('dna')}")
                if sg.get("link"):
                    print(f"        链接 {sg.get('link')}")
                if meta:
                    m = json.dumps(meta, ensure_ascii=False)
                    print(f"        元数据 {m[:200]}{'…' if len(m) > 200 else ''}")
                for na in sg.get("assets", []):
                    print(f"      · [笔记] {na.get('name')}  [{na.get('type','?')}] {na.get('status','')}")
                    if na.get("dna"):
                        print(f"        DNA {na.get('dna')}")
                    if na.get("link"):
                        print(f"        链接 {na.get('link')}")
            for e in d.get("edges", []):
                print(f"   🔗 边 · {e.get('source')} → {e.get('target')} [{e.get('type')}]")
                if e.get("label"):
                    print(f"        ↳ {e.get('label')}")
    print()


# ─────────────────────────── register / node（v1.3·2026-09-03·本地注册图谱）───────────────────────────

REG_GROUPS = ["模型层", "数据层", "工具层"]   # 本地注册图谱默认分组（可 --group 追加任意组）


def cmd_register_graph(name: str, display: str = ""):
    """lh topo register <图谱名> [--display 显示名] — 新增本地注册图谱（组骨架空资产）
    sync_from=live-check → lh topo sync 走活体校验（模型/文件/库实时探测）"""
    if not name.strip():
        raise SystemExit("  ❌ 用法: lh topo register <图谱名>   [--display 显示名]")
    try:
        _find_topo_file(name)
        raise SystemExit(f"  ❌ 图谱「{name}」已存在（改节点用: lh topo node <图谱> --group … --name …）")
    except SystemExit as e:
        if "未找到图谱" not in str(e):
            raise
    display = display or f"🧠 {name.strip()} v1.0"
    data = {
        "schema": "longhun-topo-v1",
        "topo_name": name.strip(),
        "display": display,
        "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
        "created": datetime.now().astimezone().isoformat(timespec="seconds"),
        "last_sync": "",
        "sync_from": "live-check",
        "groups": [{"name": g, "assets": []} for g in REG_GROUPS],
    }
    target = TOPO_DIR / f"{name.strip()}_legion_topo.json"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  🕸️  图谱注册成功 · {display}")
    print(f"     文件 {target.relative_to(ROOT)} · 组: {' / '.join(REG_GROUPS)}")
    print("     注册节点: lh topo node <图谱> --group 模型层 --name … --type model --dna … --status …")
    print()


def cmd_node_add(keyword: str, group: str = "", name: str = "", ntype: str = "other",
                 dna: str = "", status: str = "🟢 可用", path: str = "",
                 source: str = "", desc: str = "", link: str = ""):
    """lh topo node <图谱名> --group <层> --name <节点> --type <type> --dna <DNA>
    [--status 状态] [--path 路径] [--source 来源] [--desc 描述] [--link 链接]
    同名节点=更新；组不存在自动创建；link 缺省回退 path/source（保 verify 无缺链接）"""
    if not keyword.strip():
        raise SystemExit("  ❌ 用法: lh topo node <图谱名> --group … --name … --type … --dna …")
    f, data = _find_topo_file(keyword)
    if not group.strip() or not name.strip():
        raise SystemExit("  ❌ --group 与 --name 必填")
    groups = data.setdefault("groups", [])
    g = next((x for x in groups if x.get("name") == group.strip()), None)
    if g is None:
        g = {"name": group.strip(), "assets": []}
        groups.append(g)
    asset = {
        "name": name.strip(),
        "type": ntype.strip() or "other",
        "dna": dna.strip(),
        "status": status.strip() or "🟢 可用",
        "link": (link.strip() or path.strip() or source.strip() or ""),
    }
    for k, v in (("path", path), ("source", source), ("desc", desc)):
        if v.strip():
            asset[k] = v.strip()
    asset["registered_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    updated = False
    for i, a in enumerate(g["assets"]):
        if a.get("name") == name.strip():
            g["assets"][i] = asset
            updated = True
            break
    if updated:
        print(f"  🔄 节点「{name.strip()}」已更新 → {group.strip()}")
    else:
        g["assets"].append(asset)
        print(f"  ✅ 节点「{name.strip()}」注册 → {group.strip()}")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    green, yellow, neutral = asset_stats(data)
    print(f"     图谱 {data.get('display')} · 节点 {green+yellow+neutral} · 🟢{green} 🟡{yellow}")


# ── v1.7 对外交付文档自动拓扑同步（12_DOCS ↔ 图谱）─────────────────
# 白名单镜像 lh_doc_sync.DELIVERY_DOCS（11份交付文档）：对外文档站 9 站内文档 + 30分钟接入 + 文档体系
DOC_SYNC_MAP = [
    ("12_DOCS/DEPENDENCIES.md", "document", "依赖清单"),
    ("12_DOCS/INSTALL.md", "document", "安装指南"),
    ("12_DOCS/QUICKSTART.md", "document", "快速开始"),
    ("12_DOCS/USAGE.md", "document", "使用说明"),
    ("12_DOCS/API_REFERENCE.md", "document", "API技术文档"),
    ("12_DOCS/JSONRPC.md", "document", "JSON-RPC协议"),
    ("12_DOCS/MCP_GUIDE.md", "document", "MCP接入指南"),
    ("12_DOCS/NOTION_MCP_GUIDE.md", "document", "Notion MCP指南"),
    ("12_DOCS/TROUBLESHOOTING.md", "document", "故障排查"),
    ("12_DOCS/龍魂对外交付文档体系-v1.0.md", "document", "对外交付文档体系"),
    ("12_DOCS/30分钟接入龙魂系统.md", "article", "30分钟接入指南"),
]

# 图谱类型定义表（写 data.types · lh topo <图谱> status/list 可用）
TOPOLOGY_TYPES = {
    "document": "正式文档（DEPENDENCIES/INSTALL/USAGE/API_REFERENCE/JSONRPC/MCP_GUIDE/NOTION_MCP_GUIDE/TROUBLESHOOTING/体系总览）",
    "article": "导读文章/对外发布稿/30分钟接入指南",
    "report": "反馈报告（docs_feedback_weekly 周报产物）",
    "asset": "扩散素材包（含 4 平台 copy 子项）",
    "copy": "平台扩散文案（v2ex/osc/zhihu/hackernews）",
    "endpoint": "反馈入口/耻辱墙（反馈链路端点）",
    "issue": "GitHub Issue（#99 对外文档上线公告）",
}

_AUTO_SYNC_LOG = Path(os.path.expanduser("~/.longhun/topo_auto_sync.log"))

# ── v1.8 对外公开化：耻辱墙审计事件 + 文档站公开页（2026-09-05）──
SITE_DOC_DIR = ROOT / "docs-site" / "docs"         # 文档站源目录（mkdocs docs_dir）
SITE_TOPO_DIR = SITE_DOC_DIR / "topology"          # 文档站拓扑状态页目录
SHAME_DIR = STATE_DIR / "shame_wall"
SHAME_JSON = SHAME_DIR / "shame_wall.json"         # 归一审判官耻辱墙（judge v1.1 结构）
TOPO_AUDIT_LOG = SHAME_DIR / "topo_audit.jsonl"    # 拓扑变更/告警事件流（append-only）
TOPO_PUBLIC_PAGE = "对外交付状态页.md"              # 本地状态页产物名
TOPO_DEPLOY_LOG = STATE_DIR / "topo_auto_deploy.log"  # sync 自动部署链日志（v1.9）
KUNPENG = "root@119.13.90.27:/opt/longhun-system/docs-site/"
KUNPENG_HOST = "root@119.13.90.27"
SSH_KEY = Path.home() / ".ssh" / "longhun_kunpeng_ed25519"

# ── v2.0 可验证神经中枢（2026-09-05·自证/自审计/自响应/对外协作）──
SNAPSHOT_DIR = STATE_DIR / "topo_snapshots"          # 每次 export-page 落时间戳快照（保留 30 天·自愈恢复源）
SNAPSHOT_KEEP_DAYS = 30
TOPO_API_DIR = ROOT / "docs-site" / "topology-api"   # 公共 API 静态 JSON（rsync 鲲鹏 + nginx alias /api/topo/）
TOPO_WEEKLY_DIR = STATE_DIR / "audit" / "topo_weekly"  # 每周拓扑审计报告（GPG 签后归档）
GENESIS_FILE = SHAME_DIR / "topo_chain_genesis.json" # 事件链创世（legacy 事件段聚合哈希）
API_BASE = "https://uid9622.cn/api/topo/"            # 公共 API 基址（对外文档/页面链接）
ISSUE_NEW_URL = ("https://github.com/UID9622/longhun-system/issues/new"
                 "?template=shame_report.yml&labels=topo-feedback")  # 拓扑反馈（耻辱墙模板预填 topo-feedback 标签）
TOPO_FEEDBACK_LABEL = "topo-feedback"            # 拓扑反馈统一标签（Issue labels + 耻辱墙事件分类）
TOPO_SITE_ARCHIVE_DIR = SITE_TOPO_DIR / "archive"          # 站点归档目录（→ /docs/topology/archive/）
TOPO_ROOT_DECL = SITE_TOPO_DIR / "ROOT_HASH_DECLARATION.md"  # 根哈希公开声明页（GPG 分离签名）
GPG_SIGN_BIN = ROOT / "08_BIN" / "lh_gpg_sign.py"          # GPG 分离签名引擎
GH_API_BASE = "https://api.github.com/repos/UID9622/longhun-system"  # 本仓库 GitHub API 基址
STALE_HOURS = 24                                     # 🟡 持续阈值 → 自响应（heal）

# ── v1.9 文档站交互检索前端（export-page 每次生成 topo_live.js·纯前端零后端）──
_TOPO_LIVE_JS = r'''(function () {
  'use strict';
  var TYPE_CN = { document: '文档', article: '文章', asset: '素材', copy: '平台文案', endpoint: '入口', issue: '公告', report: '报告' };
  var style = document.createElement('style');
  style.textContent = [
    '#topo-live{font-size:14px;line-height:1.75;margin:10px 0}',
    '#topo-live-q{width:100%;box-sizing:border-box;padding:10px 14px;font-size:15px;border:1px solid #d1d5db;border-radius:10px;outline:none;background:#fff}',
    '#topo-live-q:focus{border-color:#4f46e5;box-shadow:0 0 0 3px rgba(79,70,229,.15)}',
    '.tlc{color:#64748b;font-size:13px;margin:8px 2px}',
    '.tlr{display:flex;gap:10px;align-items:baseline;padding:7px 10px;border-bottom:1px solid #f1f5f9;border-radius:8px}',
    '.tlr:hover{background:#f8fafc}',
    '.tldot{width:8px;height:8px;border-radius:50%;flex:none;align-self:center}',
    '.tln{font-weight:600;white-space:nowrap}',
    '.tldna{flex:none;font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#6d4c41;background:#efe6d5;border-radius:4px;padding:1px 6px;cursor:pointer;white-space:nowrap;max-width:22em;overflow:hidden}',
    '.tlm{color:#64748b;font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
    '.tla{margin-left:auto;flex:none;text-decoration:none;color:#4f46e5;font-size:13px;font-weight:600}',
    '.tle{margin:12px 2px;color:#334155;font-size:13px;line-height:1.9}'
  ].join('\n');
  document.head.appendChild(style);
  var q = document.getElementById('topo-live-q');
  var cnt = document.getElementById('topo-live-count');
  var list = document.getElementById('topo-live-list');
  if (!q || !cnt || !list) { return; }
  var data = null;
  fetch('data.json', { cache: 'no-store' })
    .then(function (r) { if (!r.ok) { throw new Error('HTTP ' + r.status); } return r.json(); })
    .then(function (d) { data = d; render(''); })
    .catch(function () { cnt.textContent = '⚠️ 交互数据加载失败（data.json 未就绪）'; });
  function find(f) {
    if (!f) { return data.nodes; }
    var k = f.toLowerCase();
    return data.nodes.filter(function (n) {
      return [n.name, n.group, n.type, TYPE_CN[n.type] || '', n.doc_type, n.title, n.desc, n.dna]
        .join(' ').toLowerCase().indexOf(k) >= 0;
    });
  }
  function row(n) {
    var r = document.createElement('div'); r.className = 'tlr';
    var dot = document.createElement('span'); dot.className = 'tldot';
    var st = String(n.status || '');
    dot.style.background = st.indexOf('🟢') >= 0 ? '#16a34a' : (st.indexOf('🟡') >= 0 ? '#d97706' : '#94a3b8');
    dot.title = st;
    var name = document.createElement('span'); name.className = 'tln';
    name.textContent = n.name;
    var meta = document.createElement('span'); meta.className = 'tlm';
    meta.textContent = '  ' + (TYPE_CN[n.type] || n.type || '节点')
      + (n.doc_type ? ' · ' + n.doc_type : '') + ' · ' + (n.group || '');
    r.appendChild(dot); r.appendChild(name);
    if (n.dna) {
      var dna = document.createElement('span'); dna.className = 'tldna';
      dna.textContent = (n.dna.slice(0, 8) || '?');
      dna.title = 'DNA 前缀（v2.0 可验证）· 点击展开/收起完整 DNA';
      dna.addEventListener('click', function () {
        dna.textContent = dna._full ? (n.dna.slice(0, 8)) : n.dna;
        dna._full = !dna._full;
      });
      r.appendChild(dna);
    }
    r.appendChild(meta);
    var tail = document.createElement('span'); tail.className = 'tla';
    if (n.link) {
      var a = document.createElement('a');
      a.href = n.link; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.textContent = '↗ 打开';
      r.appendChild(a);
    } else {
      tail.style.color = '#94a3b8'; tail.style.fontWeight = 'normal';
      tail.textContent = '🔒 内部资产';
      r.appendChild(tail);
    }
    return r;
  }
  function edgesBlock() {
    var w = document.createElement('div'); w.className = 'tle';
    w.textContent = '🔗 关联边 ' + (data.edges ? data.edges.length : 0) + ' 条：'
      + (data.edges || []).map(function (e) {
        return e.source + ' → ' + e.target + (e.label ? '（' + e.label + '）' : '');
      }).join(' · ');
    return w;
  }
  function render(f) {
    if (!data) { return; }
    var rows = find(f);
    cnt.textContent = '共 ' + data.nodes.length + ' 个节点 · 当前匹配 ' + rows.length + ' 个';
    list.innerHTML = '';
    rows.forEach(function (n) { list.appendChild(row(n)); });
    if (!f) { list.appendChild(edgesBlock()); }
  }
  q.addEventListener('input', function () { render(q.value.trim()); });
  // v2.0: 5 分钟轮询公共 status API → 根哈希变化即提示刷新（无后端 · 404 静默）
  var banner = document.getElementById('topo-live-updated');
  function pollStatus() {
    fetch('/api/topo/status.json', { cache: 'no-store' })
      .then(function (r) { if (!r.ok) { return null; } return r.json(); })
      .then(function (st) {
        if (st && data && banner && st.root_hash && st.root_hash !== data.root_hash) {
          banner.style.display = 'inline';
        }
      })
      .catch(function () { /* 本地/未部署 API → 静默 */ });
  }
  setInterval(pollStatus, 300000);
  pollStatus();
})();'''

# v1.9 交互检索 HTML 块（嵌入状态页 index.md 尾部·script 置于 div 块内防 markdown 拆散）
_TOPO_LIVE_HTML = """
## 🔍 图谱检索（实时过滤 · 无需后端）

<div id="topo-live">
<input id="topo-live-q" type="search" placeholder="输入节点名称 / 类型 / DNA / 关键词…  例：发布稿 · 耻辱墙 · article · D" autocomplete="off">
<p id="topo-live-count" class="tlc"></p>
<div id="topo-live-list"></div>
<script defer src="topo_live.js"></script>
</div>
"""


def _extract_doc_meta(rel: str) -> dict:
    """提取 12_DOCS 交付文档元信息：标题/文档版本行/DNA/大小/mtime/GPG签名状态"""
    p = ROOT / rel
    if not p.exists():
        return {"exists": False}
    txt = p.read_text(encoding="utf-8", errors="ignore")
    m_dna = re.search(r"#龍[^\s\n·<]*", txt[:800])
    m_t = re.search(r"^#\s*(.+)$", txt, re.M)
    m_v = re.search(r"^> 文档版本:\s*(.+)$", txt, re.M)
    st = p.stat()
    return {
        "exists": True,
        "title": (m_t.group(1).strip() if m_t else p.stem),
        "dna": m_dna.group(0) if m_dna else "",
        "version": m_v.group(1).strip() if m_v else "",
        "size": st.st_size,
        # 微秒精度（秒级截断会让「变更后立刻 sync」判定失效）
        "mtime": datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="microseconds"),
        "signed": Path(str(p) + ".asc").exists(),
        "path": rel,
    }


def cmd_topo_docs_sync(keyword: str, dry_run: bool = False):
    """lh topo sync <图谱> — 12_DOCS 交付文档 ↔ 图谱自动拓扑同步 v1.7
    白名单 11 份交付文档：扫描 DNA/大小/修改时间/GPG签名 → 补全/更新 document+article 节点
    → 移除已消失文档 → 类型定义表入 data.types → 自动 verify → 写 ~/.longhun/topo_auto_sync.log
    图谱落盘 auto_docs_sync=true（lh doc-sync 后钩子自动触发）"""
    if not keyword.strip():
        raise SystemExit("  ❌ 用法: lh topo sync <图谱名>（12_DOCS 文档自动拓扑同步）")
    f, data = _find_topo_file(keyword)
    graph = data.get("display")
    scan = [{"rel": rel, "type": t, "subtype": sub, "stem": Path(rel).stem}
            for rel, t, sub in DOC_SYNC_MAP]
    scan_idx = {it["stem"]: it for it in scan}

    def _node_map():
        out = {}
        for g in data.get("groups", []):
            for a in g.get("assets", []):
                out[a.get("name")] = (g, a)
        return out

    nodelist = _node_map()
    added, updated, removed = [], [], []
    for it in scan:
        meta = _extract_doc_meta(it["rel"])
        entry = nodelist.get(it["stem"])
        if not meta["exists"]:
            if entry is not None:
                removed.append(it["stem"])
            continue
        if entry is None:
            added.append(it)
            continue
        g, a = entry
        cur = (a.get("dna"), a.get("size"), a.get("mtime"), a.get("doc_type"),
               a.get("type") != it["type"])
        new = (meta["dna"], meta["size"], meta["mtime"], it["subtype"],
               a.get("type") != it["type"])
        if cur != new:
            updated.append(it["stem"])

    # 类型对齐（v1.7 规整）：assets → asset（扩散素材包）
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            if a.get("type") == "assets":
                a["type"] = "asset"
                updated.append(a.get("name"))
    updated = sorted(set(updated))

    print(f"\n  🕸️  12_DOCS 拓扑同步 · {graph}")
    print(f"     白名单扫描 {len(scan)} 份 · 新增 {len(added)} · 更新 {len(updated)}"
          f" · 移除 {len(removed)}" + (" · 🔍 dry-run 不落盘" if dry_run else ""))
    for it in added:
        print(f"     ➕ 新文档 → {it['stem']} [{it['type']}·{it['subtype']}]")
    for nm in updated:
        print(f"     ✏️  更新 {nm}")
    for nm in removed:
        print(f"     ➖ 移除 {nm}")
    if dry_run:
        print()
        return

    # types 元数据 + auto_docs_sync 标记
    data["types"] = dict(TOPOLOGY_TYPES)
    data["auto_docs_sync"] = True
    # 补齐/更新节点
    doc_group = next((g for g in data.get("groups", []) if g.get("name") == "D发布"), None)
    if doc_group is None:
        doc_group = {"name": "D发布", "assets": []}
        data.setdefault("groups", []).append(doc_group)
    existing = {a.get("name"): a for a in doc_group["assets"]}
    for it in added:
        meta = _extract_doc_meta(it["rel"])
        suffix = f" · {meta['version']}" if meta.get("version") else ""
        asset = {
            "name": it["stem"], "type": it["type"], "doc_type": it["subtype"],
            "dna": meta["dna"], "status": "🟢 可用",
            "link": it["rel"], "path": it["rel"],
            "size": meta["size"], "mtime": meta["mtime"],
            "signed": meta["signed"], "version": meta.get("version", ""),
            "title": meta["title"],
            "desc": f"对外交付文档·{it['subtype']}{suffix} · {meta['size']}字节"
                    f" · GPG{'已签' if meta['signed'] else '未签'}",
            "registered_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
        doc_group["assets"].append(asset)
    for nm in updated:
        it = scan_idx.get(nm)
        a = existing.get(nm)
        if it is None or a is None:
            continue
        meta = _extract_doc_meta(it["rel"])
        a["type"] = it["type"]
        a["doc_type"] = it["subtype"]
        a["dna"] = meta["dna"]
        a["link"] = it["rel"]
        a["path"] = it["rel"]
        a["size"] = meta["size"]
        a["mtime"] = meta["mtime"]
        a["signed"] = meta["signed"]
        a["version"] = meta.get("version", "")
        a["title"] = meta["title"]
        suffix = f" · {meta['version']}" if meta.get("version") else ""
        a["desc"] = f"对外交付文档·{it['subtype']}{suffix} · {meta['size']}字节" \
                    f" · GPG{'已签' if meta['signed'] else '未签'}"
    # 移除已消失文档节点（仅限本次白名单注册名）
    doc_group["assets"] = [a for a in doc_group["assets"]
                           if a.get("name") not in set(removed)]

    data["last_sync"] = datetime.now().astimezone().isoformat(timespec="seconds")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    _archive_snapshot(data)
    res = _auto_verify_write("topo-docs-auto", data)
    # 钩子日志
    with contextlib.suppress(Exception):
        _AUTO_SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
        with _AUTO_SYNC_LOG.open("a", encoding="utf-8") as lf:
            lf.write(json.dumps({
                "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                "tool": "lh-topo-docs-sync", "graph": data.get("topo_name"),
                "scan": len(scan), "added": len(added), "updated": len(updated),
                "removed": len(removed), "ok": res.get("ok"),
                "nodes": res.get("nodes"),
            }, ensure_ascii=False) + "\n")
    # v1.9: 耻辱墙变更事件（topo_change·带操作明细/severity·移除=warning）+ 自动部署链
    if added or updated or removed:
        ops = [{"name": it["stem"], "type": it.get("type"), "op": "add",
                "severity": "info"} for it in added]
        ops += [{"name": nm, "type": scan_idx[nm]["type"] if nm in scan_idx else None,
                 "op": "update", "severity": "info"} for nm in updated]
        ops += [{"name": n, "op": "remove", "severity": "warning"} for n in removed]
        _shame_topo_append(
            "topo_change",
            f"对外交付图谱拓扑变更 → 新增{len(added)}·更新{len(updated)}"
            f"·移除{len(removed)} · 节点{res.get('nodes')}"
            f" · verify {'✅通过' if res.get('ok') else '❌失败'}",
            color="🟡" if (removed or not res.get("ok")) else "🟢",
            warn=1 if removed else (0 if res.get("ok") else 1),
            ops=ops, severity="warning" if removed else "info")
        # v1.9: 变更即自动更新公开页 + 构建 + 部署鲲鹏（零变更不部署·节能）
        _topo_auto_deploy(keyword)
    elif not res.get("ok"):
        _shame_topo_append("topo_verify_alert",
                           f"拓扑自动校验告警 · 对外交付图谱 节点{res.get('nodes')}"
                           f" · 缺口{len(res.get('gaps') or [])}条",
                           color="🔴", bad=len(res.get("gaps") or []),
                           severity="warning")
    print(f"     日志 {_AUTO_SYNC_LOG}")
    print()


# ─────────────────────────── v1.8 对外公开化（2026-09-05）───────────────────────────
# 让拓扑本身成为对外交付：summary/search/export/export-page/audit-log + 耻辱墙事件链

# ── v2.0 Merkle 事件链（可验证审计链）─────────────────────────────

def _ev_self_hash(ev: dict) -> str:
    """事件自证哈希 = sha256(除 hash 外全字段稳定序列化) 前 16 大写
    sort_keys 稳定序 → 外部观察者可独立重算验证"""
    d = dict(ev)
    d.pop("hash", None)
    raw = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16].upper()


def _chain_genesis() -> str:
    """Merkle 链创世根：聚合所有 legacy（无 seq）事件 raw 行哈希并持久化
    （append-only 不重写历史·只一次性记录·已存在读缓存）"""
    try:
        if GENESIS_FILE.is_file():
            g = json.loads(GENESIS_FILE.read_text(encoding="utf-8"))
            if g.get("genesis"):
                return g["genesis"]
    except Exception:  # noqa: BLE001
        pass
    legacy = []
    with contextlib.suppress(Exception):
        if TOPO_AUDIT_LOG.is_file():
            for line in TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    is_chain = "seq" in json.loads(line)
                except Exception:  # noqa: BLE001
                    is_chain = False
                if not is_chain:
                    legacy.append(line)
    genesis = hashlib.sha256("\n".join(legacy).encode("utf-8")).hexdigest()[:16].upper()
    try:
        GENESIS_FILE.parent.mkdir(parents=True, exist_ok=True)
        GENESIS_FILE.write_text(json.dumps(
            {"genesis": genesis, "created": datetime.now().astimezone().isoformat(timespec="seconds"),
             "n_legacy": len(legacy), "alg": "sha256(legacy raw lines 串联)"},
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    return genesis


def _chain_state() -> tuple:
    """事件流尾部链状态 → (最新 seq, 最新 self hash 或 genesis)
    append-only 文件 → 只扫尾段即可（取最后一个带 seq 的行）"""
    last_seq, last_hash = 0, _chain_genesis()
    with contextlib.suppress(Exception):
        if TOPO_AUDIT_LOG.is_file():
            for line in reversed(TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines()):
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                if isinstance(ev, dict) and ev.get("seq"):
                    last_seq = int(ev["seq"])
                    if ev.get("hash"):
                        last_hash = ev["hash"]
                    break
    return last_seq, last_hash


def _audit_chain_rows():
    """全部审计事件（含 raw 原始行·供 audit-chain/audit-verify）→ [(raw, ev|None)]"""
    rows = []
    with contextlib.suppress(Exception):
        if TOPO_AUDIT_LOG.is_file():
            for line in TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append((line, json.loads(line)))
                except Exception:  # noqa: BLE001
                    rows.append((line, None))
    return rows


def _shame_topo_append(kind: str, detail: str, color: str = "🟢", bad: int = 0, warn: int = 0,
                       ops=None, severity: str = "info"):
    """拓扑审计事件 → 耻辱墙（v1.9 深化 + v2.0 Merkle 链）：
    topo_audit.jsonl（append-only）事件行带 ops 操作明细 + severity
    + seq/prev_hash/hash（可验证链·创世为 legacy 段聚合哈希）· shame_wall.json 同步"""
    with contextlib.suppress(Exception):
        SHAME_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().astimezone()
        seq, prev = _chain_state()
        ev = {"ts": ts.isoformat(timespec="seconds"), "type": kind, "color": color,
              "bad": bad, "warn": warn, "severity": severity,
              "ops": [dict(o) for o in (ops or [])], "detail": detail,
              "seq": seq + 1, "prev_hash": prev}
        ev["hash"] = _ev_self_hash(ev)
        with TOPO_AUDIT_LOG.open("a", encoding="utf-8") as lf:
            lf.write(json.dumps(ev, ensure_ascii=False) + "\n")
        if SHAME_JSON.is_file():
            sj = json.loads(SHAME_JSON.read_text(encoding="utf-8"))
            recs = sj.setdefault("记录", [])
            reason = detail
            if ops:
                n_add = sum(1 for o in ops if o.get("op") == "add")
                n_up = sum(1 for o in ops if o.get("op") == "update")
                n_rm = sum(1 for o in ops if o.get("op") == "remove")
                if n_add or n_up or n_rm:
                    reason += f" · 明细 {n_add}增/{n_up}更/{n_rm}移"
            recs.append({"date": ts.date().isoformat(),
                         "time": ts.isoformat(timespec="seconds"),
                         "type": kind, "color": color, "bad": bad, "warn": warn,
                         "severity": severity, "reason": reason})
            sj["总记录数"] = len(recs)
            sj["生成时间"] = ts.isoformat(timespec="seconds")
            SHAME_JSON.write_text(json.dumps(sj, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")


_TYPE_CN = {"document": "文档", "article": "文章", "asset": "素材", "copy": "平台文案",
            "endpoint": "入口", "issue": "公告", "report": "报告"}


def _topo_auto_deploy(keyword: str) -> bool:
    """v1.9 sync 变更后自动部署链：export-page（重生成公开页+首页区块+data.json）
    → mkdocs build → rsync 鲲鹏 → 写 ~/.longhun/topo_auto_deploy.log
    失败不中断主流程 · 自动触发仅在图谱实际变更时（零变更不部署·节能）"""
    import shutil as _sh
    started = datetime.now().astimezone()
    ok, notes = True, []
    try:
        # 1) 重生成公开页（覆盖本地 docs/topology/对外交付状态页.md + 站点源 + 首页区块）
        cmd_topo_export_page(keyword)
        notes.append("export-page 公开页已刷新")
        # 2) mkdocs build（文档站静态构建）
        mkdocs_bin = (_sh.which("mkdocs")
                      or str(Path.home() / "Library" / "Python/3.14/bin/mkdocs"))
        r = subprocess.run([mkdocs_bin, "build", "-f", "mkdocs.yml"],
                           cwd=str(ROOT / "docs-site"), capture_output=True, text=True,
                           timeout=300)
        tail = ((r.stdout + r.stderr).strip().splitlines() or [""])[-1][:120]
        notes.append(f"mkdocs build {'✅' if r.returncode == 0 else '❌'} {tail}")
        ok = ok and r.returncode == 0
        # 3) rsync 静态站 → 鲲鹏
        if ok:
            ssh = (f"ssh -i {SSH_KEY} -o ConnectTimeout=10"
                   f" -o StrictHostKeyChecking=accept-new")
            r = subprocess.run(["rsync", "-az", "-e", ssh, "site/", KUNPENG],
                               cwd=str(ROOT / "docs-site"), capture_output=True,
                               text=True, timeout=300)
            notes.append("rsync 鲲鹏 ✅" if r.returncode == 0
                         else f"rsync ❌ {r.stderr.strip()[:180]}")
            ok = ok and r.returncode == 0
            # 3b) rsync 公共 API 静态 JSON → 鲲鹏 docs-site/topology-api/（v2.0 对外协作）
            _api_src = ROOT / "docs-site" / "topology-api"
            if _api_src.is_dir():
                r = subprocess.run(
                    ["rsync", "-az", "-e", ssh, "topology-api/",
                     f"root@119.13.90.27:/opt/longhun-system/docs-site/topology-api/"],
                    cwd=str(ROOT / "docs-site"), capture_output=True, text=True, timeout=120)
                notes.append("rsync topo-api ✅" if r.returncode == 0
                             else f"topo-api rsync ❌ {r.stderr.strip()[:160]}")
                ok = ok and r.returncode == 0
    except Exception as e:  # noqa: BLE001
        ok = False
        notes.append(f"部署异常 {e}")
    TOPO_DEPLOY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(Exception), TOPO_DEPLOY_LOG.open("a", encoding="utf-8") as lf:
            lf.write(json.dumps({
                "ts": started.isoformat(timespec="seconds"),
                "graph": keyword, "ok": ok,
                "elapsed_ms": int((datetime.now().astimezone() - started).total_seconds() * 1000),
                "steps": notes,
            }, ensure_ascii=False) + "\n")
    if not ok:
        print(f"     ⚙️ 自动部署失败（已记 {TOPO_DEPLOY_LOG}）· {' | '.join(notes)}")
    else:
        print(f"     ⚙️ 自动部署完成 · 公开页已刷新上线 https://uid9622.cn/docs/topology/ · 日志 {TOPO_DEPLOY_LOG}")
    return ok


def _topo_known_types() -> list:
    """全局拓扑节点类型集合（events --node-type 过滤提示用·v2.3 审计深化）"""
    ts = set()
    for f in list_topos():
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for g in d.get("groups", []):
            for a in g.get("assets", []):
                if a.get("type"):
                    ts.add(str(a["type"]))
    return sorted(ts)


def _topo_events_rows(limit: int = 20, kind: str = "", node_type: str = "") -> list:
    """读耻辱墙拓扑事件流（topo_audit.jsonl 反向 N 条·兼容旧事件无 ops/severity）
    v2.3: 细粒度审计过滤 —— kind=事件类型 / node_type=变更节点类型（任一 ops 命中）"""
    rows = []
    if TOPO_AUDIT_LOG.is_file():
        for line in TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if kind and r.get("type") != kind:
                continue
            if node_type and not any(o.get("type") == node_type
                                     for o in (r.get("ops") or [])):
                continue
            rows.append(r)
    rows.reverse()
    return rows[: max(1, limit)]


def cmd_topo_events(keyword: str = "", limit: int = 20, json_out: bool = False,
                    kind: str = "", node_type: str = ""):
    """lh topo events [图谱名] [--limit N] [--kind 事件类型] [--node-type 节点类型]
    — 近期拓扑事件（耻辱墙事件流·带操作明细·v2.3 支持细粒度过滤审计）"""
    rows = _topo_events_rows(limit, kind=kind, node_type=node_type)
    if json_out:
        print(json.dumps({"topo": keyword or "全部", "total": len(rows),
                          "filters": {"kind": kind, "node_type": node_type},
                          "events": rows}, ensure_ascii=False, indent=2))
        return
    _f = " / ".join(x for x in [f"类型={kind}" if kind else "",
                                 f"节点类型={node_type}" if node_type else ""] if x)
    print(f"\n  🕰️  拓扑事件 · {keyword or '全部图谱'} · 最近 {len(rows)} 条"
          + (f" · 过滤[{_f}]" if _f else "") + f" · {TOPO_AUDIT_LOG}")
    op_cn = {"add": "新增", "update": "更新", "remove": "移除"}
    for r in rows:
        color = r.get("color", "🟢")
        sev = r.get("severity") or ("warning" if (r.get("warn") or r.get("bad")) else "info")
        sev_txt = "⚠️" if sev == "warning" else ""
        print(f"     [{r.get('ts')}] {r.get('type')} {color} {sev_txt} · {r.get('detail', '')}")
        for o in r.get("ops") or []:
            mark = "+" if o.get("op") == "add" else ("~" if o.get("op") == "update" else "-")
            tag = "warning" if o.get("severity") == "warning" else ""
            print(f"         {mark} {o.get('name')} [{o.get('op') and op_cn.get(o.get('op')) or ''}"
                  f"{('/' + str(o.get('type'))) if o.get('type') else ''}] {tag}")
    if not rows:
        if node_type:
            print(f"     （无匹配事件 · 已知节点类型: {', '.join(_topo_known_types())}）")
        else:
            print("     （暂无事件 · sync 变更/校验告警将自动记录至此）")
    print()


def cmd_topo_ask(keyword: str = "", question: str = "", json_out: bool = False):
    """lh topo ask [图谱名] --query <自然语言问题> — 自然语言拓扑查询 v1.9
    例: 有哪些文档？ / 最近更新了什么？ / 和耻辱墙有什么关系？ / 发布了哪些文章？"""
    if not question.strip():
        raise SystemExit("  ❌ 用法: lh topo ask <图谱名> <自然语言问题>   "
                         "例: lh topo 对外交付 ask 有哪些文档")
    kw = keyword.strip() or "对外交付"
    f, data = _find_topo_file(kw)
    q = question.strip()
    intent = _ask_intent(q)
    assets = [a for g in data.get("groups", []) for a in g.get("assets", [])]
    groups = data.get("groups", [])

    def _lines_of(nodes: list) -> list:
        out = []
        for a in nodes:
            t = a.get("type") or "?"
            cn = _TYPE_CN.get(t, t)
            doc = (a.get("doc_type") or "")
            tag = f"{cn}·{doc}" if doc else cn
            link = _public_link(a)
            out.append(f"· {a.get('name')}（{tag}）{' ↗ ' + link if link else ' 🔒内部'}")
        return out

    if intent == "documents":
        nodes = [a for a in assets if a.get("type") == "document"]
        head = f"答：共 {len(nodes)} 份对外文档（全部可在线阅读 · https://uid9622.cn/docs/）："
        lines = _lines_of(nodes)
    elif intent == "articles":
        nodes = [a for a in assets if a.get("type") == "article"]
        head = f"答：已发布文章 {len(nodes)} 篇："
        lines = _lines_of(nodes)
    elif intent == "assets":
        nodes = [a for a in assets if a.get("type") == "asset"]
        head = f"答：素材资产 {len(nodes)} 项："
        lines = _lines_of(nodes)
    elif intent == "copies":
        nodes = [a for a in assets if a.get("type") == "copy"]
        head = f"答：扩散平台文案 {len(nodes)} 套（发布稿已同步以下平台）："
        lines = _lines_of(nodes)
    elif intent == "issues":
        nodes = [a for a in assets if a.get("type") in ("issue", "endpoint")]
        head = f"答：对外公告 / 入口 {len(nodes)} 个："
        lines = _lines_of(nodes)
    elif intent == "update":
        evs = _topo_events_rows(4)
        head = (f"答：最近同步 {data.get('last_sync', '—')}。"
                f"近期变更事件 {len(evs)} 条：")
        lines = []
        for r in evs:
            lines.append(f"· [{r.get('ts')}] {r.get('color', '')} {r.get('detail', '')}")
            for o in r.get("ops") or []:
                lines.append(f"    {'+' if o.get('op') != 'remove' else '-'} {o.get('name')}"
                             f"（{'新增' if o.get('op') == 'add' else ('更新' if o.get('op') == 'update' else '移除')}）")
    elif intent == "shame":
        edges = data.get("edges", [])
        wall_edges = [e for e in edges
                      if "耻辱墙" in str(e.get("source")) or "耻辱墙" in str(e.get("target"))]
        evs = _topo_events_rows(3)
        head = (f"答：耻辱墙是交付反馈的最终落点（Issue 模板·社区可提交）。"
                f"拓扑中关联边 {len(wall_edges)} 条 · 近期事件 {len(evs)} 条：")
        lines = [f"· {e.get('source')} → {e.get('target')}（{e.get('type')}"
                 f"{' · ' + str(e.get('label')) if e.get('label') else ''}）"
                 for e in wall_edges]
        for r in evs:
            lines.append(f"· [{r.get('ts')}] {r.get('color', '')} {r.get('detail', '')}")
        if not wall_edges and not evs:
            lines.append("· （暂未记录事件）")
    elif intent == "edges":
        head = f"答：图谱关联边共 {len(data.get('edges', []))} 条（数据流向）："
        lines = [f"· {e.get('source')} → {e.get('target')}"
                 f"（{e.get('type')}{' · ' + str(e.get('label')) if e.get('label') else ''}）"
                 for e in data.get("edges", [])]
    elif intent == "types":
        dist = _type_dist(data)
        head = "答：类型分布："
        lines = [f"· {_TYPE_CN.get(k, k)} {v} 个"
                 + ("（文档站 https://uid9622.cn/docs/）" if k == "document" else "")
                 for k, v in dist.items()]
    elif intent == "verify":
        s = _topo_summary(data)
        tv = s.get("verify") or {}
        head = (f"答：{s['display']} —— 节点 {s['nodes']}（🟢{s['green']}"
                f" · 🟡{s['yellow']}）· 边 {s['edges']} · "
                f"自动校验{'全绿 ✅' if tv.get('ok') else '有缺口 ⚠️'}"
                f" · 最近同步 {s['last_sync']}。公开页 https://uid9622.cn/docs/topology/")
        lines = []
    else:  # search 兜底：关键词节点搜索
        hay_hits = []
        for a in assets:
            hay = " ".join(str(a.get(k, "")) for k in
                           ("name", "type", "doc_type", "dna", "title", "desc", "link")).lower()
            if q.lower() in hay:
                hay_hits.append(a)
        for g in groups:
            if q.lower() in str(g.get("name", "")).lower():
                hay_hits += g.get("assets", [])
        seen, nodes = set(), []
        for a in hay_hits:
            if a.get("name") not in seen:
                seen.add(a.get("name"))
                nodes.append(a)
        head = f"答：按「{q}」在 {len(assets)} 个节点中找到 {len(nodes)} 个相关项："
        lines = _lines_of(nodes)
        if not nodes:
            head = (f"答：没找到与「{q}」直接相关的节点。试试问「有哪些文档？」"
                    f"「最近更新了什么？」「和耻辱墙有什么关系？」")
    if json_out:
        print(json.dumps({"topo": data.get("display"), "question": q,
                          "intent": intent, "answer": head,
                          "items": lines}, ensure_ascii=False, indent=2))
        return
    print(f"\n  🧭 拓扑问答 · {data.get('display')}")
    print(f"     问：{q}")
    print(f"     {head}")
    for ln in lines:
        print(f"         {ln}")
    print()


# ── v2.0 可验证/可审计/自响应/对外协作命令 ─────────────────────────

def _chain_display():
    """审计链展示数据 → (创世根, 链事件正序)"""
    genesis = _chain_genesis()
    rows = [ev for _raw, ev in _audit_chain_rows()
            if isinstance(ev, dict) and ev.get("seq")]
    rows.sort(key=lambda r: int(r["seq"]))
    return genesis, rows


def cmd_topo_audit_chain(keyword: str = "", limit: int = 10, json_out: bool = False):
    """lh topo audit-chain [图谱名] [--limit N] — 显示 Merkle 审计链（v2.0）
    每事件带 seq / prev_hash(指向前一条自证哈希) / hash(本条自证)·创世根=legacy 段聚合"""
    genesis, rows = _chain_display()
    rows = rows[-max(1, limit):] if limit else rows
    if json_out:
        print(json.dumps({"genesis": genesis, "chain": rows}, ensure_ascii=False, indent=2))
        return
    print(f"\n  ⛓️  Merkle 审计链 · 共 {len(_chain_display()[1])} 条链事件 · {TOPO_AUDIT_LOG}")
    print(f"     🧬 创世根(legacy 聚合) {genesis}")
    for r in rows:
        print(f"     #{int(r.get('seq')):>3} [{r.get('ts')}] {r.get('type')} {r.get('color')} ·"
              f" ←{str(r.get('prev_hash'))[:8]}… 自证 {r.get('hash')} · {str(r.get('detail'))[:52]}")
    print()


def cmd_topo_audit_verify(keyword: str = "", json_out: bool = False):
    """lh topo audit-verify [图谱名] — 验证 Merkle 审计链完整性（v2.0）
    legacy 段 → 创世根固定 · 链事件逐条: prev_hash==前条自证 且 hash==重算值 → 未篡改"""
    genesis = _chain_genesis()
    broken, checked = [], 0
    prev_self = genesis
    for _raw, ev in _audit_chain_rows():
        if not isinstance(ev, dict) or not ev.get("seq"):
            continue
        if str(ev.get("prev_hash", "")) != prev_self:
            broken.append((int(ev["seq"]), f"prev存储{str(ev.get('prev_hash'))[:8]}",
                           f"前条自证{prev_self[:8]}"))
        calc = _ev_self_hash(ev)
        if str(ev.get("hash", "")) != calc:
            broken.append((int(ev["seq"]), f"hash存储{str(ev.get('hash'))[:8]}",
                           f"重算{calc[:8]}"))
        prev_self = calc
        checked += 1
    ok = not broken
    if json_out:
        print(json.dumps({"ok": ok, "genesis": genesis, "checked": checked,
                          "broken": [{"seq": b[0], "field": b[1], "expect": b[2]}
                                     for b in broken]}, ensure_ascii=False, indent=2))
        return
    print(f"\n  🧾 审计链完整性验证 · {TOPO_AUDIT_LOG}")
    print(f"     🧬 创世根 {genesis} · 链事件 {checked} 条")
    if ok:
        print("     ✅ 链完整：逐条 prev_hash 指向前条自证哈希 · 与事件流重算一致 · 未篡改")
    else:
        print("     🔴 链断裂：")
        for b in broken:
            print(f"        seq #{b[0]} · {b[1]} ≠ {b[2]}")
    print()
    return ok


def cmd_topo_history(keyword: str = "", since: str = "", json_out: bool = False,
                     limit: int = 30):
    """lh topo history [图谱名] [--since YYYY-MM-DD] — 拓扑变更历史（v2.0）
    事件流变更类过滤（topo_change/healed/stale_warning）· 含节点级操作与链哈希"""
    kw = keyword.strip() or "对外交付"
    rows = []
    kinds = ("topo_change", "topo_healed", "topo_stale_warning")
    for _raw, ev in _audit_chain_rows():
        if not isinstance(ev, dict) or not ev.get("seq"):
            continue
        if ev.get("type") not in kinds:
            continue
        if since:
            try:
                if str(ev.get("ts", ""))[:10] < str(since).split("T")[0]:
                    continue
            except Exception:
                pass
        rows.append(ev)
    rows.reverse()
    rows = rows[:max(1, limit)]
    if json_out:
        print(json.dumps({"topo": kw, "total": len(rows), "changes": rows},
                         ensure_ascii=False, indent=2))
        return
    print(f"\n  🕓 变更历史 · {kw} · 最近 {len(rows)} 条（链 seq 反向 · {TOPO_AUDIT_LOG}）")
    op_cn = {"add": "新增", "update": "更新", "remove": "移除"}
    for r in rows:
        print(f"     #{int(r.get('seq'))} [{r.get('ts')}] {r.get('type')} {r.get('color')}"
              f" · {r.get('detail', '')}")
        for o in r.get("ops") or []:
            print(f"        {'+' if o.get('op') == 'add' else ('~' if o.get('op') == 'update' else '-')}"
                  f" {o.get('name')} · {op_cn.get(o.get('op'), o.get('op'))}"
                  f"{('/' + str(o.get('type'))) if o.get('type') else ''}")
    print()


def _snapshot_newest(keyword: str = "") -> dict:
    """最近快照 → {root_hash, path, ts}（SNAPSHOT_DIR/<topo>_*.json·文件名反向取新·v2.0）"""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for p in sorted(SNAPSHOT_DIR.glob("*.json"), key=lambda p: p.name, reverse=True):
        try:
            snap = json.loads(p.read_text(encoding="utf-8"))
            disp = str(snap.get("display") or "")
            if keyword and keyword not in disp.replace("_", ""):
                continue
            return {"root_hash": (snap.get("meta") or {}).get("root_hash"),
                    "path": p, "ts": p.stem.split("_")[-1]}
        except Exception:
            continue
    return {}


def _stale_event() -> dict:
    """最新未处理告警事件 → {} 或 {ev, hours}（severity=warning / 🟡🔴 / 移除类）"""
    rows = [ev for _raw, ev in _audit_chain_rows()
            if isinstance(ev, dict) and ev.get("seq")]
    if not rows:
        return {}
    last = rows[-1]
    sev = last.get("severity") or ("warning" if (last.get("warn") or last.get("bad"))
                                   else "info")
    removed = any(o.get("op") == "remove" for o in (last.get("ops") or []))
    if not (sev == "warning" or last.get("color") in ("🟡", "🔴") or removed):
        return {}
    try:
        hours = (datetime.now().astimezone()
                 - datetime.fromisoformat(str(last.get("ts")))).total_seconds() / 3600
    except Exception:
        hours = 0
    return {"ev": last, "hours": max(0, hours)}


def cmd_topo_heal(keyword: str = "", dry: bool = False, json_out: bool = False):
    """lh topo heal [图谱名] [--dry] — 拓扑自修复（v2.0）
    🟡 未处理告警持续 ≥24h → 耻辱墙 topo_stale_warning(当日幂等) + 快照比对：
    快照根哈希==当前 → 数据未被改动(人工核验) · ≠ → 冻结坏图→快照回滚→自动部署"""
    kw = keyword.strip() or "对外交付"
    f, data = _find_topo_file(kw)
    st = _stale_event()
    if not st:
        msg = "✅ 拓扑无未处理告警 · 无需修复"
        if json_out:
            print(json.dumps({"ok": True, "action": "none", "message": msg},
                             ensure_ascii=False, indent=2))
            return
        print(f"\n  🩺 拓扑自修复 · {data.get('display')}")
        print(f"     {msg}\n")
        return
    hours = st["hours"]
    print(f"\n  🩺 拓扑自修复 · {data.get('display')}")
    print(f"     ⚠️ 未处理告警已持续 {hours:.0f}h（阈值 {STALE_HOURS}h）"
          f" · 事件 {st['ev'].get('type')} [{st['ev'].get('ts')}]")
    if hours < STALE_HOURS:
        print(f"     🕓 距自动响应线还差 {STALE_HOURS - hours:.0f}h · 观察中（events 查看明细）\n")
        return
    today = datetime.now().astimezone().date().isoformat()
    already = any(ev.get("type") == "topo_stale_warning"
                  and str(ev.get("ts", ""))[:10] == today
                  for _raw, ev in _audit_chain_rows()
                  if isinstance(ev, dict))
    if not already and not dry:
        _shame_topo_append("topo_stale_warning",
                           f"拓扑未处理告警持续 {hours:.0f}h ≥ {STALE_HOURS}h · 自动响应启动",
                           color="🟡", warn=1, severity="warning")
        print("     🧱 已记耻辱墙 topo_stale_warning（当日幂等·不重复刷墙）")
    cur_root = topo_root_hash(data)
    snap = _snapshot_newest(kw)
    if not (snap and snap.get("root_hash")):
        print("     ⚠️ 无可用快照（export-page 自动留存 30 天）→ 需人工介入：events 查看明细")
        print()
        return True
    if snap["root_hash"] == cur_root:
        print("     ✅ 快照根哈希与当前一致 → 图谱数据未被篡改 · 需人工核验（events --limit 5）")
        print()
        return True
    if dry:
        print(f"     🧪 dry-run：快照 {snap['root_hash']} ≠ 当前 {cur_root}"
              f" → 将冻结当前图并回滚 {snap['path'].name}")
        print()
        return
    qu_dir = SNAPSHOT_DIR / "_quarantine"
    qu_dir.mkdir(parents=True, exist_ok=True)
    q_p = qu_dir / f"{kw}_preheal_{datetime.now().astimezone().strftime('%Y%m%d-%H%M%S')}.json"
    import shutil as _sh
    _sh.copy2(f, q_p)
    _sdata = json.loads(snap["path"].read_text(encoding="utf-8"))
    graph = _sdata.get("graph") if _sdata.get("__topo_snapshot__") else _sdata
    f.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"     🧊 当前图已冻结（不删除只冻结）→ {q_p}")
    print(f"     ♻️  已回滚 {snap['path'].name} → 重新同步发布…")
    ok = _topo_auto_deploy(kw)
    _shame_topo_append("topo_healed",
                       f"拓扑已从快照 {snap['root_hash']} 自动恢复 · 坏图冻结 {q_p.name}",
                       color="🟢")
    print("     ✅ 自动恢复完成 · 已记 topo_healed\n" if ok
          else "     ❌ 自动恢复部署失败 · 需人工检查（heal 再跑一次看日志）\n")
    return True


def cmd_topo_weekly_report(keyword: str = "", json_out: bool = False):
    """lh topo weekly-report [图谱名] — 每周拓扑审计报告（v2.0·周锁幂等）
    自动路径：lh health 每轮检测缺本周报告即补生成（无定时器新增·节能）· GPG 签后归档"""
    kw = keyword.strip() or "对外交付"
    f, data = _find_topo_file(kw)
    week_key = (datetime.now().astimezone().date()
                - timedelta(days=datetime.now().astimezone().weekday())).isoformat()
    out_p = TOPO_WEEKLY_DIR / f"topo-{kw}-weekly-{week_key}.md"
    if out_p.is_file():
        msg = f"本周报告已存在（幂等）· {out_p}"
        if json_out:
            print(json.dumps({"ok": True, "path": str(out_p)}, ensure_ascii=False, indent=2))
            return
        print(f"\n  📅 拓扑每周审计 · {msg}\n")
        return
    genesis, chain_rows = _chain_display()
    s = _topo_summary(data)
    recent = [ev for _raw, ev in _audit_chain_rows()
              if isinstance(ev, dict) and ev.get("seq")][-30:]
    warn_cnt = sum(1 for e in recent if e.get("severity") == "warning"
                   or e.get("color") in ("🟡", "🔴"))
    lines = ["# 🗺️ 拓扑每周审计报告 · " + str(data.get("display")), "",
             f"> 周次: {week_key} · 生成: {datetime.now().astimezone().isoformat(timespec='seconds')}",
             "> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰",
             "> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
             f"> 事件源: {TOPO_AUDIT_LOG} · append-only Merkle 链", "",
             "## 一、本图谱概览", "",
             f"- 节点 {s['nodes']}（🟢{s['green']} · 🟡{s['yellow']}）· 边 {s['edges']}",
             f"- 拓扑根哈希: `{s['root_hash']}`",
             f"- 最近同步: {s['last_sync']}",
             f"- 自动校验: {'全绿 ✅' if (s.get('verify') or {}).get('ok') else '有缺口 ⚠️'}",
             "", "## 二、近期事件流（最近 30 条）", "",
             f"链事件总数 {len(chain_rows)} · 含告警/异常 {warn_cnt} 条", ""]
    for e in reversed(recent):
        lines.append(f"- `#{int(e.get('seq'))}` [{e.get('ts')}] {e.get('type')}"
                     f" {e.get('color')} · {str(e.get('detail'))[:76]}")
    lines += ["", "## 三、完整性验证", "",
              f"- 创世根: `{genesis}`",
              "- 验证命令: `lh topo audit-verify 对外交付` · `lh topo verify 对外交付`",
              "- 公开 API: https://uid9622.cn/api/topo/对外交付（自含根哈希）", "",
              "---", "> 龍魂系统 · 对外交付拓扑 v2.0 可验证神经中枢 · CC BY-NC-SA 4.0（核心思想层）"]
    md = "\n".join(lines) + "\n"
    TOPO_WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    out_p.write_text(md, encoding="utf-8")
    gpg = ROOT / "08_BIN" / "lh_gpg_sign.py"
    if gpg.is_file():
        subprocess.run([sys.executable, str(gpg), "sign", "--force", str(out_p)],
                       capture_output=True, text=True)
    if json_out:
        print(json.dumps({"ok": True, "path": str(out_p), "root_hash": s["root_hash"]},
                         ensure_ascii=False, indent=2))
        return
    print(f"\n  📅 拓扑每周审计报告已生成 + GPG 签名\n     {out_p}\n")


def cmd_topo_serve_api(keyword: str = "", port: int = 8873, host: str = "127.0.0.1"):
    """lh topo serve-api [图谱名] [--port N] — 本地公共 API 静态服务（v2.0 可选·只读）
    服务 docs-site/topology-api/（对外交付.json / status.json / events.json）· CORS 全开 · Ctrl-C 停"""
    TOPO_API_DIR.mkdir(parents=True, exist_ok=True)

    class _ApiHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            rel = self.path.split("?", 1)[0].lstrip("/")
            rel = rel.removeprefix("api/topo/").removeprefix("api/")
            p = (TOPO_API_DIR / rel).resolve()
            if not str(p).startswith(str(TOPO_API_DIR.resolve())) or not p.is_file():
                self.send_error(404, "not found")
                return
            body = p.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_a):
            pass

    srv = ThreadingHTTPServer((host, port), _ApiHandler)
    print(f"\n  🌐 拓扑公共 API 静态服务 · http://{host}:{port}/api/topo/ · Ctrl-C 退出")
    print(f"     端点: 对外交付.json / status.json / events.json（内容自含根哈希 · 可独立验证）\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  ⏹ 已停止")


def _ask_intent(q: str) -> str:
    """自然语言 → 意图（规则有序：具体意图词优先 · 兜底 search 关键词）v1.9"""
    rules = [
        ("shame",    ("耻辱墙", "怎么联动", "什么关系", "事件", "审计", "告警", "wall")),
        ("update",   ("最近更新", "更新了什么", "什么变了", "最新变更", "最近变更", "新增了",
                      "什么变化", "最近", "动态", "recent")),
        ("edges",    ("关联边", "边有", "数据流向", "怎么连接", "连接关系", "链路", "依赖")),
        ("documents", ("有哪些文档", "什么文档", "文档列表", "列出文档", "几份文档", "有哪些文件", "documents")),
        ("articles", ("文章", "发布稿", "导读", "教程", "发布"),),
        ("issues",   ("公告", "issue", "反馈入口", "反馈", "#99")),
        ("copies",   ("平台", "扩散", "发在哪", "v2ex", "知乎", "开源中国", "oschina", "hacker", "reddit")),
        ("assets",   ("素材", "素材包", "压缩包")),
        ("types",    ("什么类型", "类型分布", "分类")),
        ("verify",   ("状态", "健康", "全绿", "校验", "绿了吗", "有没有问题", "verify")),
    ]
    for intent, kws in rules:
        if any(k in q.lower() for k in kws):
            return intent
    return "search"


def _type_dist(data: dict) -> dict:
    """节点类型分布 {type: n}（v1.8 供 summary/状态页/首页区块）"""
    out = {}
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            t = a.get("type") or "other"
            out[t] = out.get(t, 0) + 1
    return dict(sorted(out.items()))


def _public_link(a: dict) -> str:
    """节点链接对外化：http(s) 直通 · 本地 .md → 文档站公开 URL · 其余（file/zip/本地目录）= 内部资产不给链接"""
    link = (a.get("link") or "").strip()
    if not link:
        return ""
    if link.startswith(("http://", "https://")):
        return link
    if link.startswith(("file://", "obsidian://", "yuque:")):
        return ""
    p = Path(link)
    if p.suffix.lower() in (".md", ".html"):
        return f"https://uid9622.cn/docs/{p.stem}/"
    return ""


def _topo_summary(data: dict, verify_file: Path = VERIFY_DIR / "topo-docs-auto_verify.json") -> dict:
    """图谱摘要（v1.8）：节点/边/类型分布/同步/校验 · 对外展示数据源"""
    assets = [a for g in data.get("groups", []) for a in g.get("assets", [])]
    green = sum(1 for a in assets if str(a.get("status", "")).startswith("🟢"))
    yellow = sum(1 for a in assets if str(a.get("status", "")).startswith("🟡"))
    v = None
    if verify_file.is_file():
        try:
            v = json.loads(verify_file.read_text(encoding="utf-8"))
        except Exception:
            v = None
    return {
        "topo_name": data.get("topo_name"),
        "display": data.get("display"),
        "nodes": len(assets), "green": green, "yellow": yellow,
        "edges": len(data.get("edges", [])),
        "types": _type_dist(data),
        "last_sync": data.get("last_sync") or data.get("created", ""),
        "root_hash": topo_root_hash(data),   # v2.0 拓扑根哈希（外部可独立重算验证）
        "verify": {"ok": bool(v and v.get("ok")), "node_total": (v or {}).get("nodes"),
                   "gaps": len((v or {}).get("gaps") or [])} if v else None,
    }


def cmd_topo_summary(keyword: str = "", json_out: bool = False):
    """lh topo summary [图谱名] — 图谱摘要：节点/边/类型分布/同步/校验（v1.8 公开）"""
    if keyword.strip():
        _f, data = _find_topo_file(keyword)
        graphs = [data]
    else:
        graphs = []
        for f in list_topos():
            try:
                graphs.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
    if json_out:
        print(json.dumps([_topo_summary(d) for d in graphs],
                         ensure_ascii=False, indent=2))
        return
    for d in graphs:
        s = _topo_summary(d)
        tv = s["verify"]
        vtxt = f" · verify {'✅' if tv.get('ok') else '❌'}({tv.get('node_total')}节点)" if tv else ""
        print(f"\n  📢 图谱摘要 · {s['display']}")
        print(f"     节点 {s['nodes']}（🟢{s['green']} · 🟡{s['yellow']}）· 边 {s['edges']}"
              f" · 同步 {s['last_sync']}{vtxt}")
        dist = " · ".join(f"{k}×{v}" for k, v in s["types"].items()) or "—"
        print(f"     类型分布: {dist}")
    print()


def cmd_topo_search(keyword: str = "", kw: str = "", json_out: bool = False):
    """lh topo search <图谱名> <关键词> — 在节点 名称/类型/DNA/描述/标题 中搜索（v1.8）"""
    if not kw.strip():
        raise SystemExit("  ❌ 用法: lh topo search <图谱名> <关键词>   例: lh topo search 对外交付 发布")
    f, data = _find_topo_file(keyword)
    q = kw.strip().lower()
    hits = []
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            hay = " ".join(str(a.get(k, "")) for k in
                           ("name", "type", "doc_type", "dna", "title", "desc", "link")).lower()
            if q in hay:
                hits.append({"name": a.get("name"), "group": g.get("name"),
                             "type": a.get("type"), "status": a.get("status"),
                             "dna": (a.get("dna") or "")[:40],
                             "link": _public_link(a)})
    for g in data.get("groups", []):
        if q in str(g.get("name", "")).lower():
            hits.append({"group_hit": g.get("name"),
                         "note": f"命中分组（{len(g.get('assets', []))} 节点）"})
    if json_out:
        print(json.dumps({"topo": data.get("display"), "query": kw,
                          "hits": len(hits), "items": hits}, ensure_ascii=False, indent=2))
        return
    print(f"\n  🔍 拓扑搜索 · {data.get('display')} · 「{kw}」 · 命中 {len(hits)}")
    for h in hits:
        if "group_hit" in h:
            print(f"     📂 {h['group_hit']}（{h['note']}）")
            continue
        print(f"     · {h['name']}  [{h['type'] or '?'}] {h.get('status') or ''}")
        if h.get("dna"):
            print(f"        DNA {h['dna']}")
        if h.get("link"):
            print(f"        ↳ {h['link']}")
    print()


def cmd_topo_export(keyword: str, json_out: bool = False):
    """lh topo export <图谱名> [--format json] — 导出完整图谱 JSON（供外部系统调用 v1.8）"""
    f, data = _find_topo_file(keyword)
    out = {"exported_at": datetime.now().astimezone().isoformat(timespec="seconds"),
           "source_file": str(f.relative_to(ROOT)),
           "graph": data}
    print(json.dumps(out, ensure_ascii=False, indent=2 if json_out else None))


def cmd_topo_audit_log(keyword: str = "", json_out: bool = False, limit: int = 20):
    """lh topo audit-log — 拓扑变更/告警审计历史（topo_audit.jsonl 反向 N 条 v1.8）"""
    rows = []
    if TOPO_AUDIT_LOG.is_file():
        for line in TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    rows.reverse()
    rows = rows[: max(1, limit)]
    if json_out:
        print(json.dumps({"total": len(rows), "events": rows},
                         ensure_ascii=False, indent=2))
        return
    print(f"\n  🕰️  拓扑审计日志 · 最近 {len(rows)} 条 · {TOPO_AUDIT_LOG}")
    for r in rows:
        print(f"     [{r.get('ts')}] {r.get('type')} {r.get('color', '')}"
              f" · {r.get('detail', '')}")
    if not rows:
        print("     （暂无事件 · 图谱变更/校验告警将自动记录至此）")
    print()


def _summary_block_md(s: dict) -> str:
    """首页/状态页复用的摘要 html 区块（md_in_html）"""
    tv = s.get("verify") or {}
    dist = " · ".join(f"<code>{k}</code>×{v}" for k, v in (s.get("types") or {}).items()) \
        or "—"
    vtxt = (f"🟢 全绿（{tv.get('node_total')} 节点）" if tv.get("ok")
            else f"🔴 verify 缺口 {tv.get('gaps')}") if tv else "未校验"
    return f"""<div class="topo-summary" style="border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;margin:16px 0;background:linear-gradient(180deg,#f8fafc,#ffffff)">
<table style="width:100%;border-collapse:collapse">
<tr><td style="padding:6px 12px;width:110px;white-space:nowrap;color:#64748b">🧮 节点总数</td><td style="padding:6px 12px"><strong>{s['nodes']}</strong> · 🟢{s['green']} · 🟡{s['yellow']}</td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">🔗 关联边</td><td style="padding:6px 12px"><strong>{s['edges']}</strong></td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">🏷️ 类型分布</td><td style="padding:6px 12px">{dist}</td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">⏱️ 最后同步</td><td style="padding:6px 12px"><code>{s['last_sync']}</code></td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">✅ 自动校验</td><td style="padding:6px 12px">{vtxt}</td></tr>
</table>
<p style="margin:8px 0 0">📈 <a href="topology/">查看完整拓扑 → /docs/topology/</a> · 💻 <code>lh topo summary 对外交付 --json</code></p>
</div>"""


def _node_row_md(a: dict, group: str = "") -> str:
    link = _public_link(a)
    nm = a.get("name", "?")
    dna = a.get("dna") or ""
    dna_s = (dna[:30] + "…") if len(dna) > 30 else (dna or "（待补DNA）")
    cell = f"**{nm}**" if not link or link.startswith("⚠️") or "内部" in link \
        else f"[**{nm}**]({link})"
    extra = ""
    if a.get("doc_type"):
        extra = f" · {a['doc_type']}"
    elif a.get("type"):
        extra = f" · {a['type']}"
    return f"| {cell} | <code>{dna_s}</code> | {a.get('status', '')}{extra} |"


def _root_decl_md(data: dict, s: dict, root_h: str, now: str) -> list:
    """根哈希公开声明页内容行（v2.1 · ROOT_HASH_DECLARATION.md · 方向三）"""
    tv = s.get("verify") or {}
    vtxt = f"🟢 全绿 · {tv.get('node_total', s.get('nodes'))} 节点" if tv.get("ok") \
        else "🔴 verify 有缺口"
    return [
        "---",
        "# 📜 龙魂系统 · 对外交付拓扑 根哈希公开声明",
        "# DNA: #龍芯⚡️2026-09-05-ROOT-HASH-DECLARATION-v1.0-UID9622",
        "# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "---",
        "",
        "# 📜 根哈希公开声明（Root Hash Declaration）",
        "",
        f"> 本声明公开锚定「{data.get('display') or data.get('topo_name')}」拓扑根哈希，任何人可独立重算验证。",
        "> 根哈希 = 全部节点 `name|dna` 行按序聚合 → SHA-256 前 16 位。数据一改，哈希必变。",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| 图谱 | {data.get('topo_name')} · {data.get('display')} |",
        f"| **根哈希** | `{root_h}` |",
        f"| 声明时间 | {now} |",
        f"| 节点总数 | {s.get('nodes')}（🟢 {s.get('green')} · 🟡 {s.get('yellow')}） |",
        f"| 关联边 | {s.get('edges')} |",
        f"| 自动校验 | {vtxt} |",
        "| 验证① | 本机重算: `lh topo audit-verify 对外交付` |",
        "| 验证② | 在线比对: `GET https://uid9622.cn/api/topo/status.json` 的 `root_hash` |",
        "| 验证③ | 快照比对: `GET https://uid9622.cn/docs/topology/archive/` 最新快照 |",
        "| 验证④ | 签名核验: `gpg --verify ROOT_HASH_DECLARATION.md.asc ROOT_HASH_DECLARATION.md` |",
        "| 审计链 | [⛓ Merkle 审计链](audit/) · [📦 归档快照](archive/) |",
        f"| 数据源 | `docs/topology/{data.get('topo_name')}_legion_topo.json` |",
        "| 归属名 | 诸葛鑫 \\| UID9622 · 龍芯北辰 |",
        "| GPG | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |",
        "| 协议 | CC BY-NC-SA 4.0（核心思想层） · MulanPSL v2（数据/工程层） |",
        "",
        "> 📌 声明=**可独立重算的事实锚点**：保证「此刻数据即此哈希；此后任何改动必异哈希」。",
        "> 声明不替代审计结论，一切以根哈希比对为准。欢迎任何人独立复核并提交纠错反馈。",
        "",
        f"> 🐛 发现与声明不符？[提交拓扑反馈]({ISSUE_NEW_URL})",
    ]


def cmd_topo_feedback(keyword: str = "对外交付"):
    """lh topo feedback 对外交付 — 拓扑问题反馈清单（v2.1·耻辱墙反馈闭环）
    数据源1: GitHub issues（labels=topo-feedback · open/closed）
    数据源2: 耻辱墙事件链 topo_audit.jsonl / shame_wall.json（type=topo-feedback）
    新 open 反馈自动去重写入耻辱墙（append-only 链 · seq/prev_hash 自证）
    输出: 时间倒序 Markdown 表格"""
    _ua = {"User-Agent": "longhun-topo/2.1"}
    gh_rows = []
    gh_err = ""
    try:
        _url = (f"{GH_API_BASE}/issues?labels={TOPO_FEEDBACK_LABEL}"
                "&state=all&sort=created&direction=desc&per_page=100")
        _req = urllib.request.Request(_url, headers=_ua)
        with _OPENER.open(_req, timeout=20) as _r:
            _body = json.loads(_r.read().decode("utf-8"))
        for _it in (_body or []):
            gh_rows.append({
                "title": str(_it.get("title", "?")),
                "url": str(_it.get("html_url", "")),
                "state": str(_it.get("state", "open")),
                "created": str(_it.get("created_at", "")).replace("T", " ")[:19],
            })
    except Exception as _e:   # noqa: BLE001 网络失败不阻断（本地耻辱墙仍可查）
        gh_err = f"（GitHub 拉取失败: {_e}）"
    # ── 本地耻辱墙 topo-feedback（事件链 append-only）──
    local = {}
    if TOPO_AUDIT_LOG.is_file():
        for _line in TOPO_AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line:
                continue
            try:
                _ev = json.loads(_line)
            except Exception:
                continue
            if _ev.get("type") != TOPO_FEEDBACK_LABEL:
                continue
            _d = str(_ev.get("detail", ""))
            _title = _d.split(" · ")[0] if _d else f"seq{_ev.get('seq')}"
            _url = _d.split(" · ")[1] if " · " in _d else ""
            local[_d or _title] = {
                "title": _title, "url": _url,
                "state": "open" if _ev.get("color") in ("🟡", "🔴") else "closed",
                "created": str(_ev.get("ts", "")).replace("T", " ")[:19],
            }
    # ── 新 open 反馈自动写入耻辱墙链（去重·幂等）──
    _known = set(local.keys())
    _new = 0
    for _r in gh_rows:
        _key = f"{_r['title']} · {_r['url']}"
        if _key in _known:
            continue
        if _r.get("state") == "open":
            _shame_topo_append(TOPO_FEEDBACK_LABEL,
                               f"{_r['title']} · {_r['url']} · {_r['created']} · open",
                               color="🟡", severity="info")
            local[_key] = {"title": _r["title"], "url": _r["url"],
                           "state": "open", "created": _r["created"]}
            _new += 1
    # ── 合并去重输出（url 优先键）──
    merged = {}
    for _v in list(local.values()) + gh_rows:
        merged.setdefault(_v.get("url") or _v["title"], _v)
    rows = sorted(merged.values(), key=lambda x: x.get("created", ""), reverse=True)
    print(f"\n  🐛 拓扑反馈清单 · topo-feedback · 共 {len(rows)} 条{gh_err}")
    if _new:
        print(f"     ↳ 新 {_new} 条 open 反馈已入耻辱墙链（topo_audit.jsonl · append-only）")
    if not rows:
        print("     📭 暂无反馈（即拓扑无投诉记录）")
        return 0
    print()
    print("| # | 时间 | 状态 | 标题 | 链接 |")
    print("|:---|:---|:---|:---|:---|")
    for _i, _r in enumerate(rows, 1):
        _s = "🟡 open" if _r.get("state") == "open" else "🟢 closed"
        _t = str(_r.get("title", "?")).replace("|", "\\|")[:60]
        print(f"| {_i} | {_r.get('created', '')} | {_s} | {_t} | {_r.get('url', '')} |")
    print()
    return 0


def cmd_topo_archive(keyword: str = "对外交付"):
    """lh topo archive 对外交付 — 归档可验证快照（v2.1·方向三）
    产出: ~/.longhun/topo_archive_YYYYMMDD.json（完整拓扑 JSON + 审计链 + 根哈希 + 时间戳）
      + 站点副本 docs-site/docs/topology/archive/（mkdocs build 后 /docs/topology/archive/）
      + 列表页 archive/index.md · 自动 GPG 签名 · mkdocs build + rsync 上线（_topo_auto_deploy）"""
    f, data = _find_topo_file(keyword)
    s = _topo_summary(data)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    root_h = s.get("root_hash") or topo_root_hash(data)
    tv = s.get("verify") or {}
    _genesis, _chain = "", []
    try:
        _g, _chain = _chain_display()
        _genesis = _g
    except Exception:   # noqa: BLE001
        pass
    snap = {"__topo_archive__": True, "api": "topo/archive-v2.1",
            "topo_name": data.get("topo_name"), "display": data.get("display"),
            "root_hash": root_h, "generated_at": now,
            "nodes": s.get("nodes"), "edges": s.get("edges"),
            "green": s.get("green"), "yellow": s.get("yellow"),
            "verify_ok": bool(tv.get("ok")), "genesis": _genesis,
            "audit_chain": _chain, "graph": data,
            "by": "诸葛鑫 | UID9622 · 龍芯北辰"}
    _fname = f"topo_archive_{datetime.now().astimezone():%Y%m%d}.json"
    home_p = STATE_DIR / _fname
    TOPO_SITE_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    site_p = TOPO_SITE_ARCHIVE_DIR / _fname
    home_p.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    site_p.write_text(home_p.read_text(encoding="utf-8"), encoding="utf-8")
    # ── 列表页 archive/index.md 刷新 ──
    _files = sorted(TOPO_SITE_ARCHIVE_DIR.glob("topo_archive_*.json"), reverse=True)
    _lines = ["# 📦 拓扑归档快照", "",
              f"> 图谱: {data.get('display')} · 当前根哈希 `{root_h}` · 每份快照含完整拓扑 JSON + 审计链",
              f"> 生成: {now} · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG 分离签名（.asc 同目录）",
              "", f"共 {len(_files)} 份归档 · 快照为不可变时间点（内容哈希即文件本身 · 可独立重算）", "",
              "| 快照 | 大小 | 根哈希 | 校验 |",
              "|:---|:---|:---|:---|"]
    for _pf in _files:
        try:
            _d = json.loads(_pf.read_text(encoding="utf-8"))
            _rh = str(_d.get("root_hash", root_h))
            _sz = f"{_pf.stat().st_size // 1024} KB"
            _ok = "✅" if _d.get("verify_ok") else "❌"
        except Exception:
            _rh, _sz, _ok = root_h, "?", "?"
        _lines.append(f"| [{_pf.name}]({_pf.name}) | {_sz} | `{_rh}` | {_ok} |")
    if _files:
        _lines += ["", f"> 校验: `gpg --verify {_files[0].name}.asc {_files[0].name}`（最新） · "
                        f"`lh topo audit-verify {data.get('topo_name') or '对外交付'}`", ""]
    idx_p = TOPO_SITE_ARCHIVE_DIR / "index.md"
    idx_p.write_text("\n".join(_lines) + "\n", encoding="utf-8")
    # ── GPG 签名（本地快照 + 站点副本 + 列表页 · 失败不阻断）──
    for _p in (home_p, site_p, idx_p):
        try:
            subprocess.run([sys.executable, str(GPG_SIGN_BIN), "sign", str(_p)],
                           capture_output=True, text=True, timeout=120)
        except Exception:   # noqa: BLE001
            pass
    # ── 自动上线（export-page 刷新声明 + mkdocs build + rsync 鲲鹏）──
    _topo_auto_deploy(data.get("topo_name") or keyword)
    print(f"\n  📦 拓扑归档快照已生成 · {_fname}")
    print(f"     本地: {home_p}")
    print(f"     站点: {TOPO_SITE_ARCHIVE_DIR.relative_to(ROOT)}/{_fname}（→ /docs/topology/archive/）")
    print(f"     根哈希: {root_h} · 审计链 {len(_chain)} 条 · 节点 {s.get('nodes')} · GPG 已签")
    print(f"     列表页: {idx_p.relative_to(ROOT)}")
    return 0


def cmd_topo_export_page(keyword: str = "", json_out: bool = False):
    """lh topo export-page <图谱名> — 生成拓扑公开状态页（v1.8）
    本地 docs/topology/对外交付状态页.md + 文档站源 docs-site/docs/topology/index.md
    + summary.json（首页区块数据源）· 随后 mkdocs build + rsync 上线"""
    f, data = _find_topo_file(keyword)
    s = _topo_summary(data)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    root_h = s.get("root_hash") or topo_root_hash(data)  # v2.1 前移：声明/快照共用

    def _group_md(grp_name: str, assets: list) -> str:
        if not assets:
            return ""
        head = "📂 " + grp_name
        lines = [f"### {head}", "", "| 节点 | DNA | 状态 |", "|:---|:---|:---|"]
        for a in sorted(assets, key=lambda x: x.get("name", "")):
            lines.append(_node_row_md(a))
        return "\n".join(lines) + "\n"

    body = []
    for g in data.get("groups", []):
        body.append(_group_md(g.get("name", ""), g.get("assets", [])))
    edges = []
    name_map = {}
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            name_map[a.get("name")] = a
    for e in data.get("edges", []):
        src, tgt = name_map.get(e.get("source")), name_map.get(e.get("target"))
        sl, tl = _public_link(src) if src else "", _public_link(tgt) if tgt else ""
        s_txt = f"[{e.get('source')}]({sl})" if sl else str(e.get("source"))
        t_txt = f"[{e.get('target')}]({tl})" if tl else str(e.get("target"))
        edges.append(f"| {e.get('source')} → {e.get('target')} | {s_txt} → {t_txt}"
                     f" | {e.get('type')} | {e.get('label') or '—'} |")
    edge_md = "| 边 | 端点 | 类型 | 说明 |\n|:---|:---|:---|:---|\n" + "\n".join(edges) if edges \
        else "（无边）"

    tv = s.get("verify") or {}
    vcell = f"🟢 全绿 · {tv['node_total']} 节点" if tv.get("ok") \
        else f"🔴 verify 缺口 {tv.get('gaps')} 条"
    evs = _topo_events_rows(3)
    last_change = evs[0].get("ts") if evs else (data.get("last_sync") or "")
    # ── v2.2 拓扑变更可视化：页首直展最近 3 次变更（用户打开即知变化）──
    _op_cn = {"add": "➕ 新增", "update": "✏️ 更新", "remove": "➖ 移除"}
    _type_cn = {"topo-change": "🔄 变更", "topo_change": "🔄 变更",
                "topo-feedback": "🐛 反馈", "topo-sync": "🕓 同步",
                "verify": "🧾 校验", "shame": "📛 耻辱", "topo-verify": "🧾 校验"}
    _chg = ["### 🕐 最近 3 次变更", ""]
    if evs:
        _chg += ["| 时间 | 动作 | 内容 |", "|:---|:---|:---|"]
        for _r in evs:
            _ops = _r.get("ops") or []
            _act = _op_cn.get(_ops[0].get("op")) if (_ops and _ops[0].get("op")) \
                else _type_cn.get(str(_r.get("type", "")), str(_r.get("type", "事件")))
            _det = str(_r.get("detail", "")).replace("|", "\\|")
            if len(_det) > 90:
                _det = _det[:87] + "…"
            _ts = (str(_r.get("ts", "")).replace("T", " "))[5:16]
            _chg.append(f"| {_ts} | {_act} | {_det} |")
    else:
        _chg += ["（暂无记录 · 拓扑变更将自动留痕于此）"]
    change_md = "\n".join(_chg)
    meta_bar = (
        f'<div id="topo-verify-bar" style="margin:14px 0;padding:10px 14px;'
        f'border:1px solid #d8c9a3;border-radius:8px;background:#faf6ea;'
        f'font-size:.95rem;line-height:1.7">'
        f'🔐 拓扑根哈希 <code>{s.get("root_hash", "")}</code>'
        f' · 更新 {last_change}'
        f' · <a href="audit/">⛓ 审计链</a>'
        f' · <a href="{ISSUE_NEW_URL}" target="_blank" rel="noopener">发现拓扑问题？提交反馈</a>'
        f'<span id="topo-live-updated" style="display:none;color:#b45309;font-weight:700">'
        f' · 🔄 拓扑已更新，请刷新页面</span></div>')
    page = f"""---
# 🕸️ 龙魂系统 · 对外交付图谱
# DNA: #龍芯⚡️2026-09-05-TOPO-PUBLIC-PAGE-V2.0-UID9622
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
---

# 🕸️ 龙魂系统 · 对外交付图谱

> 龙魂系统对外交付产物拓扑总览。节点即交付物：文档/文章/素材/反馈/Issue——全部可溯源（DNA）、
> 可跳转（链接）、可审计（校验全绿）、可验证（根哈希+审计链）。本页由
> `lh topo export-page 对外交付` 自动生成 · v2.0 可验证神经中枢。

{_summary_block_md(s)}

{meta_bar}

{change_md}

## 📚 节点明细（{s['nodes']}）

{chr(10).join(b for b in body if b.strip())}

## 🔗 关联边（{s['edges']}）

{edge_md}

## 🔐 可验证声明

| 项 | 值 |
|---|---|
| 归属名 | 诸葛鑫 \\| UID9622 · 龙芯北辰 |
| GPG 指纹 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| **反馈** | [发现拓扑问题？提交反馈]({ISSUE_NEW_URL}) — 耻辱墙模板 · 预填 `topo-feedback` · 自动入耻辱墙 |
| 验证命令 | `gpg --verify <file>.asc <file>` |
| **拓扑根哈希** | `{s.get('root_hash', '')}`（聚合 name\\|dna 行 → SHA-256 前 16 · 可独立重算） |
| **外部独立验证** | 本机 `lh topo audit-verify 对外交付` · 在线 `GET {API_BASE}status.json` · 快照 `GET {API_BASE}archive/<快照>.json` |
| **最近变更** | {last_change} |
| **审计链** | [⛓ 查看 Merkle 审计链](audit/)（创世根+逐条 prev_hash 自证） |
| **归档快照** | [📦 历史归档](archive/)（完整拓扑 JSON + 审计链 · GPG 签名 · 变更时快照） |
| **根哈希声明** | [📜 根哈希公开声明](ROOT_HASH_DECLARATION/)（声明时间+验证方法 · GPG 签名） |
| 图谱名 | {data.get('topo_name')} · {data.get('display')} |
| 数据源 | `docs/topology/{f.name}` |
| 生成时间 | {now} |
| 自动校验 | {vcell} |

> 外部查询：`lh topo summary/search/export/audit-log/ask/events/audit-chain/history/heal 对外交付`（本机） ·
> 在线 JSON：`summary.json`（本页同目录）· 交互数据：`data.json` · 公共 API：`{API_BASE}对外交付`
{_TOPO_LIVE_HTML}"""

    # 落盘 1: 本地缓存层产物
    out_local = TOPO_DIR / TOPO_PUBLIC_PAGE
    out_local.write_text(page, encoding="utf-8")
    # 落盘 2: 文档站源（mkdocs docs_dir/topology/index.md）
    SITE_TOPO_DIR.mkdir(parents=True, exist_ok=True)
    site_idx = SITE_TOPO_DIR / "index.md"
    site_idx.write_text(page, encoding="utf-8")
    # ── v2.1 落盘 2b: 根哈希公开声明（方向三 · ROOT_HASH_DECLARATION.md · GPG 收尾统一签）──
    TOPO_ROOT_DECL.write_text("\n".join(_root_decl_md(data, s, root_h, now)) + "\n",
                              encoding="utf-8")
    # 落盘 3: 摘要 JSON（首页区块/外部接口数据源）
    (SITE_TOPO_DIR / "summary.json").write_text(
        json.dumps({"updated_at": now, "page": "https://uid9622.cn/docs/topology/",
                    **s}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 落盘 4: 交互检索数据 data.json（v2.0: 完整 DNA + 根哈希·供页面自证 + JS 轮询对比）
    live_nodes, lname = [], {}
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            lname[a.get("name")] = a
            live_nodes.append({
                "name": a.get("name"), "group": g.get("name"), "type": a.get("type"),
                "doc_type": a.get("doc_type", ""), "title": a.get("title", ""),
                "status": str(a.get("status", "")).split("·")[0].strip(),
                "dna": a.get("dna") or "", "link": _public_link(a),
                "desc": (a.get("desc") or "")[:140]})
    live_edges = []
    for _e in data.get("edges", []):
        _s, _t = lname.get(_e.get("source")), lname.get(_e.get("target"))
        live_edges.append({"source": _e.get("source"), "target": _e.get("target"),
                           "type": _e.get("type"), "label": _e.get("label") or "",
                           "src_link": _public_link(_s) if isinstance(_s, dict) else "",
                           "tgt_link": _public_link(_t) if isinstance(_t, dict) else ""})
    (SITE_TOPO_DIR / "data.json").write_text(
        json.dumps({"updated_at": now, "root_hash": root_h,
                    "topo": data.get("display"),
                    "verify": tv, "nodes": live_nodes, "edges": live_edges},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 落盘 5: 交互检索前端 topo_live.js（内容不变则跳过写·保 asc 签名有效）
    _js_p = SITE_TOPO_DIR / "topo_live.js"
    if not _js_p.exists() or _js_p.read_text(encoding="utf-8") != _TOPO_LIVE_JS:
        _js_p.write_text(_TOPO_LIVE_JS, encoding="utf-8")

    # ── v2.0 落盘 6: 公共 API 静态 JSON（docs-site/topology-api/ · rsync 鲲鹏 + nginx alias /api/topo/）──
    TOPO_API_DIR.mkdir(parents=True, exist_ok=True)
    api_meta = {"api": "topo/v2.0", "topo_name": data.get("topo_name"),
                "display": data.get("display"), "updated_at": now,
                "root_hash": root_h, "last_sync": s["last_sync"],
                "verify": tv, "page": "https://uid9622.cn/docs/topology/",
                "verify_cmd": "lh topo audit-verify 对外交付"}
    full_payload = {**api_meta, "nodes": live_nodes, "edges": live_edges}
    (TOPO_API_DIR / f"{data.get('topo_name')}.json").write_text(
        json.dumps(full_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    status_payload = {**api_meta, "nodes_count": s["nodes"], "green": s["green"],
                      "yellow": s["yellow"], "edges_count": s["edges"],
                      "types": s["types"]}
    (TOPO_API_DIR / "status.json").write_text(
        json.dumps(status_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        genesis = _chain_genesis()
    except Exception:
        genesis = ""
    (TOPO_API_DIR / "events.json").write_text(
        json.dumps({"api": "topo/v2.0", "updated_at": now, "genesis": genesis,
                    "events": _topo_events_rows(30)},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ── v2.0 落盘 7: 时间戳快照（自愈恢复源 · 保留 30 天）──
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    _snap_p = SNAPSHOT_DIR / f"{data.get('topo_name')}_{now[:19].replace(':', '').replace('-', '').replace('T', '-')}.json"
    (_snap_p.write_text(json.dumps(
        {"__topo_snapshot__": True,
         "meta": {"root_hash": root_h, "updated_at": now, "verify_ok": bool(tv.get("ok"))},
         "display": data.get("display"), "topo_name": data.get("topo_name"),
         "graph": data}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"))
    # prune: 30 天前快照（保留 _quarantine 冻结区不动）
    _cutoff = (datetime.now().astimezone() - timedelta(days=SNAPSHOT_KEEP_DAYS)).timestamp()
    for _p in SNAPSHOT_DIR.glob("*.json"):
        if "_quarantine" in str(_p) or "_preheal" in _p.name:
            continue
        try:
            if _p.stat().st_mtime < _cutoff:
                _p.unlink()
        except Exception:
            pass

    # ── v2.0 落盘 8: Merkle 审计链页（docs-site/docs/topology/audit/index.md → /docs/topology/audit/）──
    _genesis, _chain = _chain_display()
    _aud_rows = list(reversed(_chain))[:20]
    _al = ["# ⛓️ 拓扑 Merkle 审计链",
           "",
           f"> 图谱: {data.get('display')} · 链: append-only · 每事件带 seq + prev_hash(指向前条自证) + hash(本条自证)",
           f"> 生成: {now} · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰",
           "",
           f"- 🧬 创世根（legacy 事件段聚合哈希）: `{_genesis}`",
           f"- 链事件总数: {len(_chain)}",
           f"- 当前拓扑根哈希: `{root_h}`",
           "",
           "## 最近 20 条链事件",
           "",
           "| # | 时间 | 类型 | 自证哈希 | 上一链 | 事件 |",
           "|:---|:---|:---|:---|:---|:---|"]
    for _r in _aud_rows:
        _al.append(f"| {int(_r.get('seq'))} | {_r.get('ts')} | {_r.get('type')} | "
                   f"`{_r.get('hash')}` | `{str(_r.get('prev_hash'))[:8]}…` | "
                   f"{str(_r.get('detail'))[:60]} |")
    _al += ["", "## 验证", "",
            "本机：`lh topo audit-verify 对外交付`（逐条重算比对 → 未篡改 ✅） · "
            "`lh topo audit-chain 对外交付 --limit 10`",
            "",
            f"反馈: [🐛 耻辱墙模板]({ISSUE_NEW_URL}) · 公共 API: `{API_BASE}events.json`",
            "",
            "> 龍魂系统 · 对外交付拓扑 v2.0 可验证神经中枢 · CC BY-NC-SA 4.0（核心思想层）"]
    _aud_dir = SITE_TOPO_DIR / "audit"
    _aud_dir.mkdir(parents=True, exist_ok=True)
    (_aud_dir / "index.md").write_text("\n".join(_al) + "\n", encoding="utf-8")
    # 首页拓扑区块自动刷新（<!-- TOPO-SUMMARY --> 锚点）
    home = SITE_DOC_DIR / "index.md"
    if home.is_file():
        text = home.read_text(encoding="utf-8")
        block = "<!-- TOPO-SUMMARY -->\n\n" + _summary_block_md(s) + \
                "\n\n<!-- /TOPO-SUMMARY -->"
        if "<!-- TOPO-SUMMARY -->" in text:
            text = re.sub(r"<!-- TOPO-SUMMARY -->.*?<!-- /TOPO-SUMMARY -->",
                          block, text, flags=re.S)
        elif "## 🗺️ 拓扑状态" in text:
            text = re.sub(r"(## 🗺️ 拓扑状态).*?(?=^## |\Z)",
                          r"\1\n\n" + block + "\n", text, flags=re.S | re.M)
        else:
            text += "\n## 🗺️ 拓扑状态\n\n" + block + "\n"
        home.write_text(text, encoding="utf-8")

    if json_out:
        print(json.dumps({"ok": True, "topo": s["display"], "nodes": s["nodes"],
                          "local": str(out_local), "site": str(site_idx),
                          "summary": str(SITE_TOPO_DIR / "summary.json"),
                          "live_data": str(SITE_TOPO_DIR / "data.json")},
                         ensure_ascii=False, indent=2))
        return
    print(f"\n  🖨️  拓扑状态页已生成 · {s['display']}")
    print(f"     节点 {s['nodes']} · 边 {s['edges']} · 同步 {s['last_sync']}")
    print(f"     本地产物 {out_local.relative_to(ROOT)}")
    print(f"     文档站源 {site_idx.relative_to(ROOT)}")
    print(f"     摘要 JSON  {SITE_TOPO_DIR / 'summary.json'}")
    print(f"     交互数据    {SITE_TOPO_DIR / 'data.json'}（页面 🔍 图谱检索实时读取）")
    print("     上线: cd docs-site && mkdocs build -f mkdocs.yml && rsync -az site/ 鲲鹏:/opt/longhun-system/docs-site/")
    print()


def cmd_edge_add(keyword: str, source: str = "", target: str = "", etype: str = "relates_to",
                 label: str = "", desc: str = ""):
    """lh topo edge <图谱名> --source <源> --target <目标> [--type relates_to] [--label …]
    边存 data['edges']（source→target→type 去重更新）；两端节点须已注册（group 资产或子图谱）v1.6"""
    if not keyword.strip() or not source.strip() or not target.strip():
        raise SystemExit("  ❌ 用法: lh topo edge <图谱名> --source <源节点> --target <目标节点> [--type relates_to]")
    f, data = _find_topo_file(keyword)
    names = set()
    for g in data.get("groups", []):
        names |= {a.get("name", "") for a in g.get("assets", [])}
    names |= {sg.get("name", "") for sg in data.get("subgraphs", [])}
    if source.strip() not in names:
        raise SystemExit(f"  ❌ 源节点「{source.strip()}」未注册（先 lh topo node … 或 lh topo list <图谱名> 核对名称）")
    if target.strip() not in names:
        raise SystemExit(f"  ❌ 目标节点「{target.strip()}」未注册（先注册或核对名称）")
    edges = data.setdefault("edges", [])
    edge = {"source": source.strip(), "target": target.strip(),
            "type": etype.strip() or "relates_to",
            "registered_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    if label.strip():
        edge["label"] = label.strip()
    if desc.strip():
        edge["desc"] = desc.strip()
    updated = False
    for i, e in enumerate(edges):
        if (e.get("source"), e.get("target"), e.get("type")) == (edge["source"], edge["target"], edge["type"]):
            edge["registered_at"] = e.get("registered_at", edge["registered_at"])
            if not edge.get("label") and e.get("label"):
                edge["label"] = e.get("label")
            if not edge.get("desc") and e.get("desc"):
                edge["desc"] = e.get("desc")
            edges[i] = edge
            updated = True
            break
    if updated:
        print(f"  🔄 边已更新 · {edge['source']} → {edge['target']} [{edge['type']}]")
    else:
        edges.append(edge)
        print(f"  ✅ 边已注册 · {edge['source']} → {edge['target']} [{edge['type']}]")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"     图谱 {data.get('display')} · 边 {len(edges)} 条")


def cmd_topo_status(keyword: str = ""):
    """lh topo status <图谱名> — 图谱状态速览(Markdown 表格·节点/边/更新时间/最新节点) v1.6"""
    if not keyword.strip():
        raise SystemExit("  ❌ 用法: lh topo status <图谱名>  （别名: lh topo <图谱名> status）")
    f, data = _find_topo_file(keyword)
    nodes = list(iter_nodes(data))
    n = len(nodes)
    green, yellow, _neutral = asset_stats(data)
    subs = len(data.get("subgraphs", []))
    edges = data.get("edges", [])
    newest_at, newest_name = "", ""
    for _g, asset in nodes:
        ra = asset.get("registered_at", "")
        if ra and ra > newest_at:
            newest_at, newest_name = ra, asset.get("name", "")
    for sg in data.get("subgraphs", []):
        ra = sg.get("registered_at", "")
        if ra and ra > newest_at:
            newest_at, newest_name = ra, sg.get("name", "")
    tcount = {}
    for _g, asset in nodes:
        t = asset.get("type") or "other"
        tcount[t] = tcount.get(t, 0) + 1
    tdist = " · ".join(f"{k}×{v}" for k, v in sorted(tcount.items())) or "—"
    print(f"\n  📢 图谱状态 · {data.get('display')}  ({f.relative_to(ROOT)})")
    print("  | 项目 | 值 |")
    print("  |:---|:---|")
    print(f"  | 图谱名 | {data.get('topo_name')} |")
    print(f"  | 节点总数 | {n}（🟢{green} · 🟡{yellow}）|")
    print(f"  | 类型分布 | {tdist} |")
    print(f"  | 子图谱 | {subs} |")
    print(f"  | 关联边 | {len(edges)} |")
    print(f"  | 最后同步 | {data.get('last_sync') or data.get('created')} |")
    print(f"  | 🔐 根哈希 | {topo_root_hash(data)}（聚合 name|dna 行 · 可独立重算） |")
    print(f"  | 最新节点 | {newest_name or '—'} · {newest_at or '—'} |")
    print("  🔐 完整性验证: lh topo audit-verify 对外交付（Merkle 链） ·"
          " lh topo history 对外交付 --since 2026-09-01（变更历史）")
    print()


# ─────────────────────────── verify ───────────────────────────

def cmd_subgraph_register(keyword: str, name: str = "", db_id: str = "",
                          dna: str = "", status: str = "🟢 已注册", link: str = "",
                          meta: str = "", ntype: str = "notion-db"):
    """lh topo subgraph <图谱名> --name <库名> --db-id <notion数据库ID> [--dna …] [--status …]
    [--link …] [--meta '{json}'] [--type …] — 注册关联库为子图谱节点(v1.5·任务①)
    meta JSON 承载库元数据: database_id/row_count/created/edited/parent/title。同名=更新。"""
    if not keyword.strip() or not name.strip():
        raise SystemExit("  ❌ 用法: lh topo subgraph <图谱名> --name <库名> --db-id <id> [--meta '{json}']")
    f, data = _find_topo_file(keyword)
    subgraphs = data.setdefault("subgraphs", [])
    meta_dict = {}
    if meta.strip():
        try:
            meta_dict = json.loads(meta)
        except Exception:
            raise SystemExit("  ❌ --meta 需合法 JSON 字符串(如 '{\"row_count\": 38}')") from None
    if db_id.strip():
        meta_dict["database_id"] = db_id.strip()
    if not meta_dict.get("title"):
        meta_dict["title"] = name.strip()
    node = {"name": name.strip(), "type": ntype.strip() or "notion-db",
            "dna": dna.strip(), "status": status.strip() or "🟢 已注册",
            "link": link.strip(), "subgraph_meta": meta_dict,
            "registered_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    updated = False
    for i, sg in enumerate(subgraphs):
        if sg.get("name") == name.strip():
            node["registered_at"] = sg.get("registered_at", node["registered_at"])
            subgraphs[i] = node
            updated = True
            break
    if updated:
        print(f"  🔄 子图谱「{name.strip()}」已更新 · 图谱 {data.get('display')}")
    else:
        subgraphs.append(node)
        print(f"  ✅ 子图谱「{name.strip()}」注册 · 图谱 {data.get('display')}")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    green, yellow, neutral = asset_stats(data)
    print(f"     节点 {green+yellow+neutral}（组资产 + 子图谱 {len(subgraphs)}）"
          f" · 🟢{green} 🟡{yellow}")
    if meta_dict:
        print(f"     库元数据: row_count={meta_dict.get('row_count', '?')} · "
              f"database_id={meta_dict.get('database_id', '?')}")


# ─────────────────────────── obsidian 镜像 scan/sync（v1.5·2026-09-03·任务②）───────────────────────────

OBSIDIAN_DEFAULT_DIR = "~/Obsidian/龍魂系統"
OBSIDIAN_SKIP = {".git", "__pycache__", ".github", "node_modules", ".venv", ".trash"}


def _find_obsidian_vault(dir_arg: str):
    p = Path(os.path.expanduser(dir_arg.strip() or OBSIDIAN_DEFAULT_DIR))
    if not p.is_dir():
        raise SystemExit(f"  ❌ Obsidian 库目录无效: {p}（可 --dir 指定）")
    return p


def _scan_obsidian_notes(vault: Path, keyword: str = "通心译", include_chats: bool = False):
    """扫描 vault 中与关键词相关的 .md 笔记（排除代码/缓存目录·EditorChats 默认跳过）
    命中:相对路径含关键词 或 首 6000 字符内容含关键词"""
    hits = []
    for f in sorted(vault.rglob("*.md")):
        rel = f.relative_to(vault)
        if any(part.startswith(".") or part in OBSIDIAN_SKIP for part in rel.parts):
            continue
        if not include_chats and "EditorChats" in str(rel):
            continue
        head = ""
        with contextlib.suppress(Exception):
            head = f.read_text(encoding="utf-8", errors="ignore")[:6000]
        if keyword not in str(rel) and keyword not in head:
            continue
        dna = ""
        with contextlib.suppress(Exception):
            dna = _extract_dna(f.read_text(encoding="utf-8", errors="ignore")[:5000])
        hits.append({"name": f.stem, "type": "note", "id": f"obsidian:{rel}",
                     "dna": dna, "status": "🟢 活跃" if dna else "🟡 无DNA",
                     "link": f"file://{f.resolve()}", "rel": str(rel)})
    return hits


def cmd_obsidian_scan(dir_arg: str = "", keyword: str = "通心译", include_chats: bool = False):
    """lh topo obsidian scan [--dir <vault>] [--keyword 词] [--chats] — 扫描预览不落盘"""
    vault = _find_obsidian_vault(dir_arg)
    hits = _scan_obsidian_notes(vault, keyword, include_chats)
    print(f"\n  📓 Obsidian 扫描 · {vault.resolve()}")
    print(f"     关键词「{keyword}」命中 {len(hits)} 条笔记"
          f"（EditorChats {'含' if include_chats else '跳过'}）")
    for h in hits:
        print(f"     {'🟢' if h['status'].startswith('🟢') else '🟡'} {h['name']}  {h['rel']}")
        if h["dna"]:
            print(f"        DNA {h['dna']}")
    print("     注册: lh topo obsidian sync [图谱名] [--dir …] [--keyword 词]")
    print()


def cmd_obsidian_sync(topo_keyword: str, dir_arg: str = "", keyword: str = "通心译",
                      include_chats: bool = False):
    """lh topo obsidian sync [图谱名默认通心译] [--dir <vault>] [--keyword 词] [--chats]
    命中笔记注册为 kind=obsidian-mirror 子图谱节点(assets=笔记)·重复 sync=整体更新"""
    f, data = _find_topo_file(topo_keyword or "通心译")
    vault = _find_obsidian_vault(dir_arg)
    hits = _scan_obsidian_notes(vault, keyword, include_chats)
    if not hits:
        raise SystemExit(f"  ❌ 关键词「{keyword}」在 {vault.resolve()} 无命中笔记")
    green_n = sum(1 for h in hits if h["status"].startswith("🟢"))
    sg_name = f"📓 Obsidian·{keyword} 镜像"
    node = {
        "name": sg_name, "type": "obsidian-mirror",
        "dna": f"#龍芯⚡️{datetime.now():%Y-%m-%d}-OBSIDIAN-MIRROR-{keyword}-v1.0-UID9622",
        "status": "🟢 镜像同步" if green_n == len(hits) else "🟡 部分缺DNA",
        "link": f"obsidian://{vault.resolve()}",
        "subgraph_meta": {"vault": str(vault.resolve()), "vault_name": vault.name,
                          "note_count": len(hits), "keyword": keyword,
                          "scanned_at": datetime.now().astimezone().isoformat(timespec="seconds")},
        "assets": [{k: h[k] for k in ("name", "type", "id", "dna", "status", "link")} for h in hits],
    }
    subgraphs = data.setdefault("subgraphs", [])
    for i, sg in enumerate(subgraphs):
        if sg.get("name") == sg_name:
            subgraphs[i] = node
            break
    else:
        subgraphs.append(node)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n  📓 Obsidian 镜像同步 · {vault.name} → 图谱 {data.get('display')}")
    print(f"     「{keyword}」命中 {len(hits)} 条 · 🟢 {green_n} · 🟡 {len(hits) - green_n}")
    for h in hits:
        print(f"       {h['name']}  {h['rel']}")
    print()


def cmd_verify(keyword: str, json_out: bool = False):
    data = find_topo(keyword)
    green, yellow, neutral = asset_stats(data)
    gaps = []
    for g, a in iter_nodes(data):
        name, why = a.get("name", "?"), []
        if not (a.get("dna") or "").strip():
            why.append("缺DNA")
        if not (a.get("link") or "").strip():
            why.append("缺链接")
        s = (a.get("status") or "").strip()
        if not (s.startswith("🟢") or s.startswith("🟡")):
            why.append(f"状态异常({s or '空'})")
        if why:
            gaps.append({"group": g, "name": name,
                         "id": a.get("id"), "why": "·".join(why)})

    if json_out:
        if gaps:   # v1.8: verify 失败自动耻辱墙告警
            _shame_topo_append("topo_verify_alert",
                               f"拓扑校验失败 · {data.get('display')} · 缺口{len(gaps)}条",
                               color="🔴", bad=len(gaps))
        print(json.dumps({"topo": data.get("display"), "nodes": green+yellow+neutral,
                          "green": green, "yellow": yellow, "ok": not gaps,
                          "gaps": gaps}, ensure_ascii=False, indent=2))
        sys.exit(0 if not gaps else 1)

    print(f"\n  🕸️  拓扑校验 · {data.get('display')}")
    print(f"     节点 {green+yellow+neutral} · 🟢 {green} · 🟡 {yellow}")
    print("  " + "=" * 56)
    if not gaps:
        print(f"  ✅ 全绿 · {green+yellow+neutral} 资产 DNA+链接+状态 全部在位")
    else:
        if gaps:   # v1.8: verify 失败自动耻辱墙告警
            _shame_topo_append("topo_verify_alert",
                               f"拓扑校验失败 · {data.get('display')} · 缺口{len(gaps)}条",
                               color="🔴", bad=len(gaps))
        print(f"  🔴 缺口 {len(gaps)} 条：")
        for gp in gaps:
            print(f"     [{gp['group']}] {gp['name']}")
            print(f"        ↳ {gp['why']} · {gp['id']}")
    print()
    sys.exit(0 if not gaps else 1)


# ─────────────────────────── cite 引用溯源 / frameworks 清单 / 多源共用（v1.2）───────────────────────────

def _extract_dna(text: str) -> str:
    """从文本提取第一条 DNA 指纹（#龍芯⚡️ 至空白/标点边界）· obsidian/yuque 源资产溯源用"""
    if not text:
        return ""
    m = re.search(r"#龍芯⚡️[^\s，。、；：！？“”‘’（）()【】\[\]\n]+", text)
    return m.group(0) if m else ""


def _asset_fuzzy_score(q: str, an: str) -> float:
    """资产名模糊匹配分(0-1)：全串包含=1 · 段(·/｜/空格切分)命中率· cite 用"""
    if not q or not an:
        return 0.0
    if q in an or an in q:
        return 1.0
    segs = [s for s in re.split(r"[·｜/|\s、，,]+", q) if s]
    if not segs:
        return 0.0
    return sum(1 for s in segs if s in an) / len(segs)


def _get_secret(name: str) -> str:
    """通用密钥读取：lh_vault 优先 · 环境变量兜底（与 get_token 同构）· 语雀等源用"""
    for source in ("vault", "env"):
        val = ""
        if source == "vault":
            try:
                r = subprocess.run([sys.executable, str(ROOT / "bin" / "lh_vault.py"),
                                    "get", name], capture_output=True, text=True, timeout=30)
                val = (r.stdout or "").strip()
            except Exception:
                val = ""
        else:
            val = (os.environ.get(name) or "").strip()
        if val and not val.lower().startswith(("error", "❌", "usage")):
            return val
    return ""


def cmd_cite(name: str, json_out: bool = False):
    """lh topo cite <资产名> — 资产完整引用格式（DNA+链接 · 数字人引用溯源 v1.2）"""
    if not name:
        raise SystemExit("  ❌ 用法: lh topo cite <资产名>   例: lh topo cite \"慧慧·门面官\"")
    hits = []
    for f in list_topos():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for g in data.get("groups", []):
            for a in g.get("assets", []):
                an = a.get("name", "")
                score = _asset_fuzzy_score(name, an)
                if score >= 0.6:
                    hits.append({"name": an, "group": g.get("name"), "status": a.get("status", ""),
                                 "dna": a.get("dna", ""), "link": a.get("link", ""),
                                 "topo": data.get("display"), "score": round(score, 2)})
    if not hits:
        raise SystemExit(f"  ❌ 未找到资产「{name}」· 可先 lh topo list 查看资产清单")
    hits.sort(key=lambda h: -h["score"])
    if json_out:
        print(json.dumps({"query": name, "hits": hits}, ensure_ascii=False, indent=2))
        return
    for i, h in enumerate(hits[:3], 1):
        print(f"\n  📚 引用溯源 #{i} · {h['name']}")
        print("  " + "=" * 56)
        print(f"  层级: {h['group']} · 状态: {h['status'] or '未标注'}")
        print(f"  [DNA: {h['dna'] or '（待补）'}]")
        print(f"  链接: {h['link'] or '本地缓存'}")
        print("  " + "-" * 56)
        print("  标准引用格式:")
        for ln in (f"依据「龍魂·{h['topo']} · {h['name']}」知识资产作答。",
                   f"[DNA: {h['dna'] or '未标注'}]",
                   f"来源: {h['link'] or '本地缓存'}"):
            print(f"    > {ln}")
    print("\n  归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · 分层许可 CC BY-NC-SA 4.0(思想)/MulanPSL v2(工程)")
    print()


def scan_dependencies(dirs: tuple = ()) -> list:
    """扫描龍魂引擎源码实际第三方 import → 开源框架依赖清单（真实 site-packages 解析判定）
    （lh topo frameworks / lh judge topo-scan --frameworks 共用）
    标准库 / 工程自有模块（origin 落 /longhun-system/ 或工程目录同名）一律不算依赖"""
    targets = [Path(p) for p in dirs] if dirs else [ROOT / "08_BIN", ROOT / "bin"]
    dep_map = {}
    for td in targets:
        if not td.is_dir():
            continue
        for f in td.glob("*.py"):
            try:
                src = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in re.finditer(r"^\s*(?:import\s+([A-Za-z_][\w]*)|from\s+([A-Za-z_][\w]*))",
                                 src, re.M):
                mod = m.group(1) or m.group(2)
                if mod in sys.stdlib_module_names or mod.startswith("lh_"):
                    continue
                dep_map.setdefault(mod, set()).add(f.name)
    import importlib.util as _ilu          # noqa: I001 仅 find_spec 不执行代码
    saved = list(sys.path)
    sys.path.insert(0, str(ROOT))          # 让工程自有包可解析（用完还原）
    third_party = {}
    unresolved = 0
    try:
        for mod in dep_map:
            origin = ""
            try:
                spec = _ilu.find_spec(mod)
                origin = (spec.origin or "") if spec else ""
            except (ImportError, ValueError):
                origin = ""
            if "/longhun-system/" in origin.replace("\\", "/"):
                continue                    # 工程自有（pip -e 或包内）→ 不算框架
            if not origin:
                unresolved += 1             # 悬空/工程深链引用（历史/测试模块）→ 不入清单
                continue
            third_party[mod] = origin
    finally:
        sys.path[:] = saved
    return [{"framework": mod, "used_in": sorted(dep_map[mod]),
             "count": len(dep_map[mod]), "package": origin}
            for mod, origin in sorted(third_party.items())]


def cmd_frameworks(json_out: bool = False):
    """lh topo frameworks — 龍魂引擎实际依赖的开源框架清单（M77 下近空）· 写 ~/.longhun/topo/frameworks.json"""
    deps = scan_dependencies()
    out = {"scanned_dirs": ["08_BIN", "bin"], "frameworks": deps, "total": len(deps),
           "generated_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    with contextlib.suppress(Exception):
        VERIFY_DIR.mkdir(parents=True, exist_ok=True)
        (VERIFY_DIR / "frameworks.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if json_out:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print("\n  🧩 龍魂引擎开源框架依赖清单（M77 零中间层·纯标准库基线）")
    print("  " + "=" * 56)
    if not deps:
        print("  ✅ 零第三方运行时依赖（stdlib + 本地模块）· M77 守成")
    else:
        for d in deps:
            print(f"  • {d['framework']}  （{d['count']} 文件: {', '.join(d['used_in'][:4])}）")
    print(f"     清单: {VERIFY_DIR}/frameworks.json")
    print()


def _auto_verify_write(source: str, data: dict) -> dict:
    """同步后自动 verify 结构并写 ~/.longhun/topo/{source}_verify.json（任务A.2/A.3）"""
    gaps = []
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            why = []
            if not (a.get("dna") or "").strip():
                why.append("缺DNA")
            if not (a.get("link") or "").strip():
                why.append("缺链接")
            s = (a.get("status") or "").strip()
            if not (s.startswith("🟢") or s.startswith("🟡")):
                why.append(f"状态异常({s or '空'})")
            if why:
                gaps.append({"group": g.get("name"), "name": a.get("name"),
                             "why": "·".join(why)})
    green, yellow, neutral = asset_stats(data)
    res = {"source": source, "topo": data.get("display"),
           "nodes": green + yellow + neutral, "green": green, "yellow": yellow,
           "ok": not gaps, "gaps": gaps,
           "root_hash": topo_root_hash(data),
           "verify_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    with contextlib.suppress(Exception):
        VERIFY_DIR.mkdir(parents=True, exist_ok=True)
        (VERIFY_DIR / f"{source}_verify.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if res["ok"]:
        print(f"  ✅ 自动校验通过 · 🟢{green} · 🟡{yellow}"
              f" · 校验结果 {VERIFY_DIR}/{source}_verify.json")
    else:
        print(f"  🔴 自动校验缺口 {len(gaps)} 条"
              f" · 详见 {VERIFY_DIR}/{source}_verify.json")
    return res


# ─────────────────────────── sync（Notion API）───────────────────────────

def get_token() -> str:
    """token 权威源 = lh_vault（vault 主 token·集成龍芯北辰 UID9622）；环境变量仅兜底（可能含过期旧 token）"""
    for source in ("vault", "env"):
        tok = ""
        if source == "vault":
            try:
                r = subprocess.run([sys.executable, str(ROOT / "bin" / "lh_vault.py"),
                                    "get", "NOTION_TOKEN"],
                                   capture_output=True, text=True, timeout=30)
                tok = (r.stdout or "").strip()
            except Exception:
                tok = ""
        else:
            tok = (os.environ.get("NOTION_TOKEN") or "").strip()
        if tok and not tok.lower().startswith(("error", "❌", "usage")):
            return tok
    raise SystemExit("  ❌ 拿不到 NOTION_TOKEN（lh_vault get NOTION_TOKEN 与环境变量均失败）")


def notion_query(source_id: str, token: str, is_data_source: bool = True) -> list:
    """原生 urllib 直连 Notion（零依赖）· 多端点自动切换 · 返回全部行
    候选顺序: /v1/datasources/{id}/query → /v1/data_sources/{id}/query → /v1/databases/{id}/query
    （不同 API 版本/workspace 模型对端点拼写支持不一，逐个探测）"""
    last_err = ""
    for ep in (["datasources"] if is_data_source else []) + (["data_sources"] if is_data_source else []) + ["databases"]:
        url = f"{NOTION_API}/{ep}/{source_id}/query"
        rows = []

        def _call(cursor_, url_=url):
            body = {"page_size": 100}
            if cursor_:
                body["start_cursor"] = cursor_
            req = urllib.request.Request(
                url_, data=json.dumps(body).encode("utf-8"), method="POST",
                headers={"Authorization": f"Bearer {token}",
                         "Notion-Version": "2025-09-03",
                         "Content-Type": "application/json"})
            return _OPENER.open(req, timeout=30)

        try:
            resp = _call(None)
        except urllib.error.HTTPError as e:
            last_err = f"{e.code}: {e.read().decode('utf-8')[:160]}"
            continue
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            continue
        while True:
            with resp:
                res = json.loads(resp.read().decode("utf-8"))
            rows.extend(res.get("results", []))
            if not res.get("has_more"):
                break
            try:
                resp = _call(res.get("next_cursor"))
            except Exception as e:
                raise SystemExit(f"  ❌ Notion 分页失败: {e}") from None
        return rows
    raise SystemExit(f"  ❌ Notion query 端点全部不可用（data source/database）· {last_err}")


def _rich_text(prop):
    try:
        rt = prop.get("rich_text") or []
        return "".join(t.get("plain_text", "") for t in rt).strip()
    except Exception:
        return ""


def _status(prop):
    try:
        return (prop.get("status") or {}).get("name", "") or ""
    except Exception:
        return ""


def row_to_asset(row: dict) -> dict:
    p = row.get("properties", {})
    name = ""
    with contextlib.suppress(Exception):
        name = "".join(t.get("plain_text", "")
                       for t in (p.get("名字", {}).get("title") or [])).strip()
    link = ""
    origin = ""
    with contextlib.suppress(Exception):
        lurl = (p.get("页面链接", {}) or {}).get("url")
        if lurl:
            link, origin = lurl, "property"
    if not link:   # 行自身 app.notion.com 链接兜底（内部嵌入资产）
        with contextlib.suppress(Exception):
            url = row.get("url") or ""
            if url:
                link = url
                origin = "row_url"
    return {
        "name": name or row.get("id", "?"),
        "id": row.get("id", ""),
        "dna": _rich_text(p.get("DNA", {})),
        "status": _status(p.get("状态", {})),
        "link": link,
        "link_origin": origin,
    }


# ─────────────────────── SQLite 版本历史 / diff（任务C·2026-09-03）───────────────────────

def _row_payload(data: dict) -> dict:
    """把图谱 data 压成轻量历史行（不存大段 desc/link，diff 只看结构变更）"""
    assets = []
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            assets.append({"group": g.get("name", ""), "name": a.get("name", ""),
                           "type": a.get("type", ""), "status": a.get("status", ""),
                           "dna": a.get("dna", ""), "probe": a.get("probe", "")})
    return {"topo_name": data.get("topo_name", data.get("display", "unknown")),
            "display": data.get("display", ""),
            "last_sync": data.get("last_sync", ""), "assets": assets}


def _db_conn() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""CREATE TABLE IF NOT EXISTS topo_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topo_name TEXT NOT NULL,
        ts TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        payload TEXT NOT NULL)""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_history_name ON topo_history(topo_name, ts)")
    return conn


def _archive_snapshot(data: dict):
    """sync 落盘后归档一条版本历史（append-only·SQLite 零三方依赖）"""
    try:
        row = _row_payload(data)
        payload = json.dumps(row, ensure_ascii=False)
        sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
        conn = _db_conn()
        conn.execute("INSERT INTO topo_history(topo_name, ts, sha256, payload) VALUES(?,?,?,?)",
                     (row["topo_name"], row.get("last_sync") or
                      datetime.now().astimezone().isoformat(timespec="seconds"),
                      sha, payload))
        conn.commit()
        conn.close()
    except Exception:   # noqa: BLE001 归档失败不阻断 sync
        pass


def cmd_db(action: str = "init"):
    """lh topo db init|status — SQLite 持久化层（任务C）
    init: 建库 + 把现有 docs/topology/*.json 全量灌入首次快照
    status: 库文件/表/各图谱历史条数/最后归档"""
    if action == "init":
        conn = _db_conn()
        n = 0
        for f in sorted(TOPO_DIR.glob("*_legion_topo.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            # 去重: 同 topo_name+last_sync 已存在则跳过
            row = _row_payload(d)
            payload = json.dumps(row, ensure_ascii=False)
            ts = row.get("last_sync") or ""
            cur = conn.execute(
                "SELECT 1 FROM topo_history WHERE topo_name=? AND ts=?",
                (row["topo_name"], ts)).fetchone()
            if cur is None:
                sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
                conn.execute(
                    "INSERT INTO topo_history(topo_name, ts, sha256, payload) VALUES(?,?,?,?)",
                    (row["topo_name"], ts, sha, payload))
                n += 1
        conn.commit()
        conn.close()
        print(f"\n  🗄️  SQLite 图谱库初始化 · {DB_PATH}")
        print(f"     灌入 {n} 条新快照（幂等·重复跳过）")
        return 0
    if action == "status":
        if not DB_PATH.is_file():
            print("  ⚪ SQLite 图谱库未初始化 · 先跑 lh topo db init")
            return 0
        conn = _db_conn()
        total = conn.execute("SELECT COUNT(*) FROM topo_history").fetchone()[0]
        rows = conn.execute(
            "SELECT topo_name, COUNT(*), MAX(ts) FROM topo_history "
            "GROUP BY topo_name ORDER BY topo_name").fetchall()
        conn.close()
        print(f"\n  🗄️  SQLite 图谱历史库 · {DB_PATH}")
        print(f"     总快照 {total} 条")
        for name, cnt, last in rows:
            print(f"     · {name}: {cnt} 条 · 最后 {last}")
        return 0
    print("  usage: lh topo db init|status")
    return 1


def _history_rows(topo_name: str) -> list:
    conn = _db_conn()
    rows = conn.execute(
        "SELECT ts, sha256, payload FROM topo_history WHERE topo_name=? "
        "ORDER BY ts ASC", (topo_name,)).fetchall()
    conn.close()
    out = []
    for ts, sha, payload in rows:
        try:
            out.append({"ts": ts, "sha256": sha, **json.loads(payload)})
        except Exception:
            continue
    return out


def cmd_diff(keyword: str, since: str = "", json_out: bool = False):
    """lh topo diff <图谱名> [--since <YYYY-MM-DD[THH:MM:SS]>] — 图谱变更历史（任务C）
    默认显示最近两个快照的差异；--since 指定时点(UTC)后首个快照起对比"""
    f, data = _find_topo_file(keyword)
    topo_name = data.get("topo_name")
    rows = _history_rows(topo_name)
    if len(rows) < 2:
        print(f"  ⚪ 「{topo_name}」历史不足 2 条（{len(rows)}）· 先 lh topo sync 积累快照")
        return 0
    if since:
        rows = [r for r in rows if r["ts"] >= since]
        if len(rows) < 1:
            print(f"  ⚪ since={since} 之后无快照")
            return 0
        if len(rows) == 1:
            print(f"  ⚪ since={since} 后仅 1 条快照（{rows[0]['ts']}）· 无对比对象")
            return 0
    base, cur = rows[-2], rows[-1]

    def _idx(r):
        return {a["name"]: a for a in r.get("assets", [])}

    bi, ci = _idx(base), _idx(cur)
    added = [n for n in ci if n not in bi]
    removed = [n for n in bi if n not in ci]
    changed = []
    for n, a in ci.items():
        b = bi.get(n)
        if not b:
            continue
        if b.get("status") != a.get("status"):
            changed.append((n, b.get("status"), a.get("status")))
    if json_out:
        print(json.dumps({"topo_name": topo_name, "base_ts": base["ts"],
                          "cur_ts": cur["ts"], "added": added,
                          "removed": removed,
                          "changed": [{"name": x[0], "from": x[1], "to": x[2]}
                                      for x in changed]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🕸️  图谱变更 · {topo_name}")
    print(f"     对比 {base['ts']}  →  {cur['ts']}")
    print(f"     新增 {len(added)} · 移除 {len(removed)} · 状态变更 {len(changed)}")
    for n in added:
        print(f"     ➕ {n}")
    for n in removed:
        print(f"     ➖ {n}")
    for n, frm, to in changed:
        print(f"     ✏️  {n}: {frm} → {to}")
    return 0


# ─────────────────────────── 活体校验同步 ───────────────────────────

def _sync_live_check(keyword: str, dry_run: bool = False) -> dict:
    """本地注册图谱活体校验同步（v1.3·2026-09-03·任务F）
    按节点类型实时探测: model→ollama list / engine→文件在位 / tool→ollama 命令可达
    framework→python import 探测 / dataset→总台缓存+根哈希 / 耻辱墙目录记录数
    同步训练数据=更新 dataset 节点时间戳与状态 → 刷新 last_sync 落盘（--dry-run 仅预览）
    v1.4(2026-09-03·深度学习代码精修): 探测结果统一落盘 ~/.longhun/topo/<图谱名>.json
    （ollama/torch/transformers 状态快照·lh health 与外部引擎统一读取点）"""
    import importlib.util
    import shutil
    f, data = _find_topo_file(keyword)
    live_sum: dict = {"ollama": None, "ollama_cmd": None}   # 探测结果聚合·ollama/files/py.* 动态键

    def _ollama_list():
        try:
            r = subprocess.run(["ollama", "list"], capture_output=True,
                               text=True, timeout=8)
            return r.stdout if r.returncode == 0 else ""
        except Exception:
            return None

    def _probe(asset) -> tuple:
        typ = (asset.get("type") or "").strip().lower()
        nm = (asset.get("name") or "").strip()
        stem = nm.split("（")[0].strip()
        p = (asset.get("path") or "").strip()
        src = (asset.get("source") or "") + (asset.get("desc") or "")
        s = (asset.get("status") or "").strip()
        tag = ""
        if typ == "model":
            out = _ollama_list()
            if out is None:
                live_sum["ollama"] = False
                tag = "ollama 不可达(未启动)"
            elif any(stem in ln.split()[:1] or stem in ln.split()[0]
                     for ln in out.splitlines()[1:] if ln.strip()):
                live_sum["ollama"] = True
                tag, s = "ollama 模型在位", "🟢 可用"
            else:
                live_sum["ollama"] = False
                tag = "ollama 未找到该模型"
        elif typ == "engine":
            if p:
                ok = (ROOT / p).exists() or Path(p).expanduser().exists()
                tag = "文件在位" if ok else "文件缺失"
                s = ("🟢 可用" if ok else "🔴 缺失")
                live_sum.setdefault("files", {})[stem] = bool(ok)
            else:
                tag = "无路径可检"
        elif typ == "tool":
            if shutil.which("ollama"):
                live_sum["ollama_cmd"] = True
                tag, s = "ollama 命令可达", "🟢 已接入"
            else:
                live_sum["ollama_cmd"] = False
                tag = "ollama 不在 PATH"
        elif typ == "framework":
            mod = {"PyTorch": "torch", "Transformers": "transformers"}.get(stem, "")
            ok = bool(mod) and importlib.util.find_spec(mod) is not None
            tag = f"{mod or stem} 已安装" if ok else f"{mod or stem} 未安装(保持待注册)"
            if ok:
                s = "🟢 已接入"
            elif not s:
                s = "🟡 待注册"
            if mod:
                live_sum[f"py.{mod}"] = bool(ok)
        elif typ == "dataset":
            if "总台" in src or "Notion" in src:
                cached = TOPO_DIR / "tongxinyi_legion_topo.json"
                root_ok = False
                if cached.is_file():
                    try:
                        root_ok = topo_root_hash(json.loads(
                            cached.read_text(encoding="utf-8"))) == "3C3874A43FFE1A4B"
                    except Exception:
                        root_ok = False
                tag = "总台缓存+根哈希一致" if root_ok else "总台缓存缺失/根哈希不符"
                if root_ok:
                    s = "🟢 已同步"
            elif "shame_wall" in src or "shame_wall" in p or "耻辱墙" in src:
                d = Path("~/.longhun/shame_wall/").expanduser()
                n = sum(1 for _ in d.rglob("*")) if d.is_dir() else 0
                tag = f"耻辱墙 {n} 条记录" if d.is_dir() else "耻辱墙目录缺失"
                if d.is_dir():
                    s = "🟢 有记录"
        return s, tag

    changed = []
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            new_s, tag = _probe(a)
            if tag:
                a["probe"] = tag
                a["last_probe"] = datetime.now().astimezone().isoformat(timespec="seconds")
            if new_s and new_s != (a.get("status") or "").strip():
                changed.append((a.get("name"), a.get("status"), new_s))
                if not dry_run:
                    a["status"] = new_s
    if not dry_run:
        data["last_sync"] = datetime.now().astimezone().isoformat(timespec="seconds")
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        # v1.4 精修: 活体探测结果统一落盘 ~/.longhun/topo/<图谱名>.json
        snapshot = {
            "schema": "longhun-topo-live-v1", "topo_name": data.get("topo_name"),
            "display": data.get("display"), "owner": data.get("owner", ""),
            "last_sync": data.get("last_sync", ""), "live": live_sum,
            "assets": [{"group": g.get("name"), "name": a.get("name"),
                        "type": a.get("type"), "dna": a.get("dna", ""),
                        "status": a.get("status", ""), "probe": a.get("probe", ""),
                        "last_probe": a.get("last_probe", "")}
                       for g in data.get("groups", []) for a in g.get("assets", [])],
        }
        try:
            VERIFY_DIR.mkdir(parents=True, exist_ok=True)
            (VERIFY_DIR / f"{data.get('topo_name')}.json").write_text(
                json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:   # noqa: BLE001 快照落盘失败不阻断 sync
            pass
        _archive_snapshot(data)   # 任务C: 版本历史入 SQLite（append-only·支撑 topo diff）
    green, yellow, neutral = asset_stats(data)
    print(f"\n  🕸️  图谱同步(活体校验) · {data.get('display')}")
    print(f"     节点 {green+yellow+neutral} · 🟢{green} · 🟡{yellow}"
          f"{(' · ⚪'+str(neutral)) if neutral else ''}"
          f"{' · dry-run 未落盘' if dry_run else ''}")
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            print(f"     [{g.get('name')}] {a.get('name')} → {a.get('status','')}"
                  f" · {a.get('probe','')}")
    print(f"     状态更新 {len(changed)} 条 · last_sync {data.get('last_sync','-')}")
    print()
    return {"ok": not changed}


def cmd_sync(keyword: str, dry_run: bool = False, source: str = "notion",
             obsidian_dir: str = "", yuque_namespace: str = "", live: bool = False):
    """lh topo sync 图谱名 [--source notion|obsidian|yuque] [--dir <md目录>]
    [--namespace <login/slug>] [--live]
    v1.2 多数据源：notion(默认·Notion API) / obsidian(本地 .md 目录) / yuque(语雀 API)
    每源同步后自动 lh topo verify 校验结构 → 写 ~/.longhun/topo/{source}_verify.json
    v1.4: --live 显式活体校验（本地注册图谱自动/任意图谱可强制）→ 落盘 ~/.longhun/topo/<名>.json"""
    # v1.3: 本地注册图谱（sync_from=live-check）→ 活体状态校验同步（模型/文件/库实时探测）
    try:
        _loc_f, _loc_data = _find_topo_file(keyword)
    except SystemExit:
        _loc_data = None
    if _loc_data is not None and _loc_data.get("auto_docs_sync"):
        return cmd_topo_docs_sync(keyword, dry_run)   # v1.7: 12_DOCS 文档自动拓扑同步
    if live or (_loc_data is not None and _loc_data.get("sync_from") == "live-check"):
        return _sync_live_check(keyword, dry_run)
    if source == "obsidian":
        return _sync_from_obsidian(keyword, obsidian_dir, dry_run)
    if source == "yuque":
        return _sync_from_yuque(keyword, yuque_namespace, dry_run)
    data = find_topo(keyword)
    token = get_token()
    print(f"\n  🕸️  拓扑同步 · {data.get('display')}")
    print(f"     拉取 Notion → {data.get('source_url')}")
    rows = notion_query(data.get("data_source_id") or data.get("database_id", ""), token,
                        is_data_source=bool(data.get("data_source_id")))
    print(f"     读到 {len(rows)} 行")

    old_index = {}
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            old_index[a.get("name")] = a

    # 组内按 Notion 顺序收集；组顺序固定（GROUP_ORDER）
    pending = {gname: [] for gname in GROUP_ORDER}
    pending["_other"] = []
    for row in rows:
        asset = row_to_asset(row)
        try:
            grp = ((row.get("properties", {}).get("组别", {}).get("select") or {}).get("name") or "")
        except Exception:
            grp = ""
        bucket = pending.get(grp)
        if bucket is None:
            bucket = pending["_other"]
        bucket.append(asset)

    groups = []
    for gname in GROUP_ORDER:
        if pending[gname]:
            groups.append({"name": gname, "assets": pending[gname]})
    if pending["_other"]:
        # 未知组别：归入按实际组名分桶
        others = {}
        for row in rows:
            try:
                gn = ((row.get("properties", {}).get("组别", {}).get("select") or {}).get("name") or "")
            except Exception:
                gn = ""
            if gn and gn not in GROUP_ORDER:
                others.setdefault(gn, []).append(row_to_asset(row))
        for gn, assets in others.items():
            groups.append({"name": gn, "assets": assets})

    # 差异统计
    new_index = {}
    for g in groups:
        for a in g.get("assets", []):
            new_index[a.get("name")] = a
    added = [n for n in new_index if n not in old_index]
    removed = [n for n in old_index if n not in new_index]
    changed = []
    for n, a in new_index.items():
        o = old_index.get(n)
        if o is None:
            continue
        if (a.get("dna") != o.get("dna") or a.get("link") != o.get("link")
                or a.get("status") != o.get("status")):
            changed.append(n)

    if dry_run:
        print(f"  🔍 dry-run：新增 {len(added)} · 更新 {len(changed)} · 移除 {len(removed)}（不落盘）")
        return

    data["groups"] = groups
    data["last_sync"] = datetime.now().astimezone().isoformat(timespec="seconds")
    data["sync_from"] = "notion-api-live"
    TOPO_DIR.mkdir(parents=True, exist_ok=True)
    target = TOPO_DIR / f"{data.get('topo_name', 'unknown')}_legion_topo.json"
    # 文件名稳定：优先沿用已有文件；找不到则按 topo_name 推导
    existing = next(iter(list_topos()), None)
    if existing is not None:
        try:
            cur = json.loads(existing.read_text(encoding="utf-8"))
            if cur.get("topo_name") == data.get("topo_name"):
                target = existing
        except Exception:
            pass
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    _archive_snapshot(data)   # 任务C: 版本历史入 SQLite（append-only·支撑 topo diff）
    # 同步成功后联动刷新数字人知识库状态 last_sync（任务3 定时同步 · 2026-09-02）
    with contextlib.suppress(Exception):
        if DH_KB_STATE.exists():
            st = json.loads(DH_KB_STATE.read_text(encoding="utf-8"))
            st["last_sync"] = data["last_sync"]
            st["source"] = str(target.relative_to(ROOT))
            DH_KB_STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
    for n in added:
        print(f"  ➕ 新增 {n}")
    for n in removed:
        print(f"  ➖ 移除 {n}")
    for n in changed:
        print(f"  ✏️  更新 {n}")
    green, yellow, neutral = asset_stats(data)
    print(f"  ✅ 落盘 {target.relative_to(ROOT)}")
    print(f"     共 {green+yellow+neutral} 条 · 新增 {len(added)} · 更新 {len(changed)}"
          f" · 移除 {len(removed)} · 🟢{green} · 🟡{yellow}")
    _auto_verify_write("notion", data)
    print()


def _persist_source_graph(keyword: str, source: str, display: str, source_url: str,
                          groups: list, sync_from: str, dry_run: bool = False):
    """镜像源(obsidian/yuque)落盘共用：topo_name=图谱名-source·独立缓存文件·自动校验
    不覆盖数字人 dh_kb_state（该 state 仅主图谱 Notion 源联动）"""
    topo_name = f"{keyword}-{source}"
    old = {}
    try:
        _f0, d0 = _find_topo_file(topo_name)   # 既有镜像 → 保留 display/source_url
        if d0.get("display"):
            display = d0["display"]
        if d0.get("source_url"):
            source_url = d0["source_url"]
        old = {a.get("name"): a for g in d0.get("groups", []) for a in g.get("assets", [])}
    except SystemExit:
        pass
    new = {a.get("name") for g in groups for a in g.get("assets", [])}
    added = sorted(new - set(old))
    removed = sorted(set(old) - new)
    if dry_run:
        print(f"  🔍 dry-run：新增 {len(added)} · 移除 {len(removed)}（不落盘）")
        return
    data = {"topo_name": topo_name, "display": display, "version": "v1.2",
            "source_url": source_url, "sync_from": sync_from, "source": source,
            "groups": groups,
            "last_sync": datetime.now().astimezone().isoformat(timespec="seconds")}
    TOPO_DIR.mkdir(parents=True, exist_ok=True)
    target = TOPO_DIR / f"{topo_name}_legion_topo.json"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _archive_snapshot(data)   # 任务C: 版本历史入 SQLite（append-only·支撑 topo diff）
    for n in added:
        print(f"  ➕ 新增 {n}")
    for n in removed:
        print(f"  ➖ 移除 {n}")
    green, yellow, neutral = asset_stats(data)
    print(f"  ✅ 落盘 {target.relative_to(ROOT)}")
    print(f"     共 {green+yellow+neutral} 条 · 新增 {len(added)} · 移除 {len(removed)}"
          f" · 🟢{green} · 🟡{yellow}")
    _auto_verify_write(source, data)
    print()


def _sync_from_obsidian(keyword: str, vault: str, dry_run: bool = False):
    """数据源=Obsidian 本地文档库：读取目录 .md（子目录=层级组·根级入文档库）
    资产 DNA 从文件头 #龍芯⚡️ 指纹提取；有 DNA=🟢活跃 · 无=🟡待命"""
    vault_dir = Path(os.path.expanduser(vault or ""))
    if not vault_dir.is_dir():
        raise SystemExit(f"  ❌ Obsidian 文档库目录无效: {vault or '(空)'}"
                         f"（--source obsidian 需 --dir <md目录>）")
    files = sorted(vault_dir.rglob("*.md"))
    if not files:
        raise SystemExit(f"  ❌ 目录 {vault_dir.resolve()} 下无 .md 文件")
    print(f"\n  🕸️  拓扑同步 · {keyword}（Obsidian 文档库源 v1.2）")
    print(f"     读取 {vault_dir.resolve()} → {len(files)} 个 .md")
    groups_map = {}
    for f in files:
        rel = f.relative_to(vault_dir)
        grp = str(rel.parent) if str(rel.parent) != "." else "📄 文档库"
        content = f.read_text(encoding="utf-8", errors="replace")
        dna = _extract_dna(content[:4000])
        groups_map.setdefault(grp, []).append({
            "name": f.stem, "id": f"obsidian:{rel}", "dna": dna,
            "status": "🟢 活跃" if dna else "🟡 待命",
            "link": f"file://{f.resolve()}", "link_origin": "local-file"})
    groups = [{"name": gn, "assets": sorted(ga, key=lambda a: a["name"])}
              for gn, ga in sorted(groups_map.items())]
    _persist_source_graph(keyword, "obsidian", f"🌐 {keyword} 文档库镜像 · Obsidian",
                          f"obsidian://{vault_dir.resolve()}", groups,
                          "obsidian-local", dry_run)


def _sync_from_yuque(keyword: str, namespace: str, dry_run: bool = False):
    """数据源=语雀(Yuque) API v2：GET repos/{login/slug}/docs · X-Auth-Token=YUQUE_TOKEN
    ≤40 篇小库逐篇拉正文提 DNA；link 按 slug 拼 yuque.com/{ns}/{slug}"""
    token = _get_secret("YUQUE_TOKEN")
    if not token:
        raise SystemExit("  ❌ 语雀源需要 token：lh_vault set YUQUE_TOKEN <token>"
                         "（vault 优先·环境变量兜底）")
    ns = namespace or _get_secret("YUQUE_NAMESPACE")
    if not ns or "/" not in ns:
        raise SystemExit("  ❌ 语雀 namespace 必给: --namespace <login/slug>"
                         "（如 zhugexin/知识库slug）")
    print(f"\n  🕸️  拓扑同步 · {keyword}（语雀知识库源 v1.2）")
    url = f"{YUQUE_API}/repos/{ns}/docs"
    try:
        req = urllib.request.Request(
            url, headers={"X-Auth-Token": token, "User-Agent": "longhun-topo/1.2"})
        with _OPENER.open(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as e:   # noqa: BLE001 网络/401 统一报错
        raise SystemExit(f"  ❌ 语雀 API 失败（{url}）: {e}") from None
    docs = body.get("data") or []
    print(f"     读到 {len(docs)} 篇文档 · {url}")
    assets = []
    for doc in docs[:60]:
        title = doc.get("title") or doc.get("slug") or "?"
        slug = doc.get("slug") or str(doc.get("id", ""))
        did = str(doc.get("id", ""))
        text = title + " " + (doc.get("description") or "")
        if len(docs) <= 40:    # 小库逐篇拉正文提 DNA 指纹（防 N+1 放大）
            try:
                req2 = urllib.request.Request(
                    f"{YUQUE_API}/repos/{ns}/docs/{did}",
                    headers={"X-Auth-Token": token, "User-Agent": "longhun-topo/1.2"})
                with _OPENER.open(req2, timeout=30) as r2:
                    det = json.loads(r2.read().decode("utf-8")).get("data", {})
                body_html = det.get("body_html") or det.get("body") or ""
                text += " " + re.sub(r"<[^>]+>", " ", body_html)[:8000]
            except Exception:   # noqa: BLE001 单篇正文失败不阻断
                pass
        dna = _extract_dna(text[:4000])
        assets.append({"name": title, "id": f"yuque:{did or slug}", "dna": dna,
                       "status": "🟢 活跃" if dna else "🟡 待命",
                       "link": f"https://www.yuque.com/{ns}/{slug}",
                       "link_origin": "yuque-api"})
    groups = [{"name": "📚 文档库", "assets": assets}]
    _persist_source_graph(keyword, "yuque", f"🌐 {keyword} 知识库镜像 · 语雀",
                          f"https://www.yuque.com/{ns}", groups, "yuque-api-live", dry_run)


# ─────────────────────────── main ───────────────────────────

_ACTIONS = ["list", "verify", "sync", "stats", "serve", "kb-status",
            "cite", "frameworks", "register", "node", "diff", "db",
            "subgraph", "obsidian", "edge", "status", "summary", "export",
            "export-page", "audit-log", "search", "ask", "events",
            "audit-chain", "audit-verify", "history", "heal",
            "weekly-report", "serve-api", "feedback", "archive"]


def main():
    # 口语化词序规整 v1.8: 「lh topo <图谱名> <action> [关键词/--flags]」
    #   → 「lh topo <action> <图谱名> [--kw 关键词/--flags]」· search 裸关键词转 --kw
    if len(sys.argv) >= 3 and sys.argv[1] not in _ACTIONS and sys.argv[2] in _ACTIONS:
        act, graph, tail = sys.argv[2], sys.argv[1], list(sys.argv[3:])
        new_argv = sys.argv[:1] + [act, graph]
        i = 0
        while i < len(tail):
            t = tail[i]
            if act in ("search", "ask") and not t.startswith("-"):
                new_argv += ["--query", t]
            else:
                new_argv.append(t)
            i += 1
        sys.argv = new_argv
    ap = argparse.ArgumentParser(description="龍魂知识图谱拓扑引擎 (lh topo)")
    ap.add_argument("action", nargs="?", default="list", choices=_ACTIONS,
                    help="list/verify/sync/serve/kb-status/cite/frameworks/register/node/diff/db/subgraph/obsidian/edge/status/summary/search/export/export-page/audit-log/audit-chain/audit-verify/history/heal/weekly-report/serve-api")
    ap.add_argument("keyword", nargs="?", default="", help="图谱名/资产名关键词（如 通心译）")
    ap.add_argument("--query", default="", help="search 搜索关键词（名称/类型/DNA/描述）")
    ap.add_argument("--format", default="json", choices=["json"],
                    help="export 导出格式（当前 json）")
    ap.add_argument("--limit", type=int, default=20, help="audit-log 最近 N 条")
    ap.add_argument("--kind", default="",
                    help="events 按事件类型过滤 (topo_change/topo-feedback/topo-verify_alert/topo_healed…)")
    ap.add_argument("--node-type", default="",
                    help="events 按变更节点类型过滤 (model/engine/document/article/asset/…)")
    ap.add_argument("--port", type=int, default=8762, help="serve 监听端口 (默认 8762)")
    ap.add_argument("--api-port", type=int, default=8873, help="serve-api 监听端口 (默认 8873)")
    ap.add_argument("--host", default="127.0.0.1",
                    help="serve 监听地址 (默认 127.0.0.1·对外显式 0.0.0.0)")
    ap.add_argument("--source", default="notion",
                    help="sync 数据源 (notion/obsidian/yuque) 或 node 的来源")
    ap.add_argument("--dir", default="", help="--source obsidian 的本地 .md 目录")
    ap.add_argument("--namespace", default="", help="--source yuque 的 <login/slug>")
    ap.add_argument("--dry-run", action="store_true", help="sync 预览不落盘")
    ap.add_argument("--live", action="store_true",
                    help="sync 显式活体校验(本地注册图谱自动·任意图谱可强制) v1.4")
    ap.add_argument("--since", default="", help="diff 起始时点 (YYYY-MM-DD[THH:MM:SS]·任务C)")
    ap.add_argument("--json", action="store_true", help="verify/kb-status/cite/frameworks/diff 输出 JSON")
    ap.add_argument("--display", default="", help="register 图谱显示名")
    ap.add_argument("--group", default="", help="node 所属组（如 模型层·不存在自动建）")
    ap.add_argument("--name", default="", help="node 节点名")
    ap.add_argument("--type", default="other", help="node 类型 model/engine/dataset/tool/framework")
    ap.add_argument("--dna", default="", help="node DNA 追溯码")
    ap.add_argument("--status", default="🟢 可用", help="node 状态（🟢/🟡）")
    ap.add_argument("--path", default="", help="node 本地路径")
    ap.add_argument("--desc", default="", help="node 描述/用途")
    ap.add_argument("--link", default="", help="node 链接（缺省回退 path/source）")
    ap.add_argument("--db-id", default="", help="subgraph 关联库 database id")
    ap.add_argument("--meta", default="", help="subgraph 库元数据 JSON（row_count/created/edited/parent）")
    ap.add_argument("--kw", default="", help="obsidian scan/sync 命中关键词（默认 通心译）")
    ap.add_argument("--chats", action="store_true", help="obsidian 含 EditorChats 会话存档")
    ap.add_argument("--target", default="", help="edge 目标节点")
    ap.add_argument("--label", default="", help="edge 标签/说明")
    args = ap.parse_args()

    if args.action == "list":
        cmd_list(args.keyword)
    elif args.action == "stats":
        s = load_topo_data()
        print(json.dumps(s, ensure_ascii=False, indent=2))
    elif args.action == "verify":
        cmd_verify(args.keyword or "通心译", json_out=args.json)
    elif args.action == "sync":
        cmd_sync(args.keyword or "通心译", dry_run=args.dry_run, source=args.source,
                 obsidian_dir=args.dir, yuque_namespace=args.namespace, live=args.live)
    elif args.action == "serve":
        cmd_serve(port=args.port, host=args.host, keyword=args.keyword or "通心译")
    elif args.action == "kb-status":
        cmd_kb_status(args.keyword or "通心译", json_out=args.json)
    elif args.action == "cite":
        cmd_cite(args.keyword, json_out=args.json)
    elif args.action == "frameworks":
        cmd_frameworks(json_out=args.json)
    elif args.action == "register":
        cmd_register_graph(args.keyword, display=args.display)
    elif args.action == "node":
        cmd_node_add(args.keyword, group=args.group, name=args.name, ntype=args.type,
                     dna=args.dna, status=args.status, path=args.path,
                     source=args.source, desc=args.desc, link=args.link)
    elif args.action == "edge":
        cmd_edge_add(args.keyword, source=args.source, target=args.target,
                     etype=(args.type if args.type and args.type != "other" else ""),
                     label=args.label, desc=args.desc)
    elif args.action == "status":
        cmd_topo_status(args.keyword)
    elif args.action == "summary":
        cmd_topo_summary(args.keyword, json_out=args.json)
    elif args.action == "search":
        cmd_topo_search(args.keyword, kw=args.query, json_out=args.json)
    elif args.action == "export":
        cmd_topo_export(args.keyword, json_out=args.json)
    elif args.action == "export-page":
        cmd_topo_export_page(args.keyword, json_out=args.json)
    elif args.action == "feedback":
        cmd_topo_feedback(args.keyword or "对外交付")
    elif args.action == "archive":
        cmd_topo_archive(args.keyword or "对外交付")
    elif args.action == "audit-log":
        cmd_topo_audit_log(args.keyword, json_out=args.json, limit=args.limit)
    elif args.action == "ask":
        cmd_topo_ask(args.keyword, question=args.query, json_out=args.json)
    elif args.action == "events":
        cmd_topo_events(args.keyword, limit=args.limit, json_out=args.json,
                        kind=args.kind, node_type=args.node_type)
    elif args.action == "audit-chain":
        cmd_topo_audit_chain(args.keyword, limit=args.limit, json_out=args.json)
    elif args.action == "audit-verify":
        cmd_topo_audit_verify(args.keyword, json_out=args.json)
    elif args.action == "history":
        cmd_topo_history(args.keyword, since=args.since, json_out=args.json)
    elif args.action == "heal":
        cmd_topo_heal(args.keyword, dry=args.dry_run, json_out=args.json)
    elif args.action == "weekly-report":
        cmd_topo_weekly_report(args.keyword, json_out=args.json)
    elif args.action == "serve-api":
        cmd_topo_serve_api(args.keyword, port=args.api_port, host=args.host)
    elif args.action == "diff":
        cmd_diff(args.keyword, since=args.since, json_out=args.json)
    elif args.action == "db":
        cmd_db(action=args.keyword or "init")
    elif args.action == "subgraph":
        cmd_subgraph_register(args.keyword, name=args.name, db_id=args.db_id,
                              dna=args.dna, status=args.status, link=args.link,
                              meta=args.meta, ntype=args.type)
    elif args.action == "obsidian":
        mode = args.keyword if args.keyword in ("scan", "sync") else "scan"
        kw = args.kw or "通心译"
        if mode == "sync":
            cmd_obsidian_sync(args.name or "通心译", dir_arg=args.dir,
                              keyword=kw, include_chats=args.chats)
        else:
            cmd_obsidian_scan(dir_arg=args.dir, keyword=kw, include_chats=args.chats)
    else:
        cmd_list(args.keyword)


if __name__ == "__main__":
    main()
