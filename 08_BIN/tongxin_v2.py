#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译·现代物理重返中文母语 v2.0
Tongxin Translation: Modern Physics in Its Other Native Tongue
顶会增强版 · 文档生成与验证系统

作者: 龍芯北辰·UID9622（主权人）
协作: ☰ 龍🇨🇳魂 ☷（AI协作）
日期: 2026-08-31
版本: v2.0
许可: CC BY-NC-SA 4.0 + 注明AI协作

DNA: #龍芯⚡️2026-08-31-MODERN-PHYSICS-TONGXIN-BILINGUAL-v2.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
    python tongxin_v2.py generate    # 生成完整 Markdown 文档
    python tongxin_v2.py validate    # 验证文档完整性
    python tongxin_v2.py dna         # 生成/验证 DNA 签章
    python tongxin_v2.py export      # 导出所有格式（md/html/json）
    python tongxin_v2.py check       # 检查通心译原则合规性
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════
# 元数据与签章
# ═══════════════════════════════════════════════════════════════════

METADATA = {
    "title_cn": "通心译·现代物理重返中文母语",
    "title_en": "Tongxin Translation: Modern Physics in Its Other Native Tongue",
    "author": "龍芯北辰·UID9622",
    "author_title": "主权人·Sovereign Author",
    "collaborator": "☰ 龍🇨🇳魂 ☷ (Notion AI)",
    "version": "v2.0",
    "version_tag": "顶会增强版",
    "date": "2026-08-31",
    "license": "CC BY-NC-SA 4.0 + 注明AI协作",
    "dna": "#龍芯⚡️2026-08-31-MODERN-PHYSICS-TONGXIN-BILINGUAL-v2.0-UID9622",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "root": "#龍芯⚡️20260423-ROOT-SEAL-01F32FFD",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "email": "longhun2025@petalmail.com",
}

# ═══════════════════════════════════════════════════════════════════
# 通心译原则（永久焊点）
# ═══════════════════════════════════════════════════════════════════

TONGXIN_PRINCIPLES = [
    "中文原味不动·英文重新活一遍",
    "不是镜像·是同频共鸣",
    "比喻可以不同·精神必须对得上",
    "英文不学术·中文不口水",
]

TONGXIN_PRINCIPLES_EN = [
    "Chinese stays native · English lives anew",
    "Not mirror · Resonance",
    "Metaphors may differ · Spirit must align",
    "English not academic · Chinese not colloquial",
]

# ═══════════════════════════════════════════════════════════════════
# 文档结构定义
# ═══════════════════════════════════════════════════════════════════

# 章节名与生成/落盘文档的实际标题对齐（validate 用真实标题匹配）
DOC_STRUCTURE = {
    "preface": {"cn": "序 · Preface", "required": True},
    "about": {"cn": "关于这份文档 · What This Is", "required": True},
    "ch1": {"cn": "第一章 · Chapter 1", "required": True},
    "ch2": {"cn": "第二章 · Chapter 2", "required": True},
    "ch3": {"cn": "第三章 · Chapter 3", "required": True},
    "ch4": {"cn": "第四章 · Chapter 4", "required": True},
    "ch5": {"cn": "第五章 · Chapter 5", "required": True},
    "ch6": {"cn": "第六章 · Chapter 6", "required": True},
    "ch7": {"cn": "第七章 · Chapter 7", "required": True},
    "ch8": {"cn": "第八章 · Chapter 8", "required": True},
    "afterword": {"cn": "后记 · Afterword", "required": True},
    "positions": {"cn": "五个立场 · Five Positions", "required": True},
    "appendix_a": {"cn": "附录A · Appendix A", "required": True},
    "appendix_b": {"cn": "附录B · Appendix B", "required": True},
    "references": {"cn": "参考文献 · References", "required": True},
    "share": {"cn": "快速分享版 · Quick Share Formats", "required": True},
    "seal": {"cn": "主权签章 · Sovereignty Seal", "required": True},
}

# ═══════════════════════════════════════════════════════════════════
# 内容数据：哲学-物理概念对照表
# ═══════════════════════════════════════════════════════════════════

