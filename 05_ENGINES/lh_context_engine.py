#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 上下文感知引擎 (Context-Aware Sensing Engine)
DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-CONTEXT-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 主动感知当前会话上下文 —— 当前目录、历史命令、打开文件、环境变量、git 分支等。
      不依赖外部 API，零费用，鲲鹏 ARM64 原生友好。
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / ".state" / "context_engine"
STATE_DIR.mkdir(parents=True, exist_ok=True)

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-CONTEXT-ENGINE-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _safe_run(cmd: List[str], timeout: int = 5) -> str:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=PROJECT_ROOT
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _get_git_branch(path: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=3,
            cwd=path if path.is_dir() else path.parent,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def _get_recent_files(path: Path, n: int = 20, pattern: str = "*") -> List[str]:
    """获取最近修改的 n 个文件（递归），鲲鹏友好：不依赖 fswatch/inotify"""
    try:
        # 优先使用系统 find 命令，速度比 Python rglob 快一个数量级
        import shutil
        if shutil.which("find"):
            cmd = [
                "find", str(path),
                "-maxdepth", "4",
                "-type", "f",
                "-name", pattern.replace("*.", "*."),
                "!", "-path", "*/.git/*",
                "-print0",
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            raw = result.stdout.decode("utf-8", errors="ignore")
            files = [Path(p) for p in raw.split("\0") if p]
            files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return [str(p.relative_to(path)) for p in files[:n]]
    except Exception:
        pass

    # Fallback：限制深度的 Python 递归
    try:
        files: List[Path] = []
        for root, dirs, filenames in os.walk(path, topdown=True):
            # 限制深度
            depth = root[len(str(path)):].count(os.sep)
            if depth >= 4:
                del dirs[:]
                continue
            if ".git" in dirs:
                dirs.remove(".git")
            for fn in filenames:
                if pattern == "*" or fn.endswith(pattern.lstrip("*")):
                    files.append(Path(root) / fn)
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return [str(p.relative_to(path)) for p in files[:n]]
    except Exception:
        return []


def _get_shell_history(limit: int = 50) -> List[str]:
    """读取当前 shell 历史（支持 bash/zsh），仅本地，不上传"""
    history_files = []
    home = Path.home()
    shell = os.environ.get("SHELL", "").lower()
    if "zsh" in shell:
        history_files.append(home / ".zsh_history")
    elif "bash" in shell:
        history_files.append(home / ".bash_history")
    else:
        history_files.extend([home / ".zsh_history", home / ".bash_history"])

    lines: List[str] = []
    for hf in history_files:
        if hf.exists():
            try:
                raw = hf.read_text(encoding="utf-8", errors="ignore").splitlines()
                for line in raw:
                    # zsh history 格式：: 1234567890:0;command
                    cleaned = re.sub(r"^:\s*\d+:\d+;", "", line.strip())
                    if cleaned:
                        lines.append(cleaned)
                if lines:
                    break
            except Exception:
                continue
    return lines[-limit:]


def capture_context(extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """捕获当前会话上下文"""
    cwd = Path.cwd()
    ctx = {
        "dna": ENGINE_DNA,
        "timestamp": now_iso(),
        "session_id": f"{UID}-{datetime.now(CST).strftime('%Y%m%d%H%M%S')}",
        "cwd": str(cwd),
        "project_root": str(PROJECT_ROOT),
        "git_branch": _get_git_branch(cwd),
        "env_snapshot": {
            k: v
            for k, v in os.environ.items()
            if k.startswith(("LH_", "LONGHUN_", "CNSH_")) or k in ("USER", "HOME", "SHELL")
        },
        "recent_files": _get_recent_files(PROJECT_ROOT, n=20, pattern="*.md"),
        "recent_py_files": _get_recent_files(PROJECT_ROOT, n=10, pattern="*.py"),
        "shell_history": _get_shell_history(limit=20),
        "active_goals": _read_active_goals(),
    }
    if extra:
        ctx.update(extra)
    return ctx


def _read_active_goals() -> List[Dict[str, str]]:
    """读取当前活跃目标（如果存在 .longhun/goals 目录）"""
    goals_dir = Path.home() / ".longhun" / "goals"
    goals: List[Dict[str, str]] = []
    if goals_dir.exists():
        for gf in sorted(goals_dir.glob("*.json"))[:5]:
            try:
                data = json.loads(gf.read_text(encoding="utf-8"))
                goals.append({"id": gf.stem, "objective": data.get("objective", "")[:80]})
            except Exception:
                continue
    return goals


def save_context(ctx: Dict[str, Any], label: str = "auto") -> Path:
    """保存上下文快照"""
    fname = f"{label}_{datetime.now(CST).strftime('%Y%m%d%H%M%S')}.json"
    fpath = STATE_DIR / fname
    fpath.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
    return fpath


def load_recent_contexts(limit: int = 10) -> List[Dict[str, Any]]:
    """读取最近上下文快照"""
    files = sorted(STATE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    contexts: List[Dict[str, Any]] = []
    for f in files[:limit]:
        try:
            contexts.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return contexts


def summarize_context(ctx: Dict[str, Any]) -> str:
    """生成上下文一句话摘要"""
    files = ctx.get("recent_files", [])
    branch = ctx.get("git_branch", "unknown")
    cwd = ctx.get("cwd", "")
    return (
        f"[{ENGINE_DNA}] 当前在 {cwd} ({branch} 分支)，"
        f"最近文件: {', '.join(files[:3]) if files else '无'}"
    )


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂上下文感知引擎")
    parser.add_argument("--save", action="store_true", help="保存当前上下文快照")
    parser.add_argument("--recent", action="store_true", help="显示最近上下文快照")
    parser.add_argument("--summary", action="store_true", help="输出一句话摘要")
    parser.add_argument("--label", default="auto", help="快照标签")
    args = parser.parse_args()

    if args.recent:
        for ctx in load_recent_contexts(limit=5):
            print(f"\n[{ctx.get('timestamp')}] {ctx.get('session_id')}")
            print(f"  cwd: {ctx.get('cwd')}")
            print(f"  recent: {', '.join(ctx.get('recent_files', [])[:3])}")
        return

    ctx = capture_context()
    if args.save:
        path = save_context(ctx, label=args.label)
        print(f"✅ 上下文已保存: {path}")
    if args.summary or not (args.save or args.recent):
        print(summarize_context(ctx))


if __name__ == "__main__":
    cli()
