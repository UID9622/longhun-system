#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-DISCOVERY-v1.0-8C41940D
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
🐉 龍魂 · Notion 引擎发现扫描器 v1.1
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-DISCOVERY-v1.0-8C41940D
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

扫描 engines/ bin/ 02_SKILLS/ 下所有引擎文件，提取元数据，生成 Notion 导入就绪的注册表 JSON。

用法:
  python3 bin/lh_notion_engine_discovery.py              # 全量扫描→data/notion_sync/engine_registry.json
  python3 bin/lh_notion_engine_discovery.py --output md  # 输出 Markdown 表格
  python3 bin/lh_notion_engine_discovery.py --scan bin   # 只扫描 bin/
  python3 bin/lh_notion_engine_discovery.py --diff       # 增量：只输出变更
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import time
import warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-DISCOVERY-v1.0-8C41940D"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SCHEMA_VERSION = "1.1.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
REGISTRY_FILE = OUTPUT_DIR / "engine_registry.json"
STATE_FILE = OUTPUT_DIR / "discovery_state.json"
TESTS_DIR = ROOT / "tests"

# ── 扫描目标 ─────────────────────────────────────────
SCAN_TARGETS = {
    "engines": {
        "path": ROOT / "engines",
        "type": "engine",
        "priority": 1,  # P1=核心引擎
    },
    "bin": {
        "path": ROOT / "bin",
        "type": "script",
        "priority": 2,  # P2=工具脚本
    },
    "skills": {
        "path": ROOT / "01_技能庫",
        "type": "skill",
        "priority": 3,  # P3=技能库
    },
}

# ── 需要跳过的目录 ───────────────────────────────────
SKIP_DIRS = {
    "__pycache__", ".venv", "venv", "node_modules", ".git", ".hg", ".svn",
    "_archive", ".archive", ".pytest_cache", ".mypy_cache", ".tox",
    ".DS_Store", ".idea", ".vscode", ".claude", ".codebuddy",
}

# ── 多级分类规则 ─────────────────────────────────────
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


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "SCAN": "🔍"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _file_hash(path: Path) -> str:
    """文件内容 SHA256（前8字符）"""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def _extract_dna(content: str) -> Optional[str]:
    """从文件头提取 DNA 字符串，支持 # DNA: 和 docstring 内 DNA:"""
    for line in content.split("\n")[:50]:
        # 匹配：DNA: #龍芯... 或 # DNA: #龍芯...
        m = re.search(r'DNA[:\s]+(#龍芯[^\n]+)', line)
        if m:
            return m.group(1).strip()
    return None


def _extract_docstring(content: str) -> Optional[str]:
    """提取模块 docstring（第一段非元信息）"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(content)
        doc = ast.get_docstring(tree)
        if doc:
            lines = [l.strip() for l in doc.split("\n") if l.strip()]
            # 跳过 DNA/创建者/协议 行
            body = [l for l in lines if not l.startswith(("DNA:", "创建者:", "协议:", "CC ", "🐉 "))]
            return body[0][:200] if body else lines[-1][:200]
    except SyntaxError:
        pass
    return None


def _extract_imports(content: str) -> List[str]:
    """提取 import 的顶层模块名"""
    imports = set()
    for line in content.split("\n"):
        line = line.strip()
        m = re.match(r'^(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
        if m:
            mod = m.group(1)
            if mod not in ("__future__",):
                imports.add(mod)
    return sorted(imports)


def _extract_functions(content: str) -> List[str]:
    """提取顶层函数名"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(content)
        funcs = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    funcs.append(node.name)
        return funcs[:30]
    except SyntaxError:
        return []


