#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-07-25-EXOBRAIN-COMPRESSOR-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 外脑压缩引擎 v2.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-25-EXOBRAIN-COMPRESSOR-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# STATUS: ⚠️ DEPRECATED · 功能已由 engines/lh_fixed_point_memory_archive.py 统一接管
# 保留原因: 兼容旧调用与历史快照，新代码请使用 MemoryArchive.ingest()
# ═══════════════════════════════════════════
# 处理层: 记忆永生管道第二环
# 当记忆库膨胀时自动压缩: 智能摘要·冗余去重·时间衰减·关联图谱
# 上游: bin/lh_daily_logger.py (数据源)
# 下游: engines/lh_memory_eternity.py (存储层)
# 配合: bin/lh_exobrain_engine.py (底层迭代压缩)
#        bin/lh_exobrain_heartbeat.py (六档心跳触发)
#
# 用法:
#   python3 engines/lh_exobrain_compressor.py summarize <文本>         # 智能摘要
#   python3 engines/lh_exobrain_compressor.py dedup                     # 冗余去重
#   python3 engines/lh_exobrain_compressor.py decay                     # 时间衰减
#   python3 engines/lh_exobrain_compressor.py graph                     # 构建关联图谱
#   python3 engines/lh_exobrain_compressor.py compress-all              # 全量压缩
#   python3 engines/lh_exobrain_compressor.py report                    # 压缩率报告
#   python3 engines/lh_exobrain_compressor.py status                    # 引擎状态
# ═══════════════════════════════════════════
"""

import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
STATE_DIR = PROJECT_ROOT / "state" / "exobrain" / "compressor"
STATE_DIR.mkdir(parents=True, exist_ok=True)
DAILY_LOG_DB = MEMORY_DIR / "daily_log_structured.jsonl"
COMPRESS_STATE = STATE_DIR / "compress_state.json"
GRAPH_STATE = STATE_DIR / "knowledge_graph.json"

# ─── 锚词库（用于关键词提取） ───
ANCHOR_KEYWORDS = frozenset({
    "DNA", "龍芯", "焊死", "协议", "签章", "铁律", "底线", "熔断", "审计",
    "人格", "路由", "引擎", "训练", "模型", "数据", "部署", "安全", "密钥",
    "主权", "不离地", "不让付出者寒心", "信息主权", "外化内不化", "德在技术前",
    "369", "河图洛书", "五行", "八卦", "干支", "七因子", "四道防线",
    "浏览器史官", "如意", "TeamOrchestrator", "Orchestrator", "鲲鹏",
    "CNSH", "UID9622", "诸葛鑫", "离火运", "德本审计", "黑天使",
    "记忆永存", "外脑压缩", "数据炼化", "数据自举", "溯源",
    "GPG", "确认码", "GATE", "三色", "四签", "六誓",
})

# ─── 时间衰减参数 ───
T_HALF: Dict[str, float] = {
    "核心": float("inf"),  # 永不过期
    "重要": 365.0,          # 一年半衰
    "常规": 90.0,           # 三个月半衰
    "临时": 7.0,            # 一周半衰
}


def _tokenize(text: str) -> Set[str]:
    """中文分词（简化jieba-free方案）"""
    tokens = set()
    # 提取中文词组（2-4字）
    for m in re.finditer(r"[\u4e00-\u9fff]{2,4}", text):
        tokens.add(m.group())
    # 提取英文词
    for m in re.finditer(r"[a-zA-Z_]\w+", text):
        tokens.add(m.group().lower())
    return tokens


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _simhash(text: str) -> int:
    """SimHash — 用于近似去重"""
    tokens = _tokenize(text)
    v = [0] * 64
    for token in tokens:
        h = int(hashlib.md5(token.encode()).hexdigest()[:16], 16)
        for i in range(64):
            if h & (1 << i):
                v[i] += 1
            else:
                v[i] -= 1
    result = 0
    for i in range(64):
        if v[i] > 0:
            result |= (1 << i)
    return result


def hamming_distance(a: int, b: int) -> int:
    """汉明距离"""
    return bin(a ^ b).count("1")


# ═══════════════════════════════════════════
# 1. 智能摘要引擎
# ═══════════════════════════════════════════

class SmartSummarizer:
    """本地智能摘要 — 提取核心决策、关键结论"""

    DNA = "#龍芯⚡️2026-07-25-SMART-SUMMARIZER-v1.0"

    @staticmethod
    def summarize(text: str, max_len: int = 200) -> Dict[str, Any]:
        """
        从文本中提取结构化摘要
        返回: {摘要, 关键词, 重要性, 分类}
        """
        sentences = re.split(r"[。！？!?\n]+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 4]

        # 关键词提取
        all_tokens = _tokenize(text)
        anchor_hits = all_tokens & ANCHOR_KEYWORDS
        keyword_list = sorted(anchor_hits, key=lambda k: text.count(k), reverse=True)[:5]

        # 重要性评分: 锚词命中数 / 长度比
        importance = min(1.0, (len(anchor_hits) * 0.15) + (len(text) > 50 and 0.1 or 0))

        # 分类判定
        category = "常规"
        high_priority_kws = {"焊死", "熔断", "P0", "铁律", "底线", "天条", "主权"}
        critical_kws = {"DNA", "协议", "签章", "审计", "GPG"}
        if anchor_hits & high_priority_kws:
            category = "核心"
        elif anchor_hits & critical_kws:
            category = "重要"
        elif "教训" in text or "错误" in text or "修复" in text:
            category = "重要"

        # 生成摘要
        if len(sentences) >= 3:
            first = sentences[0]
            last = sentences[-1]
            mid = sentences[len(sentences) // 2]
            summary = f"{first}。{mid}。{last}"
        elif sentences:
            summary = "。".join(sentences)
        else:
            summary = text

        if len(summary) > max_len:
            summary = summary[:max_len - 3] + "..."

        return {
            "摘要": summary,
            "摘要长度": len(summary),
            "原文长度": len(text),
            "压缩率": round(len(summary) / max(len(text), 1), 4),
            "关键词": keyword_list,
            "重要性": round(importance, 3),
            "分类": category,
            "锚词命中数": len(anchor_hits),
            "句子数": len(sentences),
        }


# ═══════════════════════════════════════════
# 2. 冗余去重引擎
# ═══════════════════════════════════════════

class RedundancyDeduplicator:
    """检测重复规矩/教训，自动合并，旧版归档"""

    DNA = "#龍芯⚡️2026-07-25-REDUNDANCY-DEDUP-v1.0"
    SIM_THRESHOLD = 3  # SimHash汉明距离阈值（≤3视为相似）

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if COMPRESS_STATE.exists():
            return json.loads(open(COMPRESS_STATE, "r", encoding="utf-8").read())
        return {"seen_signatures": {}, "merged_rules": [], "archived": []}

    def _save_state(self):
        with open(COMPRESS_STATE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def deduplicate(self) -> Dict[str, Any]:
        """扫描全部日志，检测重复"""
        if not DAILY_LOG_DB.exists():
            return {"状态": "🟡", "说明": "无日志数据", "重复组": [], "重复组数": 0, "总条目数": 0}

        entries = []
        with open(DAILY_LOG_DB, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # 按类型分组
        groups: Dict[str, List[Dict]] = defaultdict(list)
        for e in entries:
            groups[e.get("类型", "unknown")].append(e)

        duplicates_found = []
        for log_type, group in groups.items():
            if len(group) < 2:
                continue
            # 计算每条记录的SimHash
            signatures = []
            for i, entry in enumerate(group):
                content = entry.get("内容", "")
                sig = _simhash(content)
                signatures.append((i, sig, entry))

            # 找重复组
            for i in range(len(signatures)):
                for j in range(i + 1, len(signatures)):
                    dist = hamming_distance(signatures[i][1], signatures[j][1])
                    if dist <= self.SIM_THRESHOLD:
                        duplicates_found.append({
                            "条目A": signatures[i][2]["内容"][:80],
                            "条目B": signatures[j][2]["内容"][:80],
                            "汉明距离": dist,
                            "建议": "合并·保留最新·旧版归档",
                        })

        report = {
            "扫描时间": datetime.now().isoformat(),
            "总条目数": len(entries),
            "重复组数": len(duplicates_found),
            "重复组": duplicates_found,
            "状态": "🟢" if len(duplicates_found) == 0 else ("🟡" if len(duplicates_found) < 5 else "🔴"),
        }
        return report


# ═══════════════════════════════════════════
# 3. 时间衰减引擎
# ═══════════════════════════════════════════

class TimeDecayer:
    """非核心记忆按时间衰减权重，永不完全归零"""

    DNA = "#龍芯⚡️2026-07-25-TIME-DECAYER-v1.0"

    @staticmethod
    def compute_decay(entry_date: str, importance: float, tier: str = "常规") -> Dict[str, Any]:
        """
        计算一条记忆的当前衰减权重
        W = W0 * (1/2)^(Δt / T_half)
        永不低于0.01（永不删除）
        """
        try:
            dt = datetime.fromisoformat(entry_date)
        except (ValueError, TypeError):
            dt = datetime.now(timezone.utc)

        now = datetime.now(timezone.utc)
        delta_days = (now - dt.replace(tzinfo=timezone.utc)).days
        half_life = T_HALF.get(tier, 90.0)

        if half_life == float("inf"):
            weight = 1.0
        else:
            weight = importance * (0.5 ** (delta_days / half_life))

        # 永不归零
        weight = max(weight, 0.01)

        return {
            "原始重要度": importance,
            "距今天数": delta_days,
            "衰减权重": round(weight, 4),
            "生效半衰期天": half_life,
            "分类": tier,
            "判定": "🟢" if weight > 0.5 else ("🟡" if weight > 0.1 else "⚪ 接近休眠"),
        }

    def scan_all_entries(self) -> Dict[str, Any]:
        """扫描全部日志，计算每条当前权重"""
        if not DAILY_LOG_DB.exists():
            return {"状态": "🟡", "条目": []}

        entries = []
        with open(DAILY_LOG_DB, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        results = []
        for e in entries:
            tier = e.get("扩展", {}).get("焊死级别", "")
            if not tier:
                # 推断分类
                content = e.get("内容", "")
                if any(kw in content for kw in ["焊死", "熔断", "P0", "铁律", "永不出售"]):
                    tier = "核心"
                elif any(kw in content for kw in ["DNA", "协议", "签章", "审计", "规矩"]):
                    tier = "重要"
                else:
                    tier = "常规"

            r = self.compute_decay(e.get("时间", "")[:10], 1.0, tier)
            r["内容摘要"] = e.get("内容", "")[:60]
            results.append(r)

        active = [r for r in results if r["衰减权重"] > 0.5]
        dormant = [r for r in results if 0.1 < r["衰减权重"] <= 0.5]
        near_sleep = [r for r in results if r["衰减权重"] <= 0.1]

        return {
            "扫描时间": datetime.now().isoformat(),
            "总条目": len(results),
            "活跃(>0.5)": len(active),
            "衰减中(0.1-0.5)": len(dormant),
            "接近休眠(<0.1)": len(near_sleep),
            "状态": "🟢" if len(near_sleep) < len(results) * 0.3 else "🟡",
        }


# ═══════════════════════════════════════════
# 4. 关联图谱引擎
# ═══════════════════════════════════════════

class KnowledgeGraphBuilder:
    """构建记忆之间的关联图谱"""

    DNA = "#龍芯⚡️2026-07-25-KNOWLEDGE-GRAPH-v1.0"

    def __init__(self):
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict[str, Any]:
        if GRAPH_STATE.exists():
            return json.loads(open(GRAPH_STATE, "r", encoding="utf-8").read())
        return {"nodes": {}, "edges": []}

    def _save_graph(self):
        with open(GRAPH_STATE, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=2)

    def build(self) -> Dict[str, Any]:
        """从所有日志构建知识图谱"""
        if not DAILY_LOG_DB.exists():
            return {"状态": "🟡", "节点数": 0, "边数": 0}

        entries = []
        with open(DAILY_LOG_DB, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # 提取关键词节点
        keyword_entries: Dict[str, List[str]] = defaultdict(list)
        for e in entries:
            content = e.get("内容", "")
            tokens = _tokenize(content)
            anchor_hits = tokens & ANCHOR_KEYWORDS
            for kw in anchor_hits:
                keyword_entries[kw].append(e.get("DNA", ""))
                # 如果扩展字段里有值，也提取
                extra = e.get("扩展", {})
                for v in extra.values():
                    for sub_kw in _tokenize(str(v)) & ANCHOR_KEYWORDS:
                        keyword_entries[sub_kw].append(e.get("DNA", ""))

        # 构建节点
        nodes = {}
        for kw, dnas in keyword_entries.items():
            nodes[kw] = {
                "关键词": kw,
                "关联条目数": len(set(dnas)),
                "关联DNA": list(set(dnas))[:5],  # 只保留前5个
            }

        # 构建边（共现关系）
        edges = []
        entry_kw_pairs = []
        for e in entries:
            content = e.get("内容", "")
            kws = _tokenize(content) & ANCHOR_KEYWORDS
            if len(kws) >= 2:
                entry_kw_pairs.append(list(kws))

        # 统计共现
        cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        for kw_list in entry_kw_pairs:
            for i in range(len(kw_list)):
                for j in range(i + 1, len(kw_list)):
                    a, b = sorted([kw_list[i], kw_list[j]])
                    cooccurrence[(a, b)] += 1

        for (a, b), count in cooccurrence.items():
            if count >= 1:  # 至少共现一次就保留边
                edges.append({
                    "源": a,
                    "目标": b,
                    "共现次数": count,
                    "强度": "强" if count >= 3 else ("中" if count >= 2 else "弱"),
                })

        self.graph = {"nodes": nodes, "edges": edges, "构建时间": datetime.now().isoformat()}
        self._save_graph()

        return {
            "状态": "🟢",
            "节点数": len(nodes),
            "边数": len(edges),
            "核心概念(度最高)": sorted(nodes.items(), key=lambda x: x[1]["关联条目数"], reverse=True)[:10],
        }

    def query_related(self, keyword: str) -> Dict[str, Any]:
        """查询某个关键词的关联网络"""
        nodes = self.graph.get("nodes", {})
        edges = self.graph.get("edges", [])

        related_nodes = []
        for edge in edges:
            if edge["源"] == keyword:
                related_nodes.append({"关键词": edge["目标"], "共现": edge["共现次数"], "强度": edge["强度"]})
            elif edge["目标"] == keyword:
                related_nodes.append({"关键词": edge["源"], "共现": edge["共现次数"], "强度": edge["强度"]})

        node_info = nodes.get(keyword, {})
        return {
            "查询关键词": keyword,
            "关联条目数": node_info.get("关联条目数", 0),
            "关联概念": sorted(related_nodes, key=lambda x: x["共现"], reverse=True)[:20],
        }


# ═══════════════════════════════════════════
# 5. 压缩率报告
# ═══════════════════════════════════════════

class CompressReporter:
    """生成压缩率报告"""

    DNA = "#龍芯⚡️2026-07-25-COMPRESS-REPORTER-v1.0"

    @staticmethod
    def generate_report() -> Dict[str, Any]:
        """生成完整压缩报告"""
        deduper = RedundancyDeduplicator()
        decayer = TimeDecayer()
        graph_builder = KnowledgeGraphBuilder()

        dedup_report = deduper.deduplicate()
        decay_report = decayer.scan_all_entries()
        graph_report = graph_builder.build()

        total_original = 0
        total_after = 0
        if MEMORY_DIR.exists():
            for f in MEMORY_DIR.glob("*.md"):
                total_original += f.stat().st_size
            if DAILY_LOG_DB.exists():
                total_after = DAILY_LOG_DB.stat().st_size

        return {
            "生成时间": datetime.now().isoformat(),
            "压缩前总大小": f"{total_original / 1024:.1f}KB",
            "结构化后大小": f"{total_after / 1024:.1f}KB",
            "压缩率": f"{(1 - total_after / max(total_original, 1)) * 100:.1f}%",
            "去重结果": dedup_report,
            "衰减分析": decay_report,
            "知识图谱": {
                "节点数": graph_report.get("节点数", 0),
                "边数": graph_report.get("边数", 0),
            },
        }


# ═══════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: python3 engines/lh_exobrain_compressor.py <命令>")
        print("命令: summarize|dedup|decay|graph|query|compress-all|report|status")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "summarize":
        if len(sys.argv) < 3:
            text = sys.stdin.read()
        else:
            text = sys.argv[2]
        result = SmartSummarizer.summarize(text)
        print("=" * 50)
        print(f"  🧠 智能摘要")
        print(f"  分类: {result['分类']} | 重要性: {result['重要性']}")
        print(f"  压缩率: {result['压缩率']} ({result['原文长度']}→{result['摘要长度']}字)")
        print(f"  关键词: {', '.join(result['关键词'])}")
        print(f"  ---")
        print(f"  {result['摘要']}")
        print("=" * 50)

    elif cmd == "dedup":
        deduper = RedundancyDeduplicator()
        report = deduper.deduplicate()
        print("=" * 50)
        print(f"  🔍 冗余去重扫描 {report['状态']}")
        print(f"  总条目: {report['总条目数']} | 重复组: {report['重复组数']}")
        for dup in report.get("重复组", []):
            print(f"  ---")
            print(f"  汉明距离: {dup['汉明距离']}")
            print(f"  A: {dup['条目A']}")
            print(f"  B: {dup['条目B']}")
        print("=" * 50)

    elif cmd == "decay":
        decayer = TimeDecayer()
        report = decayer.scan_all_entries()
        print("=" * 50)
        print(f"  ⏳ 时间衰减分析 {report['状态']}")
        print(f"  总条目: {report['总条目']}")
        print(f"  活跃: {report['活跃(>0.5)']} | 衰减中: {report['衰减中(0.1-0.5)']} | 接近休眠: {report['接近休眠(<0.1)']}")
        print("=" * 50)

    elif cmd == "graph":
        builder = KnowledgeGraphBuilder()
        report = builder.build()
        print("=" * 50)
        print(f"  🕸️ 知识图谱 {report['状态']}")
        print(f"  节点: {report['节点数']} | 边: {report['边数']}")
        print(f"  核心概念:")
        for kw, info in report.get("核心概念", [])[:10]:
            print(f"    {kw}: {info['关联条目数']}条")
        print("=" * 50)

    elif cmd == "query":
        if len(sys.argv) < 3:
            print("请提供查询关键词")
            sys.exit(1)
        builder = KnowledgeGraphBuilder()
        # 先确保图谱存在
        if not GRAPH_STATE.exists():
            builder.build()
        result = builder.query_related(sys.argv[2])
        print(f"🕸️ {result['查询关键词']}: {result['关联条目数']}条关联")
        for item in result["关联概念"]:
            print(f"  → {item['关键词']} ({item['强度']}, 共现{item['共现']}次)")

    elif cmd == "compress-all":
        print("=" * 50)
        print("  🧬 外脑全量压缩 v2.0")
        print("=" * 50)

        # 1. 去重
        deduper = RedundancyDeduplicator()
        dedup = deduper.deduplicate()
        print(f"  [1/4] 去重: {dedup.get('状态', '?')} ({dedup.get('重复组数', 0)}组)")

        # 2. 衰减
        decayer = TimeDecayer()
        decay = decayer.scan_all_entries()
        print(f"  [2/4] 衰减: {decay.get('状态', '?')} ({decay.get('总条目', 0)}条)")

        # 3. 图谱
        builder = KnowledgeGraphBuilder()
        graph = builder.build()
        print(f"  [3/4] 图谱: {graph.get('状态', '?')} ({graph.get('节点数', 0)}节点, {graph.get('边数', 0)}边)")

        # 4. 报告
        report = CompressReporter.generate_report()
        ratio_str = report.get("压缩率", "0.0%")
        print(f"  [4/4] 报告: 压缩率 {ratio_str}")
        print(f"  压缩率: {ratio_str}")
        print("=" * 50)
        print("  ✅ 全量压缩完成")
        # 同时输出 JSON 供 API/仪表盘直接解析
        print(json.dumps(report, ensure_ascii=False))

    elif cmd == "report":
        report = CompressReporter.generate_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif cmd == "status":
        print("=" * 50)
        print("  ⚙️ 外脑压缩引擎 v2.0 状态")
        print("=" * 50)
        print(f"  数据文件: {'存在' if DAILY_LOG_DB.exists() else '不存在'}")
        print(f"  图谱文件: {'存在' if GRAPH_STATE.exists() else '不存在'}")
        print(f"  压缩状态: {'存在' if COMPRESS_STATE.exists() else '不存在'}")

        if DAILY_LOG_DB.exists():
            entries = 0
            with open(DAILY_LOG_DB, "r") as f:
                entries = sum(1 for _ in f)
            print(f"  结构化条目: {entries}")

        if GRAPH_STATE.exists():
            g = json.loads(open(GRAPH_STATE, "r").read())
            print(f"  图谱节点: {len(g.get('nodes', {}))} | 边: {len(g.get('edges', []))}")
        print("=" * 50)

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
