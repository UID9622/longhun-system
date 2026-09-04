#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·CodeQL 自动响应闭环 v1.0
DNA: #龍芯⚡️2026-09-03-CODEQL-LISTENER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能: GitHub CodeQL 扫描结果监听器 —— 自动响应闭环的「耳朵」
  · lh codeql listen [--interval 60] [--once] [--daemon] → 轮询扫描状态·发现新完成扫描自动触发修复
  · lh codeql status                          → 显示当前扫描状态（等待/进行中/完成/失败）
  · lh codeql fetch [--sarif] [--repo o/r]    → 拉取最新 CodeQL 扫描结果（alerts / SARIF）
  · 触发链: GitHub push/PR → CodeQL 扫描 → 本监听器捕获 complete → 解析分组 → 调 lh_codeql_autofix
  · 守护模式: --daemon 后台循环（launchd/systemd 亦可托管）
  · 日志: ~/.longhun/logs/codeql_listener.log · 状态: ~/.longhun/codeql/state.json · 结果: last_results.json

安全:
  · token 读取链: --token > env GITHUB_TOKEN > lh_vault github-pat > Keychain > mcp.json
  · 只读 GitHub API；修复/提交动作一律交给 autofix 模块（有熔断）
  · 不落盘 token · 日志不含密钥

v1.0 2026-09-03 · CodeQL 自动响应闭环任务1
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import threading
import urllib.request
import urllib.error
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CQL_DIR = Path.home() / ".longhun" / "codeql"
STATE = CQL_DIR / "state.json"
RESULTS = CQL_DIR / "last_results.json"
LOG = Path.home() / ".longhun" / "logs" / "codeql_listener.log"
PIDFILE = CQL_DIR / "listener.pid"

DEFAULT_REPO = "UID9622/longhun-system"
WORKFLOW_MARK = "CodeQL"          # workflow 名包含即视为 CodeQL 扫描 workflow
SCAN_EVENT_MARK = "push"           # 只监听 push 事件（PR 扫描由 PR 内驱动）

severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "note": 1, "warning": 2, "error": 3}


def log(msg: str, level: str = "INFO"):
    line = f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] {level} {msg}"
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ─────────────────────────── GitHub token / API ───────────────────────────

def resolve_token(cli_token: str = "") -> tuple:
    """返回 (token, source)。顺序: --token > env > vault > Keychain"""
    if cli_token:
        return cli_token, "--token 参数"
    env = os.environ.get("GITHUB_TOKEN", "").strip()
    if env:
        return env, "env GITHUB_TOKEN"
    # vault
    try:
        p = subprocess.run([sys.executable, str(ROOT / "08_BIN" / "lh_vault.py"), "get", "github-pat"],
                           capture_output=True, text=True, timeout=15)
        out = (p.stdout or "").strip().splitlines()
        if p.returncode == 0 and out:
            last = out[-1].strip()
            if last and not last.startswith(("✅", "❌", "⚠", "🔑", "使用", "lh_vault")):
                return last, "lh_vault github-pat"
    except Exception:
        pass
    # Keychain
    try:
        p = subprocess.run(
            ["security", "find-internet-password", "-s", "github.com", "-a", "UID9622", "-w"],
            capture_output=True, text=True, timeout=10)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip(), "Keychain github.com/UID9622"
    except Exception:
        pass
    return "", ""


_NO_PROXY_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 防 socks5h 代理劫持


def gh_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "longhun-codeql-listener/1.0")
    with _NO_PROXY_OPENER.open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _check_err(data: dict) -> str:
    """GitHub 错误响应提取（403/404/无 advanced-security 等）"""
    if isinstance(data, dict) and data.get("message"):
        return str(data.get("message"))[:160]
    return ""


# ─────────────────────────── 状态/结果落盘 ───────────────────────────

def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": 1, "last_run_id": 0, "status": "unknown", "conclusion": "",
            "fetched_at": "", "last_checked_at": "", "issue_counts": {}, "errors": []}