def _extract_classes(content: str) -> List[str]:
    """提取类名"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(content)
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes
    except SyntaxError:
        return []


def _classify_engine(filepath: Path, content: str) -> Tuple[str, str]:
    """多级分类：路径优先→文件名→代码内容"""
    path_str = str(filepath).lower()
    name = filepath.stem.lower()

    # 1. 路径关键词匹配（最长路径优先）
    matched = None
    matched_len = 0
    for keyword, (cat, sub) in PATH_CATEGORIES.items():
        kw_lower = keyword.lower()
        if kw_lower in path_str:
            if len(kw_lower) > matched_len:
                matched = (cat, sub)
                matched_len = len(kw_lower)
    if matched:
        return matched

    # 2. 文件名关键词匹配
    for keyword, (cat, sub) in NAME_CATEGORIES.items():
        if keyword in name:
            return (cat, sub)

    # 3. 代码内容推断
    code_lower = content[:5000].lower()
    import_keywords = {
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
    for kw, (cat, sub) in import_keywords.items():
        if kw in code_lower:
            return (cat, sub)

    # 4. 默认：工程执行
    return ("⚙️ 工程与部署", "脚本工具")


def _has_test_file(filepath: Path) -> bool:
    """检查是否存在对应的测试文件"""
    name = filepath.stem
    # 常见测试文件名模式
    candidates = [
        TESTS_DIR / f"test_{name}.py",
        TESTS_DIR / f"{name}_test.py",
        filepath.parent / f"test_{name}.py",
        filepath.parent / f"{name}_test.py",
    ]
    return any(c.exists() for c in candidates)


def _compute_ops_tags(filepath: Path, content: str) -> List[str]:
    """计算运维标记标签"""
    tags = []
    path_str = str(filepath).lower()
    name = filepath.stem.lower()

    # 文档状态
    doc = _extract_docstring(content)
    if not doc or len(doc) < 20:
        tags.append("待文档化")

    # 测试状态
    if not _has_test_file(filepath) and "test" not in name and "_test" not in path_str:
        tags.append("未测试")
    else:
        tags.append("已测试")

    # 位置标记
    if "/engines/" in path_str:
        tags.append("核心引擎")
    elif "/bin/" in path_str:
        tags.append("工具脚本")
    elif "/02_SKILLS/" in path_str:
        tags.append("技能库")

    # 复杂度标记
    lines = content.count("\n")
    if lines > 1000:
        tags.append("大型文件")
    elif lines < 50:
        tags.append("轻量文件")
    else:
        tags.append("中型文件")

    # 状态标记
    head = content[:500].lower()
    if "deprecated" in head or "废弃" in head:
        tags.append("已废弃")
    if "experimental" in head or "实验" in head:
        tags.append("实验性")
    if "TODO" in content or "FIXME" in content:
        tags.append("待修复")

    # 依赖标记
    if "requests" in content or "urllib" in content:
        tags.append("有网络依赖")
    if "subprocess" in content:
        tags.append("有系统调用")

    return tags


def _should_skip_dir(path: Path) -> bool:
    """判断路径是否包含需要跳过的目录"""
    return any(part in SKIP_DIRS for part in path.parts)


def scan_file(filepath: Path, target_type: str, target_priority: int) -> Optional[Dict[str, Any]]:
    """扫描单个文件，返回引擎条目"""
    if not filepath.exists():
        _log(f"跳过不存在路径: {filepath.name}", "SKIP")
        return None
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        _log(f"跳过二进制/无权限/断链: {filepath.name}", "SKIP")
        return None

    lines = content.count("\n")
    size = len(content.encode("utf-8"))

    if lines < 5 and size < 200:
        return None  # 太短，跳过

    relpath = str(filepath.relative_to(ROOT))
    dna = _extract_dna(content)
    docstring = _extract_docstring(content)
    imports = _extract_imports(content)
    functions = _extract_functions(content)
    classes = _extract_classes(content)
    category, subcategory = _classify_engine(filepath, content)
    ops_tags = _compute_ops_tags(filepath, content)
    file_hash = _file_hash(filepath)

    entry = {
        "id": f"ENG-{file_hash}",
        "name": filepath.stem,
        "filename": filepath.name,
        "path": relpath,
        "dna": dna or "未注册",
        "description": docstring or "（无描述）",
        "category": category,
        "subcategory": subcategory,
        "type": target_type,
        "priority": target_priority,
        "lines": lines,
        "size_bytes": size,
        "hash": file_hash,
        "imports": imports[:20],
        "functions": functions[:15],
        "classes": classes,
        "ops_tags": ops_tags,
        "status": "active",
        "scanned_at": _now(),
    }
    return entry


def scan_all(targets: Optional[List[str]] = None) -> Dict[str, Any]:
    """全量扫描所有目标目录"""
    _log("开始全量扫描...", "SCAN")
    start_ts = time.time()

    registry: Dict[str, Any] = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "total_engines": 0,
        "engines": [],
        "stats": {
            "by_category": {},
            "by_subcategory": {},
            "by_type": {},
            "by_status": {},
            "total_lines": 0,
            "total_size_bytes": 0,
        },
        "scan_duration_ms": 0,
    }

    targets_to_scan = targets or list(SCAN_TARGETS.keys())
    engines: List[Dict[str, Any]] = []

    for target_name in targets_to_scan:
        if target_name not in SCAN_TARGETS:
            _log(f"未知扫描目标: {target_name}", "WARN")
            continue

        cfg = SCAN_TARGETS[target_name]
        target_path = cfg["path"]
        target_type = cfg["type"]
        target_priority = cfg["priority"]

        if not target_path.exists():
            _log(f"目标路径不存在: {target_path}", "WARN")
            continue

        _log(f"扫描 {target_name}/ ({target_type}) ...", "SCAN")
        count = 0
        for py_file in sorted(target_path.rglob("*.py")):
            if _should_skip_dir(py_file):
                continue

            entry = scan_file(py_file, target_type, target_priority)
            if entry:
                engines.append(entry)
                count += 1

                cat = entry["category"]
                sub = entry["subcategory"]
                etype = entry["type"]
                status = entry["status"]

                registry["stats"]["by_category"][cat] = registry["stats"]["by_category"].get(cat, 0) + 1
                registry["stats"]["by_subcategory"][f"{cat} > {sub}"] = (
                    registry["stats"]["by_subcategory"].get(f"{cat} > {sub}", 0) + 1
                )
                registry["stats"]["by_type"][etype] = registry["stats"]["by_type"].get(etype, 0) + 1
                registry["stats"]["by_status"][status] = registry["stats"]["by_status"].get(status, 0) + 1
                registry["stats"]["total_lines"] += entry["lines"]
                registry["stats"]["total_size_bytes"] += entry["size_bytes"]

        _log(f"  → {count} 个文件", "OK")

    elapsed_ms = int((time.time() - start_ts) * 1000)
    registry["total_engines"] = len(engines)
    registry["engines"] = engines
    registry["scan_duration_ms"] = elapsed_ms
    _log(f"扫描完成: {registry['total_engines']} 个引擎 · {elapsed_ms}ms", "OK")

    return registry


def scan_diff() -> Dict[str, Any]:
    """增量扫描：只输出变更的文件"""
    _log("增量扫描模式...", "SCAN")

    prev_state: Dict[str, str] = {}
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            prev_state = json.load(f).get("hashes", {})

    current = scan_all()
    diff = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "new": [],
        "changed": [],
        "deleted": [],
        "unchanged": 0,
    }

    current_hashes: Dict[str, str] = {}
    for eng in current["engines"]:
        current_hashes[eng["path"]] = eng["hash"]
        prev_hash = prev_state.get(eng["path"])
        if prev_hash is None:
            diff["new"].append(eng)
        elif prev_hash != eng["hash"]:
            diff["changed"].append(eng)

    for old_path in prev_state:
        if old_path not in current_hashes:
            diff["deleted"].append({"path": old_path, "previous_hash": prev_state[old_path]})

    diff["unchanged"] = len(current_hashes) - len(diff["new"]) - len(diff["changed"])

    _log(
        f"变更: +{len(diff['new'])} ~{len(diff['changed'])} -{len(diff['deleted'])} ={diff['unchanged']}",
        "OK",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"dna": DNA, "schema_version": SCHEMA_VERSION, "updated_at": _now(), "hashes": current_hashes}, f, ensure_ascii=False, indent=2)

    return diff


def save_registry(registry: Dict[str, Any]):
    """保存注册表到文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    _log(f"注册表已保存: {REGISTRY_FILE}", "OK")


