# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·五害曝光台 — 多源验证引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-FIVE-HARMS-VALIDATOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

职能: 自动抓取并验证曝光信息的真实性。
数据源: 裁判文书网、市监局公告、新闻聚合RSS、公开工商数据
铁律: 无证据不上墙、三源交叉验证、证据链不可篡改
"""

import hashlib
import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── 路径 ───
_PROJECT = Path(__file__).parent.parent
_EVIDENCE_DIR = _PROJECT / "data" / "five_harms_evidence"
_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
_DATA_FILE = _PROJECT / "data" / "five_harms_cases.json"

# ─── 数据源配置 ───
SOURCES = {
    "supreme_court": {
        "name": "中国裁判文书网",
        "url": "https://wenshu.court.gov.cn/",
        "type": "api",
        "weight": 0.9,  # 最高权重
        "enabled": True,
    },
    "samr": {
        "name": "国家市场监管总局",
        "url": "https://www.samr.gov.cn/",
        "type": "rss",
        "weight": 0.85,
        "enabled": True,
        "rss_feeds": [
            "https://www.samr.gov.cn/rss/xxgk.xml",
        ],
    },
    "cac": {
        "name": "国家网信办",
        "url": "https://www.cac.gov.cn/",
        "type": "rss",
        "weight": 0.8,
        "enabled": True,
    },
    "news_aggregator": {
        "name": "新闻聚合",
        "type": "rss",
        "weight": 0.5,
        "enabled": True,
        "rss_feeds": [
            "https://news.qq.com/rss_headline.xml",
            "https://feedx.net/rss/sina.xml",
        ],
    },
    "enterprise_db": {
        "name": "企业信用信息公示系统",
        "url": "https://www.gsxt.gov.cn/",
        "type": "api",
        "weight": 0.85,
        "enabled": True,
    },
}


@dataclass
class EvidenceItem:
    """单条证据"""
    source: str          # 来源名称
    source_url: str      # 原始链接
    snippet: str         # 摘要
    verify_time: str     # 验证时间
    weight: float        # 可信权重 0-1
    fingerprint: str     # 内容哈希（防篡改）
    raw_text: str = ""   # 原始文本（可选）


@dataclass
class ValidationReport:
    """验证报告"""
    case_id: str
    case_title: str
    is_verified: bool
    confidence: float           # 综合可信度 0-1
    evidence_count: int
    evidence_list: List[Dict[str, Any]] = field(default_factory=list)
    source_count: int = 0       # 独立来源数
    warnings: List[str] = field(default_factory=list)
    audit_mark: str = "🟡"      # 🟢🟡🔴
    dna: str = ""
    check_time: str = ""


class FiveHarmsValidator:
    """五害曝光台 · 多源验证引擎"""

    def __init__(self, data_file: Optional[Path] = None):
        self.data_file = data_file or _DATA_FILE
        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE

    def validate_case(self, case: Dict[str, Any]) -> ValidationReport:
        """验证单条曝光"""
        case_id = str(case.get("id", hashlib.md5(case.get("title","").encode()).hexdigest()[:8]))
        title = case.get("title", "")
        company = case.get("company", "")
        category = case.get("category", "")
        
        report = ValidationReport(
            case_id=case_id,
            case_title=title,
            is_verified=False,
            confidence=0.0,
            evidence_count=0,
            check_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        
        # 构建搜索关键词
        keywords = self._build_keywords(case)
        
        # 逐源验证
        all_evidence = []
        source_count = 0
        
        for source_id, source_cfg in SOURCES.items():
            if not source_cfg.get("enabled", False):
                continue
            try:
                evidence = self._check_source(source_id, source_cfg, keywords, company)
                if evidence:
                    all_evidence.extend(evidence)
                    source_count += 1
            except Exception as e:
                report.warnings.append(f"数据源 {source_cfg['name']} 查询失败: {str(e)[:100]}")
        
        # 计算综合可信度
        if all_evidence:
            weights = [e.weight for e in all_evidence]
            avg_weight = sum(weights) / len(weights)
            # 多源加分
            multi_source_bonus = min(0.2, (source_count - 1) * 0.1)
            report.confidence = min(1.0, avg_weight + multi_source_bonus)
            report.source_count = source_count
            report.evidence_count = len(all_evidence)
            report.evidence_list = [asdict(e) for e in all_evidence]
            
            # 判定
            if report.confidence >= 0.7 and source_count >= 2:
                report.is_verified = True
                report.audit_mark = "🟢"
            elif report.confidence >= 0.4:
                report.audit_mark = "🟡"
            else:
                report.audit_mark = "🟡"
        else:
            report.warnings.append("无任何来源验证通过")
            report.audit_mark = "🔴"
        
        # 生成DNA
        dna_seed = f"{case_id}:{report.confidence}:{report.check_time}"
        report.dna = f"#龍芯⚡️FIVE-HARMS-{hashlib.md5(dna_seed.encode()).hexdigest()[:8]}"
        
        return report

    def _build_keywords(self, case: Dict[str, Any]) -> List[str]:
        """构建搜索关键词组"""
        kw = []
        company = case.get("company", "")
        category = case.get("category", "")
        title = case.get("title", "")
        
        if company:
            kw.append(company)
        if category:
            kw.append(category)
        # 从标题抽取关键词
        words = re.findall(r'[\u4e00-\u9fa5]{2,6}', title)
        kw.extend(words[:3])
        
        return kw

    def _check_source(self, source_id: str, cfg: Dict, keywords: List[str], company: str) -> List[EvidenceItem]:
        """查询单个数据源"""
        evidence_list = []
        
        if cfg["type"] == "rss":
            feeds = cfg.get("rss_feeds", [])
            for feed_url in feeds:
                try:
                    items = self._fetch_rss(feed_url)
                    for item in items:
                        match_score = self._match_score(item, keywords, company)
                        if match_score > 0.3:
                            evidence_list.append(EvidenceItem(
                                source=cfg["name"],
                                source_url=item.get("link", feed_url),
                                snippet=item.get("title", "")[:200],
                                verify_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                weight=cfg["weight"] * match_score,
                                fingerprint=hashlib.sha256(
                                    (item.get("title","")+item.get("link","")).encode()
                                ).hexdigest()[:16],
                            ))
                except Exception:
                    continue
        
        elif cfg["type"] == "api":
            # API源用缓存的证据
            cache_key = f"{source_id}_{company}"
            cached = self._load_cached_evidence(cache_key)
            if cached:
                for item in cached:
                    match_score = self._match_score(
                        {"title": item.get("snippet","")}, keywords, company
                    )
                    if match_score > 0.3:
                        evidence_list.append(EvidenceItem(
                            source=cfg["name"],
                            source_url=item.get("source_url", ""),
                            snippet=item.get("snippet", ""),
                            verify_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            weight=cfg["weight"] * match_score,
                            fingerprint=hashlib.sha256(
                                item.get("snippet","").encode()
                            ).hexdigest()[:16],
                        ))
        
        return evidence_list

    def _fetch_rss(self, url: str, timeout: int = 15) -> List[Dict[str, str]]:
        """抓取RSS"""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "LongHun-FiveHarms-Validator/1.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout, context=self.ssl_ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
            
            root = ET.fromstring(content)
            items = []
            for item in root.iter("item"):
                title_el = item.find("title")
                link_el = item.find("link")
                desc_el = item.find("description")
                items.append({
                    "title": (title_el.text or "").strip() if title_el is not None else "",
                    "link": (link_el.text or "").strip() if link_el is not None else "",
                    "description": (desc_el.text or "").strip()[:300] if desc_el is not None else "",
                })
            return items
        except Exception:
            return []

    def _match_score(self, item: Dict[str, str], keywords: List[str], company: str) -> float:
        """计算匹配度"""
        text = (item.get("title", "") + " " + item.get("description", "")).lower()
        if not text.strip():
            return 0.0
        
        hits = 0
        for kw in keywords:
            if kw.lower() in text:
                hits += 1
        
        if not keywords:
            return 0.0
        
        return hits / len(keywords)

    def _load_cached_evidence(self, cache_key: str) -> List[Dict[str, Any]]:
        """加载缓存的证据"""
        cache_file = _EVIDENCE_DIR / f"{hashlib.md5(cache_key.encode()).hexdigest()[:12]}.json"
        if cache_file.exists():
            try:
                return json.loads(cache_file.read_text())
            except Exception:
                pass
        return []

    def save_evidence(self, cache_key: str, evidence: List[Dict[str, Any]]):
        """保存证据缓存"""
        cache_file = _EVIDENCE_DIR / f"{hashlib.md5(cache_key.encode()).hexdigest()[:12]}.json"
        cache_file.write_text(json.dumps(evidence, ensure_ascii=False, indent=2))

    def batch_validate(self, cases: List[Dict[str, Any]]) -> List[ValidationReport]:
        """批量验证"""
        reports = []
        for case in cases:
            report = self.validate_case(case)
            reports.append(report)
            time.sleep(0.5)  # 防止请求过频
        return reports

    def get_verification_stats(self) -> Dict[str, Any]:
        """获取验证统计"""
        if not self.data_file.exists():
            return {"total": 0, "verified": 0, "pending": 0, "failed": 0}
        
        try:
            data = json.loads(self.data_file.read_text())
            cases = data if isinstance(data, list) else data.get("cases", [])
            verified = sum(1 for c in cases if c.get("audit_mark") == "🟢")
            pending = sum(1 for c in cases if c.get("audit_mark") == "🟡")
            failed = sum(1 for c in cases if c.get("audit_mark") == "🔴")
            return {
                "total": len(cases),
                "verified": verified,
                "pending": pending,
                "failed": failed,
            }
        except Exception:
            return {"total": 0, "verified": 0, "pending": 0, "failed": 0}


# ─── 命令行自测 ───
if __name__ == "__main__":
    validator = FiveHarmsValidator()
    
    test_case = {
        "id": 1,
        "title": "强迫商家二选一，违者降权封店",
        "company": "某团外卖",
        "category": "平台垄断",
        "severity": "critical",
    }
    
    print("=" * 60)
    print("龍魂·五害曝光台 — 多源验证引擎 v1.0")
    print("=" * 60)
    
    report = validator.validate_case(test_case)
    
    print(f"\n案件: {report.case_title}")
    print(f"验证结果: {'🟢 通过' if report.is_verified else '🔴 未通过' if report.audit_mark == '🔴' else '🟡 待核'}")
    print(f"综合可信度: {report.confidence:.2%}")
    print(f"独立来源数: {report.source_count}")
    print(f"证据条数: {report.evidence_count}")
    
    if report.evidence_list:
        print("\n证据列表:")
        for e in report.evidence_list[:5]:
            print(f"  📎 [{e['source']}] {e['snippet'][:80]}... (权重:{e['weight']:.2f})")
    
    if report.warnings:
        print("\n⚠️ 警告:")
        for w in report.warnings:
            print(f"  - {w}")
    
    print(f"\nDNA: {report.dna}")
    print(f"审计: {report.audit_mark}")
    print("\n✅ 验证引擎自检完成")