def save_state(s: dict):
    CQL_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def load_results() -> dict:
    if RESULTS.exists():
        try:
            return json.loads(RESULTS.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"fetched_at": "", "run_id": 0, "alerts": [], "groups": {}}


def save_results(r: dict):
    CQL_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")


# ─────────────────────────── CodeQL 扫描状态查询 ───────────────────────────

def _latest_codeql_run(token: str, repo: str) -> dict:
    """定位最新 CodeQL workflow run（push 事件）。返回 {} 表示无"""
    url = f"https://api.github.com/repos/{repo}/actions/workflows"
    try:
        data = gh_get(url, token)
        if _check_err(data):
            return {"error": _check_err(data)}
        cq = [w for w in data.get("workflows", []) if WORKFLOW_MARK in w["name"]]
        if not cq:
            return {"error": f"仓库无含 '{WORKFLOW_MARK}' 的 workflow"}
        wf = cq[0]
        url2 = (f"https://api.github.com/repos/{repo}/actions/workflows/{wf['id']}/runs"
                f"?event=push&per_page=1")
        data2 = gh_get(url2, token)
        if _check_err(data2):
            return {"error": _check_err(data2)}
        runs = data2.get("workflow_runs", [])
        if not runs:
            return {"workflow": wf["name"], "run": None}
        r = runs[0]
        return {"workflow": wf["name"], "run": {
            "id": r["id"], "status": r["status"], "conclusion": r.get("conclusion"),
            "head_sha": r["head_sha"][:8], "created_at": r["created_at"],
            "updated_at": r.get("updated_at"), "html_url": r["html_url"]}}
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": str(e)[:160]}


def fetch_alerts(token: str, repo: str, sarif: bool = False) -> dict:
    """拉取 CodeQL alerts（或 SARIF 摘要）。
    返回统一结构: {run_id, fetched_at, alerts:[...], groups:{...}, sarif_info?}
    alert: {rule_id, severity, description, file, line, tags}
    """
    out = {"fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
           "repo": repo, "alerts": [], "groups": {}, "sarif": None}
    try:
        url = (f"https://api.github.com/repos/{repo}/code-scanning/alerts"
               f"?state=open&per_page=100")
        data = gh_get(url, token)
        if _check_err(data):
            out["error"] = _check_err(data)
            return out
        if not isinstance(data, list):
            out["error"] = "响应非列表"
            return out
        for a in data:
            sev = str(a.get("rule", {}).get("severity") or "note").lower()
            ss = a.get("rule", {}).get("security_severity_level") or ""
            if sev == "error" and ss:
                sev = ss.lower()  # high/critical 更精确
            tags = a.get("rule", {}).get("tags") or []
            loc = a.get("most_recent_instance", {}).get("location", {})
            alert = {
                "rule_id": a.get("rule", {}).get("id", ""),
                "severity": sev,
                "description": a.get("rule", {}).get("description", ""),
                "file": loc.get("path", ""),
                "line": loc.get("start_line", 0),
                "tags": tags,
                "alert_url": a.get("html_url", ""),
                "state": a.get("state", ""),
            }
            if alert["rule_id"] and alert["file"]:
                out["alerts"].append(alert)
        # 分组 by severity
        for a in out["alerts"]:
            out["groups"].setdefault(a["severity"], 0)
            out["groups"][a["severity"]] += 1
        # SARIF: 最新 analysis 元数据（CodeQL 不提供完整 SARIF 在线下载·附关键元数据）
        if sarif:
            try:
                u2 = f"https://api.github.com/repos/{repo}/code-scanning/analyses?per_page=1"
                d2 = gh_get(u2, token)
                if isinstance(d2, list) and d2:
                    a0 = d2[0]
                    out["sarif"] = {"analysis_id": a0.get("id"), "commit_sha": a0.get("commit_sha")[:12],
                                    "analysis_key": a0.get("analysis_key"),
                                    "created_at": a0.get("created_at"),
                                    "error_count": a0.get("error_count")}
            except Exception as e:
                out["sarif"] = {"note": f"SARIF 摘要不可用: {str(e)[:120]}"}
        return out
    except urllib.error.HTTPError as e:
        out["error"] = f"HTTP {e.code} {e.reason}"
        return out
    except Exception as e:
        out["error"] = str(e)[:160]
        return out


