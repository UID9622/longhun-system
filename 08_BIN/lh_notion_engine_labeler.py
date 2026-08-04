#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎标签归类器 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-LABELER-v1.0-2C681225
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-LABELER-v1.0-2C681225"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
REGISTRY_FILE = OUTPUT_DIR / "engine_registry.json"
LABELED_REGISTRY_FILE = OUTPUT_DIR / "labeled_registry.json"
LABEL_REPORT_FILE = OUTPUT_DIR / "label_report.json"

# ── 默认分类规则 ─────────────────────────────────────
# 路径关键词 → (主分类, 子分类)
PATH_CATEGORIES: Dict[str, Tuple[str, str]] = {
    "engines/turbulence": ("🧠 智能与推理", "推演预测"),
    "engines/ant_colony": ("🧠 智能与推理", "检测识别"),
    "engines/collaboration": ("🎭 人格与协作", "团队协作"),
    "engines/security": ("🛡️ 安全与治理", "红蓝对抗"),
    "engines/mental_immune": ("🛡️ 安全与治理", "熔断保护"),
    "engines/core": ("⚙️ 工程与部署", "编译构建"),
    "engines/guanlan": ("🌐 交互与表达", "人机交互"),
    "engines/dao": ("🔮 哲学与数学", "哲学引擎"),
    "engines/tao": ("🔮 哲学与数学", "哲学引擎"),
    "engines/math": ("🔮 哲学与数学", "数理计算"),
    "engines/number": ("🔮 哲学与数学", "数理计算"),
    "engines/formula": ("🔮 哲学与数学", "数理计算"),
    "engines/bagua": ("🔮 哲学与数学", "易经体系"),
    "engines/yijing": ("🔮 哲学与数学", "易经体系"),
    "engines/philosophy": ("🔮 哲学与数学", "哲学引擎"),
    "engines/video": ("🌐 交互与表达", "多媒体"),
    "engines/visual": ("🌐 交互与表达", "多媒体"),
    "engines/voice": ("🌐 交互与表达", "多媒体"),
    "engines/avatar": ("🌐 交互与表达", "多媒体"),
    "engines/image": ("🌐 交互与表达", "多媒体"),
    "engines/chat": ("🌐 交互与表达", "人机交互"),
    "engines/transl": ("🌐 交互与表达", "人机交互"),
    "engines/teach": ("🌐 交互与表达", "人机交互"),
    "engines/data": ("📡 数据与知识", "数据主权"),
    "engines/memory": ("📡 数据与知识", "知识管理"),
    "engines/knowledge": ("📡 数据与知识", "知识管理"),
    "engines/learn": ("📡 数据与知识", "学习进化"),
    "engines/evol": ("📡 数据与知识", "学习进化"),
    "engines/sync": ("📡 数据与知识", "数据主权"),
    "engines/backup": ("📡 数据与知识", "数据主权"),
    "engines/api": ("🔗 集成与桥接", "API网关"),
    "engines/gateway": ("🔗 集成与桥接", "API网关"),
    "engines/deploy": ("⚙️ 工程与部署", "部署运维"),
    "engines/setup": ("⚙️ 工程与部署", "部署运维"),
    "engines/health": ("⚙️ 工程与部署", "部署运维"),
    "engines/nginx": ("⚙️ 工程与部署", "部署运维"),
    "engines/build": ("⚙️ 工程与部署", "编译构建"),
    "engines/compil": ("⚙️ 工程与部署", "编译构建"),
    "engines/train": ("🧠 智能与推理", "模型训练"),
    "engines/lora": ("🧠 智能与推理", "模型训练"),
    "engines/distill": ("🧠 智能与推理", "模型训练"),
    "engines/model": ("🧠 智能与推理", "模型训练"),
    "engines/inference": ("🧠 智能与推理", "AI推理"),
    "engines/predict": ("🧠 智能与推理", "推演预测"),
    "engines/detect": ("🧠 智能与推理", "检测识别"),
    "engines/classif": ("🧠 智能与推理", "检测识别"),
    "engines/innovation": ("🧠 智能与推理", "推演预测"),
    "engines/seven_factor": ("🔮 哲学与数学", "数理计算"),
    "01_技能庫": ("🎭 人格与协作", "技能库"),
    "01_protocols": ("🛡️ 安全与治理", "协议规范"),
    "bin/": ("⚙️ 工程与部署", "脚本工具"),
}

