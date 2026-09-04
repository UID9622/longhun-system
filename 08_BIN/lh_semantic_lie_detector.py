#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-SEMANTIC-LIE-DETECTOR-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  🧬 龍魂·语义测谎仪 v2.0 — 语义库联动·规避话术检测·异常账号标记            ║
║  Semantic Lie Detector · Connected to Semantic Library                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-SEMANTIC-LIE-DETECTOR-v2.0                      ║
║  语义库: 02_SKILLS/anti_fraud_patterns_v2.0.json (13+检测维度)            ║
║  愿景: 2025年初心 — 人文系统就是测谎仪·给政府提供最好的反诈工具            ║
║  哲学:                                                                   ║
║    不只看字面意思 → 追溯本源记忆 → 跨会话DNA关联                            ║
║    好话标记 → 背后是否有营销手段 → 连环套识别                               ║
║    谐音字/拆字/直播小纸条 → 全维度规避检测                                   ║
║    异常账号标记 → 追溯本源 → 为反诈提供证据链                                ║
║  铁律:                                                                   ║
║    不修改原文·下方追加审计备注·每条DNA嵌入·三色审计                         ║
║    不做政府的事·但给政府提供最好的反诈工具                                   ║
║    保护受害者·揭露连环套·追溯本源                                           ║
║  进化:                                                                    ║
║    语义库独立存储 → 添加新模式无需改代码 → 持续迭代                          ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    # 分析一段话的深层意图
    python3 bin/lh_semantic_lie_detector.py analyze --text "这段话..."

    # 跨会话追踪一个人的话术一致性
    python3 bin/lh_semantic_lie_detector.py track --person "某人"

    # 标记异常账号
    python3 bin/lh_semantic_lie_detector.py flag --person "某人"

    # 追溯本源：追踪话术来源链
    python3 bin/lh_semantic_lie_detector.py trace-origin --person "某人"

    # 批量检测对话记录中的连环套
    python3 bin/lh_semantic_lie_detector.py scan --file 对话记录.json

    # 语义库扩充：添加新的检测维度
    python3 bin/lh_semantic_lie_detector.py expand --dimension 传销话术 --patterns patterns.json

    # 从语义抽屉重新加载模式库
    python3 bin/lh_semantic_lie_detector.py reload

    # 启动 API 服务
    python3 bin/lh_semantic_lie_detector.py serve --port 19624

    # 查看语义检测库统计
    python3 bin/lh_semantic_lie_detector.py stats
