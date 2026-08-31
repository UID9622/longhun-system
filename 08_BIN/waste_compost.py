#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂废料翻堆机 waste_compost.py v1.0
DNA: #龍芯⚡️2026-08-31-WASTE-COMPOST-CRON-v1.0-UID9622
铁律: #IRON-WASTE-REUSE-FERMENTATION
用法: python3 08_BIN/waste_compost.py   # 追加翻堆报告到 WASTE/manifest.log（不覆盖）
逻辑: 遍历 WASTE/ 子目录 -> 统计文件数量+最后修改时间 -> 输出三色分类报告
三色: 🟢已发酵(防再犯机制/复用记录) · 🟡发酵中(有潜力未出池) · 🔴待归档(>4周未动)
"""
import os
import sys
import time
import datetime

WASTE = os.path.expanduser("~/longhun-system/WASTE")
MANIFEST = os.path.join(WASTE, "manifest.log")
FOUR_WEEKS = 28 * 24 * 3600
CATS = ["dialogue", "code", "log", "memory", "frozen"]

# 已发酵标记：文件名含 FERMENTED/已发酵，或 manifest 中已有 🟢 记录
FERMENTED_MARKS = ("FERMENTED", "已发酵", "发酵完成")
# 发酵中标记：文件名含 FERMENTING/发酵中
FERMENTING_MARKS = ("FERMENTING", "发酵中")


def classify(p):
    """按名称+内容+mtime 判定三色。返回 (状态, 天数)。"""
    name = os.path.basename(p)
    mtime = os.path.getmtime(p)
    age = time.time() - mtime
    days = int(age // 86400)
    if age > FOUR_WEEKS:
        return "🔴待归档", days
    if any(m in name for m in FERMENTING_MARKS):
        return "🟡发酵中", days
    if any(m in name for m in FERMENTED_MARKS):
        return "🟢已发酵", days
    # 内容含防再犯机制/复用记录/已发酵标记 → 🟢
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(2000)
        if any(k in head for k in ("防再犯", "已发酵", "复用记录", "🟢已发酵")):
            return "🟢已发酵", days
    except Exception:
        pass
    # 默认：有潜力但未出池
    return "🟡发酵中", days


def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    today = now.split()[0]
    if not os.path.isdir(WASTE):
        with open(MANIFEST, "a", encoding="utf-8") as fh:
            fh.write(f"WASTE:{today}:error: 废料池不存在 {WASTE}\n")
        print(f"ERROR: 废料池不存在 {WASTE}")
        return 1

    counts = {"🟢已发酵": 0, "🟡发酵中": 0, "🔴待归档": 0}
    lines = [
        "",
        f"# ===== 翻堆报告 {now} · waste_compost.py v1.0 =====",
        f"# DNA: #龍芯⚡️2026-08-31-WASTE-COMPOST-CRON-v1.0-UID9622",
    ]
    any_file = False
    for cat in CATS:
        d = os.path.join(WASTE, cat)
        if not os.path.isdir(d):
            continue
        entries = sorted(os.listdir(d))
        for f in entries:
            p = os.path.join(d, f)
            if os.path.isdir(p):
                continue
            any_file = True
            status, days = classify(p)
            counts[status] += 1
            line = f"WASTE:{today}:{cat}:{f}:{status}:age={days}d"
            lines.append(line)
            # 每行输出便于直接读取
            print(f"  [{status}] {cat}/{f} · {days} 天前")
    if not any_file:
        lines.append("WASTE:%s:summary:(空) 无废料文件" % today)
        print("  (空) 无废料文件")
    lines.append(
        "WASTE:%s:summary:翻堆汇总 🟢已发酵 %d · 🟡发酵中 %d · 🔴待归档 %d"
        % (today, counts["🟢已发酵"], counts["🟡发酵中"], counts["🔴待归档"])
    )
    # 追加不覆盖
    with open(MANIFEST, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  → 已追加翻堆报告到 {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
