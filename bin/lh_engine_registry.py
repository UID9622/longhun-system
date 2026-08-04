#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·甲辰·離為火-ENGINE-REGISTRY-v1.0-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·引擎统一注册表 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━
自动发现全项目所有 Python 脚本/引擎，分类归集，去重检测，生成统一注册表。

用法:
    python3 bin/lh_engine_registry.py scan          # 全量扫描生成注册表
    python3 bin/lh_engine_registry.py stats         # 显示统计
    python3 bin/lh_engine_registry.py find <关键词>  # 按关键词查找引擎
    python3 bin/lh_engine_registry.py dupes          # 检测重复/冗余
    python3 bin/lh_engine_registry.py export         # 导出 JSON 注册表
    python3 bin/lh_engine_registry.py --json         # JSON 输出（管道友好）

注册表输出: data/engine_registry.json
"""

import os, sys, re, json, hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "data" / "engine_registry.json"
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

# ─── 扫描范围 ───
SCAN_DIRS = [
    ("bin", ROOT / "bin", True),         # 核心脚本
    ("engines", ROOT / "engines", True), # 引擎层
    ("scripts", ROOT / "scripts", True), # 运维脚本
    ("tools", ROOT / "tools", True),     # 工具集
    ("layers", ROOT / "layers", True),   # 分层架构
    ("cnsh", ROOT / "cnsh", True),       # CNSH 编译器
    ("governance", ROOT / "governance", True), # 治理
    ("audit", ROOT / "audit", True),     # 审计
    ("01_技能庫", ROOT / "01_技能庫", False), # 技能库
    ("skills", ROOT / "skills", False),  # 技能系统
]

# 排除模式
EXCLUDE_PATTERNS = [
    "__pycache__", ".venv", "GPT_SoVITS", "gpt_sovits",
    ".asc", "node_modules", ".git"
]

# ─── 功能分类映射 ───
CATEGORY_KEYWORDS = {
    "🧠 AI训练": ["train", "lora", "fine_tune", "mlx", "ollama", "checkpoint", "fuse", "gguf", "dataset", "sample", "data_gen"],
    "🛡️ 安全审计": ["audit", "security", "governance", "fuse", "meltdown", "patrol", "veto", "sovereign", "guard", "shield", "defend", "firewall"],
    "🧬 DNA/身份": ["dna", "gpg", "sign", "identity", "ganzhi", "hash", "registry", "verify", "validate"],
    "🤖 人格系统": ["persona", "agent", "orchestrat", "scheduler", "router", "dispatch", "character"],
    "📝 CNSH语言": ["cnsh", "compiler", "interpreter", "syntax", "editor", "parser"],
    "💾 记忆/存储": ["memory", "vault", "store", "archive", "freeze", "eternity", "snapshot", "backup", "sync"],
    "🌐 API/服务": ["api", "server", "fastapi", "flask", "gateway", "bridge", "relay", "endpoint", "web"],
    "📊 数据/分析": ["data", "analy", "metric", "monitor", "dashboard", "report", "stats", "track", "scan", "health"],
    "🎬 视频/媒体": ["video", "media", "3d", "image", "visual", "avatar", "voice", "audio", "commentary"],
    "📚 知识/学习": ["knowledge", "learn", "teach", "train_data", "corpus", "notion", "article", "document", "paper"],
    "🔮 推演/博弈": ["sandbox", "predict", "simulate", "seven_dimension", "yijing", "quantum", "wuxing", "bagua", "iching"],
    "🔄 同步/集成": ["sync", "notion", "bridge", "integrat", "migrate", "import", "export", "absorb"],
    "💬 语义/沟通": ["semantic", "intent", "emotion", "sentiment", "translate", "tongxinyi", "anxiety", "lie"],
    "⚙️ 系统/运维": ["deploy", "setup", "install", "config", "systemd", "launchd", "health", "check", "daemon", "watchdog"],
    "💰 经济/审计": ["price", "ecom", "cost", "finance", "pay", "audit_price", "trust", "market"],
    "🧹 工具/杂项": ["util", "helper", "tool", "fix", "clean", "organize", "convert", "format", "template"],
}


class EngineRegistry:
    """龍魂引擎统一注册表"""

    def __init__(self):
        self.engines: List[Dict] = []
        self.by_category: Dict[str, List] = defaultdict(list)
        self.by_dir: Dict[str, List] = defaultdict(list)
        self.duplicates: List[Tuple] = []
        self.stats = {}

    def scan(self) -> Dict:
        """全量扫描所有 Python 脚本"""
        self.engines = []
        total_scanned = 0
        total_skipped = 0

        for dir_tag, dir_path, recursive in SCAN_DIRS:
            if not dir_path.exists():
                continue
            pattern = "**/*.py" if recursive else "*.py"
            for f in dir_path.glob(pattern):
                total_scanned += 1
                # 排除检查
                skip = False
                for exc in EXCLUDE_PATTERNS:
                    if exc in str(f):
                        skip = True
                        break
                if skip:
                    total_skipped += 1
                    continue
                if not f.exists() or f.is_symlink():
                    total_skipped += 1
                    continue

                try:
                    engine_info = self._extract_info(f, dir_tag)
                    if engine_info:
                        self.engines.append(engine_info)
                except Exception:
                    total_skipped += 1

        # 后处理
        self._categorize()
        self._find_duplicates()
        self._compute_stats(total_scanned, total_skipped)

        return self._build_report()

    def _extract_info(self, filepath: Path, dir_tag: str) -> Optional[Dict]:
        """提取单个脚本的元数据"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return None

        name = filepath.stem
        size_kb = round(filepath.stat().st_size / 1024, 1)
        lines = content.count('\n') + 1

        # DNA
        dna = ""
        for line in content.split('\n')[:8]:
            if 'DNA:' in line or '龍芯' in line:
                dna = line.strip()[:120]
                break

        # 功能分类
        category = self._classify(name, content)

        # 入口类型
        has_main = "if __name__" in content
        has_argparse = "argparse" in content and "add_argument" in content
        has_fastapi = "FastAPI" in content
        has_flask = "flask" in content.lower() and "Flask" in content
        has_click = "click.command" in content or "click.group" in content

        entry_type = "library"  # 默认
        if has_fastapi:
            entry_type = "api_fastapi"
        elif has_flask:
            entry_type = "api_flask"
        elif has_argparse:
            entry_type = "cli_argparse"
        elif has_main and "sys.argv" in content:
            entry_type = "cli_basic"
        elif has_click:
            entry_type = "cli_click"
        elif has_main:
            entry_type = "script"

        # 关键函数/类
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)

        # import 依赖
        bin_imports = list(set(re.findall(r'(?:from bin\.|import bin\.)(\w+)', content)))
        engine_imports = list(set(re.findall(r'(?:from engines\.|import engines\.)(\w+)', content)))

        # 版本估算 (从文件名或内容中)
        version = "unknown"
        ver_match = re.search(r'[vV](\d+\.\d+(?:\.\d+)?)', name + content[:500])
        if ver_match:
            version = f"v{ver_match.group(1)}"

        rel_path = str(filepath.relative_to(ROOT))

        return {
            "name": name,
            "path": rel_path,
            "dir": dir_tag,
            "size_kb": size_kb,
            "lines": lines,
            "dna": dna,
            "category": category,
            "entry_type": entry_type,
            "has_main": has_main,
            "has_argparse": has_argparse,
            "version": version,
            "classes": classes[:10],
            "functions": functions[:20],
            "bin_imports": bin_imports[:10],
            "engine_imports": engine_imports[:5],
        }

    def _classify(self, name: str, content: str) -> str:
        """自动分类"""
        combined = (name + content[:2000]).lower()
        scores = Counter()
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in combined:
                    scores[cat] += 1
        if scores:
            return scores.most_common(1)[0][0]
        return "🧹 工具/杂项"

    def _categorize(self):
        """按分类和目录重组"""
        self.by_category = defaultdict(list)
        self.by_dir = defaultdict(list)
        for e in self.engines:
            self.by_category[e["category"]].append(e)
            self.by_dir[e["dir"]].append(e)

    def _find_duplicates(self):
        """检测重复/冗余脚本"""
        self.duplicates = []
        # 按名称相似度检测
        name_groups = defaultdict(list)
        for e in self.engines:
            base = re.sub(r'[vV]\d+[\d.]*', '', e["name"]).strip('_')
            name_groups[base].append(e)

        for base, group in name_groups.items():
            if len(group) >= 2:
                # 同基础名多个版本
                versions = sorted(set(e["version"] for e in group))
                paths = [e["path"] for e in group]
                self.duplicates.append({
                    "base": base,
                    "count": len(group),
                    "versions": versions,
                    "paths": paths,
                    "type": "multi_version"
                })

        # 按大小+类名检测
        size_groups = defaultdict(list)
        for e in self.engines:
            if e["classes"]:
                key = (e["size_kb"], tuple(sorted(e["classes"][:3])))
                size_groups[key].append(e)
        for key, group in size_groups.items():
            if len(group) >= 2:
                paths = [e["path"] for e in group]
                self.duplicates.append({
                    "base": f"similar_{key[0]}KB",
                    "count": len(group),
                    "versions": [],
                    "paths": paths,
                    "type": "similar_content"
                })

    def _compute_stats(self, scanned: int, skipped: int):
        """计算统计"""
        cat_counts = Counter(e["category"] for e in self.engines)
        dir_counts = Counter(e["dir"] for e in self.engines)
        entry_counts = Counter(e["entry_type"] for e in self.engines)

        total_lines = sum(e["lines"] for e in self.engines)
        total_kb = sum(e["size_kb"] for e in self.engines)

        self.stats = {
            "scan_time": datetime.now().isoformat(),
            "total_scanned": scanned,
            "total_skipped": skipped,
            "total_registered": len(self.engines),
            "total_lines": total_lines,
            "total_size_mb": round(total_kb / 1024, 1),
            "by_category": dict(cat_counts.most_common()),
            "by_directory": dict(dir_counts),
            "by_entry_type": dict(entry_counts),
            "duplicate_groups": len([d for d in self.duplicates if d["type"] == "multi_version"]),
            "has_dna": sum(1 for e in self.engines if e["dna"]),
            "executable_count": sum(1 for e in self.engines if e["has_main"]),
            "api_count": sum(1 for e in self.engines if "api" in e["entry_type"]),
        }

    def _build_report(self) -> Dict:
        """构建完整报告"""
        return {
            "stats": self.stats,
            "engines": self.engines,
            "by_category": {k: [e["name"] for e in v] for k, v in self.by_category.items()},
            "duplicates": self.duplicates[:100],  # 截断
        }

    def save(self, path: Optional[Path] = None):
        """保存注册表到 JSON"""
        target = path or REGISTRY_PATH
        report = self._build_report()
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        return target

    def load(self, path: Optional[Path] = None):
        """加载已有注册表"""
        target = path or REGISTRY_PATH
        if not target.exists():
            return False
        data = json.loads(target.read_text(encoding='utf-8'))
        self.engines = data.get("engines", [])
        self.stats = data.get("stats", {})
        self._categorize()
        return True

    def find(self, keyword: str) -> List[Dict]:
        """关键词搜索 — 支持中文+分类+关键词映射"""
        kw = keyword.lower()
        # 中文关键词 → 英文搜索词扩展
        cn_map = {
            "视频": ["video", "media", "visual", "avatar", "3d", "image", "voice", "audio", "movie", "commentary"],
            "安全": ["audit", "security", "guard", "firewall", "shield", "defend", "sovereign", "fuse", "meltdown", "patrol"],
            "审计": ["audit", "governance", "verify", "validate"],
            "训练": ["train", "lora", "fine_tune", "mlx", "checkpoint", "dataset"],
            "记忆": ["memory", "vault", "store", "archive", "snapshot", "sync"],
            "知识": ["knowledge", "learn", "corpus", "notion", "article", "document", "paper"],
            "部署": ["deploy", "setup", "install", "config", "systemd", "launchd"],
            "人格": ["persona", "agent", "orchestrat", "character", "emotion", "intent"],
            "推演": ["sandbox", "predict", "simulate", "quantum", "wuxing", "bagua", "iching"],
            "数据": ["data", "analy", "metric", "monitor", "report", "stats"],
            "代码": ["cnsh", "compiler", "interpreter", "syntax", "parser", "align"],
            "搜索": ["search", "engine", "crawl", "browser"],
            "同步": ["sync", "bridge", "integrat", "migrate", "import", "export"],
        }
        search_terms = [kw]
        for cn, en_list in cn_map.items():
            if cn in kw or kw in cn:
                search_terms.extend(en_list)

        results = []
        seen = set()
        for e in self.engines:
            score = 0
            name_lower = e["name"].lower()
            cat_lower = e.get("category", "").lower()
            path_lower = e["path"].lower()
            for term in search_terms:
                if term == name_lower:
                    score += 100
                elif term in name_lower:
                    score += 50
                if term in cat_lower:
                    score += 15
                if term in path_lower:
                    score += 10
                if any(term in c.lower() for c in e.get("classes", [])):
                    score += 8
                if any(term in f.lower() for f in e.get("functions", [])):
                    score += 5
            if score > 0 and e["path"] not in seen:
                seen.add(e["path"])
                results.append((score, e))
        results.sort(key=lambda x: -x[0])
        return [r[1] for r in results[:30]]


