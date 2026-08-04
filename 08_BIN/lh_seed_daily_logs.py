#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-07-25-SEED-DAILY-LOGS-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 每日日志种子回填脚本 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-25-SEED-DAILY-LOGS-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GOSKILLS: longhun-memory-bootstrap, longhun-dna-align
# ═══════════════════════════════════════════
# 用途:
#   把已有的 YYYY-MM-DD.md 每日记忆文件解析成结构化 daily_log_structured.jsonl，
#   让外脑压缩引擎、知识图谱、记忆仪表盘真正“有料”。
#   多次运行幂等：已存在 DNA 的条目不会重复写入。
#
# 用法:
#   python3 bin/lh_seed_daily_logs.py          # 扫描全部 .md 回填
#   python3 bin/lh_seed_daily_logs.py --dry-run # 只预览不写入
#   python3 bin/lh_seed_daily_logs.py --date 2026-07-09 # 只处理某天
# ═══════════════════════════════════════════
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
DAILY_LOG_DB = MEMORY_DIR / "daily_log_structured.jsonl"

# 从 lh_daily_logger.py 同步
LOG_TYPES = {
    "decision": {"label": "决策", "emoji": "⚡"},
    "lesson": {"label": "教训", "emoji": "🔴"},
    "rule": {"label": "规矩", "emoji": "🔒"},
    "emotion": {"label": "情绪", "emoji": "💢"},
    "execution": {"label": "执行", "emoji": "🔧"},
    "milestone": {"label": "里程碑", "emoji": "🏆"},
}


def _parse_date_from_filename(stem: str) -> Optional[str]:
    """从文件名提取日期。"""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", stem):
        return stem
    return None


def _generate_dna(content: str, log_type: str, date_str: str) -> str:
    """基于内容、类型、日期生成稳定 DNA。"""
    content_hash = hashlib.sha256(
        f"{date_str}:{log_type}:{content[:200]}".encode()
    ).hexdigest()[:8]
    return f"#龍芯⚡️{date_str.replace('-', '')}-SEED-{log_type.upper()}-{content_hash}"


def _classify_log_type(section_title: str, body: str) -> str:
    """根据标题和正文推断日志类型。"""
    text = (section_title + " " + body).lower()

    if any(kw in text for kw in ["教训", "错误", "修复", "踩坑", "反思", "改进"]):
        return "lesson"
    if any(kw in text for kw in ["决策", "决定", "拍板", "选择", "战略", "选定"]):
        return "decision"
    if any(kw in text for kw in ["规矩", "规则", "铁律", "协议", "焊死", "底线"]):
        return "rule"
    if any(kw in text for kw in ["情绪", "发火", "委屈", "疲惫", "兴奋", "玩笑", "敷衍"]):
        return "emotion"
    if any(kw in text for kw in ["完成", "落地", "执行", "部署", "上线", "新建", "修改", "生成", "实现"]):
        return "execution"

    # 默认里程碑
    return "milestone"


def _extract_dnas(body: str) -> List[str]:
    """提取正文中已有的 DNA 字符串。"""
    return re.findall(r"#龍芯⚡️[^`\s]+", body)


def _extract_confirm_codes(body: str) -> List[str]:
    """提取确认码。"""
    return re.findall(r"#CONFIRM🌌[^`\s]+", body)


def _extract_bullet_points(body: str) -> List[str]:
    """提取无序列表条目作为结构化扩展。"""
    points = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith(("- ", "* ", "+ ")):
            clean = line[2:].strip()
            if clean:
                points.append(clean)
    return points