# 文件名关键词 → (主分类, 子分类)
NAME_CATEGORIES: Dict[str, Tuple[str, str]] = {
    "audit": ("🛡️ 安全与治理", "审计监察"),
    "fuse": ("🛡️ 安全与治理", "熔断保护"),
    "privacy": ("🛡️ 安全与治理", "审计监察"),
    "shield": ("🛡️ 安全与治理", "审计监察"),
    "governance": ("🛡️ 安全与治理", "审计监察"),
    "sign": ("🛡️ 安全与治理", "认证签章"),
    "dna": ("🛡️ 安全与治理", "认证签章"),
    "gpg": ("🛡️ 安全与治理", "认证签章"),
    "register": ("🛡️ 安全与治理", "认证签章"),
    "persona": ("🎭 人格与协作", "人格路由"),
    "agent": ("🎭 人格与协作", "人格路由"),
    "orchestrat": ("🎭 人格与协作", "团队协作"),
    "team": ("🎭 人格与协作", "团队协作"),
    "cnsh": ("🎭 人格与协作", "人格路由"),
    "train": ("🧠 智能与推理", "模型训练"),
    "lora": ("🧠 智能与推理", "模型训练"),
    "distill": ("🧠 智能与推理", "模型训练"),
    "model": ("🧠 智能与推理", "模型训练"),
    "inference": ("🧠 智能与推理", "AI推理"),
    "predict": ("🧠 智能与推理", "推演预测"),
    "detect": ("🧠 智能与推理", "检测识别"),
    "classif": ("🧠 智能与推理", "检测识别"),
    "deploy": ("⚙️ 工程与部署", "部署运维"),
    "setup": ("⚙️ 工程与部署", "部署运维"),
    "health": ("⚙️ 工程与部署", "部署运维"),
    "nginx": ("⚙️ 工程与部署", "部署运维"),
    "build": ("⚙️ 工程与部署", "编译构建"),
    "compil": ("⚙️ 工程与部署", "编译构建"),
    "api": ("🔗 集成与桥接", "API网关"),
    "gateway": ("🔗 集成与桥接", "API网关"),
    "sync": ("📡 数据与知识", "数据主权"),
    "backup": ("📡 数据与知识", "数据主权"),
    "memory": ("📡 数据与知识", "知识管理"),
    "knowledge": ("📡 数据与知识", "知识管理"),
    "learn": ("📡 数据与知识", "学习进化"),
    "evol": ("📡 数据与知识", "学习进化"),
    "data": ("📡 数据与知识", "数据主权"),
    "math": ("🔮 哲学与数学", "数理计算"),
    "number": ("🔮 哲学与数学", "数理计算"),
    "formula": ("🔮 哲学与数学", "数理计算"),
    "bagua": ("🔮 哲学与数学", "易经体系"),
    "yijing": ("🔮 哲学与数学", "易经体系"),
    "philosophy": ("🔮 哲学与数学", "哲学引擎"),
    "dao": ("🔮 哲学与数学", "哲学引擎"),
    "tao": ("🔮 哲学与数学", "哲学引擎"),
    "video": ("🌐 交互与表达", "多媒体"),
    "visual": ("🌐 交互与表达", "多媒体"),
    "voice": ("🌐 交互与表达", "多媒体"),
    "avatar": ("🌐 交互与表达", "多媒体"),
    "image": ("🌐 交互与表达", "多媒体"),
    "chat": ("🌐 交互与表达", "人机交互"),
    "transl": ("🌐 交互与表达", "人机交互"),
    "teach": ("🌐 交互与表达", "人机交互"),
    "notion": ("📡 数据与知识", "知识管理"),
}

# 代码导入关键词 → (主分类, 子分类)
IMPORT_CATEGORIES: Dict[str, Tuple[str, str]] = {
    "torch": ("🧠 智能与推理", "模型训练"),
    "transformers": ("🧠 智能与推理", "模型训练"),
    "mlx": ("🧠 智能与推理", "模型训练"),
    "flask": ("🔗 集成与桥接", "API网关"),
    "fastapi": ("🔗 集成与桥接", "API网关"),
    "aiohttp": ("🔗 集成与桥接", "API网关"),
    "sqlite": ("📡 数据与知识", "数据主权"),
    "sqlalchemy": ("📡 数据与知识", "数据主权"),
    "cryptography": ("🛡️ 安全与治理", "认证签章"),
    "subprocess": ("⚙️ 工程与部署", "部署运维"),
    "paramiko": ("⚙️ 工程与部署", "部署运维"),
}


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "LABEL": "🏷️"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _load_rules(path: Optional[Path]) -> Dict[str, Any]:
    """加载用户覆盖规则（YAML 或 JSON）"""
    if not path:
        return {}
    if not path.exists():
        _log(f"规则文件不存在: {path}", "WARN")
        return {}

    text = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()

    if ext in (".yaml", ".yml"):
        try:
            import yaml
            return yaml.safe_load(text) or {}
        except ImportError:
            _log("未安装 PyYAML，尝试按 JSON 解析规则文件", "WARN")
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                _log(f"规则文件 JSON 解析失败: {e}", "ERROR")
                return {}
    else:
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            _log(f"规则文件 JSON 解析失败: {e}", "ERROR")
            return {}


