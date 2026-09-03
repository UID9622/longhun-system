#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-03-FORK-TRACKER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂 GitHub fork 追踪引擎 v1.0
# 目标: 一眼看清 UID9622/longhun-system 被谁 fork 了、有没有新 fork。
#       list=全量快照; check=对比上次缓存(~/.longhun/fork_cache.json)报增量并刷新缓存。
#       fork 是社区触达的入口信号——fork 了新面孔，社区响应模板第一条就有人可回复。
#
# 用法:
#   python3 08_BIN/lh_fork_tracker.py list [--json]
#   python3 08_BIN/lh_fork_tracker.py check [--json]
#   (经 lh:  lh fork list / lh fork check)
#
# 设计铁律:
#   - 零三方依赖(标准库 urllib); 公开 fork 列表匿名可读，带 token 则提高速率上限
#   - token 读取序: --token > GH_TOKEN/GITHUB_TOKEN > lh_vault github-pat > Keychain > mcp.json
#   - token 只读不落盘、绝不打印明文(一律 _mask); 缓存只存 full_name 清单，不含任何敏感信息
#   - 代理注意: urllib 不认 socks5h:// 代理 scheme → 默认强制直连(实测 api.github.com 可直连)
#   - 网络失败如实标一行原因并退出，不自动重试(节能协议 v1.1)
#   - exit: 0=🟢成功 / 2=🔴网络或 API 失败
#
# A-BOM 算法物料清单（算法审计协议 v1.0 备案）:
#   - 目标函数: 拉取公开 fork 元数据 → 输出列表或与上次快照做差集(新增/消失)
#   - 输入特征: GitHub REST /repos/{owner}/{repo}/forks (owner=UID9622 repo=longhun-system)
#   - 用户影响: 只读公开数据与本地缓存，不改任何远端状态; fork 增量仅作社区触达提示
#   - 申诉通道: UID9622（诸葛鑫）· GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F

import sys
import os
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent          # longhun-system/
GITHUB_API = "https://api.github.com"
UA = "LongHun-LH-CLI/1.0 (UID9622; fork tracker)"
TIMEOUT = 10
OWNER = "UID9622"
REPO = "longhun-system"
CACHE = Path.home() / ".longhun" / "fork_cache.json"
FINE_PREFIX = "github_pat_"
CLASSIC_PREFIX = "ghp_"
OAUTH_PREFIX = "gho_"

PROXY = None  # 可选 http 代理 (--proxy)，默认直连


# ── token 探测(按序找第一个可用，不打印明文) ─────────────────
def _mask(tok: str) -> str:
    if not tok:
        return "(无)"
    head = tok[:9]
    tail = tok[-4:] if len(tok) > 4 else "????"
    return f"{head}…{tail}"


def _try_vault():
    """python3 08_BIN/lh_vault.py get github-pat → 捕获 stdout 末行 token 特征"""
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "08_BIN" / "lh_vault.py"), "get", "github-pat"],
            capture_output=True, text=True, timeout=8,
        )
        if r.returncode != 0:
            return None
        for line in reversed((r.stdout or "").splitlines()):
            line = line.strip()
            if any(line.startswith(p) for p in (CLASSIC_PREFIX, FINE_PREFIX, OAUTH_PREFIX)):
                return line
    except Exception:
        pass
    return None


def _try_keychain():
    """Keychain service=github.com account=UID9622 (git 推送同一把)"""
    try:
        r = subprocess.run(
            ["security", "find-internet-password", "-s", "github.com", "-a", "UID9622", "-w"],
            capture_output=True, text=True, timeout=8,
        )
        if r.returncode == 0 and r.stdout:
            return r.stdout.strip()
    except Exception:
        pass
    return None


def _try_mcp():
    """扫描 ~/.codebuddy/mcp.json 与 {root}/.codebuddy/mcp.json 的 GitHub server token"""
    cands = [Path.home() / ".codebuddy" / "mcp.json", ROOT / ".codebuddy" / "mcp.json"]
    for p in cands:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        servers = data.get("mcpServers") or {}
        for srv in servers.values():
            env = srv.get("env") or {}
            for key in ("GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN"):
                val = env.get(key)
                if val and any(val.startswith(p) for p in (CLASSIC_PREFIX, FINE_PREFIX, OAUTH_PREFIX)):
                    return val
    return None


