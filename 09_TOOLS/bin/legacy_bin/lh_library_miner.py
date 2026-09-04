#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·乙未·未时·䷜坎-LIBRARY-MINER-V1.0-bf8e1a2d
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: ~/Library 应用数据勘探·挖掘·索引·链接·训练数据生成
"""
龍魂·Library 数据矿场引擎 v1.0
──────────────────────────────────
五阶段流水线:
  STAGE-1: 资产勘探 — 扫描 ~/Library 大小/类型/应用分布
  STAGE-2: 内容提取 — AI对话/代码/浏览/日志 文本提取
  STAGE-3: 清洗去重 — 格式统一·脱敏·去重·质量打分
  STAGE-4: 节点链接 — 与知识图谱节点建立关联边
  STAGE-5: 训练输出 — 导出JSONL训练数据

用法:
  python3 bin/lh_library_miner.py scan       # 资产勘探
  python3 bin/lh_library_miner.py extract    # 内容提取
  python3 bin/lh_library_miner.py link       # 图谱链接
  python3 bin/lh_library_miner.py all        # 全流水线
  python3 bin/lh_library_miner.py status     # 状态报告
"""

import os, sys, json, time, hashlib, re, glob, sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict

# ── 常量 ──
LIBRARY_ROOT = Path.home() / "Library"
APP_SUPPORT = LIBRARY_ROOT / "Application Support"
CONTAINERS = LIBRARY_ROOT / "Containers"
GROUP_CONTAINERS = LIBRARY_ROOT / "Group Containers"
CACHES = LIBRARY_ROOT / "Caches"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "library_mine"
GRAPH_PATH = Path(__file__).parent.parent / "03_知識圖譜" / "graph_data.json"

# 关键 AI 应用
AI_APPS = {
    "Claude": APP_SUPPORT / "Claude",
    "CodeBuddy CN": APP_SUPPORT / "CodeBuddy CN",
    "CodeBuddyExtension": APP_SUPPORT / "CodeBuddyExtension",
    "Cursor": APP_SUPPORT / "Cursor",
    "Code": APP_SUPPORT / "Code",
}

# 关键浏览器
BROWSER_APPS = {
    "Chrome": APP_SUPPORT / "Google" / "Chrome",
    "Arc": APP_SUPPORT / "Arc",
    "Brave": APP_SUPPORT / "BraveSoftware",
}

# 可挖掘的文件类型
MINE_EXTENSIONS = {
    '.md', '.txt', '.json', '.jsonl', '.log', '.csv', '.xml', '.yaml', '.yml',
    '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.sql',
    '.toml', '.ini', '.cfg', '.conf',
}


@dataclass
class AppAsset:
    """应用数据资产"""
    name: str
    path: str
    size_bytes: int = 0
    size_mb: float = 0.0
    file_count: int = 0
    mineable_count: int = 0
    mineable_size_mb: float = 0.0
    data_types: Dict[str, int] = field(default_factory=dict)
    status: str = "🟡 未勘探"  # 🟢已提取 🟡待勘探 🔴无数据
    last_scan: str = ""


@dataclass
class MineRecord:
    """挖掘记录"""
    source: str
    file_path: str
    content_preview: str
    word_count: int
    quality_score: float  # 0-1
    extracted_at: str
    dna: str
    linked_nodes: List[str] = field(default_factory=list)