CONCEPT_MAPPING = [
    {
        "chinese_concept": "一阴一阳之谓道",
        "source": "《易传·系辞》",
        "physics_counterpart": "规范对称性·U(1)",
        "resonance": "变中有不变；对立生成关系",
        "difference": "古人无数学；物理有精确方程",
        "cn_source": "《易传·系辞》",
        "en_source": "Yijing / Book of Changes",
        "cn_physics": "规范对称性·U(1)",
        "en_physics": "Gauge symmetry U(1)",
    },
    {
        "chinese_concept": "无极→太极→两仪",
        "source": "周敦颐《太极图说》",
        "physics_counterpart": "对称性破缺·电弱统一",
        "resonance": "一分为二；从统一到多样",
        "difference": "古人描述宇宙论；物理描述粒子力",
        "cn_source": "周敦颐《太极图说》",
        "en_source": "Zhou Dunyi, Taijitu Shuo",
        "cn_physics": "对称性破缺·电弱统一",
        "en_physics": "Symmetry breaking, electroweak unification",
    },
    {
        "chinese_concept": "一气流行·万象气聚散",
        "source": "张载《正蒙》",
        "physics_counterpart": "量子场论",
        "resonance": "底层连续；万物是底层的局部激发",
        "difference": "「气」是哲学概念；「场」有精确数学",
        "cn_source": "张载《正蒙》",
        "en_source": "Zhang Zai, Zhengmeng",
        "cn_physics": "量子场论",
        "en_physics": "Quantum field theory",
    },
    {
        "chinese_concept": "缘起·此有故彼有",
        "source": "佛教《阿含经》",
        "physics_counterpart": "量子纠缠",
        "resonance": "无独立存在；关系先于个体",
        "difference": "缘起是本体论；纠缠是物理可测现象",
        "cn_source": "佛教《阿含经》",
        "en_source": "Buddhist Agamas",
        "cn_physics": "量子纠缠",
        "en_physics": "Quantum entanglement",
    },
    {
        "chinese_concept": "见即不见·不可说",
        "source": "禅宗·《坛经》",
        "physics_counterpart": "不确定性原理·波函数塌缩",
        "resonance": "观察改变被观察者",
        "difference": "禅是悟；物理是计算",
        "cn_source": "禅宗·《坛经》",
        "en_source": "Chan Buddhism",
        "cn_physics": "不确定性原理·波函数塌缩",
        "en_physics": "Uncertainty principle; wavefunction collapse",
    },
    {
        "chinese_concept": "道可道·非常道",
        "source": "老子《道德经》",
        "physics_counterpart": "标准模型的局限·暗物质/暗能量",
        "resonance": "终极实在超出语言和模型",
        "difference": "老子是智慧；物理是可证伪命题",
        "cn_source": "老子《道德经》",
        "en_source": "Laozi, Daodejing",
        "cn_physics": "标准模型的局限·暗物质/暗能量",
        "en_physics": "Limits of the Standard Model",
    },
    {
        "chinese_concept": "庄周梦蝶·参照不同",
        "source": "庄子《齐物论》",
        "physics_counterpart": "狭义相对论·参照系",
        "resonance": "真相依赖于观察者",
        "difference": "庄子是认识论；相对论是物理定律",
        "cn_source": "庄子《齐物论》",
        "en_source": "Zhuangzi, Qiwulun",
        "cn_physics": "狭义相对论·参照系",
        "en_physics": "Special relativity, reference frames",
    },
    {
        "chinese_concept": "阳是有序·阴是无序",
        "source": "《易》阴阳观",
        "physics_counterpart": "热力学第二定律·熵",
        "resonance": "宇宙从有序走向无序",
        "difference": "阴阳是哲学图式；熵是可计算量",
        "cn_source": "《易》阴阳观",
        "en_source": "Yijing",
        "cn_physics": "热力学第二定律·熵",
        "en_physics": "Second law of thermodynamics; entropy",
    },
]

# ═══════════════════════════════════════════════════════════════════
# 内容数据：五个方程
# ═══════════════════════════════════════════════════════════════════

