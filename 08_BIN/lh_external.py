#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷟恒-EXTERNAL-SENSE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""🌐 外部源码感知引擎 v1.0 — 全局记忆系统 A4（2026-09-04落地）

理念: 自动感知 GitHub 龍魂生态仓库变更，关联到全局状态/时间轴/耻辱墙通知区。
扫关键词域: longhun / cnsh / wuxing / 龙魂 / 五行 / UID9622（watch 目标以显式添加为主·scan 顺带搜候选提示）

数据:
  ~/.longhun/external/watches.json   跟踪列表 {"repo": {"last_commit","last_scan",...}}
  ~/.longhun/external/<repo>.json    最近变更快照
  ~/.longhun/shame_wall/notices.jsonl 通知区（外部相关变更提醒·append-only）
集成:
  scan 检测到新 commit → 写快照 + 更新 global_state(external字段) + timeline(type=external) + 提醒
用法:
  lh external watch <owner/repo>    → 加入跟踪并记录当前 commit
  lh external unwatch <owner/repo>
  lh external status                → 跟踪列表及状态
  lh external scan [--force]        → 扫描变更（距上次<10min自动跳过·--force 强制）
  lh external diff <owner/repo>     → 查看该仓库最近变更
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# 引擎间本地 import 路径注入（解析真实目录防 bin 软链偏差）
_BIN_DIR = Path(__file__).resolve().parent
if str(_BIN_DIR) not in sys.path:
    sys.path.insert(0, str(_BIN_DIR))

ROOT = Path.home() / ".longhun"
EXT_DIR = ROOT / "external"
GLOBAL = ROOT / "state" / "global_state.json"
NOTICES = ROOT / "shame_wall" / "notices.jsonl"
SESSION = ROOT / "session_context.json"
API = "https://api.github.com"
KEYWORDS = ("longhun", "cnsh", "wuxing", "龙魂", "五行", "UID9622")

# 匿名 60 req/h 够用；有 GITHUB_TOKEN 则自动带上（public_repo 可查公开仓）
def _token() -> str:
    return os.environ.get("GITHUB_TOKEN", "")


def _local_now():
    return datetime.now().astimezone()


