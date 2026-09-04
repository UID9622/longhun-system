#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷟恒-CODE-MEMORY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""🧬 源码记忆引擎 v1.0 — 全局记忆系统 A2（2026-09-04落地）

理念: 每次 git 变更（commit）自动留档 → 可追溯的源码历史。
与 lh timeline（操作时间轴）/ lh state（全局状态）互补：code=源码层·timeline=动作层。

数据: ~/.longhun/code_memory/<repo>/<commit_hash>.json
字段: timestamp(ISO+干支) / commit_hash / message / files_changed /
      diff_summary(+x/-y) / dna(干支+hash8) / task(关联 session active_task)
用法:
  lh code record [--message "xxx"]   → 记录当前 HEAD commit（post-commit 钩子自动调）
  lh code history [--repo <name>]    → 查看源码变更历史
  lh code diff <hash1> <hash2>       → 对比两次变更
  lh code status                     → 当前工作区与上次记录的差异
  lh code install-hooks              → 安装 post-commit 钩子（自动触发 record）
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 引擎间本地 import（lh_timeline.record / ganzhi_simple）路径注入：解析真实目录防 bin 软链偏差
_BIN_DIR = Path(__file__).resolve().parent
if str(_BIN_DIR) not in sys.path:
    sys.path.insert(0, str(_BIN_DIR))

ROOT = Path.home() / ".longhun"
CODE_DIR = ROOT / "code_memory"
SESSION = ROOT / "session_context.json"


def _run_git(args: list[str], cwd: str | None = None) -> str:
    try:
        r = subprocess.run(["git"] + args, capture_output=True, text=True,
                           cwd=cwd, timeout=20)
        return r.stdout.strip()
    except Exception:
        return ""


def _git_cwd() -> str:
    """lh.py 统一 cwd=项目根跑引擎·git 感知需取 shell 真实目录（PWD 透传·post-commit 钩子=仓库目录）"""
    return os.environ.get("PWD") or os.getcwd()


def repo_name(cwd: str | None = None) -> str:
    """仓库名: 取 remote origin 路径 · 无 remote 取目录名"""
    url = _run_git(["remote", "get-url", "origin"], cwd)
    if url:
        m = re.sub(r"\.git$", "", url).rstrip("/")
        # 支持 git@github.com:O/R / https://github.com/O/R 等
        m = re.sub(r".*[:/]", "", m)
        return m
    return Path(cwd or os.getcwd()).name


def _local_now():
    return datetime.now().astimezone()


def _session_task() -> str:
    try:
        if SESSION.exists():
            d = json.loads(SESSION.read_text(encoding="utf-8"))
            return (d.get("active_task") or "").strip()
    except Exception:
        pass
    return ""


