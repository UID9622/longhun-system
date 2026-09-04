#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 标签自动归类器 v1.0
DNA: #龍芯⚡️丙午·乙未·乙未·申时·䷀乾-NOTION-TAG-CLASSIFIER-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

基于引擎代码特征自动推断标签。读取引擎注册表 JSON，分析每个引擎的代码内容，
按 21 个标签维度打标，输出增强后的注册表。

用法:
  python3 bin/lh_notion_tag_classifier.py              # 读取注册表→自动打标→输出
  python3 bin/lh_notion_tag_classifier.py --engine xxx  # 只分析单个引擎
  python3 bin/lh_notion_tag_classifier.py --dry-run     # 预览不打标
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·乙未·申时·䷀乾-NOTION-TAG-CLASSIFIER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry.json"
OUTPUT_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry_tagged.json"

# ── 21 维度标签体系 ─────────────────────────────────
# 每个标签含：名称、说明、检测规则

TAG_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    # === 功能标签 ===
    "has_dna": {
        "name": "有DNA签名",
        "dimension": "治理",
        "detect": lambda c: bool(re.search(r'DNA:\s*#龍芯', c)),
    },
    "has_doc": {
        "name": "有文档",
        "dimension": "治理",
        "detect": lambda c: bool(_get_docstring(c)) and len(_get_docstring(c) or "") > 30,
    },
    "has_tests": {
        "name": "有测试",
        "dimension": "质量",
        "detect": lambda c: "unittest" in c or "pytest" in c or "test_" in c,
    },
    "has_error_handling": {
        "name": "有错误处理",
        "dimension": "质量",
        "detect": lambda c: bool(re.search(r'try\s*:', c)) or "raise " in c,
    },
    "has_logging": {
        "name": "有日志",
        "dimension": "质量",
        "detect": lambda c: "logging" in c or "_log(" in c or "logger" in c,
    },
    "has_typing": {
        "name": "有类型注解",
        "dimension": "质量",
        "detect": lambda c: bool(re.search(r'def \w+\([^)]*:\s*\w+', c)),
    },
    "has_cli": {
        "name": "有CLI入口",
        "dimension": "功能",
        "detect": lambda c: "argparse" in c or "click" in c or "if __name__" in c,
    },
    "has_api": {
        "name": "有API/网络",
        "dimension": "功能",
        "detect": lambda c: any(m in c for m in ("flask", "fastapi", "aiohttp", "requests", "urllib", "http.server", "socket")),
    },
    "has_db": {
        "name": "有数据库",
        "dimension": "功能",
        "detect": lambda c: any(m in c for m in ("sqlite", "sqlalchemy", "pymysql", "psycopg", "redis", "chromadb")),
    },
    "has_file_io": {
        "name": "有文件IO",
        "dimension": "功能",
        "detect": lambda c: bool(re.search(r'(open|Path)\(', c)) or "write" in c,
    },
    "has_subprocess": {
        "name": "有系统调用",
        "dimension": "功能",
        "detect": lambda c: "subprocess" in c or "os.system" in c,
    },
    "has_parallel": {
        "name": "有并行处理",
        "dimension": "性能",
        "detect": lambda c: any(m in c for m in ("threading", "multiprocessing", "asyncio", "concurrent")),
    },

    # === 架构标签 ===
    "is_service": {
        "name": "长驻服务",
        "dimension": "架构",
        "detect": lambda c: bool(re.search(r'(while\s+True|run_forever|serve_forever|app\.run)', c)),
    },
    "is_cron": {
        "name": "定时任务",
        "dimension": "架构",
        "detect": lambda c: "schedule" in c or "cron" in c or "APScheduler" in c,
    },
    "is_daemon": {
        "name": "守护进程",
        "dimension": "架构",
        "detect": lambda c: "daemon" in c.lower() or "launchd" in c,
    },
    "is_module": {
        "name": "库/模块",
        "dimension": "架构",
        "detect": lambda c: ("class " in c and "if __name__" not in c[:500]) or "__all__" in c,
    },

    # === 安全相关 ===
    "touches_credentials": {
        "name": "涉及凭证",
        "dimension": "安全",
        "detect": lambda c: bool(re.search(r'(password|secret|token|key|credential)', c, re.I)),
    },
    "touches_privacy": {
        "name": "涉及隐私数据",
        "dimension": "安全",
        "detect": lambda c: bool(re.search(r'(phone|email|身份证|手机号|隐私|privacy|personal)', c, re.I)),
    },
    "touches_crypto": {
        "name": "涉及加密",
        "dimension": "安全",
        "detect": lambda c: any(m in c for m in ("crypto", "hashlib", "hmac", "gpg", "sign", "encrypt", "decrypt")),
    },

    # === 龍魂特有 ===
    "uses_cnsh": {
        "name": "使用CNSH",
        "dimension": "龍魂",
        "detect": lambda c: "cnsh" in c.lower() or "CNSH" in c,
    },
    "uses_persona": {
        "name": "使用人格系统",
        "dimension": "龍魂",
        "detect": lambda c: "persona" in c.lower() or "人格" in c,
    },
}

# ── 运维标记检测 ─────────────────────────────────────