def _http_json(url: str) -> dict | None:
    """直连 GitHub API（清代理·urllib 不认 socks5h）"""
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(k, None)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "longhun-external-sense-v1.0")
    t = _token()
    if t:
        req.add_header("Authorization", f"Bearer {t}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _load_watches() -> dict:
    EXT_DIR.mkdir(parents=True, exist_ok=True)
    if not (EXT_DIR / "watches.json").exists():
        return {}
    try:
        d = json.loads((EXT_DIR / "watches.json").read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save_watches(w: dict) -> None:
    (EXT_DIR / "watches.json").write_text(
        json.dumps(w, ensure_ascii=False, indent=2), encoding="utf-8")


def _norm_repo(repo: str) -> str:
    """owner/name 归一（接受 URL 输入）"""
    m = re.sub(r"https?://github.com/|git@github.com:", "", repo.strip())
    m = m.rstrip("/").replace(".git", "")
    return m


def _fetch_latest(repo: str) -> dict | None:
    """拉最新 commit（per_page=1）"""
    return _http_json(f"{API}/repos/{repo}/commits?per_page=1")


def _fetch_detail(repo: str, sha: str) -> dict | None:
    return _http_json(f"{API}/repos/{repo}/commits/{sha}")


def _session_task() -> str:
    try:
        if SESSION.exists():
            d = json.loads(SESSION.read_text(encoding="utf-8"))
            return (d.get("active_task") or "").strip()
    except Exception:
        pass
    return ""


def _update_global(external_info: dict) -> None:
    """扫描结果同步到全局状态总线 global_state.json.external"""
    try:
        import lh_state
        d = lh_state.read_global()
        d["external"] = external_info
        lh_state.save_global(d)
    except Exception:
        pass


def _notice(repo: str, msg: str) -> None:
    NOTICES.parent.mkdir(parents=True, exist_ok=True)
    line = {"ts": _local_now().isoformat(), "type": "external_sense",
            "repo": repo, "message": msg, "dna": "#龍芯⚡️EXTERNAL-SENSE"}
    with open(NOTICES, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def cmd_watch(repo_raw: str) -> int:
    repo = _norm_repo(repo_raw)
    if "/" not in repo:
        print(f"  ❌ 格式应为 owner/repo · 收到: {repo_raw}")
        return 1
    latest = _fetch_latest(repo)
    if latest is None or not isinstance(latest, list) or not latest:
        print(f"  ❌ 仓库 {repo} 不可达（网络/不存在/超限）")
        return 1
    c = latest[0].get("commit", {})
    sha = latest[0].get("sha", "")
    w = _load_watches()
    w[repo] = {
        "last_commit": sha[:8],
        "last_sha": sha,
        "last_message": (c.get("message") or "").splitlines()[0][:60],
        "last_scan": _local_now().isoformat(),
        "added_at": w.get(repo, {}).get("added_at", _local_now().isoformat()),
    }
    _save_watches(w)
    print(f"  🌐 已跟踪 {repo} @ {sha[:8]} {(c.get('message') or '')[:50]}")
    return 0


def cmd_unwatch(repo_raw: str) -> int:
    repo = _norm_repo(repo_raw)
    w = _load_watches()
    if repo not in w:
        print(f"  ⏭️  {repo} 不在跟踪列表")
        return 1
    del w[repo]
    _save_watches(w)
    print(f"  🌐 已停止跟踪 {repo}")
    return 0


def cmd_status() -> int:
    w = _load_watches()
    if not w:
        print("  🌐 跟踪列表为空 → lh external watch <owner/repo> 添加\n"
              "     （龍魂生态候选可试: lh external scan 自动搜索候选）")
        return 0
    print(f"  🌐 外部跟踪 · {len(w)} 个仓库\n")
    for repo, info in sorted(w.items()):
        since = ""
        ls = info.get("last_scan", "")
        if ls:
            try:
                mins = int((time.time() - datetime.fromisoformat(ls).timestamp()) // 60)
                since = f"{mins}分钟前"
            except Exception:
                since = ls[:16]
        print(f"  {repo:45} {info.get('last_commit', '-')}  「{info.get('last_message', '')[:40]}」 {since}")
    return 0


def cmd_scan(force: bool = False) -> int:
    import lh_state
    import lh_timeline as TL
    w = _load_watches()
    if not w:
        print("  🌐 跟踪列表为空·先按关键词搜候选（lh external watch <owner/repo> 添加）:")
        cand = _http_json(f"{API}/search/repositories?q=longhun+cnsh+in:name&sort=updated&per_page=5")
        items = (cand or {}).get("items") or []
        if items:
            for it in items[:5]:
                print(f"    → {it['full_name']} ⭐{it.get('stargazers_count', 0)} {it.get('description','')[:40]}")
            print("  命中即 watch: lh external watch <owner/repo>")
        else:
            print("  （搜索无命中或超限·可直接 watch 已知仓库）")
        return 0
    # 节流: 距上次<10分钟且非 --force → 跳过（节能）
    newest = max((i.get("last_scan", "") for i in w.values()), default="")
    if not force and newest:
        try:
            if time.time() - datetime.fromisoformat(newest).timestamp() < 600:
                print(f"  🌐 距上次扫描 <10 分钟（节能节流）· --force 可强制")
                return 0
        except Exception:
            pass
    changed = []
    for repo in sorted(w):
        latest = _fetch_latest(repo)
        if latest is None or not isinstance(latest, list) or not latest:
            continue
        c0 = latest[0]
        sha = c0.get("sha", "")
        info = w[repo]
        if sha and sha[:8] == info.get("last_commit"):
            info["last_scan"] = _local_now().isoformat()
            continue
        # 有新 commit！
        cm = (c0.get("commit", {}) or {}).get("message", "") or ""
        detail = _fetch_detail(repo, sha) if sha else None
        files = [f.get("filename", "") for f in (detail or {}).get("files", [])] if detail else []
        now = _local_now()
        snap = {
            "repo_name": repo,
            "last_commit": sha[:8],
            "last_sha": sha,
            "last_scan": now.isoformat(),
            "ganzhi": TL.ganzhi_simple(now),
            "files_changed": files[:100],
            "message": cm.splitlines()[0][:120] if cm else "",
            "task": _session_task(),
        }
        (EXT_DIR / "snapshots").mkdir(parents=True, exist_ok=True)
        (EXT_DIR / "snapshots" / f"{repo.replace('/', '_')}.json").write_text(
            json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
        info["last_commit"] = sha[:8]
        info["last_sha"] = sha
        info["last_message"] = cm.splitlines()[0][:60] if cm else ""
        info["last_scan"] = now.isoformat()
        changed.append((repo, sha, cm))
        # 集成: timeline 事件
        try:
            TL.record(f"external {repo} @{sha[:8]} 新commit", "external",
                      {"repo": repo, "sha": sha[:8]})
        except Exception:
            pass
        # 集成: 相关变更提醒 → 耻辱墙通知区（关键词关联）
        blob = cm + " " + repo + " " + " ".join(files)
        related = [k for k in KEYWORDS if k.lower() in blob.lower()]
        if related:
            _notice(repo, f"外部相关变更 {sha[:8]} ({','.join(related)}) · {cm.splitlines()[0][:60]}")
    _save_watches(w)
    _update_global({
        "last_scan": _local_now().isoformat(),
        "watched": len(w),
        "changed": [{"repo": r, "sha": s[:8]} for r, s, _ in changed],
        "last_change_at": changed and _local_now().isoformat() or "",
    })
    if changed:
        for r, s, cm in changed:
            print(f"  🔔 {r} @{s[:8]} 新 commit · {cm.splitlines()[0][:50]}")
        print(f"  🌐 检测到 {len(changed)} 个仓库变更 → 已写时间轴/状态总线/通知区")
    else:
        print(f"  🌐 全部 {len(w)} 个仓库无新 commit")
    return 0


def cmd_diff(repo_raw: str) -> int:
    repo = _norm_repo(repo_raw)
    commits = _http_json(f"{API}/repos/{repo}/commits?per_page=5")
    if commits is None or not isinstance(commits, list) or not commits:
        print(f"  ❌ {repo} 不可达或无 commit")
        return 1
    print(f"  🌐 {repo} 最近变更:\n")
    for c in commits:
        cm = (c.get("commit", {}) or {}).get("message", "").splitlines()
        au = ((c.get("commit", {}) or {}).get("author", {}) or {}).get("date", "")[:10]
        print(f"  {c.get('sha', '')[:8]}  {au}  {cm[0][:70] if cm else ''}")
    # 对比本地快照
    sp = EXT_DIR / "snapshots" / f"{repo.replace('/', '_')}.json"
    if sp.exists():
        d = json.loads(sp.read_text(encoding="utf-8"))
        print(f"\n  🧠 本地快照: {d.get('last_commit')} {d.get('last_scan', '')[:16]}")
        fc = d.get("files_changed", [])
        if fc:
            print(f"    变更文件 {len(fc)}:")
            for f in fc[:15]:
                print(f"      {f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh external", description="🌐 外部源码感知")
    sub = ap.add_subparsers(dest="cmd")
    sc = sub.add_parser("scan", help="扫描跟踪仓库变更")
    sc.add_argument("--force", action="store_true")
    sub.add_parser("status", help="跟踪列表及状态")
    df = sub.add_parser("diff", help="查看某仓库最近变更")
    df.add_argument("repo")
    wa = sub.add_parser("watch", help="加入跟踪")
    wa.add_argument("repo")
    uw = sub.add_parser("unwatch", help="停止跟踪")
    uw.add_argument("repo")
    args = ap.parse_args()
    if args.cmd in (None, "status"):
        return cmd_status()
    if args.cmd == "scan":
        return cmd_scan(args.force)
    if args.cmd == "diff":
        return cmd_diff(args.repo)
    if args.cmd == "watch":
        return cmd_watch(args.repo)
    if args.cmd == "unwatch":
        return cmd_unwatch(args.repo)
    print(f"  ❌ 未知子命令: {args.cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