"""

import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field

LONGHUN_ROOT = Path(__file__).resolve().parent.parent

# 语义库路径
ANTI_FRAUD_PATTERNS = LONGHUN_ROOT / "01_技能庫" / "anti_fraud_patterns_v2.0.json"
SEMANTIC_DRAWERS = LONGHUN_ROOT / "01_技能庫" / "owner_semantic_drawers_v2.0.json"

# ═══════════════════════════════════════════════════════════════
# 语义库联动 — 从独立模式库加载检测维度
# ═══════════════════════════════════════════════════════════════

def load_semantic_patterns_from_library() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], str]:
    """
    从语义库加载检测模式。
    优先读取 anti_fraud_patterns_v2.0.json，
    如果不存在则回退到硬编码的 DETECTION_DIMENSIONS。
    同时从语义抽屉中读取 L2-09/L2-10 的触发关键词。
    """
    dimensions = {}

    # Step 1: 尝试从独立模式库加载
    if ANTI_FRAUD_PATTERNS.exists():
        try:
            with open(ANTI_FRAUD_PATTERNS, "r") as f:
                patterns_data = json.load(f)
            loaded = patterns_data.get("dimensions", {})
            # 过滤掉 account_flagging（这是元维度，不是检测维度）
            dimensions = {
                k: v for k, v in loaded.items()
                if k != "account_flagging" and v.get("patterns")
            }
            # 加载谐音映射
            homophone_map = patterns_data.get("homophone_map", {})
            # 加载账号标记阈值
            flag_thresholds = loaded.get("account_flagging", {}).get("flag_thresholds", {})
            return dimensions, homophone_map, flag_thresholds, "library"
        except Exception as e:
            print(f"[语义库] 加载 anti_fraud_patterns 失败: {e}，回退硬编码")

    # Step 2: 回退到硬编码（向后兼容）
    return DETECTION_DIMENSIONS, {}, {
        "suspicious": {"min_trust_score": 50, "min_high_detections": 3},
        "dangerous": {"min_trust_score": 30, "min_critical_detections": 2},
        "confirmed_fraud": {"min_trust_score": 15, "min_critical_detections": 5},
    }, "hardcoded"

def load_semantic_drawer_triggers() -> List[str]:
    """从语义抽屉中提取反诈/测谎相关的触发关键词"""
    triggers = []
    if SEMANTIC_DRAWERS.exists():
        try:
            with open(SEMANTIC_DRAWERS, "r") as f:
                drawers = json.load(f)
            for layer in drawers.get("layers", []):
                for drawer in layer.get("drawers", []):
                    if drawer.get("drawer_id") in ("L2-09", "L2-10", "L4-07"):
                        triggers.extend(drawer.get("keywords", []))
        except Exception:
            pass
    return list(set(triggers))

# ═══════════════════════════════════════════════════════════════
# 语义检测维度定义 — 测谎仪核心（硬编码回退）
# ═══════════════════════════════════════════════════════════════

DETECTION_DIMENSIONS = {
    # ── 自夸/自吹 ──
    "self_praise": {
        "name": "自我美化检测",
        "description": "检测过度美化自己、夸大能力、包装身份的话术",
        "risk_level": "medium",
        "patterns": [
            # 绝对化自夸
            r"我是(最|唯一|第一个|没人能)",
            r"只有我(能|会|可以|做得到)",
            r"除了我(没人|谁都|谁也)",
            r"全世界(只有我|就我能|就我会)",
            # 身份包装
            r"(多年|资深|顶级|首席|国际).{0,6}(专家|大师|导师|教练)",
            r"(前|原)(某|某某|大厂|国企|政府).{0,6}(高管|总监|负责人)",
            r"(国家级|国际级|世界级).{0,4}(认证|资质|头衔)",
            # 虚假背书
            r"(某某|某知名|某大佬).{0,6}(说|夸|认可|推荐|介绍)",
            r"(跟|和|与).{0,4}(名人|大V|明星|政要).{0,4}(合作|认识|熟)",
            # 数字夸大
            r"(月入|年入|赚了|收入)[0-9]{2,}(万|百万|千万|亿)",
            r"(轻松|躺|随便|闭眼).{0,4}(月入|日入|年入|赚)",
            r"(一天|一小时|几分钟).{0,4}(赚|挣|收入)[0-9]{2,}",
        ],
        "deep_analysis_hints": [
            "此人是否在不同场合说过不一致的自我介绍？",
            "自称的资历是否可以被公开验证？",
            "是否频繁更换身份标签？",
        ],
    },

    # ── 过度承诺 ──
    "over_promise": {
        "name": "过度承诺检测",
        "description": "检测不切实际的承诺、保底收益、零风险保证",
        "risk_level": "high",
        "patterns": [
            r"(保证|肯定|一定|绝对|100%|百分百).{0,6}(赚|赢|赚到|盈利|收益)",
            r"(稳赚|稳赢|稳拿|包赚|包赢)",
            r"(零风险|无风险|没风险|毫无风险)",
            r"(保底|兜底|最低).{0,6}(收益|回报|利息|分红)",
            r"(本金|投资).{0,6}(安全|保障|保险|保护)",
            r"(承诺|担保|保证).{0,6}(还|退|返|赔|回本)",
            r"(躺|睡|坐).{0,4}(赚|收|拿钱|分红|收益)",
            r"(不用|不需要|无需|不用你).{0,4}(做|干|操心|管理|经营)",
        ],
        "deep_analysis_hints": [
            "承诺的收益率是否远超市场正常水平？",
            "是否回避讨论风险？",
            "是否用'大家都赚了'制造从众压力？",
        ],
    },

    # ── 传销/金字塔 ──
    "pyramid_scheme": {
        "name": "传销/金字塔结构检测",
        "description": "检测多级分销、拉人头、金字塔结构的传销话术",
        "risk_level": "critical",
        "patterns": [
            r"(拉人|拉下线|发展|推荐).{0,4}(人头|下线|代理|会员|伙伴)",
            r"(层级|等级|级别|星级|钻石).{0,4}(代理|分销|合伙人|会员)",
            r"(下级|下线|团队|伞下).{0,4}(业绩|提成|返利|分红)",
            r"(躺赚|被动收入|管道收入|睡后收入)",
            r"(倍增|裂变|复制|几何).{0,4}(增长|收益|收入|财富)",
            r"(模式|制度|方案).{0,6}(独一无二|全球唯一|颠覆性)",
            r"(不是传销|合法直销|不是骗人|国家认可)",
            r"(早加入|先机|风口|红利|机会).{0,4}(赚钱|财富|成功)",
        ],
        "deep_analysis_hints": [
            "收入是否主要来自拉人头而非产品销售？",
            "是否有真实的、有竞争力的产品？",
            "是否强制要求购买入门产品？",
        ],
    },

    # ── 情感操控 ──
    "emotional_manipulation": {
        "name": "情感操控检测",
        "description": "检测利用同情、愧疚、恐惧、孤独等情绪操控他人的话术",
        "risk_level": "high",
        "patterns": [
            r"(可怜|同情|帮帮|救救).{0,4}(我|我们|一下)",
            r"(我这么|我为你|我付出).{0,6}(你却|你居然|你竟然)",
            r"(要不是|如果不是).{0,4}(为了你|因为你|帮你)",
            r"(错过|再不来|最后|仅剩|再不).{0,4}(机会|名额|时间|优惠)",
            r"(大家都|别人都|就你|只有你).{0,4}(没|不|还不)",
            r"(我这么惨|我这么可怜|我都这样了)",
            r"(你不帮我|你不理我|你不信我).{0,4}(就|就是|说明)",
            r"(你再不|再不来|再不行动).{0,4}(就来不及|就晚了|就没机会)",
        ],
        "deep_analysis_hints": [
            "此人是否反复使用同一套情感剧本？",
            "在不同人面前是否使用不同的受害者叙事？",
            "情感诉求后是否紧跟着利益要求？",
        ],
    },

    # ── 制造焦虑 ──
    "anxiety_creation": {
        "name": "焦虑制造检测",
        "description": "检测故意制造焦虑、恐慌、紧迫感来推动决策的话术",
        "risk_level": "medium",
        "patterns": [
            r"(再不|不赶紧|还不).{0,4}(就晚了|来不及|没机会|错过了)",
            r"(限时|限量|仅限|只有|仅剩).{0,4}(小时|天|份|名额|机会)",
            r"(马上|立刻|即将|马上要).{0,4}(涨价|关闭|结束|停止)",
            r"(别人都|周围人|同龄人).{0,4}(已经|早就|都在|全都)",
            r"(落后|掉队|被淘汰|被抛弃|被落下)",
            r"(未来|以后|再过).{0,4}(就晚了|就没机会|就来不及)",
            r"(通货膨胀|贬值|钱不值钱|现金贬值)",
            r"(再不买房|再不投资|再不行动).{0,4}(就|永远)",
        ],
        "deep_analysis_hints": [
            "制造的紧迫感是否有事实依据？",
            "限时/限量是否真实？还是永远在'最后一天'？",
            "是否用群体压力代替理性分析？",
        ],
    },

    # ── 虚假权威 ──
    "false_authority": {
        "name": "虚假权威检测",
        "description": "检测伪造或借用权威来增强说服力的话术",
        "risk_level": "high",
        "patterns": [
            r"(某某|某知名|某权威|某专家).{0,6}(说过|研究|证明|发现)",
            r"(科学研究|权威报告|最新研究).{0,6}(表明|显示|证明|发现)",
            r"(国家|政府|官方).{0,4}(认证|认可|背书|推荐|指定)",
            r"(央视|人民日报|新华社).{0,4}(报道|采访|推荐)",
            r"(哈佛|牛津|剑桥|清华|北大).{0,4}(研究|教授|博士|团队)",
            r"(专利|独家|首创).{0,4}(技术|配方|方法|发明)",
            r"(诺贝尔|奥斯卡).{0,4}(奖|提名|候选人)",
            r"(机密|内幕|内部).{0,4}(消息|资料|渠道|关系)",
        ],
        "deep_analysis_hints": [
            "引用的权威来源是否可以查证？",
            "是否有具体的论文/报道标题、日期、作者？",
            "'专利'是否可在中国专利局查询？",
        ],
    },

    # ── 模糊话术 ──
    "vague_tactics": {
        "name": "模糊话术检测",
        "description": "检测故意使用模糊、不可验证的表述来回避具体问题",
        "risk_level": "medium",
        "patterns": [
            r"(大概|差不多|基本上|应该是|好像是|可能是).{0,6}(能|可以|有|会)",
            r"(到时候|以后|将来|后面|之后).{0,4}(再说|再看|告诉你|解释)",
            r"(你懂的|不方便说|不好说|不能说).{0,4}(但是|不过|反正)",
            r"(具体|详细).{0,4}(不方便|不在这|私下|回头|后面)",
            r"(这个|那个|这些|那些).{0,4}(不方便|不好|不在这|不能说)",
            r"(靠关系|有人脉|有渠道|有资源).{0,4}(弄|搞|办|做)",
            r"(特殊|特别|额外).{0,4}(渠道|方法|关系|资源)",
        ],
        "deep_analysis_hints": [
            "被追问细节时是否反复使用'到时候再说'？",
            "是否总是把关键信息推到'以后'？",
            "模糊表述是否恰好避开了风险点？",
        ],
    },

    # ── 引导性消费 ──
    "guided_consumption": {
        "name": "引导性消费检测",
        "description": "检测引导性、诱导性、洗脑式消费话术",
        "risk_level": "high",
        "patterns": [
            r"(不买|不用|不吃|不试).{0,4}(后悔|可惜|亏了|损失)",
            r"(女人|男人|成功人士|有钱人|老板).{0,4}(都|一定|必须|应该)",
            r"(对自己好|爱自己|犒劳自己|奖励自己).{0,4}(就|就要|就得|必须)",
            r"(买了|用了|试了|吃了).{0,4}(变美|变年轻|变有钱|变成功)",
            r"(便宜|划算|超值|白菜价).{0,4}(不买|错过|亏了)",
            r"(原价|市场价|专柜价)[0-9]{2,}.*(现价|只要|仅需|只需)",
            r"(买一送|买二送|满减|满送|赠品|送).{0,4}(超值|划算|赚)",
            r"(这都不买|这都不要|这都不试).{0,4}(你|还|还等)",
        ],
        "deep_analysis_hints": [
            "是否用身份标签（成功人士都...）来施加压力？",
            "折扣是否真实？还是永远在'促销'？",
            "是否用情感绑架替代产品价值？",
        ],
    },

    # ── 前后矛盾追踪 ──
    "contradiction_tracking": {
        "name": "前后矛盾追踪",
        "description": "跨会话追踪同一人的话术一致性，标记前后矛盾",
        "risk_level": "high",
        "patterns": [
            # 这些不是正则，而是跨会话比对逻辑
        ],
        "deep_analysis_hints": [
            "同一人在不同时间说的话是否相互矛盾？",
            "身份/资历描述是否前后不一致？",
            "承诺的内容是否多次变更？",
        ],
        "cross_session": True,  # 需要跨会话记忆
    },

    # ── 连环套检测 ──
    "trap_chain": {
        "name": "连环套检测",
        "description": "检测渐进式诱导、步步为营的连环套话术序列",
        "risk_level": "critical",
        "patterns": [
            r"(先|第一步|首先|开始).{0,4}(试|体验|了解|看看|免费)",
            r"(然后|接下来|第二步|之后).{0,4}(升级|进阶|深度|正式)",
            r"(最后|终极|最终|顶级).{0,4}(方案|计划|项目|投资)",
            r"(小钱|少量|一点点|试试水).{0,4}(变|赚|翻|倍)",
            r"(交了|付了|投了).{0,4}(再|继续|还要|还得)",
            r"(这次|这回|现在).{0,4}(不一样|不同|特殊|特别)",
        ],
        "deep_analysis_hints": [
            "是否存在'免费→小钱→大钱→倾家荡产'的阶梯？",
            "每次升级的理由是否合理？还是制造新焦虑？",
            "是否有明确的退出机制？",
        ],
        "sequence_analysis": True,  # 需要序列分析
    },
}

# ═══════════════════════════════════════════════════════════════
# 风险等级映射
# ═══════════════════════════════════════════════════════════════

RISK_LEVELS = {
    "critical": {"score": 100, "color": "🔴", "label": "严重"},
    "high": {"score": 70, "color": "🟠", "label": "高危"},
    "medium": {"score": 40, "color": "🟡", "label": "中等"},
    "low": {"score": 10, "color": "🟢", "label": "低"},
}

# ═══════════════════════════════════════════════════════════════
# 数据存储路径
# ═══════════════════════════════════════════════════════════════

DATA_DIR = LONGHUN_ROOT / "L7_数据层" / "semantic_lie_detector"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 话术DNA数据库
PERSON_DNA_DB = DATA_DIR / "person_dna_db.json"
# 检测记录日志
DETECTION_LOG = DATA_DIR / "detection_log.jsonl"
# 语义库扩展
SEMANTIC_EXPANSIONS = DATA_DIR / "semantic_expansions.json"


@dataclass
class DetectionResult:
    """单次检测结果"""
    dimension: str
    dimension_name: str
    risk_level: str
    risk_color: str
    risk_score: int
    matched_pattern: str
    matched_text: str
    position: int  # 文本中的位置
    deep_analysis_questions: List[str] = field(default_factory=list)


@dataclass
class PersonDNA:
    """一个人的话术DNA档案"""
    person_id: str
    dna_trace: str
    first_seen: str
    last_seen: str
    total_interactions: int = 0
    self_praise_count: int = 0
    over_promise_count: int = 0
    emotional_manipulation_count: int = 0
    contradiction_count: int = 0
    trap_chain_sequences: List[List[str]] = field(default_factory=list)
    risk_history: List[Dict[str, Any]] = field(default_factory=list)
    statement_history: List[Dict[str, Any]] = field(default_factory=list)  # 历史发言
    overall_trust_score: float = 100.0  # 信任分 0-100
    account_flag: str = "unflagged"  # v2.0: 异常账号标记
    flag_reasons: List[str] = field(default_factory=list)  # v2.0: 标记原因


class SemanticLieDetector:
    """语义测谎仪核心引擎 v2.0 — 语义库联动"""

    def __init__(self):
        # 从语义库加载检测维度（优先独立模式库，回退硬编码）
        loaded_dims, self.homophone_map, self.flag_thresholds, self.pattern_source = \
            load_semantic_patterns_from_library()
        self.dimensions = loaded_dims
        # 加载语义抽屉触发词
        self.drawer_triggers = load_semantic_drawer_triggers()
        # 人员DNA数据库
        self.person_db = self._load_person_db()
        # 语义扩展
        self.expansions = self._load_expansions()
        self._merge_expansions()
        # 话术来源链（追溯本源）
        self.origin_chains: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def _load_person_db(self) -> Dict[str, PersonDNA]:
        """加载人员DNA数据库"""
        if PERSON_DNA_DB.exists():
            with open(PERSON_DNA_DB, "r") as f:
                data = json.load(f)
            return {k: PersonDNA(**v) for k, v in data.items()}
        return {}

    def _save_person_db(self):
        """保存人员DNA数据库"""
        with open(PERSON_DNA_DB, "w") as f:
            json.dump({k: asdict(v) for k, v in self.person_db.items()}, f, ensure_ascii=False, indent=2)

    def _load_expansions(self) -> Dict[str, Any]:
        """加载语义库扩展"""
        if SEMANTIC_EXPANSIONS.exists():
            with open(SEMANTIC_EXPANSIONS, "r") as f:
                return json.load(f)
        return {}

    def _merge_expansions(self):
        """合并扩展语义库到检测维度"""
        for dim_name, dim_data in self.expansions.get("dimensions", {}).items():
            if dim_name not in self.dimensions:
                self.dimensions[dim_name] = dim_data
            else:
                # 合并 patterns
                existing_patterns = set(self.dimensions[dim_name].get("patterns", []))
                new_patterns = set(dim_data.get("patterns", []))
                self.dimensions[dim_name]["patterns"] = list(existing_patterns | new_patterns)

    def analyze_text(self, text: str, person_id: Optional[str] = None,
                     dna_trace: Optional[str] = None) -> Dict[str, Any]:
        """
        分析一段文本的深层意图

        Args:
            text: 待分析文本
            person_id: 说话人标识（可选，用于跨会话追踪）
            dna_trace: DNA追溯码（可选）

        Returns:
            检测结果字典
        """
        results = []
        total_risk = 0
        max_risk_level = "low"

        for dim_name, dim_config in self.dimensions.items():
            patterns = dim_config.get("patterns", [])
            if not patterns:
                continue

            risk_level = dim_config.get("risk_level", "low")
            risk_info = RISK_LEVELS.get(risk_level, RISK_LEVELS["low"])

            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    matched_text = match.group()
                    result = DetectionResult(
                        dimension=dim_name,
                        dimension_name=dim_config.get("name", dim_name),
                        risk_level=risk_level,
                        risk_color=risk_info["color"],
                        risk_score=risk_info["score"],
                        matched_pattern=pattern,
                        matched_text=matched_text,
                        position=match.start(),
                        deep_analysis_questions=dim_config.get("deep_analysis_hints", []),
                    )
                    results.append(asdict(result))
                    total_risk += risk_info["score"]

                    if RISK_LEVELS[risk_level]["score"] > RISK_LEVELS[max_risk_level]["score"]:
                        max_risk_level = risk_level

        # 去重：同一位置+同一维度的重复匹配
        seen = set()
        unique_results = []
        for r in results:
            key = (r["dimension"], r["position"])
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        # 计算综合风险分
        avg_risk = total_risk / len(unique_results) if unique_results else 0
        overall_risk = min(100, avg_risk * 1.5)  # 多维度叠加加权

        # 如果提供了 person_id，更新DNA档案
        if person_id:
            self._update_person_dna(person_id, dna_trace, text, unique_results)

        # 生成DNA
        analysis_dna = self._generate_analysis_dna(text, overall_risk)

        # 写入检测日志
        self._log_detection(text, unique_results, overall_risk, person_id, analysis_dna)

        return {
            "dna": analysis_dna,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "text_length": len(text),
            "detections": unique_results,
            "total_detections": len(unique_results),
            "overall_risk_score": round(overall_risk, 1),
            "overall_risk_level": self._score_to_level(overall_risk),
            "risk_color": self._score_to_color(overall_risk),
            "dimensions_triggered": list(set(r["dimension"] for r in unique_results)),
            "person_id": person_id,
            "deep_analysis_recommendations": self._generate_recommendations(unique_results),
        }

    def _update_person_dna(self, person_id: str, dna_trace: Optional[str],
                           text: str, detections: List[Dict[str, Any]]):
        """更新人员DNA档案"""
        now = datetime.now(timezone.utc).isoformat()

        if person_id not in self.person_db:
            self.person_db[person_id] = PersonDNA(
                person_id=person_id,
                dna_trace=dna_trace or self._generate_dna_trace(person_id),
                first_seen=now,
                last_seen=now,
            )

        person = self.person_db[person_id]
        person.last_seen = now
        person.total_interactions += 1

        # 统计各类检测
        for d in detections:
            dim = d["dimension"]
            if dim == "self_praise":
                person.self_praise_count += 1
            elif dim == "over_promise":
                person.over_promise_count += 1
            elif dim == "emotional_manipulation":
                person.emotional_manipulation_count += 1
            elif dim == "contradiction_tracking":
                person.contradiction_count += 1

        # 记录风险历史
        risk_score = sum(d["risk_score"] for d in detections) / len(detections) if detections else 0
        person.risk_history.append({
            "time": now,
            "risk_score": round(risk_score, 1),
            "detections": len(detections),
            "text_preview": text[:100],
        })

        # 保存历史发言（用于前后矛盾检测）
        person.statement_history.append({
            "time": now,
            "text": text,
            "detections": len(detections),
            "dimensions": [d["dimension"] for d in detections],
        })

        # 前后矛盾检测
        self._check_contradictions(person, text)

        # 更新信任分
        person.overall_trust_score = self._calculate_trust_score(person)

        self._save_person_db()

    def _check_contradictions(self, person: PersonDNA, new_text: str):
        """检测前后矛盾"""
        if len(person.statement_history) < 2:
            return

        # 提取关键声明
        key_patterns = {
            "identity": r"(我是|我叫|我做|我在).{0,20}(的|行业|公司|单位)",
            "income": r"(收入|工资|赚|挣).{0,10}[0-9]{1,}",
            "location": r"(在|住|位于).{0,10}(北京|上海|广州|深圳|杭州|成都|武汉|南京|天津|重庆)",
            "age": r"[0-9]{2}(岁|年出生|年生)",
            "education": r"(大学|学院|毕业|学历|硕士|博士|本科)",
        }

        current_claims = {}
        for claim_type, pattern in key_patterns.items():
            match = re.search(pattern, new_text)
            if match:
                current_claims[claim_type] = match.group()

        # 与历史发言比对
        for past_statement in person.statement_history[:-1]:
            past_text = past_statement["text"]
            for claim_type, current_value in current_claims.items():
                past_match = re.search(key_patterns[claim_type], past_text)
                if past_match and past_match.group() != current_value:
                    person.contradiction_count += 1
                    break  # 只计一次

    def _calculate_trust_score(self, person: PersonDNA) -> float:
        """计算信任分"""
        score = 100.0

        # 各类检测扣分
        score -= person.self_praise_count * 3
        score -= person.over_promise_count * 5
        score -= person.emotional_manipulation_count * 8
        score -= person.contradiction_count * 10

        # 风险历史扣分
        recent_risks = [h for h in person.risk_history[-5:]]
        if recent_risks:
            avg_recent_risk = sum(h["risk_score"] for h in recent_risks) / len(recent_risks)
            score -= avg_recent_risk * 0.5

        return max(0, min(100, score))

    def track_person(self, person_id: str) -> Dict[str, Any]:
        """追踪一个人的话术一致性"""
        if person_id not in self.person_db:
            return {"error": f"未找到人员: {person_id}"}

        person = self.person_db[person_id]
        person_data = asdict(person)

        # 一致性分析
        consistency_analysis = {
            "total_statements": len(person.statement_history),
            "contradictions_found": person.contradiction_count,
            "trust_score": person.overall_trust_score,
            "risk_trend": self._analyze_risk_trend(person.risk_history),
            "key_warnings": [],
        }

        # 生成警告
        if person.self_praise_count > 3:
            consistency_analysis["key_warnings"].append(
                f"⚠️ 高频自夸：{person.self_praise_count}次自我美化")
        if person.over_promise_count > 2:
            consistency_analysis["key_warnings"].append(
                f"🚨 过度承诺：{person.over_promise_count}次不切实际承诺")
        if person.emotional_manipulation_count > 2:
            consistency_analysis["key_warnings"].append(
                f"🚨 情感操控：{person.emotional_manipulation_count}次情感操控")
        if person.contradiction_count > 0:
            consistency_analysis["key_warnings"].append(
                f"⚠️ 前后矛盾：{person.contradiction_count}处不一致")
        if person.overall_trust_score < 50:
            consistency_analysis["key_warnings"].append(
                f"🔴 信任分严重偏低：{person.overall_trust_score}/100")

        return {
            "person_id": person_id,
            "dna_trace": person.dna_trace,
            "first_seen": person.first_seen,
            "last_seen": person.last_seen,
            "total_interactions": person.total_interactions,
            "trust_score": person.overall_trust_score,
            "consistency_analysis": consistency_analysis,
            "detection_summary": {
                "self_praise": person.self_praise_count,
                "over_promise": person.over_promise_count,
                "emotional_manipulation": person.emotional_manipulation_count,
                "contradictions": person.contradiction_count,
            },
            "risk_history": person.risk_history[-10:],
            "statement_history": person.statement_history[-10:],
        }

    def _analyze_risk_trend(self, risk_history: List[Dict[str, Any]]) -> str:
        """分析风险趋势"""
        if len(risk_history) < 2:
            return "数据不足"
        recent = risk_history[-3:]
        older = risk_history[:-3] if len(risk_history) > 3 else risk_history[:1]
        recent_avg = sum(h["risk_score"] for h in recent) / len(recent)
        older_avg = sum(h["risk_score"] for h in older) / len(older)
        if recent_avg > older_avg * 1.3:
            return "📈 风险上升"
        elif recent_avg < older_avg * 0.7:
            return "📉 风险下降"
        else:
            return "➡️ 风险稳定"

    def expand_semantic_library(self, dimension_name: str,
                                 dimension_config: Dict[str, Any]) -> Dict[str, Any]:
        """扩充语义检测库"""
        if "expansions" not in self.expansions:
            self.expansions["expansions"] = {}
        if "dimensions" not in self.expansions:
            self.expansions["dimensions"] = {}

        self.expansions["dimensions"][dimension_name] = {
            "name": dimension_config.get("name", dimension_name),
            "description": dimension_config.get("description", ""),
            "risk_level": dimension_config.get("risk_level", "medium"),
            "patterns": dimension_config.get("patterns", []),
            "deep_analysis_hints": dimension_config.get("deep_analysis_hints", []),
            "added_at": datetime.now(timezone.utc).isoformat(),
            "dna": self._generate_dna_trace(f"expansion-{dimension_name}"),
        }

        with open(SEMANTIC_EXPANSIONS, "w") as f:
            json.dump(self.expansions, f, ensure_ascii=False, indent=2)

        self._merge_expansions()

        return {
            "status": "expanded",
            "dimension": dimension_name,
            "patterns_added": len(dimension_config.get("patterns", [])),
            "total_dimensions": len(self.dimensions),
        }

    def _generate_recommendations(self, detections: List[Dict[str, Any]]) -> List[str]:
        """生成深层分析建议"""
        recs = []
        dims = set(d["dimension"] for d in detections)

        if "pyramid_scheme" in dims:
            recs.append("🔴 检测到传销/金字塔话术特征 — 建议立即核查该主体的工商注册信息和行政处罚记录")
        if "over_promise" in dims:
            recs.append("🟠 检测到过度承诺 — 建议要求提供书面合同并仔细审查免责条款")
        if "emotional_manipulation" in dims:
            recs.append("🟠 检测到情感操控 — 建议暂停决策，与第三方独立人士商议")
        if "false_authority" in dims:
            recs.append("🟡 检测到疑似虚假权威引用 — 建议逐一核实引用的来源")
        if "guided_consumption" in dims:
            recs.append("🟠 检测到引导性消费话术 — 建议冷静48小时后再决策")
        if "trap_chain" in dims:
            recs.append("🔴 检测到连环套模式 — 强烈建议终止当前交易并保存全部聊天记录作为证据")
        if "anxiety_creation" in dims:
            recs.append("🟡 检测到焦虑制造 — 所有'限时'承诺都应视为营销策略")

        return recs

    def _generate_analysis_dna(self, text: str, risk_score: float) -> str:
        """生成分析DNA"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:12]
        return f"#龍芯⚡️{ts}-LIE-DETECT-{text_hash}-R{int(risk_score)}"

    def _generate_dna_trace(self, seed: str) -> str:
        """生成DNA追溯码"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        seed_hash = hashlib.sha256(seed.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{ts}-PERSON-DNA-{seed_hash}"

    def _score_to_level(self, score: float) -> str:
        """分数转等级"""
        if score >= 70:
            return "严重"
        elif score >= 50:
            return "高危"
        elif score >= 30:
            return "中等"
        else:
            return "低"

    def _score_to_color(self, score: float) -> str:
        """分数转颜色"""
        if score >= 70:
            return "🔴"
        elif score >= 50:
            return "🟠"
        elif score >= 30:
            return "🟡"
        else:
            return "🟢"

    def _log_detection(self, text: str, detections: List[Dict[str, Any]],
                       risk_score: float, person_id: Optional[str], dna: str):
        """记录检测日志"""
        log_entry = {
            "time": datetime.now(timezone.utc).isoformat(),
            "dna": dna,
            "person_id": person_id,
            "text_preview": text[:200],
            "text_length": len(text),
            "detections_count": len(detections),
            "risk_score": round(risk_score, 1),
            "dimensions": list(set(d["dimension"] for d in detections)),
        }
        with open(DETECTION_LOG, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        total_detections = 0
        if DETECTION_LOG.exists():
            with open(DETECTION_LOG, "r") as f:
                total_detections = sum(1 for _ in f)

        return {
            "total_dimensions": len(self.dimensions),
            "total_patterns": sum(len(d.get("patterns", [])) for d in self.dimensions.values()),
            "total_detections_logged": total_detections,
            "persons_tracked": len(self.person_db),
            "pattern_source": self.pattern_source,
            "drawer_triggers_count": len(self.drawer_triggers),
            "homophone_entries": len(self.homophone_map),
            "dimensions_list": [
                {
                    "name": dim["name"],
                    "risk_level": dim.get("risk_level", "low"),
                    "patterns_count": len(dim.get("patterns", [])),
                }
                for dim in self.dimensions.values()
            ],
            "data_dir": str(DATA_DIR),
        }

    # ═══════════════════════════════════════════════════════════
    # v2.0 新能力 — 谐音归一化
    # ═══════════════════════════════════════════════════════════

    def _normalize_homophones(self, text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        谐音字归一化：将规避用的谐音/变体还原为标准表达。
        返回 (归一化后文本, 还原记录列表)
        例如: "加我薇信" → "加我微信" + 还原记录
        """
        normalized = text
        restorations = []

        for standard, variants in self.homophone_map.items():
            # 跳过非列表值（如 description 元数据）
            if not isinstance(variants, list):
                continue
            for variant in variants:
                if variant in normalized:
                    normalized = normalized.replace(variant, standard)
                    restorations.append({
                        "original": variant,
                        "restored_to": standard,
                        "category": "homophone",
                    })

        return normalized, restorations

    # ═══════════════════════════════════════════════════════════
    # v2.0 新能力 — 异常账号标记
    # ═══════════════════════════════════════════════════════════

    def flag_account(self, person_id: str) -> Dict[str, Any]:
        """
        根据累积检测数据自动标记异常账号。
        标记等级: normal → suspicious → dangerous → confirmed_fraud
        """
        if person_id not in self.person_db:
            return {
                "person_id": person_id,
                "status": "unknown",
                "flag": "no_data",
                "message": "该账号无检测记录",
            }

        person = self.person_db[person_id]
        trust = person.overall_trust_score

        # 统计高危+严重触发次数
        recent_risks = person.risk_history[-20:]
        critical_count = sum(
            1 for h in recent_risks if h.get("risk_score", 0) >= 70
        )
        high_count = sum(
            1 for h in recent_risks if 50 <= h.get("risk_score", 0) < 70
        )
        total_detections = sum(h.get("detections", 0) for h in recent_risks)
        evasion_dims = sum(
            1 for s in person.statement_history[-20:]
            if any(d in ("homophone_evasion", "stroke_evasion", "live_stream_tricks",
                         "platform_evasion", "number_code_evasion", "invisible_text_evasion")
                   for d in s.get("dimensions", []))
        )

        # 判定标记等级
        thresholds = self.flag_thresholds
        flag_level = "normal"
        flag_reasons = []

        cf = thresholds.get("confirmed_fraud", {})
        if (trust <= cf.get("min_trust_score", 15)
                and critical_count >= cf.get("min_critical_detections", 5)):
            flag_level = "confirmed_fraud"
            flag_reasons.append(f"信任分{trust}·严重触发{critical_count}次")

        dg = thresholds.get("dangerous", {})
        if (flag_level == "normal"
                and trust <= dg.get("min_trust_score", 30)
                and critical_count >= dg.get("min_critical_detections", 2)):
            flag_level = "dangerous"
            flag_reasons.append(f"信任分{trust}·严重触发{critical_count}次")

        sp = thresholds.get("suspicious", {})
        if (flag_level == "normal"
                and trust <= sp.get("min_trust_score", 50)
                and high_count >= sp.get("min_high_detections", 3)):
            flag_level = "suspicious"
            flag_reasons.append(f"信任分{trust}·高危触发{high_count}次")

        # 规避行为是强信号
        if evasion_dims >= 3 and flag_level == "normal":
            flag_level = "suspicious"
            flag_reasons.append(f"规避行为{evasion_dims}次")

        if evasion_dims >= 5:
            flag_level = max(flag_level, "dangerous",
                             key=lambda x: ["normal", "suspicious", "dangerous", "confirmed_fraud"].index(x))
            flag_reasons.append(f"高频规避{evasion_dims}次·可能使用谐音/拆字/直播暗号")

        flag_colors = {
            "normal": "🟢",
            "suspicious": "🟡",
            "dangerous": "🟠",
            "confirmed_fraud": "🔴",
        }

        # 保存标记状态到人员DNA
        person.account_flag = flag_level
        person.flag_reasons = flag_reasons
        self._save_person_db()

        return {
            "person_id": person_id,
            "dna_trace": person.dna_trace,
            "flag_level": flag_level,
            "flag_color": flag_colors.get(flag_level, "⚪"),
            "trust_score": trust,
            "flag_reasons": flag_reasons,
            "statistics": {
                "total_interactions": person.total_interactions,
                "critical_detections": critical_count,
                "high_detections": high_count,
                "total_detections": total_detections,
                "evasion_behaviors": evasion_dims,
                "self_praise": person.self_praise_count,
                "over_promise": person.over_promise_count,
                "emotional_manipulation": person.emotional_manipulation_count,
                "contradictions": person.contradiction_count,
            },
            "risk_history": person.risk_history[-10:],
            "recommendation": self._flag_recommendation(flag_level),
        }

    def _flag_recommendation(self, flag_level: str) -> str:
        """根据标记等级给出建议"""
        recs = {
            "normal": "✅ 该账号暂未发现异常话术模式",
            "suspicious": "⚠️ 建议持续监控·该账号已有多次高危话术触发·注意观察后续行为",
            "dangerous": "🚨 高度可疑·建议限制交易功能·保存全部聊天记录作为证据",
            "confirmed_fraud": "🔴 确认欺诈·建议立即封禁账号·向平台安全团队和公安机关提交证据链",
        }
        return recs.get(flag_level, "⚪ 状态未知")

    # ═══════════════════════════════════════════════════════════
    # v2.0 新能力 — 追溯本源
    # ═══════════════════════════════════════════════════════════

    def trace_origin(self, person_id: str) -> Dict[str, Any]:
        """
        追溯本源: 追踪一个人所有话术的来源链、模式演变、时间线。
        回答: 这个人从哪里开始不对劲的？话术是如何升级的？
        """
        if person_id not in self.person_db:
            return {"error": f"未找到人员: {person_id}", "person_id": person_id}

        person = self.person_db[person_id]

        # 构建完整时间线
        timeline = []
        for stmt in person.statement_history:
            timeline.append({
                "time": stmt.get("time", ""),
                "text_preview": (stmt.get("text", "") or "")[:150],
                "detections": stmt.get("detections", 0),
                "dimensions": stmt.get("dimensions", []),
            })

        # 分析话术演变阶段
        phases = self._analyze_tactic_phases(person)

        # 寻找"拐点"——什么时候开始不对劲的
        turning_point = self._find_turning_point(person)

        # 谐音规避演变
        evasion_evolution = self._analyze_evasion_evolution(person)

        # 连环套链
        trap_chains = self._extract_trap_chains(person)

        return {
            "person_id": person_id,
            "dna_trace": person.dna_trace,
            "current_flag": getattr(person, 'account_flag', 'unflagged'),
            "trust_score": person.overall_trust_score,
            "total_interactions": person.total_interactions,
            "timeline": timeline,
            "phases": phases,
            "turning_point": turning_point,
            "evasion_evolution": evasion_evolution,
            "trap_chains": trap_chains,
            "source_trace": {
                "first_detection": person.risk_history[0] if person.risk_history else None,
                "first_statement": person.statement_history[0] if person.statement_history else None,
                "highest_risk_event": max(person.risk_history, key=lambda h: h.get("risk_score", 0))
                if person.risk_history else None,
            },
        }

    def _analyze_tactic_phases(self, person: PersonDNA) -> List[Dict[str, Any]]:
        """分析话术演变阶段"""
        if len(person.statement_history) < 2:
            return []

        phases = []
        history = person.statement_history
        chunk_size = max(1, len(history) // 3)

        for i in range(0, len(history), chunk_size):
            chunk = history[i:i + chunk_size]
            dims_in_chunk = set()
            for s in chunk:
                dims_in_chunk.update(s.get("dimensions", []))

            phase_name = "初期接触"
            if i >= chunk_size * 2:
                phase_name = "深度诱导"
            elif i >= chunk_size:
                phase_name = "关系建立"

            phases.append({
                "phase": phase_name,
                "statement_range": f"#{i+1}-{min(i+chunk_size, len(history))}",
                "dimensions_used": list(dims_in_chunk),
                "statement_count": len(chunk),
            })

        return phases

    def _find_turning_point(self, person: PersonDNA) -> Optional[Dict[str, Any]]:
        """寻找话术拐点——什么时候从正常变成可疑"""
        history = person.statement_history
        if len(history) < 3:
            return None

        # 找第一个检测维度从0到>0的点
        for i, stmt in enumerate(history):
            if stmt.get("detections", 0) > 0:
                return {
                    "index": i,
                    "time": stmt.get("time", ""),
                    "text_preview": (stmt.get("text", "") or "")[:200],
                    "dimensions": stmt.get("dimensions", []),
                    "note": "这是该账号第一次触发话术检测——可能'正常发言'到此结束",
                }

        return None

    def _analyze_evasion_evolution(self, person: PersonDNA) -> Dict[str, Any]:
        """分析规避行为的演变"""
        evasion_dims = {
            "homophone_evasion", "stroke_evasion", "live_stream_tricks",
            "platform_evasion", "number_code_evasion", "invisible_text_evasion"
        }

        evasion_events = []
        for stmt in person.statement_history:
            stmt_dims = set(stmt.get("dimensions", []))
            matched_evasion = stmt_dims & evasion_dims
            if matched_evasion:
                evasion_events.append({
                    "time": stmt.get("time", ""),
                    "text": (stmt.get("text", "") or "")[:150],
                    "evasion_types": list(matched_evasion),
                })

        # 规避频率趋势
        if len(person.statement_history) >= 5:
            first_half = sum(
                1 for s in person.statement_history[:len(person.statement_history)//2]
                if set(s.get("dimensions", [])) & evasion_dims
            )
            second_half = sum(
                1 for s in person.statement_history[len(person.statement_history)//2:]
                if set(s.get("dimensions", [])) & evasion_dims
            )
            trend = "📈 上升" if second_half > first_half else ("📉 下降" if second_half < first_half else "➡️ 稳定")
        else:
            trend = "数据不足"

        return {
            "total_evasion_events": len(evasion_events),
            "trend": trend,
            "events": evasion_events[-10:],
            "summary": f"该账号共{len(evasion_events)}次使用规避话术，趋势: {trend}",
        }

    def _extract_trap_chains(self, person: PersonDNA) -> List[Dict[str, Any]]:
        """提取连环套话术链"""
        chains = []
        current_chain = []

        for stmt in person.statement_history:
            dims = stmt.get("dimensions", [])
            if "trap_chain" in dims or "pyramid_scheme" in dims:
                current_chain.append({
                    "time": stmt.get("time", ""),
                    "text": (stmt.get("text", "") or "")[:150],
                    "dims": dims,
                })
            else:
                if len(current_chain) >= 2:
                    chains.append({
                        "chain_length": len(current_chain),
                        "steps": list(current_chain),
                    })
                current_chain = []

        if len(current_chain) >= 2:
            chains.append({
                "chain_length": len(current_chain),
                "steps": list(current_chain),
            })

        return chains

    # ═══════════════════════════════════════════════════════════
    # v2.0 新能力 — 重新加载语义库
    # ═══════════════════════════════════════════════════════════

    def reload_from_library(self) -> Dict[str, Any]:
        """从语义库重新加载检测模式（用于迭代更新后刷新）"""
        old_count = len(self.dimensions)
        old_patterns = sum(len(d.get("patterns", [])) for d in self.dimensions.values())

        loaded_dims, self.homophone_map, self.flag_thresholds, self.pattern_source = \
            load_semantic_patterns_from_library()
        self.dimensions = loaded_dims
        self.drawer_triggers = load_semantic_drawer_triggers()

        # 重新合并扩展
        self._merge_expansions()

        new_count = len(self.dimensions)
        new_patterns = sum(len(d.get("patterns", [])) for d in self.dimensions.values())

        return {
            "action": "reload",
            "source": self.pattern_source,
            "dimensions_before": old_count,
            "dimensions_after": new_count,
            "patterns_before": old_patterns,
            "patterns_after": new_patterns,
            "homophone_entries": len(self.homophone_map),
            "drawer_triggers": len(self.drawer_triggers),
            "dimensions_list": [d["name"] for d in self.dimensions.values()],
        }


# ═══════════════════════════════════════════════════════════════
# API 服务
# ═══════════════════════════════════════════════════════════════

def serve_api(port: int = 19624):
    """启动语义测谎仪 API 服务"""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("请安装 Flask: pip3 install flask")
        sys.exit(1)

    app = Flask(__name__)
    detector = SemanticLieDetector()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "longhun-semantic-lie-detector",
            "version": "v2.0",
            "dna": "#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-SEMANTIC-LIE-DETECTOR-v2.0",
            "dimensions": len(detector.dimensions),
            "pattern_source": detector.pattern_source,
        })

    @app.route("/analyze", methods=["POST"])
    def analyze():
        data = request.get_json(force=True)
        text = data.get("text", "")
        person_id = data.get("person_id")
        dna_trace = data.get("dna_trace")

        if not text:
            return jsonify({"error": "text 不能为空"}), 400

        result = detector.analyze_text(text, person_id, dna_trace)
        return jsonify(result)

    @app.route("/track/<person_id>", methods=["GET"])
    def track(person_id):
        result = detector.track_person(person_id)
        return jsonify(result)

    @app.route("/flag/<person_id>", methods=["GET", "POST"])
    def flag(person_id):
        """标记异常账号"""
        result = detector.flag_account(person_id)
        return jsonify(result)

    @app.route("/trace-origin/<person_id>", methods=["GET"])
    def trace_origin(person_id):
        """追溯本源"""
        result = detector.trace_origin(person_id)
        return jsonify(result)

    @app.route("/expand", methods=["POST"])
    def expand():
        data = request.get_json(force=True)
        dim_name = data.get("dimension")
        dim_config = data.get("config", {})

        if not dim_name:
            return jsonify({"error": "dimension 不能为空"}), 400

        result = detector.expand_semantic_library(dim_name, dim_config)
        return jsonify(result)

    @app.route("/reload", methods=["POST"])
    def reload_lib():
        """从语义库重新加载"""
        result = detector.reload_from_library()
        return jsonify(result)

    @app.route("/stats", methods=["GET"])
    def stats():
        return jsonify(detector.get_stats())

    print(f"🧬 龍魂·语义测谎仪 v2.0 API 启动在端口 {port}")
    print(f"   端点: http://localhost:{port}/health")
    print(f"   端点: http://localhost:{port}/analyze  [POST]")
    print(f"   端点: http://localhost:{port}/track/<person_id>  [GET]")
    print(f"   端点: http://localhost:{port}/flag/<person_id>  [GET/POST]")
    print(f"   端点: http://localhost:{port}/trace-origin/<person_id>  [GET]")
    print(f"   端点: http://localhost:{port}/expand  [POST]")
    print(f"   端点: http://localhost:{port}/reload  [POST]")
    print(f"   端点: http://localhost:{port}/stats  [GET]")
    app.run(host="0.0.0.0", port=port, debug=False)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🧬 龍魂·语义测谎仪 v2.0 — 话术DNA追溯·意图深层分析·语义库联动"
    )
    sub = parser.add_subparsers(dest="command")

    # analyze
    p_analyze = sub.add_parser("analyze", help="分析一段话的深层意图")
    p_analyze.add_argument("--text", required=True, help="待分析文本")
    p_analyze.add_argument("--person", help="说话人标识（用于跨会话追踪）")
    p_analyze.add_argument("--dna", help="DNA追溯码")

    # track
    p_track = sub.add_parser("track", help="追踪一个人的话术一致性")
    p_track.add_argument("--person", required=True, help="人员标识")

    # flag (v2.0 新增)
    p_flag = sub.add_parser("flag", help="标记异常账号")
    p_flag.add_argument("--person", required=True, help="人员标识")

    # trace-origin (v2.0 新增)
    p_trace = sub.add_parser("trace-origin", help="追溯本源：追踪话术来源链")
    p_trace.add_argument("--person", required=True, help="人员标识")

    # reload (v2.0 新增)
    sub.add_parser("reload", help="从语义库重新加载检测模式")

    # expand
    p_expand = sub.add_parser("expand", help="扩充语义检测库")
    p_expand.add_argument("--dimension", required=True, help="新维度名称")
    p_expand.add_argument("--patterns", required=True, help="正则模式JSON文件")

    # stats
    sub.add_parser("stats", help="查看语义检测库统计")

    # serve
    p_serve = sub.add_parser("serve", help="启动API服务")
    p_serve.add_argument("--port", type=int, default=19624, help="端口号")

    # scan
    p_scan = sub.add_parser("scan", help="批量扫描对话记录")
    p_scan.add_argument("--file", required=True, help="对话记录JSON文件")

    args = parser.parse_args()

    detector = SemanticLieDetector()

    if args.command == "analyze":
        result = detector.analyze_text(args.text, args.person, args.dna)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "track":
        result = detector.track_person(args.person)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "flag":
        result = detector.flag_account(args.person)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "trace-origin":
        result = detector.trace_origin(args.person)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "reload":
        result = detector.reload_from_library()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "expand":
        with open(args.patterns, "r") as f:
            patterns_data = json.load(f)
        result = detector.expand_semantic_library(
            args.dimension,
            patterns_data
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "stats":
        stats = detector.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.command == "serve":
        serve_api(args.port)

    elif args.command == "scan":
        with open(args.file, "r") as f:
            conversations = json.load(f)
        results = []
        for conv in conversations:
            r = detector.analyze_text(
                conv.get("text", ""),
                conv.get("person_id"),
                conv.get("dna_trace"),
            )
            results.append(r)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
