#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-03-GITHUB-PERMS-TOOL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂 GitHub 权限自检工具 v1.0
# 目标: 社区联动(第三方仓库发评论/PR)前先检后发——测当前 PAT 权限状态，
#       缺什么直接告诉缺什么、怎么补（docs/github-pat-setup-guide.md），不再卡住等指示。
#
# 用法:
#   python3 bin/lh_github_perms.py test-perms [--repo owner/repo ...] [--json] [--token xxx]
#   python3 bin/lh_github_perms.py token-hint [--json] [--token xxx]
#   (经 lh:  lh github test-perms / lh github token-hint)
#
# 设计铁律:
#   - 只读取本地 token 配置(env → vault → Keychain → mcp.json)，不存储任何敏感信息
#   - 任何输出路径绝不打印 token 明文，一律掩码(前缀+尾4位)
#   - 零三方依赖(标准库 urllib)，静态判定不了的如实标 🟡 不编造
#   - exit: 0=🟢可发 / 1=🟡缺权限待补 / 2=🔴token不可用或网络错

import sys
import os
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # longhun-system/
GITHUB_API = "https://api.github.com"
UA = "LongHun-LH-CLI/1.0 (UID9622; github perms selfcheck)"  # HTTP 头必须 ASCII，禁止中文
TIMEOUT = 10
# 目标仓库默认 = DeepSeek Issue #1622 所在仓库
DEFAULT_REPOS = ["deepseek-ai/DeepSeek-V3"]
GUIDE = "docs/github-pat-setup-guide.md"
FINE_PREFIX = "github_pat_"
CLASSIC_PREFIX = "ghp_"
OAUTH_PREFIX = "gho_"

# ── token 探测(按序找第一个可用，不打印明文) ─────────────────
def _mask(tok: str) -> str:
    if not tok:
        return "(无)"
    head = tok[:9]
    tail = tok[-4:] if len(tok) > 4 else "????"
    return f"{head}…{tail}"

def _token_class(tok: str) -> str:
    if tok.startswith(FINE_PREFIX):
        return "fine-grained"
    if tok.startswith(CLASSIC_PREFIX):
        return "classic"
    if tok.startswith(OAUTH_PREFIX):
        return "oauth-app"
    return "unknown"

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
            if any(line.startswith(p) for p in ("ghp_", "github_pat_", "gho_")):
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
                if val and any(val.startswith(p) for p in ("ghp_", "github_pat_", "gho_")):
                    return val
    return None

def load_token(cli_token=None):
    """返回 (token, source)。顺序: --token > env > vault > Keychain > mcp.json"""
    if cli_token:
        return cli_token, "--token 参数"
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        val = os.environ.get(var)
        if val and val.startswith(("ghp_", "github_pat_", "gho_")):
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

# ── GitHub API 调用 ────────────────────────────────────────
PROXY = None  # 可选 http 代理 (--proxy)，默认直连

def gh_request(token: str, path: str):
    """返回 (status_code, json_body, headers)。
    注意: urllib 不支持 socks5h:// 代理 scheme(常见于本机 HTTP_PROXY)，
    因此默认强制直连(实测 api.github.com 可直连)；如需代理请显式 --proxy http://..."""
    url = GITHUB_API + path
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": UA,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if PROXY:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    else:
        # 忽略环境 socks 代理，直连
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
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

def check_repo(token: str, repo: str):
    """单仓库检查 → dict"""
    out = {"repo": repo}
    st, body, _ = gh_request(token, f"/repos/{repo}")
    if st == 404:
        out.update(status="no-access", color="🔴",
                   detail="token 看不到该仓库(未授权或不存在)")
        return out
    if st != 200:
        out.update(status="error", color="🔴",
                   detail=f"GET /repos 失败 HTTP {st}")
        return out
    out["repo_full_name"] = body.get("full_name")
    out["private"] = bool(body.get("private"))
    # issues 读取探测
    st2, _, hdrs2 = gh_request(token, f"/repos/{repo}/issues?per_page=1")
    scopes = (hdrs2.get("X-OAuth-Scopes") or "").split(", ") if hdrs2 else []
    out["x_oauth_scopes"] = [s for s in scopes if s]
    tok_class = _token_class(token)
    out["token_class"] = tok_class
    if tok_class == "classic":
        sc = set(s.lower() for s in out["x_oauth_scopes"])
        if {"public_repo", "repo"} & sc:
            out.update(status="ok-write", color="🟢",
                       detail="classic token 含 public_repo/repo → 可对公开仓库发评论/PR")
        else:
            out.update(status="no-write", color="🟡",
                       detail=f"classic token 缺 public_repo/repo scope(现有: {out['x_oauth_scopes'] or '无'})")
    elif tok_class == "fine-grained":
        out.update(status="unknown-write", color="🟡",
                   detail="fine-grained 授权无法静态判定 → 请对照指南方案B确认 Issues/Pull requests=Read and write，或试发一条评论实测")
    else:
        out.update(status="unknown-write", color="🟡",
                   detail=f"token 类型未知({tok_class}) → 请对照指南核对")
    out["issues_read_http"] = st2
    return out