# ─── CLI ───
def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·引擎统一注册表 v1.0")
    p.add_argument("action", nargs="?", default="scan",
                   choices=["scan", "stats", "find", "dupes", "export", "quick"])
    p.add_argument("keyword", nargs="?", help="搜索关键词 (find 模式)")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--output", "-o", help="输出文件路径")
    args = p.parse_args()

    reg = EngineRegistry()

    if args.action == "scan":
        if not args.json:
            print("🔍 全量扫描中...")
        report = reg.scan()
        reg.save(Path(args.output) if args.output else None)
        s = reg.stats
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"\n✅ 扫描完成")
            print(f"   总计: {s['total_registered']} 脚本注册")
            print(f"   代码行: {s['total_lines']:,} 行")
            print(f"   代码量: {s['total_size_mb']} MB")
            print(f"   可执行: {s['executable_count']} 个")
            print(f"   API服务: {s['api_count']} 个")
            print(f"   有DNA签名: {s['has_dna']} 个")
            print(f"   多版本冗余: {s['duplicate_groups']} 组")
            print(f"\n📊 分类分布:")
            for cat, cnt in s["by_category"].items():
                bar = "█" * min(cnt // 5, 40)
                print(f"   {cat}: {cnt} {bar}")
            print(f"\n   注册表已保存: {REGISTRY_PATH}")

    elif args.action == "stats":
        if not reg.load():
            print("❌ 注册表不存在，请先运行 scan")
            sys.exit(1)
        s = reg.stats
        if args.json:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            print(f"📊 引擎注册表统计")
            print(f"   注册脚本: {s['total_registered']}")
            print(f"   代码行数: {s['total_lines']:,}")
            print(f"   代码量: {s['total_size_mb']} MB")
            print(f"   可执行: {s['executable_count']}")
            print(f"   API服务: {s['api_count']}")
            print(f"   多版本组: {s['duplicate_groups']}")
            print(f"\n📂 目录分布:")
            for d, cnt in sorted(s["by_directory"].items()):
                print(f"   {d}/: {cnt}")
            print(f"\n🏷️ 分类分布:")
            for cat, cnt in s["by_category"].items():
                print(f"   {cat}: {cnt}")

    elif args.action == "find":
        if not args.keyword:
            print("❌ 请提供搜索关键词")
            sys.exit(1)
        if not reg.load():
            print("❌ 注册表不存在，请先运行 scan")
            sys.exit(1)
        results = reg.find(args.keyword)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"🔍 搜索 '{args.keyword}': {len(results)} 结果")
            for r in results:
                ver = f" [{r['version']}]" if r['version'] != 'unknown' else ""
                print(f"   📄 {r['name']}{ver}")
                print(f"      {r['path']} ({r['size_kb']}KB, {r['lines']}行)")
                print(f"      {r['category']} | {r['entry_type']}")
                if r['dna']:
                    print(f"      {r['dna'][:80]}")

    elif args.action == "dupes":
        if not reg.load():
            reg.scan()
            reg.save()
        dups = [d for d in reg.duplicates if d["type"] == "multi_version"]
        if args.json:
            print(json.dumps(dups, ensure_ascii=False, indent=2))
        else:
            print(f"🔍 多版本冗余: {len(dups)} 组")
            for d in dups[:30]:
                print(f"\n   {d['base']} ({d['count']} 版本)")
                for p in d["paths"][:5]:
                    print(f"      - {p}")

    elif args.action == "export":
        if not reg.load():
            reg.scan()
        output = Path(args.output) if args.output else REGISTRY_PATH
        reg.save(output)
        print(f"✅ 注册表已导出: {output}")

    elif args.action == "quick":
        # 快速模式：只扫描bin/目录
        global SCAN_DIRS
        SCAN_DIRS = [("bin", ROOT / "bin", True)]
        report = reg.scan()
        reg.save()
        print(f"✅ 快速扫描: {reg.stats['total_registered']} 脚本")


if __name__ == "__main__":
    main()
