#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-DAILY-LOGGER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 结构化每日日志记录器 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-DAILY-LOGGER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
# 数据源层: 记忆永生管道第一环
# 把每日动作结构化记录为：决策/教训/规矩/情绪 四维日志
# 每条日志自动绑定DNA追溯码
# 输出: .codebuddy/memory/YYYY-MM-DD.md
# 
# 用法:
#   python3 bin/lh_daily_logger.py log --type decision --content "..."     # 记决策
#   python3 bin/lh_daily_logger.py log --type lesson --content "..."       # 记教训
#   python3 bin/lh_daily_logger.py log --type rule --content "..."         # 记规矩
#   python3 bin/lh_daily_logger.py log --type emotion --content "..."      # 记情绪
#   python3 bin/lh_daily_logger.py log --type execution --content "..."    # 记执行动作
#   python3 bin/lh_daily_logger.py stats                                   # 统计
#   python3 bin/lh_daily_logger.py export --format json|markdown           # 导出
#   python3 bin/lh_daily_logger.py search --keyword "熔断"                  # 搜索
# ═══════════════════════════════════════════
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
DAILY_LOG_DB = MEMORY_DIR / "daily_log_structured.jsonl"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# ─── 不动点记忆归档引擎（记忆永生管道升级）───
try:
    from engines.lh_fixed_point_memory_archive import MemoryArchive
except Exception:
    MemoryArchive = None

# ─── 日志类型定义 ───
LOG_TYPES = {
    "decision": {
        "label": "决策",
        "emoji": "⚡",
        "fields": ["决策内容", "决策依据", "影响范围", "执行人格", "结果"],
    },
    "lesson": {
        "label": "教训",
        "emoji": "🔴",
        "fields": ["错误描述", "根因分析", "修复方案", "防止再犯规则", "责任人"],
    },
    "rule": {
        "label": "规矩",
        "emoji": "🔒",
        "fields": ["规矩内容", "适用范围", "违反后果", "关联协议", "焊死级别"],
    },
    "emotion": {
        "label": "情绪",
        "emoji": "💢",
        "fields": ["情绪类型", "触发事件", "强度(1-10)", "对象", "后续行动"],
    },
    "execution": {
        "label": "执行",
        "emoji": "🔧",
        "fields": ["任务描述", "交付物", "涉及文件", "状态", "审计标记"],
    },
    "milestone": {
        "label": "里程碑",
        "emoji": "🏆",
        "fields": ["事件", "影响", "相关交付物", "参与人格"],
    },
}


def generate_dna(content: str, log_type: str) -> str:
    """为日志条目生成DNA追溯码"""
    now = datetime.now(timezone.utc)
    content_hash = hashlib.sha256(
        f"{now.isoformat()}:{log_type}:{content[:200]}".encode()
    ).hexdigest()[:8]
    date_str = now.strftime("%Y%m%d")
    return f"#龍芯⚡️{date_str}-DAILY-{log_type.upper()}-{content_hash}"