OPS_MARKERS = [
    ("待文档化", lambda c, e: not e.get("description") or len(e.get("description", "")) < 20),
    ("未测试", lambda c, e: "test" not in e.get("name", "").lower() and "test_" not in e.get("path", "")),
    ("大型文件", lambda c, e: e.get("lines", 0) > 800),
    ("轻量文件", lambda c, e: e.get("lines", 0) < 30),
    ("实验性", lambda c, e: "experimental" in c[:500].lower() or "实验" in c[:500]),
    ("已废弃", lambda c, e: "deprecated" in c[:500].lower() or "废弃" in c[:500]),
    ("待修复", lambda c, e: "TODO" in c or "FIXME" in c),
    ("有网络依赖", lambda c, e: bool(re.search(r'(import requests|import urllib|import aiohttp)', c))),
    ("有系统依赖", lambda c, e: "subprocess" in c or "ctypes" in c),
    ("单点故障风险", lambda c, e: bool(re.search(r'(while\s+True|run_forever)', c)) and not ("threading" in c or "multiprocessing" in c)),
    ("冷数据", lambda c, e: "archive" in c.lower() or "backup" in c.lower() or "deprecated" in c.lower()),
    ("热路径", lambda c, e: ("while True" in c or "for " in c) and e.get("lines", 0) < 100),
]


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _get_docstring(content: str) -> Optional[str]:
    try:
        tree = ast.parse(content)
        return ast.get_docstring(tree)
    except SyntaxError:
        return None


def classify_engine(entry: Dict[str, Any]) -> Dict[str, Any]:
    """对单个引擎执行所有标签检测"""
    filepath = ROOT / entry["path"]
    content = ""
    if filepath.exists():
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            pass

    # 功能标签
    tags = []
    for tag_id, tag_def in TAG_DEFINITIONS.items():
        if tag_def["detect"](content):
            tags.append({
                "id": tag_id,
                "name": tag_def["name"],
                "dimension": tag_def["dimension"],
            })

    # 运维标记
    ops = []
    for name, detector in OPS_MARKERS:
        if detector(content, entry):
            ops.append(name)

    # 增强条目
    enhanced = dict(entry)
    enhanced["tags"] = tags
    enhanced["ops_tags"] = ops
    enhanced["tagged_at"] = _now()
    enhanced["tag_count"] = len(tags)
    return enhanced


def classify_all(registry: Optional[Dict] = None) -> Dict[str, Any]:
    """对所有引擎执行标签分类"""
    if registry is None:
        if not REGISTRY_FILE.exists():
            _log("注册表不存在，请先运行 lh_notion_engine_discovery.py", "ERROR")
            sys.exit(1)
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)

    _log(f"开始标签分类: {registry['total_engines']} 个引擎...")
    engines = registry.get("engines", [])

    tagged = []
    stats = {"total": len(engines), "tagged": 0, "by_dimension": {}, "by_tag": {}}

    for i, eng in enumerate(engines):
        enhanced = classify_engine(eng)
        tagged.append(enhanced)

        for t in enhanced.get("tags", []):
            dim = t["dimension"]
            stats["by_dimension"][dim] = stats["by_dimension"].get(dim, 0) + 1
            stats["by_tag"][t["name"]] = stats["by_tag"].get(t["name"], 0) + 1

        stats["tagged"] += 1
        if (i + 1) % 50 == 0:
            _log(f"  进度: {i+1}/{len(engines)}")

    result = {
        "dna": DNA,
        "version": "1.0-tagged",
        "generated_at": _now(),
        "total_engines": len(tagged),
        "stats": stats,
        "engines": tagged,
    }

    _log(f"分类完成: {stats['tagged']} 引擎 · {sum(len(e.get('tags',[])) for e in tagged)} 标签", "OK")

    # 标签分布
    for dim, cnt in sorted(stats["by_dimension"].items()):
        _log(f"  {dim}: {cnt}", "INFO")

    return result


def save_tagged(result: Dict[str, Any]):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {OUTPUT_FILE}", "OK")


# ── 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 标签自动归类器")
    parser.add_argument("--engine", type=str, help="只分析单个引擎名称")
    parser.add_argument("--dry-run", action="store_true", help="预览不打标")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    if args.engine:
        if not REGISTRY_FILE.exists():
            _log("注册表不存在", "ERROR")
            sys.exit(1)
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)
        for eng in registry["engines"]:
            if eng["name"] == args.engine:
                enhanced = classify_engine(eng)
                print(json.dumps(enhanced, ensure_ascii=False, indent=2))
                return
        _log(f"未找到引擎: {args.engine}", "ERROR")
        return

    result = classify_all()

    if not args.dry_run:
        save_tagged(result)
    else:
        _log("dry-run 模式，未保存", "WARN")

    # 统计摘要
    tag_dist = result["stats"]["by_tag"]
    print(f"\n🏷️  标签分布 Top 15:")
    for name, cnt in sorted(tag_dist.items(), key=lambda x: -x[1])[:15]:
        bar = "█" * max(1, cnt // 5)
        print(f"  {name:16s} {cnt:4d}  {bar}")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
