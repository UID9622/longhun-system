# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 压缩守护进程 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-COMPRESS-WATCHDOG-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
依赖: bin/compress_all.py（全库扫描压缩引擎）

后台监控：compress 类受管文件超限 → 自动压缩；report 类超限 → 仅列出。
默认只报告不压，--run 才真压缩（安全优先）。

用法:
    python3 bin/compress_watchdog.py                # 60s 轮询·只报告超限
    python3 bin/compress_watchdog.py --run          # 60s 轮询·compress类超限自动压
    python3 bin/compress_watchdog.py --interval 300 # 5 分钟轮询
"""

import argparse
import time
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compress_all import collect_status, compress_all  # noqa: E402

DEFAULT_INTERVAL = 60


def watch(interval: int, do_compress: bool):
    print("👁️  压缩守护进程启动（Ctrl+C 退出）")
    print(f"   轮询间隔: {interval}s · 模式: {'自动压缩' if do_compress else '只报告'}")
    while True:
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            rows = collect_status()
            # compress 类超限 → 自动压；report 类超限 → 列出
            comp_over = [r for r in rows if r[3] > r[1] and r[2] == "compress" and r[4]]
            report_over = [r for r in rows if r[3] > r[1] and r[2] == "report" and r[4]]
            if comp_over or report_over:
                if comp_over:
                    print(f"\n[{ts}] 🗜️  compress类超限 {len(comp_over)} 个:")
                    for f, limit, *_ in comp_over:
                        print(f"    · {f}: {f.stat().st_size:,}B > {limit:,}B")
                    if do_compress:
                        results = compress_all(dry_run=False, audit=False)
                        print(f"[{ts}] ✅ 已压缩 {results['count']} 个，节省 {results['total_saved']:,} B")
                    else:
                        print(f"[{ts}] 🔕 只报告模式，未压缩（--run 开启自动压）")
                if report_over:
                    print(f"[{ts}] 📋 report类超限 {len(report_over)} 个（建议人工归档）:")
                    for f, limit, *_ in report_over:
                        print(f"    · {f}: {f.stat().st_size:,}B > {limit:,}B")
            # else: 静默（不刷屏）
        except KeyboardInterrupt:
            print("\n👁️  守护进程已停止")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️  守护异常: {e}")
        time.sleep(interval)


def main():
    ap = argparse.ArgumentParser(description="龍魂 · 压缩守护进程 v1.0")
    ap.add_argument("--run",       action="store_true", help="超限自动压缩（默认只报告）")
    ap.add_argument("--interval",  type=int, default=DEFAULT_INTERVAL, help="轮询间隔秒数（默认60）")
    args = ap.parse_args()
    watch(args.interval, args.run)


if __name__ == "__main__":
    main()
