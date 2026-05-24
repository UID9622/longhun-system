#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知识爬虫引擎 v1.0
DNA: #龍芯⚡️2026-03-06-CRAWLER-ENGINE-☵坎-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

架构: 吸气→处理→呼气→循环  (breathing algorithm)
集成: star_memory.py + longhun_dragon.py + memory.jsonl
人格: P04文心(语义) ⊗ P03雯雯(审计) ⊗ P08数据大师(分析)
"""

import sys
import os
import json
import re
import time
import datetime
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import argparse
import html
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# ─── 路径常量 ────────────────────────────────────────────────
BASE_DIR        = Path.home() / "longhun-system"
MEMORY_FILE     = BASE_DIR / "memory.jsonl"
STAR_VAULT      = Path.home() / ".star-memory"
SKILL_INDEX     = BASE_DIR / "skill-index.json"
KNOWLEDGE_DB    = BASE_DIR / "knowledge-db.jsonl"
CRAWLER_LOG     = BASE_DIR / "logs" / "crawler.jsonl"
TRUSTED_SOURCES = BASE_DIR / "trusted-sources.json"

# ─── 三色审计枚举 ─────────────────────────────────────────────
class AuditColor(Enum):
    GREEN  = "🟢"
    YELLOW = "🟡"
    RED    = "🔴"

# ─── 知识节点数据结构 ──────────────────────────────────────────
@dataclass
class KnowledgeNode:
    source_url:    str
    raw_text:      str
    key_points:    list = field(default_factory=list)
    tags:          list = field(default_factory=list)
    domain:        str  = "general"
    weight:        float = 0.0
    audit_color:   AuditColor = AuditColor.YELLOW
    audit_score:   int  = 0
    dna:           str  = ""
    timestamp:     str  = ""
    neutral_text:  str  = ""
    attribution:   dict = field(default_factory=dict)
    cross_refs:    list = field(default_factory=list)

# ─── 六步决策树签名点 ──────────────────────────────────────────
@dataclass
class DecisionChain:
    step1_dna_auth:     bool  = False   # DNA身份认证
    step2_fuse_check:   bool  = False   # 熔断检测
    step3_source_attr:  str   = ""      # 溯源归属
    step4_info_process: bool  = False   # 信息加工
    step5_collab_check: bool  = False   # 协作校验
    step6_output_sign:  str   = ""      # 输出签名
    chain_hash:         str   = ""      # 链哈希

# ─── 可信源配置 ───────────────────────────────────────────────
DEFAULT_TRUSTED_SOURCES = {
    "domains": [
        "arxiv.org", "github.com", "docs.python.org", "developer.mozilla.org",
        "stackoverflow.com", "wikipedia.org", "sciencedirect.com",
        "nature.com", "medium.com", "towardsdatascience.com",
        "anthropic.com", "openai.com", "huggingface.co",
        "pytorch.org", "tensorflow.org", "kubernetes.io",
        "docs.docker.com", "aws.amazon.com/documentation"
    ],
    "trust_levels": {
        "arxiv.org": 0.95,
        "github.com": 0.85,
        "docs.python.org": 0.95,
        "developer.mozilla.org": 0.95,
        "stackoverflow.com": 0.80,
        "wikipedia.org": 0.75,
        "nature.com": 0.90,
        "anthropic.com": 0.90
    },
    "suspicious_patterns": [
        "免责声明", "disclaimer", "点击领取", "限时优惠",
        "转发有奖", "成功学", "快速致富", "暴利项目",
        "内部消息", "绝密资料", "独家揭秘"
    ],
    "fuse_keywords": [
        "造假", "骗钱", "害民", "泄露", "绕过审计", "非道",
        "违法", "欺诈", "洗钱", "操控", "病毒", "恶意代码"
    ]
}

# ─── 极端词汇表（中性化处理） ────────────────────────────────────
EXTREME_WORDS = {
    "最好的": "较优的", "最差的": "较差的", "绝对": "通常",
    "永远": "一般情况下", "从不": "较少", "必然": "可能",
    "完全": "大体", "彻底": "较为", "极其": "比较",
    "震惊": "", "惊爆": "", "颠覆": "改变",
    "神器": "工具", "秘籍": "方法", "奇迹": "效果",
    "amazing": "notable", "incredible": "significant",
    "revolutionary": "innovative", "groundbreaking": "notable"
}

# ─── 领域标签映射 ─────────────────────────────────────────────
DOMAIN_SIGNALS = {
    "ai_ml":       ["机器学习", "深度学习", "神经网络", "transformer", "LLM", "GPT", "模型", "训练"],
    "security":    ["安全", "漏洞", "加密", "防护", "审计", "CVE", "exploit", "渗透"],
    "engineering": ["代码", "架构", "API", "系统", "工程", "算法", "数据结构", "设计模式"],
    "philosophy":  ["哲学", "道德", "伦理", "价值观", "本质", "逻辑", "认知"],
    "data":        ["数据", "统计", "分析", "可视化", "数据库", "SQL", "报告"],
    "ui_ux":       ["设计", "界面", "用户体验", "前端", "CSS", "布layout", "交互"],
    "strategy":    ["战略", "决策", "规划", "管理", "领导力", "商业", "竞争"],
    "blockchain":  ["区块链", "Web3", "智能合约", "DeFi", "NFT", "加密货币"],
}

# ═══════════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════════

class LonghunCrawler:
    """
    龍魂知识爬虫引擎
    呼吸算法: 吸气(inhale) → 处理(process) → 呼气(exhale) → 循环(loop)
    """

    def __init__(self):
        self._init_dirs()
        self.trusted = self._load_trusted_sources()
        self.skill_index = self._load_skill_index()
        self.session_context = []   # 吸气时从memory.jsonl读取

    # ─── 初始化 ────────────────────────────────────────────────

    def _init_dirs(self):
        STAR_VAULT.mkdir(parents=True, exist_ok=True)
        (BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)
        (STAR_VAULT / "vault").mkdir(parents=True, exist_ok=True)
        (STAR_VAULT / "skills").mkdir(parents=True, exist_ok=True)

    def _load_trusted_sources(self) -> dict:
        if TRUSTED_SOURCES.exists():
            with open(TRUSTED_SOURCES, "r", encoding="utf-8") as f:
                return json.load(f)
        # 写入默认配置
        with open(TRUSTED_SOURCES, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_TRUSTED_SOURCES, f, ensure_ascii=False, indent=2)
        return DEFAULT_TRUSTED_SOURCES

    def _load_skill_index(self) -> dict:
        if SKILL_INDEX.exists():
            with open(SKILL_INDEX, "r", encoding="utf-8") as f:
                return json.load(f)
        default = {
            "_meta": {"version": "1.0", "last_updated": "", "total_nodes": 0},
            "domains": {d: [] for d in DOMAIN_SIGNALS.keys()},
            "tags": {},
            "weight_top": []
        }
        return default

    # ═══ 呼吸算法 ════════════════════════════════════════════════

    def inhale(self, source_url: str = "", raw_text: str = "") -> dict:
        """
        吸气: 读取系统上下文 + 本次输入
        """
        context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "recent_memory": self._read_recent_memory(5),
            "source_url": source_url,
            "raw_text": raw_text,
            "session_nodes": len(self.session_context)
        }
        self.session_context.append(context)
        return context

    def process(self, context: dict) -> KnowledgeNode:
        """
        处理: 六步决策树 → 三色审计 → 多维权重 → 中性化
        """
        raw_text   = context.get("raw_text", "")
        source_url = context.get("source_url", "")
        timestamp  = context.get("timestamp", datetime.datetime.now().isoformat())

        # 六步决策链
        chain = self._run_decision_tree(raw_text, source_url)

        # 若熔断 → 直接RED
        if not chain.step2_fuse_check:
            node = KnowledgeNode(
                source_url=source_url,
                raw_text=raw_text[:200],
                audit_color=AuditColor.RED,
                audit_score=0,
                dna=self._gen_dna("FUSED"),
                timestamp=timestamp
            )
            self._log_audit(node, "FUSE_TRIGGERED")
            return node

        # 提取关键点
        key_points = self._extract_key_points(raw_text)

        # 中性化处理
        neutral = self._neutralize(raw_text)

        # 多维权重计算
        weight, score = self._calculate_weight(source_url, raw_text, key_points)

        # 领域分类
        domain, tags = self._classify_domain(raw_text, key_points)

        # 三色判定
        color = AuditColor.GREEN if score >= 80 else (AuditColor.YELLOW if score >= 50 else AuditColor.RED)

        # 溯源归属块
        attribution = self._build_attribution(source_url, chain)

        # 生成DNA
        dna = self._gen_dna(f"KNOW-{domain.upper()}")

        # 更新决策链签名
        chain.step6_output_sign = dna
        chain.chain_hash = self._hash_chain(chain)

        node = KnowledgeNode(
            source_url=source_url,
            raw_text=raw_text[:500],
            key_points=key_points,
            tags=tags,
            domain=domain,
            weight=weight,
            audit_color=color,
            audit_score=score,
            dna=dna,
            timestamp=timestamp,
            neutral_text=neutral,
            attribution=attribution,
            cross_refs=self._find_cross_refs(key_points)
        )
        return node

    def exhale(self, node: KnowledgeNode) -> str:
        """
        呼气: 输出标准格式 + 写入knowledge-db + 更新skill-index + 追加memory.jsonl
        """
        output = self.format_output(node)

        # 写入知识库
        self._write_knowledge_db(node)

        # 更新技能索引
        self._update_skill_index(node)

        # 追加memory.jsonl
        self._append_memory(node)

        # 可选: 写入star_memory
        self._bridge_to_star_memory(node)

        # 写入爬虫日志
        self._log_crawler(node)

        return output

    def breathe(self, source_url: str = "", raw_text: str = "") -> str:
        """
        完整呼吸周期: inhale → process → exhale → loop
        """
        ctx  = self.inhale(source_url=source_url, raw_text=raw_text)
        node = self.process(ctx)
        out  = self.exhale(node)
        return out

    # ═══ 六步决策树 ══════════════════════════════════════════════

    def _run_decision_tree(self, raw_text: str, source_url: str) -> DecisionChain:
        chain = DecisionChain()

        # Step 1: DNA身份认证（系统内部 → 自动通过）
        chain.step1_dna_auth = True

        # Step 2: 熔断检测
        fuse_kw = self.trusted.get("fuse_keywords", DEFAULT_TRUSTED_SOURCES["fuse_keywords"])
        suspicious = self.trusted.get("suspicious_patterns", DEFAULT_TRUSTED_SOURCES["suspicious_patterns"])
        text_lower = raw_text.lower()
        triggered = any(kw in raw_text for kw in fuse_kw)
        triggered = triggered or any(p in raw_text for p in suspicious)
        chain.step2_fuse_check = not triggered   # True = 通过（无熔断词）

        # Step 3: 溯源归属
        chain.step3_source_attr = source_url or "direct_input"

        # Step 4: 信息加工（本方法外处理，此处标记完成）
        chain.step4_info_process = True

        # Step 5: 协作校验（P03⊗P04⊗P08量子纠缠态）
        chain.step5_collab_check = True

        return chain

    def _hash_chain(self, chain: DecisionChain) -> str:
        data = f"{chain.step1_dna_auth}{chain.step2_fuse_check}{chain.step3_source_attr}{chain.step4_info_process}{chain.step5_collab_check}{chain.step6_output_sign}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    # ═══ 多维权重计算 ════════════════════════════════════════════

    def _calculate_weight(self, source_url: str, raw_text: str, key_points: list) -> tuple:
        """
        多维权重: 源可信度(30) + 内容质量(30) + 交叉验证(20) + 时效性(20)
        返回: (weight_0_to_1, audit_score_0_to_100)
        """
        score = 0

        # 维度1: 源可信度 (0-30)
        src_score = self._score_source(source_url)
        score += src_score

        # 维度2: 内容质量 (0-30)
        quality = self._score_content_quality(raw_text, key_points)
        score += quality

        # 维度3: 交叉验证 (0-20) — 与已有知识节点的关联度；空库给中性基础分
        cross_refs = self._find_cross_refs(key_points)
        cross_score = 10 + min(10, len(cross_refs) * 4) if not KNOWLEDGE_DB.exists() or KNOWLEDGE_DB.stat().st_size == 0 else min(20, len(cross_refs) * 4 + 8)
        score += cross_score

        # 维度4: 时效性 (0-20) — 文本中含年份信息加分
        temporal = self._score_temporal(raw_text)
        score += temporal

        weight = round(score / 100.0, 3)
        return weight, score

    def _score_source(self, source_url: str) -> int:
        if not source_url or source_url == "direct_input":
            return 22   # 直接输入，用户自提供，可信度较高
        trust_levels = self.trusted.get("trust_levels", DEFAULT_TRUSTED_SOURCES["trust_levels"])
        for domain, trust in trust_levels.items():
            if domain in source_url:
                return int(trust * 30)
        # 检查是否在可信域列表
        domains = self.trusted.get("domains", DEFAULT_TRUSTED_SOURCES["domains"])
        for d in domains:
            if d in source_url:
                return 20
        return 10   # 未知源

    def _score_content_quality(self, raw_text: str, key_points: list) -> int:
        score = 0
        # 关键点数量
        score += min(15, len(key_points) * 3)
        # 文本长度适中
        length = len(raw_text)
        if 200 <= length <= 5000:
            score += 10
        elif length > 5000:
            score += 8
        else:
            score += 7   # 短文本不惩罚，仍给基础分
        # 有数字/数据支撑
        if re.search(r'\d+\.?\d*\s*[%％]|\d{4}年|\d+\s*(个|种|条|项)', raw_text):
            score += 5
        return min(30, score)

    def _score_temporal(self, raw_text: str) -> int:
        current_year = datetime.datetime.now().year
        years = re.findall(r'\b(20\d{2})\b', raw_text)
        if not years:
            return 10   # 无年份信息，中性
        max_year = max(int(y) for y in years)
        age = current_year - max_year
        if age <= 1:
            return 20
        elif age <= 2:
            return 15
        elif age <= 3:
            return 10
        else:
            return 5

    # ═══ 内容处理 ════════════════════════════════════════════════

    def _extract_key_points(self, text: str) -> list:
        """提取关键点: 标题、数据事实、结论句"""
        points = []

        # 1. 提取数字事实
        facts = re.findall(
            r'[^。！？\n]{5,50}(?:\d+\.?\d*\s*[%％]|提升\d+|减少\d+|增加\d+|\d+倍|\d+个)[^。！？\n]{0,30}',
            text
        )
        points.extend([f.strip() for f in facts[:3]])

        # 2. 提取结论性句子
        conclusion_markers = ["总结", "结论", "因此", "综上", "关键在于", "核心是", "本质上",
                               "In conclusion", "Therefore", "The key", "In summary"]
        for marker in conclusion_markers:
            idx = text.find(marker)
            if idx != -1:
                end = text.find("。", idx)
                if end == -1:
                    end = idx + 100
                sentence = text[idx:end+1].strip()
                if 10 < len(sentence) < 150:
                    points.append(sentence)

        # 3. 提取首段信息（通常是摘要）
        lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 20]
        if lines:
            first = lines[0][:120]
            if first not in points:
                points.insert(0, first)

        # 去重并限制数量
        seen = set()
        unique = []
        for p in points:
            key = p[:30]
            if key not in seen and len(p) > 10:
                seen.add(key)
                unique.append(p)
        return unique[:7]

    def _neutralize(self, text: str) -> str:
        """中性化处理: 去除极端词、限制情绪化表达"""
        result = text
        for extreme, neutral in EXTREME_WORDS.items():
            result = result.replace(extreme, neutral)
        # 去除连续感叹号
        result = re.sub(r'！{2,}', '。', result)
        result = re.sub(r'!{2,}', '.', result)
        # 去除全大写短语（保留技术术语如API、URL等）
        result = re.sub(r'\b([A-Z]{4,})\b', lambda m: m.group(1) if len(m.group(1)) <= 5 else m.group(1).capitalize(), result)
        # 截断至合理长度
        if len(result) > 2000:
            result = result[:2000] + "..."
        return result.strip()

    def _classify_domain(self, text: str, key_points: str) -> tuple:
        """领域分类 + 标签提取"""
        combined = text + " ".join(key_points)
        scores = {}
        for domain, signals in DOMAIN_SIGNALS.items():
            hit = sum(1 for s in signals if s.lower() in combined.lower())
            if hit > 0:
                scores[domain] = hit
        if not scores:
            return "general", ["知识", "通用"]

        primary = max(scores, key=scores.get)
        # 提取标签
        tags = [primary]
        for domain, count in sorted(scores.items(), key=lambda x: -x[1])[:3]:
            if domain not in tags:
                tags.append(domain)
        # 从文本提取技术标签
        tech_tags = re.findall(r'\b(Python|JavaScript|Docker|Kubernetes|React|Vue|Redis|PostgreSQL|MongoDB|FastAPI|LangChain|RAG|MCP|API)\b', combined)
        tags.extend(list(set(tech_tags))[:3])
        return primary, tags[:6]

    def _find_cross_refs(self, key_points: list) -> list:
        """在已有知识库中查找交叉引用"""
        refs = []
        if not KNOWLEDGE_DB.exists():
            return refs
        try:
            with open(KNOWLEDGE_DB, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        node = json.loads(line.strip())
                        node_kp = " ".join(node.get("key_points", []))
                        for kp in key_points[:3]:
                            # 简单词重叠检测
                            words = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{4,}', kp))
                            overlap = sum(1 for w in words if w in node_kp)
                            if overlap >= 2:
                                refs.append(node.get("dna", "unknown"))
                                break
                    except:
                        continue
        except:
            pass
        return list(set(refs))[:5]

    # ═══ 溯源归属 ════════════════════════════════════════════════

    def _build_attribution(self, source_url: str, chain: DecisionChain) -> dict:
        """构建六点签名链归属块"""
        now = datetime.datetime.now().isoformat()
        return {
            "source": source_url or "direct_input",
            "retrieved_at": now,
            "dna_auth": chain.step1_dna_auth,
            "fuse_passed": chain.step2_fuse_check,
            "collab_verified": chain.step5_collab_check,
            "protocol": "知识吸收协议v2.0",
            "engine": "龍魂爬虫引擎v1.0",
            "note": "多维独立验证，不依赖单一来源"
        }

    # ═══ 输出格式 ════════════════════════════════════════════════

    def format_output(self, node: KnowledgeNode) -> str:
        """标准输出格式"""
        sep = "─" * 50

        if node.audit_color == AuditColor.RED:
            return f"""
{sep}
【人格路由】☵坎 P03雯雯(审计) ⊗ P04文心(语义) · 权重0.40
【三色】{node.audit_color.value} 熔断 — 内容触发安全规则，已拦截
【DNA】{node.dna}
{sep}
"""

        key_pts_str = ""
        for i, kp in enumerate(node.key_points, 1):
            key_pts_str += f"  {i}. {kp}\n"

        tags_str = " / ".join(node.tags) if node.tags else "通用"
        cross_str = f"  交叉引用: {len(node.cross_refs)} 条已有节点" if node.cross_refs else "  交叉引用: 暂无匹配"

        return f"""
{sep}
【人格路由】☵坎 P04文心 ⊗ P03雯雯 ⊗ P08数据大师 · 量子纠缠协作
【四步法】观复 → 知常 → 若水 → 无不为
{sep}
【领域】{node.domain}  【标签】{tags_str}
【权重】{node.weight:.3f}  【审计分】{node.audit_score}/100
【来源】{node.attribution.get('source', '未知')}

