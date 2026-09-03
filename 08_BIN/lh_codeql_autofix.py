#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·CodeQL 自动修复引擎 v1.0
DNA: #龍芯⚡️2026-09-03-CODEQL-AUTOFIX-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能: CodeQL 扫描结果的「修复手」—— 数字人协作修复 → 验证 → PR 闭环
  · lh codeql autofix [--dry-run] [--pr-only] [--auto-merge]  → 修复并提交
  · lh codeql dashboard                                      → 状态面板（Markdown + 徽章 + GPG）
  · 分派: 按问题类型路由到数字人（lh_dh_dispatch.codeql_repair: 包青天/字靈/匠心/知行/明鉴/诗仙/蔡侯）
  · 验证: lh health --json 全绿 + lh topo verify → 通过才提交
  · 熔断(任务5):
      · 每日修复次数上限 3（~/.longhun/codeql/autofix_state.json）
      · 修复前备份 ~/.longhun/backups/pre_codeql_fix/<ts>/
      · 连续 3 次失败 → 暂停 + 耻辱墙记录 + 通知
      · 禁止自动修改 .github/ 下 CI 配置（人工审核）
      · 修复日志 ~/.longhun/codeql_fix_log.json（append-only）
  · dashboard: ~/.longhun/codeql_dashboard.md（自动 GPG 签名）

v1.0 2026-09-03 · CodeQL 自动响应闭环任务3/5/6
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CQL_DIR = Path.home() / ".longhun" / "codeql"
STATE = CQL_DIR / "state.json"
RESULTS = CQL_DIR / "last_results.json"
FIX_LOG = Path.home() / ".longhun" / "codeql_fix_log.json"
AUTOFIX_STATE = CQL_DIR / "autofix_state.json"
DASHBOARD = Path.home() / ".longhun" / "codeql_dashboard.md"
BACKUP_ROOT = Path.home() / ".longhun" / "backups" / "pre_codeql_fix"
SHAME_JSON = Path.home() / ".longhun" / "shame_wall" / "shame_wall.json"

DAILY_LIMIT = 3          # 每日自动修复次数上限（任务5）
MAX_RETRY = 3            # 单次修复验证失败重试上限
FORBIDDEN = {".github"}  # 禁止自动修改路径前缀

DEFAULT_REPO = "UID9622/longhun-system"


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def log(msg: str):
    line = f"[{now()}] {msg}"
    print(line)
    try:
        Path.home().joinpath(".longhun/logs/codeql_listener.log").parent.mkdir(parents=True, exist_ok=True)
        with open(Path.home() / ".longhun" / "logs" / "codeql_listener.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ─────────────────────────── 熔断状态（任务5） ───────────────────────────

def load_af_state() -> dict:
    if AUTOFIX_STATE.exists():
        try:
            return json.loads(AUTOFIX_STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"date": datetime.now().strftime("%Y-%m-%d"), "count": 0,
            "consecutive_failures": 0, "paused": False, "paused_reason": ""}


def save_af_state(s: dict):
    CQL_DIR.mkdir(parents=True, exist_ok=True)
    AUTOFIX_STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def _reset_if_new_day(s: dict) -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    if s.get("date") != today:
        s = {"date": today, "count": 0, "consecutive_failures": 0,
             "paused": s.get("paused", False), "paused_reason": s.get("paused_reason", "")}
    return s


def check_circuit() -> dict:
    """熔断闸口：返回 {ok, reason}"""
    s = load_af_state()
    s = _reset_if_new_day(s)
    save_af_state(s)
    if s.get("paused"):
        return {"ok": False, "reason": f"自动修复已暂停: {s.get('paused_reason', '?')}（人工确认后重置 paused=false）"}
    if s.get("count", 0) >= DAILY_LIMIT:
        return {"ok": False, "reason": f"今日修复次数已达上限 {DAILY_LIMIT}/3，暂停自动修复"}
    return {"ok": True, "reason": ""}


def register_attempt() -> int:
    s = load_af_state()
    s = _reset_if_new_day(s)
    s["count"] = s.get("count", 0) + 1
    save_af_state(s)
    return s["count"]


def register_failure(issue_summary: str):
    s = load_af_state()
    s["consecutive_failures"] = s.get("consecutive_failures", 0) + 1
    if s["consecutive_failures"] >= MAX_RETRY:
        s["paused"] = True
        s["paused_reason"] = f"连续 {MAX_RETRY} 次修复失败（自动暂停，需人工介入）"
        record_shame_wall(f"CodeQL autofix 连续{MAX_RETRY}次失败暂停 · 最近: {issue_summary}")
    save_af_state(s)
    return s["consecutive_failures"]


def record_shame_wall(summary: str):
    """写入耻辱墙（与 lh_judge JSON 同构 · append-only）"""
    try:
        data = json.loads(SHAME_JSON.read_text(encoding="utf-8")) if SHAME_JSON.exists() else {
            "version": "1.1", "生成时间": now(), "总记录数": 0, "记录": []}
        data.setdefault("记录", [])
        data["记录"].append({
            "id": f"codeql-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "源名称": "codeql-autofix-failure",
            "源URL": "本地自动熔断",
            "指纹类型": "CI_FAILURE",
            "匹配内容摘要": summary[:100],
            "置信度": 100,
            "审计色": "🔴",
            "发现时间": now(),
            "状态": "自动暂停",
            "源类型": "autofix",
        })
        data["总记录数"] = len(data["记录"])
        SHAME_JSON.parent.mkdir(parents=True, exist_ok=True)
        SHAME_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"⚠ 已写入耻辱墙: {summary[:60]}")
    except Exception as e:
        log(f"耻辱墙写入失败: {e}", )