def _key(engine: Dict[str, Any]) -> Tuple[str, str, str]:
    """排序键：分类→子分类→文件名"""
    return (engine.get("category", ""), engine.get("subcategory", ""), engine.get("name", ""))


def render_markdown(registry: Dict[str, Any]) -> str:
    """渲染为 Markdown 表格"""
    engines = sorted(registry["engines"], key=_key)
    stats = registry["stats"]

    md = f"""# 🐉 龍魂引擎注册表

> DNA: {DNA}
> Schema: {SCHEMA_VERSION}
> 生成时间: {registry["generated_at"]}
> 引擎总数: {registry["total_engines"]}
> 代码总行数: {stats["total_lines"]}
> 代码总体积: {stats["total_size_bytes"]:,} bytes
> 扫描耗时: {registry.get("scan_duration_ms", 0)} ms

## 统计概览

### 按一级分类

| 分类 | 数量 |
|:---|:---:|
"""
    for cat, cnt in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        md += f"| {cat} | {cnt} |\n"

    md += "\n### 按子分类\n\n| 分类 | 数量 |\n|:---|:---:|\n"
    for sub, cnt in sorted(stats["by_subcategory"].items(), key=lambda x: -x[1]):
        md += f"| {sub} | {cnt} |\n"

    md += f"""
## 引擎清单

| # | 名称 | 分类 | 子分类 | 类型 | 行数 | DNA | 说明 |
|:---:|:---|:---|:---|:---|:---:|:---|:---|
"""
    for i, eng in enumerate(engines, 1):
        desc = (eng.get("description") or "")[:60].replace("|", "\\|").replace("\n", " ")
        dna_short = (eng.get("dna") or "未注册")[:30]
        md += f"| {i} | `{eng['name']}` | {eng['category']} | {eng['subcategory']} | {eng['type']} | {eng['lines']} | {dna_short} | {desc} |\n"

    return md


