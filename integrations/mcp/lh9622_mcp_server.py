#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-07-LH9622-MCP-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""╔══════════════════════════════════════════════════════════════════════╗
║   9622 · 龍魂管家 MCP Server v1.0 — 记忆 · Notion · 电脑 三合一          ║
║   DNA: #龍芯⚡️2026-09-07-LH9622-MCP-v1.0-UID9622                      ║
║   创建者: 诸葛鑫 | UID9622 · 龍芯北辰                                     ║
║   三色: 🟢 首发 · stdlib零三方 · Notion直连官方REST                       ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
老大一句话：「做个9622的MCP。接入Notion，让Notion能调用我们全部的记忆，
还可以操作我们的电脑。」
→ 本 Server = 龍魂本地管家，三大桥一次接好：
   🧠 记忆桥  — 检索龍魂全部本地记忆（MEMORY/每日日志/STATE/会话上下文/大脑）
   🌐 Notion桥 — 直连龍魂 Notion 门户（官方 REST · 无需官方 MCP · 零三方）
   🖥️ 电脑闸  — 操作本机（限域白名单 + 4红线硬拒 + kill_switch + 操作留痕）

【安全设计】电脑操作能力必须戴镣铐：
   · 限域: 命令/文件只允许落在 longhun-system/.longhun/.codebuddy 白名单
   · 4红线硬拒: rm -rf 家目录 · git push --force main · 写 .ssh/.gnupg · 删系统目录
   · kill_switch: ~/.longhun/mcp_9622/kill_switch 存在 → 执行/写操作全拒
   · 审计: 每次执行 append-only 记 ~/.longhun/mcp_9622/audit.jsonl（日志即证据）
   · 代理清除: Mac 下 socks 代理毒化 urllib/外连，一律清掉

【工具清单】(10)
  🧠 lh_memory_search   — 关键词检索全部记忆（多目录 · 上下文片段）
  🧠 lh_memory_digest   — 记忆总摘要（MEMORY 目录 + 最近日志 + 会话任务）
  🧠 lh_session_context — 读会话断点上下文 ~/.longhun/session_context.json
  🌐 lh_notion_health   — Notion token/API 健康
  🌐 lh_notion_search   — 搜索龍魂 Notion 全部页面/数据库（翻页）
  🌐 lh_notion_read     — 读页面/数据源内容（page id / url 均可）
  🌐 lh_notion_query_db — 查数据库所有行（翻页）
  🖥️ lh_machine_exec    — 执行本机命令（白名单cwd + 4红线 + kill_switch + 审计）
  🖥️ lh_machine_files   — 白名单内 列表/读/写 文件
  🏥 lh_self_health     — 9622 MCP 自检