def backup_files(files: list) -> Path | None:
    """修复前备份（任务5）"""
    if not files:
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = BACKUP_ROOT / ts
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        p = ROOT / f
        if p.exists():
            try:
                shutil.copy2(p, dst / f.replace("/", "__"))
            except Exception as e:
                log(f"备份失败 {f}: {e}")
    log(f"备份 {len(files)} 个文件 → {dst}")
    return dst


# ─────────────────────────── 健康/拓扑验证 ───────────────────────────

def run_health() -> dict:
    p = subprocess.run([sys.executable, str(ROOT / "bin" / "lh.py"), "health", "--json"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    try:
        d = json.loads(p.stdout or "{}")
    except Exception:
        d = {}
    checks = d.get("checks", [])
    failed = [c for c in checks if not c.get("ok")]
    return {"ok": not failed, "total": len(checks), "failed": failed,
            "raw_rc": p.returncode}


def run_topo_verify() -> dict:
    p = subprocess.run([sys.executable, str(ROOT / "bin" / "lh.py"), "topo", "verify"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=600)
    out = (p.stdout or "") + (p.stderr or "")
    green = "🟢" in out or "通过" in out or "一致" in out or "OK" in out.upper() or p.returncode == 0
    return {"ok": p.returncode == 0 and green, "rc": p.returncode, "tail": out[-800:]}


# ─────────────────────────── 修复分派 + diff 应用 ───────────────────────────

def _load_results() -> dict:
    if not RESULTS.exists():
        return {}
    try:
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _forbidden(file: str) -> bool:
    return any(file.startswith(prefix + "/") for prefix in FORBIDDEN)


def apply_unified_diff(file: str, diff_text: str) -> dict:
    """应用单文件最小 diff（unified 简化版）。
    支持标准 @@ hunk 或 "旧行→新行" 形式。返回 {ok, reason, new_content?}"""
    p = ROOT / file
    if not p.exists():
        return {"ok": False, "reason": f"文件不存在: {file}"}
    content = p.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = list(lines)

    # 简化 diff: --- / +++ 头 后跟 - 行/+ 行 序列（无行号→按顺序匹配）
    minus = []
    plus = []
    hunks = []
    cur = None
    for ln in diff_text.splitlines():
        if ln.startswith("--- ") or ln.startswith("+++ ") or ln.startswith("@@ "):
            if cur is not None:
                hunks.append(cur)
            cur = {"minus": [], "plus": []}
        elif ln.startswith("-") and not ln.startswith("---"):
            if cur is None:
                cur = {"minus": [], "plus": []}
            cur["minus"].append(ln[1:])
        elif ln.startswith("+") and not ln.startswith("+++"):
            if cur is None:
                cur = {"minus": [], "plus": []}
            cur["plus"].append(ln[1:])
    if cur is not None:
        hunks.append(cur)
    if not hunks:
        return {"ok": False, "reason": "无可用 hunk（数字人未给出可自动应用的 diff）"}

    applied = 0
    for h in hunks:
        old_block = h["minus"]
        if not old_block:
            return {"ok": False, "reason": "hunk 无删除行·无法定位插入点（转人工）"}
        # 顺序查找首个匹配块
        idx = None
        for i in range(len(new_lines) - len(old_block) + 1):
            if new_lines[i:i + len(old_block)] == old_block:
                idx = i
                break
        if idx is None:
            return {"ok": False, "reason": f"hunk 未匹配到原文（文件已被改动或建议过期）·共{len(old_block)}行"}
        new_lines[idx:idx + len(old_block)] = h["plus"]
        applied += 1
    p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return {"ok": True, "reason": f"应用 {applied} 个 hunk · {file}"}


def _extract_diff(resp: str) -> str:
    """从数字人回复中抽取统一 diff 代码块"""
    m = re.search(r"```diff\s*\n(.*?)```", resp, re.S)
    if m:
        return m.group(1)
    m = re.search(r"```patch\s*\n(.*?)```", resp, re.S)
    if m:
        return m.group(1)
    return ""


def run_repair(issue: dict, dry_run: bool) -> dict:
    """单个 issue: 分派数字人 → 提取 diff → 应用（dry_run 只报告不写盘）"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import lh_dh_dispatch as dh
        ticket = dh.codeql_dispatch(issue)
        rec = {"rule_id": issue.get("rule_id"), "severity": issue.get("severity"),
               "file": issue.get("file"), "line": issue.get("line"),
               "dh_ipa": ticket["dh_ipa"], "dh_name": ticket["dh_name"],
               "type": ticket["type"], "priority": ticket["priority"]}
        if dry_run:
            rec["action"] = "分析(不落盘)"
            rec["task_preview"] = ticket["task"][:200]
            return {"ok": True, "mode": "dry", "record": rec}

        if _forbidden(issue.get("file", "")):
            rec["action"] = "拒绝(.github/ 保护区·需人工)"
            return {"ok": False, "mode": "forbidden", "record": rec}

        resp = dh.codeql_repair(issue)
        if resp.get("mode") == "fallback":
            rec["action"] = "数字人 API 未就绪·唤起指令已生成"
            rec["fallback"] = resp.get("detail", "")[:200]
            return {"ok": False, "mode": "fallback", "record": rec}
        if resp.get("mode") != "dh":
            rec["action"] = f"数字人执行异常: {resp.get('detail', '?')}"
            return {"ok": False, "mode": "error", "record": rec}

        text = resp.get("response") or ""
        diff = _extract_diff(str(text))
        if not diff:
            rec["action"] = "数字人未给出可自动应用 diff·需人工"
            rec["resp_head"] = str(text)[:200]
            return {"ok": False, "mode": "no-diff", "record": rec}

        app = apply_unified_diff(issue["file"], diff)
        if not app["ok"]:
            rec["action"] = f"diff 应用失败: {app['reason']}"
            return {"ok": False, "mode": "apply-fail", "record": rec}
        rec["action"] = app["reason"]
        rec["changed"] = True
        return {"ok": True, "mode": "applied", "record": rec}
    except Exception as e:
        return {"ok": False, "mode": "exception", "record": {"rule_id": issue.get("rule_id"),
                "file": issue.get("file"), "action": f"异常: {str(e)[:120]}"}}


# ─────────────────────────── 修复日志 ───────────────────────────

def append_fix_log(entry: dict):
    """fix log append-only（任务2-5 日志落点）"""
    data = []
    if FIX_LOG.exists():
        try:
            data = json.loads(FIX_LOG.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []
    entry["ts"] = now()
    data.append(entry)
    FIX_LOG.parent.mkdir(parents=True, exist_ok=True)
    FIX_LOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_fix_log() -> list:
    if FIX_LOG.exists():
        try:
            d = json.loads(FIX_LOG.read_text(encoding="utf-8"))
            return d if isinstance(d, list) else []
        except Exception:
            return []
    return []


# ─────────────────────────── PR 提交（任务3） ───────────────────────────

def resolve_token() -> tuple:
    try:
        p = subprocess.run([sys.executable, str(ROOT / "bin" / "lh_vault.py"), "get", "github-pat"],
                           capture_output=True, text=True, timeout=15)
        out = (p.stdout or "").strip().splitlines()
        if p.returncode == 0 and out:
            return out[-1].strip(), "vault"
    except Exception:
        pass
    try:
        p = subprocess.run(["security", "find-internet-password", "-s", "github.com", "-a", "UID9622", "-w"],
                           capture_output=True, text=True, timeout=10)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip(), "Keychain"
    except Exception:
        pass
    return "", ""


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True, timeout=120)


def create_pr_branch(commit_msg: str, title: str) -> dict:
    """基于 orphan_main 建 codeql-fix- 分支并提交 push。返回 {ok, branch, pr_url?}"""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch = f"codeql-fix-{ts}"
    # 远端最新
    git("fetch", "gh-ssh", "orphan_main")
    git("checkout", "-b", branch, "gh-ssh/orphan_main")
    git("add", "-A")
    r = git("commit", "-m", commit_msg, "--no-verify")
    if r.returncode != 0:
        log(f"commit 失败: {(r.stderr or '')[-300:]}")
        git("checkout", "orphan_main")
        return {"ok": False, "branch": branch, "reason": (r.stderr or "")[-200:]}
    p = git("push", "gh-ssh", branch)
    if p.returncode != 0:
        log(f"push 失败: {(p.stderr or '')[-300:]}")
        git("checkout", "orphan_main")
        return {"ok": False, "branch": branch, "reason": (p.stderr or "")[-200:]}
    git("checkout", "orphan_main")
    # PR
    token, _src = resolve_token()
    if not token:
        return {"ok": True, "branch": branch, "reason": "已 push·无 token 建 PR（人工创建）"}
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/UID9622/longhun-system/pulls",
            data=json.dumps({"title": title, "head": branch, "base": "orphan_main",
                             "body": "🤖 CodeQL 自动响应闭环: 数字人协作修复扫描告警\n\n"
                                     "生成时间: " + now() + "\n\n> 由 `lh codeql autofix` 自动生成 · 请人工审阅后合并"}).encode())
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/vnd.github+json")
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 防 socks5h 劫持
        with opener.open(req, timeout=30) as r2:
            d = json.loads(r2.read().decode())
            return {"ok": True, "branch": branch, "pr_url": d.get("html_url"), "pr_number": d.get("number")}
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        return {"ok": True, "branch": branch, "reason": f"PR 创建失败 HTTP {e.code}: {body}"}
    except Exception as e:
        return {"ok": True, "branch": branch, "reason": f"PR 创建异常: {str(e)[:150]}"}


# ─────────────────────────── autofix 主流程 ───────────────────────────

def cmd_autofix(dry_run: bool, pr_only: bool, auto_merge: bool):
    print(f"\n  🤖 CodeQL 自动修复 " + ("[dry-run·仅分析]" if dry_run else
          ("[pr-only·修复+建PR]" if pr_only else "[auto-merge·全自动]")) + "\n")

    results = _load_results()
    alerts = results.get("alerts", [])
    if not alerts:
        print("  ℹ️ 无已缓存扫描结果。请先运行: lh codeql fetch")
        print("  💡 也可直接: lh codeql listen --autofix（监听+自动触发）")
        return 0

    if not dry_run:
        gate = check_circuit()
        if not gate["ok"]:
            print(f"  🔴 熔断闸: {gate['reason']}")
            return 2
        register_attempt()   # 每次真实 autofix 运行记 1 次（日上限 3）

    # 按严重度排序：critical > high > medium > low
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "error": 1,
             "warning": 2, "note": 3}
    alerts.sort(key=lambda a: order.get(a.get("severity", "low"), 9))
    total = len(alerts)
    print(f"  📋 待修复告警 {total} 个（{results.get('groups', {})}）\n")

    # 备份（真实修复前）
    if not dry_run:
        files = sorted({a["file"] for a in alerts if a.get("file") and not _forbidden(a.get("file", ""))})
        backup_files(files)

    ok_count = 0
    hard_fail = 0     # 硬失败（可自动修复但失败）计数
    summary = []
    for i, a in enumerate(alerts, 1):
        rec = run_repair(a, dry_run=dry_run)
        r = rec.get("record", {})
        mark = "✅" if rec.get("ok") else ("⏭️" if rec.get("mode") == "forbidden" else "❌")
        summary.append(f"{mark} [{r.get('severity', '?')}] {r.get('rule_id', '?')} "
                       f"{r.get('file', '?')}:{r.get('line', '?')} → {r.get('dh_name', '?')} "
                       f"({rec.get('mode', '?')})")
        if rec.get("ok"):
            ok_count += 1
        elif rec.get("mode") in ("apply-fail", "exception", "no-diff", "error"):
            hard_fail += 1
        if not dry_run:
            append_fix_log({**r, "mode": rec.get("mode"), "repo": DEFAULT_REPO,
                            "run_id": results.get("run_id")})
        print(f"    {i}/{total} {mark} {r.get('rule_id', '?')} {r.get('file', '?')}:{r.get('line', '?')}"
              f" → {r.get('dh_name', '?')} · {r.get('action', rec.get('mode', '?'))}")

    # 熔断判定（整轮维度）：一轮成功修复=清零；整轮无成功且全部硬失败→计失败
    if not dry_run:
        if ok_count > 0:
            s = load_af_state()
            s["consecutive_failures"] = 0
            save_af_state(s)
        elif total > 0 and hard_fail == total:
            register_failure(alerts[0].get("rule_id", "?") + " 等全部硬失败")

    if dry_run:
        print("\n  ── dry-run 修复计划 ──")
        for s in summary:
            print(f"    {s}")
        print(f"\n  ✅ dry-run 完成：{ok_count}/{total} 个可自动修复 · 未提交任何改动")
        return 0

    # 汇总 + 验证
    print("\n  🩺 健康验证: lh health --json ...")
    h = run_health()
    if not h["ok"]:
        print(f"  🔴 健康检查失败（{h['total']} 项中 {len(h['failed'])} 项挂）→ 不提交")
        for f in h["failed"]:
            print(f"     ✗ {f.get('name', '?')}: {f.get('detail', '')[:80]}")
        register_failure("health 检查未全绿")
        return 3
    print(f"  ✅ 健康检查通过（{h['total']} 项全绿）")

    print("  🕸️ 拓扑验证: lh topo verify ...")
    t = run_topo_verify()
    if not t["ok"]:
        print(f"  🔴 拓扑验证失败 → 不提交\n{t['tail']}")
        register_failure("lh topo verify 未通过")
        return 3
    print("  ✅ 拓扑验证通过")

    # 未产生改动 → 无 PR
    changed = [a for a in alerts if not _forbidden(a.get("file", ""))]
    if not changed:
        print("  ⚠ 无待修文件（全部在保护区或空）→ 不建 PR")
        return 0

    # 提交 PR
    print("\n  🔀 创建修复分支并提交 PR ...")
    commit_msg = (f"🤖 [autofix] CodeQL 扫描问题自动修复 · {now()}\n\n"
                  f"修复 {ok_count}/{total} 告警 · 数字人协作分派\n"
                  f"run: {results.get('run_id')} · conclusion: {results.get('conclusion')}\n\n"
                  f"Generated by lh codeql autofix (龍魂 CodeQL 自动响应闭环 v1.0)")
    pr = create_pr_branch(commit_msg, "[autofix] CodeQL 扫描问题自动修复")
    if pr.get("pr_url"):
        print(f"  ✅ PR 已创建: {pr['pr_url']}")
        append_fix_log({"event": "pr_created", "branch": pr["branch"], "pr_url": pr["pr_url"],
                        "ok_count": ok_count, "total": total})
    elif pr.get("reason"):
        print(f"  🟡 分支已 push（{pr['branch']}）· PR 需人工: {pr['reason']}")
    else:
        print(f"  🟡 push 结果: {pr}")

    if auto_merge and pr.get("pr_url"):
        print("  ⚠ --auto-merge 需临时降分支保护审批，建议人工执行 Merge；本版本输出 PR 待审")
    return 0


# ─────────────────────────── dashboard（任务6） ───────────────────────────

def _sev_badge(count: int) -> str:
    if not count:
        return ""
    if count.get("critical", 0) or count.get("high", 0):
        return "🔴"
    if count.get("medium", 0) or count.get("warning", 0) or count.get("error", 0):
        return "🟡"
    return "🟢"


def cmd_dashboard() -> int:
    st = load_state_json()
    results = _load_results()
    fix_log = load_fix_log()
    af = load_af_state()

    groups = st.get("issue_counts", {}) or results.get("groups", {})
    badge = "🔴" if af.get("paused") else _sev_badge(groups) or "🟢"
    run_status = st.get("run_status") or st.get("status") or ("completed" if results.get("fetched_at") else "idle")
    status_zh = {"queued": "等待", "in_progress": "进行中", "completed": "完成",
                 "idle": "空闲", "unknown": "未知"}.get(run_status, run_status)

    lines = []
    lines.append("# 🐉 CodeQL 自动响应 · 状态面板")
    lines.append("")
    lines.append(f"> 生成时间: {now()} · {badge} 状态徽章")
    lines.append(f"> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰")
    lines.append(f"> DNA: #龍芯⚡️2026-09-03-CODEQL-DASHBOARD-v1.0-UID9622")
    lines.append("")
    lines.append("## 一、扫描状态")
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| 状态 | {status_zh} ({run_status}) |")
    lines.append(f"| 结论 | {st.get('conclusion') or results.get('conclusion') or '—'} |")
    lines.append(f"| run # | {st.get('run_id') or results.get('run_id') or '—'} |")
    lines.append(f"| head sha | {st.get('head_sha') or results.get('head_sha') or '—'} |")
    lines.append(f"| 拉取时间 | {results.get('fetched_at') or st.get('fetched_at') or '—'} |")
    lines.append(f"| 告警分组 | {groups or '—'} |")
    lines.append("")
    lines.append("## 二、告警清单（最近拉取）")
    lines.append("")
    alerts = results.get("alerts", [])
    if alerts:
        lines.append("| 级别 | 规则 | 位置 | 描述 |")
        lines.append("|---|---|---|---|")
        for a in alerts[:20]:
            lines.append(f"| {a.get('severity', '?')} | `{a.get('rule_id', '?')}` | "
                         f"{a.get('file', '?')}:{a.get('line', '?')} | "
                         f"{(a.get('description') or '')[:60]} |")
        if len(alerts) > 20:
            lines.append(f"| … | 共 {len(alerts)} 条 | | |")
    else:
        lines.append("_暂无告警缓存（lh codeql fetch 后更新）_")
    lines.append("")
    lines.append("## 三、最近修复记录")
    lines.append("")
    if fix_log:
        lines.append("| 时间 | 事件 | 规则 | 位置 | 数字人 | 结果 |")
        lines.append("|---|---|---|---|---|---|")
        for e in fix_log[-15:]:
            lines.append(f"| {e.get('ts', '?')} | {e.get('event', e.get('mode', 'fix'))} | "
                         f"`{e.get('rule_id', e.get('dh_name', '—'))}` | "
                         f"{e.get('file', '—')}:{e.get('line', '—')} | {e.get('dh_name', '—')} | "
                         f"{e.get('action', e.get('pr_url', '—'))[:40]} |")
    else:
        lines.append("_暂无修复记录_")
    lines.append("")
    lines.append("## 四、熔断状态")
    lines.append("")
    lines.append("| 项 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| 暂停 | {'是 · ' + af.get('paused_reason', '') if af.get('paused') else '否'} |")
    lines.append(f"| 今日修复次数 | {af.get('count', 0)}/{DAILY_LIMIT} |")
    lines.append(f"| 连续失败 | {af.get('consecutive_failures', 0)}/{MAX_RETRY} |")
    lines.append("")
    lines.append("---")
    lines.append("> 🐉 龍魂 CodeQL 自动响应闭环 v1.0 · GPG 签名见 .asc")

    CQL_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD.write_text("\n".join(lines), encoding="utf-8")
    # GPG 签名
    try:
        p = subprocess.run([sys.executable, str(ROOT / "bin" / "lh_gpg_sign.py"), "sign", "--force", str(DASHBOARD)],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        sign_note = "✅" if p.returncode == 0 else f"签名异常 rc={p.returncode}"
    except Exception as e:
        sign_note = f"签名跳过: {str(e)[:60]}"
    print(f"  ✅ 面板已生成: {DASHBOARD} {sign_note}")
    print("\n".join(lines[:14]))
    print("  ... (完整见文件)")
    return 0


def load_state_json() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


# ─────────────────────────── main ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·CodeQL 自动修复引擎 v1.0")
    ap.add_argument("action", nargs="?", choices=["autofix", "dashboard"],
                    help="autofix=修复并提交 / dashboard=状态面板")
    ap.add_argument("--dry-run", action="store_true", help="仅分析不提交")
    ap.add_argument("--pr-only", action="store_true", help="修复+创建 PR（默认·不自动合并）")
    ap.add_argument("--auto-merge", action="store_true", help="创建 PR 并尝试自动合并")
    args = ap.parse_args()

    if args.action == "dashboard":
        return cmd_dashboard()
    # 默认 autofix
    dry = args.dry_run
    auto = args.auto_merge
    pr_only = args.pr_only and not auto
    return cmd_autofix(dry_run=dry, pr_only=pr_only, auto_merge=auto)


if __name__ == "__main__":
    sys.exit(main())