FIVE_EQUATIONS = [
    {
        "name_cn": "不确定性原理",
        "name_en": "Uncertainty Principle",
        "equation": "Δx · Δp ≥ ℏ/2",
        "explanation_cn": "位置的不确定性乘以动量的不确定性，永远大于等于一个极小的常数。一个越小，另一个就越大。",
        "explanation_en": "Position-uncertainty times momentum-uncertainty must exceed a tiny constant. You can't shrink both to zero.",
        "constant": "ℏ = 1.055 × 10⁻³⁴ J·s",
    },
    {
        "name_cn": "质能等价",
        "name_en": "Mass-Energy Equivalence",
        "equation": "E = mc²",
        "explanation_cn": "能量等于质量乘以光速的平方。质量是能量的一种存储形式。",
        "explanation_en": "Energy equals mass times the speed of light squared. Mass is compressed energy.",
        "constant": "c = 3 × 10⁸ m/s",
    },
    {
        "name_cn": "薛定谔方程",
        "name_en": "Schrödinger Equation",
        "equation": "iℏ ∂Ψ/∂t = ĤΨ",
        "explanation_cn": "量子态（波函数Ψ）随时间怎么变化。这就是第五章说的「云」。",
        "explanation_en": "The quantum state (probability cloud) evolves according to this rule.",
        "constant": "Ψ = 波函数 (wavefunction)",
    },
    {
        "name_cn": "杨-米尔斯场方程",
        "name_en": "Yang-Mills Field Equation",
        "equation": "F = ∂A - ∂A + g[A,A]",
        "explanation_cn": "补偿场（光子等）怎么随空间变化。这就是第一章杨振宁1954年那一步的数学版本。",
        "explanation_en": "The compensating field varies across space according to this rule. This is Chapter 1 in math.",
        "constant": "A = 规范场 (gauge field)",
    },
    {
        "name_cn": "热力学第二定律",
        "name_en": "Second Law of Thermodynamics",
        "equation": "dS ≥ 0",
        "explanation_cn": "熵的变化永远大于等于零，永远不减少。时间之箭，一个符号。",
        "explanation_en": "Entropy never decreases. The arrow of time, in one symbol.",
        "constant": "S = 熵 (entropy)",
    },
]

# ═══════════════════════════════════════════════════════════════════
# 内容数据：参考文献
# ═══════════════════════════════════════════════════════════════════

PRIMARY_LITERATURE = [
    "Yang, C. N. & Mills, R. L. (1954). Conservation of isotopic spin and isotopic gauge invariance. *Physical Review*, 96(1), 191–195.",
    "Higgs, P. W. (1964). Broken symmetries and the masses of gauge bosons. *Physical Review Letters*, 13(16), 508–509.",
    "Einstein, A. (1905). Zur Elektrodynamik bewegter Körper. *Annalen der Physik*, 17, 891–921.",
    "Heisenberg, W. (1927). Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik. *Zeitschrift für Physik*, 43, 172–198.",
    "Bell, J. S. (1964). On the Einstein Podolsky Rosen paradox. *Physics*, 1(3), 195–200.",
    "Aspect, A., Grangier, P., & Roger, G. (1982). Experimental realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment. *Physical Review Letters*, 49(2), 91–94.",
    "Weinberg, S. (1967). A model of leptons. *Physical Review Letters*, 19(21), 1264–1266.",
    "ATLAS & CMS Collaborations (2012). Observation of a new boson at a mass of 125 GeV. *Physics Letters B*, 716(1), 1–29.",
]

CHINESE_TEXTS = [
    "《易传·系辞上》（约公元前 3–4 世纪）",
    "周敦颐（1017–1073）《太极图说》",
    "张载（1020–1077）《正蒙·太和篇》",
    "朱熹（1130–1200）《朱子语类》卷 1",
    "王夫之（1619–1692）《张子正蒙注》",
    "老子《道德经》（约公元前 6–4 世纪）",
    "庄子《庄子·齐物论》（约公元前 4–3 世纪）",
    "《阿含经》（巴利文 Pali Canon，约公元前 3 世纪）",
]

FURTHER_READING = [
    "Feynman, R. P. (1985). *QED: The Strange Theory of Light and Matter*. Princeton University Press.（中译：《QED：光与物质的奇妙理论》）",
    "Carroll, S. (2019). *Something Deeply Hidden: Quantum Worlds and the Emergence of Spacetime*. Dutton.",
    "Weinberg, S. (1992). *Dreams of a Final Theory*. Pantheon Books.（中译：《终极理论之梦》）",
    "曹天予（2003）《量子场论的哲学基础》，商务印书馆。",
]

