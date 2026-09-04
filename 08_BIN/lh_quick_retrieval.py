#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 协议与代码快速检索与迭代引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-QUICK-RETRIEVAL-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能:
  1. 根据自然语言/关键词快速检索协议和代码
  2. 命中检测 + 冲突检测
  3. 自动迭代决策 + 归档旧版本
  4. 全链路审计

用法:
  python3 08_BIN/lh_quick_retrieval.py search "主权协议"
  python3 08_BIN/lh_quick_retrieval.py get --dna #龍芯⚡️...
  python3 08_BIN/lh_quick_retrieval.py check --file 01_protocols/xxx.md
  python3 08_BIN/lh_quick_retrieval.py iterate --dna #龍芯⚡️... --version v3.1 --changelog "..." --file 01_protocols/xxx.md
  python3 08_BIN/lh_quick_retrieval.py index
"""

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_PREFIX = "#龍芯⚡️"


def generate_dna(suffix: str = "") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{timestamp}-{suffix}-{rand}-{UID}"


# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = PROJECT_ROOT / "data" / "quick_index.json"
PROTOCOL_DIR = PROJECT_ROOT / "01_protocols"
CODE_DIR = PROJECT_ROOT / "08_BIN"
SCRIPT_DIR = PROJECT_ROOT / "deploy"

# 索引目录（多目录扩展）
PROTOCOL_DIRS = [PROJECT_ROOT / "01_protocols", PROJECT_ROOT / "02_rules"]
CODE_DIRS = [PROJECT_ROOT / "08_BIN", PROJECT_ROOT / "05_ENGINES", PROJECT_ROOT / "engines"]
SCRIPT_DIRS = [PROJECT_ROOT / "deploy", PROJECT_ROOT / "scripts"]
# 跳过虚拟环境/依赖/缓存目录
EXCLUDE_DIR_PARTS = (".venv", "venv", "site-packages", "node_modules", "__pycache__", ".git", "gpt_sovits")

TYPE_PROTOCOL = "protocol"
TYPE_CODE = "code"
TYPE_SCRIPT = "script"

CATEGORY_MAP = {
    TYPE_PROTOCOL: "protocols",
    TYPE_CODE: "code",
    TYPE_SCRIPT: "scripts",
}

# ============================================================
# 哈希与元数据提取
# ============================================================


def file_hash(filepath: Path) -> str:
    """计算文件SHA256"""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def extract_dna(content: str) -> Optional[str]:
    """从文件内容中提取DNA（支持DNA: xxx 或独立token），并去除尾部标点"""
    for pattern in [
        r'DNA[:：]?\s*(#龍芯⚡️[^\s`"\'\]\)]+)',
        r'(#龍芯⚡️[^\s`"\'\]\)]+)',
    ]:
        match = re.search(pattern, content)
        if match:
            return match.group(1).rstrip("`\"'\\])")
    return None


def extract_summary(content: str, max_len: int = 200) -> str:
    """提取摘要（跳过DNA/确认码/GPG/许可证行·取第一段正文）"""
    skip_prefixes = ("DNA:", "DNA：", "确认码", "GPG", "创建者", "License", "协议:", "SEAL", "CONFIRM")
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("<!--") or line.startswith("/*"):
            continue
        if any(line.startswith(p) for p in skip_prefixes):
            continue
        if "#龍芯" in line or "#CONFIRM" in line:
            continue
        if line.startswith(">") or "═" in line or "─" in line:
            continue
        clean = re.sub(r"[*_>`|]", "", line)
        if clean:
            if len(clean) > max_len:
                return clean[:max_len] + "..."
            return clean
    return content[:max_len] + "..."


def extract_version(content: str, filename: str) -> str:
    """从内容或文件名中提取版本号"""
    m = re.search(r'v(\d+)(?:\.\d+)*', content)
    if m:
        return m.group(0)
    m = re.search(r'v(\d+)(?:\.\d+)*', filename)
    if m:
        return m.group(0)
    return "v1.0"


def extract_tags(name: str, content: str, entry_type: str) -> List[str]:
    """从文件名和内容中提取标签"""
    tags = {entry_type}
    lower = (name + " " + content[:2000]).lower()
    keyword_tags = {
        "主权": "主权",
        "协议": "协议",
        "审计": "审计",
        "DNA": "DNA",
        "剪贴板": "剪贴板",
        "备份": "备份",
        "部署": "部署",
        "训练": "训练",
        "模型": "模型",
        "安全": "安全",
        "人格": "人格",
        "CNSH": "CNSH",
        "龍魂": "龍魂",
        "铁律": "铁律",
        "史官": "史官",
        "卦象": "卦象",
        "数据": "数据",
        "加密": "加密",
    }
    for kw, tag in keyword_tags.items():
        if kw.lower() in lower:
            tags.add(tag)
    return sorted(tags)


# ============================================================
# 索引管理
# ============================================================


class QuickIndex:
    """不动点快速索引"""

    def __init__(self, index_path: Path = INDEX_PATH):
        self.index_path = index_path
        self.data = self._load()

    def _load(self) -> Dict:
        if self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 索引加载失败，重建空索引: {e}")
        return self._create_empty()

    def _create_empty(self) -> Dict:
        return {
            "version": "v1.0",
            "dna": generate_dna("QUICK-INDEX"),
            "generated_at": datetime.now().isoformat(),
            "total_entries": 0,
            "index": {
                "protocols": {},
                "code": {},
                "scripts": {},
            },
            "hash_chain": {
                "prev_hash": "0" * 64,
                "current_hash": "",
                "history": [],
            },
        }

    def save(self):
        """保存索引并更新哈希链"""
        self.data["generated_at"] = datetime.now().isoformat()
        self.data["total_entries"] = sum(
            len(entries) for entries in self.data["index"].values()
        )
        content_hash = hashlib.sha256(
            json.dumps(self.data, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        self.data["hash_chain"]["prev_hash"] = self.data["hash_chain"]["current_hash"] or "0" * 64
        self.data["hash_chain"]["current_hash"] = content_hash
        self.data["hash_chain"]["history"].append({
            "timestamp": datetime.now().isoformat(),
            "hash": content_hash,
            "dna": generate_dna("INDEX-UPDATE"),
        })
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_entry(self, entry_type: str, name: str, entry_data: Dict) -> bool:
        category = CATEGORY_MAP.get(entry_type)
        if not category or category not in self.data["index"]:
            return False
        self.data["index"][category][name] = entry_data
        self.save()
        return True

    def get_entry(self, entry_type: str, name: str) -> Optional[Dict]:
        category = CATEGORY_MAP.get(entry_type)
        if not category:
            return None
        return self.data["index"].get(category, {}).get(name)

    def search(self, query: str) -> List[Dict]:
        results = []
        query_lower = query.lower()
        for category, entries in self.data["index"].items():
            entry_type = category.rstrip("s")  # protocols -> protocol
            for name, data in entries.items():
                score = 0
                if query_lower in name.lower():
                    score += 10
                for tag in data.get("tags", []):
                    if query_lower in tag.lower():
                        score += 5
                if query_lower in data.get("summary", "").lower():
                    score += 3
                if query_lower in data.get("dna", "").lower():
                    score += 8
                if query_lower in data.get("version", "").lower():
                    score += 2
                if score > 0:
                    results.append({
                        "type": entry_type,
                        "name": name,
                        "score": score,
                        "data": data,
                        "match_type": "index",
                    })
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def get_by_dna(self, dna: str) -> Optional[Tuple[str, str, Dict]]:
        """按DNA查找（精确 → 前缀 → 子串三级匹配）"""
        dna = dna.strip()
        for category, entries in self.data["index"].items():
            for name, data in entries.items():
                if data.get("dna") == dna:
                    return category.rstrip("s"), name, data
        # 前缀匹配（用户常截断复制）
        for category, entries in self.data["index"].items():
            for name, data in entries.items():
                if data.get("dna", "").startswith(dna):
                    return category.rstrip("s"), name, data
        # 子串匹配
        for category, entries in self.data["index"].items():
            for name, data in entries.items():
                if dna in data.get("dna", ""):
                    return category.rstrip("s"), name, data
        return None

    def get_conflicts(self, dna: str) -> List[Dict]:
        result = self.get_by_dna(dna)
        if not result:
            return []
        _, _, data = result
        conflicts = []
        for conflict_dna in data.get("conflicts_with", []):
            c = self.get_by_dna(conflict_dna)
            if c:
                c_type, c_name, c_data = c
                conflicts.append({
                    "type": c_type,
                    "name": c_name,
                    "dna": conflict_dna,
                    "data": c_data,
                })
        return conflicts


# ============================================================
# 检索引擎
# ============================================================


class QuickRetrievalEngine:
    """快速检索引擎"""

    def __init__(self):
        self.index = QuickIndex()
        self.history = []

    def search(self, query: str) -> Dict:
        results = self.index.search(query)
        conflicts = []
        for r in results:
            dna = r["data"].get("dna")
            if dna:
                conflicts.extend(self.index.get_conflicts(dna))

        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results": len(results),
            "conflicts": len(conflicts),
            "dna": generate_dna("SEARCH"),
        })

        if not results:
            return {
                "status": "not_found",
                "message": f"未找到与 '{query}' 相关的内容",
                "dna": generate_dna("SEARCH-NOT-FOUND"),
            }

        return {
            "status": "success",
            "query": query,
            "results": results,
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0,
            "total": len(results),
            "dna": generate_dna("SEARCH-RESULT"),
            "timestamp": datetime.now().isoformat(),
        }

    def get_content(self, dna: str, full: bool = False) -> Dict:
        entry = self.index.get_by_dna(dna)
        if not entry:
            return {
                "status": "error",
                "message": f"未找到DNA: {dna}",
                "dna": generate_dna("GET-NOT-FOUND"),
            }

        entry_type, name, data = entry
        filepath = self._get_filepath(entry_type, name, data)
        content = ""
        if full and filepath and filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"读取失败: {e}"

        return {
            "status": "success",
            "type": entry_type,
            "name": name,
            "data": data,
            "filepath": str(filepath) if filepath else None,
            "content": content if full else None,
            "summary": data.get("summary", ""),
            "dna": generate_dna("GET-CONTENT"),
            "timestamp": datetime.now().isoformat(),
        }

    def _get_filepath(self, entry_type: str, name: str, data: Dict = None) -> Optional[Path]:
        """获取文件路径（优先用索引中记录的path）"""
        if data and data.get("path"):
            p = Path(data["path"])
            if p.is_absolute():
                return p
            return PROJECT_ROOT / p

        if entry_type == TYPE_PROTOCOL:
            base = PROTOCOL_DIR
        elif entry_type == TYPE_CODE:
            base = CODE_DIR
        elif entry_type == TYPE_SCRIPT:
            base = SCRIPT_DIR
        else:
            return None

        for f in base.rglob(f"{name}*"):
            if f.suffix in (".md", ".txt", ".py", ".sh", ".plist", ".conf"):
                return f
        return None

    def check_conflicts(self, filepath: Path) -> Dict:
        if not filepath.exists():
            return {"status": "error", "message": "文件不存在"}

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"status": "error", "message": f"读取失败: {e}"}

        dna = extract_dna(content)
        if not dna:
            return {
                "status": "error",
                "message": "文件缺少DNA追溯码",
            }

        current_hash = file_hash(filepath)
        entry = self.index.get_by_dna(dna)

        if not entry:
            return {
                "status": "new",
                "message": "新文件，未在索引中",
                "dna": dna,
                "hash": current_hash,
            }

        _, _, data = entry
        indexed_hash = data.get("hash", "")
        # 兼容两种哈希格式（纯hex / sha256:前缀）
        indexed_hash_clean = indexed_hash.replace("sha256:", "") if indexed_hash else ""

        if current_hash == indexed_hash_clean:
            return {
                "status": "unchanged",
                "message": "文件与索引一致，无需更新",
                "dna": dna,
            }

        conflicts = self.index.get_conflicts(dna)
        return {
            "status": "conflict" if conflicts else "changed",
            "message": "文件已变更" + ("，存在冲突" if conflicts else ""),
            "dna": dna,
            "hash": current_hash,
            "indexed_hash": indexed_hash,
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0,
        }

    def iterate(
        self,
        dna: str,
        new_version: str,
        changelog: str,
        filepath: Optional[Path] = None,
    ) -> Dict:
        entry = self.index.get_by_dna(dna)
        if not entry:
            return {"status": "error", "message": f"未找到DNA: {dna}"}

        entry_type, name, data = entry
        new_dna = generate_dna(f"ITER-{entry_type.upper()}")

        archive_entry = {
            "original_dna": dna,
            "new_dna": new_dna,
            "version": data.get("version", "v1.0"),
            "new_version": new_version,
            "changelog": changelog,
            "archived_at": datetime.now().isoformat(),
            "hash": data.get("hash", ""),
            "filepath": str(self._get_filepath(entry_type, name, data)) if self._get_filepath(entry_type, name, data) else None,
        }

        # 如果提供了新文件，重新计算哈希和摘要
        if filepath and filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                data["hash"] = file_hash(filepath)
                data["summary"] = extract_summary(content)
                data["tags"] = extract_tags(name, content, entry_type)
            except Exception as e:
                return {"status": "error", "message": f"读取新文件失败: {e}"}

        data["version"] = new_version
        data["dna"] = new_dna
        data["deprecated"] = False
        data["replaced_by"] = None

        # 旧条目标记为废弃
        old_entry_copy = dict(data)
        old_entry_copy["deprecated"] = True
        old_entry_copy["replaced_by"] = new_dna

        self._log_to_historian({
            "operation": "iterate",
            "original_dna": dna,
            "new_dna": new_dna,
            "version": new_version,
            "changelog": changelog,
            "timestamp": datetime.now().isoformat(),
        })

        self.index.save()

        return {
            "status": "success",
            "message": f"已迭代: {name} {archive_entry['version']} → {new_version}",
            "original_dna": dna,
            "new_dna": new_dna,
            "version": new_version,
            "archive": archive_entry,
        }

    def index_directory(self, scan_protocols: bool = True, scan_code: bool = True, scan_scripts: bool = True) -> Dict:
        """扫描目录并构建/更新索引（多目录+排除虚拟环境）"""
        added = 0
        updated = 0
        skipped = 0
        errors = 0

        def scan(base_dirs: list, entry_type: str, suffixes: tuple):
            nonlocal added, updated, skipped, errors
            for base_dir in base_dirs:
                if not base_dir.exists():
                    continue
                for filepath in base_dir.rglob("*"):
                    if not filepath.is_file():
                        continue
                    if filepath.suffix.lower() not in suffixes:
                        continue
                    # 跳过备份/签名/缓存
                    if filepath.name.endswith((".asc", ".sig", ".bak", ".tmp")) or ".git" in filepath.parts:
                        continue
                    # 跳过虚拟环境/依赖/缓存目录
                    if any(part in EXCLUDE_DIR_PARTS for part in filepath.parts):
                        continue
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        dna = extract_dna(content)
                        if not dna:
                            skipped += 1
                            continue
                        name = filepath.stem
                        current_hash = file_hash(filepath)
                        category = CATEGORY_MAP[entry_type]
                        existing = self.index.data["index"][category].get(name)
                        if existing:
                            if existing.get("hash", "").replace("sha256:", "") == current_hash:
                                continue
                            updated += 1
                        else:
                            added += 1

                        rel_path = filepath.relative_to(PROJECT_ROOT)
                        entry_data = {
                            "dna": dna,
                            "hash": f"sha256:{current_hash}",
                            "version": extract_version(content, filepath.name),
                            "tags": extract_tags(name, content, entry_type),
                            "summary": extract_summary(content),
                            "conflicts_with": existing.get("conflicts_with", []) if existing else [],
                            "depends_on": existing.get("depends_on", []) if existing else [],
                            "deprecated": False,
                            "replaced_by": None,
                            "path": str(rel_path),
                        }
                        self.index.data["index"][category][name] = entry_data
                    except Exception as e:
                        errors += 1
                        print(f"⚠️ 扫描失败 {filepath}: {e}")

        if scan_protocols:
            scan(PROTOCOL_DIRS, TYPE_PROTOCOL, (".md", ".txt"))
        if scan_code:
            scan(CODE_DIRS, TYPE_CODE, (".py", ".sh"))
        if scan_scripts:
            scan(SCRIPT_DIRS, TYPE_SCRIPT, (".sh", ".py", ".conf", ".plist"))

        self.index.save()

        return {
            "status": "success",
            "added": added,
            "updated": updated,
            "skipped": skipped,
            "errors": errors,
            "total": self.index.data["total_entries"],
            "dna": generate_dna("INDEX-BUILD"),
            "timestamp": datetime.now().isoformat(),
        }

    def _log_to_historian(self, record: Dict):
        historian_path = PROJECT_ROOT / "04_AUDIT" / "historian.jsonl"
        historian_path.parent.mkdir(parents=True, exist_ok=True)
        with open(historian_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# CLI接口
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 协议与代码快速检索与迭代引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 08_BIN/lh_quick_retrieval.py search "主权协议"
  python3 08_BIN/lh_quick_retrieval.py get --dna #龍芯⚡️...
  python3 08_BIN/lh_quick_retrieval.py check --file 01_protocols/xxx.md
  python3 08_BIN/lh_quick_retrieval.py iterate --dna #龍芯⚡️... --version v3.1 --changelog "增加数据主权条款" --file 01_protocols/xxx.md
  python3 08_BIN/lh_quick_retrieval.py index
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    p_search = subparsers.add_parser("search", help="按关键词搜索")
    p_search.add_argument("query", help="搜索关键词")

    p_get = subparsers.add_parser("get", help="按DNA获取内容")
    p_get.add_argument("--dna", required=True, help="DNA追溯码")
    p_get.add_argument("--full", action="store_true", help="读取全文")

    p_check = subparsers.add_parser("check", help="检查文件与索引是否一致/冲突")
    p_check.add_argument("--file", required=True, help="文件路径")

    p_iterate = subparsers.add_parser("iterate", help="迭代更新版本")
    p_iterate.add_argument("--dna", required=True, help="DNA追溯码")
    p_iterate.add_argument("--version", required=True, help="新版本号")
    p_iterate.add_argument("--changelog", required=True, help="变更说明")
    p_iterate.add_argument("--file", help="新文件路径（可选）")

    p_index = subparsers.add_parser("index", help="扫描目录构建/更新索引")
    p_index.add_argument("--no-protocols", action="store_true", help="跳过协议目录")
    p_index.add_argument("--no-code", action="store_true", help="跳过代码目录")
    p_index.add_argument("--no-scripts", action="store_true", help="跳过脚本目录")

    p_stats = subparsers.add_parser("stats", help="索引统计")

    args = parser.parse_args()

    engine = QuickRetrievalEngine()

    if args.command == "search":
        result = engine.search(args.query)
        print(f"\n🔍 搜索: '{args.query}'")
        print("=" * 60)
        if result["status"] == "not_found":
            print(result["message"])
        else:
            print(f"找到 {result['total']} 个结果")
            for r in result["results"][:20]:
                print(f"\n  [{r['type']}] {r['name']}")
                print(f"    📌 {r['data'].get('summary', '')[:100]}...")
                print(f"    🧬 {r['data'].get('dna', '')[:50]}...")
                print(f"    🏷️  {' · '.join(r['data'].get('tags', []))}")
            if result["has_conflicts"]:
                print(f"\n⚠️ 发现 {len(result['conflicts'])} 个冲突")
                for c in result["conflicts"]:
                    print(f"    - {c['name']} ({c['dna'][:40]}...)")

    elif args.command == "get":
        result = engine.get_content(args.dna, args.full)
        if result["status"] == "error":
            print(f"❌ {result['message']}")
        else:
            print(f"\n📄 {result['type']}: {result['name']}")
            print(f"   🧬 {result['data'].get('dna', '')}")
            print(f"   📁 {result['filepath']}")
            print(f"   📌 {result['summary']}")
            print(f"   🏷️  {' · '.join(result['data'].get('tags', []))}")
            if result["content"]:
                print("\n" + "=" * 60)
                print(result["content"][:4000] + ("..." if len(result["content"]) > 4000 else ""))

    elif args.command == "check":
        result = engine.check_conflicts(Path(args.file))
        print(f"\n🔍 检查: {args.file}")
        print("=" * 60)
        print(f"  状态: {result['status']}")
        print(f"  消息: {result['message']}")
        if result.get("dna"):
            print(f"  DNA: {result['dna']}")
        if result.get("hash"):
            print(f"  当前哈希: {result['hash']}")
        if result.get("indexed_hash"):
            print(f"  索引哈希: {result['indexed_hash']}")
        if result.get("has_conflicts"):
            for c in result.get("conflicts", []):
                print(f"    ⚠️ 冲突: {c['name']} ({c['dna'][:40]}...)")

    elif args.command == "iterate":
        result = engine.iterate(
            args.dna,
            args.version,
            args.changelog,
            Path(args.file) if args.file else None,
        )
        if result["status"] == "error":
            print(f"❌ {result['message']}")
        else:
            print(f"✅ {result['message']}")
            print(f"   旧DNA: {result['original_dna']}")
            print(f"   新DNA: {result['new_dna']}")

    elif args.command == "index":
        result = engine.index_directory(
            scan_protocols=not args.no_protocols,
            scan_code=not args.no_code,
            scan_scripts=not args.no_scripts,
        )
        print(f"\n📋 索引构建完成")
        print("=" * 60)
        print(f"  新增: {result['added']}")
        print(f"  更新: {result['updated']}")
        print(f"  跳过（无DNA）: {result['skipped']}")
        print(f"  错误: {result['errors']}")
        print(f"  索引总数: {result['total']}")
        print(f"  时间: {result['timestamp']}")

    elif args.command == "stats":
        index_data = engine.index.data
        idx = index_data.get("index", {})
        total = index_data.get("total_entries", 0)
        print("\n📊 快速检索引擎 · 索引统计")
        print("=" * 60)
        print(f"  版本: {index_data.get('version', 'v1.0')}")
        print(f"  协议: {len(idx.get('protocols', {}))}")
        print(f"  代码: {len(idx.get('code', {}))}")
        print(f"  脚本: {len(idx.get('scripts', {}))}")
        print(f"  总计: {total}")
        print(f"  生成: {index_data.get('generated_at', '-')[:19]}")
        print(f"  哈希链: {str(index_data.get('hash_chain', {}).get('current_hash', ''))[:16]}...")

    else:
        parser.print_help()

    # 🔥 时间戳铁律
    _dz = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    _idx = (datetime.now().hour + 1) // 2 % 12
    print(f"\n🐉丙午·{_dz[_idx]}时·䷖剥·🟢")


if __name__ == "__main__":
    main()