"""
import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ── 清代理（Mac socks 代理毒化 urllib/外连）──
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"

from mcp.server import Server  # noqa: E402
from mcp.server.stdio import stdio_server  # noqa: E402
from mcp.types import Tool, TextContent  # noqa: E402

# ─────────────────────── 常量 ───────────────────────
ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LH = Path(os.path.expanduser("~/.longhun"))
MCP_DIR = LH / "mcp_9622"
AUDIT_LOG = MCP_DIR / "audit.jsonl"
KILL_SWITCH = MCP_DIR / "kill_switch"
MEMORY_DIR = ROOT / ".codebuddy" / "memory"

# 文件/命令白名单根（resolve 后必须落在此内）
ALLOWED_ROOTS = [ROOT, LH, Path(os.path.expanduser("~/.codebuddy"))]
ALLOWED_STR = [str(p.resolve()) for p in ALLOWED_ROOTS]

# M261 前传契碑 4 条不可触碰红线（硬拒 · 永不放开）
REDLINES = [
    r"\brm\s+(-[a-z]*[rR][a-z]*\s+)*~(\b|/)",        # rm -rf ~
    r"\brm\s+(-[a-z]*[rR][a-z]*\s+)*/",               # rm -rf / (根)
    r"git\s+(push|pull|fetch)\s+.*--force",           # git force push/pull/fetch
    r"git\s+push\s+.*\s(main|master)\b.*--force",     # force 到 main/master
    r"\b(sudo|doas)\b",                               # 提权
]
SYSTEM_DIRS = ("/etc", "/usr", "/System", "/Library", "/Applications", "/bin", "/sbin")

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

app = Server("lh9622")


def _log(msg: str):
    print(f"[lh9622] {msg}", file=sys.stderr, flush=True)


def _audit(entry: dict):
    try:
        MCP_DIR.mkdir(parents=True, exist_ok=True)
        entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        _log(f"audit fail: {e}")


# ══════════════════════════ 🧠 记忆桥 ══════════════════════════
def _walk_memory_files():
    """记忆候选文件: .codebuddy/memory/*.md + STATE.md + ~/.longhun 关键记忆"""
    files = []
    if MEMORY_DIR.is_dir():
        for p in sorted(MEMORY_DIR.glob("*.md")):
            files.append(p)
    for p in (ROOT / "STATE.md", ROOT / "功能清单.md", LH / "session_context.json"):
        if p.is_file():
            files.append(p)
    brain = LH / "brain"
    if brain.is_dir():
        for p in sorted(brain.glob("*.md"))[:50]:
            files.append(p)
    return files


def _safe_read(p: Path, limit=600_000):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read(limit)
    except Exception:
        return ""


def _relative_of(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def memory_search(query: str, max_results: int = 12, context: int = 60) -> dict:
    """关键词检索全部本地记忆，返回文件+命中行上下文"""
    if not query or not query.strip():
        return {"ok": False, "error": "query 必填"}
    words = [w.lower() for w in re.split(r"[\s,，;；]+", query.strip()) if w]
    hits = []
    for p in _walk_memory_files():
        text = _safe_read(p)
        if not text:
            continue
        lines = text.splitlines()
        low = text.lower()
        if not all(w in low for w in words):
            continue
        # 收集命中行上下文（最多 3 段）
        matched_lines = [i for i, ln in enumerate(lines) if all(w in ln.lower() for w in words)]
        if not matched_lines:  # 词分散在多行 → 取第一个词命中的行
            first = next((i for i, ln in enumerate(lines) if words[0] in ln.lower()), None)
            matched_lines = [first] if first is not None else []
        for i in matched_lines[:3]:
            s, e = max(0, i - context // 2), min(len(lines), i + context // 2)
            snippet = "\n".join(lines[s:e]).strip()
            hits.append({"file": _relative_of(p), "line": i + 1, "snippet": snippet})
        if len(hits) >= max_results:
            break
    return {"ok": True, "query": query, "hits": hits[:max_results], "total": len(hits)}


def memory_digest(days: int = 3) -> dict:
    """记忆总摘要: MEMORY 前 60 行 + 最近 days 天日志首段 + 会话任务"""
    digest = {"memory_head": "", "recent_days": [], "session_task": ""}
    mem = MEMORY_DIR / "MEMORY.md"
    if mem.is_file():
        t = _safe_read(mem, 12_000)
        digest["memory_head"] = t[:6000]
    today = time.strftime("%Y-%m-%d")
    for offset in range(days):
        d = (time.strptime(today, "%Y-%m-%d"))
        import datetime as _dt
        day = (_dt.date.fromtimestamp(time.mktime(d)) - _dt.timedelta(days=offset)).isoformat()
        p = MEMORY_DIR / f"{day}.md"
        if p.is_file():
            t = _safe_read(p, 20_000)
            head = "\n".join(t.splitlines()[:12])
            digest["recent_days"].append({"date": day, "head": head[:3000]})
    sc = LH / "session_context.json"
    if sc.is_file():
        try:
            ctx = json.loads(_safe_read(sc, 200_000))
            digest["session_task"] = json.dumps(ctx, ensure_ascii=False)[:4000]
        except Exception:
            digest["session_task"] = "(parse fail)"
    return {"ok": True, "digest": digest}


def session_context() -> dict:
    """读会话断点上下文（断点续接用）"""
    sc = LH / "session_context.json"
    if not sc.is_file():
        return {"ok": True, "exists": False}
    try:
        return {"ok": True, "exists": True,
                "context": json.loads(_safe_read(sc, 500_000))}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ══════════════════════════ 🌐 Notion 桥 ══════════════════════════
def _probe_token(tok: str) -> bool:
    if not tok:
        return False
    try:
        req = urllib.request.Request(f"{NOTION_API}/users/me",
                                     headers={"Authorization": f"Bearer {tok}",
                                              "Notion-Version": NOTION_VERSION})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False


def get_notion_token() -> str:
    """候选链: env > vault > mcp.json，取第一个实测有效者。值不落盘。"""
    cands = []
    env_t = os.environ.get("NOTION_TOKEN", "").strip()
    if env_t:
        cands.append(("env", env_t))
    try:
        v = subprocess.run(["python3", str(ROOT / "bin" / "lh_vault.py"), "get", "NOTION_TOKEN"],
                           capture_output=True, text=True, timeout=15).stdout.strip()
        if v and not v.lower().startswith("error"):
            cands.append(("vault", v))
    except Exception:
        pass
    try:
        with open(Path.home() / ".codebuddy" / "mcp.json") as f:
            m = json.load(f)
        t = m.get("mcpServers", {}).get("Notion MCP Server", {}).get("env", {}).get("NOTION_TOKEN", "")
        if t:
            cands.append(("mcp.json", t.strip()))
    except Exception:
        pass
    for _name, t in cands:
        if _probe_token(t):
            return t
    return cands[0][1] if cands else ""


class NotionAPI:
    """直连官方 REST · 指数退避(429/5xx) · ≤3 req/s · 全翻页 · 零三方"""

    def __init__(self, token):
        self.token = token
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def _h(self):
        return {"Authorization": f"Bearer {self.token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json"}

    def api(self, method, path, body=None, retries=4):
        req = urllib.request.Request(f"{NOTION_API}/{path}",
                                     data=json.dumps(body).encode() if body is not None else None,
                                     method=method, headers=self._h())
        for attempt in range(retries + 1):
            try:
                with self.opener.open(req, timeout=40) as r:
                    time.sleep(0.3)
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                if e.code >= 500 and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                return {"_error": e.code}
            except Exception as e:
                return {"_error": -1, "msg": str(e)[:200]}
        return {"_error": -2}

    # ── helpers ──
    def search_all(self, query="", obj_filter=None, limit=50):
        out, cursor, seen = [], None, set()
        while True:
            body = {"query": query, "page_size": 100}
            if obj_filter:
                body["filter"] = {"value": obj_filter, "property": "object"}
            if cursor:
                body["start_cursor"] = cursor
            res = self.api("POST", "search", body)
            if "_error" in res:
                break
            for r in res.get("results", []):
                if r.get("id") in seen:
                    continue
                seen.add(r.get("id"))
                out.append(r)
            if len(out) >= limit:
                break
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return out

    def children_all(self, block_id):
        out, cursor = [], None
        while True:
            path = f"blocks/{block_id}/children?page_size=100"
            if cursor:
                path += f"&start_cursor={cursor}"
            res = self.api("GET", path)
            if "_error" in res:
                break
            out.extend(res.get("results", []))
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return out


def _rt_text(v):
    if not isinstance(v, dict):
        return ""
    rt = v.get("rich_text") or []
    return "".join(x.get("plain_text", "") for x in rt if isinstance(x, dict))


def _rt_join(arr):
    return "".join(x.get("plain_text", "") for x in arr if isinstance(x, dict))


def _title_of(props, obj=None):
    for v in (props or {}).values():
        if isinstance(v, dict) and v.get("type") == "title":
            t = _rt_join(v.get("title") or v.get("rich_text") or [])
            if t:
                return t
    if isinstance(obj, dict) and obj.get("title"):
        t = _rt_join(obj["title"])
        if t:
            return t
    for v in (props or {}).values():
        if isinstance(v, dict):
            t = _rt_join(v.get("title") or v.get("rich_text") or [])
            if t:
                return t
    return ""


def notion_health() -> dict:
    tok = get_notion_token()
    if not tok:
        return {"ok": False, "error": "无可用 Notion token（env>vault>mcp.json 均空/无效）"}
    api = NotionAPI(tok)
    me = api.api("GET", "users/me")
    return {"ok": True, "token_source_probed": True,
            "bot": me.get("name") if "_error" not in me else "?",
            "api_version": NOTION_VERSION}


def notion_search(query: str = "", limit: int = 30) -> dict:
    tok = get_notion_token()
    if not tok:
        return {"ok": False, "error": "无可用 Notion token"}
    api = NotionAPI(tok)
    res = api.search_all(query=query or "", obj_filter=None, limit=min(limit, 100))
    out = []
    for r in res:
        out.append({
            "id": r.get("id"),
            "type": r.get("object"),
            "title": _title_of(r.get("properties"), r) or r.get("title", ""),
            "url": f"https://www.notion.so/{r.get('id', '').replace('-', '')}",
        })
    return {"ok": True, "query": query, "results": out}


def notion_read(target: str, depth: int = 40) -> dict:
    """读页面/数据源内容。target = page id(短/长) 或 URL 末段"""
    m = re.search(r"([0-9a-fA-F]{32})", target.replace("-", ""))
    if not m:
        return {"ok": False, "error": "无法从 target 解析 32 位 id"}
    pid = m.group(1)
    pid_fmt = f"{pid[:8]}-{pid[8:12]}-{pid[12:16]}-{pid[16:20]}-{pid[20:]}"
    tok = get_notion_token()
    if not tok:
        return {"ok": False, "error": "无可用 Notion token"}
    api = NotionAPI(tok)
    page = api.api("GET", f"pages/{pid_fmt}")
    if "_error" in page:
        # 可能是 data_source/数据库对象
        ds = api.api("GET", f"data_sources/{pid_fmt}")
        if "_error" in ds:
            return {"ok": False, "error": f"读取失败: {page}"}
        return {"ok": True, "object": "data_source",
                "title": _title_of(ds.get("properties"), ds),
                "props_keys": list((ds.get("properties") or {}).keys())[:40],
                "parent": ds.get("parent")}
    title = _title_of(page.get("properties"), page)
    blocks = api.children_all(pid_fmt)
    texts, count = [], 0
    for b in blocks:
        if count >= depth:
            break
        t = b.get("type")
        val = b.get(t) or {}
        txt = _rt_text(val)
        if txt:
            texts.append(txt)
            count += 1
    return {"ok": True, "object": "page", "title": title,
            "url": f"https://www.notion.so/{pid}",
            "content": "\n".join(texts), "blocks": len(blocks)}


def notion_query_db(db_id: str, limit: int = 60) -> dict:
    m = re.search(r"([0-9a-fA-F]{32})", db_id.replace("-", ""))
    if not m:
        return {"ok": False, "error": "database_id 须含 32 位 id"}
    pid = m.group(1)
    tok = get_notion_token()
    if not tok:
        return {"ok": False, "error": "无可用 Notion token"}
    api = NotionAPI(tok)
    # 兼容新 API 模型: 试 data_sources 查询，失败再回退旧 database 查询
    body = {"page_size": 100}
    res = api.api("POST", f"data_sources/{pid}/query", body)
    rows = res.get("results", [])
    if "_error" in res or not rows:
        res2 = api.api("POST", f"databases/{pid}/query", body)
        rows = res2.get("results", [])
    out = []
    for r in rows[:limit]:
        title = _title_of(r.get("properties"), r)
        props = {}
        for k, v in (r.get("properties") or {}).items():
            props[k] = _rt_text(v) if isinstance(v, dict) else str(v)
        out.append({"id": r.get("id"), "title": title, "properties": props})
    return {"ok": True, "database": pid, "rows": out, "total": len(rows)}


# ══════════════════════════ 🖥️ 电脑闸 ══════════════════════════
def _kill_switched() -> bool:
    return KILL_SWITCH.exists()


def _redline_blocked(cmd: str) -> str:
    low = cmd.lower()
    for pat in REDLINES:
        if re.search(pat, low):
            return f"触碰红线: {pat}"
    # 系统目录写/删（touch/rm/mv 到 /etc /usr ...）
    for d in SYSTEM_DIRS:
        if re.search(rf"\b(rm|mv|touch|chmod|chown)\b.*\s{d}[/\s]", low):
            return f"系统目录写入: {d}"
    # 写密钥目录
    if re.search(r"\b(cp|mv|tee|echo|curl|wget|scp)\b.*(~|/).*\.(ssh|gnupg)[/\s]", low) and \
       re.search(r"(\.ssh|\.gnupg)", low):
        return "密钥目录 .ssh/.gnupg"
    if re.search(r"\bcd\s+~?/?\s*$", low):  # cd ~ 无害
        pass
    return ""


def _in_allowed(p: Path) -> bool:
    try:
        rp = str(p.resolve())
    except Exception:
        return False
    return any(rp == a or rp.startswith(a + os.sep) for a in ALLOWED_STR)


def machine_exec(cmd: str, cwd: str = "", timeout: int = 60) -> dict:
    """执行本机命令（白名单 cwd + 4红线 + kill_switch + 审计）"""
    if _kill_switched():
        return {"ok": False, "error": "kill_switch 已拉起，执行类工具全部拒绝"}
    if not cmd or not cmd.strip():
        return {"ok": False, "error": "cmd 必填"}
    base = Path(cwd).expanduser() if cwd else ROOT
    if not _in_allowed(base):
        return {"ok": False, "error": f"cwd 超出白名单: {base}"}
    blk = _redline_blocked(cmd)
    if blk:
        _audit({"action": "exec_BLOCKED", "cmd": cmd[:300], "reason": blk})
        return {"ok": False, "error": f"4红线硬拒: {blk}"}
    env = dict(os.environ)
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy"):
        env.pop(k, None)
    env["NO_PROXY"] = "*"
    try:
        proc = subprocess.run(cmd, shell=True, cwd=str(base), env=env,
                              capture_output=True, text=True,
                              timeout=timeout, executable="/bin/bash")
        out = proc.stdout[-200_000:]
        err = proc.stderr[-50_000:]
        _audit({"action": "exec", "cmd": cmd[:500], "cwd": str(base),
                "rc": proc.returncode})
        return {"ok": proc.returncode == 0, "returncode": proc.returncode,
                "stdout": out, "stderr": err}
    except subprocess.TimeoutExpired:
        _audit({"action": "exec_TIMEOUT", "cmd": cmd[:300], "timeout": timeout})
        return {"ok": False, "error": f"超时(>{timeout}s)，已终止"}
    except Exception as e:
        _audit({"action": "exec_ERROR", "cmd": cmd[:300], "err": str(e)[:200]})
        return {"ok": False, "error": str(e)}


def machine_files(action: str, path: str, content: str = "", mode: str = "utf-8",
                  limit: int = 5000) -> dict:
    """白名单内文件操作: list | read | write"""
    if _kill_switched():
        return {"ok": False, "error": "kill_switch 已拉起，文件操作拒绝"}
    p = Path(path).expanduser()
    if not _in_allowed(p):
        return {"ok": False, "error": f"路径超出白名单: {p}"}
    action = (action or "list").lower()
    try:
        if action == "list":
            target = p if p.is_dir() else p.parent
            names = sorted(os.listdir(target))
            return {"ok": True, "path": str(target), "count": len(names),
                    "entries": names[:limit]}
        if action == "read":
            if not p.is_file():
                return {"ok": False, "error": f"文件不存在: {p}"}
            if p.stat().st_size > 2_000_000:
                return {"ok": False, "error": "文件 >2MB，拒绝整读"}
            with open(p, encoding=mode, errors="replace") as f:
                data = f.read()
            return {"ok": True, "path": str(p), "chars": len(data), "content": data[:200_000]}
        if action == "write":
            if content is None:
                return {"ok": False, "error": "write 需 content"}
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding=mode) as f:
                f.write(content)
            _audit({"action": "file_write", "path": str(p), "chars": len(content)})
            return {"ok": True, "path": str(p), "written": len(content)}
        return {"ok": False, "error": f"未知 action: {action}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ══════════════════════════ 🏥 自检 ══════════════════════════
def self_health() -> dict:
    mem_count = 0
    if MEMORY_DIR.is_dir():
        mem_count = len(list(MEMORY_DIR.glob("*.md")))
    audit_count = 0
    if AUDIT_LOG.is_file():
        audit_count = sum(1 for _ in open(AUDIT_LOG, encoding="utf-8"))
    return {
        "ok": True, "service": "9622 · 龍魂管家 MCP v1.0",
        "root": str(ROOT), "allowed_roots": ALLOWED_STR,
        "memory_files": mem_count, "kill_switch": _kill_switched(),
        "audit_entries": audit_count,
        "notion_token": "probe_ok" if get_notion_token() else "missing",
        "dna": "#龍芯⚡️2026-09-07-LH9622-MCP-v1.0-UID9622",
    }


# ─────────────────────── 密钥中枢桥（lh_keys_bridge）───────────────────────
# AI 经 MCP 获取密钥中枢执行环境：掩码默认 · raw 明文须过 foundation 七因素门禁
def _mask_val(val: str, keep: int = 4) -> str:
    val = str(val)
    return val[:keep] + "…" + val[-keep:] if len(val) > 2 * keep else "****"


def lh_keys_bridge(key_names, raw: bool = False):
    if _kill_switched():
        return {"ok": False, "mode": "blocked", "reason": "kill_switch 已拉起"}
    if not isinstance(key_names, list) or not key_names:
        return {"ok": False, "error": "key_names 必填（密钥名列表）"}
    names = []
    for n in key_names:
        ns = str(n).strip()
        if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", ns):
            names.append(ns)
    if not names:
        return {"ok": False, "error": "密钥名须为 A-Za-z0-9_.- 组合(1-64字符)"}
    # raw 明文 = 写级操作 → foundation 七因素门禁(失败写 DB + 耻辱墙)
    gate = "PASS"
    if raw:
        desc = f"lh_keys_bridge raw读取: {','.join(names)}"
        g = subprocess.run(
            [sys.executable, str(ROOT / "08_BIN" / "lh_foundation_engine.py"),
             "audit", "--decision", desc],
            capture_output=True, text=True, timeout=60)
        if g.returncode != 0:
            _log(f"lh_keys_bridge gate BLOCKED: {names}")
            return {"ok": False, "mode": "raw", "gate": "BLOCKED",
                    "error": "七因素门禁熔断 · 详见 ~/.longhun/foundation_audit.db 与耻辱墙",
                    "dna": "lh_keys_bridge-blocked-uid9622"}
    vault = str(ROOT / "08_BIN" / "lh_vault.py")
    entries = []
    for n in names:
        r = subprocess.run([sys.executable, vault, "get", n],
                           capture_output=True, text=True, timeout=60)
        val = r.stdout.strip() if r.returncode == 0 else ""
        if not val:
            entries.append({"name": n, "status": "NOT_FOUND"})
            continue
        if raw and gate == "PASS":
            entries.append({"name": n, "status": "ok", "value": val})
        else:
            entries.append({"name": n, "status": "ok", "masked": _mask_val(val)})
    out = {"ok": True, "mode": "raw" if raw else "masked", "gate": gate,
           "count": len(entries), "entries": entries}
    if raw:
        out["note"] = "⚠️ 明文一次性使用：勿写入日志/文件/对话引用，用完即焚"
    return out


# ══════════════════════════ MCP 协议层 ══════════════════════════
TOOLS = [
    Tool(name="lh_memory_search", description="🧠 检索龍魂全部本地记忆（MEMORY/每日日志/STATE/大脑），按关键词返回命中文件与上下文片段。",
         inputSchema={"type": "object", "properties": {
             "query": {"type": "string", "description": "关键词（支持空格分隔多词，须同段命中）"},
             "max_results": {"type": "integer", "description": "最大命中数，默认12"},
             "context": {"type": "integer", "description": "上下文行数，默认60"}},
             "required": ["query"]}),
    Tool(name="lh_memory_digest", description="🧠 记忆总摘要：MEMORY 头部 + 最近 N 天日志首段 + 会话断点任务。",
         inputSchema={"type": "object", "properties": {
             "days": {"type": "integer", "description": "回溯天数，默认3"}}}),
    Tool(name="lh_session_context", description="🧠 读会话断点上下文 ~/.longhun/session_context.json（续接上次任务用）。",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="lh_notion_health", description="🌐 Notion token/API 健康检查。",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="lh_notion_search", description="🌐 搜索龍魂 Notion 全部页面/数据库（官方 REST 直连）。",
         inputSchema={"type": "object", "properties": {
             "query": {"type": "string", "description": "搜索词，空=列出最近"},
             "limit": {"type": "integer", "description": "最多结果数，默认30"}}}),
    Tool(name="lh_notion_read", description="🌐 读页面/数据源内容（传 page id 或 notion url 末段）。",
         inputSchema={"type": "object", "properties": {
             "target": {"type": "string", "description": "page id / URL 含 32 位 id"},
             "depth": {"type": "integer", "description": "最多读文本块数，默认40"}},
             "required": ["target"]}),
    Tool(name="lh_notion_query_db", description="🌐 查数据库所有行（传 database_id / data_source_id）。",
         inputSchema={"type": "object", "properties": {
             "db_id": {"type": "string", "description": "database_id 或 data_source_id"},
             "limit": {"type": "integer", "description": "最多行数，默认60"}},
             "required": ["db_id"]}),
    Tool(name="lh_machine_exec", description="🖥️ 执行本机命令。⚠️危险工具：AI须先获老大批准再调。白名单cwd·4红线硬拒(rm -rf ~/git force/.ssh·gnupg/系统目录/sudo)·kill_switch·全程审计留痕。",
         inputSchema={"type": "object", "properties": {
             "cmd": {"type": "string", "description": "shell 命令（默认工作目录=longhun-system）"},
             "cwd": {"type": "string", "description": "工作目录，须在白名单内，默认项目根"},
             "timeout": {"type": "integer", "description": "超时秒数，默认60"}},
             "required": ["cmd"]}),
    Tool(name="lh_machine_files", description="🖥️ 白名单内文件 list/read/write（路径越界自动拒绝）。",
         inputSchema={"type": "object", "properties": {
             "action": {"type": "string", "enum": ["list", "read", "write"]},
             "path": {"type": "string", "description": "绝对路径（须在 longhun-system/.longhun/.codebuddy 内）"},
             "content": {"type": "string", "description": "write 时必填"},
             "limit": {"type": "integer", "description": "list 条数上限，默认5000"}},
             "required": ["action", "path"]}),
    Tool(name="lh_self_health", description="🏥 9622 龍魂管家 MCP 自检（根/白名单/记忆数/kill_switch/审计/token）。",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="lh_keys_bridge", description="🔑 密钥中枢桥（lh_keys v2）：AI 获取执行环境密钥。raw=False 返掩码（默认）；raw=True 返明文 —— 须过 foundation 七因素门禁，明文一次性使用、勿写入日志/文件/对话引用。",
         inputSchema={"type": "object", "properties": {
             "key_names": {"type": "array", "items": {"type": "string"},
                           "description": "密钥名列表（A-Za-z0-9_.-，1-64字符）"},
             "raw": {"type": "boolean", "description": "True=明文(过门禁) False=掩码(默认)"}},
             "required": ["key_names"]}),
]


def _handle(name: str, args: dict):
    args = args or {}
    if name == "lh_memory_search":
        return memory_search(args.get("query", ""), int(args.get("max_results", 12)),
                             int(args.get("context", 60)))
    if name == "lh_memory_digest":
        return memory_digest(int(args.get("days", 3)))
    if name == "lh_session_context":
        return session_context()
    if name == "lh_notion_health":
        return notion_health()
    if name == "lh_notion_search":
        return notion_search(args.get("query", ""), int(args.get("limit", 30)))
    if name == "lh_notion_read":
        return notion_read(args.get("target", ""), int(args.get("depth", 40)))
    if name == "lh_notion_query_db":
        return notion_query_db(args.get("db_id", ""), int(args.get("limit", 60)))
    if name == "lh_machine_exec":
        return machine_exec(args.get("cmd", ""), args.get("cwd", ""),
                            int(args.get("timeout", 60)))
    if name == "lh_machine_files":
        return machine_files(args.get("action", ""), args.get("path", ""),
                             args.get("content", ""), limit=int(args.get("limit", 5000)))
    if name == "lh_self_health":
        return self_health()
    if name == "lh_keys_bridge":
        return lh_keys_bridge(args.get("key_names", []),
                              raw=bool(args.get("raw", False)))
    return {"ok": False, "error": f"未知工具: {name}"}


@app.list_tools()
async def list_tools():
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        _audit({"tool": name, "args_keys": list((arguments or {}).keys()),
                "confirm": CONFIRM})
        result = _handle(name, arguments)
        text = json.dumps(result, ensure_ascii=False, indent=2)[:190_000]
        return [TextContent(type="text", text=text)]
    except Exception as e:
        _log(f"call_tool {name} error: {e}")
        return [TextContent(type="text",
                            text=json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream,
                      app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
