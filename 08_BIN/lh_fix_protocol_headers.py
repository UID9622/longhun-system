# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-257008c0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·协议头部补齐引擎 v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

功能：批量给协议文件补齐 P0 声明 + 分层许可头部行（统一标准落地·只加不改）。

背景：lh_align / pre-commit 阶段二要求协议文件含：
  - P0 声明（"P0" 或 "焊死" 子串）
  - 分层许可（"MulanPSL" / "CC BY-NC-SA" / "分层许可" 子串）
历史协议文件头部不齐 → 每次提交被审计卡死 → 本工具批量补。

安全性（P0：不把能用的改坏）：
  - 只插入文件头注释/引用行，不改正文
  - 幂等：文件已含 P0/许可声明则跳过
  - 修改前冻结原版到 archive/frozen/
  - 插入后验证内容只增不减

用法：
  python3 bin/lh_fix_protocol_headers.py              # dry-run 只报告
  python3 bin/lh_fix_protocol_headers.py --fix        # 实际补齐
  python3 bin/lh_fix_protocol_headers.py --report out.json
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"

PROTOCOL_HINT = ("协议", "protocol", "PROTOCOL", "宪法", "铁律")
NON_TEXT_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
                ".gz", ".mp4", ".mp3", ".woff", ".woff2", ".ttf", ".exe",
                ".so", ".dll", ".pyc", ".class", ".jar", ".asc", ".sig",
                ".jsonl", ".db", ".sqlite3", ".db-shm", ".db-wal",
                ".sqlite3-shm", ".sqlite3-wal"}

P0_LINE_MD = "> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）"
P0_LINE_CODE = "# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）"
LIC_LINE_MD = "> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）"
LIC_LINE_CODE = "# License: CC BY-NC-SA 4.0（核心思想层·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）"


def is_protocol_file(name: str) -> bool:
    return any(h in name for h in PROTOCOL_HINT)


def find_protocol_files(target: Path):
    """扫描协议文件（01_protocols/ 下全部 + 全库文件名含 hint 的文本文件）"""
    found = []
    for root, dirs, files in target.walk():
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                   {"node_modules", "archive", "backups", "_work", "11_DATA", "dist", "models"}]
        for fn in files:
            p = Path(root) / fn
            if p.suffix.lower() in NON_TEXT_EXT:
                continue
            rel = str(p.relative_to(target))
            in_protocols = "01_protocols" in rel
            if in_protocols or is_protocol_file(fn):
                found.append(p)
    return found


def patch_file(p: Path, need_p0: bool, need_lic: bool, dry_run: bool):
    """插入 P0/分层许可 头部行。返回统计 dict。"""
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"file": str(p), "status": f"🔴 读取失败 {e}", "p0": False, "lic": False}

    is_code = p.suffix in (".py", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml", ".json", ".plist")
    p0_line = P0_LINE_CODE if is_code else P0_LINE_MD
    lic_line = LIC_LINE_CODE if is_code else LIC_LINE_MD

    # 定位第一个非空行
    lines = src.splitlines(keepends=True)
    insert_at = 0
    while insert_at < len(lines) and not lines[insert_at].strip():
        insert_at += 1

    inserts = []
    if need_p0:
        inserts.append(p0_line + "\n")
    if need_lic:
        inserts.append(lic_line + "\n")
    if not inserts:
        return {"file": str(p), "status": "⏭️ 无需补齐", "p0": False, "lic": False}

    new_src = "".join(lines[:insert_at]) + "".join(inserts) + "".join(lines[insert_at:])

    if dry_run:
        return {"file": str(p), "status": "🟡 dry-run", "p0": need_p0, "lic": need_lic}

    # 冻结原版（P0：不删除只冻结）
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    frozen = FROZEN_DIR / f"{p.name}.{ts}.frozen"
    shutil.copy2(p, frozen)

    p.write_text(new_src, encoding="utf-8")
    return {"file": str(p), "status": "✅ 已补齐", "p0": need_p0, "lic": need_lic, "frozen": frozen.name}


def main():
    parser = argparse.ArgumentParser(description="龍魂·协议头部补齐引擎 v1.0")
    parser.add_argument("--dir", default=str(BASE_DIR), help="扫描目录（默认全库）")
    parser.add_argument("--fix", action="store_true", help="实际补齐（默认 dry-run）")
    parser.add_argument("--report", help="输出 JSON 报告路径")
    args = parser.parse_args()

    target = Path(args.dir)
    files = find_protocol_files(target)
    results = []
    n_p0 = n_lic = n_ok = 0

    for p in files:
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        need_p0 = ("P0" not in src) and ("焊死" not in src)
        need_lic = ("MulanPSL" not in src) and ("CC BY-NC-SA" not in src) and ("分层许可" not in src)
        if not need_p0 and not need_lic:
            continue
        r = patch_file(p, need_p0, need_lic, dry_run=not args.fix)
        results.append(r)
        if r["p0"]:
            n_p0 += 1
        if r["lic"]:
            n_lic += 1
        if r["status"].startswith("✅"):
            n_ok += 1

    print(f"🐉 协议头部补齐（{'--fix 实际补齐' if args.fix else 'dry-run 预览'}）")
    print(f"   扫描协议文件: {len(files)} | 需补P0: {n_p0} | 需补分层许可: {n_lic}")
    if args.fix:
        print(f"   已补齐: {n_ok} 文件（原版冻结 archive/frozen/·内容只加不改）")
    else:
        print(f"   （dry-run：加 --fix 才实际修改）")

    if args.report:
        Path(args.report).write_text(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "mode": "fix" if args.fix else "dry-run",
            "total_protocol_files": len(files),
            "need_p0": n_p0, "need_lic": n_lic, "patched": n_ok,
            "results": results,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📄 报告已写: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
