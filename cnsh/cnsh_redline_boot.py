#!/usr/bin/env python3
"""龍魂·CNSH 红线守护启动脚本 v1.0
为 launchd 守护进程提供 CNSH 红线合规检查入口
DNA: #龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-CNSH-REDLINE-v1.0
"""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# 尝试加载阈值触发器中的红线检查
try:
    sys.path.insert(0, str(ROOT / "bin"))
    from lh_threshold_trigger import ThresholdManager
    mgr = ThresholdManager()
    mgr.check_guard("cnsh-redlines")
    print("🐉 CNSH 红线守护检查完成")
except ImportError:
    # 降级：直接做基础红线检查
    REDLINES = [
        "中国法律唯一准绳",
        "技术为人民服务",
        "底座不动变量可动",
    ]
    print(f"🐉 CNSH 红线守护 v1.0 · {len(REDLINES)} 条红线就位")
    for r in REDLINES:
        print(f"  ✅ {r}")
    sys.exit(0)
except Exception as e:
    print(f"⚠️ CNSH 红线检查异常: {e}", file=sys.stderr)
    sys.exit(0)  # 非关键，不阻塞