# ── 子命令 ─────────────────────────────────────────────────
def cmd_test_perms(token: str, repos, as_json: bool):
    print(f"🔑 当前 token: {_mask(token)} [{_token_class(token)}]")
    st0, body0, _ = gh_request(token, "/user")
    if st0 == 401:
        msg = {"status": "invalid-token", "color": "🔴",
               "detail": "token 无效或已过期 → 请按指南重发 token 并 lh_vault set github-pat"}
        return _emit(msg, as_json, exit_code=2)
    if st0 != 200:
        err = body0.get("_err", "")
        msg = {"status": "network-error", "color": "🔴",
               "detail": f"GET /user 失败 HTTP {st0}{' · ' + err if err else ''}"
                        f"{' → 若走代理可试 --proxy http://127.0.0.1:PORT' if not PROXY else ''}"}
        return _emit(msg, as_json, exit_code=2)
    login = body0.get("login")
    print(f"👤 登录账号: {login}")
    results = [check_repo(token, r) for r in repos]
    colors = [r.get("color") for r in results]
    for r in results:
        print(f"{r.get('color')} {r.get('repo')}: {r.get('detail')}")
    if as_json:
        payload = {"login": login, "token_class": _token_class(token),
                   "results": results}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if "🔴" in colors:
            print("\n🟥 结论: 当前 PAT 不可用，先修 token 再发")
            _hint_extra(token)
            return 2
        if any(c == "🟡" for c in colors):
            print("\n🟨 结论: 有仓库写权限待确认/待补 → 看 token-hint 给补法")
            return 1
        print("\n🟩 结论: 权限就绪，可以发评论/PR")
    return 0

def cmd_token_hint(token: str, as_json: bool):
    tok_class = _token_class(token)
    hint = {"token_present": bool(token), "token_class": tok_class,
            "masked": _mask(token) if token else None}
    if not token:
        hint.update(color="🔴", guide=GUIDE,
                    detail="本地没有可用的 GitHub token。① 生成(指南) ② lh_vault set github-pat 存入")
    elif tok_class == "fine-grained":
        hint.update(color="🟡", guide=GUIDE,
                    detail="fine-grained token 已找到，但 API 无法静态返回授权清单。请确认: Repository access=All public repositories，且 Issues / Pull requests = Read and write(指南方案B第5步)")
    elif tok_class == "classic":
        # 真实 scope 需一次探测
        st, body, hdrs = gh_request(token, "/user")
        if st != 200:
            err = body.get("_err", "")
            hint.update(color="🔴", detail=f"网络/API 失败 HTTP {st}{' · ' + err if err else ''}"
                                           f"{' → 可试 --proxy http://127.0.0.1:PORT' if not PROXY else ''}")
            if as_json:
                print(json.dumps(hint, ensure_ascii=False, indent=2))
            else:
                print(f"🔑 token: {hint['masked']} [{hint['token_class']}]")
                print(f"{hint.get('color')} {hint['detail']}")
            return 2
        scopes = (hdrs.get("X-OAuth-Scopes") or "") if hdrs else ""
        sc = set(s.lower() for s in scopes.split(", ") if s)
        if {"public_repo", "repo"} & sc:
            hint.update(color="🟢", detail="classic token 已含 public_repo/repo，可发公开仓库评论/PR")
        else:
            hint.update(color="🟡", guide=GUIDE,
                        detail=f"classic token 缺 public_repo/repo scope(现有: {scopes or '无'}) → 指南方案A: scopes 勾 public_repo")
    else:
        hint.update(color="🟡", guide=GUIDE,
                    detail=f"token 类型 {tok_class} 不在 classic/fine-grained 识别表，请对照指南确认")
    if as_json:
        print(json.dumps(hint, ensure_ascii=False, indent=2))
    else:
        print(f"🔑 token: {hint['masked']} [{hint['token_class']}]")
        print(f"{hint.get('color')} {hint['detail']}")
        if hint.get("guide"):
            print(f"📖 按图操作: {hint['guide']}")
    return 0 if hint.get("color") == "🟢" else (2 if hint.get("color") == "🔴" else 1)

def _hint_extra(token: str):
    tok_class = _token_class(token)
    if tok_class == "fine-grained":
        print("💡 这是 fine-grained token: 去指南方案B 确认 Issues/PR = Read and write")
    elif tok_class == "classic":
        print("💡 这是 classic token: 去指南方案A 勾 public_repo scope")

def _emit(msg, as_json, exit_code: int):
    if as_json:
        print(json.dumps(msg, ensure_ascii=False, indent=2))
    else:
        print(f"{msg.get('color')} {msg.get('detail')}")
    return exit_code

def usage():
    print("""龍魂 GitHub 权限自检工具 v1.0
用法:
  lh github test-perms [--repo owner/repo ...] [--json] [--token xxx]
      → 测当前 PAT 对目标仓库(默认 deepseek-ai/DeepSeek-V3)的权限状态
  lh github token-hint [--json] [--token xxx]
      → 输出缺失权限范围建议(指向 docs/github-pat-setup-guide.md)
token 读取顺序: --token > GH_TOKEN/GITHUB_TOKEN > lh_vault github-pat > Keychain > mcp.json""")

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
    repos = list(DEFAULT_REPOS)
    # 轻量参数解析(--repo 可多次 / --token / --proxy)
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "--json":
            pass
        elif a == "--repo" and i + 1 < len(rest):
            repos.append(rest[i + 1])
            i += 1
        elif a == "--token" and i + 1 < len(rest):
            cli_token = rest[i + 1]
            i += 1
        elif a == "--proxy" and i + 1 < len(rest):
            PROXY = rest[i + 1]
            i += 1
        i += 1
    token, source = load_token(cli_token)
    if not as_json and token and source:
        print(f"🗂️ token 来源: {source}")
    if cmd == "test-perms":
        if not token:
            return _emit({"color": "🔴",
                          "detail": "本地没有可用 GitHub token → 先看 docs/github-pat-setup-guide.md 生成并 lh_vault set github-pat"},
                         as_json, exit_code=2)
        return cmd_test_perms(token, repos, as_json)
    if cmd == "token-hint":
        return cmd_token_hint(token, as_json)
    print(f"❓ 未知子命令: {cmd}")
    usage()
    return 1

if __name__ == "__main__":
    sys.exit(main())