def _classify(path_str: str, name: str, imports: List[str], desc: str) -> Tuple[str, str]:
    """基于路径、名称、导入自动分类"""
    path_lower = path_str.lower()
    name_lower = name.lower()
    desc_lower = desc.lower()

    # 1. 路径关键词（最长匹配优先）
    matched = None
    matched_len = 0
    for keyword, (cat, sub) in PATH_CATEGORIES.items():
        kw_lower = keyword.lower()
        if kw_lower in path_lower:
            if len(kw_lower) > matched_len:
                matched = (cat, sub)
                matched_len = len(kw_lower)
    if matched:
        return matched

    # 2. 文件名关键词
    for keyword, (cat, sub) in NAME_CATEGORIES.items():
        if keyword in name_lower:
            return (cat, sub)

    # 3. 导入关键词
    for imp in imports:
        imp_lower = imp.lower()
        for keyword, (cat, sub) in IMPORT_CATEGORIES.items():
            if keyword == imp_lower:
                return (cat, sub)

    # 4. 描述关键词
    desc_keywords = {
        "语音": ("🌐 交互与表达", "多媒体"),
        "图像": ("🌐 交互与表达", "多媒体"),
        "视频": ("🌐 交互与表达", "多媒体"),
        "训练": ("🧠 智能与推理", "模型训练"),
        "推理": ("🧠 智能与推理", "AI推理"),
        "审计": ("🛡️ 安全与治理", "审计监察"),
        "安全": ("🛡️ 安全与治理", "熔断保护"),
        "部署": ("⚙️ 工程与部署", "部署运维"),
        "同步": ("📡 数据与知识", "数据主权"),
        "知识": ("📡 数据与知识", "知识管理"),
        "备份": ("📡 数据与知识", "数据主权"),
    }
    for keyword, (cat, sub) in desc_keywords.items():
        if keyword in desc_lower:
            return (cat, sub)

    # 5. 默认
    return ("⚙️ 工程与部署", "脚本工具")


def _compute_ops_tags(path_str: str, name: str, description: str, lines: int, imports: List[str]) -> List[str]:
    """计算运维标签"""
    tags = []
    path_lower = path_str.lower()

    # 文档状态
    if not description or len(description) < 20 or description == "（无描述）":
        tags.append("待文档化")
    else:
        tags.append("已文档化")

    # 位置标记
    if "/engines/" in path_lower:
        tags.append("核心引擎")
    elif "/bin/" in path_lower:
        tags.append("工具脚本")
    elif "/02_SKILLS/" in path_lower:
        tags.append("技能库")

    # 复杂度
    if lines > 1000:
        tags.append("大型文件")
    elif lines < 50:
        tags.append("轻量文件")
    else:
        tags.append("中型文件")

    # 依赖特征
    imports_lower = [i.lower() for i in imports]
    if any(i in ("requests", "urllib", "httpx", "aiohttp") for i in imports_lower):
        tags.append("有网络依赖")
    if "subprocess" in imports_lower:
        tags.append("有系统调用")
    if any(i in ("torch", "transformers", "mlx", "tensorflow") for i in imports_lower):
        tags.append("AI模型依赖")
    if any(i in ("sqlite3", "sqlalchemy") for i in imports_lower):
        tags.append("数据库依赖")

    return tags


