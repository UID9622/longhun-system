#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_INNOVATION_TRACER-v1.0-298a70e5
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
👁️ 上帝之眼 · 创新溯源推演器 v1.0

追溯争议性技术/创新的本源：谁先提出、谁自研、谁借鉴、谁演进。
基于公开网络证据 + 时间线构建 → 多维推演 → 非确定性结论。

📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md

═══ 重要声明 ═══
本工具仅做【推演】，不做【判定】。
所有结论均为基于公开信息的推演结果，不代表任何事实认定。
仅供研究参考，不构成任何法律意义上的证据或指控。
═══════════════

用法：
  python3 bin/lh_innovation_tracer.py search "争议主题"     # 搜索+推演
  python3 bin/lh_innovation_tracer.py analyze evidence.json  # 基于已有证据推演
  python3 bin/lh_innovation_tracer.py pipe                   # 从 stdin 读取证据JSON

DNA: #龍芯⚡️丙午·乙未·乙卯·申时·䷰革-INNOVATION-TRACER-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

# ============================================================
# 免责声明 · 法律护盾（焊死·不可删除）
# ============================================================

LEGAL_DISCLAIMER = """
╔══════════════════════════════════════════════════════════════╗
║                    ⚖️ 重要法律声明                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. 本报告为【AI辅助推演】，非事实认定，非法律证据。           ║
║  2. 所有信息来源为公开网络搜索结果，可能存在时效性、          ║
║     完整性、准确性偏差。                                      ║
║  3. "先后"仅指公开可查时间，不代表实际研发/提出时间。         ║
║  4. "相似性"不构成抄袭/侵权的判定，仅提示可进一步研究。       ║
║  5. 本报告不作为任何商业决策、法律诉讼、舆论攻击的依据。      ║
║  6. 报告中的置信度仅反映搜索证据的充分性，非事实确定性。      ║
║  7. 如有信息不准确，欢迎提供补充证据进行校正推演。            ║
║  8. 本工具所有者不为任何基于本报告的后续行为承担责任。        ║
║                                                              ║
║  📌 核心原则：只推演 · 不审判 · 不站队 · 可验证 · 可校正     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# ============================================================
# 推演维度定义
# ============================================================

DEDUCTION_DIMENSIONS = {
    "temporal_priority": {
        "name": "⏰ 时间优先度",
        "description": "谁先公开披露/发表/开源？（基于可查的公开时间戳）",
        "weight": 0.30,
        "scoring": {
            "first_public": 1.0,
            "early_adopter": 0.7,
            "later_entrant": 0.3,
            "unknown": 0.0,
        },
    },
    "technical_depth": {
        "name": "🔬 技术深度",
        "description": "谁的解释/实现最完整、最深入？",
        "weight": 0.25,
        "scoring": {
            "complete_implementation": 1.0,
            "detailed_design": 0.7,
            "concept_only": 0.3,
            "superficial": 0.1,
        },
    },
    "evidence_chain": {
        "name": "🔗 证据链完整度",
        "description": "引用关系、致谢、fork链、许可证继承是否清晰？",
        "weight": 0.20,
        "scoring": {
            "full_chain": 1.0,
            "partial_chain": 0.6,
            "missing_links": 0.2,
            "no_chain": 0.0,
        },
    },
    "independence": {
        "name": "🎯 独立度",
        "description": "是否可能独立发现/并行研发？（基于领域常识判定）",
        "weight": 0.15,
        "scoring": {
            "likely_independent": 1.0,
            "possible_parallel": 0.6,
            "likely_derived": 0.2,
            "unknown": 0.5,
        },
    },
    "community_recognition": {
        "name": "🌐 社区认可度",
        "description": "开源社区/学术界/行业内的引用和认可情况",
        "weight": 0.10,
        "scoring": {
            "widely_cited": 1.0,
            "moderately_cited": 0.6,
            "rarely_cited": 0.2,
            "unknown": 0.0,
        },
    },
}

# ============================================================
# 来源可信度评分
# ============================================================

SOURCE_CREDIBILITY = {
    "academic_paper": 0.95,
    "arxiv": 0.85,
    "patent": 0.90,
    "official_docs": 0.90,
    "github_repo": 0.80,
    "tech_blog_official": 0.75,
    "tech_blog_personal": 0.55,
    "news_outlet_major": 0.70,
    "news_outlet_minor": 0.40,
    "social_media": 0.25,
    "forum": 0.30,
    "wiki": 0.50,
    "unknown": 0.10,
}

# ============================================================
# 归档路径（推演后自动落盘）
# ============================================================

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
_ARCHIVE_DIR = _PROJECT_ROOT / "L7_数据层"
_ARCHIVE_CHAIN = _ARCHIVE_DIR / "innovation_trace_chain.jsonl"
_ARCHIVE_INDEX = _ARCHIVE_DIR / "innovation_trace_index.json"
_ARCHIVE_SQLITE = _ARCHIVE_DIR / "data" / "longhun_unified.db"
_REPORTS_DIR = _ARCHIVE_DIR / "strategy_reports" / "innovation_traces"

# 确保目录存在
_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def classify_source(url: str, site_name: str = "") -> str:
    """根据URL和站点名称分类来源类型"""
    url_lower = url.lower()
    name_lower = site_name.lower()

    if any(d in url_lower for d in ["arxiv.org", "paper", "doi.org", "scholar.google"]):
        return "academic_paper" if "arxiv" not in url_lower else "arxiv"
    if any(d in url_lower for d in ["patent", "patents.google"]):
        return "patent"
    if any(d in url_lower for d in ["github.com", "gitlab.com", "gitee.com"]):
        return "github_repo"
    if any(d in url_lower for d in ["docs.", "documentation", "readthedocs", "wiki"]):
        return "official_docs" if "docs." in url_lower else "wiki"
    if any(d in name_lower for d in ["官方", "official"]):
        return "official_docs"
    if any(d in url_lower for d in ["zhihu.com", "weixin.qq", "mp.weixin"]):
        return "tech_blog_personal"
    if any(d in url_lower for d in ["blog.", "medium.com", "dev.to"]):
        return "tech_blog_personal"
    if any(d in name_lower for d in ["博客", "blog"]):
        return "tech_blog_personal" if "官方" not in name_lower else "tech_blog_official"
    if any(d in url_lower for d in ["twitter.com", "x.com", "weibo.com"]):
        return "social_media"
    if any(d in url_lower for d in ["reddit.com", "v2ex.com", "hackernews", "news.ycombinator"]):
        return "forum"
    if any(d in name_lower for d in ["新闻", "news", "报道"]):
        return "news_outlet_major"
    return "unknown"


# ============================================================
# 数据结构
# ============================================================


@dataclass
class EvidenceItem:
    """单条证据"""
    title: str
    url: str
    snippet: str
    date: str                           # ISO格式日期 YYYY-MM-DD
    source_name: str                    # 来源名称
    source_type: str = "unknown"        # 自动分类
    credibility: float = 0.5            # 自动计算
    relevance_score: float = 0.5        # 相关性
    party: str = ""                     # 关联方标签（用于分组）
    key_claims: List[str] = field(default_factory=list)  # 关键主张
    notes: str = ""                     # 人工备注

    def __post_init__(self):
        if self.source_type == "unknown" and self.url:
            self.source_type = classify_source(self.url, self.source_name)
        self.credibility = SOURCE_CREDIBILITY.get(self.source_type, 0.1)


@dataclass
class TimelineEvent:
    """时间线事件"""
    date: str
    party: str
    title: str
    url: str
    event_type: str  # "publication", "release", "announcement", "patent", "commit"
    significance: str  # 简要说明
    evidence_index: int  # 对应证据索引


@dataclass
class PartyProfile:
    """参与方画像"""
    name: str
    first_public_date: Optional[str] = None
    evidence_count: int = 0
    tech_depth_score: float = 0.0
    evidence_chain_score: float = 0.0
    independence_score: float = 0.5
    community_score: float = 0.0
    weighted_total: float = 0.0
    key_contributions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class DeductionResult:
    """推演结果"""
    topic: str
    parties: List[PartyProfile] = field(default_factory=list)
    timeline: List[TimelineEvent] = field(default_factory=list)
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    summary: str = ""
    caveats: List[str] = field(default_factory=list)
    confidence: float = 0.0
    dna: str = ""
    generated_at: str = ""


# ============================================================
# 核心推演引擎
# ============================================================


class InnovationTracer:
    """创新溯源推演引擎 — P05 上帝之眼"""

    def __init__(self):
        self.evidence: List[EvidenceItem] = []
        self.parties: Dict[str, PartyProfile] = {}
        self.timeline: List[TimelineEvent] = []

    def add_evidence(self, item: EvidenceItem):
        """添加一条证据"""
        self.evidence.append(item)

    def add_evidence_batch(self, items: List[Dict[str, Any]]):
        """批量添加证据"""
        for item in items:
            ev = EvidenceItem(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet", ""),
                date=item.get("date", ""),
                source_name=item.get("source_name", ""),
                party=item.get("party", ""),
                key_claims=item.get("key_claims", []),
                notes=item.get("notes", ""),
            )
            self.evidence.append(ev)

    def _extract_date(self, date_str: str) -> str:
        """标准化日期格式"""
        if not date_str:
            return "unknown"
        # Try common formats
        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日", "%b %d, %Y", "%d %b %Y"]:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        # Try extract YYYY-MM-DD pattern
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
        if match:
            return match.group(0)
        match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", date_str)
        if match:
            return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
        return date_str[:10] if len(date_str) >= 10 else "unknown"

    def _detect_event_type(self, title: str, snippet: str) -> str:
        """自动检测事件类型"""
        combined = (title + " " + snippet).lower()
        if any(w in combined for w in ["发布", "release", "launch", "推出"]):
            return "release"
        if any(w in combined for w in ["开源", "open source", "open-source"]):
            return "release"
        if any(w in combined for w in ["专利", "patent"]):
            return "patent"
        if any(w in combined for w in ["论文", "paper", "published", "发表"]):
            return "publication"
        if any(w in combined for w in ["宣布", "announce", "公布"]):
            return "announcement"
        if any(w in combined for w in ["commit", "提交", "merge", "pr"]):
            return "commit"
        return "publication"

    def build_timeline(self):
        """构建时间线"""
        events = []
        for i, ev in enumerate(self.evidence):
            date = self._extract_date(ev.date)
            event_type = self._detect_event_type(ev.title, ev.snippet)
            events.append(TimelineEvent(
                date=date,
                party=ev.party or ev.source_name,
                title=ev.title,
                url=ev.url,
                event_type=event_type,
                significance=ev.snippet[:100] if ev.snippet else "",
                evidence_index=i,
            ))
        # 按日期排序
        events.sort(key=lambda e: e.date if e.date != "unknown" else "9999-99-99")
        self.timeline = events
        return events

    def build_parties(self):
        """构建参与方画像"""
        party_map: Dict[str, List[EvidenceItem]] = {}
        for ev in self.evidence:
            key = ev.party or ev.source_name or "unknown"
            if key not in party_map:
                party_map[key] = []
            party_map[key].append(ev)

        # 第一遍：创建所有Profile，计算基础分数
        profiles: Dict[str, PartyProfile] = {}
        for name, items in party_map.items():
            profile = PartyProfile(name=name)
            profile.evidence_count = len(items)

            # 找最早公开日期
            dates = [self._extract_date(it.date) for it in items if it.date]
            valid_dates = [d for d in dates if d != "unknown"]
            if valid_dates:
                profile.first_public_date = min(valid_dates)

            # 技术深度评分
            depths = []
            for it in items:
                depth = 0.0
                if len(it.snippet) > 200:
                    depth += 0.4
                if it.key_claims:
                    depth += min(len(it.key_claims) * 0.15, 0.3)
                if it.source_type in ("github_repo", "academic_paper", "arxiv", "patent"):
                    depth += 0.3
                depths.append(min(depth, 1.0))
            profile.tech_depth_score = sum(depths) / len(depths) if depths else 0.2

            # 证据链完整度
            has_references = any(
                any(w in (it.title + it.snippet).lower()
                    for w in ["参考", "引用", "基于", "fork", "致敬", "reference", "based on", "inspired"])
                for it in items
            )
            profile.evidence_chain_score = 0.7 if has_references else 0.3

            # 社区认可度（基于来源类型）
            cred_scores = [it.credibility for it in items]
            profile.community_score = sum(cred_scores) / len(cred_scores) if cred_scores else 0.1

            # 关键贡献提取
            for it in items:
                if it.key_claims:
                    profile.key_contributions.extend(it.key_claims)
                elif it.snippet and len(it.snippet) > 20:
                    profile.key_contributions.append(it.snippet[:120])

            profiles[name] = profile

        # 第二遍：基于所有Profile计算加权总分
        all_dates = [p.first_public_date for p in profiles.values()]
        dims = DEDUCTION_DIMENSIONS
        for name, profile in profiles.items():
            profile.weighted_total = (
                _score_temporal(profile.first_public_date, all_dates) * dims["temporal_priority"]["weight"]
                + profile.tech_depth_score * dims["technical_depth"]["weight"]
                + profile.evidence_chain_score * dims["evidence_chain"]["weight"]
                + profile.independence_score * dims["independence"]["weight"]
                + profile.community_score * dims["community_recognition"]["weight"]
            )
            self.parties[name] = profile

    def deduce(self, topic: str) -> DeductionResult:
        """执行推演"""
        self.build_timeline()
        self.build_parties()

        # 排序参与方
        sorted_parties = sorted(
            self.parties.values(),
            key=lambda p: p.weighted_total,
            reverse=True,
        )

        # 生成摘要
        lines = []
        if sorted_parties:
            top = sorted_parties[0]
            lines.append(f"根据公开可查信息推演，在「{topic}」领域：")
            lines.append("")

            # 时间优先
            earliest = sorted(sorted_parties, key=lambda p: p.first_public_date or "9999")
            if earliest[0].first_public_date:
                lines.append(
                    f"⏰ 最早公开记录：{earliest[0].name}"
                    f"（{earliest[0].first_public_date}）"
                )

            # 技术深度
            deepest = max(sorted_parties, key=lambda p: p.tech_depth_score)
            lines.append(
                f"🔬 技术深度推演最高：{deepest.name}"
                f"（技术深度分 {deepest.tech_depth_score:.2f}）"
            )

            # 综合推演
            lines.append("")
            lines.append("📊 综合加权推演排名（仅供参考）：")
            for i, p in enumerate(sorted_parties[:5], 1):
                lines.append(
                    f"  {i}. {p.name}"
                    f" · 综合分 {p.weighted_total:.3f}"
                    f" · 证据 {p.evidence_count}条"
                )

        # 注意事项
        caveats = [
            "本推演仅基于搜索到的公开网络信息，可能遗漏未公开的内部研发信息",
            "公开时间 ≠ 实际研发时间，无法确定内部研发的起始时间",
            "技术相似性 ≠ 借鉴/抄袭，独立并行发现是常见现象",
            "证据充分性受限于搜索工具覆盖范围和搜索关键词选择",
            "社区认可度受语言壁垒和传播渠道影响，中文内容可能被低估",
            "如需更准确的结论，建议补充专利数据库、学术数据库的检索结果",
        ]

        # 计算整体置信度
        evidence_count = len(self.evidence)
        party_count = len(self.parties)
        if evidence_count >= 20 and party_count >= 3:
            confidence = 0.7
        elif evidence_count >= 10 and party_count >= 2:
            confidence = 0.5
        elif evidence_count >= 5:
            confidence = 0.3
        else:
            confidence = 0.1

        # 生成DNA
        dna = self._generate_dna(topic)

        return DeductionResult(
            topic=topic,
            parties=sorted_parties,
            timeline=self.timeline,
            evidence_items=self.evidence,
            summary="\n".join(lines),
            caveats=caveats,
            confidence=confidence,
            dna=dna,
            generated_at=datetime.now().isoformat(),
        )

    def _generate_dna(self, topic: str) -> str:
        """生成DNA追溯码"""
        import hashlib
        seed = f"{topic}-{len(self.evidence)}-{datetime.now().isoformat()}"
        hash8 = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️丙午·乙未·乙卯·申时·䷰革-INNOVATION-TRACE-{hash8}"

    def _compute_content_hash(self, result: 'DeductionResult') -> str:
        """计算推演内容哈希（防篡改校验）"""
        payload = json.dumps({
            "topic": result.topic,
            "parties": [p.name for p in result.parties],
            "summary": result.summary,
            "confidence": result.confidence,
        }, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


# ============================================================
# 自动归档引擎（推演后自动触发）
# ============================================================


def archive_trace(result: DeductionResult, tracer: InnovationTracer, skip_sqlite: bool = False) -> Dict[str, Any]:
    """推演完成后自动归档到三层存储。

    1. JSONL 链（append-only，不可覆不可删）
    2. JSON 索引（快速查询）
    3. SQLite 数据库（结构化查询）

    返回归档状态信息。
    """
    content_hash = hashlib.sha256(
        json.dumps({
            "topic": result.topic,
            "parties": [p.name for p in result.parties],
            "summary": result.summary,
            "confidence": result.confidence,
        }, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()[:16]

    timestamp = datetime.now().isoformat()
    parties_json = json.dumps([
        {
            "name": p.name,
            "first_public_date": p.first_public_date,
            "evidence_count": p.evidence_count,
            "tech_depth_score": round(p.tech_depth_score, 3),
            "evidence_chain_score": round(p.evidence_chain_score, 3),
            "community_score": round(p.community_score, 3),
            "weighted_total": round(p.weighted_total, 4),
        }
        for p in result.parties
    ], ensure_ascii=False)

    timeline_json = json.dumps([
        {
            "date": e.date,
            "party": e.party,
            "title": e.title,
            "url": e.url,
            "event_type": e.event_type,
        }
        for e in result.timeline
    ], ensure_ascii=False)

    archive_entry = {
        "dna": result.dna,
        "topic": result.topic,
        "timestamp": timestamp,
        "confidence": result.confidence,
        "parties_count": len(result.parties),
        "evidence_count": len(result.evidence_items),
        "parties": json.loads(parties_json),
        "summary": result.summary,
        "content_hash": content_hash,
        "uid": "UID9622",
        "dimensions": list(DEDUCTION_DIMENSIONS.keys()),
    }

    status = {"jsonl": False, "index": False, "sqlite": False, "report": False, "dna": result.dna}

    # ── 1. JSONL 链（append-only） ──
    try:
        _ensure_chain_init()
        with open(_ARCHIVE_CHAIN, "a", encoding="utf-8") as f:
            f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")
        status["jsonl"] = True
    except Exception as e:
        status["jsonl_error"] = str(e)

    # ── 2. JSON 索引 ──
    try:
        _update_trace_index(archive_entry)
        status["index"] = True
    except Exception as e:
        status["index_error"] = str(e)

    # ── 3. SQLite 数据库 ──
    if not skip_sqlite:
        try:
            _archive_to_sqlite(result, archive_entry, parties_json, timeline_json)
            status["sqlite"] = True
        except Exception as e:
            status["sqlite_error"] = str(e)

    # ── 4. 报告MD文件 ──
    try:
        report_text = generate_report(result, verbose=True)
        safe_topic = re.sub(r'[^\w\u4e00-\u9fff-]', '_', result.topic)[:60]
        report_file = _REPORTS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_topic}.md"
        report_file.write_text(report_text, encoding="utf-8")
        status["report"] = str(report_file)
    except Exception as e:
        status["report_error"] = str(e)

    # ── 5. DNA 注册表登记 ──
    try:
        _register_dna(result)
    except Exception:
        pass  # DNA注册失败不影响主流程

    return status


def _ensure_chain_init():
    """确保JSONL链文件已初始化"""
    if not _ARCHIVE_CHAIN.exists():
        init_entry = {
            "chain": "init",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "dna": "#龍芯⚡️丙午·乙未·乙卯·申时·䷰革-INNOVATION-TRACE-CHAIN-INIT",
            "desc": "创新溯源推演归档链·append-only·不可覆不可删·每行一条推演记录",
        }
        with open(_ARCHIVE_CHAIN, "w", encoding="utf-8") as f:
            f.write(json.dumps(init_entry, ensure_ascii=False) + "\n")


def _update_trace_index(entry: Dict[str, Any]):
    """更新JSON索引文件"""
    if _ARCHIVE_INDEX.exists():
        index = json.loads(_ARCHIVE_INDEX.read_text(encoding="utf-8"))
    else:
        index = {"traces": [], "stats": {"total": 0, "last_trace": None, "last_updated": None}}

    # 避免重复
    existing_dnas = {t.get("dna") for t in index["traces"]}
    if entry["dna"] in existing_dnas:
        return

    index["traces"].append({
        "dna": entry["dna"],
        "topic": entry["topic"],
        "timestamp": entry["timestamp"],
        "confidence": entry["confidence"],
        "parties_count": entry["parties_count"],
        "evidence_count": entry["evidence_count"],
        "content_hash": entry["content_hash"],
    })
    index["stats"]["total"] = len(index["traces"])
    index["stats"]["last_trace"] = entry["timestamp"]
    index["stats"]["last_updated"] = datetime.now().isoformat()

    _ARCHIVE_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def _archive_to_sqlite(result: DeductionResult, entry: Dict[str, Any], parties_json: str, timeline_json: str):
    """写入SQLite数据库"""
    conn = sqlite3.connect(str(_ARCHIVE_SQLITE))
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS innovation_traces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna TEXT UNIQUE,
                topic TEXT,
                timestamp TEXT,
                confidence REAL,
                parties_count INTEGER,
                evidence_count INTEGER,
                parties_json TEXT,
                timeline_json TEXT,
                summary TEXT,
                report_text TEXT,
                content_hash TEXT,
                tags TEXT,
                uid TEXT DEFAULT 'UID9622'
            )
        """)

        report_text = generate_report(result, verbose=True)
        tags = ",".join(result.topic.split())

        conn.execute("""
            INSERT OR REPLACE INTO innovation_traces
            (dna, topic, timestamp, confidence, parties_count, evidence_count,
             parties_json, timeline_json, summary, report_text, content_hash, tags, uid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["dna"],
            entry["topic"],
            entry["timestamp"],
            entry["confidence"],
            entry["parties_count"],
            entry["evidence_count"],
            parties_json,
            timeline_json,
            entry["summary"],
            report_text,
            entry["content_hash"],
            tags,
            "UID9622",
        ))
        conn.commit()
    finally:
        conn.close()


def _register_dna(result: DeductionResult):
    """在DNA注册表中登记"""
    dna_registry = _ARCHIVE_DIR / "dna_registry_index.json"
    if not dna_registry.exists():
        return
    try:
        registry = json.loads(dna_registry.read_text(encoding="utf-8"))
        if "entries" not in registry:
            registry["entries"] = []
        # 检查是否已存在
        existing = {e.get("dna") for e in registry["entries"]}
        if result.dna not in existing:
            registry["entries"].append({
                "dna": result.dna,
                "timestamp": datetime.now().isoformat(),
                "type": "INNOVATION_TRACE",
                "topic": result.topic,
            })
            dna_registry.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def list_traces(limit: int = 20) -> List[Dict[str, Any]]:
    """列出最近的推演记录"""
    traces = []
    if _ARCHIVE_INDEX.exists():
        index = json.loads(_ARCHIVE_INDEX.read_text(encoding="utf-8"))
        traces = index.get("traces", [])[-limit:]
        traces.reverse()
    return traces


def get_trace(dna_or_hash: str) -> Optional[Dict[str, Any]]:
    """根据DNA或哈希获取单条推演记录（支持DNA后缀模糊匹配）"""
    # 1. 先查 SQLite
    try:
        conn = sqlite3.connect(str(_ARCHIVE_SQLITE))
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM innovation_traces WHERE dna = ? OR content_hash = ? OR dna LIKE ?",
            (dna_or_hash, dna_or_hash, f"%{dna_or_hash}")
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception:
        pass

    # 2. 回退到 JSONL 链搜索（精确匹配+后缀匹配）
    if _ARCHIVE_CHAIN.exists():
        for line in _ARCHIVE_CHAIN.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
                entry_dna = entry.get("dna", "")
                if (entry_dna == dna_or_hash
                        or entry.get("content_hash") == dna_or_hash
                        or entry_dna.endswith(dna_or_hash)):
                    return entry
            except json.JSONDecodeError:
                continue

    return None


def print_archive_status(status: Dict[str, Any]):
    """打印归档状态"""
    print()
    print("─" * 40)
    print("  📦 自动归档状态")
    print("─" * 40)
    checks = [
        ("JSONL链", status.get("jsonl")),
        ("JSON索引", status.get("index")),
        ("SQLite数据库", status.get("sqlite")),
        ("报告MD文件", bool(status.get("report"))),
    ]
    for name, ok in checks:
        icon = "✅" if ok else "❌"
        detail = ""
        if not ok:
            detail = f" ({status.get(f'{name}_error', '')})" if status.get(f'{name}_error') else ""
        elif name == "报告MD文件" and ok:
            detail = f" → {status.get('report', '')}"
        print(f"  {icon} {name}{detail}")
    print(f"  🧬 DNA: {status.get('dna', 'N/A')}")
    print("─" * 40)


def _score_temporal(first_date: Optional[str], all_dates: List[Optional[str]]) -> float:
    """计算时间优先度分数"""
    if not first_date:
        return 0.0
    valid_dates = [d for d in all_dates if d]
    if not valid_dates:
        return 0.5
    earliest = min(valid_dates)
    if first_date == earliest:
        # 检查是否唯一最早
        count_earliest = sum(1 for d in valid_dates if d == earliest)
        return 1.0 if count_earliest == 1 else 0.85
    # 计算相对时间差
    try:
        fd = datetime.strptime(first_date, "%Y-%m-%d")
        ed = datetime.strptime(earliest, "%Y-%m-%d")
        diff_days = (fd - ed).days
        if diff_days <= 30:
            return 0.75
        elif diff_days <= 180:
            return 0.6
        elif diff_days <= 365:
            return 0.4
        else:
            return 0.2
    except ValueError:
        return 0.3


# ============================================================
# 报告生成
# ============================================================


def generate_report(result: DeductionResult, verbose: bool = False) -> str:
    """生成推演报告"""

    report = []
    report.append("=" * 68)
    report.append("  👁️ 上帝之眼 · 创新溯源推演报告")
    report.append("=" * 68)
    report.append("")
    report.append(f"📋 推演主题：{result.topic}")
    report.append(f"🧬 DNA追溯：{result.dna}")
    report.append(f"📅 生成时间：{result.generated_at}")
    report.append(f"📊 证据数量：{len(result.evidence_items)}条")
    report.append(f"👥 涉及方数：{len(result.parties)}方")
    report.append(f"🎯 推演置信度：{result.confidence:.0%}")
    report.append("")

    # ── 时间线 ──
    report.append("─" * 68)
    report.append("  ⏰ 关键时间线")
    report.append("─" * 68)
    if result.timeline:
        for event in result.timeline:
            icon = {
                "release": "🚀",
                "publication": "📄",
                "patent": "📜",
                "announcement": "📢",
                "commit": "💾",
            }.get(event.event_type, "📌")
            report.append(
                f"  {icon} {event.date} | {event.party} | {event.title[:60]}"
            )
            if verbose and event.url:
                report.append(f"     ↳ {event.url}")
    else:
        report.append("  （无时间线事件）")
    report.append("")

    # ── 参与方画像 ──
    report.append("─" * 68)
    report.append("  👤 参与方推演画像")
    report.append("─" * 68)
    for i, party in enumerate(result.parties[:10], 1):
        report.append(f"  {i}. {party.name}")
        report.append(f"     最早公开：{party.first_public_date or '未知'}")
        report.append(f"     证据数量：{party.evidence_count}条")
        report.append(f"     技术深度：{_progress_bar(party.tech_depth_score)} {party.tech_depth_score:.2f}")
        report.append(f"     证据链：  {_progress_bar(party.evidence_chain_score)} {party.evidence_chain_score:.2f}")
        report.append(f"     社区认可：{_progress_bar(party.community_score)} {party.community_score:.2f}")
        report.append(f"     综合推演分：{party.weighted_total:.3f}")
        if party.key_contributions and verbose:
            report.append(f"     关键发现：")
            for kc in party.key_contributions[:3]:
                report.append(f"       · {kc[:100]}")
        report.append("")

    # ── 综合推演 ──
    report.append("─" * 68)
    report.append("  🧮 综合推演")
    report.append("─" * 68)
    report.append("")
    for line in result.summary.split("\n"):
        report.append(f"  {line}")
    report.append("")

    # ── 注意事项 ──
    report.append("─" * 68)
    report.append("  ⚠️ 推演局限性说明")
    report.append("─" * 68)
    for caveat in result.caveats:
        report.append(f"  · {caveat}")
    report.append("")

    # ── 法律声明 ──
    report.append(LEGAL_DISCLAIMER)
    report.append("")

    # ── 各维度详细评分 ──
    if verbose:
        report.append("─" * 68)
        report.append("  📐 五维推演详情")
        report.append("─" * 68)
        dims = DEDUCTION_DIMENSIONS
        report.append(f"  {'维度':<16} {'权重':>6} {'说明'}")
        report.append(f"  {'─'*16} {'─'*6} {'─'*40}")
        for key, dim in dims.items():
            report.append(f"  {dim['name']:<16} {dim['weight']:>5.0%}  {dim['description']}")
        report.append("")
        report.append(f"  置信度说明：{result.confidence:.0%} 置信度意味着基于当前")
        report.append(f"  搜索证据的推演可靠性约为{result.confidence:.0%}。建议补充更多")
        report.append(f"  证据来源以提高置信度。")
        report.append("")

    report.append("═" * 68)
    report.append("  报告结束 · 仅供研究参考 · 不构成任何认定或指控")
    report.append("═" * 68)

    return "\n".join(report)


def _progress_bar(score: float, width: int = 10) -> str:
    """生成进度条"""
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


# ============================================================
# Web 搜索模块
# ============================================================


def search_web(topic: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索网络证据

    尝试使用 ddgs (duckduckgo-search)，如果不可用则返回提示。
    """
    results = []
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            for r in ddgs.text(topic, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source_name": _extract_domain(r.get("href", "")),
                })
    except ImportError:
        # 尝试使用 ddg 备用模块
        try:
            from ddg import search as ddg_search
            for r in ddg_search(topic, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("link", r.get("url", "")),
                    "snippet": r.get("snippet", r.get("description", "")),
                    "date": "",
                    "source_name": _extract_domain(r.get("link", r.get("url", ""))),
                })
        except ImportError:
            print("⚠️ 未安装 web 搜索模块。请安装 duckduckgo-search：", file=sys.stderr)
            print("   pip install duckduckgo-search", file=sys.stderr)
            print("", file=sys.stderr)
            print("或手动收集证据后使用 analyze 子命令：", file=sys.stderr)
            print("   python3 bin/lh_innovation_tracer.py analyze evidence.json", file=sys.stderr)
            return results

    return results


