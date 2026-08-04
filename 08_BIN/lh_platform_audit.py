#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂一键审计工具 v1.0
平台规则 vs 华夏法则 · 不对称战争审计引擎

DNA: #龍芯⚡️丙午·丙申·己酉·卯时·䷐随-AUDIT-ENGINE-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  1. 粘贴平台用户协议/隐私政策 → 自动审计
  2. 五维博弈矩阵分析（军事·历史·哲学·经济·政治）
  3. 三色判定输出（🟢🟡🔴）
  4. 违规条款定位 + 华夏法则对照
  5. ROOT_CARD生成
  6. 一键导出审计报告

用法:
  python3 bin/lh_platform_audit.py --file agreement.txt
  python3 bin/lh_platform_audit.py --text "粘贴协议内容"
  python3 bin/lh_platform_audit.py --url "https://xxx.com/privacy"
  python3 bin/lh_platform_audit.py --interactive
  lh pa --file agreement.txt
  lh pa --interactive
"""

import os
import sys
import json
import re
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 固定锚点
# ============================================================

DNA = "#龍芯⚡️丙午·丙申·己酉·卯时·䷐随-AUDIT-ENGINE-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 华夏法则条款库
# ============================================================

@dataclass
class LawClause:
    """华夏法则条款"""
    id: str
    name: str
    law: str
    article: str
    content: str
    level: str  # 宪法/法律/法规/部门规章

LAW_DATABASE = [
    LawClause(
        id="L001",
        name="公平交易权",
        law="消费者权益保护法",
        article="第10条",
        content="消费者享有公平交易的权利。消费者在购买商品或者接受服务时，有权获得质量保障、价格合理、计量正确等公平交易条件，有权拒绝经营者的强制交易行为。",
        level="法律"
    ),
    LawClause(
        id="L002",
        name="知情权",
        law="消费者权益保护法",
        article="第8条",
        content="消费者享有知悉其购买、使用的商品或者接受的服务的真实情况的权利。",
        level="法律"
    ),
    LawClause(
        id="L003",
        name="个人信息最小必要原则",
        law="个人信息保护法",
        article="第13条",
        content="处理个人信息应当具有明确、合理的目的，并应当与处理目的直接相关，采取对个人权益影响最小的方式。收集个人信息，应当限于实现处理目的的最小范围。",
        level="法律"
    ),
    LawClause(
        id="L004",
        name="个人信息告知义务",
        law="个人信息保护法",
        article="第17条",
        content="个人信息处理者在处理个人信息前，应当以显著方式、清晰易懂的语言真实、准确、完整地向个人告知个人信息处理者的名称和联系方式、个人信息的处理目的和处理方式、处理的个人信息种类和保存期限。",
        level="法律"
    ),
    LawClause(
        id="L005",
        name="格式条款无效",
        law="民法典",
        article="第497条",
        content="提供格式条款一方不合理地免除或者减轻其责任、加重对方责任、限制对方主要权利的，该格式条款无效。",
        level="法律"
    ),
    LawClause(
        id="L006",
        name="格式条款解释规则",
        law="民法典",
        article="第498条",
        content="对格式条款的理解发生争议的，应当按照通常理解予以解释。对格式条款有两种以上解释的，应当作出不利于提供格式条款一方的解释。",
        level="法律"
    ),
    LawClause(
        id="L007",
        name="算法推荐管理",
        law="互联网信息服务算法推荐管理规定",
        article="第9条",
        content="算法推荐服务提供者应当加强信息安全管理，建立健全用于识别违法和不良信息的特征库，完善入库标准、规则和程序。",
        level="部门规章"
    ),
    LawClause(
        id="L008",
        name="平台规则监督",
        law="网络交易平台规则监督管理办法",
        article="2026年",
        content="平台对商家采取降权、封号等限制措施，必须提前告知且有充分理由；无故封号或不提供申诉渠道的行为，构成违法。",
        level="部门规章"
    ),
    LawClause(
        id="L009",
        name="隐私政策合规",
        law="App违法违规收集使用个人信息行为认定方法",
        article="第1条",
        content="未以显著方式向用户明示收集使用个人信息的目的、方式、范围，或未经用户同意收集使用个人信息，均属违规行为。",
        level="部门规章"
    ),
    LawClause(
        id="L010",
        name="数据安全最小化",
        law="数据安全法",
        article="第27条",
        content="开展数据处理活动应当依照法律、法规的规定，建立健全全流程数据安全管理制度，采取相应的技术措施和其他必要措施，保障数据安全。",
        level="法律"
    ),
    LawClause(
        id="L011",
        name="合同公平原则",
        law="民法典",
        article="第496条",
        content="格式条款是当事人为了重复使用而预先拟定，并在订立合同时未与对方协商的条款。提供格式条款的一方应当遵循公平原则确定当事人之间的权利和义务。",
        level="法律"
    ),
    LawClause(
        id="L012",
        name="数据跨境传输管控",
        law="个人信息保护法",
        article="第38条",
        content="个人信息处理者因业务等需要，确需向中华人民共和国境外提供个人信息的，应当通过国家网信部门组织的安全评估，或者按照国家网信部门的规定经专业机构进行个人信息保护认证。",
        level="法律"
    ),
]

# ============================================================
# 违规模式库
# ============================================================

@dataclass
class ViolationPattern:
    """违规模式"""
    id: str
    name: str
    keywords: List[str]
    law_refs: List[str]
    severity: str  # CRITICAL/HIGH/MEDIUM/LOW
    description: str
    typical_case: str
    category: str  # 违规类型分类

VIOLATION_PATTERNS = [
    ViolationPattern(
        id="V001",
        name="单方修改/解释权",
        keywords=["最终解释权", "单方修改", "有权变更", "随时调整", "无需另行通知", "继续使用即表示"],
        law_refs=["L005", "L006", "L011"],
        severity="HIGH",
        description="平台拥有单方修改协议和最终解释权，剥夺用户的协商权利。违反民法典第496、497、498条。",
        typical_case="大麦网'一经售出概不退换'、BOSS直聘'未经沟通直接封号'",
        category="power_abuse"
    ),
    ViolationPattern(
        id="V002",
        name="过度收集个人信息",
        keywords=["读取相册", "位置信息", "通讯录", "IMEI", "后台读取", "跨APP", "设备信息", "浏览记录"],
        law_refs=["L003", "L004", "L009"],
        severity="CRITICAL",
        description="收集与服务无关的个人信息，或后台频繁读取，违反最小必要原则。个人信息保护法第13条明确要求最小范围。",
        typical_case="淘宝APP每分钟读取用户相册3次，跨APP追踪设备信息",
        category="privacy"
    ),
    ViolationPattern(
        id="V003",
        name="默认勾选/一揽子授权",
        keywords=["默认同意", "自动勾选", "一揽子授权", "视为同意", "继续使用即表示", "无需单独授权"],
        law_refs=["L004", "L009"],
        severity="HIGH",
        description="默认勾选同意或一揽子授权，剥夺用户的知情选择和拒绝权。最高法2025年7月典型案例已明确判罚。",
        typical_case="某词典APP自动为用户勾选同意隐私政策·被判侵权",
        category="consent"
    ),
    ViolationPattern(
        id="V004",
        name="封号/降权无正当程序",
        keywords=["封号", "限制", "停用", "冻结", "违规", "滥用", "申诉", "不予恢复"],
        law_refs=["L008", "L005"],
        severity="CRITICAL",
        description="平台单方面封号或降权，不告知理由、不提供有效申诉渠道。2026年新规明确必须提前告知且有充分理由。",
        typical_case="BOSS直聘'恶意封号无证据'、抖音'先封后审'",
        category="power_abuse"
    ),
    ViolationPattern(
        id="V005",
        name="格式条款加重用户责任",
        keywords=["概不退换", "不承担", "免责", "损失自负", "风险自担", "一切解释权", "不予补偿"],
        law_refs=["L005", "L001", "L011"],
        severity="HIGH",
        description="利用格式条款不合理地免除自身责任、加重用户责任。民法典第497条明确此类条款无效。",
        typical_case="大麦网'一经售出概不退换'、去哪儿'下单后不可退款'",
        category="clause_abuse"
    ),
    ViolationPattern(
        id="V006",
        name="算法黑箱/不透明",
        keywords=["算法", "技术中立", "系统判定", "自动化", "无法告知", "商业秘密", "算法模型"],
        law_refs=["L007", "L008"],
        severity="MEDIUM",
        description="以'技术中立'或'商业秘密'为由，拒绝公开算法逻辑和判定依据。北京互联网法院明确不能以此逃避法律责任。",
        typical_case="北京互联网法院：平台不能以'技术中立'和'算法黑箱'为由逃避法律责任",
        category="algorithm"
    ),
    ViolationPattern(
        id="V007",
        name="杀熟/价格歧视",
        keywords=["差异化定价", "价格歧视", "大数据杀熟", "定向", "用户画像", "个性化定价"],
        law_refs=["L001", "L003"],
        severity="HIGH",
        description="利用用户数据进行差异化定价，损害消费者公平交易权。消费者权益保护法第10条保障公平交易权。",
        typical_case="2023年某知名互联网平台因算法价格歧视被市场监管部门约谈",
        category="pricing"
    ),
    ViolationPattern(
        id="V008",
        name="申诉机制形同虚设",
        keywords=["申诉", "客服", "人工", "反馈", "联系", "处理", "无人工客服"],
        law_refs=["L008"],
        severity="MEDIUM",
        description="虽设有申诉入口，但实际无人处理或处理周期过长。电诉宝数据显示维权成功率<15%。",
        typical_case="电诉宝数据：维权成功率<15%，处理周期90-180天",
        category="power_abuse"
    ),
    ViolationPattern(
        id="V009",
        name="数据跨境传输未告知",
        keywords=["境外", "跨境", "海外", "国际传输", "境外服务器", "海外数据中心"],
        law_refs=["L012"],
        severity="CRITICAL",
        description="涉及向境外传输个人信息，未告知用户且未经安全评估。违反个人信息保护法第38条。",
        typical_case="上海市通管局通报145款APP涉跨境传输未明确安全措施",
        category="privacy"
    ),
    ViolationPattern(
        id="V010",
        name="强制索取非必要权限",
        keywords=["获取权限", "授权", "允许访问", "开启权限", "授予", "获取手机"],
        law_refs=["L003", "L009"],
        severity="HIGH",
        description="强制索取与服务无关的系统权限，违反最小必要原则。工信部通报多批次APP涉及此问题。",
        typical_case="工信部2025-2026年累计通报200+款APP侵害用户权益",
        category="permission"
    ),
]

# ============================================================
# 五维博弈矩阵
# ============================================================

class GameDimension(Enum):
    MILITARY = "军事维度"
    HISTORICAL = "历史维度"
    PHILOSOPHICAL = "哲学维度"
    ECONOMIC = "经济维度"
    POLITICAL = "政治维度"

@dataclass
class DimensionScore:
    dimension: GameDimension
    score: int  # 0-100
    weight: float
    findings: List[str]
    analysis: str

# ============================================================
# 核心审计引擎
# ============================================================

class AuditEngine:
    """龍魂审计引擎"""

    def __init__(self):
        self.laws = LAW_DATABASE
        self.patterns = VIOLATION_PATTERNS
        self.violations_found: List[Dict] = []
        self.match_score = 0
        self.severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

    def audit(self, text: str) -> Dict:
        """执行审计"""
        self.text = text
        self._scan_patterns()
        self._analyze_dimensions()
        return self._generate_report()

    def _scan_patterns(self):
        """扫描违规模式"""
        for pattern in self.patterns:
            matches = []
            for keyword in pattern.keywords:
                if keyword.lower() in self.text.lower():
                    matches.append(keyword)
            if matches:
                self.violations_found.append({
                    "pattern_id": pattern.id,
                    "name": pattern.name,
                    "matches": matches,
                    "severity": pattern.severity,
                    "law_refs": pattern.law_refs,
                    "description": pattern.description,
                    "typical_case": pattern.typical_case,
                    "category": pattern.category
                })
                self.severity_counts[pattern.severity] += 1

        # 计算匹配分数 (0-100)
        if self.violations_found:
            severity_weights = {"CRITICAL": 1.5, "HIGH": 1.0, "MEDIUM": 0.6, "LOW": 0.3}
            weighted_found = sum(severity_weights.get(v["severity"], 0.5) for v in self.violations_found)
            weighted_max = sum(severity_weights.get(p.severity, 0.5) for p in self.patterns)
            self.match_score = min(100, int((weighted_found / weighted_max) * 100))

    def _analyze_dimensions(self):
        """五维博弈分析"""
        self.dimensions = []

        # 1. 军事维度
        military_findings = []
        if self.severity_counts["CRITICAL"] > 0:
            military_findings.append("存在CRITICAL级违规，平台处于绝对优势地位")
        if self.severity_counts["HIGH"] > 0:
            military_findings.append("存在HIGH级违规，用户防御工事薄弱")
        if self.match_score > 60:
            military_findings.append("兵力对比严重失衡，用户无对等博弈基础")
        military_score = min(100, self.match_score + 10)
        military_findings.append("平台响应速度: 毫秒级 / 用户响应速度: 45-90天")

        self.dimensions.append(DimensionScore(
            dimension=GameDimension.MILITARY,
            score=military_score, weight=0.25,
            findings=military_findings,
            analysis="平台通过算法自动执行规则，在信息不对称、速度不对称、成本不对称中占据绝对优势"
        ))

        # 2. 历史维度
        historical_findings = []
        if self.match_score > 50:
            historical_findings.append("特权泡沫预警：规则制定者不受规则约束的结构不可持续")
        if any(k in self.text.lower() for k in ["最终解释权", "单方修改", "有权变更"]):
            historical_findings.append("历史类比：封建佃农制 → 数字地主")
        historical_score = min(100, self.match_score + 5)

        self.dimensions.append(DimensionScore(
            dimension=GameDimension.HISTORICAL,
            score=historical_score, weight=0.15,
            findings=historical_findings,
            analysis="历史周期律显示：所有'治外法权'最终走向崩溃或外部矫正"
        ))

        # 3. 哲学维度
        philosophical_findings = []
        if any(k in self.text.lower() for k in ["最终解释权", "单方修改"]):
            philosophical_findings.append("契约不对等：用户协议是'诏书'而非'契约'")
        if any(k in self.text.lower() for k in ["默认同意", "视为同意", "继续使用即表示"]):
            philosophical_findings.append("同意机制失真：'同意或退出'不是自由缔约")
        philosophical_score = min(100, self.match_score + 10)

        self.dimensions.append(DimensionScore(
            dimension=GameDimension.PHILOSOPHICAL,
            score=philosophical_score, weight=0.15,
            findings=philosophical_findings,
            analysis="卢梭《社会契约论》前提是所有权利转让给共同体，平台协议是所有权利转让给平台"
        ))

        # 4. 经济维度
        economic_findings = []
        if self.match_score > 40:
            economic_findings.append("成本转嫁链：合规成本→用户、治理成本→社会、维权成本→个体")
        if any(k in self.text.lower() for k in ["概不退换", "免责", "不承担"]):
            economic_findings.append("零和博弈：平台将全部商业风险转嫁给用户")
        economic_score = min(100, self.match_score + 10)

        self.dimensions.append(DimensionScore(
            dimension=GameDimension.ECONOMIC,
            score=economic_score, weight=0.20,
            findings=economic_findings,
            analysis="平台承担5%-20%治理成本，其余转嫁给用户和社会"
        ))

        # 5. 政治维度
        political_findings = []
        if any(k in self.text.lower() for k in ["规则", "解释"]) and any(k in self.text.lower() for k in ["权利", "权力"]):
            political_findings.append("规则制定权垄断：平台自定规则、自解释、自执行")
        if self.match_score > 50:
            political_findings.append("数字封建领地：平台在华夏法则疆域内构建平行规则体系")
        political_score = min(100, self.match_score + 15)

        self.dimensions.append(DimensionScore(
            dimension=GameDimension.POLITICAL,
            score=political_score, weight=0.25,
            findings=political_findings,
            analysis="平台通过技术和资本构建事实上的'治外法权'"
        ))

    def _generate_report(self) -> Dict:
        """生成审计报告"""
        total_weighted = sum(d.score * d.weight for d in self.dimensions)

        # 三色判定
        if total_weighted >= 70:
            color = "🔴"
            status = "严重违规"
            root_meaning = "失衡 / 垄断 / 转嫁 / 黑箱 / 封建"
        elif total_weighted >= 40:
            color = "🟡"
            status = "警告"
            root_meaning = "结构性隐患 / 权力模糊 / 需要整改"
        else:
            color = "🟢"
            status = "合规"
            root_meaning = "基本符合 / 需持续监督"

        # 适用法律
        laws_applicable = []
        for v in self.violations_found:
            for ref in v.get("law_refs", []):
                law = next((l for l in self.laws if l.id == ref), None)
                if law and law.id not in [la["id"] for la in laws_applicable]:
                    laws_applicable.append({
                        "id": law.id, "name": law.name,
                        "law": law.law, "article": law.article
                    })

        # 类别分布
        categories = {}
        for v in self.violations_found:
            cat = v.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "meta": {
                "dna": DNA, "confirm": CONFIRM, "seal": SEAL,
                "gpg": GPG_KEY,
                "timestamp": datetime.now().isoformat(),
                "engine_version": "v1.0"
            },
            "summary": {
                "match_score": self.match_score,
                "total_weighted_score": round(total_weighted, 2),
                "color": color, "status": status,
                "root_meaning": root_meaning,
                "severity_counts": self.severity_counts,
                "category_distribution": categories,
                "violation_count": len(self.violations_found)
            },
            "violations": self.violations_found,
            "dimensions": [asdict(d) for d in self.dimensions],
            "laws_applicable": laws_applicable
        }

# ============================================================
# 报告生成器
# ============================================================

class ReportGenerator:
    """审计报告生成器"""

    @staticmethod
    def _get_law_names(law_refs: List[str]) -> str:
        names = []
        for ref in law_refs:
            law = next((l for l in LAW_DATABASE if l.id == ref), None)
            if law:
                names.append(f"{law.law} {law.article}")
        return ", ".join(names) if names else ""

    @staticmethod
    def _severity_emoji(sev: str) -> str:
        return {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")

    @classmethod
    def generate_markdown(cls, report: Dict) -> str:
        """生成Markdown格式报告"""
        s = report["summary"]
        lines = []
        lines.append("# 🔐 龍魂平台规则审计报告\n")
        lines.append(f"**DNA追溯码：** `{report['meta']['dna']}`")
        lines.append(f"**确认码：** `{report['meta']['confirm']}`")
        lines.append(f"**审计时间：** {report['meta']['timestamp']}")
        lines.append(f"**引擎版本：** {report['meta']['engine_version']}\n")

        # 审计结论
        lines.append("## 📊 审计结论\n")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 违规匹配度 | {s['match_score']}% |")
        lines.append(f"| 综合风险评分 | {s['total_weighted_score']}/100 |")
        lines.append(f"| 三色判定 | {s['color']} {s['status']} |")
        lines.append(f"| 根因 | {s['root_meaning']} |")
        lines.append(f"| 违规项数 | {s['violation_count']} |\n")
        lines.append(f"**违规严重程度分布：**")
        for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            emoji = cls._severity_emoji(level)
            lines.append(f"- {emoji} {level}: {s['severity_counts'][level]} 项\n")

        # 违规详情
        if report["violations"]:
            lines.append("## 🚨 检测到的违规条款\n")
            for i, v in enumerate(report["violations"], 1):
                lines.append(f"### {i}. {cls._severity_emoji(v['severity'])} {v['name']}\n")
                lines.append(f"- **严重程度：** {v['severity']}")
                lines.append(f"- **违规类型：** {v.get('category', 'other')}")
                lines.append(f"- **匹配关键词：** {', '.join(v['matches'])}")
                lines.append(f"- **描述：** {v['description']}")
                lines.append(f"- **典型案例：** {v['typical_case']}")
                if v.get("law_refs"):
                    law_names = cls._get_law_names(v["law_refs"])
                    if law_names:
                        lines.append(f"- **涉嫌违反：** {law_names}")
                lines.append("")

        # 五维博弈分析
        lines.append("## 🧠 五维博弈分析\n")
        for d in report["dimensions"]:
            lines.append(f"### {d['dimension']} (权重: {d['weight']*100:.0f}%)\n")
            lines.append(f"**评分：** {d['score']}/100\n")
            lines.append("**发现：**")
            for finding in d["findings"]:
                lines.append(f"- {finding}")
            lines.append(f"\n**分析：** {d['analysis']}\n")

        # 适用法律
        if report["laws_applicable"]:
            lines.append("## ⚖️ 适用华夏法则\n")
            lines.append("| 条款 | 法律依据 |")
            lines.append("|------|---------|")
            for law in report["laws_applicable"]:
                lines.append(f"| **{law['name']}** | {law['law']} {law['article']} |")
            lines.append("")

        # ROOT_CARD
        lines.append("## 🃏 ROOT_CARD\n")
        lines.append("```")
        lines.append("【ROOT_CARD｜数学根审计】")
        lines.append(f"Root: {s['total_weighted_score']:.0f}")
        lines.append("Wuxing: 土")
        lines.append(f"RootMeaning: {s['root_meaning']}")
        lines.append(f"TriColor: {s['color']}")
        lines.append("DataLevel: L0_PUBLIC")
        lines.append("Route: [PLATFORM-AUDIT-ENGINE-v1.0]")
        lines.append("Action: audit")
        lines.append(f"DNA: {report['meta']['dna']}")
        lines.append(f"CONFIRM: {report['meta']['confirm']}")
        lines.append(f"SEAL: {report['meta']['seal']}")
        lines.append(f"GPG: {report['meta']['gpg']}")
        lines.append("```\n")

        lines.append("---\n")
        lines.append("*报告由 龍魂一键审计工具 v1.0 生成*")
        lines.append("*数据不说谎，算法不中立，平台不无辜。*\n")
        return "\n".join(lines)

    @classmethod
    def generate_json(cls, report: Dict) -> str:
        """生成JSON格式报告"""
        return json.dumps(report, ensure_ascii=False, indent=2)


# ============================================================
# 违宪库管理
# ============================================================

class ViolationDB:
    """平台规则违宪库"""

    def __init__(self, db_path: Path = None):
        if db_path is None:
            db_path = PROJECT_ROOT / "audit" / "platform_violations.json"
        self.db_path = db_path

    def load(self) -> Dict:
        if self.db_path.exists():
            return json.loads(self.db_path.read_text(encoding='utf-8'))
        return {"version": "1.0", "platforms": [], "last_updated": None}

    def add_report(self, platform: str, url: str, report: Dict):
        db = self.load()
        db["platforms"].append({
            "platform": platform,
            "url": url,
            "audited_at": report["meta"]["timestamp"],
            "score": report["summary"]["total_weighted_score"],
            "color": report["summary"]["color"],
            "violations": [v["name"] for v in report["violations"]],
            "summary": report["summary"]["root_meaning"]
        })
        db["last_updated"] = datetime.now().isoformat()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')


# ============================================================
# 自检函数
# ============================================================

def self_test():
    """自检——用已知违规文本验证审计引擎"""
    test_text = """