def _apply_rules(engine: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    """应用用户规则覆盖"""
    if not rules:
        return engine

    name = engine.get("name", "")
    path = engine.get("path", "")

    # 按名称精确匹配
    by_name = rules.get("by_name", {})
    if name in by_name:
        engine.update(by_name[name])

    # 按路径正则匹配
    by_path = rules.get("by_path", {})
    for pattern, overrides in by_path.items():
        if re.search(pattern, path):
            engine.update(overrides)

    # 全局追加标签
    append_tags = rules.get("append_ops_tags", [])
    if append_tags:
        existing = set(engine.get("ops_tags", []))
        existing.update(append_tags)
        engine["ops_tags"] = sorted(existing)

    return engine


def label_registry(registry: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """对注册表进行标签归类，返回新注册表和变更报告"""
    _log("开始标签归类...", "LABEL")

    labeled = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "source_registry": registry.get("dna", "unknown"),
        "total_engines": registry.get("total_engines", 0),
        "engines": [],
    }

    changes: List[Dict[str, Any]] = []
    stats = {
        "category_changed": 0,
        "subcategory_changed": 0,
        "ops_tags_changed": 0,
        "rule_overrides": 0,
        "unchanged": 0,
    }

    for eng in registry.get("engines", []):
        new_eng = dict(eng)
        path_str = new_eng.get("path", "")
        name = new_eng.get("name", "")
        desc = new_eng.get("description", "")
        imports = new_eng.get("imports", [])
        lines = new_eng.get("lines", 0)

        old_cat = new_eng.get("category", "")
        old_sub = new_eng.get("subcategory", "")
        old_tags = new_eng.get("ops_tags", [])

        new_cat, new_sub = _classify(path_str, name, imports, desc)
        new_tags = _compute_ops_tags(path_str, name, desc, lines, imports)

        new_eng["category"] = new_cat
        new_eng["subcategory"] = new_sub
        new_eng["ops_tags"] = new_tags

        # 应用用户规则
        rule_before = dict(new_eng)
        new_eng = _apply_rules(new_eng, rules)
        rule_applied = new_eng != rule_before

        change_record: Dict[str, Any] = {
            "id": new_eng.get("id"),
            "name": name,
            "path": path_str,
            "changes": {},
        }

        if old_cat != new_eng.get("category"):
            change_record["changes"]["category"] = {"from": old_cat, "to": new_eng.get("category")}
            stats["category_changed"] += 1
        if old_sub != new_eng.get("subcategory"):
            change_record["changes"]["subcategory"] = {"from": old_sub, "to": new_eng.get("subcategory")}
            stats["subcategory_changed"] += 1
        if sorted(old_tags) != sorted(new_eng.get("ops_tags", [])):
            change_record["changes"]["ops_tags"] = {"from": old_tags, "to": new_eng.get("ops_tags")}
            stats["ops_tags_changed"] += 1
        if rule_applied:
            stats["rule_overrides"] += 1

        if change_record["changes"]:
            changes.append(change_record)
        else:
            stats["unchanged"] += 1

        new_eng["labeled_at"] = _now()
        labeled["engines"].append(new_eng)

    report = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "generated_at": _now(),
        "stats": stats,
        "total_changes": len(changes),
        "changes": changes,
    }

    _log(f"归类完成: 变更 {len(changes)} 条 · 未变 {stats['unchanged']} 条", "OK")
    return labeled, report


def save_outputs(labeled: Dict[str, Any], report: Dict[str, Any], dry_run: bool, in_place: bool):
    """保存输出文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if in_place:
        target = REGISTRY_FILE
        _log("--in-place 已启用，将覆盖原注册表", "WARN")
    else:
        target = LABELED_REGISTRY_FILE

    if dry_run:
        _log(f"[DRY-RUN] 不写入文件: {target}", "SKIP")
        _log(f"[DRY-RUN] 不写入文件: {LABEL_REPORT_FILE}", "SKIP")
        return

    with open(target, "w", encoding="utf-8") as f:
        json.dump(labeled, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {target}", "OK")

    with open(LABEL_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {LABEL_REPORT_FILE}", "OK")


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎标签归类器")
    parser.add_argument("--registry", type=Path, default=REGISTRY_FILE,
                        help="输入注册表路径 (默认: data/notion_sync/engines/engine_registry.json)")
    parser.add_argument("--rules", type=Path, default=None,
                        help="用户覆盖规则文件 (YAML 或 JSON)")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅打印结果，不保存文件")
    parser.add_argument("--in-place", action="store_true",
                        help="覆盖原注册表 engine_registry.json (谨慎使用)")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    if not args.registry.exists():
        _log(f"注册表不存在: {args.registry}", "ERROR")
        sys.exit(1)

    with open(args.registry, "r", encoding="utf-8") as f:
        registry = json.load(f)

    rules = _load_rules(args.rules)
    if rules:
        _log(f"已加载规则文件: {args.rules}", "OK")

    labeled, report = label_registry(registry, rules)

    print("\n📊 归类统计:")
    for key, val in report["stats"].items():
        print(f"  {key}: {val}")
    print(f"  总变更数: {report['total_changes']}")

    save_outputs(labeled, report, args.dry_run, args.in_place)

    if args.dry_run:
        _log("DRY-RUN 模式完成，未写入任何文件", "OK")
    else:
        _log("完成", "OK")


if __name__ == "__main__":
    main()
