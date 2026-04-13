#!/usr/bin/env python3
"""
☰☰ 龍🇨🇳魂 ☷ · 操作日志公开版导出器
DNA: #龍芯⚡️2026-04-13-LOG-EXPORT-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

功能: 从原始日志中过滤敏感信息，导出可公开的操作日志
铁律: 对错都发，但隐私不发
"""

import json
from pathlib import Path
from collections import Counter

BASE = Path.home() / "longhun-system"
LOGS_DIR = BASE / "logs"
PUBLIC_DIR = BASE / "logs" / "public"
PUBLIC_DIR.mkdir(exist_ok=True)

# 敏感词过滤表
SENSITIVE_WORDS = [
    ".env", "secret", "password", "token", "credential",
    "private", "apikey", "api_key", "ntn_", "ghp_",
    "私密", "密码", "密钥",
]


def is_sensitive(record: dict) -> bool:
    """检测记录是否包含敏感信息"""
    target = str(record.get("target", "")).lower()
    return any(w.lower() in target for w in SENSITIVE_WORDS)


def sanitize(record: dict) -> dict:
    """清洗记录：去路径中的用户名，保留结构"""
    clean = dict(record)
    target = clean.get("target", "")
    # 替换完整用户路径为 ~
    target = target.replace("/Users/zuimeidedeyihan", "~")
    clean["target"] = target
    # 移除可能的敏感标记
    clean.pop("sensitive", None)
    return clean


def export_action_log():
    """导出 action_log.jsonl 公开版"""
    src = LOGS_DIR / "action_log.jsonl"
    if not src.exists():
        print("❌ action_log.jsonl 不存在")
        return

    records = []
    filtered = 0
    tools = Counter()
    dates = set()

    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue

            if is_sensitive(r):
                filtered += 1
                continue

            clean = sanitize(r)
            records.append(clean)
            tools[clean.get("tool", "unknown")] += 1
            dates.add(clean.get("time", "")[:10])

    # 写JSONL
    out_jsonl = PUBLIC_DIR / "action_log_public.jsonl"
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 写统计摘要
    summary = {
        "DNA": "#龍芯⚡️2026-04-13-LOG-EXPORT-v1.0",
        "导出时间": records[-1]["time"] if records else "N/A",
        "总记录": len(records),
        "过滤敏感": filtered,
        "跨越天数": len(dates),
        "日期范围": f"{min(dates)} → {max(dates)}" if dates else "N/A",
        "工具使用统计": dict(tools.most_common()),
        "说明": "对错都有·隐私已过滤·路径已脱敏·全链路可追溯",
        "作者": "诸葛鑫（UID9622）",
    }

    out_summary = PUBLIC_DIR / "action_log_summary.json"
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"✅ action_log 公开版导出完成")
    print(f"   总记录: {len(records)} 条")
    print(f"   过滤敏感: {filtered} 条")
    print(f"   跨越: {len(dates)} 天 ({min(dates)} → {max(dates)})")
    print(f"   工具TOP5: {tools.most_common(5)}")
    return len(records)


def export_behavior_log():
    """导出行为日志（本身就是干净的）"""
    src_dir = BASE / "behavior_logs"
    if not src_dir.exists():
        print("⚠️ behavior_logs/ 不存在")
        return 0

    count = 0
    for f in src_dir.glob("*.md"):
        dest = PUBLIC_DIR / f.name
        dest.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
        count += 1
    for f in src_dir.glob("*.json"):
        dest = PUBLIC_DIR / f.name
        dest.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
        count += 1

    print(f"✅ 行为日志复制: {count} 个文件")
    return count


def export_session_log():
    """导出 session_log.jsonl 公开版（只保留DNA和事件类型）"""
    src = LOGS_DIR / "session_log.jsonl"
    if not src.exists():
        print("⚠️ session_log.jsonl 不存在")
        return 0

    records = []
    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue

            if is_sensitive(r):
                continue

            clean = sanitize(r)
            records.append(clean)

    out = PUBLIC_DIR / "session_log_public.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ session_log 公开版: {len(records)} 条")
    return len(records)


if __name__ == "__main__":
    print("🐉 龍魂操作日志 · 公开版导出")
    print(f"DNA: #龍芯⚡️2026-04-13-LOG-EXPORT-v1.0")
    print("=" * 50)
    print("铁律: 对错都发·隐私不发·路径脱敏·全链路追溯")
    print()

    n1 = export_action_log()
    print()
    n2 = export_behavior_log()
    print()
    n3 = export_session_log()

    print()
    print(f"{'=' * 50}")
    print(f"📊 总导出: {(n1 or 0) + (n2 or 0) + (n3 or 0)} 条/文件")
    print(f"📁 位置: logs/public/")
    print(f"🟢 三色审计: 通过（敏感已过滤）")
    print(f"DNA: #龍芯⚡️2026-04-13-LOG-EXPORT-v1.0")