def today_log_file() -> Path:
    """获取今天的日志文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{today}.md"


def log_entry(
    log_type: str,
    content: str,
    extra: Optional[Dict[str, str]] = None,
    dna: Optional[str] = None,
) -> Dict[str, Any]:
    """创建一条结构化日志条目"""
    if log_type not in LOG_TYPES:
        raise ValueError(f"未知日志类型: {log_type}。可选: {list(LOG_TYPES.keys())}")

    now = datetime.now(timezone.utc)
    if dna is None:
        dna = generate_dna(content, log_type)

    entry = {
        "时间": now.isoformat(),
        "类型": log_type,
        "类型标签": LOG_TYPES[log_type]["label"],
        "内容": content,
        "DNA": dna,
    }
    if extra:
        entry["扩展"] = extra

    return entry


def append_daily(entry: Dict[str, Any]) -> None:
    """追加日志到结构化JSONL + 人类可读MD，并联动不动点记忆归档"""
    # 写 JSONL
    with open(DAILY_LOG_DB, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 写每日MD
    log_file = today_log_file()
    log_type = entry["类型"]
    type_info = LOG_TYPES.get(log_type, {})
    emoji = type_info.get("emoji", "📝")
    label = type_info.get("label", log_type)

    md_block = f"\n### {emoji} {label} | {entry['时间'][:19].replace('T', ' ')}\n"
    md_block += f"- **内容**: {entry['内容']}\n"

    extra = entry.get("扩展", {})
    if extra:
        for key, val in extra.items():
            md_block += f"- **{key}**: {val}\n"

    md_block += f"- **DNA**: `{entry['DNA']}`\n"

    # ─── 联动不动点记忆归档引擎 ───
    if MemoryArchive is not None:
        try:
            archive = MemoryArchive()
            archive_result = archive.ingest(
                entry["内容"],
                source="daily_logger",
                tags=[log_type],
                context={"log_type": log_type, "daily_dna": entry["DNA"]},
            )
            md_block += f"- **归档状态**: `{archive_result.get('status', 'unknown')}`"
            if archive_result.get("state"):
                md_block += f" / 不动点 `{archive_result['state']}`"
            md_block += "\n"
            if archive_result.get("score") is not None:
                md_block += f"- **不动点得分**: {archive_result['score']}\n"
            if archive_result.get("dna"):
                md_block += f"- **归档DNA**: `{archive_result['dna']}`\n"
            if archive_result.get("reasons"):
                reasons = "; ".join(archive_result["reasons"])
                md_block += f"- **归档理由**: {reasons}\n"
            # 将归档结果写回 entry 扩展，供下游使用
            entry.setdefault("扩展", {}).update({
                "归档状态": archive_result.get("status", "unknown"),
                "不动点状态": archive_result.get("state"),
                "不动点得分": archive_result.get("score"),
                "归档DNA": archive_result.get("dna"),
                "归档理由": archive_result.get("reasons", []),
            })
        except Exception as e:
            md_block += f"- **归档联动**: 失败（{e}）\n"

    # 追加到MD文件
    if log_file.exists():
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(md_block)
    else:
        with open(log_file, "w", encoding="utf-8") as f:
            today = datetime.now().strftime("%Y-%m-%d")
            f.write(f"# {today} 工作记录\n\n")
            f.write("> 结构化日志 · 记忆永生管道数据源\n\n")
            f.write(md_block)


def load_daily_entries(date_str: Optional[str] = None) -> List[Dict[str, Any]]:
    """加载指定日期的结构化日志"""
    entries = []
    if date_str:
        target = MEMORY_DIR / f"{date_str}.md"
        if not target.exists():
            return []

    if DAILY_LOG_DB.exists():
        with open(DAILY_LOG_DB, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if date_str:
                        entry_date = entry.get("时间", "")[:10]
                        if entry_date == date_str:
                            entries.append(entry)
                    else:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
    return entries


def search_entries(keyword: str) -> List[Dict[str, Any]]:
    """搜索日志条目"""
    results = []
    entries = load_daily_entries()
    kw_lower = keyword.lower()
    for entry in entries:
        content = entry.get("内容", "").lower()
        extra = entry.get("扩展", {})
        extra_text = " ".join(str(v).lower() for v in extra.values())
        if kw_lower in content or kw_lower in extra_text:
            results.append(entry)
    return results


def get_stats() -> Dict[str, Any]:
    """统计日志数据"""
    entries = load_daily_entries()
    if not entries:
        return {"总条目": 0, "时间跨度": "无数据"}

    type_counts = {}
    date_set = set()
    for e in entries:
        lt = e.get("类型", "unknown")
        type_counts[lt] = type_counts.get(lt, 0) + 1
        date_set.add(e.get("时间", "")[:10])

    dates = sorted(date_set)
    return {
        "总条目": len(entries),
        "时间跨度": f"{dates[0]} ~ {dates[-1]}" if dates else "今日",
        "覆盖天数": len(date_set),
        "类型分布": type_counts,
        "最近条目": entries[-1]["内容"][:100] if entries else "无",
    }


def export_entries(fmt: str = "json") -> str:
    """导出日志"""
    entries = load_daily_entries()
    if fmt == "json":
        return json.dumps(entries, ensure_ascii=False, indent=2)
    else:  # markdown
        lines = ["# 龍魂每日日志导出", "", f"导出时间: {datetime.now().isoformat()}", "", "---", ""]
        for e in entries:
            type_info = LOG_TYPES.get(e.get("类型", ""), {})
            lines.append(f"## {type_info.get('emoji', '')} {type_info.get('label', '')} | {e.get('时间', '')[:19]}")
            lines.append(f"- {e.get('内容', '')}")
            extra = e.get("扩展", {})
            for k, v in extra.items():
                lines.append(f"  - {k}: {v}")
            lines.append(f"  - DNA: `{e.get('DNA', '')}`")
            lines.append("")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·结构化每日日志记录器 v1.0 — 记忆永生管道·数据源层",
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # log 命令
    log_parser = subparsers.add_parser("log", help="记录一条日志")
    log_parser.add_argument("--type", "-t", required=True,
                            choices=list(LOG_TYPES.keys()),
                            help="日志类型")
    log_parser.add_argument("--content", "-c", required=True, help="日志内容")
    log_parser.add_argument("--decision-basis", help="决策依据")
    log_parser.add_argument("--scope", help="影响范围")
    log_parser.add_argument("--persona", help="执行人格")
    log_parser.add_argument("--outcome", help="结果")
    log_parser.add_argument("--root-cause", help="根因")
    log_parser.add_argument("--fix", help="修复方案")
    log_parser.add_argument("--related-protocol", help="关联协议")
    log_parser.add_argument("--weld-level", help="焊死级别")
    log_parser.add_argument("--intensity", type=int, help="情绪强度1-10")
    log_parser.add_argument("--target", help="对象/责任人")
    log_parser.add_argument("--files", help="涉及文件")
    log_parser.add_argument("--audit-mark", help="审计标记")

    # stats 命令
    subparsers.add_parser("stats", help="统计日志")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索日志")
    search_parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出日志")
    export_parser.add_argument("--format", "-f", default="json",
                               choices=["json", "markdown"], help="导出格式")

    args = parser.parse_args()

    if args.command == "log":
        extra = {}
        log_type = args.type
        field_map = {
            "decision_basis": ("决策依据", args.decision_basis),
            "scope": ("影响范围", args.scope),
            "persona": ("执行人格", args.persona),
            "outcome": ("结果", args.outcome),
            "root_cause": ("根因分析", args.root_cause),
            "fix": ("修复方案", args.fix),
            "related_protocol": ("关联协议", args.related_protocol),
            "weld_level": ("焊死级别", args.weld_level),
            "intensity": ("强度", str(args.intensity) if args.intensity else None),
            "target": ("对象", args.target),
            "files": ("涉及文件", args.files),
            "audit_mark": ("审计标记", args.audit_mark),
        }
        for k, (label, val) in field_map.items():
            if val:
                extra[label] = val

        entry = log_entry(log_type, args.content, extra)
        append_daily(entry)

        type_info = LOG_TYPES[log_type]
        print(f"{type_info['emoji']} {type_info['label']}已记录")
        print(f"   DNA: {entry['DNA']}")
        print(f"   文件: {today_log_file()}")

    elif args.command == "stats":
        stats = get_stats()
        print("=" * 50)
        print("  📊 龍魂每日日志统计")
        print("=" * 50)
        for k, v in stats.items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for tk, tv in v.items():
                    type_label = LOG_TYPES.get(tk, {}).get("label", tk)
                    print(f"    {type_label}: {tv}")
            else:
                print(f"  {k}: {v}")
        print("=" * 50)

    elif args.command == "search":
        results = search_entries(args.keyword)
        print(f"🔍 搜索 '{args.keyword}': 找到 {len(results)} 条")
        for r in results:
            type_info = LOG_TYPES.get(r.get("类型", ""), {})
            print(f"  {type_info.get('emoji', '')} [{r['时间'][:19]}] {r['内容'][:80]}")
            print(f"     DNA: {r['DNA']}")

    elif args.command == "export":
        output = export_entries(args.format)
        print(output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