def _build_extra(section_title: str, body: str) -> Dict[str, Any]:
    """构建扩展字段。"""
    extra: Dict[str, Any] = {}

    dnas = _extract_dnas(body)
    if dnas:
        extra["原文DNA"] = dnas[0]
        if len(dnas) > 1:
            extra["相关DNA"] = dnas[1:5]

    confirms = _extract_confirm_codes(body)
    if confirms:
        extra["确认码"] = confirms[0]

    bullets = _extract_bullet_points(body)
    if bullets:
        extra["要点"] = bullets[:20]

    # 提取分数/百分比数字
    scores = re.findall(r"(\d+(?:\.\d+)?)\s*/\s*(?:10|100)", body)
    if scores:
        extra["评分"] = scores[0]

    # 提取文件路径
    paths = re.findall(r"`([^`]+\.(?:py|md|json|jsonl|sh|yml|yaml|txt|html|css|js))`", body)
    if paths:
        extra["涉及文件"] = list(set(paths))[:10]

    return extra


def parse_md_file(md_path: Path) -> List[Dict[str, Any]]:
    """解析单个 .md 文件为若干结构化日志条目。"""
    date_str = _parse_date_from_filename(md_path.stem)
    if not date_str:
        return []

    text = md_path.read_text(encoding="utf-8")
    # 统一换行
    text = text.replace("\r\n", "\n")

    entries: List[Dict[str, Any]] = []

    # 按 ## 二级标题拆分章节
    # 第一个 ## 之前的文本作为引言忽略
    sections = re.split(r"\n(?=##\s+)", text)

    for section in sections:
        section = section.strip()
        if not section.startswith("## "):
            continue

        # 去掉标题标记
        lines = section.splitlines()
        title_line = lines[0].strip().lstrip("#").strip()
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue

        log_type = _classify_log_type(title_line, body)
        extra = _build_extra(title_line, body)
        content = f"{title_line}：{body[:400]}"
        if len(body) > 400:
            content = content[:397] + "..."

        dna = _generate_dna(content, log_type, date_str)

        # 使用文件日期当天的随机时间（UTC noon）
        iso_time = f"{date_str}T12:00:00+00:00"

        entry = {
            "时间": iso_time,
            "类型": log_type,
            "类型标签": LOG_TYPES.get(log_type, {}).get("label", log_type),
            "内容": content,
            "DNA": dna,
            "扩展": extra,
        }
        entries.append(entry)

    return entries


def load_existing_dnas() -> Set[str]:
    """加载已有的 DNA，避免重复。"""
    existing: Set[str] = set()
    if not DAILY_LOG_DB.exists():
        return existing
    with open(DAILY_LOG_DB, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                existing.add(entry.get("DNA", ""))
            except json.JSONDecodeError:
                continue
    return existing


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·每日日志种子回填 — 让历史记忆进入结构化管道"
    )
    parser.add_argument("--date", help="只处理指定日期 (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="预览，不写入")
    args = parser.parse_args()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if args.date:
        files = [MEMORY_DIR / f"{args.date}.md"]
    else:
        files = sorted(MEMORY_DIR.glob("????-??-??.md"))

    existing_dnas = load_existing_dnas()
    new_entries: List[Dict[str, Any]] = []

    for md_path in files:
        if not md_path.exists():
            continue
        entries = parse_md_file(md_path)
        for e in entries:
            if e["DNA"] not in existing_dnas:
                new_entries.append(e)
                existing_dnas.add(e["DNA"])  # 防止同一次运行内部重复

    if not new_entries:
        print("=" * 50)
        print("  🟡 没有新增条目（可能已全量回填）")
        print("=" * 50)
        return

    print("=" * 50)
    print(f"  📝 发现 {len(new_entries)} 条待回填日志")
    print("=" * 50)
    for e in new_entries[:10]:
        print(f"  [{e['类型标签']}] {e['内容'][:60]}...")
        print(f"      DNA: {e['DNA']}")
    if len(new_entries) > 10:
        print(f"  ... 还有 {len(new_entries) - 10} 条")

    if args.dry_run:
        print("\n  🟡 --dry-run 模式，未写入")
        return

    # 追加写入 JSONL
    with open(DAILY_LOG_DB, "a", encoding="utf-8") as f:
        for e in new_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print("\n" + "=" * 50)
    print(f"  ✅ 已回填 {len(new_entries)} 条到 {DAILY_LOG_DB}")
    print("=" * 50)


if __name__ == "__main__":
    main()