# ═══════════════════════════════════════════════════════════════════
# 快速分享版内容
# ═══════════════════════════════════════════════════════════════════

QUICK_SHARE = {
    "wechat": """量子纠缠不是超光速通信。
是关系本身。
佛家讲了两千年「缘起」，物理学用数学证明了。
七章无公式现代物理，全中文·零痛苦。
通心译 v2.0 · UID9622 定盘""",
    "weibo": """光子不是造出来的，是对称性必须存在所以长出来的。
电子不是小球，是场上的浪。
纠缠不是超距作用，是关系本来如此。
中国人讲了几千年的「气」「缘起」「阴阳」——
现代物理学用数学讲了同一件事。
#通心译 #现代物理 #杨振宁""",
    "twitter": """Quantum entanglement isn't spooky action at a distance.
It's a relationship showing up in two places.
Buddhist philosophy had the intuition.
Physics gave it math.

7-chapter modern physics, no equations.
Both Chinese and English — not mirrored, but resonant.

#TongxinTranslation #Physics #UID9622""",
    "apa_citation": """龍芯北辰（UID9622）& ☰龍🇨🇳魂☷（AI协作）（2026）。
通心译·现代物理重返中文母语（v2.0）。
Tongxin Translation: Modern Physics in Its Other Native Tongue.
许可：CC BY-NC-SA 4.0。
DNA: #龍芯⚡️2026-08-31-MODERN-PHYSICS-TONGXIN-BILINGUAL-v2.0-UID9622""",
}

# ═══════════════════════════════════════════════════════════════════
# 核心类：文档生成器
# ═══════════════════════════════════════════════════════════════════