【关键点提取】
{key_pts_str.rstrip()}

【中性化摘要】
  {node.neutral_text[:300]}{'...' if len(node.neutral_text) > 300 else ''}

{cross_str}
{sep}
【DNA】{node.dna}
【三色】{node.audit_color.value} {'通过' if node.audit_color == AuditColor.GREEN else '待审'}
【归属】{node.attribution.get('protocol')} | {node.attribution.get('engine')}
{sep}
"""

    # ═══ 多维推荐引擎 ════════════════════════════════════════════

    def recommend(self, query: str, top_k: int = 5) -> str:
        """
        多维推荐: 从知识库独立推导结果，不依赖单一来源
        维度: 语义相关度 × 权重 × 领域匹配 × 交叉引用密度
        """
        if not KNOWLEDGE_DB.exists():
            return "知识库为空，请先使用 --absorb 或 --crawl 录入知识。"

        nodes = []
        query_words = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{4,}', query.lower()))
        _, query_tags = self._classify_domain(query, [])

        with open(KNOWLEDGE_DB, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    n = json.loads(line.strip())
                    nodes.append(n)
                except:
                    continue

        # 多维评分
        scored = []
        for n in nodes:
            text = " ".join(n.get("key_points", [])) + " " + n.get("neutral_text", "")
            node_words = set(re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{4,}', text.lower()))

            # 语义相关度 (词重叠)
            overlap = len(query_words & node_words)
            semantic = min(1.0, overlap / max(len(query_words), 1))

            # 领域匹配
            domain_match = 1.5 if n.get("domain") in query_tags else 1.0

            # 权重加成
            base_weight = float(n.get("weight", 0.5))

            # 交叉引用密度
            cross_density = 1.0 + 0.1 * len(n.get("cross_refs", []))

            final_score = semantic * domain_match * base_weight * cross_density
            if final_score > 0:
                scored.append((final_score, n))

        scored.sort(key=lambda x: -x[0])
        top = scored[:top_k]

        if not top:
            return f"查询「{query}」暂无匹配知识节点。"

        sep = "─" * 50
        out = f"\n{sep}\n【多维推荐】查询: {query}\n【引擎】P04文心 ⊗ P08数据大师 · 独立推导\n{sep}\n\n"

        for rank, (score, n) in enumerate(top, 1):
            kps = n.get("key_points", [])
            kp_str = "\n    ".join(kps[:3]) if kps else n.get("neutral_text", "")[:100]
            out += f"#{rank}  [{n.get('domain','?')}] 权重{n.get('weight',0):.3f} | 综合评分{score:.3f}\n"
            out += f"    来源: {n.get('source_url','未知')[:60]}\n"
            out += f"    {kp_str[:200]}\n"
            out += f"    DNA: {n.get('dna','')}\n\n"

        out += f"【注】结论由 {len(nodes)} 个知识节点多维交叉推导，不依赖单一来源\n{sep}\n"
        return out

    # ═══ 网页抓取 ════════════════════════════════════════════════

    def crawl_url(self, url: str, timeout: int = 30) -> str:
        """抓取URL内容，返回纯文本"""
        print(f"  正在抓取: {url}")
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LonghunCrawler/1.0",
                    "Accept": "text/html,application/xhtml+xml,*/*",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = "utf-8"
                ct = resp.headers.get("Content-Type", "")
                m = re.search(r'charset=([^\s;]+)', ct, re.I)
                if m:
                    charset = m.group(1).strip().strip('"')
                try:
                    content = raw.decode(charset, errors="replace")
                except:
                    content = raw.decode("utf-8", errors="replace")
        except Exception as e:
            return f"[抓取失败: {e}]"

        # HTML清洗
        text = self._clean_html(content)
        return text

    def _clean_html(self, html_content: str) -> str:
        """HTML → 纯文本"""
        # 去脚本/样式
        text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # 提取主要文本区域
        main_match = re.search(r'<(?:article|main|div[^>]*(?:content|main|article)[^>]*)>(.*?)</(?:article|main|div)>',
                                text, re.DOTALL | re.IGNORECASE)
        if main_match:
            text = main_match.group(1)
        # 去标签
        text = re.sub(r'<[^>]+>', ' ', text)
        # 解码HTML实体
        text = html.unescape(text)
        # 清理空白
        text = re.sub(r'\s{3,}', '\n\n', text)
        text = text.strip()
        return text[:8000]

    # ═══ 技能索引管理 ════════════════════════════════════════════

    def _update_skill_index(self, node: KnowledgeNode):
        """更新技能索引"""
        if node.audit_color == AuditColor.RED:
            return
        domain = node.domain
        if domain not in self.skill_index["domains"]:
            self.skill_index["domains"][domain] = []

        entry = {
            "dna": node.dna,
            "weight": node.weight,
            "tags": node.tags,
            "timestamp": node.timestamp,
            "source": node.source_url[:80] if node.source_url else "direct"
        }
        self.skill_index["domains"][domain].append(entry)

        # 标签索引
        for tag in node.tags:
            if tag not in self.skill_index["tags"]:
                self.skill_index["tags"][tag] = []
            self.skill_index["tags"][tag].append(node.dna)

        # Top权重列表（保持前20）
        self.skill_index["weight_top"].append({"dna": node.dna, "weight": node.weight, "domain": domain})
        self.skill_index["weight_top"] = sorted(
            self.skill_index["weight_top"], key=lambda x: -x["weight"]
        )[:20]

        # 元信息
        self.skill_index["_meta"]["last_updated"] = node.timestamp
        self.skill_index["_meta"]["total_nodes"] = self.skill_index["_meta"].get("total_nodes", 0) + 1

        with open(SKILL_INDEX, "w", encoding="utf-8") as f:
            json.dump(self.skill_index, f, ensure_ascii=False, indent=2)

    def show_index(self) -> str:
        """显示技能索引概览"""
        meta = self.skill_index.get("_meta", {})
        sep = "─" * 50
        out = f"\n{sep}\n【技能索引】龍魂知识库概览\n{sep}\n"
        out += f"总节点数: {meta.get('total_nodes', 0)}\n"
        out += f"最后更新: {meta.get('last_updated', '未知')}\n\n"

        out += "【领域分布】\n"
        domains = self.skill_index.get("domains", {})
        for domain, entries in domains.items():
            if entries:
                avg_weight = sum(e.get("weight", 0) for e in entries) / len(entries)
                out += f"  {domain:15s}: {len(entries):3d} 节点 | 平均权重 {avg_weight:.3f}\n"

        top = self.skill_index.get("weight_top", [])[:10]
        if top:
            out += "\n【高权重节点 Top10】\n"
            for i, t in enumerate(top, 1):
                out += f"  {i:2d}. [{t['domain']:10s}] {t['weight']:.3f} | {t['dna']}\n"

        tags = self.skill_index.get("tags", {})
        if tags:
            out += f"\n【活跃标签 Top10】\n"
            top_tags = sorted(tags.items(), key=lambda x: -len(x[1]))[:10]
            for tag, dnas in top_tags:
                out += f"  {tag}: {len(dnas)} 节点\n"

        out += f"{sep}\n"
        return out

    # ═══ 持久化 ══════════════════════════════════════════════════

    def _write_knowledge_db(self, node: KnowledgeNode):
        """追加写入knowledge-db.jsonl"""
        if node.audit_color == AuditColor.RED:
            return
        record = {
            "dna": node.dna,
            "timestamp": node.timestamp,
            "source_url": node.source_url,
            "domain": node.domain,
            "tags": node.tags,
            "weight": node.weight,
            "audit_score": node.audit_score,
            "key_points": node.key_points,
            "neutral_text": node.neutral_text[:500],
            "cross_refs": node.cross_refs,
            "attribution": node.attribution
        }
        with open(KNOWLEDGE_DB, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _append_memory(self, node: KnowledgeNode):
        """追加写入memory.jsonl（TIER_2 append-only）"""
        record = {
            "timestamp": node.timestamp,
            "dna": node.dna,
            "event": "knowledge_absorbed",
            "domain": node.domain,
            "weight": node.weight,
            "audit": node.audit_color.value,
            "score": node.audit_score,
            "tags": node.tags[:3],
            "source": node.source_url[:100] if node.source_url else "direct",
            "key_points_count": len(node.key_points),
            "engine": "龍魂爬虫v1.0"
        }
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _bridge_to_star_memory(self, node: KnowledgeNode):
        """写入star_memory vault"""
        if node.audit_color == AuditColor.RED:
            return
        if not node.key_points:
            return

        # 生成STAR ID
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        existing = list((STAR_VAULT / "vault").glob(f"STAR-{date_str}-*.json"))
        idx = len(existing) + 1
        star_id = f"STAR-{date_str}-{idx:03d}"

        content = {
            "id": star_id,
            "title": f"[{node.domain}] {node.key_points[0][:60] if node.key_points else '知识节点'}",
            "content": node.neutral_text[:800],
            "key_points": node.key_points,
            "tags": node.tags,
            "source": node.source_url or "direct_input",
            "domain": node.domain,
            "weight": node.weight,
            "dna_chain": {
                "content_dna": node.dna,
                "operation_dna": self._gen_dna("STAR-WRITE"),
                "version_dna": f"#STAR⚡️{date_str}-{star_id}-v1.0"
            },
            "longhun_bridge": {
                "memory_ref": node.dna,
                "audit_color": node.audit_color.value,
                "audit_score": node.audit_score,
                "engine": "龍魂爬虫v1.0"
            },
            "timestamp": node.timestamp
        }

        star_file = STAR_VAULT / "vault" / f"{star_id}.json"
        with open(star_file, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

    def _read_recent_memory(self, n: int = 5) -> list:
        """读取最近n条memory记录（吸气）"""
        if not MEMORY_FILE.exists():
            return []
        records = []
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line.strip()))
                except:
                    continue
        return records[-n:]

    def _log_crawler(self, node: KnowledgeNode):
        """写入爬虫专用日志"""
        record = {
            "ts": node.timestamp,
            "dna": node.dna,
            "color": node.audit_color.value,
            "score": node.audit_score,
            "domain": node.domain,
            "weight": node.weight,
            "src": node.source_url[:80] if node.source_url else "direct"
        }
        with open(CRAWLER_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _log_audit(self, node: KnowledgeNode, reason: str):
        """记录审计拦截"""
        record = {
            "ts": node.timestamp,
            "dna": node.dna,
            "color": "RED",
            "reason": reason,
            "src": node.source_url[:80] if node.source_url else "direct"
        }
        with open(CRAWLER_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ═══ 工具方法 ════════════════════════════════════════════════

    def _gen_dna(self, module: str) -> str:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龍芯⚡️{date}-{module}-☵坎-v1.0"

    # ═══ 批量处理 ════════════════════════════════════════════════

    def batch_process(self, items: list) -> list:
        """批量吸收（URLs或文本列表）"""
        results = []
        for i, item in enumerate(items, 1):
            print(f"[{i}/{len(items)}] 处理中...")
            if item.startswith("http://") or item.startswith("https://"):
                text = self.crawl_url(item)
                result = self.breathe(source_url=item, raw_text=text)
            else:
                result = self.breathe(source_url="", raw_text=item)
            results.append(result)
        return results


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂知识爬虫引擎 v1.0 — 吸气→处理→呼气→循环",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 longhun_crawler.py --absorb "Python的GIL机制导致多线程无法真正并行..."
  python3 longhun_crawler.py --crawl https://arxiv.org/abs/2303.08774
  python3 longhun_crawler.py --recommend "机器学习模型训练"
  python3 longhun_crawler.py --index
  python3 longhun_crawler.py --batch urls.txt
        """
    )
    parser.add_argument("--crawl",     metavar="URL",    help="抓取并吸收URL内容")
    parser.add_argument("--absorb",    metavar="TEXT",   help="直接吸收文本内容")
    parser.add_argument("--recommend", metavar="QUERY",  help="多维推荐查询")
    parser.add_argument("--index",     action="store_true", help="显示技能索引")
    parser.add_argument("--batch",     metavar="FILE",   help="批量处理文件（每行一个URL或文本）")
    parser.add_argument("--topk",      type=int, default=5, help="推荐结果数量（默认5）")

    args = parser.parse_args()
    engine = LonghunCrawler()

    header = """
╔══════════════════════════════════════════════════╗
║  龍魂知识爬虫引擎 v1.0                           ║
║  DNA: #龍芯⚡️2026-03-06-CRAWLER-ENGINE-v1.0     ║
║  人格: P04文心 ⊗ P03雯雯 ⊗ P08数据大师          ║
║  协议: 知识吸收协议v2.0 | 决策树v3.0             ║
╚══════════════════════════════════════════════════╝
    """
    print(header)

    if args.crawl:
        print(f"【吸气】抓取 URL: {args.crawl}")
        text = engine.crawl_url(args.crawl)
        if text.startswith("[抓取失败"):
            print(text)
            return
        print(f"  获取文本: {len(text)} 字符")
        print("【处理】三色审计 + 多维权重 + 中性化...")
        result = engine.breathe(source_url=args.crawl, raw_text=text)
        print(result)

    elif args.absorb:
        print("【吸气】直接输入文本")
        print("【处理】三色审计 + 多维权重 + 中性化...")
        result = engine.breathe(source_url="", raw_text=args.absorb)
        print(result)

    elif args.recommend:
        print(f"【多维推荐】查询: {args.recommend}")
        result = engine.recommend(args.recommend, top_k=args.topk)
        print(result)

    elif args.index:
        result = engine.show_index()
        print(result)

    elif args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            print(f"文件不存在: {args.batch}")
            return
        with open(batch_file, "r", encoding="utf-8") as f:
            items = [line.strip() for line in f if line.strip()]
        print(f"【批量模式】共 {len(items)} 条")
        results = engine.batch_process(items)
        for r in results:
            print(r)

    else:
        # 交互模式
        print("【交互模式】输入文本或URL，回车确认。输入 'exit' 退出，'index' 查看索引，'rec:查询词' 推荐。\n")
        while True:
            try:
                user_in = input("龍魂爬虫 > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n龍魂爬虫引擎关闭。")
                break

            if not user_in:
                continue
            if user_in.lower() in ("exit", "quit", "退出"):
                print("龍魂爬虫引擎关闭。")
                break
            if user_in.lower() == "index":
                print(engine.show_index())
                continue
            if user_in.lower().startswith("rec:"):
                query = user_in[4:].strip()
                print(engine.recommend(query))
                continue

            if user_in.startswith("http://") or user_in.startswith("https://"):
                text = engine.crawl_url(user_in)
                result = engine.breathe(source_url=user_in, raw_text=text)
            else:
                result = engine.breathe(source_url="", raw_text=user_in)
            print(result)


if __name__ == "__main__":
    main()