def show_stats(registry: Dict[str, Any]):
    """终端友好统计输出"""
    stats = registry["stats"]
    print(f"\n{'='*60}")
    print(f"  龍魂引擎注册表 · {registry['generated_at']}")
    print(f"  Schema: {registry['schema_version']}")
    print(f"  引擎总数: {registry['total_engines']}  ·  代码: {stats['total_lines']:,} 行  ·  {stats['total_size_bytes']//1024:,} KB")
    print(f"  扫描耗时: {registry.get('scan_duration_ms', 0)} ms")
    print(f"{'='*60}\n")

    print("📊 按一级分类:")
    for cat, cnt in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        bar = "█" * max(1, cnt // 3)
        print(f"  {cat:20s} {cnt:4d}  {bar}")

    print(f"\n📊 按类型:")
    for etype, cnt in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {etype:12s} {cnt:4d}")

    tag_counts: Dict[str, int] = {}
    for eng in registry["engines"]:
        for tag in eng.get("ops_tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    print(f"\n🏷️  运维标记 Top 10:")
    for tag, cnt in sorted(tag_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  #{tag:15s} {cnt:4d}")


# ── 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎发现扫描器")
    parser.add_argument("--scan", nargs="*", choices=list(SCAN_TARGETS.keys()),
                        help="指定扫描目标（默认全部）")
    parser.add_argument("--output", choices=["json", "md"], default="json",
                        help="输出格式 (默认 json)")
    parser.add_argument("--diff", action="store_true",
                        help="增量模式：只输出变更")
    parser.add_argument("--stats-only", action="store_true",
                        help="仅显示统计")
    parser.add_argument("--no-save", action="store_true",
                        help="不保存到文件")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    if args.diff:
        result = scan_diff()
        if not args.no_save:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(OUTPUT_DIR / "engine_diff.json", "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            _log("增量报告已保存", "OK")
    else:
        targets = args.scan if args.scan else None
        registry = scan_all(targets)
        show_stats(registry)

        if not args.no_save:
            save_registry(registry)

        if args.output == "md":
            md_content = render_markdown(registry)
            md_path = OUTPUT_DIR / "engine_registry.md"
            with open(md_path, "w") as f:
                f.write(md_content)
            _log(f"Markdown 已保存: {md_path}", "OK")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
