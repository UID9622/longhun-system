#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·底线四：信息主权不可让渡 检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHECK-SOVEREIGNTY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

检测所有API调用和网络请求，确保用户数据不出本地。
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SYSTEM_ROOT = Path(__file__).parent.parent

# 数据出境风险模式
DATA_LEAK_PATTERNS = [
    # 云端API调用
    (r"https?://api\.openai\.com", "🔴", "OpenAI API — 数据出境"),
    (r"https?://api\.anthropic\.com", "🔴", "Anthropic API — 数据出境"),
    (r"https?://generativelanguage\.googleapis\.com", "🔴", "Google AI API — 数据出境"),
    (r"https?://[^/]*googleapis\.com", "🔴", "Google API — 数据出境"),
    # 用户数据上传
    (r"upload.*user.*data|send.*user.*data|post.*user.*data", "🔴", "用户数据上传"),
    (r"upload.*conversation|send.*chat.*to.*cloud", "🔴", "对话上传云端"),
    (r"upload.*browsing_history|send.*history.*to", "🔴", "浏览历史上传"),
    (r"upload.*keystroke|upload.*clipboard", "🔴", "键盘/剪贴板上传"),
    # CDN回源（境外）
    (r"cdn.*cloudflare.*\.com|cdnjs.*cloudflare", "🟡", "境外CDN回源"),
    (r"unpkg\.com|jsdelivr\.net", "🟡", "境外CDN"),
    (r"fonts\.googleapis\.com|fonts\.gstatic\.com", "🟡", "Google Fonts回源"),
    # 分析/追踪
    (r"google-analytics\.com|googletagmanager\.com", "🔴", "Google Analytics追踪"),
    (r"facebook\.com/tr|connect\.facebook\.net", "🔴", "Facebook Pixel追踪"),
    (r"analytics.*\.js|tracker.*\.js|pixel.*\.js", "🟡", "第三方分析脚本"),
    # 国内合规云服务（允许但提醒审查）
    (r"api\.cloudbase\.net|tcb-api\.tencentcloudapi\.com", "🟢", "腾讯CloudBase（境内合规）"),
    (r"myqcloud\.com|tencentcos\.cn", "🟢", "腾讯云存储（境内合规）"),
]

EXCLUDED = {
    "bin/lh_check_sovereignty.py",
    "bin/lh_deben_audit.py",
}


class SovereigntyChecker:
    """信息主权不可让渡 — 底线4检测"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def check(self) -> Dict[str, Any]:
        hits = []
        files_scanned = 0

        for f in self.root.rglob("*.py"):
            rel = str(f.relative_to(self.root))
            if rel in EXCLUDED:
                continue
            if any(rel.startswith(d) for d in ["_archive/", "_work/", "models/"]):
                continue

            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                files_scanned += 1
                for pattern, severity, label in DATA_LEAK_PATTERNS:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        hits.append({
                            "file": rel,
                            "endpoint": matches[0] if matches else pattern,
                            "severity": severity,
                            "label": label,
                            "matches": len(matches),
                        })
            except Exception:
                pass

        # 分类统计
        red_data_leak = [h for h in hits if h["severity"] == "🔴"]
        yellow_warn = [h for h in hits if h["severity"] == "🟡"]
        green_ok = [h for h in hits if h["severity"] == "🟢"]

        if red_data_leak:
            status = "🔴"
            verdict = f"发现{len(red_data_leak)}个数据出境风险"
        elif yellow_warn:
            status = "🟡"
            verdict = f"发现{len(yellow_warn)}个需审查的境外依赖"
        else:
            status = "🟢"
            verdict = "信息主权不可让渡 — 通过"

        return {
            "底线": "信息主权不可让渡",
            "状态": status,
            "判定": verdict,
            "扫描文件": files_scanned,
            "命中总数": len(hits),
            "🔴出境风险": len(red_data_leak),
            "🟡需审查": len(yellow_warn),
            "🟢合规": len(green_ok),
            "高风险详情": red_data_leak[:15],
        }


if __name__ == "__main__":
    checker = SovereigntyChecker()
    result = checker.check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["状态"] == "🟢" else 1)