def summarize_status(repo: str, token: str) -> dict:
    """扫描状态汇总（驱动 status 命令与 listen 决策）"""
    info = _latest_codeql_run(token, repo)
    if info.get("error"):
        return {"ok": False, "status": "unknown", "error": info["error"], "workflow": None}
    run = info.get("run")
    if not run:
        return {"ok": True, "status": "idle", "workflow": info.get("workflow"),
                "note": "尚无 push 触发的扫描运行"}
    m = {"queued": "等待", "in_progress": "进行中", "completed": "完成"}
    return {"ok": True, "status": run["status"], "status_zh": m.get(run["status"], run["status"]),
            "conclusion": run.get("conclusion"), "run_id": run["id"],
            "head_sha": run.get("head_sha"), "workflow": info.get("workflow"),
            "created_at": run.get("created_at"), "html_url": run.get("html_url")}


def alerts_fingerprint(alerts: list) -> str:
    """结果去重指纹: (rule_id|file|line|severity) 集合哈希。防 PR 自激循环重复 autofix"""
    if not alerts:
        return ""
    sig = "\n".join(sorted(f"{a.get('rule_id')}|{a.get('file')}|{a.get('line')}|{a.get('severity')}"
                           for a in alerts))
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()[:16]


def read_last_fingerprint() -> str:
    st = load_state()
    return st.get("last_autofix_fp", "")


# ─────────────────────────── 触发修复（转 autofix）───────────────────────────