def _safe_repo(repo: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", repo)


def _write(rec: dict, repo: str) -> Path:
    d = CODE_DIR / _safe_repo(repo)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{rec['commit_hash']}.json"
    p.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def cmd_record(message: str = "", silent: bool = False, cwd: str | None = None) -> int:
    """记录当前 HEAD commit（已存在同 hash 则跳过·防重）"""
    import lh_timeline as TL
    head = _run_git(["rev-parse", "HEAD"], cwd)
    if not head:
        print("  ❌ 当前目录不是 git 仓库或尚无 commit")
        return 1
    repo = repo_name(cwd)
    p = CODE_DIR / _safe_repo(repo) / f"{head}.json"
    if p.exists():
        if not silent:
            print(f"  ⏭️  {repo}@{head[:8]} 已记录")
        return 0
    if not message:
        message = _run_git(["log", "-1", "--format=%s"], cwd)
    files_raw = _run_git(["show", "--name-only", "--format=", "HEAD"], cwd)
    files = [f for f in files_raw.splitlines() if f.strip()]
    numstat = _run_git(["show", "--numstat", "--format=", "HEAD"], cwd)
    ins = dels = 0
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            if parts[0].isdigit():
                ins += int(parts[0])
            if parts[1].isdigit():
                dels += int(parts[1])
    now = _local_now()
    rec = {
        "timestamp": now.isoformat(),
        "ganzhi": TL.ganzhi_simple(now),
        "commit_hash": head,
        "short_hash": head[:8],
        "message": message,
        "repo": repo,
        "files_changed": files[:200],
        "diff_summary": f"+{ins}/-{dels} · {len(files)} files",
        "insertions": ins,
        "deletions": dels,
        "dna": f"#龍芯⚡️{head[:8]}-CODE-MEMORY-{len(files)}F",
        "task": _session_task(),
        "recorded_at": now.isoformat(),
    }
    _write(rec, repo)
    try:
        TL.record(f"code {repo}@{head[:8]} {message[:40]}", "code",
                  {"hash": head[:8], "repo": repo})
    except Exception:
        pass
    if not silent:
        print(f"  🧬 已记录 {repo}@{head[:8]} {rec['diff_summary']}")
    return 0


def cmd_history(repo_filter: str = "") -> int:
    if not CODE_DIR.exists():
        print("  🧬 源码记忆为空（lh code record 记录首个 commit 后可见）")
        return 0
    rows = []
    for repo_dir in sorted(CODE_DIR.iterdir()):
        if not repo_dir.is_dir():
            continue
        if repo_filter and repo_filter not in repo_dir.name:
            continue
        for f in sorted(repo_dir.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                rows.append((d.get("timestamp", ""), repo_dir.name, d))
            except Exception:
                continue
    rows.sort(reverse=True)
    if not rows:
        print("  🧬 无匹配记录")
        return 0
    print(f"  🧬 源码变更历史 · {len(rows)} 条\n")
    for ts, repo, d in rows[:30]:
        print(f"  {ts[:19]}  [{repo}] {d.get('short_hash')} {d.get('message', '')[:50]}"
              f" · {d.get('diff_summary', '')}")
    return 0


def _load_hashes(repo: str) -> list[str]:
    d = CODE_DIR / _safe_repo(repo)
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


def cmd_diff(h1: str, h2: str, repo: str = "") -> int:
    repo = repo or _run_git(["remote", "get-url", "origin"]).split("/")[-1].replace(".git", "") or "repo"
    if repo == "repo":
        repo = repo_name()
    target = CODE_DIR / _safe_repo(repo)
    if not target.exists():
        print(f"  ❌ {repo} 无源码记忆")
        return 1
    d1 = d2 = None
    for f in target.glob("*.json"):
        h = f.stem
        if h.startswith(h1):
            d1 = json.loads(f.read_text(encoding="utf-8"))
        if h.startswith(h2):
            d2 = json.loads(f.read_text(encoding="utf-8"))
    if not d1 or not d2:
        print(f"  ❌ 未找到 {h1} / {h2}（短哈希前8位即可）")
        return 1
    f1, f2 = set(d1.get("files_changed", [])), set(d2.get("files_changed", []))
    print(f"  🧬 {d1.get('repo')} {h1} vs {h2}\n")
    print(f"  [{h1[:8]}] {d1.get('timestamp','')[:19]} {d1.get('message','')}\n"
          f"      文件 {len(f1)} · {d1.get('diff_summary','')}")
    print(f"  [{h2[:8]}] {d2.get('timestamp','')[:19]} {d2.get('message','')}\n"
          f"      文件 {len(f2)} · {d2.get('diff_summary','')}")
    added = f2 - f1
    removed = f1 - f2
    if added:
        print(f"\n  ➕ 新增文件 ({len(added)}):")
        for f in sorted(added)[:15]:
            print(f"    {f}")
    if removed:
        print(f"\n  ➖ 移除文件 ({len(removed)}):")
        for f in sorted(removed)[:15]:
            print(f"    {f}")
    return 0


def cmd_status(cwd: str | None = None) -> int:
    repo = repo_name(cwd)
    dirty = _run_git(["status", "--porcelain"], cwd)
    lines = [l for l in dirty.splitlines() if l.strip()]
    head_full = _run_git(["rev-parse", "HEAD"], cwd)
    print(f"  🧬 {repo} @ {(head_full or '?')[:8]}")
    if lines:
        print(f"  🟡 工作区有 {len(lines)} 处未提交变更:")
        for l in lines[:15]:
            print(f"    {l[:90]}")
    else:
        print("  🟢 工作区干净")
    # 与上次记录对比（完整 hash 比对）
    hashes = _load_hashes(repo)
    if not hashes:
        print("  🧬 尚无源码记忆（首次 commit 后自动记录）")
        return 0
    last_h = hashes[-1]
    p = CODE_DIR / _safe_repo(repo) / f"{last_h}.json"
    if head_full and last_h == head_full:
        print(f"  🟢 已与上次记录同步（{last_h[:8]}）")
    else:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            print(f"  🟡 上次记录 {last_h[:8]} {d.get('message','')[:40]}（HEAD 已变·可 lh code record）")
        except Exception:
            pass
    return 0


MARKER = "# ===== lh code 源码记忆（install-hooks 自动安装）====="


def _hook_block() -> str:
    lh_script = Path(__file__).resolve().parent.parent / "bin" / "lh.py"
    if not lh_script.exists():
        lh_script = Path(__file__).resolve().parent / "lh.py"
    return (f"{MARKER}\n"
            f"{sys.executable} \"{lh_script}\" code record --silent >/dev/null 2>&1 || true\n"
            f"# ===== end lh code =====\n")


def cmd_install_hooks(cwd: str | None = None) -> int:
    """安装 post-commit 钩子 · 识别 core.hooksPath（全局生效目录）· 顶部插入且保留原钩子内容（如 LFS）"""
    git_dir = _run_git(["rev-parse", "--git-dir"], cwd)
    if not git_dir:
        print("  ❌ 当前目录不是 git 仓库")
        return 1
    base = Path(cwd or os.getcwd())
    hp = _run_git(["config", "--get", "core.hooksPath"], cwd)
    if hp:
        hooks_dir = Path(hp) if Path(hp).is_absolute() else base / hp
    else:
        hooks_dir = base / git_dir / "hooks"
    hook_file = hooks_dir / "post-commit"
    block = _hook_block()
    if hook_file.exists():
        old = hook_file.read_text(encoding="utf-8")
        if MARKER in old:
            print(f"  🟢 post-commit 钩子已含 lh code（{hook_file}）")
            return 0
        # 保留 shebang 在顶部，marker 块插其后（不破坏 LFS 等原逻辑）
        body = old
        shebang = ""
        if old.startswith("#!"):
            nl = old.find("\n")
            shebang = old[: nl + 1]
            body = old[nl + 1:]
        hook_file.write_text(shebang + block + "\n" + body, encoding="utf-8")
        print(f"  🧬 post-commit 顶部已插入 lh code（保留原内容 → {hook_file}）")
    else:
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_file.write_text("#!/bin/sh\n" + block, encoding="utf-8")
        print(f"  🧬 post-commit 钩子已安装 → {hook_file}")
    try:
        hook_file.chmod(0o755)
    except Exception:
        pass
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh code", description="🧬 源码记忆引擎")
    sub = ap.add_subparsers(dest="cmd")
    rc = sub.add_parser("record", help="记录当前 HEAD commit")
    rc.add_argument("--message", default="")
    rc.add_argument("--silent", action="store_true")
    hi = sub.add_parser("history", help="查看源码变更历史")
    hi.add_argument("--repo", default="")
    df = sub.add_parser("diff", help="对比两次变更")
    df.add_argument("hash1")
    df.add_argument("hash2")
    sub.add_parser("status", help="当前工作区与上次记录的差异")
    sub.add_parser("install-hooks", help="安装 post-commit 钩子")
    args = ap.parse_args()
    gwd = _git_cwd()
    if args.cmd in (None, "record"):
        return cmd_record(args.message, getattr(args, "silent", False), cwd=gwd)
    if args.cmd == "history":
        return cmd_history(args.repo)
    if args.cmd == "diff":
        return cmd_diff(args.hash1, args.hash2)
    if args.cmd == "status":
        return cmd_status(cwd=gwd)
    if args.cmd == "install-hooks":
        return cmd_install_hooks(cwd=gwd)
    print(f"  ❌ 未知子命令: {args.cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
