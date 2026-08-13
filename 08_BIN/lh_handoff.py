#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·己未·癸酉-HANDOFF-CLI-v1.0-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
lh_handoff — 跨 AI 窗口会话交接引擎（Kimi/CodeBuddy/Claude/任何后来者）
上位协议: 01_protocols/LH-AI-HANDOFF-v1.0.md

用法:
    python3 08_BIN/lh_handoff.py save --from kimi --summary "..." --next "..."
    python3 08_BIN/lh_handoff.py load [--file <文件名>]
    python3 08_BIN/lh_handoff.py list
"""
import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF_DIR = ROOT / "12_DOCS" / "handoffs"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _load_rizhu():
    core_path = ROOT / "05_ENGINES" / "core"
    if str(core_path) not in sys.path:
        sys.path.insert(0, str(core_path))
    try:
        import rizhu_core
        return rizhu_core
    except Exception:
        return None


def _ganzhi() -> str:
    rz = _load_rizhu()
    if rz is not None:
        try:
            return rz.sizhu_ganzhi(datetime.now())
        except Exception:
            pass
    return "丙午·甲申·辛丑·坤卦"


def _dna(suffix: str) -> str:
    rz = _load_rizhu()
    if rz is not None:
        try:
            return rz.quick_dna(datetime.now(), suffix, "v1.0", "UID9622")
        except Exception:
            pass
    return "#龍芯⚡️" + _ganzhi() + "-" + suffix + "-UID9622"


def _gpg_sign(plain_path: Path) -> Path:
    asc_path = plain_path.with_suffix(plain_path.suffix + ".asc")
    cmd = [
        "gpg", "--batch", "--yes", "--armor",
        "--local-user", GPG_KEY,
        "--detach-sign", "--output", str(asc_path),
        str(plain_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("GPG 签名失败: " + r.stderr)
    return asc_path


def _git_status() -> str:
    r = subprocess.run(["git", "-C", str(ROOT), "status", "--short"],
                       capture_output=True, text=True)
    lines = [ln.strip() for ln in r.stdout.strip().splitlines() if ln.strip()]
    return "\n".join(lines) if lines else "（工作区干净）"


def cmd_save(args) -> int:
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    gz = _ganzhi()
    src = args.src or "AI"
    dna = _dna("HANDOFF-" + src + "-v1.0")
    fname = "HANDOFF-" + gz + "-" + src + "-v1.0.md"
    fpath = HANDOFF_DIR / fname
    content = (
        "# 🐉 龍魂 · AI 窗口会话交接包\n\n"
        "**DNA:** `" + dna + "`\n"
        "**确认码:** `" + CONFIRM + "`\n"
        "**GPG:** `" + GPG_KEY + "`\n"
        "**三色:** 🟢 通过\n"
        "**上一窗口:** " + src + "\n"
        "**交接时间:** `" + stamp + "`\n\n"
        "---\n\n"
        "## 一、会话摘要\n\n" + (args.summary or "（待填写）") + "\n\n"
        "## 二、TODO 状态\n\n" + (args.todo or "（待填写）") + "\n\n"
        "## 三、关键上下文\n\n" + (args.context or "（待填写）") + "\n\n"
        "## 四、未验证假设\n\n" + (args.assumptions or "1. （待填写）") + "\n\n"
        "## 五、本地未提交改动\n\n```\n" + _git_status() + "\n```\n\n"
        "## 六、下一步建议\n\n" + (args.next or "（待填写）") + "\n\n"
        "---\n\n🐉 **" + gz + "·🟢**\n"
    )
    fpath.write_text(content, encoding="utf-8")
    asc = _gpg_sign(fpath)
    print("✅ 交接包已写入: " + fpath.relative_to(ROOT).as_posix())
    print("✅ GPG 签名: " + asc.relative_to(ROOT).as_posix())
    print("👉 下一 AI 窗口进场执行: lh handoff load")
    return 0


def cmd_load(args) -> int:
    files = sorted(HANDOFF_DIR.glob("HANDOFF-*.md"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("❌ 无交接包。收尾窗口请先执行: lh handoff save")
        return 1
    target = files[0]
    if args.filename:
        cand = HANDOFF_DIR / args.filename
        if not cand.exists():
            try:
                idx = int(args.filename)
                cand = files[idx - 1]
            except (ValueError, IndexError):
                pass
        if not cand.exists():
            print("❌ 找不到交接包: " + args.filename)
            return 1
        target = cand
    print("📤 读取交接包: " + target.relative_to(ROOT).as_posix())
    print("=" * 60)
    print(target.read_text(encoding="utf-8"))
    return 0


def cmd_list(_args) -> int:
    files = sorted(HANDOFF_DIR.glob("HANDOFF-*.md"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("❌ 无交接包")
        return 1
    print("📂 历史交接包（" + str(len(files)) + " 个，最新在前）:")
    for i, p in enumerate(files, 1):
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print("  " + str(i) + ". " + p.name + "  [" + mtime + "]")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="龍魂跨AI窗口交接引擎 · LH-AI-HANDOFF-v1.0 协议落地",
        add_help=False, allow_abbrev=False)
    sub = parser.add_subparsers(dest="cmd")

    sp = sub.add_parser("save")
    sp.add_argument("--from", dest="src", default="AI", help="上一窗口名")
    sp.add_argument("--summary", default="", help="会话摘要")
    sp.add_argument("--todo", default="", help="TODO 状态表")
    sp.add_argument("--context", default="", help="关键上下文")
    sp.add_argument("--assumptions", default="", help="未验证假设")
    sp.add_argument("--next", default="", help="下一步建议")
    sp.set_defaults(func=cmd_save)

    lp = sub.add_parser("load")
    lp.add_argument("--file", dest="filename", default="", help="指定交接包文件")
    lp.set_defaults(func=cmd_load)

    lst = sub.add_parser("list")
    lst.set_defaults(func=cmd_list)

    args = parser.parse_args()
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
