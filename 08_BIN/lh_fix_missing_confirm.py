#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·自动补确认码 v1.0
DNA: 由 bin/lh_dna_generator.py 生成
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

补齐调度器路由表中引用但 v1.0 缺失的修复脚本。
确认码是固定常量，直接写入即可（无需调用生成器）。
写入前冻结原文件（P0：不删除只冻结）。幂等，已有确认码则跳过。
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"
CONFIRM_LINE = "# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CONFIRM_MARK = "#CONFIRM🌌9622"


def fix_confirm(filepath: str) -> str:
    p = Path(filepath)
    if not p.exists():
        return f"❌ 文件不存在: {filepath}"

    content = p.read_text(encoding="utf-8", errors="replace")
    if CONFIRM_MARK in content:
        return f"⏭️ 已存在确认码: {filepath}"

    # 冻结原版
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    frozen_path = FROZEN_DIR / f"{p.name}.{ts}.frozen"
    shutil.copy2(p, frozen_path)

    # 有DNA行就插在其后，否则放文件头
    lines = content.splitlines(keepends=True)
    insert_at = 0
    for i, line in enumerate(lines[:20]):
        if line.startswith("# DNA:"):
            insert_at = i + 1
            break
    lines.insert(insert_at, CONFIRM_LINE + "\n")
    p.write_text("".join(lines), encoding="utf-8")
    return f"✅ 已补确认码: {filepath}（原版已冻结: {frozen_path.name}）"


def main() -> int:
    files = [f for f in sys.argv[1:] if f.strip()]
    if not files and not sys.stdin.isatty():
        files = [line.strip() for line in sys.stdin if line.strip()]
    if not files:
        print("没有待处理文件。")
        return 0

    ok = skipped = failed = 0
    for f in files:
        msg = fix_confirm(f)
        print(msg)
        if msg.startswith("✅"):
            ok += 1
        elif msg.startswith("⏭️"):
            skipped += 1
        else:
            failed += 1
    print(f"\n📊 补确认码总结: 成功 {ok} | 跳过 {skipped} | 失败 {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