def load_token(cli_token=None):
    """返回 (token, source)。顺序: --token > env > vault > Keychain > mcp.json"""
    if cli_token:
        return cli_token, "--token 参数"
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        val = os.environ.get(var)
        if val and val.startswith((CLASSIC_PREFIX, FINE_PREFIX, OAUTH_PREFIX)):
            return val, f"环境变量 {var}"
    val = _try_vault()
    if val:
        return val, "lh_vault get github-pat"
    val = _try_keychain()
    if val:
        return val, "Keychain(github.com/UID9622)"
    val = _try_mcp()
    if val:
        return val, ".codebuddy/mcp.json(GitHub server)"
    return None, None


# ── GitHub API 调用(urllib 直连·不认 socks5h 代理) ───────────
def gh_request(token, path: str):
    """返回 (status_code, json_body, headers)。匿名时 token=None。"""
    url = GITHUB_API + path
    headers = {
        "User-Agent": UA,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    if PROXY:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    else:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 忽略环境 socks 代理
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
            except Exception:
                payload = {}
            return resp.status, payload, resp.headers
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8")) if e.fp else {}
        except Exception:
            payload = {}
        return e.code, payload, e.headers
    except Exception as e:
        return 0, {"_err": str(e)}, {}


# ── fork 数据 ─────────────────────────────────────────────────
def fetch_forks(token):
    """拉取全部公开 fork(分页 per_page=100)。返回 (forks_list|None, status, err_str)。"""
    forks = []
    page = 1
    while True:
        path = f"/repos/{OWNER}/{REPO}/forks?per_page=100&page={page}"
        st, body, _ = gh_request(token, path)
        if st != 200:
            err = body.get("_err", "")
            msg = body.get("message", "") if isinstance(body, dict) else ""
            detail = f"HTTP {st}"
            if msg:
                detail += f" · {msg}"
            if err:
                detail += f" · {err}"
            return None, st, detail
        if not isinstance(body, list):
            return None, st, "响应非列表(疑似 API 限流或数据格式异常)"
        forks.extend(body)
        if len(body) < 100:
            break
        page += 1
        if page > 10:  # 保险丝: 最多拉 1000 个，足够任何真实规模
            break
    return forks, 200, ""


def _simplify(fork_item):
    """fork 元数据 → 展示字段(owner 取 login)"""
    owner = (fork_item.get("owner") or {}).get("login", "?")
    return {
        "owner": owner,
        "full_name": fork_item.get("full_name") or f"{owner}/{REPO}",
        "created_at": fork_item.get("created_at") or "",
        "pushed_at": fork_item.get("pushed_at") or "",
        "private": bool(fork_item.get("private")),
    }


# ── 时间戳(调龍魂时间引擎·失败降级 ISO) ─────────────────────
def _stamp() -> str:
    """🐉 干支·卦·三色 时间戳。lh_time_engine 依赖 requests，失败时降级 ISO，绝不阻塞本工具。"""
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "bin" / "lh_time_engine.py"), "--stamp-simple"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0 and (r.stdout or "").strip():
            return r.stdout.strip()
    except Exception:
        pass
    return datetime.now().astimezone().isoformat()