用户协议
1. 本公司拥有最终解释权，有权随时修改本协议而无需另行通知。
2. 用户继续使用即表示同意修改后的协议。
3. 本公司将收集您的设备信息、位置信息、通讯录、相册等数据用于优化用户体验。
4. 本公司有权单方面限制、冻结或终止用户账号，无需提供具体理由。
5. 所有费用一经收取概不退换，本公司不承担任何由此产生的损失。
6. 用户同意本公司将数据跨境传输至海外服务器进行处理。
7. 本协议的最终解释权归本公司所有。
    """
    engine = AuditEngine()
    report = engine.audit(test_text)
    ok = (
        report["summary"]["violation_count"] >= 5
        and report["summary"]["total_weighted_score"] > 50
        and report["summary"]["severity_counts"]["CRITICAL"] >= 1
    )
    return ok, report


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🔐 龍魂一键审计工具 - 平台规则 vs 华夏法则",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh pa --text "用户协议内容..."
  lh pa --file agreement.txt
  lh pa --url "https://xxx.com/privacy"
  lh pa --interactive
  lh pa --test       # 自检
        """
    )

    parser.add_argument("--text", type=str, help="直接粘贴协议文本")
    parser.add_argument("--file", "-f", type=str, help="从文件读取协议文本")
    parser.add_argument("--url", "-u", type=str, help="从URL读取协议文本")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--format", "-F", type=str, default="md", choices=["md", "json"], help="输出格式")
    parser.add_argument("--test", action="store_true", help="运行自检")
    parser.add_argument("--save", "-s", type=str, help="保存到违宪库（指定平台名称）")

    args = parser.parse_args()

    # 自检模式
    if args.test:
        ok, report = self_test()
        print(ReportGenerator.generate_markdown(report))
        print(f"\n{'✅ 自检通过' if ok else '🔴 自检失败'}")
        return 0 if ok else 1

    # 获取待审计文本
    text = None

    if args.interactive:
        print("🔐 龍魂一键审计工具 v1.0")
        print("=" * 50)
        print("请粘贴平台用户协议或隐私政策文本")
        print("输入完成后按 Ctrl+D (Mac/Linux) 或 Ctrl+Z (Windows)")
        print("=" * 50)
        try:
            lines = []
            while True:
                lines.append(input())
        except EOFError:
            pass
        text = "\n".join(lines)
        if not text.strip():
            print("❌ 未输入任何内容")
            return 1

    elif args.url:
        try:
            import requests
            from bs4 import BeautifulSoup
            resp = requests.get(args.url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, 'html.parser')
            for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
        except ImportError:
            print("❌ 需要安装 requests 和 beautifulsoup4")
            print("   pip install requests beautifulsoup4")
            return 1
        except Exception as e:
            print(f"❌ 获取URL失败: {e}")
            return 1

    elif args.file:
        try:
            text = Path(args.file).read_text(encoding='utf-8')
        except FileNotFoundError:
            print(f"❌ 文件不存在: {args.file}")
            return 1
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return 1

    elif args.text:
        text = args.text

    else:
        parser.print_help()
        return 0

    if not text or len(text.strip()) < 50:
        print("❌ 文本内容过短（至少50字符），请提供完整的用户协议或隐私政策")
        return 1

    # 执行审计
    print("🔍 正在审计...", file=sys.stderr)
    engine = AuditEngine()
    report = engine.audit(text)

    # 生成报告
    if args.format == "json":
        output = ReportGenerator.generate_json(report)
    else:
        output = ReportGenerator.generate_markdown(report)

    # 保存到违宪库
    if args.save:
        db = ViolationDB()
        db.add_report(args.save, args.url or "", report)
        print(f"✅ 已保存到违宪库：{args.save}", file=sys.stderr)

    # 输出
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"✅ 报告已保存到: {args.output}", file=sys.stderr)
    else:
        print(f"\n{'=' * 70}")
        print(output)
        print(f"\n{'=' * 70}")

    # 输出时间戳
    try:
        from lh_time_engine import get_output_stamp
        print(f"\n{get_output_stamp()}", file=sys.stderr)
    except ImportError:
        pass

    return 0

if __name__ == "__main__":
    sys.exit(main())