def trigger_autofix(extra: list) -> subprocess.CompletedProcess:
    """调用 lh_codeql_autofix.py（默认 --pr-only，不自动合并；--auto-merge 由调用方传入）"""
    script = ROOT / "bin" / "lh_codeql_autofix.py"
    cmd = [sys.executable, str(script)] + (extra or ["--pr-only"])
    log(f"触发修复: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(ROOT), check=False, capture_output=True, text=True, timeout=1800)


# ─────────────────────────── listen 主循环 ───────────────────────────

def listen_once(interval: int, token: str, repo: str, trigger: bool,
                autofix_extra: list | None = None, sarif: bool = False) -> dict:
    """单轮轮询: 查状态 → 完成且新 run → 拉结果 → (可)触发修复。返回结果 dict"""
    st = load_state()
    info = _latest_codeql_run(token, repo)
    if info.get("error"):
        st["errors"] = (st.get("errors") or [])[-4:] + [info["error"]]
        st["last_checked_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
        save_state(st)
        log(f"查询失败: {info['error']}", "WARN")
        return {"ok": False, "error": info["error"]}

    run = info.get("run")
    if not run:
        st["last_checked_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
        save_state(st)
        return {"ok": True, "status": "idle", "note": "无扫描运行"}

    run_id = run["id"]
    st["last_checked_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    st["workflow"] = info.get("workflow")
    st["run_id"] = run_id
    st["run_status"] = run["status"]
    st["run_conclusion"] = run.get("conclusion")

    # 扫描未完成 → 仅记录
    if run["status"] != "completed":
        save_state(st)
        return {"ok": True, "status": run["status"], "conclusion": run.get("conclusion"),
                "note": f"扫描 {run['status']}（run #{run_id}），继续等待"}

    # 已完成: 拉结果
    res = fetch_alerts(token, repo, sarif=sarif)
    res["run_id"] = run_id
    res["conclusion"] = run.get("conclusion")
    res["head_sha"] = run.get("head_sha")
    st["fetched_at"] = res["fetched_at"]
    st["conclusion"] = run.get("conclusion")
    st["issue_counts"] = res.get("groups", {})
    st["last_result_run_id"] = run_id
    save_state(st)
    save_results(res)

    total = len(res.get("alerts", []))
    if res.get("error"):
        log(f"run #{run_id} 完成但拉取失败: {res['error']}", "WARN")
        return {"ok": False, "status": "completed", "error": res["error"], "alerts": []}

    log(f"run #{run_id} 完成 · {run.get('conclusion')} · alerts={total} "
        f"groups={res.get('groups', {})}")
    if total == 0:
        return {"ok": True, "status": "completed", "conclusion": run.get("conclusion"),
                "alerts": [], "note": "扫描完成·0 告警·无需修复"}

    # 触发修复（仅当 trigger=True 且结论 success；失败结论=扫描自身挂了→不自动修）
    if trigger and run.get("conclusion") == "success":
        fp = alerts_fingerprint(res.get("alerts", []))
        last_fp = read_last_fingerprint()
        if fp and fp == last_fp:
            log(f"run #{run_id} 告警集合与上次 autofix 相同（指纹 {fp}）· 跳过防自激循环")
            st["last_autofix_fp"] = fp
            st["last_autofix_skip"] = now_iso()
            save_state(st)
            return {"ok": True, "status": "completed", "conclusion": run.get("conclusion"),
                    "alerts": total, "note": "告警未变化·跳过重复修复"}
        log(f"发现 {total} 个告警（fp={fp}）· 触发数字人协作修复")
        r = trigger_autofix(list(autofix_extra or ["--pr-only"]))
        st["last_autofix_fp"] = fp
        st["last_autofix_at"] = now_iso()
        save_state(st)
        return {"ok": True, "status": "completed", "conclusion": run.get("conclusion"),
                "alerts": total, "autofix_rc": r.returncode,
                "autofix_out": (r.stdout or "")[-2000:]}
    return {"ok": True, "status": "completed", "conclusion": run.get("conclusion"),
            "alerts": total, "note": "扫描完成·告警已落盘"}


def daemon_loop(interval: int, token: str, repo: str, sarif: bool, autofix_extra: list | None):
    CQL_DIR.mkdir(parents=True, exist_ok=True)
    PIDFILE.write_text(str(os.getpid()), encoding="utf-8")
    log(f"🚀 CodeQL 监听守护启动 · repo={repo} · interval={interval}s · pid={os.getpid()}")
    while True:
        try:
            r = listen_once(interval, token, repo, trigger=True, autofix_extra=autofix_extra, sarif=sarif)
            if not r.get("ok"):
                log(f"本轮异常: {r.get('error', '?')}", "WARN")
        except KeyboardInterrupt:
            log("监听守护收到中断，退出")
            break
        except Exception as e:
            log(f"本轮异常: {str(e)[:200]}", "ERROR")
        time.sleep(interval)


# ─────────────────────────── 输出助手 ───────────────────────────

def print_table(rows: list, headers: list):
    """极简对齐表格输出"""
    widths = []
    for i, h in enumerate(headers):
        w = len(str(h))
        for row in rows:
            v = str(row[i]) if i < len(row) else ""
            w = max(w, min(len(v), 40))
        widths.append(w)
    line = "  " + " │ ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    sep = "  " + "─┼─".join("─" * widths[i] for i in range(len(headers)))
    print(line)
    print(sep)
    for row in rows:
        cells = []
        for i, h in enumerate(headers):
            v = str(row[i]) if i < len(row) else ""
            cells.append(v.ljust(widths[i]))
        print("  " + " │ ".join(cells))


def cmd_status(repo: str, token: str):
    st = load_state()
    s = summarize_status(repo, token)
    if not s.get("ok"):
        print(f"🔴 状态查询失败: {s.get('error')}")
        return 1
    status_zh = s.get("status_zh", s.get("status", "?"))
    emoji = {"等待": "⏳", "进行中": "🔵", "完成": "✅"}.get(status_zh, "❓")
    print(f"\n  {emoji} CodeQL 扫描状态 · {s.get('workflow', '?')}\n")
    print_table([
        ["状态", f"{status_zh} ({s.get('status')})"],
        ["结论", s.get("conclusion") or "—"],
        ["run #", s.get("run_id") or "—"],
        ["head sha", s.get("head_sha") or "—"],
        ["创建时间", s.get("created_at") or "—"],
        ["最近告警", f"{st.get('issue_counts', {}) or '—'}"],
        ["上次检查", st.get("last_checked_at") or "—"],
        ["链接", s.get("html_url") or "—"],
    ], ["字段", "值"])
    return 0


def cmd_fetch(repo: str, token: str, sarif: bool):
    print(f"\n  🔬 拉取 CodeQL 扫描结果 · {repo}" + ("（含 SARIF 摘要）" if sarif else "") + "\n")
    res = fetch_alerts(token, repo, sarif=sarif)
    if res.get("error"):
        print(f"  🔴 拉取失败: {res['error']}")
        return 1
    total = len(res.get("alerts", []))
    groups = res.get("groups", {})
    print(f"  ✅ 拉取成功 · open alerts = {total} · {groups or '无告警'}")
    if res.get("sarif"):
        print(f"  📄 SARIF 摘要: {json.dumps(res['sarif'], ensure_ascii=False)}")
    if res["alerts"]:
        rows = [[a["severity"], a["rule_id"], f"{a['file']}:{a['line']}",
                 (a.get("description") or "")[:50]] for a in res["alerts"]]
        print_table(rows, ["级别", "规则", "位置", "描述"])
    # 落盘（含 run 元数据 → dashboard/status 联动）
    s_meta = summarize_status(repo, token)
    if s_meta.get("ok") and s_meta.get("run_id"):
        res["run_id"] = s_meta["run_id"]
        res["conclusion"] = s_meta.get("conclusion")
        res["head_sha"] = s_meta.get("head_sha")
        res["scan_html_url"] = s_meta.get("html_url")
    res["fetched_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    save_results(res)
    st = load_state()
    st["fetched_at"] = res["fetched_at"]
    st["issue_counts"] = groups
    if s_meta.get("ok") and s_meta.get("run_id"):
        st["run_id"] = s_meta["run_id"]
        st["run_status"] = s_meta.get("status")
        st["conclusion"] = s_meta.get("conclusion")
        st["head_sha"] = s_meta.get("head_sha")
    save_state(st)
    return 0


# ─────────────────────────── webhook 服务（任务4 联动）───────────────────────────
_WEBHOOK_ACT = None
_WEBHOOK_LOCK = threading.Lock()


def _act_webhook():
    """收到 GitHub workflow_run 事件 → 立刻跑一轮 listen（触发修复）"""
    global _WEBHOOK_ACT
    with _WEBHOOK_LOCK:
        try:
            r = listen_once(60, _WEBHOOK_ACT["token"], _WEBHOOK_ACT["repo"],
                            trigger=True, autofix_extra=["--pr-only"])
            log(f"webhook 触发一轮 · {r.get('status', '?')} alerts={r.get('alerts', '?')} "
                f"note={r.get('note', '')[:80]}")
        except Exception as e:
            log(f"webhook 触发异常: {str(e)[:120]}", "ERROR")


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            ln = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(ln).decode("utf-8", "replace")
            try:
                ev = json.loads(body or "{}")
            except Exception:
                ev = {"raw": body[:200]}
            log(f"webhook 收到事件: {json.dumps(ev, ensure_ascii=False)[:200]}")
            threading.Thread(target=_act_webhook, daemon=True).start()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok": true, "message": "codeql trigger received"}')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode()[:200])

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"longhun-codeql-listener webhook : ok")

    def log_message(self, *a):
        pass


def serve_webhook(port: int, repo: str, token: str, interval: int) -> int:
    """webhook 模式: 启动 HTTP 端点 + 后台轮询兜底。返回进程保持运行"""
    global _WEBHOOK_ACT
    CQL_DIR.mkdir(parents=True, exist_ok=True)
    PIDFILE.write_text(str(os.getpid()), encoding="utf-8")
    _WEBHOOK_ACT = {"token": token, "repo": repo}
    # 兜底轮询线程（webhook 断线时仍每 interval 查一次）
    def _poll():
        while True:
            try:
                listen_once(interval, token, repo, trigger=True, autofix_extra=["--pr-only"])
            except Exception as e:
                log(f"兜底轮询异常: {str(e)[:120]}", "ERROR")
            time.sleep(interval)
    threading.Thread(target=_poll, daemon=True).start()
    log(f"🌐 CodeQL webhook 服务 :{port} · POST / 即可唤醒触发一轮 · 兜底轮询 {interval}s")
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", port), WebhookHandler)
        srv.serve_forever()
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        log(f"webhook 服务异常: {str(e)[:120]}", "ERROR")
        return 1
    return 0


# ─────────────────────────── main ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·CodeQL 监听器 v1.0")
    ap.add_argument("action", nargs="?", choices=["listen", "status", "fetch", "dashboard", "webhook"],
                    help="listen=轮询监听 / status=状态 / fetch=拉取 / dashboard=面板 / webhook=联动端点")
    ap.add_argument("--interval", type=int, default=60, help="轮询间隔秒（默认60）")
    ap.add_argument("--once", action="store_true", help="listen 单轮后退出（不循环）")
    ap.add_argument("--daemon", action="store_true", help="listen 后台守护循环")
    ap.add_argument("--sarif", action="store_true", help="fetch 附带最新 analysis SARIF 摘要")
    ap.add_argument("--repo", default=DEFAULT_REPO, help=f"仓库 owner/repo（默认 {DEFAULT_REPO}）")
    ap.add_argument("--token", default="", help="GitHub token（默认自动链读取）")
    ap.add_argument("--no-trigger", action="store_true", help="listen 只拉取不触发修复")
    ap.add_argument("--autofix", action="store_true", help="listen 发现告警时自动触发修复并建 PR")
    ap.add_argument("--auto-merge", action="store_true", help="触发修复时自动合并 PR（需人工审核，默认不合并）")
    ap.add_argument("--webhook-port", type=int, default=9786, help="webhook 监听端口（默认9786）")
    args = ap.parse_args()

    if args.action == "dashboard":
        # dashboard 归 autofix 模块输出（需要修复日志）
        script = ROOT / "bin" / "lh_codeql_autofix.py"
        sys.exit(subprocess.run([sys.executable, str(script), "dashboard"], cwd=str(ROOT)).returncode)

    token, source = resolve_token(args.token)
    if not token:
        print("🔴 无 GitHub token（--token / GITHUB_TOKEN / lh_vault github-pat / Keychain 均不可用）")
        return 1
    print(f"  🔑 token 来源: {source}\n")

    if args.action == "webhook":
        # webhook 模式（任务4 联动：codeql-trigger.yml workflow_run → curl 内网隧道 → 本端点）
        port = args.webhook_port or 9786
        return serve_webhook(port, args.repo, token, args.interval)

    if args.action == "status":
        return cmd_status(args.repo, token)
    if args.action == "fetch":
        return cmd_fetch(args.repo, token, sarif=args.sarif)

    # listen
    if args.once or not (args.daemon):
        extra = []
        if args.autofix:
            extra += (["--auto-merge"] if args.auto_merge else ["--pr-only"])
        r = listen_once(args.interval, token, args.repo,
                        trigger=bool(args.autofix) and not args.no_trigger,
                        autofix_extra=extra, sarif=args.sarif)
        print(json.dumps({k: v for k, v in r.items() if k != "autofix_out"},
                         ensure_ascii=False, indent=2))
        if r.get("autofix_out"):
            print("── autofix 输出 ──")
            print(r["autofix_out"])
        return 0 if r.get("ok") else 1

    daemon_loop(args.interval, token, args.repo, args.sarif,
                (["--auto-merge"] if args.auto_merge else ["--pr-only"]) if args.autofix else None)
    return 0


if __name__ == "__main__":
    main()
