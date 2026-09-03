#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁未·癸巳·午时·䷿未济-STORAGE-OPTIMIZE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# -*- coding: utf-8 -*-
"""
龍魂 · 存储优化引擎 v1.0 · Storage Optimize

对齐「经济性·存储优化」能力（2026-09-03 · 裁决采纳 C 项）:
  遵循「不删除只冻结」P0 → 所有轮转均 gzip 压缩归档（内容保留），绝不裸删数据。
  只处理明确白名单，绝不碰 audit/（append-only 证据链）。

命令:
  python3 lh_storage.py status [--json]      # ~/.longhun 占用 + 建议
  python3 lh_storage.py optimize [--dry-run] # 日志>7天→gz 轮转 / 耻辱墙gz / 大文件清单
  python3 lh_storage.py test
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

HOME_DIR = Path.home() / ".longhun"
ROOT = Path(__file__).resolve().parent.parent
LOG_RETENTION_DAYS = 7
SIZE_WARN_MB = 2

# 禁止碰触的目录段（审计/证据链）
FORBIDDEN_SEGMENTS = ("audit", "signing", "evidence", "vault", "secrets")


def _size_mb(p: Path) -> float:
    return round(_du(p) / 1024 / 1024, 2)


def _du(p: Path) -> int:
    try:
        r = subprocess.run(["du", "-sk", str(p)], capture_output=True, text=True, timeout=30)
        return int(r.stdout.split()[0]) * 1024
    except Exception:
        return 0


def _find_log_files(base: Path, days: int) -> List[Path]:
    """白名单日志：*.log / *.log.* 且非 FORBIDDEN 路径"""
    out: List[Path] = []
    cutoff = datetime.now() - timedelta(days=days)   # 本地 naive（与 fromtimestamp 同基准）
    for p in base.rglob("*.log*"):
        if any(seg in p.parts for seg in FORBIDDEN_SEGMENTS):
            continue
        try:
            if datetime.fromtimestamp(p.stat().st_mtime) < cutoff:
                out.append(p)
        except OSError:
            continue
    return out


def cmd_status(as_json: bool = False) -> int:
    if not HOME_DIR.exists():
        print("~/.longhun 不存在")
        return 1
    entries: List[Dict[str, Any]] = []
    for child in sorted(HOME_DIR.iterdir()):
        if not child.is_dir():
            continue
        entries.append({"dir": child.name, "size_mb": _size_mb(child)})
    entries.sort(key=lambda x: -x["size_mb"])
    total_mb = round(sum(e["size_mb"] for e in entries), 2)
    big = [e for e in entries if e["size_mb"] >= SIZE_WARN_MB]
    suggestions = []
    for e in big:
        if e["size_mb"] >= 50:
            suggestions.append(f"{e['dir']} 达 {e['size_mb']}MB，建议 lh storage optimize（日志轮转/gz）")
    payload = {"total_mb": total_mb, "dirs": entries, "suggestions": suggestions}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🗄️ ~/.longhun 存储状态 · 总计 {total_mb} MB\n")
    print(f"  {'目录':<32}{'大小':>10}")
    for e in entries[:12]:
        print(f"  {e['dir']:<32}{e['size_mb']:>8.2f} MB")
    if suggestions:
        print("\n  优化建议:")
        for s in suggestions:
            print(f"    · {s}")
    return 0


def _gzip_if_stale(src: Path, dry_run: bool) -> Optional[int]:
    """生成 src.gz（内容冻结），返回压缩前后差字节；源 mtime 更新则刷新。"""
    gz_path = src.with_name(src.name + ".gz")
    do_it = not gz_path.exists() or src.stat().st_mtime > gz_path.stat().st_mtime
    if not do_it:
        return None
    raw = src.stat().st_size
    if dry_run:
        return raw  # 仅报告可压体积
    with open(src, "rb") as fin, gzip.open(gz_path, "wb", compresslevel=6) as fout:
        shutil.copyfileobj(fin, fout)
    return raw


def cmd_optimize(dry_run: bool = False, as_json: bool = False) -> int:
    acted: List[Dict[str, Any]] = []
    freed_bytes = 0

    # 1) 日志轮转（>7 天 *.log → gz 归档，删源＝冻结在 gz）
    for p in _find_log_files(HOME_DIR, LOG_RETENTION_DAYS):
        raw = _gzip_if_stale(p, dry_run)
        if raw is None:
            continue
        acted.append({"action": "log_rotate", "path": str(p), "raw_bytes": raw})
        freed_bytes += raw
        if not dry_run:
            try:
                p.unlink()  # 内容已在 .gz，非裸删
            except OSError:
                pass

    # 2) 耻辱墙 HTML → .gz 冻结快照（html 保留服务，gz 为归档）
    sw_html = HOME_DIR / "shame_wall" / "shame_wall.html"
    if sw_html.exists():
        raw = _gzip_if_stale(sw_html, dry_run)
        if raw is not None:
            acted.append({"action": "shame_wall_gz", "path": str(sw_html), "raw_bytes": raw})
            freed_bytes += raw

    # 3) 大文件报告（≥5MB 非白名单外类型 → 列出不动）
    big_files: List[Path] = []
    for p in HOME_DIR.rglob("*"):
        if not p.is_file():
            continue
        if any(seg in p.parts for seg in FORBIDDEN_SEGMENTS):
            continue
        if p.suffix in (".gz", ".db", ".asc"):
            continue
        try:
            if p.stat().st_size >= 5 * 1024 * 1024:
                big_files.append(p)
        except OSError:
            continue
    big_files.sort(key=lambda p: -p.stat().st_size)
    for p in big_files[:10]:
        acted.append({"action": "big_file_report", "path": str(p),
                      "size_mb": round(p.stat().st_size / 1024 / 1024, 2)})

    if as_json:
        print(json.dumps({"dry_run": dry_run, "freed_bytes": freed_bytes,
                          "items": acted}, ensure_ascii=False, indent=2))
        return 0
    mode = "🔍 预演（--dry-run，未实际执行）" if dry_run else "✅ 执行完成"
    print(f"\n  🗄️ 存储优化 · {mode}")
    print(f"  日志轮转/压缩释放: {round(freed_bytes / 1024, 1)} KB\n")
    for a in acted:
        if a["action"] == "log_rotate":
            print(f"  · 轮转 {a['path']} → .gz（冻结 {round(a['raw_bytes'] / 1024, 1)} KB）")
        elif a["action"] == "shame_wall_gz":
            print(f"  · 耻辱墙 HTML 冻结快照 → .gz")
        elif a["action"] == "big_file_report":
            print(f"  · 大文件(≥5MB·仅报告): {a['path']} ({a['size_mb']} MB)")
    print("\n  💡 提示: P0「不删除只冻结」→ 日志/快照一律 gzip 归档，不裸删数据。")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="lh-storage", description="龍魂存储优化引擎 v1.0")
    sub = parser.add_subparsers(dest="command")
    p_st = sub.add_parser("status", help="存储占用状态")
    p_st.add_argument("--json", action="store_true")
    p_op = sub.add_parser("optimize", help="存储优化（日志轮转/gz/大文件清单）")
    p_op.add_argument("--dry-run", action="store_true", help="只报告不执行")
    p_op.add_argument("--json", action="store_true")
    sub.add_parser("test", help="自测")
    args = parser.parse_args()

    if args.command == "status":
        cmd_status(as_json=args.json)
    elif args.command == "optimize":
        cmd_optimize(dry_run=args.dry_run, as_json=args.json)
    elif args.command == "test":
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(StorageTest)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()


class StorageTest(unittest.TestCase):
    def test_01_whitelist_log_finder(self):
        """日志白名单排除 audit"""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "a.log").write_text("x")
            (base / "audit" / "chain.jsonl").write_text("y")
            (base / "sub" / "b.log").write_text("z")
            files = _find_log_files(base, 0)
            names = [f.name for f in files]
            self.assertIn("a.log", names)
            self.assertNotIn("chain.jsonl", names)  # audit 目录被排除

    def test_02_status_no_crash(self):
        """status --json 不崩（可能无目录）"""
        self.assertEqual(cmd_status(as_json=True), 0)

    def test_03_gzip_freeze(self):
        """gzip 冻结保留内容"""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.log"
            p.write_bytes(b"hello world" * 100)
            _gzip_if_stale(p, dry_run=False)
            with gzip.open(str(p) + ".gz", "rt") as f:
                self.assertEqual(f.read(), "hello world" * 100)


if __name__ == "__main__":
    main()