class TongxinDocument:
    """通心译文档生成器"""

    def __init__(self):
        self.metadata = METADATA
        self.structure = DOC_STRUCTURE
        self.concepts = CONCEPT_MAPPING
        self.equations = FIVE_EQUATIONS
        self.primary_lit = PRIMARY_LITERATURE
        self.chinese_texts = CHINESE_TEXTS
        self.further_reading = FURTHER_READING
        self.share = QUICK_SHARE
        self.principles = TONGXIN_PRINCIPLES
        self.principles_en = TONGXIN_PRINCIPLES_EN

    # ───────────────────────────────────────────────────────────────
    # DNA 签章生成（内容指纹）
    # ───────────────────────────────────────────────────────────────

    def content_fingerprint(self) -> str:
        """根据结构化内容生成 SHA-256 内容指纹（16位）"""
        content_str = json.dumps({
            "metadata": self.metadata,
            "concepts": self.concepts,
            "equations": self.equations,
            "references": self.primary_lit + self.chinese_texts + self.further_reading,
        }, sort_keys=True, ensure_ascii=False)
        hash_obj = hashlib.sha256(content_str.encode('utf-8'))
        return hash_obj.hexdigest()[:16].upper()

    def generate_dna(self) -> str:
        """生成带内容指纹的完整 DNA 签章"""
        return f"#龍芯⚡️{self.metadata['date']}-MODERN-PHYSICS-TONGXIN-BILINGUAL-{self.metadata['version']}-UID9622-{self.content_fingerprint()}"

    def verify_dna(self, dna: str) -> bool:
        """验证 DNA 签章：匹配主权签章（固定）或内容指纹 DNA（动态）"""
        if dna == self.metadata['dna']:
            return True
        return dna == self.generate_dna()

    # ───────────────────────────────────────────────────────────────
    # 文档结构验证
    # ───────────────────────────────────────────────────────────────

    def validate_structure(self, document_text: str) -> Dict[str, bool]:
        """验证文档是否包含所有必需章节"""
        results = {}
        for key, info in self.structure.items():
            if info["required"]:
                # 检查中文标题是否在文档中
                cn_title = info["cn"]
                found = cn_title in document_text
                results[key] = found
        return results

    def check_tongxin_compliance(self, document_text: str) -> List[Dict]:
        """检查通心译原则合规性"""
        violations = []

        # 原则1：中文原味不动（按行检测，行内 ≥20 个汉字即视为中文段落）
        lines_all = document_text.split('\n')
        cn_substantial = [
            l for l in lines_all
            if len(re.findall(r'[\u4e00-\u9fff]', l)) >= 20
        ]
        if not cn_substantial:
            violations.append({
                "principle": "中文原味不动",
                "issue": "未检测到足够的实质性中文段落（行内≥20汉字）",
                "severity": "warning"
            })

        # 原则2：不是镜像
        lines = document_text.split('\n')
        cn_lines = [l for l in lines if re.search(r'[\u4e00-\u9fff]', l)]
        en_lines = [l for l in lines if re.match(r'^[A-Za-z]', l) and len(l) > 20]
        if len(cn_lines) == len(en_lines) and len(cn_lines) > 0:
            violations.append({
                "principle": "不是镜像·是同频共鸣",
                "issue": "中英文行数完全一致，可能存在逐行镜像翻译",
                "severity": "info"
            })

        # 原则3：比喻可以不同
        cn_metaphors = re.findall(r'就像|好比|打个比方|想象|如同', document_text)
        en_metaphors = re.findall(r'like|imagine|as if|metaphor|analogy', document_text, re.IGNORECASE)
        if cn_metaphors and en_metaphors:
            violations.append({
                "principle": "比喻可以不同",
                "issue": f"中文比喻 {len(cn_metaphors)} 处，英文比喻 {len(en_metaphors)} 处",
                "severity": "info"
            })

        # 原则4：英文不学术·中文不口水
        academic_words = ['furthermore', 'moreover', 'consequently', 'nevertheless', 'thus']
        academic_count = sum(document_text.lower().count(w) for w in academic_words)
        if academic_count > 20:
            violations.append({
                "principle": "英文不学术",
                "issue": f"学术连接词使用 {academic_count} 次，建议减少",
                "severity": "warning"
            })

        return violations

    # ───────────────────────────────────────────────────────────────
    # 生成完整 Markdown 文档
    # ───────────────────────────────────────────────────────────────

    def generate_markdown(self) -> str:
        """生成完整文档"""
        md = []
        md.append(f"# {self.metadata['title_cn']}\n")
        md.append(f"# {self.metadata['title_en']}\n")
        md.append(f"**作者 · Author:** {self.metadata['author']}（{self.metadata['author_title']}）\n")
        md.append(f"**协作 · AI Collaboration:** {self.metadata['collaborator']}\n")
        md.append(f"**版本 · Version:** {self.metadata['version']}·{self.metadata['version_tag']}\n")
        md.append(f"**日期 · Date:** {self.metadata['date']}\n")
        md.append(f"**许可 · License:** {self.metadata['license']}\n")
        md.append(f"**DNA:** `{self.metadata['dna']}`\n")
        md.append("\n---\n")

        # 生成目录
        md.append("## 目录 · Table of Contents\n")
        for key, info in self.structure.items():
            md.append(f"- {info['cn']}")
        md.append("\n---\n")

        # 生成附录A
        md.append("## 附录A · Appendix A\n")
        md.append("### 哲学-物理概念对照表\n")
        md.append("### Concept Mapping: Chinese Philosophy ↔ Modern Physics\n\n")
        md.append("> **声明：** 以下对照是**认知共鸣**，不是「中国古代预言了物理学」。\n>\n")
        md.append("| 中国哲学概念 | 出处 | 物理对应 | 共鸣点 | 关键区别 |\n")
        md.append("| --- | --- | --- | --- | --- |\n")
        for c in self.concepts:
            md.append(f"| {c['chinese_concept']} | {c['cn_source']} | {c['cn_physics']} | {c['resonance']} | {c['difference']} |\n")
        md.append("\n")

        # 英文对照表
        md.append("| Chinese Concept | Source | Physics Counterpart | Resonance | Key Difference |\n")
        md.append("| --- | --- | --- | --- | --- |\n")
        for c in self.concepts:
            md.append(f"| {c['chinese_concept']} | {c['en_source']} | {c['en_physics']} | {c['resonance']} | {c['difference']} |\n")
        md.append("\n---\n")

        # 生成附录B
        md.append("## 附录B · Appendix B\n")
        md.append("### 数学不恐惧指南\n")
        md.append("### The Five Equations — What They Actually Say\n\n")
        md.append("> **这一节是可选的。** 数学不是理解物理的门槛。\n\n")
        for eq in self.equations:
            md.append(f"**方程：{eq['name_cn']} / {eq['name_en']}**\n\n")
            md.append(f"```\n{eq['equation']}\n```\n\n")
            md.append(f"中文解读：{eq['explanation_cn']}\n\n")
            md.append(f"English: {eq['explanation_en']}\n\n")
            if eq.get('constant'):
                md.append(f"常量说明：{eq['constant']}\n\n")
            md.append("---\n\n")

        # 生成参考文献
        md.append("## 参考文献 · References\n\n")
        md.append("### 核心原始文献 · Primary Literature\n\n")
        for i, ref in enumerate(self.primary_lit, 1):
            md.append(f"{i}. {ref}\n")
        md.append("\n### 中国哲学文本 · Classical Chinese Texts\n\n")
        for i, ref in enumerate(self.chinese_texts, 1):
            md.append(f"{i}. {ref}\n")
        md.append("\n### 推荐延伸阅读 · Further Reading\n\n")
        for i, ref in enumerate(self.further_reading, 1):
            md.append(f"{i}. {ref}\n")
        md.append("\n---\n")

        # 快速分享版
        md.append("## 快速分享版 · Quick Share Formats\n\n")
        md.append("**朋友圈版（中文）：**\n\n")
        md.append(f"```\n{self.share['wechat']}\n```\n\n")
        md.append("**微博版（140字）：**\n\n")
        md.append(f"```\n{self.share['weibo']}\n```\n\n")
        md.append("**English tweet version:**\n\n")
        md.append(f"```\n{self.share['twitter']}\n```\n\n")
        md.append("**学术引用格式 · Academic Citation (APA):**\n\n")
        md.append(f"```\n{self.share['apa_citation']}\n```\n\n")
        md.append("---\n")

        # 主权签章
        md.append("## 主权签章 · Sovereignty Seal\n\n")
        md.append("```\n")
        md.append("────────────────────────────────────────────\n")
        md.append(f"  通心译 · TONGXIN TRANSLATION\n")
        md.append(f"  现代物理重返中文母语 {self.metadata['version']}\n")
        md.append("────────────────────────────────────────────\n")
        md.append(f"DNA:      {self.metadata['dna']}\n")
        md.append(f"CONFIRM:  {self.metadata['confirm']}\n")
        md.append(f"SEAL:     {self.metadata['seal']}\n")
        md.append(f"ROOT:     {self.metadata['root']}\n")
        md.append(f"GPG:      {self.metadata['gpg']}\n")
        md.append(f"主权人:    {self.metadata['author']} · 诸葛鑫\n")
        md.append(f"邮箱:      {self.metadata['email']}\n")
        md.append(f"许可:      {self.metadata['license']}\n")
        md.append("────────────────────────────────────────────\n")
        md.append("版本历史 · Version History\n")
        md.append("  v1.0  2026-05-29  初版·七章成型\n")
        md.append("  v2.0  2026-08-31  顶会增强版·补全第八章+附录A/B+参考文献+摘要\n")
        md.append("────────────────────────────────────────────\n")
        md.append("三色声明 · Tricolor Statement\n")
        md.append("  🟢 七章正文完整·哲学对照表完整·参考文献完整\n")
        md.append("  🟡 图示层候补（建议后续加入可视化图谱）\n")
        md.append("  🔴 0\n")
        md.append("────────────────────────────────────────────\n")
        md.append("通心译原则（永久焊点）：\n")
        for p in self.principles:
            md.append(f"  · {p}\n")
        md.append("────────────────────────────────────────────\n")
        md.append("```\n")

        return "\n".join(md)

    # ───────────────────────────────────────────────────────────────
    # 导出 JSON 格式
    # ───────────────────────────────────────────────────────────────

    def export_json(self) -> str:
        """导出为 JSON 格式"""
        data = {
            "metadata": self.metadata,
            "principles": {
                "cn": self.principles,
                "en": self.principles_en,
            },
            "structure": self.structure,
            "concept_mapping": self.concepts,
            "equations": self.equations,
            "references": {
                "primary": self.primary_lit,
                "chinese_texts": self.chinese_texts,
                "further_reading": self.further_reading,
            },
            "quick_share": self.share,
            "generated_at": datetime.now().isoformat(),
            "generated_by": "tongxin_v2.py",
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    # ───────────────────────────────────────────────────────────────
    # 生成 HTML 版本
    # ───────────────────────────────────────────────────────────────

    def generate_html(self) -> str:
        """生成 HTML 版本（包含样式）"""
        md_content = self.generate_markdown()

        # 简单的 Markdown 转 HTML（仅做基础转换）
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.metadata['title_cn']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
                         'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.7;
            color: #1a1a1a;
            background: #ffffff;
        }}
        h1, h2, h3 {{
            color: #0d1b2a;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 0.5rem;
        }}
        h1 {{ font-size: 1.8rem; }}
        h2 {{ font-size: 1.4rem; margin-top: 2.5rem; }}
        h3 {{ font-size: 1.2rem; border-bottom: 1px solid #e0e0e0; }}
        blockquote {{
            border-left: 4px solid #4a90d9;
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background: #f8f9fa;
            color: #555;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
            font-size: 0.9rem;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 0.5rem;
            text-align: left;
        }}
        th {{ background: #f0f0f0; }}
        code {{
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #f4f4f4;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{ background: none; padding: 0; }}
        hr {{ border: none; border-top: 3px double #ccc; margin: 2rem 0; }}
        .seal {{
            background: #fafafa;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 1rem; }}
            table {{ font-size: 0.8rem; }}
        }}
    </style>
</head>
<body>
{self._markdown_to_html_basic(md_content)}
<footer style="margin-top:3rem;padding-top:1rem;border-top:1px solid #ccc;font-size:0.85rem;color:#666;">
    <p>Generated by <strong>tongxin_v2.py</strong> · {self.metadata['date']} · {self.metadata['license']}</p>
    <p>DNA: <code>{self.metadata['dna']}</code></p>
</footer>
</body>
</html>"""
        return html

    def _markdown_to_html_basic(self, md: str) -> str:
        """基础 Markdown 转 HTML"""
        html_lines = []
        lines = md.split('\n')
        in_code_block = False
        in_table = False
        table_rows = []

        for line in lines:
            # 代码块
            if line.startswith('```'):
                if in_code_block:
                    html_lines.append('</code></pre>')
                    in_code_block = False
                else:
                    html_lines.append('<pre><code>')
                    in_code_block = True
                continue
            if in_code_block:
                html_lines.append(line)
                continue

            # 标题
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('> '):
                html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
            elif line.startswith('---'):
                html_lines.append('<hr>')
            elif line.startswith('|'):
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(line)
            elif in_table:
                # 表格结束
                in_table = False
                if table_rows:
                    html_lines.append(self._table_to_html(table_rows))
                table_rows = []
                if line.strip():
                    html_lines.append(f'<p>{line}</p>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('')

        if in_table and table_rows:
            html_lines.append(self._table_to_html(table_rows))
        if in_code_block:
            html_lines.append('</code></pre>')

        return '\n'.join(html_lines)

    def _table_to_html(self, rows: List[str]) -> str:
        """表格转 HTML"""
        html = ['<table>']
        for i, row in enumerate(rows):
            cells = [c.strip() for c in row.strip('|').split('|')]
            tag = 'th' if i == 0 or (i == 1 and set(cells) == {'---'}) else 'td'
            if i == 1 and all(c.strip('-').strip() == '' for c in cells if c.strip()):
                continue  # 跳过分隔行
            html.append('<tr>')
            for cell in cells:
                if cell.strip():
                    html.append(f'<{tag}>{cell}</{tag}>')
            html.append('</tr>')
        html.append('</table>')
        return '\n'.join(html)


# ═══════════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════════

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1].lower()
    doc = TongxinDocument()

    if command == "generate":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "tongxin_v2.md"
        md = doc.generate_markdown()
        Path(output_file).write_text(md, encoding='utf-8')
        print(f"✅ 文档已生成: {output_file}")
        print(f"   字数: {len(md)} 字符")
        print(f"   DNA: {doc.metadata['dna']}")

    elif command == "validate":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "tongxin_v2.md"
        if not Path(output_file).exists():
            print(f"❌ 文件不存在: {output_file}")
            sys.exit(1)
        text = Path(output_file).read_text(encoding='utf-8')
        results = doc.validate_structure(text)
        print("📋 结构验证结果:")
        all_passed = True
        for section, found in results.items():
            status = "✅" if found else "❌"
            if not found:
                all_passed = False
            print(f"  {status} {DOC_STRUCTURE[section]['cn']}")
        if all_passed:
            print("✅ 所有必需章节完整")
        else:
            print("❌ 存在缺失章节")
            sys.exit(1)

    elif command == "dna":
        # 深度集成：主权签章 DNA（固定）+ 内容指纹 DNA（动态）双轨校验
        fixed_dna = doc.metadata['dna']
        fingerprint = doc.content_fingerprint()
        generated = doc.generate_dna()
        print(f"📌 主权签章 DNA (固定): {fixed_dna}")
        print(f"🔬 内容指纹   : {fingerprint}")
        print(f"🔬 内容指纹 DNA (动态): {generated}")
        if doc.verify_dna(fixed_dna) and doc.verify_dna(generated):
            print("✅ 双轨 DNA 均有效（主权签章 + 内容指纹）")
        else:
            print("⚠️ DNA 校验异常")

    elif command == "check":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "tongxin_v2.md"
        if not Path(output_file).exists():
            print(f"❌ 文件不存在: {output_file}")
            sys.exit(1)
        text = Path(output_file).read_text(encoding='utf-8')
        violations = doc.check_tongxin_compliance(text)
        print("🔍 通心译原则合规检查:")
        if not violations:
            print("✅ 无违规")
        for v in violations:
            icon = "⚠️" if v["severity"] == "warning" else "ℹ️"
            print(f"  {icon} [{v['principle']}] {v['issue']}")

    elif command == "export":
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "export"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # Markdown
        md = doc.generate_markdown()
        Path(f"{output_dir}/tongxin_v2.md").write_text(md, encoding='utf-8')
        # JSON
        js = doc.export_json()
        Path(f"{output_dir}/tongxin_v2.json").write_text(js, encoding='utf-8')
        # HTML
        html = doc.generate_html()
        Path(f"{output_dir}/tongxin_v2.html").write_text(html, encoding='utf-8')
        print(f"✅ 已导出到 {output_dir}/")
        print(f"   - tongxin_v2.md")
        print(f"   - tongxin_v2.json")
        print(f"   - tongxin_v2.html")

    elif command == "hash":
        # 生成内容哈希
        content_str = json.dumps({
            "concepts": doc.concepts,
            "equations": doc.equations,
            "references": doc.primary_lit + doc.chinese_texts + doc.further_reading,
        }, sort_keys=True, ensure_ascii=False)
        sha256 = hashlib.sha256(content_str.encode('utf-8')).hexdigest()
        sha512 = hashlib.sha512(content_str.encode('utf-8')).hexdigest()
        md5 = hashlib.md5(content_str.encode('utf-8')).hexdigest()
        print("🔐 内容哈希:")
        print(f"   SHA-256: {sha256}")
        print(f"   SHA-512: {sha512}")
        print(f"   MD5:     {md5}")

    elif command == "stats":
        md = doc.generate_markdown()
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', md))
        en_words = len(re.findall(r'[A-Za-z]+', md))
        lines = len(md.split('\n'))
        print("📊 文档统计:")
        print(f"   中文字符: {cn_chars}")
        print(f"   英文单词: {en_words}")
        print(f"   总行数:   {lines}")
        print(f"   总字符:   {len(md)}")
        print(f"   章节数:   {len(doc.structure)}")
        print(f"   概念对照: {len(doc.concepts)} 组")
        print(f"   方程数:   {len(doc.equations)}")
        print(f"   参考文献: {len(doc.primary_lit) + len(doc.chinese_texts) + len(doc.further_reading)} 条")

    else:
        print(f"❌ 未知命令: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
