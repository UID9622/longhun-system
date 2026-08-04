#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·反算法收割审计引擎  v1.0
================================
落地 [[clause_harvest_audit]]：扫描直播/文案文本，识别 PK/倒计时/加成/排名/抽成 等
情绪收割信号，打分评级（🟢🟡🔴），输出带 DNA 的审计报告并归档。

用法：
  python3 bin/lh_anti_algorithmic_harvest.py --demo
  python3 bin/lh_anti_algorithmic_harvest.py --text "双屏PK比拼 倒计时 3倍加成 榜一 打赏"
  python3 bin/lh_anti_algorithmic_harvest.py --file live_title.txt

DNA：#龍芯⚡️丙午·辛未·乙酉·申时·观-LONGHUN-HARVEST-AUDIT-<hash8>
归属：UID9622 · 诸葛鑫（Lucky）· 确认码 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime

# 农历干支（当前会话固定，禁公历）
LUNAR = "丙午·辛未·乙酉"
SHICHEN = "申时"

# 收割信号词典
SIGNALS = {
    "PK对立": ["比拼", "连麦", "pk", "PK", "对战", "站队", "输赢", "榜一", "榜二", "倒数第一"],
    "倒计时压迫": ["倒计时", "限时", "最后", "秒", "马上结束", "即将结束", "错过"],
    "加成诱导": ["倍数", "加成", "3倍", "翻倍", "福利", "补贴价", "秒杀"],
    "排名虚荣": ["排名", "上榜", "热门", "冲榜", "推荐", "人气", "点赞榜"],
    "打赏抽成": ["打赏", "礼物", "刷", "嘉年华", "刷起来", "火箭", "跑车"],
}

LEVEL_MAP = {0: "🟢安全", 1: "🟡谨慎", 2: "🟡谨慎", 3: "🔴高危", 4: "🔴高危", 5: "🔴高危"}

AUDIT_DIR = "state/threshold_trigger/harvest_audit"


def scan(text: str) -> dict[str, Any]:
    """扫描文本，返回命中信号与评级。"""
    hits = {}
    for cat, kws in SIGNALS.items():
        found = sorted({kw for kw in kws if kw in text})
        if found:
            hits[cat] = found
    n_cat = len(hits)
    level = LEVEL_MAP.get(n_cat, "🔴高危")
    return {"hits": hits, "n_cat": n_cat, "level": level}


def make_dna(text: str) -> str:
    h = hashlib.sha256((text + str(datetime.now())).encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️{LUNAR}·{SHICHEN}·观-LONGHUN-HARVEST-AUDIT-{h}"


def audit(text: str, source: str = "manual") -> dict[str, Any]:
    res = scan(text)
    report = {
        "protocol": "protocol_anti_algorithmic_harvest",
        "clause": "clause_harvest_audit",
        "time": f"{LUNAR}·{SHICHEN}",
        "source": source,
        "text": text,
        "hits": res["hits"],
        "category_count": res["n_cat"],
        "level": res["level"],
        "verdict": "🔴 有罪·情绪收割" if res["n_cat"] >= 3 else (
            "🟡 疑似操控" if res["n_cat"] >= 1 else "🟢 无收割信号"),
        "dna": make_dna(text),
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }
    return report


def persist(report: dict[str, Any]) -> str:
    os.makedirs(AUDIT_DIR, exist_ok=True)
    h = report["dna"].split("-")[-1]
    path = os.path.join(AUDIT_DIR, f"{LUNAR.replace('·','')}-{h}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path


def render(report: dict[str, Any]) -> str:
    lines = [
        "╔══════════════════════════════════════════╗",
        "  龍魂·反算法收割审计报告  v1.0",
        "╚══════════════════════════════════════════╝",
        f"来源   : {report['source']}",
        f"时间   : {report['time']}",
        f"文本   : {report['text'][:60]}{'…' if len(report['text'])>60 else ''}",
        f"命中类 : {report['category_count']} / {len(SIGNALS)}",
        f"评级   : {report['level']}",
        f"判决   : {report['verdict']}",
    ]
    if report["hits"]:
        lines.append("—— 命中信号 ——")
        for cat, kws in report["hits"].items():
            lines.append(f"  [{cat}] {', '.join(kws)}")
    lines.append(f"DNA    : {report['dna']}")
    lines.append(f"确认码 : {report['confirm']}")
    return "\n".join(lines)


DEMO_TEXT = ("双屏PK比拼 比分88597 vs 22114 倒计时06:18 "
             "3倍加成中(18s) 上热门了🔥 共10人推荐 榜一冲榜 "
             "打赏刷起来 嘉年华 错过即损失")


def main():
    ap = argparse.ArgumentParser(description="龍魂反算法收割审计引擎")
    ap.add_argument("--text", help="待扫描文本")
    ap.add_argument("--file", help="待扫描文本文件")
    ap.add_argument("--demo", action="store_true", help="跑内置抖音PK案例")
    args = ap.parse_args()

    if args.demo:
        text, src = DEMO_TEXT, "抖音直播PK案例(内置)"
    elif args.text:
        text, src = args.text, "命令行--text"
    elif args.file:
        text, src = open(args.file, encoding="utf-8").read(), f"文件:{args.file}"
    else:
        ap.print_help()
        return

    report = audit(text, src)
    print(render(report))
    path = persist(report)
    print(f"归档   : {path}")


if __name__ == "__main__":
    main()