@dataclass
class LibraryReport:
    """完整勘探报告"""
    generated_at: str
    total_size_gb: float
    total_files: int
    total_mineable: int
    total_mineable_gb: float
    apps: List[AppAsset] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class LibraryMiner:
    """Library 数据矿场引擎"""

    def __init__(self):
        self.report = LibraryReport(
            generated_at=datetime.now().isoformat(),
            total_size_gb=0.0,
            total_files=0,
            total_mineable=0,
            total_mineable_gb=0.0,
        )
        self.mine_records: List[MineRecord] = []
        self.graph_nodes: Dict[str, Any] = {}
        self.graph_edges: List[Any] = []
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ═══════════ STAGE-1: 资产勘探 ═══════════
    def scan(self) -> LibraryReport:
        """勘探 ~/Library 下所有应用数据资产"""
        print("🔍 STAGE-1: 资产勘探...")

        # 1.1 扫描 AI 应用
        for name, path in AI_APPS.items():
            asset = self._scan_app(name, str(path))
            self.report.apps.append(asset)

        # 1.2 扫描浏览器
        for name, path in BROWSER_APPS.items():
            asset = self._scan_app(name, str(path))
            self.report.apps.append(asset)

        # 1.3 扫描其他大目录
        other_dirs = [APP_SUPPORT, CACHES]
        for d in other_dirs:
            if d.exists():
                size = self._dir_size(d)
                if size > 100 * 1024 * 1024:  # >100MB
                    # 找出子应用
                    for sub in sorted(d.iterdir()):
                        if sub.is_dir():
                            sub_size = self._dir_size(sub)
                            if sub_size > 50 * 1024 * 1024:
                                existing = any(a.path == str(sub) for a in self.report.apps)
                                if not existing:
                                    asset = self._scan_app(sub.name, str(sub))
                                    self.report.apps.append(asset)

        # 1.4 汇总
        total = sum(a.size_bytes for a in self.report.apps)
        mineable = sum(a.mineable_count for a in self.report.apps)
        mineable_gb = sum(a.mineable_size_mb for a in self.report.apps) / 1024

        self.report.total_size_gb = round(total / (1024**3), 2)
        self.report.total_files = sum(a.file_count for a in self.report.apps)
        self.report.total_mineable = mineable
        self.report.total_mineable_gb = round(mineable_gb, 2)

        top5 = sorted(self.report.apps, key=lambda a: a.mineable_size_mb, reverse=True)[:5]
        self.report.summary = {
            "ai_apps": {a.name: f"{a.size_mb:.0f}MB/{a.mineable_count}文件" for a in self.report.apps if a.name in AI_APPS},
            "browsers": {a.name: f"{a.size_mb:.0f}MB" for a in self.report.apps if a.name in BROWSER_APPS},
            "other_large": {a.name: f"{a.size_mb:.0f}MB" for a in self.report.apps if a.name not in AI_APPS and a.name not in BROWSER_APPS},
            "top_mineable": [asdict(a) for a in top5],
        }

        # 保存报告
        self._save_report()
        return self.report

    def _scan_app(self, name: str, path_str: str) -> AppAsset:
        """扫描单个应用目录"""
        path = Path(path_str)
        if not path.exists():
            return AppAsset(name=name, path=path_str, status="🔴 无数据")

        total_size = self._dir_size(path)
        size_mb = round(total_size / (1024**2), 1)

        # 统计可挖掘文件
        file_count = 0
        mineable_count = 0
        mineable_size = 0
        data_types: Dict[str, int] = defaultdict(int)

        try:
            for root, dirs, files in os.walk(path):
                # 跳过 node_modules/.git/__pycache__
                dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__', '.venv', 'venv')]
                file_count += len(files)
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in MINE_EXTENSIONS:
                        fp = os.path.join(root, f)
                        try:
                            fs = os.path.getsize(fp)
                            mineable_count += 1
                            mineable_size += fs
                            data_types[ext] = data_types.get(ext, 0) + 1
                        except OSError:
                            pass
        except PermissionError:
            pass

        return AppAsset(
            name=name,
            path=path_str,
            size_bytes=total_size,
            size_mb=size_mb,
            file_count=file_count,
            mineable_count=mineable_count,
            mineable_size_mb=round(mineable_size / (1024**2), 1),
            data_types=dict(data_types),
            status="🟢 已勘探",
            last_scan=datetime.now().isoformat(),
        )

    def _dir_size(self, path: Path, max_depth: int = 3) -> int:
        """快速估算目录大小"""
        total = 0
        try:
            for item in path.iterdir():
                if item.is_file():
                    try:
                        total += item.stat().st_size
                    except OSError:
                        pass
                elif item.is_dir() and max_depth > 0 and not item.name.startswith('.'):
                    total += self._dir_size(item, max_depth - 1)
        except PermissionError:
            pass
        return total

    def _save_report(self):
        """保存勘探报告"""
        report_path = OUTPUT_DIR / "scan_report.json"
        # 简化 apps 字段用于 JSON
        report_dict = {
            "generated_at": self.report.generated_at,
            "total_size_gb": self.report.total_size_gb,
            "total_files": self.report.total_files,
            "total_mineable": self.report.total_mineable,
            "total_mineable_gb": self.report.total_mineable_gb,
            "apps": [asdict(a) for a in self.report.apps],
            "summary": self.report.summary,
        }
        with open(report_path, 'w') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        print(f"  📄 勘探报告: {report_path}")

    # ═══════════ STAGE-2: 内容提取 ═══════════
    def extract(self, limit_per_app: int = 100, max_size_kb: int = 50) -> int:
        """从已勘探的应用提取文本内容"""
        print("📤 STAGE-2: 内容提取...")
        self.mine_records = []

        # 如果 report.apps 为空，加载上次 scan 的结果
        if not self.report.apps:
            report_path = OUTPUT_DIR / "scan_report.json"
            if report_path.exists():
                with open(report_path) as f:
                    data = json.load(f)
                for a in data.get('apps', []):
                    asset = AppAsset(**a)
                    self.report.apps.append(asset)
                self.report.total_size_gb = data.get('total_size_gb', 0)
                self.report.total_files = data.get('total_files', 0)
                self.report.total_mineable = data.get('total_mineable', 0)

        for asset in self.report.apps:
            if asset.mineable_count == 0:
                continue

            extracted = 0
            path = Path(asset.path)
            if not path.exists():
                continue

            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__', '.venv')]

                for f in files:
                    if extracted >= limit_per_app:
                        break
                    ext = os.path.splitext(f)[1].lower()
                    if ext not in MINE_EXTENSIONS:
                        continue

                    fp = os.path.join(root, f)
                    try:
                        fs = os.path.getsize(fp)
                        if fs > max_size_kb * 1024 or fs == 0:
                            continue

                        # 读文本
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                            content = fh.read()

                        if len(content) < 30:  # 跳过太短的
                            continue

                        # 质量评分
                        quality = self._quality_score(content)

                        # DNA
                        dna = self._make_dna(asset.name, f, content)

                        record = MineRecord(
                            source=asset.name,
                            file_path=fp,
                            content_preview=content[:200],
                            word_count=len(content.split()),
                            quality_score=quality,
                            extracted_at=datetime.now().isoformat(),
                            dna=dna,
                        )
                        self.mine_records.append(record)
                        extracted += 1

                    except (OSError, UnicodeDecodeError) as e:
                        continue

                if extracted >= limit_per_app:
                    break

            asset.status = f"🟢 已提取({extracted}条)"
            print(f"  📦 {asset.name}: 提取 {extracted} 条")

        # 保存
        self._save_extracts()
        return len(self.mine_records)

    def _quality_score(self, content: str) -> float:
        """简单质量评分: 中文比例·句子长度·特殊字符比例"""
        score = 0.5
        # 中文含量高加分
        cn_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
        if len(content) > 0:
            cn_ratio = cn_chars / len(content)
            score += cn_ratio * 0.3
        # 平均句子长度适中
        sentences = [s for s in re.split(r'[。！？\n]', content) if s.strip()]
        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)
            if 10 < avg_len < 200:
                score += 0.2
        # 代码/日志占比较高扣分
        code_lines = sum(1 for line in content.split('\n') if line.strip().startswith(('#', '//', 'import', 'def ', 'class ')))
        if len(content.split('\n')) > 0:
            code_ratio = code_lines / len(content.split('\n'))
            if code_ratio > 0.5:
                score -= 0.2
        return round(max(0.0, min(1.0, score)), 2)

    def _make_dna(self, app: str, filename: str, content: str) -> str:
        """生成挖掘记录DNA"""
        h = hashlib.sha256(f"{app}:{filename}:{content[:100]}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-LIBRARY-MINE-{app[:4].upper()}-{h}"

    def _save_extracts(self):
        """保存提取结果"""
        path = OUTPUT_DIR / "extracts.jsonl"
        with open(path, 'w') as f:
            for r in self.mine_records:
                f.write(json.dumps(asdict(r), ensure_ascii=False) + '\n')
        print(f"  📄 提取结果: {path} ({len(self.mine_records)}条)")

    # ═══════════ STAGE-3: 清洗去重 ═══════════
    def clean(self, min_quality: float = 0.3) -> int:
        """清洗: 去重·低质量过滤·脱敏"""
        print("🧹 STAGE-3: 清洗去重...")

        seen_hashes = set()
        cleaned = []

        for r in self.mine_records:
            if r.quality_score < min_quality:
                continue

            # 去重 (内容哈希)
            h = hashlib.md5(r.content_preview.encode()).hexdigest()
            if h in seen_hashes:
                continue
            seen_hashes.add(h)

            # 隐私脱敏
            r.content_preview = self._sanitize(r.content_preview)
            cleaned.append(r)

        self.mine_records = cleaned

        path = OUTPUT_DIR / "cleaned.jsonl"
        with open(path, 'w') as f:
            for r in cleaned:
                f.write(json.dumps(asdict(r), ensure_ascii=False) + '\n')

        print(f"  🟢 清洗后: {len(cleaned)} 条 (原{len(seen_hashes)}去重)")
        return len(cleaned)

    _PHONE_RE = re.compile(r'1[3-9]\d{9}')
    _ID_RE = re.compile(r'\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]')
    _EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    def _sanitize(self, text: str) -> str:
        """脱敏处理"""
        text = self._PHONE_RE.sub('138****0000', text)
        text = self._ID_RE.sub('1101011990****1234', text)
        text = self._EMAIL_RE.sub('***@email.com', text)
        return text

    # ═══════════ STAGE-4: 图谱节点链接 ═══════════
    def link_to_graph(self):
        """将挖掘数据链接到知识图谱节点"""
        print("🔗 STAGE-4: 节点链接...")

        # 加载图谱
        self._load_graph()

        new_edges = 0
        for r in self.mine_records:
            # 关键词匹配
            content = r.content_preview + r.file_path
            matched = self._match_nodes(content)
            r.linked_nodes = matched
            new_edges += len(matched)

        # 保存增强数据
        path = OUTPUT_DIR / "linked.jsonl"
        with open(path, 'w') as f:
            for r in self.mine_records:
                f.write(json.dumps(asdict(r), ensure_ascii=False) + '\n')

        # 保存链接报告
        link_report = {
            "total_records": len(self.mine_records),
            "total_new_edges": new_edges,
            "avg_links_per_record": round(new_edges / max(1, len(self.mine_records)), 1),
            "top_linked_nodes": self._top_linked_nodes(),
        }
        with open(OUTPUT_DIR / "link_report.json", 'w') as f:
            json.dump(link_report, f, ensure_ascii=False, indent=2)

        print(f"  🟢 新增 {new_edges} 条边 · 均 {link_report['avg_links_per_record']} 链接/记录")
        return link_report

    def _load_graph(self):
        """加载知识图谱"""
        if GRAPH_PATH.exists():
            with open(GRAPH_PATH) as f:
                data = json.load(f)
                self.graph_nodes = data.get('nodes', {})
                self.graph_edges = data.get('edges', data.get('links', []))

    def _match_nodes(self, content: str) -> List[str]:
        """关键词匹配图谱节点"""
        matched = []
        keywords_map = {
            '/kimi-webbridge': ['kimi', 'webbridge', '浏览器', '浏览器自动化'],
            '/code-audit': ['审计', '安全', '代码审查', 'code audit'],
            '/dna-gen': ['dna', '追溯', '签名', 'dna生成'],
            'l0-core': ['核心', '引擎', 'core', 'L0'],
            'l1-storage': ['存储', '数据库', 'storage', 'sqlite'],
            '/api-check': ['api', '接口', '检查', '健康'],
        }
        for node_id, keywords in keywords_map.items():
            if any(kw.lower() in content.lower() for kw in keywords):
                matched.append(node_id)
        return matched[:5]  # 最多5个链接

    def _top_linked_nodes(self) -> List[Dict]:
        """被链接最多的节点"""
        count = defaultdict(int)
        for r in self.mine_records:
            for n in r.linked_nodes:
                count[n] += 1
        return sorted([{"node": k, "count": v} for k, v in count.items()], key=lambda x: -x['count'])[:10]

    # ═══════════ STAGE-5: 训练数据导出 ═══════════
    def export_training_data(self) -> int:
        """导出JSONL训练数据"""
        print("🎓 STAGE-5: 训练数据导出...")

        train_path = OUTPUT_DIR / "library_train.jsonl"
        count = 0

        with open(train_path, 'w') as f:
            for r in self.mine_records:
                if r.quality_score < 0.4:
                    continue
                # 构造训练格式
                item = {
                    "messages": [
                        {"role": "system", "content": f"你是龍魂系统的数据矿工。来源: {r.source}。DNA: {r.dna}"},
                        {"role": "user", "content": f"分析以下来自{r.source}的文件内容:\n{r.content_preview[:500]}"},
                        {"role": "assistant", "content": f"该文件来自{r.source}应用数据，关联节点: {', '.join(r.linked_nodes)}。内容概要: {r.content_preview[:100]}... 质量评分: {r.quality_score}"},
                    ],
                    "metadata": {
                        "source": r.source,
                        "file": r.file_path,
                        "quality": r.quality_score,
                        "dna": r.dna,
                        "linked_nodes": r.linked_nodes,
                        "domain": "library_mine",
                    }
                }
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                count += 1

        print(f"  🟢 训练数据: {train_path} ({count}条)")
        return count

    # ═══════════ 全流水线 ═══════════
    def run_all(self):
        """执行全流水线"""
        print("=" * 60)
        print("  龍魂·Library 数据矿场引擎 v1.0")
        print("  全流水线: 勘探→提取→清洗→链接→导出")
        print("=" * 60)

        t0 = time.time()
        self.scan()
        self.extract()
        self.clean()
        link_report = self.link_to_graph()
        train_count = self.export_training_data()

        elapsed = time.time() - t0
        print(f"\n🟢 全流水线完成 ({elapsed:.1f}s)")
        print(f"  勘探: {self.report.total_size_gb}GB / {self.report.total_mineable}个可挖掘文件")
        print(f"  提取: {len(self.mine_records)}条记录")
        print(f"  链接: {link_report['total_new_edges']}条新图谱边")
        print(f"  训练: {train_count}条训练数据")

    def status_report(self) -> Dict[str, Any]:
        """状态报告"""
        report = {
            "engine": "Library Miner v1.0",
            "dna": "#龍芯⚡️丙午·乙未·乙未·未时·䷜坎-LIBRARY-MINER-V1.0-bf8e1a2d",
            "output_dir": str(OUTPUT_DIR),
        }

        # 检查各阶段产物
        stages = {
            "scan_report.json": "STAGE-1 勘探",
            "extracts.jsonl": "STAGE-2 提取",
            "cleaned.jsonl": "STAGE-3 清洗",
            "linked.jsonl": "STAGE-4 链接",
            "library_train.jsonl": "STAGE-5 训练数据",
        }
        for fname, stage in stages.items():
            fp = OUTPUT_DIR / fname
            if fp.exists():
                lines = sum(1 for _ in open(fp))
                size = fp.stat().st_size
                report[stage] = f"✅ {lines}条 ({size/1024:.0f}KB)"
            else:
                report[stage] = "⏳ 未执行"

        # 勘探报告
        report_fp = OUTPUT_DIR / "scan_report.json"
        if report_fp.exists():
            with open(report_fp) as f:
                scan = json.load(f)
                report["资产总览"] = f"{scan['total_size_gb']}GB / {scan['total_mineable']}个可挖掘文件"
                report["应用数量"] = len(scan.get('apps', []))

        return report


# ═══════════ CLI ═══════════
if __name__ == "__main__":
    miner = LibraryMiner()

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "scan":
        report = miner.scan()
        print(f"\n🟢 勘探完成: {report.total_size_gb}GB / {report.total_mineable}可挖掘")

    elif cmd == "extract":
        count = miner.extract()
        print(f"\n🟢 提取完成: {count}条")

    elif cmd == "clean":
        count = miner.clean()
        print(f"\n🟢 清洗完成: {count}条")

    elif cmd == "link":
        report = miner.link_to_graph()
        print(f"\n🟢 链接完成: {report['total_new_edges']}条边")

    elif cmd == "train":
        count = miner.export_training_data()
        print(f"\n🟢 训练数据: {count}条")

    elif cmd == "all":
        miner.run_all()

    elif cmd == "status":
        report = miner.status_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))

    else:
        print(__doc__)
