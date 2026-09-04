#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🛡️ P0焊死(2026-09-04·P72加封): 社区状态聚合引擎·源码修改须走三色治理v2.1 §十二门槛
# DNA: #龍芯⚡️2026-09-04-COMMUNITY-STATUS-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·社区 Issue 状态聚合感知 v1.0 — lh community status|weekly|watch
需求3: 每周社区状态报告(#1622/#1627/#89 等)·哪些有更新/待响应/已闭环(老大 2026-09-04 指令)。
数据: ~/.longhun/community_watch.json(关注清单·默认种子 1622/1627/89)
      ~/.longhun/validation/issues.jsonl(challenge 本地状态·append-only)
产出: ~/.longhun/community_status_weekly.md(每周报告·lh community weekly 生成)
用法:
  lh community status [--live] [--json] → 实时状态(默认纯本地零联网·--live 查 GitHub API)
  lh community weekly [--live]          → 生成每周报告 md
  lh community watch list|add <owner/repo> <issue_id> [--tag 备注]|remove <issue_id>
待响应判定(live): 我(UID9622)最后发言 → 等上游/已闭环; 他人最新评论 → 待响应。
"""
import json, os, sys, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.home() / ".longhun"
WATCH = ROOT / "community_watch.json"
ISSUES_LOCAL = ROOT / "validation" / "issues.jsonl"
WEEKLY = ROOT / "community_status_weekly.md"
ME = "UID9622"
API = "https://api.github.com"

DEFAULT_SEEDS = [
    {"owner": "deepseek-ai", "repo": "DeepSeek-V3", "id": "1622",
     "tag": "社区质疑·验证回应", "ours": False},
    {"owner": "deepseek-ai", "repo": "DeepSeek-V3", "id": "1627",
     "tag": "DeepSeek安全侦查汇总", "ours": True},
    {"owner": "arikusi", "repo": "deepseek-mcp-server", "id": "89",
     "tag": "CVE修复验证提醒", "ours": True},
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_watch() -> list:
    if WATCH.exists():
        try:
            return json.loads(WATCH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return list(DEFAULT_SEEDS)


def _save_watch(entries: list):
    ROOT.mkdir(parents=True, exist_ok=True)
    WATCH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def _github_get(url: str) -> dict:
    """GitHub API 直连(urllib·M77 零中间层·清代理)"""
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "LongHun-UID9622"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def _local_state(issue_id: str) -> str:
    if not ISSUES_LOCAL.exists():
        return ""
    for line in ISSUES_LOCAL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        if str(d.get("issue_id")) == str(issue_id):
            return str(d.get("状态", ""))
    return ""


def cmd_watch(argv: list) -> int:
    sub = argv[0] if argv else "list"
    if sub == "list":
        for e in _load_watch():
            print(f"  {e['owner']}/{e['repo']}#{e['id']} · {e.get('tag','')}")
        return 0
    if sub == "add":
        if len(argv) < 3:
            print("  ❌ 用法: lh community watch add <owner/repo> <issue_id> [--tag 备注]")
            return 1
        owner_repo = argv[1].strip("/")
        iid = argv[2]
        tag = ""
        if "--tag" in argv:
            k = argv.index("--tag")
            if k + 1 < len(argv):
                tag = argv[k + 1]
        owner, _, repo = owner_repo.partition("/")
        entries = _load_watch()
        entries = [e for e in entries if not (e["owner"] == owner and e["repo"] == repo and e["id"] == iid)]
        entries.append({"owner": owner, "repo": repo, "id": iid, "tag": tag, "ours": False})
        _save_watch(entries)
        print(f"  ✅ 已加入关注: {owner}/{repo}#{iid} {tag}")
        return 0
    if sub == "remove":
        if len(argv) < 2:
            print("  ❌ 用法: lh community watch remove <issue_id>")
            return 1
        iid = argv[1]
        entries = [e for e in _load_watch() if e["id"] != iid]
        _save_watch(entries)
        print(f"  ✅ 已移出关注: #{iid}")
        return 0
    print("用法: lh community watch list|add|remove")
    return 1


def _agg(entries: list, live: bool) -> list:
    rows = []
    for e in entries:
        row = {"owner": e["owner"], "repo": e["repo"], "id": e["id"],
               "tag": e.get("tag", ""), "ours": bool(e.get("ours")),
               "local": _local_state(e["id"])}
        if live:
            try:
                url = f"{API}/repos/{e['owner']}/{e['repo']}/issues/{e['id']}"
                d = _github_get(url)
                row["state"] = d.get("state", "?")
                row["title"] = d.get("title", "")[:70]
                row["updated"] = (d.get("updated_at") or "")[:16]
                row["comments"] = int(d.get("comments", 0))
                row["live_ok"] = True
                # 待响应: 取最新评论作者(未认证也能读评论? GET comments 需按 issue comments API)
                try:
                    cs = _github_get(f"{url}/comments?per_page=1")
                    row["last_comment_by"] = cs[-1]["user"]["login"] if cs else ""
                except Exception:
                    row["last_comment_by"] = ""
            except Exception as ex:
                row["live_ok"] = False
                row["live_err"] = str(ex)[:60]
        rows.append(row)
    return rows


def _print_rows(rows: list):
    for r in rows:
        hdr = f"{r['owner']}/{r['repo']}#{r['id']} · {r['tag']}"
        print(f"\n  {hdr}")
        if r.get("local"):
            print(f"     本地状态: {r['local']}")
        if r.get("live_ok"):
            mark = {"closed": "✅", "open": "🟡"}.get(r.get("state"), "?")
            act = ""
            if r.get("state") == "closed":
                act = "· ✅ 已闭环"
            elif r.get("last_comment_by") == ME:
                act = "· 🟢 我方最后发言·观望上游"
            elif r.get("last_comment_by"):
                act = "· 🔴 待响应(他人最新评论·需我方跟进)"
            else:
                act = "· 🟡 无新评论·等上游回应"
            print(f"     {mark} state={r.get('state')} · 评论{r.get('comments')} · 更新{r.get('updated')}"
                  f" · 最新评论by {r.get('last_comment_by','?')} {act}")
        elif "live_err" in r:
            print(f"     🟡 线上查询失败: {r['live_err']} (降级用本地状态·不自动重试)")
        else:
            print(f"     (加 --live 查线上更新/评论/闭环判定)")


def cmd_status(argv: list) -> int:
    live = "--live" in argv
    j = "--json" in argv
    rows = _agg(_load_watch(), live)
    if j:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print(f"🐉 社区 Issue 状态聚合({len(rows)}个关注"
          + ("·线上实时" if live else "·本地缓存·--live 查线上") + ")\n" + "=" * 46)
    _print_rows(rows)
    return 0


def cmd_weekly(argv: list) -> int:
    live = "--live" in argv
    rows = _agg(_load_watch(), live)
    lines = ["# 🐉 龍魂·社区状态周报\n",
             f"> 生成: {_now()[:16]} UTC · 关注 {len(rows)} 个 Issue · 详情见 "
             "`lh community status --live`\n",
             "| Issue | 标签 | 线上状态 | 我方 | 本地 | 判定 |",
             "|:---|:---|:---|:---|:---|:---|"]
    for r in rows:
        judge = ""
        if r.get("live_ok"):
            if r["state"] == "closed":
                judge = "✅ 已闭环"
            elif r.get("last_comment_by") == ME:
                judge = "🟢 我方最后发言·观望"
            elif r.get("last_comment_by"):
                judge = "🔴 待响应(他人新言)"
            else:
                judge = "🟡 等上游回应"
        elif r.get("local"):
            judge = f"本地:{r['local']}"
        else:
            judge = "? 未查询"
        st = r.get("state") or r.get("local") or "-"
        ours = "我方" if r.get("ours") else "他方"
        lines.append(f"| `{r['owner']}/{r['repo']}#{r['id']}` | {r['tag']} | {st} | {ours} | "
                     f"{r.get('local') or '-'} | {judge} |")
    txt = "\n".join(lines) + "\n"
    WEEKLY.write_text(txt, encoding="utf-8")
    print(f"  ✅ 社区周报已生成: {WEEKLY}")
    print(f"  📄 {len(rows)} 个 Issue · 有线上数据的判待响应/闭环(本页带 --live 生成才有线上判定)")
    return 0


def main() -> int:
    argv = sys.argv[1:] or ["status"]
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "status":
        return cmd_status(rest)
    if cmd == "weekly":
        return cmd_weekly(rest)
    if cmd == "watch":
        return cmd_watch(rest)
    print("用法: lh community status [--live]|weekly [--live]|watch list|add|remove")
    return 1


if __name__ == "__main__":
    sys.exit(main())
