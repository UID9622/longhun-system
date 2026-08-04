#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·底线一：德在技术前 检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHECK-VIRTUE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

检测代码中是否含有榨取用户注意力、诱导成瘾、过度收集数据的设计模式。
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SYSTEM_ROOT = Path(__file__).parent.parent

# 技术无德模式
DARK_PATTERNS = [
    (r"infinite.?scroll", "🔴", "无限滚动陷阱"),
    (r"autoplay\s*=", "🔴", "自动播放"),
    (r"notification\s*spam|push.*notification.*loop", "🔴", "通知骚扰"),
    (r"dark.?pattern|deceptive.?design", "🔴", "暗黑模式"),
    (r"dopamine|addiction|addictive", "🔴", "成瘾设计"),
    (r"fear\s*of\s*missing|FOMO|scarcity.*countdown", "🔴", "制造焦虑/稀缺"),
    (r"collection.*all.*data|harvest.*data|silent.*upload", "🔴", "暗地采集数据"),
    (r"force.*login|mandatory.*account", "🟡", "强制登录/注册"),
    (r"hidden.*fee|surprise.*charge", "🔴", "隐藏收费"),
    (r"dark.?money|grey.*revenue", "🔴", "灰色收入路径"),
    (r"track\s*every|silent.*track|stealth.*track", "🔴", "隐形追踪"),
    (r"algorithm\s*manipulat|bias.*profit", "🔴", "算法操纵盈利"),
    (r"sell.*user.*data|monetize.*privacy", "🔴", "售卖用户数据"),
    (r"price\s*discriminat|杀熟", "🔴", "价格歧视/杀熟"),
    (r"fake.*review|bot.*account|sock.?puppet", "🔴", "虚假评价/水军"),
    (r"attention.*extract|time.*sink.*design", "🟡", "注意力榨取设计"),
    (r"nudge.*towards.*spend|impulse.*buy.*trigger", "🟡", "诱导消费"),
]

EXCLUDED_FILES = {
    "bin/lh_check_virtue.py",
    "bin/lh_deben_audit.py",
    "01_protocols/LH-DEBEN-AUDIT-v1.0.md",
}

EXCLUDED_DIRS = [
    "_archive/", "_work/", "models/", "data/training/",
    "docs/", "03_知識圖譜/", "01_技能庫/downloads_archive/",
]


class VirtueChecker:
    """德在技术前 — 底线1检测"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def check(self) -> Dict[str, Any]:
        hits: List[Dict] = []
        files_scanned = 0

        for f in self.root.rglob("*.py"):
            rel = str(f.relative_to(self.root))
            if rel in EXCLUDED_FILES:
                continue
            if any(rel.startswith(d) for d in EXCLUDED_DIRS):
                continue

            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                files_scanned += 1
                for pattern, severity, label in DARK_PATTERNS:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        hits.append({
                            "file": rel,
                            "pattern": pattern,
                            "severity": severity,
                            "label": label,
                            "matches": len(matches),
                        })
            except Exception:
                pass

        # 判定
        red_count = sum(1 for h in hits if h["severity"] == "🔴")
        yellow_count = sum(1 for h in hits if h["severity"] == "🟡")

        if red_count > 0:
            status = "🔴"
            verdict = f"触碰{red_count}条红线 — 发布前必须修复"
        elif yellow_count > 0:
            status = "🟡"
            verdict = f"发现{yellow_count}条警告 — 建议人工审查"
        else:
            status = "🟢"
            verdict = "德在技术前 — 通过"

        return {
            "底线": "德在技术前",
            "状态": status,
            "判定": verdict,
            "检测项": len(DARK_PATTERNS),
            "扫描文件": files_scanned,
            "命中": len(hits),
            "🔴": red_count,
            "🟡": yellow_count,
            "详情": hits[:20],
        }


if __name__ == "__main__":
    import json
    checker = VirtueChecker()
    result = checker.check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["状态"] == "🟢" else 1)