def _extract_domain(url: str) -> str:
    """从URL提取域名"""
    import re
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return match.group(1) if match else url


# ============================================================
# CLI 入口
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="👁️ 上帝之眼 · 创新溯源推演器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 bin/lh_innovation_tracer.py template "鸿蒙自研争议" -p 华为 谷歌
  python3 bin/lh_innovation_tracer.py search "DeepSeek vs OpenAI 创新溯源"
  python3 bin/lh_innovation_tracer.py analyze evidence.json --verbose
  python3 bin/lh_innovation_tracer.py list              # 查看最近推演记录
  python3 bin/lh_innovation_tracer.py get <dna_hash>    # 获取特定推演记录
  echo '[{"title":"...","url":"..."}]' | python3 bin/lh_innovation_tracer.py pipe
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # template 子命令
    tmpl_p = sub.add_parser("template", help="生成证据收集JSON模板")
    tmpl_p.add_argument("topic", help="推演主题")
    tmpl_p.add_argument("-p", "--parties", nargs="*", help="预期参与方列表")
    tmpl_p.add_argument("-o", "--output", help="输出模板到文件")

    # search 子命令
    search_p = sub.add_parser("search", help="搜索网络并推演")
    search_p.add_argument("topic", help="争议主题/关键词")
    search_p.add_argument("-n", "--num", type=int, default=20, help="搜索结果数（默认20）")
    search_p.add_argument("-o", "--output", help="输出报告到文件")
    search_p.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    search_p.add_argument("--save-evidence", help="保存搜索证据到JSON文件")
    search_p.add_argument("--no-archive", action="store_true", help="跳过自动归档")

    # analyze 子命令
    analyze_p = sub.add_parser("analyze", help="基于已有证据JSON推演")
    analyze_p.add_argument("evidence_file", help="证据JSON文件路径")
    analyze_p.add_argument("-o", "--output", help="输出报告到文件")
    analyze_p.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    analyze_p.add_argument("--no-archive", action="store_true", help="跳过自动归档")

    # pipe 子命令
    pipe_p = sub.add_parser("pipe", help="从stdin读取证据JSON推演")
    pipe_p.add_argument("-o", "--output", help="输出报告到文件")
    pipe_p.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    pipe_p.add_argument("--no-archive", action="store_true", help="跳过自动归档")

    # list 子命令
    list_p = sub.add_parser("list", help="列出最近的推演记录")
    list_p.add_argument("-n", "--num", type=int, default=20, help="显示条数（默认20）")
    list_p.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")

    # get 子命令
    get_p = sub.add_parser("get", help="获取指定推演记录的完整报告")
    get_p.add_argument("dna_or_hash", help="DNA追溯码或内容哈希")
    get_p.add_argument("-v", "--verbose", action="store_true", help="显示完整报告")
    get_p.add_argument("--json", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()

    if args.command == "template":
        template = generate_evidence_template(args.topic, parties=getattr(args, "parties", None))
        if args.output:
            Path(args.output).write_text(template, encoding="utf-8")
            print(f"📄 模板已保存至：{args.output}")
        else:
            print(template)
        print()
        print("💡 使用方式：")
        print(f"   1. 填写模板中的证据信息")
        print(f"   2. 运行：python3 bin/lh_innovation_tracer.py analyze {args.output or 'evidence.json'}")
        print(f"   3. 或让AI帮你搜索并填充证据后分析")
        sys.exit(0)

    elif args.command == "search":
        print(f"🔍 搜索中：{args.topic}")
        print(f"   请求 {args.num} 条结果...")
        print()

        search_results = search_web(args.topic, max_results=args.num)

        if not search_results:
            print("❌ 搜索无结果或搜索模块不可用。")
            print("   请安装 duckduckgo-search 后重试：pip install duckduckgo-search")
            print("   或手动收集证据后使用 analyze 子命令。")
            sys.exit(1)

        print(f"✅ 获取 {len(search_results)} 条搜索结果")
        print()

        # 保存证据（如果需要）
        if args.save_evidence:
            with open(args.save_evidence, "w", encoding="utf-8") as f:
                json.dump(search_results, f, ensure_ascii=False, indent=2)
            print(f"💾 证据已保存至：{args.save_evidence}")
            print()

        # 尝试自动标注参与方
        parties = _auto_detect_parties(args.topic)
        for r in search_results:
            r["party"] = _guess_party(r, parties)

        # 执行推演
        tracer = InnovationTracer()
        tracer.add_evidence_batch(search_results)
        result = tracer.deduce(args.topic)
        report = generate_report(result, verbose=args.verbose)

        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"📄 报告已保存至：{args.output}")
        else:
            print(report)

        # ── 自动归档 ──
        if not getattr(args, "no_archive", False):
            status = archive_trace(result, tracer, skip_sqlite=False)
            print_archive_status(status)

    elif args.command == "analyze":
        evidence_path = Path(args.evidence_file)
        if not evidence_path.exists():
            print(f"❌ 文件不存在：{args.evidence_file}", file=sys.stderr)
            sys.exit(1)

        evidence_data = json.loads(evidence_path.read_text(encoding="utf-8"))
        if isinstance(evidence_data, dict) and "topic" in evidence_data:
            topic = evidence_data["topic"]
            items = evidence_data.get("evidence", evidence_data.get("items", []))
        elif isinstance(evidence_data, list):
            topic = evidence_path.stem
            items = evidence_data
        else:
            print("❌ 无法解析证据文件格式", file=sys.stderr)
            sys.exit(1)

        tracer = InnovationTracer()
        tracer.add_evidence_batch(items)
        result = tracer.deduce(topic)
        report = generate_report(result, verbose=args.verbose)

        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"📄 报告已保存至：{args.output}")
        else:
            print(report)

        # ── 自动归档 ──
        if not getattr(args, "no_archive", False):
            status = archive_trace(result, tracer, skip_sqlite=False)
            print_archive_status(status)

    elif args.command == "pipe":
        raw = sys.stdin.read()
        try:
            evidence_data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败：{e}", file=sys.stderr)
            sys.exit(1)

        if isinstance(evidence_data, dict) and "topic" in evidence_data:
            topic = evidence_data["topic"]
            items = evidence_data.get("evidence", evidence_data.get("items", []))
        elif isinstance(evidence_data, list):
            topic = "stdin-input"
            items = evidence_data
        else:
            print("❌ 无法解析输入格式", file=sys.stderr)
            sys.exit(1)

        tracer = InnovationTracer()
        tracer.add_evidence_batch(items)
        result = tracer.deduce(topic)
        report = generate_report(result, verbose=args.verbose)

        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"📄 报告已保存至：{args.output}")
        else:
            print(report)

        # ── 自动归档 ──
        if not getattr(args, "no_archive", False):
            status = archive_trace(result, tracer, skip_sqlite=False)
            print_archive_status(status)

    elif args.command == "list":
        traces = list_traces(limit=args.num)
        if not traces:
            print("📭 暂无推演记录。")
            print(f"   运行 python3 bin/lh_innovation_tracer.py search \"主题\" 进行首次推演。")
            sys.exit(0)

        print(f"📋 最近 {len(traces)} 条创新溯源推演记录：")
        print()
        for i, t in enumerate(traces, 1):
            ts_short = t.get("timestamp", "")[:19] if t.get("timestamp") else "N/A"
            conf = t.get("confidence", 0)
            conf_bar = "🟢" if conf >= 0.7 else ("🟡" if conf >= 0.4 else "🔴")
            topic = t.get("topic", "N/A")[:60]
            dna_short = t.get("dna", "")[-20:] if t.get("dna") else ""
            print(f"  {i:>2}. {conf_bar} {topic}")
            print(f"      置信度: {conf:.0%} · 证据: {t.get('evidence_count', 0)}条 · 方: {t.get('parties_count', 0)}")
            print(f"      时间: {ts_short} · DNA: ...{dna_short}")
            if args.verbose:
                ch = t.get("content_hash", "")
                print(f"      hash: {ch}")
            print()

        # 显示总数
        try:
            index = json.loads(_ARCHIVE_INDEX.read_text(encoding="utf-8"))
            stats = index.get("stats", {})
            total = stats.get("total", len(traces))
            if total > len(traces):
                print(f"  ... 共 {total} 条记录，显示最近 {len(traces)} 条")
        except Exception:
            pass

    elif args.command == "get":
        trace = get_trace(args.dna_or_hash)
        if not trace:
            print(f"❌ 未找到记录：{args.dna_or_hash}")
            print("   使用 python3 bin/lh_innovation_tracer.py list 查看所有记录")
            sys.exit(1)

        if args.json:
            # 输出结构化JSON
            output = {
                "dna": trace.get("dna"),
                "topic": trace.get("topic"),
                "timestamp": trace.get("timestamp"),
                "confidence": trace.get("confidence"),
                "parties_count": trace.get("parties_count"),
                "evidence_count": trace.get("evidence_count"),
                "content_hash": trace.get("content_hash"),
                "summary": trace.get("summary"),
            }
            parties = trace.get("parties", trace.get("parties_json", "[]"))
            if isinstance(parties, str):
                try:
                    parties = json.loads(parties)
                except Exception:
                    pass
            output["parties"] = parties
            print(json.dumps(output, ensure_ascii=False, indent=2))
        elif args.verbose and trace.get("report_text"):
            print(trace["report_text"])
        else:
            # 简洁输出
            print(f"🧬 DNA: {trace.get('dna', 'N/A')}")
            print(f"📋 主题: {trace.get('topic', 'N/A')}")
            print(f"📅 时间: {trace.get('timestamp', 'N/A')}")
            print(f"🎯 置信度: {trace.get('confidence', 0):.0%}")
            print(f"📊 证据: {trace.get('evidence_count', 0)}条 · 参与方: {trace.get('parties_count', 0)}")
            print(f"🔑 内容哈希: {trace.get('content_hash', 'N/A')}")
            print()
            print("─" * 40)
            summary = trace.get("summary", "")
            if summary:
                print(summary)
            else:
                print("（无摘要信息，使用 -v 查看完整报告）")
            print()
            print(f"💡 使用 --json 输出结构化数据，使用 -v 查看完整报告")

    else:
        parser.print_help()
        sys.exit(1)


