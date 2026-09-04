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
from datetime import datetime
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

def main():
    ap = argparse.ArgumentParser(description="龍魂知识图谱拓扑引擎 (lh topo)")
    ap.add_argument("action", nargs="?", default="list",
                    choices=["list", "verify", "sync", "stats", "serve", "kb-status",
                             "cite", "frameworks", "register", "node", "diff", "db",
                             "subgraph", "obsidian"],
                    help="list/verify/sync/serve/kb-status/cite/frameworks/register/node/diff/db/subgraph/obsidian")
    ap.add_argument("keyword", nargs="?", default="", help="图谱名/资产名关键词（如 通心译）")
    ap.add_argument("--port", type=int, default=8762, help="serve 监听端口 (默认 8762)")
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