# ── list: 全量 fork 快照 ──────────────────────────────────────
def cmd_list(token, source, as_json: bool) -> int:
    forks, st, err = fetch_forks(token)
    if forks is None:
        msg = {"status": "error", "color": "🔴",
               "detail": f"拉取 fork 列表失败 {err}（不重试·可稍后手动再跑）"}
        if as_json:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
        else:
            print(f"{msg['color']} {msg['detail']}")
        return 2

    rows = [_simplify(f) for f in forks]
    pub = [r for r in rows if not r["private"]]
    if as_json:
        payload = {
            "repo": f"{OWNER}/{REPO}", "total": len(rows),
            "public": len(pub), "private": len(rows) - len(pub),
            "token_source": source, "forks": rows, "stamp": _stamp(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if token and source:
            print(f"🗂️ token 来源: {source}（掩码 {_mask(token)}）")
        print(f"🍴 {OWNER}/{REPO} 全部 fork · {len(rows)} 个（public {len(pub)} · private {len(rows) - len(pub)}）")
        for i, r in enumerate(rows, 1):
            vis = "🌐 public" if not r["private"] else "🔒 private"
            print(f"[{i:>3}] {r['full_name']:<48} created={r['created_at'][:10]} pushed={r['pushed_at'][:10]} {vis}")
        print(_stamp())
    return 0


# ── check: 对比缓存增量并刷新 ────────────────────────────────
def _read_cache():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception:
        return None


def cmd_check(token, source, as_json: bool) -> int:
    forks, st, err = fetch_forks(token)
    if forks is None:
        msg = {"status": "error", "color": "🔴",
               "detail": f"拉取 fork 列表失败 {err}（不重试·可稍后手动再跑）"}
        if as_json:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
        else:
            print(f"{msg['color']} {msg['detail']}")
        return 2

    current = sorted({_simplify(f)["full_name"] for f in forks})
    now = datetime.now().astimezone().isoformat()
    old = _read_cache()
    old_names = set(old.get("forks") or []) if isinstance(old, dict) else set()

    new_found = [n for n in current if n not in old_names]
    disappeared = [n for n in old_names if n not in current]

    # 刷新缓存(只存 full_name·不含敏感信息)
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps({"fetched_at": now, "forks": current},
                                    ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        # 缓存写失败不算 API 失败，如实告知但继续
        print(f"⚠️ 缓存写入失败: {e}", file=sys.stderr)

    if as_json:
        payload = {
            "repo": f"{OWNER}/{REPO}", "fetched_at": now,
            "total": len(current),
            "new_forks": new_found,
            "disappeared": disappeared,
            "cache_updated": True, "stamp": _stamp(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not old:
            print(f"🍴 首次检查无历史缓存，本次 {len(current)} 个 fork 已建基线。")
        elif new_found:
            print(f"🍴 发现 {len(new_found)} 个新 fork:")
            for n in new_found:
                print(f"  ✨ {n}")
            if disappeared:
                print(f"   （另 {len(disappeared)} 个不在本次列表: {', '.join(disappeared)}——可能已删除或转私有）")
        else:
            print(f"🍴 无新 fork（仍 {len(current)} 个）。")
            if disappeared:
                print(f"   （{len(disappeared)} 个不在本次列表: {', '.join(disappeared)}——可能已删除或转私有）")
        print(f"🗂️ 缓存已更新: {CACHE}")
        print(_stamp())
    return 0


def usage():
    print(f"""龍魂 GitHub fork 追踪引擎 v1.0
用法:
  lh fork list [--json]     → 列出 {OWNER}/{REPO} 全部 fork（owner/full_name/created/pushed/private）
  lh fork check [--json]    → 对比上次缓存(~/.longhun/fork_cache.json)·报新 fork·刷新缓存
token 读取顺序: --token > GH_TOKEN/GITHUB_TOKEN > lh_vault github-pat > Keychain > mcp.json
（公开 fork 列表匿名可读; 带 token 提高速率上限·token 只读不落盘不打印明文）
代理: 默认直连(urllib 不认 socks5h); 需走 http 代理用 --proxy http://127.0.0.1:PORT""")


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        usage()
        return 1
    cmd = argv[0]
    rest = argv[1:]
    global PROXY
    as_json = "--json" in rest
    cli_token = None
    i = 0
    while i < len(rest):
        a = rest[i]
        if a in ("--json",):
            pass
        elif a == "--token" and i + 1 < len(rest):
            cli_token = rest[i + 1]
            i += 1
        elif a == "--proxy" and i + 1 < len(rest):
            PROXY = rest[i + 1]
            i += 1
        i += 1
    token, source = load_token(cli_token)
    if cmd == "list":
        return cmd_list(token, source, as_json)
    if cmd == "check":
        return cmd_check(token, source, as_json)
    print(f"❓ 未知子命令: {cmd}")
    usage()
    return 1


if __name__ == "__main__":
    sys.exit(main())
