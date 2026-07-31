#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Claude 留证技能收集器 v1.0

从 /Users/zuimeidedeyihan/Downloads/Claude的留证 中自动提取所有被提及/实现过的技能，
输出结构化清单（JSON + Markdown），方便纳入龍魂系统内核统一管理。

DNA: #龍芯⚡️2026-07-01-LONGHUN-SKILL-COLLECTOR-v1.0
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

EVIDENCE_DIR = Path.home() / "Downloads" / "Claude的留证"
OUTPUT_DIR = Path.home() / "longhun-system" / "data" / "forensic_kernel"

# 技能名 -> 搜索关键词（不区分大小写）
# 同一技能可能在不同记录里叫法不同，用多个关键词兜底
SKILL_KEYWORDS: Dict[str, List[str]] = {
    # 10 个已集成 HTML/Python Skills
    "skill-1-algorithmic-art": ["skill-1", "algorithmic-art", "算法艺术", "Perlin噪声"],
    "skill-2-brand-guidelines": ["skill-2", "brand-guidelines", "品牌设计", "色彩规范"],
    "skill-3-canvas-design": ["skill-3", "canvas-design", "Canvas绘图", "滤镜效果"],
    "skill-4-doc-coauthoring": ["skill-4", "doc-coauthoring", "协作编辑", "版本控制"],
    "skill-5-internal-comms": ["skill-5", "internal-comms", "消息任务", "进度追踪"],
    "skill-6-mcp-builder": ["skill-6", "mcp-builder", "FastMCP", "MCP生成"],
    "skill-7-skill-creator": ["skill-7", "skill-creator", "技能模板", "技能框架"],
    "skill-8-slack-gif-creator": ["skill-8", "slack-gif-creator", "GIF动画", "Slack集成"],
    "skill-9-theme-factory": ["skill-9", "theme-factory", "色彩系统", "CSS生成"],
    "skill-10-web-artifacts-builder": ["skill-10", "web-artifacts-builder", "React组件", "HTML模板"],

    # ~/.龍魂/ 本地工具
    "dna_validator.py": ["dna_validator", "DNA 格式校验", "DNA校验"],
    "term_translator.py": ["term_translator", "术语自动转换", "術語自動化"],
    "index_resolver.py": ["index_resolver", "索引树生成", "索引樹"],
    "notion_sync_checker.py": ["notion_sync_checker", "Notion 同步", "同步狀態監控"],
    "validate_new_welding_point.py": ["validate_new_welding_point", "新焊点验收", "焊點驗收"],

    # Kimi / Claude 已安装或恢复的技能
    "kimi-webbridge": ["kimi-webbridge", "WebBridge", "浏览器控制"],
    "audit": ["audit", "审计", "審計"],
    "time-decay": ["time-decay", "时间衰减", "時間衰減"],

    # 龍魂系统级模块/技能
    "十五人格API": ["persona_api", "15 人格", "十五人格", "人格 API"],
    "人格调度器": ["persona_scheduler", "人格调度", "persona_cert"],
    "宝宝菜单系统": ["宝宝菜单", "宝宝_菜单系统", "语音交互"],
    "五色审计v3": ["longhun-wucai-v3", "五色审计", "五色審計"],
    "三色审计": ["三色审计", "三色審計", "batch_auditor"],
    "决策流场主控页": ["决策流场", "流场主控页", "v2.7.36"],
    "龍魂Skill管理核心": ["skills/__init__.py", "Skill 管理核心", "Skills 管理核心"],
    "龍魂Skill API": ["skills/api.py", "Skill API", "longhun-skills"],

    # 2026-05-27 对话中承诺/设想的系统
    "凭证管理系统": ["凭证管理", "CREDIBILITY-SYSTEM", "确认码", "SEAL"],
    "文字即权重可视化": ["文字即权重", "权重可视化"],
    "单一真实源头": ["单一真实源头", "官方版本源", "版本源一元化"],
    "跨窗口持久化记忆": ["跨窗口记忆", "持久化记忆", "SESSION_MEMORY", "铁律 13"],
    "DNA签章系统": ["DNA签章", "DNA 签章"],

    # 部署与治理
    "longhun888.com部署": ["longhun888.com", "Cloudflare", "Let's Encrypt"],
    "仓库治理/BFG清理": ["BFG", "M270", "大文件清理", "仓库清理"],
    "安全修复v4.1.1": ["SECURITY-HOTFIX", "安全修复", "Security Hotfix"],
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def 收集技能() -> Dict[str, Any]:
    if not EVIDENCE_DIR.exists():
        raise FileNotFoundError(f"证据目录不存在: {EVIDENCE_DIR}")

    files = [f for f in EVIDENCE_DIR.iterdir() if f.is_file() and f.suffix.lower() in (".md", ".txt")]
    skill_hits: Dict[str, Dict[str, Any]] = {}

    for skill_name, keywords in SKILL_KEYWORDS.items():
        skill_hits[skill_name] = {
            "技能名": skill_name,
            "关键词": keywords,
            "提及次数": 0,
            "来源文件": [],
            "状态": "候选",
        }

    for file_path in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True):
        content = _read_text(file_path)
        lower = content.lower()
        for skill_name, keywords in SKILL_KEYWORDS.items():
            count = sum(lower.count(kw.lower()) for kw in keywords)
            if count > 0:
                skill_hits[skill_name]["提及次数"] += count
                if file_path.name not in skill_hits[skill_name]["来源文件"]:
                    skill_hits[skill_name]["来源文件"].append(file_path.name)

    # 过滤掉完全没命中的
    inventory = {k: v for k, v in skill_hits.items() if v["提及次数"] > 0}

    # 状态判定
    for item in inventory.values():
        if item["提及次数"] >= 5 or any(w in str(item["来源文件"]) for w in ["部署", "完成", "就绪", "正常", "验证"]):
            item["状态"] = "已实现/已部署"
        elif item["提及次数"] >= 2:
            item["状态"] = "已识别"
        else:
            item["状态"] = "候选"

    # 按状态分组
    groups = defaultdict(list)
    for item in inventory.values():
        groups[item["状态"]].append(item)

    return {
        "系统DNA": "#龍芯⚡️2026-07-01-LONGHUN-SKILL-COLLECTOR-v1.0",
        "生成时间": _now(),
        "证据总数": len(files),
        "技能总数": len(inventory),
        "技能清单": list(inventory.values()),
        "按状态分组": dict(groups),
    }


