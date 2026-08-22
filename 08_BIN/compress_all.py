# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 全库扫描压缩引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-COMPRESS-ALL-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
依赖: bin/memory_compress.py（P0-P5 评分 + 里程碑折叠 + 字节线达标）

安全设计（2026-08-21 修正）:
  - 受管文件分两类: compress=超限自动压 / report=超限只报告(人工决定)
  - 每日日志属 report——流水账被段落压缩会丢细节，正确动作是人工归档
  - COMMAND_INDEX.md 属 report——252KB 单一真相源，段落压缩会撕裂表格
  - 5MB 以上文件直接跳过（防 30MB 级大文件卡死）

用法:
    python3 bin/compress_all.py --audit     # 只扫描超限文件，不写
    python3 bin/compress_all.py --dry-run   # 预演压缩，不写文件
    python3 bin/compress_all.py --run       # 真压缩 compress 类超限文件
"""

import sys
from pathlib import Path

# 同目录导入 memory_compress（bin/ 下相对导入）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from memory_compress import compress_memory  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# ────────────────────────────────────────────────
# § 1  受管文件清单（按重要性排序）
#      (glob模式, 字节上限, 动作)
#      action: "compress"=超限自动压 | "report"=超限只报告
# ────────────────────────────────────────────────

MANAGED_FILES = [
    (".codebuddy/memory/MEMORY.md",      7_500, "compress"),  # 注入上限 7.5KB·唯一自动压缩目标
    (".codebuddy/COMMAND_INDEX.md",     12_000, "report"),    # 命令索引·超限报告不压(单一真相源)
    (".codebuddy/memory/2026-*.md",      5_000, "report"),    # 每日日志·超限报告(人工归档)
]

# 防护：大于该字节数的文件跳过（防 30MB 级大文件跑段落解析卡死）
MAX_SKIP_BYTES = 5 * 1024 * 1024  # 5MB


def collect_status() -> list:
    """扫描受管文件，返回 [(path, limit, action, size, over)] 全量状态。"""
    rows = []
    for pattern, limit, action in MANAGED_FILES:
        for f in sorted(ROOT.glob(pattern)):
            size = f.stat().st_size
            if size > MAX_SKIP_BYTES:
                rows.append((f, limit, action, size, False, "跳过>5MB"))
                continue
            over = size > limit
            rows.append((f, limit, action, size, over, ""))
    return rows


def compress_all(dry_run: bool = False, audit: bool = False) -> dict:
    """
    扫描受管文件：compress 类超限自动压，report 类只列清单。
    返回战报 dict: {compressed:[], reported:[], total_saved, count}
    """
    rows = collect_status()
    results = {"compressed": [], "reported": [], "skipped": [],
               "total_saved": 0, "count": 0}

    for f, limit, action, size, over, note in rows:
        if note:  # 跳过>5MB
            results["skipped"].append((str(f), size))
            continue
        if not over:
            # 只对 compress 类打印安全确认，report 类（日志/索引）静默
            if action == "compress":
                print(f"  ✅ {f.name}: {size:,}B ≤ {limit:,}B 安全")
            continue
        if action == "compress":
            print(f"\n⚠️  {f.name}: {size:,}B > {limit:,}B 阈值，触发压缩...")
            r = compress_memory(
                src          = f,
                target_bytes = limit,
                dry_run      = dry_run,
                audit_only   = audit,
            )
            saved = r["before_bytes"] - r["after_bytes"]
            results["compressed"].append((str(f), limit, r))
            results["total_saved"] += saved
            results["count"] += 1
            print(f"   🗜️  {r['before_bytes']:,}B → {r['after_bytes']:,}B (-{r['ratio']*100:.1f}%)")
        else:  # report —— 只记录不逐行打印（防刷屏），战报里汇总显示
            results["reported"].append((str(f), limit, size))

    return results


def print_summary(results: dict, mode: str):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"🗜️  战报 · 模式: {mode}")
    if results["compressed"]:
        print(f"  ✅ 已压缩 {len(results['compressed'])} 个 · 节省 {results['total_saved']:,} B")
    if results["reported"]:
        print(f"  📋 超限待处理 {len(results['reported'])} 个（建议人工归档/瘦身）:")
        for path, limit, size in results["reported"][:5]:
            print(f"     · {Path(path).name}: {size:,}B > {limit:,}B")
        if len(results["reported"]) > 5:
            print(f"     · … 等 {len(results['reported'])-5} 个")
    if results["skipped"]:
        print(f"  ⏭️  跳过>5MB {len(results['skipped'])} 个:")
        for path, size in results["skipped"]:
            print(f"     · {Path(path).name}: {size/1024/1024:.1f}MB")
    if not results["compressed"] and not results["reported"] and not results["skipped"]:
        print("  🟢 所有受管文件在安全线内")
    print(sep)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂 · 全库扫描压缩引擎 v1.0")
    ap.add_argument("--audit",    action="store_true", help="只扫描超限文件，不写")
    ap.add_argument("--dry-run",  action="store_true", help="预演压缩，不写文件")
    ap.add_argument("--run",      action="store_true", help="真压缩 compress 类超限文件")
    args = ap.parse_args()

    dry_run = args.dry_run or (not args.run and not args.audit)
    audit   = args.audit
    mode    = "审计（只扫描）" if audit else ("预演（不写文件）" if dry_run else "已压缩")

    print(f"🐉 龍魂 · 全库扫描压缩引擎 v1.0")
    print(f"受管文件: {len(MANAGED_FILES)} 组模式")
    for pattern, limit, action in MANAGED_FILES:
        print(f"  · {pattern:<32s} → {limit:,}B 上限 · {action}")

    results = compress_all(dry_run=dry_run, audit=audit)
    print_summary(results, mode)


if __name__ == "__main__":
    main()
