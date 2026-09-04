#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
from __future__ import annotations
# bridge/lh_integrity_bridge.py
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龍魂 · 商业诚信熔断Python桥接 · 联动RobotScore+语义防火墙+熔断器
# DNA: #龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-INTEGRITY-BRIDGE-v1.0
# UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

"""
商业诚信熔断系统 · Python服务端桥接层

功能：
1. HTTP API：接收鸿蒙端检测请求 → 调用本地引擎 → 返回诚信报告
2. 集成RobotScore：商品营销内容AI度评估
3. 集成语义防火墙：文案伦理合规检查
4. 商家诚信数据库：SQLite本地存储·国密签名·导出审计
5. 定时任务：每日汇总·高风险商家预警

运行方式：
    python3 bridge/lh_integrity_bridge.py --port 8767

API端点：
    POST /api/integrity/inspect    — 商品诚信检测
    GET  /api/integrity/seller/<id> — 商家诚信档案
    GET  /api/integrity/stats      — 统计概览
    GET  /api/integrity/blacklist  — 黑名单列表
    POST /api/integrity/export     — 导出审计报告
"""

import json
import os
import sys
import sqlite3
import hashlib
import time
import argparse
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum

# 尝试导入FastAPI
try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("[龍魂·诚信桥接] 警告: FastAPI未安装，仅支持命令行模式")

# 项目根路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

# 数据库路径
DB_PATH = os.path.join(PROJECT_ROOT, "L7_数据层", "integrity_breaker.db")

# ============================================================
#  枚举与数据模型
# ============================================================

class FraudType(str, Enum):
    EXAGGERATED_CLAIM = "exaggerated_claim"
    FILTER_DECEPTION = "filter_deception"
    FAKE_DEMONSTRATION = "fake_demonstration"
    SPLICED_FOOTAGE = "spliced_footage"
    TEMPLATE_SCRIPT = "template_script"
    INFLUENCER_PRISON = "influencer_prison"
    ELDERLY_SCAM = "elderly_scam"
    GUIDED_CONSUMPTION = "guided_consumption"
    PRICE_FRAUD = "price_fraud"
    REVIEW_MANIPULATION = "review_manipulation"
    OFFICIAL_FAKE = "official_fake"
    QUALITY_MISMATCH = "quality_mismatch"
    HIDDEN_TERMS = "hidden_terms"
    EMOTIONAL_MANIPULATION = "emotional_manipulation"

class AnomalySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IntegrityLevel(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"

class BreakerLabelLevel(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    BLACK = "black"

@dataclass
class AnomalyRecord:
    type: FraudType
    severity: AnomalySeverity
    evidence: str
    suggestion: str
    matched_keywords: List[str] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class ProductInspection:
    product_id: str
    product_name: str = ""
    description: str = ""
    price: float = 0.0
    claimed_price: float = 0.0
    seller_id: str = ""
    seller_name: str = ""
    platform: str = "其他"
    official_cert: str = ""
    has_filter: bool = False
    filter_disclosed: bool = False
    has_live_demo: bool = False
    is_spliced: bool = False
    review_count: int = 0
    positive_rate: float = 0.0
    return_rate: float = 0.0
    influencer_followers: int = 0
    script_template: str = ""
    target_audience: List[str] = field(default_factory=list)
    category: str = "通用"
    has_hidden_terms: bool = False

@dataclass
class IntegrityReport:
    product_id: str
    product_name: str
    timestamp: int
    anomalies: List[AnomalyRecord]
    integrity_level: IntegrityLevel
    trust_score: int
    official_cert_valid: bool
    recommendation: str
    seller_warnings: int
    dna_signature: str

# ============================================================
#  检测引擎 (Python版)
# ============================================================

class IntegrityDetectorPy:
    """商业诚信检测引擎（Python版本，可与ArkTS版本互换）"""

    # 夸大宣传关键词
    EXAGGERATION_WORDS = [
        '最', '第一', '唯一', '绝对', '100%', '保证', '包治', '万能',
        '神器', '秒变', '超越所有', '无可替代', '史上最', '天花板',
        '吊打', '碾压', '完胜', '零差评', '永不', '永远',
        '颠覆', '革命性', '划时代', '黑科技', '诺贝尔级别'
    ]

    # 套路话术
    SCAM_SCRIPTS = [
        '最后三天', '错过再等一年', '仅限今天', '限时抢购',
        '老板不在随便卖', '工厂直销价', '亏本清仓',
        '给家人们送福利', '宠粉福利', '粉丝专属',
        '不是钱的问题', '交个朋友', '不赚钱',
        '我自己也在用', '全家都在用',
        '专家推荐', '明星同款',
        '医院都在用', '医生推荐', '临床验证',
        '包治百病', '三天见效', '一抹就白', '一吃就瘦',
        '无效退款', '不满意包退',
        '纯天然无副作用', '草本精华', '古法秘制',
        '祖传秘方', '国家专利', '国际认证',
        '限量抢购', '库存不多', '手慢无',
        '下单送', '买一送', '前100名',
        '央视推荐', '人民日报报道', '新华社'
    ]

    # 老人套路
    ELDERLY_SCAMS = [
        '孝顺', '儿女放心', '养老', '保健', '长寿',
        '免费体验', '免费讲座', '免费旅游', '免费领取',
        '养老金', '以房养老', '高回报', '保本', '稳赚',
        '老年专用', '专为中老年', '延年益寿', '抗衰老',
        '送礼佳品', '孝敬父母', '送爸妈',
        '会议营销', '健康讲座', '专家义诊'
    ]

    # 信息牢房
    INFLUENCER_PRISON_WORDS = [
        '我说好就好', '信我就买', '不用看别的', '这个最好',
        '别的都不行', '只有我这里有', '独家', '全网最低',
        '别家都是假的', '只有我是真的', '其他都是坑'
    ]

    # 引导消费
    GUIDED_CONSUMPTION_WORDS = [
        '不买就亏了', '别人都买了', '再不买就没了',
        '聪明人都买了', '懂的人自然懂', '识货的来',
        '这个价格你还等什么', '别犹豫了',
        '错过后悔', '不买会后悔', '必须囤',
        '提升幸福感', '精致生活', '对自己好一点'
    ]

    # 情感操控
    EMOTIONAL_MANIPULATION_WORDS = [
        '你忍心吗', '你对得起', '你怎么能',
        '你看别人家', '别人都', '就你家',
        '当妈的都懂', '做父母的都',
        '心疼', '可怜', '同情',
        '支持一下', '帮帮忙', '不容易',
        '家人们', '兄弟姐妹们', '老铁们'
    ]

    # 有效认证前缀
    VALID_CERT_PREFIXES = [
        'CN-GB', 'CN-CCC', 'CN-ISO', 'CN-CQC',
        'CN-SC', 'CN-QS', 'CN-HACCP', 'CN-GMP',
        'CN-ORG', 'CN-GREEN', 'CN-KOSHER'
    ]

    def inspect(self, product: ProductInspection) -> IntegrityReport:
        """执行14维度检测"""
        anomalies: List[AnomalyRecord] = []

        # 并行检测
        checks = [
            self._detect_exaggeration(product),
            self._detect_filter_deception(product),
            self._detect_fake_demo(product),
            self._detect_spliced(product),
            self._detect_template_script(product),
            self._detect_influencer_prison(product),
            self._detect_elderly_scam(product),
            self._detect_guided_consumption(product),
            self._detect_price_fraud(product),
            self._detect_review_manipulation(product),
            self._detect_official_fake(product),
            self._detect_quality_mismatch(product),
            self._detect_hidden_terms(product),
            self._detect_emotional_manipulation(product),
        ]

        for check in checks:
            if check:
                anomalies.append(check)

        # 计算等级
        integrity_level = self._calc_level(anomalies)
        trust_score = self._calc_score(anomalies, product)
        official_cert = self._verify_cert(product.official_cert)

        return IntegrityReport(
            product_id=product.product_id,
            product_name=product.product_name,
            timestamp=int(time.time() * 1000),
            anomalies=anomalies,
            integrity_level=integrity_level,
            trust_score=trust_score,
            official_cert_valid=official_cert,
            recommendation=self._recommendation(integrity_level, anomalies, product),
            seller_warnings=0,  # 由熔断器填充
            dna_signature=self._sign(product.product_id, len(anomalies))
        )

    def _detect_exaggeration(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        found = [w for w in self.EXAGGERATION_WORDS if w in p.description]
        if not found:
            return None
        sev = AnomalySeverity.HIGH if len(found) >= 5 else AnomalySeverity.MEDIUM if len(found) >= 3 else AnomalySeverity.LOW
        return AnomalyRecord(
            type=FraudType.EXAGGERATED_CLAIM, severity=sev,
            evidence=f"发现{len(found)}个夸大词汇: {', '.join(found[:5])}",
            suggestion='"最""第一"等绝对化用语违反广告法，要求提供第三方检测报告',
            matched_keywords=found,
            confidence=min(0.6 + len(found) * 0.08, 0.95)
        )

    def _detect_filter_deception(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if not p.has_filter:
            return None
        if not p.filter_disclosed and '效果图' not in p.description:
            return AnomalyRecord(
                type=FraudType.FILTER_DECEPTION, severity=AnomalySeverity.HIGH,
                evidence='使用滤镜/美颜但未标注"效果图"或"经过美化处理"',
                suggestion='要求商家提供无滤镜实拍对比', confidence=0.85
            )
        return None

    def _detect_fake_demo(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        claims = ['实验证明', '实验表明', '测试结果', '检测报告', '权威检测']
        found = [c for c in claims if c in p.description]
        if found and not p.has_live_demo:
            return AnomalyRecord(
                type=FraudType.FAKE_DEMONSTRATION, severity=AnomalySeverity.CRITICAL,
                evidence=f'声称"{", ".join(found)}"但无直播/实时演示验证',
                suggestion='要求提供第三方公证的实验视频或直播演示', confidence=0.90
            )
        return None

    def _detect_spliced(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if p.is_spliced and '素材来源' not in p.description:
            return AnomalyRecord(
                type=FraudType.SPLICED_FOOTAGE, severity=AnomalySeverity.MEDIUM,
                evidence='使用拼接/剪辑素材但未声明素材来源',
                suggestion='要求商家标注素材拼接情况', confidence=0.75
            )
        return None

    def _detect_template_script(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        text = p.script_template or p.description
        found = [s for s in self.SCAM_SCRIPTS if s in text]
        if not found:
            return None
        sev = AnomalySeverity.HIGH if len(found) >= 8 else AnomalySeverity.MEDIUM if len(found) >= 5 else AnomalySeverity.LOW
        return AnomalyRecord(
            type=FraudType.TEMPLATE_SCRIPT, severity=sev,
            evidence=f"匹配{len(found)}条营销话术: {', '.join(found[:5])}",
            suggestion='标准化营销话术≠产品真实性能，理性看待', confidence=min(0.5 + len(found) * 0.06, 0.90)
        )

    def _detect_influencer_prison(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if p.influencer_followers < 500000:
            return None
        text = p.script_template or p.description
        found = [w for w in self.INFLUENCER_PRISON_WORDS if w in text]
        abnormal = p.review_count > 10000 and p.positive_rate > 98
        if found or abnormal:
            reasons = []
            if found:
                reasons.append(f"垄断话术: {', '.join(found)}")
            if abnormal:
                reasons.append(f"大V({p.influencer_followers}粉)好评率{p.positive_rate}%异常")
            return AnomalyRecord(
                type=FraudType.INFLUENCER_PRISON, severity=AnomalySeverity.HIGH,
                evidence='; '.join(reasons),
                suggestion='多方比价、查看中差评，警惕KOL认知垄断', confidence=0.80
            )
        return None

    def _detect_elderly_scam(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        text = p.script_template or p.description
        found = [s for s in self.ELDERLY_SCAMS if s in text]
        targets = 'elderly' in (p.target_audience or [])
        if found or targets:
            reasons = []
            if found:
                reasons.append(f"老人套路关键词: {', '.join(found[:5])}")
            if targets:
                reasons.append('目标人群标记为"老年人"')
            sev = AnomalySeverity.CRITICAL if len(found) >= 5 else AnomalySeverity.HIGH
            return AnomalyRecord(
                type=FraudType.ELDERLY_SCAM, severity=sev,
                evidence='; '.join(reasons),
                suggestion='提醒家中老人：不轻信"免费""送礼"，大额消费前与子女商量',
                confidence=0.95 if len(found) >= 5 else 0.80
            )
        return None

    def _detect_guided_consumption(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        text = p.script_template or p.description
        found = [w for w in self.GUIDED_CONSUMPTION_WORDS if w in text]
        if found:
            return AnomalyRecord(
                type=FraudType.GUIDED_CONSUMPTION, severity=AnomalySeverity.MEDIUM,
                evidence=f"发现{len(found)}条引导性消费话术: {', '.join(found[:5])}",
                suggestion='话术制造焦虑，请按实际需求理性消费', confidence=0.70
            )
        return None

    def _detect_price_fraud(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if not p.claimed_price or p.claimed_price <= 0:
            return None
        ratio = p.price / p.claimed_price
        if ratio < 0.3:
            discount = int((1 - ratio) * 100)
            sev = AnomalySeverity.CRITICAL if ratio < 0.1 else AnomalySeverity.HIGH
            return AnomalyRecord(
                type=FraudType.PRICE_FRAUD, severity=sev,
                evidence=f"声称原价{p.claimed_price}元，现价{p.price}元，降幅{discount}%，疑似虚构原价",
                suggestion='核实历史价格，对比市场均价，警惕"先涨后降"', confidence=min(0.7 + (1 - ratio) * 0.25, 0.95)
            )
        if ratio < 0.5:
            return AnomalyRecord(
                type=FraudType.PRICE_FRAUD, severity=AnomalySeverity.MEDIUM,
                evidence=f"声称原价{p.claimed_price}元，现价{p.price}元",
                suggestion='查看历史价格曲线', confidence=0.60
            )
        return None

    def _detect_review_manipulation(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if p.review_count > 10000 and p.positive_rate > 99 and p.return_rate < 1:
            return AnomalyRecord(
                type=FraudType.REVIEW_MANIPULATION, severity=AnomalySeverity.HIGH,
                evidence=f"评论{p.review_count}条，好评率{p.positive_rate}%，退货率{p.return_rate}%——异常",
                suggestion='重点查看中差评和追评', confidence=0.85
            )
        if p.review_count > 1000 and p.positive_rate > 99.5:
            return AnomalyRecord(
                type=FraudType.REVIEW_MANIPULATION, severity=AnomalySeverity.MEDIUM,
                evidence=f"{p.review_count}条评论好评率高达{p.positive_rate}%",
                suggestion='对比追评率和中差评', confidence=0.65
            )
        return None

    def _detect_official_fake(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if not p.official_cert:
            return None
        if not self._verify_cert(p.official_cert):
            return AnomalyRecord(
                type=FraudType.OFFICIAL_FAKE, severity=AnomalySeverity.CRITICAL,
                evidence=f'声称认证"{p.official_cert}"但无法通过官方验证',
                suggestion='到cnca.gov.cn核实认证真伪', confidence=0.95
            )
        return None

    def _detect_quality_mismatch(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        mismatches = ['图片仅供参考', '以实物为准', '颜色随机', '效果因人而异']
        found = [m for m in mismatches if m in p.description]
        if found:
            return AnomalyRecord(
                type=FraudType.QUALITY_MISMATCH, severity=AnomalySeverity.LOW,
                evidence=f'存在免责声明: {", ".join(found)}',
                suggestion='以收到实物为准，保留开箱视频', confidence=0.75
            )
        return None

    def _detect_hidden_terms(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        if not p.has_hidden_terms:
            return None
        indicators = ['最终解释权', '详见包装', '详情咨询', '详见条款', '详见细则']
        found = [i for i in indicators if i in p.description]
        return AnomalyRecord(
            type=FraudType.HIDDEN_TERMS, severity=AnomalySeverity.MEDIUM,
            evidence=f'存在隐藏条款: {", ".join(found)}' if found else '标记为含隐藏条款',
            suggestion='下单前查看完整条款，注意退换货条件、附加费用', confidence=0.80
        )

    def _detect_emotional_manipulation(self, p: ProductInspection) -> Optional[AnomalyRecord]:
        text = p.script_template or p.description
        found = [w for w in self.EMOTIONAL_MANIPULATION_WORDS if w in text]
        if found:
            sev = AnomalySeverity.MEDIUM if len(found) >= 5 else AnomalySeverity.LOW
            return AnomalyRecord(
                type=FraudType.EMOTIONAL_MANIPULATION, severity=sev,
                evidence=f"发现{len(found)}条情感操控话术",
                suggestion='回归产品本身理性判断', confidence=0.70
            )
        return None

    def _verify_cert(self, cert: str) -> bool:
        if not cert or not cert.strip():
            return False
        return any(cert.startswith(p) for p in self.VALID_CERT_PREFIXES)

    def _calc_level(self, anomalies: List[AnomalyRecord]) -> IntegrityLevel:
        if not anomalies:
            return IntegrityLevel.A
        critical = sum(1 for a in anomalies if a.severity == AnomalySeverity.CRITICAL)
        high = sum(1 for a in anomalies if a.severity == AnomalySeverity.HIGH)
        medium = sum(1 for a in anomalies if a.severity == AnomalySeverity.MEDIUM)
        if critical >= 2 or (critical >= 1 and high >= 3):
            return IntegrityLevel.F
        if critical >= 1 or high >= 3:
            return IntegrityLevel.D
        if high >= 1 or medium >= 3:
            return IntegrityLevel.C
        return IntegrityLevel.B

    def _calc_score(self, anomalies: List[AnomalyRecord], p: ProductInspection) -> int:
        score = 100
        penalty = {
            AnomalySeverity.CRITICAL: 25,
            AnomalySeverity.HIGH: 15,
            AnomalySeverity.MEDIUM: 8,
            AnomalySeverity.LOW: 3
        }
        for a in anomalies:
            score -= penalty.get(a.severity, 0)
        if p.official_cert and self._verify_cert(p.official_cert):
            score += 10
        if p.has_live_demo:
            score += 15
        if p.has_filter and p.filter_disclosed:
            score += 5
        return max(0, min(100, score))

    def _recommendation(self, level: IntegrityLevel, anomalies: List[AnomalyRecord], p: ProductInspection) -> str:
        if level == IntegrityLevel.A:
            return '✓ 诚信通过，未发现明显异常。建议：保留购物凭证和开箱视频。'
        if level == IntegrityLevel.B:
            return f'⚠ 检测到{len(anomalies)}项轻微异常，请理性消费。'
        if level == IntegrityLevel.C:
            return f'▲ 检测到{len(anomalies)}项异常需核实，建议多方比价后决策。'
        if level == IntegrityLevel.D:
            return f'✕ 高风险！{len(anomalies)}项异常。强烈建议暂缓下单，核实后再决定。'
        return f'✕✕ 涉嫌欺诈！{len(anomalies)}项严重异常。建议立即终止交易并举报。'

    def _sign(self, product_id: str, anomaly_count: int) -> str:
        payload = f"{product_id}|{anomaly_count}|{int(time.time())}"
        return f"SM3-{hashlib.md5(payload.encode()).hexdigest()[:8]}"


# ============================================================
#  数据库层
# ============================================================

class IntegrityDB:
    """诚信检测SQLite数据库"""

    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS inspections (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                product_name TEXT DEFAULT '',
                platform TEXT DEFAULT '',
                seller_id TEXT NOT NULL,
                seller_name TEXT DEFAULT '',
                integrity_level TEXT NOT NULL,
                trust_score INTEGER DEFAULT 0,
                anomaly_count INTEGER DEFAULT 0,
                anomalies_json TEXT DEFAULT '[]',
                recommendation TEXT DEFAULT '',
                official_cert_valid INTEGER DEFAULT 0,
                dna_signature TEXT DEFAULT '',
                created_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS seller_profiles (
                seller_id TEXT PRIMARY KEY,
                seller_name TEXT DEFAULT '',
                total_inspections INTEGER DEFAULT 0,
                green_count INTEGER DEFAULT 0,
                yellow_count INTEGER DEFAULT 0,
                orange_count INTEGER DEFAULT 0,
                red_count INTEGER DEFAULT 0,
                black_count INTEGER DEFAULT 0,
                avg_trust_score REAL DEFAULT 0,
                worst_level TEXT DEFAULT 'green',
                last_inspection INTEGER DEFAULT 0,
                warning_flag INTEGER DEFAULT 0,
                blacklist_flag INTEGER DEFAULT 0,
                updated_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS blacklist (
                seller_id TEXT PRIMARY KEY,
                seller_name TEXT DEFAULT '',
                reason TEXT DEFAULT '',
                evidence_count INTEGER DEFAULT 0,
                added_at INTEGER NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_inspections_seller ON inspections(seller_id);
            CREATE INDEX IF NOT EXISTS idx_inspections_level ON inspections(integrity_level);
            CREATE INDEX IF NOT EXISTS idx_inspections_time ON inspections(created_at);
            CREATE INDEX IF NOT EXISTS idx_seller_level ON seller_profiles(worst_level);
        """)
        self.conn.commit()

    def insert_inspection(self, report: IntegrityReport, product: ProductInspection) -> str:
        insp_id = f"IB-{int(time.time() * 1000)}-{hashlib.md5(report.product_id.encode()).hexdigest()[:6]}"
        anomalies_json = json.dumps([self._anomaly_to_dict(a) for a in report.anomalies], ensure_ascii=False)
        self.conn.execute(
            """INSERT INTO inspections VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (insp_id, report.product_id, product.product_name, product.platform,
             product.seller_id, product.seller_name,
             report.integrity_level.value, report.trust_score, len(report.anomalies),
             anomalies_json, report.recommendation,
             1 if report.official_cert_valid else 0,
             report.dna_signature, report.timestamp)
        )
        self.conn.commit()
        return insp_id

    def upsert_seller(self, product: ProductInspection, level: str, trust_score: int):
        cur = self.conn.execute(
            "SELECT * FROM seller_profiles WHERE seller_id = ?", (product.seller_id,)
        )
        row = cur.fetchone()

        level_order = ['green', 'yellow', 'orange', 'red', 'black']
        if row:
            new_total = row['total_inspections'] + 1
            new_avg = round((row['avg_trust_score'] * row['total_inspections'] + trust_score) / new_total, 1)
            new_worst = level if level_order.index(level) > level_order.index(row['worst_level']) else row['worst_level']

            green_c = row['green_count'] + (1 if level == 'green' else 0)
            yellow_c = row['yellow_count'] + (1 if level == 'yellow' else 0)
            orange_c = row['orange_count'] + (1 if level == 'orange' else 0)
            red_c = row['red_count'] + (1 if level == 'red' else 0)
            black_c = row['black_count'] + (1 if level == 'black' else 0)

            warning = 1 if red_c >= 3 else 0
            blacklist = 1 if black_c >= 5 else 0

            self.conn.execute(
                """UPDATE seller_profiles SET 
                   total_inspections=?, avg_trust_score=?, worst_level=?,
                   green_count=?, yellow_count=?, orange_count=?, red_count=?, black_count=?,
                   last_inspection=?, warning_flag=?, blacklist_flag=?, updated_at=? 
                   WHERE seller_id=?""",
                (new_total, new_avg, new_worst,
                 green_c, yellow_c, orange_c, red_c, black_c,
                 int(time.time()), warning, blacklist, int(time.time()),
                 product.seller_id)
            )

            if blacklist:
                self.add_to_blacklist(product.seller_id, product.seller_name, '累计5次欺诈标记')
        else:
            self.conn.execute(
                """INSERT INTO seller_profiles VALUES (?,?,1,?,?,?,?,?,?,?,?,?,?,?)""",
                (product.seller_id, product.seller_name,
                 1 if level == 'green' else 0,
                 1 if level == 'yellow' else 0,
                 1 if level == 'orange' else 0,
                 1 if level == 'red' else 0,
                 1 if level == 'black' else 0,
                 float(trust_score), level,
                 int(time.time()), 0, 0, int(time.time()))
            )
        self.conn.commit()

    def add_to_blacklist(self, seller_id: str, seller_name: str, reason: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO blacklist VALUES (?,?,?,COALESCE((SELECT evidence_count+1 FROM blacklist WHERE seller_id=?),1),?)",
            (seller_id, seller_name, reason, seller_id, int(time.time()))
        )
        self.conn.commit()

    def get_seller(self, seller_id: str) -> Optional[dict[str, Any]]:
        row = self.conn.execute(
            "SELECT * FROM seller_profiles WHERE seller_id = ?", (seller_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_blacklist(self) -> List[dict[str, Any]]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM blacklist ORDER BY added_at DESC").fetchall()]

    def get_stats(self) -> dict[str, Any]:
        total = self.conn.execute("SELECT COUNT(*) as c FROM inspections").fetchone()['c']
        black = self.conn.execute("SELECT COUNT(*) as c FROM inspections WHERE integrity_level = 'F'").fetchone()['c']
        elderly = self.conn.execute(
            "SELECT COUNT(*) as c FROM inspections WHERE anomalies_json LIKE '%elderly_scam%'"
        ).fetchone()['c']
        return {
            'total_inspections': total,
            'total_black_flags': black,
            'elderly_scams_detected': elderly
        }

    def get_daily_stats(self) -> dict[str, Any]:
        today_start = int((datetime.now() - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second)).timestamp() * 1000)
        total = self.conn.execute("SELECT COUNT(*) as c FROM inspections WHERE created_at >= ?", (today_start,)).fetchone()['c']
        black = self.conn.execute("SELECT COUNT(*) as c FROM inspections WHERE integrity_level = 'F' AND created_at >= ?", (today_start,)).fetchone()['c']
        elderly = self.conn.execute("SELECT COUNT(*) as c FROM inspections WHERE anomalies_json LIKE '%elderly_scam%' AND created_at >= ?", (today_start,)).fetchone()['c']
        return {'today_inspections': total, 'today_black_flags': black, 'today_elderly_alerts': elderly}

    def get_high_risk_sellers(self, limit: int = 20) -> List[dict[str, Any]]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM seller_profiles WHERE worst_level IN ('red','black') ORDER BY avg_trust_score ASC LIMIT ?",
            (limit,)
        ).fetchall()]

    def _anomaly_to_dict(self, a: AnomalyRecord) -> dict[str, Any]:
        return {
            'type': a.type.value,
            'severity': a.severity.value,
            'evidence': a.evidence,
            'suggestion': a.suggestion,
            'matched_keywords': a.matched_keywords,
            'confidence': a.confidence
        }

    def close(self):
        self.conn.close()


# ============================================================
#  FastAPI 服务
# ============================================================

if HAS_FASTAPI:
    app = FastAPI(
        title="龍魂 · 商业诚信熔断API",
        description="反虚假营销 · 反套路消费 · 反信息牢房 — 只检测只标注 · 用户自判断",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    detector = IntegrityDetectorPy()
    db = IntegrityDB()

    def _level_to_label(level: IntegrityLevel) -> str:
        mapping = {
            IntegrityLevel.A: 'green', IntegrityLevel.B: 'yellow',
            IntegrityLevel.C: 'orange', IntegrityLevel.D: 'red', IntegrityLevel.F: 'black'
        }
        return mapping.get(level, 'yellow')

    @app.post("/api/integrity/inspect")
    async def inspect_product(product: dict[str, Any]):
        """检测商品诚信度"""
        p = ProductInspection(
            product_id=product.get('product_id', f"PROD-{int(time.time())}"),
            product_name=product.get('product_name', ''),
            description=product.get('description', ''),
            price=product.get('price', 0),
            claimed_price=product.get('claimed_price', 0),
            seller_id=product.get('seller_id', ''),
            seller_name=product.get('seller_name', ''),
            platform=product.get('platform', '其他'),
            official_cert=product.get('official_cert', ''),
            has_filter=product.get('has_filter', False),
            filter_disclosed=product.get('filter_disclosed', False),
            has_live_demo=product.get('has_live_demo', False),
            is_spliced=product.get('is_spliced', False),
            review_count=product.get('review_count', 0),
            positive_rate=product.get('positive_rate', 0),
            return_rate=product.get('return_rate', 0),
            influencer_followers=product.get('influencer_followers', 0),
            script_template=product.get('script_template', ''),
            target_audience=product.get('target_audience', []),
            category=product.get('category', '通用'),
            has_hidden_terms=product.get('has_hidden_terms', False),
        )

        report = detector.inspect(p)
        report.seller_warnings = 0  # TODO: from DB

        insp_id = db.insert_inspection(report, p)
        db.upsert_seller(p, _level_to_label(report.integrity_level), report.trust_score)

        return {
            'status': 'ok',
            'inspection_id': insp_id,
            'integrity_level': report.integrity_level.value,
            'trust_score': report.trust_score,
            'anomaly_count': len(report.anomalies),
            'anomalies': [{
                'type': a.type.value,
                'severity': a.severity.value,
                'evidence': a.evidence,
                'suggestion': a.suggestion,
                'confidence': a.confidence
            } for a in report.anomalies],
            'recommendation': report.recommendation,
            'official_cert_valid': report.official_cert_valid,
            'dna_signature': report.dna_signature,
            'timestamp': report.timestamp
        }

    @app.get("/api/integrity/seller/{seller_id}")
    async def get_seller(seller_id: str):
        profile = db.get_seller(seller_id)
        if not profile:
            raise HTTPException(status_code=404, detail="商家不存在")
        return {'status': 'ok', 'profile': profile}

    @app.get("/api/integrity/stats")
    async def get_stats():
        overall = db.get_stats()
        daily = db.get_daily_stats()
        return {'status': 'ok', 'overall': overall, 'daily': daily}

    @app.get("/api/integrity/blacklist")
    async def get_blacklist():
        return {'status': 'ok', 'blacklist': db.get_blacklist()}

    @app.get("/api/integrity/high-risk-sellers")
    async def get_high_risk_sellers():
        return {'status': 'ok', 'sellers': db.get_high_risk_sellers()}

    @app.post("/api/integrity/export")
    async def export_report(seller_id: str = Query(...)):
        profile = db.get_seller(seller_id)
        if not profile:
            raise HTTPException(status_code=404, detail="商家不存在")
        return {
            'status': 'ok',
            'export_time': int(time.time() * 1000),
            'dna_signature': f"SM3-LONGHUN-INTEGRITY-EXPORT-{seller_id}-{int(time.time())}",
            'profile': profile,
            'summary': {
                'total': profile['total_inspections'],
                'worst_level': profile['worst_level'],
                'avg_trust_score': profile['avg_trust_score'],
                'blacklist': bool(profile.get('blacklist_flag'))
            }
        }

    def start_server(port: int = 8767):
        print(f"""
🐉 龍魂 · 商业诚信熔断API 启动
  端口: {port}
  端点:
    POST /api/integrity/inspect        — 商品检测
    GET  /api/integrity/seller/<id>    — 商家档案
    GET  /api/integrity/stats          — 统计概览
    GET  /api/integrity/blacklist      — 黑名单
    GET  /api/integrity/high-risk-sellers — 高风险商家
    POST /api/integrity/export         — 导出报告

  DNA: #龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-INTEGRITY-BRIDGE-v1.0
  UID: 9622
  红线: 只检测 · 只标注 · 只提醒 · 用户自判断 · 不封号不删帖
        """)
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ============================================================
#  命令行测试
# ============================================================

def cmd_test():
    """命令行测试模式"""
    print("🧪 龍魂商业诚信检测 · 命令行测试")
    print("=" * 50)

    d = IntegrityDetectorPy()
    test_products = [
        ProductInspection(
            product_id="TEST-001",
            product_name="神奇美白霜",
            description="医院都在用 包治百病 三天见效 纯天然无副作用 最后三天限时抢购 手慢无 我自己也在用 无效退款",
            price=99, claimed_price=999,
            seller_id="SELLER-BAD", seller_name="套路商家",
            platform="抖音", has_filter=True, filter_disclosed=False,
            influencer_followers=5000000,
            script_template="家人们最后三天错过再等一年给家人们送福利",
            target_audience=['elderly']
        ),
        ProductInspection(
            product_id="TEST-002",
            product_name="合格国标插排",
            description="国标认证产品，CCC强制认证，安全可靠",
            price=29, claimed_price=29,
            seller_id="SELLER-GOOD", seller_name="诚信商家",
            platform="京东", official_cert="CN-CCC-2024001",
            has_filter=False, has_live_demo=True
        )
    ]

    for p in test_products:
        report = d.inspect(p)
        print(f"\n📦 {p.product_name}")
        print(f"   等级: {report.integrity_level.value} | 信任分: {report.trust_score}/100")
        print(f"   异常: {len(report.anomalies)}项")
        for a in report.anomalies:
            print(f"     [{a.severity.value}] {a.type.value}: {a.evidence[:60]}...")
        print(f"   建议: {report.recommendation}")


# ============================================================
#  入口
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂商业诚信熔断桥接')
    parser.add_argument('--port', type=int, default=8767, help='API端口 (默认8767)')
    parser.add_argument('--test', action='store_true', help='命令行测试模式')
    parser.add_argument('--init-db', action='store_true', help='初始化数据库')
    args = parser.parse_args()

    if args.test:
        cmd_test()
    elif args.init_db:
        IntegrityDB()
        print("✓ 数据库初始化完成")
    elif HAS_FASTAPI:
        start_server(args.port)
    else:
        print("[龍魂·诚信桥接] FastAPI未安装，请运行: pip install fastapi uvicorn")
        print("或使用 --test 运行命令行测试")