def 生成Markdown清单(inventory: Dict[str, Any]) -> str:
    lines = [
        "# 🐉 龍魂 · Claude 留证技能清单",
        f"**系统 DNA**: `{inventory['系统DNA']}`",
        f"**生成时间**: {inventory['生成时间']}",
        f"**证据文件数**: {inventory['证据总数']} 份",
        f"**识别技能数**: {inventory['技能总数']} 个",
        "",
    ]

    for status in ["已实现/已部署", "已识别", "候选"]:
        items = inventory["按状态分组"].get(status, [])
        if not items:
            continue
        lines.append(f"## {status}（{len(items)} 个）")
        for item in sorted(items, key=lambda x: x["提及次数"], reverse=True):
            lines.append(f"### {item['技能名']}")
            lines.append(f"- 关键词: {', '.join(item['关键词'])}")
            lines.append(f"- 提及次数: {item['提及次数']}")
            lines.append(f"- 来源: {', '.join(item['来源文件'])}")
            lines.append("")
    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = 收集技能()

    json_path = OUTPUT_DIR / "skill_inventory.json"
    json_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")

    md = 生成Markdown清单(inventory)
    md_path = OUTPUT_DIR / "skill_inventory.md"
    md_path.write_text(md, encoding="utf-8")

    print(md)
    print(f"\n🐉 技能清单已保存:")
    print(f"   JSON: {json_path}")
    print(f"   Markdown: {md_path}")


if __name__ == "__main__":
    main()