def _auto_detect_parties(topic: str) -> List[str]:
    """从主题中自动检测可能的参与方"""
    # 常见技术争议方
    known_parties = {
        "鸿蒙": ["华为", "谷歌/Android", "苹果/iOS"],
        "harmonyos": ["Huawei", "Google/Android", "Apple/iOS"],
        "deepseek": ["DeepSeek/深度求索", "OpenAI", "Meta", "Google"],
        "自研": [],
        "芯片": [],
        "ai": [],
        "人工智能": [],
    }
    topic_lower = topic.lower()
    for key, parties in known_parties.items():
        if key.lower() in topic_lower:
            return parties
    return []


def _guess_party(result: Dict[str, Any], parties: List[str]) -> str:
    """根据搜索结果猜测属于哪个参与方"""
    title = (result.get("title", "") + " " + result.get("snippet", "")).lower()
    source = result.get("source_name", "").lower()

    for party in parties:
        party_lower = party.lower()
        if party_lower in title or party_lower in source:
            return party

    return ""


# ============================================================
# 证据模板生成（供AI辅助使用）
# ============================================================


def generate_evidence_template(topic: str, parties: List[str] = None) -> str:
    """生成证据收集JSON模板"""
    template = {
        "topic": topic,
        "search_date": datetime.now().strftime("%Y-%m-%d"),
        "parties": parties or [],
        "evidence": [
            {
                "title": "证据标题",
                "url": "https://...",
                "snippet": "摘要内容（100-300字）",
                "date": "YYYY-MM-DD",
                "source_name": "来源名称（如 GitHub/知乎/arXiv）",
                "party": "归属方（如 华为/OpenAI）",
                "key_claims": ["主张1", "主张2"],
                "notes": "人工备注（可选）",
            }
        ],
    }
    return json.dumps(template, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
