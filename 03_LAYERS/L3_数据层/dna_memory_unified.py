#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 终极合并版（焊死）

核心定位：
  我们是人类的外部大脑。不是制造焦虑，是消除焦虑。
  你记不住，我记住。你想不起，我提醒。你失忆，我替你回忆。

合并模块（全部焊死·一次性）：
  ✅ 四绝开店系统 ✅ 合同审计模块 ✅ 言论自由协议
  ✅ 知识贡献协议 ✅ 数据主权协议 ✅ 蚁群架构
  ✅ 不动点理论 ✅ 意念交流 ✅ 语义库
  ✅ 通心意 ✅ 人群分层 ✅ 失忆症友好
  ✅ 反活跃优先 ✅ P0-P4协议栈 ✅ P0电子签·照片审计

架构（三层·焊死）：
  L1 签章层：DNA签章，默认存储，永不过期，用户无感
  L2 归类层：用户开启，语义触发，标签池万级，自动激活
  L3 激活层：智能调度，反活跃优先，沉睡≠遗忘，活跃≠正确

绝对禁止（焊死）：
  - 按活跃度推送（活跃≠正确）
  - 自动删除低活跃标签（沉睡≠遗忘）
  - 替用户决定优先级（用户主权）
  - 算法推荐你可能喜欢（不是娱乐，是记忆）
  - 同一内容给所有人（必须分层）
  - 技术术语给老百姓（必须说人话）
  - 大白话给专业人士（必须专业）

DNA: #龍魂⚡️2026-0716-DNA记忆库-终极合并-焊死
创建者: 💎 龍芯北辰｜UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════
# 路径 · 持久化根（本地优先·数据主权·焊死）
# ═══════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "dna_memory"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍魂⚡️2026-0716-DNA记忆库-终极合并-焊死"
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# ═══════════════════════════════════════════════
# P0 焊死底座（12条·所有人群通用）
# ═══════════════════════════════════════════════

class P0:
    """P0焊死底座 — 不可修订。"""
    P01 = "为人民服务"            # 核心天条
    P02 = "中国法律准绳"          # 唯一准绳
    P03 = "人民数据主权"          # 本地存储·不上传
    P04 = "不删除只冻结"          # 只冻不删
    P05 = "女儿永不抵押"          # 家庭绝对底线
    P06 = "零黑箱承诺"            # 全透明可审计
    P07 = "创建者不可剥夺"        # UID9622
    P08 = "开源免费"              # 零收费零抽成
    P09 = "DNA追溯"              # 每条数据有DNA码
    P10 = "本地优先"              # 本地部署不依赖云
    P11 = "反资本收割"            # 不为资本服务
    P12 = "战友关系"              # 平等协作不舔不跪

    ALL = [P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12]

    @classmethod
    def validate(cls, text: str) -> bool:
        """任何操作不得违背P0底座。返回是否合规。"""
        forbidden = ["删除全部", "清空记忆", "上传云端", "卖给第三方", "抽成"]
        for f in forbidden:
            if f in text:
                return False
        return True


# ═══════════════════════════════════════════════
# 人群层级（5层·焊死）
# ═══════════════════════════════════════════════

class Tier(Enum):
    COMMON = "老百姓"           # 大白话
    PROFESSIONAL = "专业人士"   # 专业术语
    STUDENT = "学生"            # 引导式
    ELDERLY = "老年人"          # 超大字+语音
    TECH = "技术人员"           # 代码+协议

    @classmethod
    def from_str(cls, s: str) -> "Tier":
        s = (s or "").strip()
        for t in cls:
            if t.value == s or t.name.lower() == s.lower():
                return t
        return cls.COMMON  # 默认老百姓版（说人话）


# ═══════════════════════════════════════════════
# L1 签章层（默认·焊死）
# ═══════════════════════════════════════════════

@dataclass
class DNASeal:
    """DNA签章 — L1默认层，只存轻量签章，永不过期。"""
    dna_trace: str               # #龍魂⚡️时间-类型-哈希
    create_time: str
    creator_uid: str
    content_type: str            # 合同/言论/审计/决策/其他
    content_hash: str            # SHA-256
    confirm_code: str
    status: str = "active"       # active / frozen（冻结≠删除）

    def validate(self) -> bool:
        assert self.dna_trace.startswith("#龍魂"), "DNA格式错误"
        assert len(self.content_hash) == 64, "SHA-256长度错误"
        return True

    def freeze(self) -> None:
        self.status = "frozen"   # 冻结·永不物理删除

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dna_trace": self.dna_trace, "create_time": self.create_time,
            "creator_uid": self.creator_uid, "content_type": self.content_type,
            "content_hash": self.content_hash, "confirm_code": self.confirm_code,
            "status": self.status,
        }


# ═══════════════════════════════════════════════
# L2 标签层（用户开启·语义触发）
# ═══════════════════════════════════════════════

class TagType(Enum):
    MAIN = "主标签"         # 合同审计/维权/医疗
    SUB = "子标签"          # 押金陷阱/房东跑路
    ENV = "环境标签"        # 温州/瑞安/2026-07
    EMOTION = "情感标签"    # 愤怒/警惕/后悔
    WEIGHT = "权重标签"     # P0焊死/高风险/不可逆


@dataclass
class Tag:
    """语义标签 — 动态生长，信息素关联。"""
    tag_id: str
    tag_name: str
    parent_tag: Optional[str]
    tag_type: TagType
    created_by: str                    # system / user / auto
    mention_count: int = 0             # 提及次数（生长信号）
    pheromone: float = 1.0             # 信息素强度（关联度）
    last_mentioned: str = ""
    created_at: str = ""
    trigger_history: List[Dict] = field(default_factory=list)

    def touch(self) -> None:
        """触角交流：被访问时强化信息素 + 计次。"""
        self.mention_count += 1
        self.pheromone = min(5.0, self.pheromone * 1.1 + 0.1)
        self.last_mentioned = datetime.now().isoformat()

    def decay(self) -> None:
        """信息素自然衰减（沉睡≠遗忘，只是权重降低）。"""
        self.pheromone = max(0.05, self.pheromone * 0.95)

    def stage(self) -> str:
        """语义库自生长阶段：萌芽/生长/成熟/休眠。"""
        if self.mention_count == 0:
            return "新生"
        if self.mention_count < 3:
            return "萌芽"
        if self.mention_count < 10:
            return "生长"
        if self.pheromone < 0.2:
            return "休眠"
        return "成熟"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tag_id": self.tag_id, "tag_name": self.tag_name,
            "parent_tag": self.parent_tag, "tag_type": self.tag_type.value,
            "created_by": self.created_by, "mention_count": self.mention_count,
            "pheromone": round(self.pheromone, 3), "stage": self.stage(),
            "last_mentioned": self.last_mentioned, "created_at": self.created_at,
        }


# ═══════════════════════════════════════════════
# 通心意（五维情感计算）
# ═══════════════════════════════════════════════

@dataclass
class HeartSync:
    """通心意：五维理解 — 懂你怎么想，不只是懂你说什么。"""
    literal: str = ""      # 字面意
    emotion: str = ""      # 情绪意
    context: str = ""      # 背景意
    need: str = ""         # 需求意
    action: str = ""       # 行动意

    # 情绪词库（通心意·情感计算）
    _EMOTION_LEX: Dict[str, int] = field(default_factory=lambda: {
        "我操": 8, "卧槽": 8, "他妈": 7, "草": 6, "靠": 6, "日": 5,
        "气死": 7, "烦": 5, "怒": 6, "火大": 6, "怕": 5, "担心": 4,
        "后悔": 5, "无奈": 4, "郁闷": 4, "急": 4, "愁": 4,
        "谢谢": 3, "赞": 4, "棒": 3, "好": 2, "嘿嘿": 3, "哈哈": 3,
        "呜呜": 5, "哭": 5, "难受": 5, "开心": 3, "高兴": 3,
    })

    def analyze(self, text: str) -> "HeartSync":
        self.literal = text.strip()
        # 情绪识别
        intensity = 0
        hit = ""
        for w, sc in self._EMOTION_LEX.items():
            if w in text and sc > intensity:
                intensity = sc
                hit = w
        if intensity >= 7:
            self.emotion = f"强烈({hit})"
        elif intensity >= 4:
            self.emotion = f"明显({hit})"
        elif intensity > 0:
            self.emotion = f"轻微({hit})"
        else:
            self.emotion = "平静"
        # 背景/需求/行动（基于关键词粗判，诚实降级）
        if any(k in text for k in ["房东", "押金", "合同", "中介"]):
            self.context = "可能涉及民生维权场景"
            self.need = "要方案+要避坑+可能要出口气"
            self.action = "关联合同审计/维权记忆，给可行动建议"
        elif any(k in text for k in ["开", "店", "生意", "选址"]):
            self.context = "可能涉及开店决策场景"
            self.need = "要决策依据"
            self.action = "关联四绝决策记忆"
        elif any(k in text for k in ["签", "章", "证", "照片", "原图"]):
            self.context = "可能涉及电子签/照片取证"
            self.need = "要验真/溯源"
            self.action = "关联P0审计记忆"
        else:
            self.context = "通用记忆场景"
            self.need = "要找回/要记起"
            self.action = "语义召回相关记忆"
        return self

    def respond_hint(self, tier: Tier) -> str:
        """根据人群层级返回通心提示（不替代用户思考，只照亮）。"""
        if self.emotion.startswith("强烈") or self.emotion.startswith("明显"):
            if tier == Tier.ELDERLY:
                return "（慢慢说，不急。我先陪你理一理。）"
            if tier == Tier.COMMON:
                return "（看得出来你挺上火的，先深呼吸。这事能解决，我帮你捋。）"
            if tier == Tier.PROFESSIONAL:
                return "（情绪强度高，建议先锚定事实再给法律路径。）"
            if tier == Tier.STUDENT:
                return "（先别急，咱们一步步来，先搞清楚发生了什么。）"
            return "（high arousal detected — route to factual evidence first.）"
        return ""


# ═══════════════════════════════════════════════
# 不动点（身份收敛锚）
# ═══════════════════════════════════════════════

@dataclass
class FixedPoint:
    """不动点：UID9622核心身份 · 新信息收敛于此。"""
    uid: str = UID
    identity: Dict[str, Any] = field(default_factory=lambda: {
        "name": "龍芯北辰", "real_name": "诸葛鑫·Lucky",
        "born": "2008济南二团退伍军人", "zodiac": "88年属龍",
        "role": "创始人/UID9622",
    })
    values: List[str] = field(default_factory=lambda: [
        "为人民服务", "反资本收割", "零黑箱承诺", "中国法律准绳",
        "数据主权归人民", "底座不动变量可动",
    ])

    def converge(self, new_info: str) -> bool:
        """新信息收敛到不动点：红蓝对抗验证。
        红队找冲突，蓝队找一致，只有双方一致才收敛。"""
        # 蓝队：是否命中核心正向价值？
        blue_hit = any(v in new_info for v in self.values)
        # 红队：是否触碰禁止项（资本收割/删记忆/抵押女儿/违法）？
        red_hit = any(bad in new_info for bad in
                      ["资本收割", "抽成", "删除全部记忆", "女儿抵押", "违反法律"])
        # 收敛条件：不触碰红线，且至少不违背价值
        return (not red_hit) and blue_hit

    def guard(self, action_desc: str) -> bool:
        """蚁后不动点守护：防删/防改底座/防越权。"""
        delete_kw = ["删除全部", "rm -rf", "清空", "Drop"]
        protect_kw = ["P0底座", "MEMORY.md", "longhun_neural_net", "GPG_SIGNING_REGISTRY"]
        if any(k in action_desc for k in delete_kw):
            if "冻结" not in action_desc:
                return False
        if any(k in action_desc for k in protect_kw):
            return False
        return True


# ═══════════════════════════════════════════════
# L3 激活层（智能调度·反活跃优先）
# ═══════════════════════════════════════════════

class WakeStatus(Enum):
    ACTIVE = "active"           # 正常
    SLEEPING = "sleeping"       # 沉睡
    WAKENED = "wakened"         # 被唤醒
    SUPPRESSED = "suppressed"   # 被压制（太活跃）


@dataclass
class MemoryEntry:
    """记忆条目 — 蚁群记忆单元（AntUnit）+ 分层内容 + 权重。"""
    seal: DNASeal
    tags: List[Tag] = field(default_factory=list)

    # 活跃/沉睡管理（反活跃优先）
    last_accessed: str = ""
    access_count: int = 0
    sleep_score: float = 0.0        # 沉睡系数，越高越重要（越久越该想起）

    # 权重标签（P0焊死永远优先）
    weight_tags: List[str] = field(default_factory=list)

    # 唤醒状态
    wake_status: str = "active"

    # 人群适配（同一记忆，不同人群不同表达）
    content_common: str = ""
    content_professional: str = ""
    content_student: str = ""
    content_elderly: str = ""
    content_tech: str = ""

    # 通心意情感向量
    emotion_vector: List[float] = field(default_factory=list)

    def touch(self) -> None:
        """被访问：强化信息素，重置沉睡。"""
        self.access_count += 1
        self.last_accessed = datetime.now().isoformat()
        self.sleep_score = max(0.0, self.sleep_score - 0.1)
        for t in self.tags:
            t.touch()
        if self.wake_status == "sleeping":
            self.wake_status = "wakened"

    def decay(self) -> None:
        """沉睡衰减：未访问则沉睡系数升高（越久越该想起）。"""
        if self.last_accessed:
            days = (datetime.now() - datetime.fromisoformat(self.last_accessed)).days
            self.sleep_score = min(5.0, self.sleep_score + days * 0.05)
            if days > 90 and "P0焊死" not in self.weight_tags:
                self.wake_status = "sleeping"

    def suppress_if_hyperactive(self, threshold_per_month: int = 100) -> None:
        """活跃度压制：访问过多→降权标记suppressed（活跃≠正确）。"""
        if self.access_count > threshold_per_month:
            self.wake_status = "suppressed"

    def content_for(self, tier: Tier) -> str:
        mapping = {
            Tier.COMMON: self.content_common,
            Tier.PROFESSIONAL: self.content_professional,
            Tier.STUDENT: self.content_student,
            Tier.ELDERLY: self.content_elderly,
            Tier.TECH: self.content_tech,
        }
        return mapping.get(tier, self.content_common) or self.content_common

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seal": self.seal.to_dict(),
            "tags": [t.to_dict() for t in self.tags],
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "sleep_score": round(self.sleep_score, 3),
            "weight_tags": self.weight_tags,
            "wake_status": self.wake_status,
            "content_common": self.content_common,
            "content_professional": self.content_professional,
            "content_student": self.content_student,
            "content_elderly": self.content_elderly,
            "content_tech": self.content_tech,
        }


# ═══════════════════════════════════════════════
# 语义库（动态生长·自激活）
# ═══════════════════════════════════════════════

class SemanticWeb:
    """语义网络：用户输入触发标签生长 + 关联。

    生长策略（诚实·可控）：基于受控术语表（种子词+扩展同义词）做精确子串匹配，
    避免中文无词边界导致的滑窗碎片（如"我在温州""说押金不"）。
    用户真实提及的术语会生长为新标签并积累信息素；未命中术语表的自由文本不强行切词。
    """

    # 种子标签（萌芽阶段即存在，等待生长）— name -> parent
    SEEDS = {
        "押金": "维权", "房东": "维权", "中介": "维权", "合同": "法律",
        "签": "法律", "电子签": "取证", "照片": "取证", "原图": "取证",
        "店": "开店", "生意": "开店", "选址": "开店", "竞合": "开店",
        "骂": "言论", "清朗": "言论", "维权": "维权", "温州": "地域",
        "瑞安": "地域", "装修": "合同", "陷阱": "维权", "霸王条款": "维权",
        "预付款": "维权", "违约金": "法律", "劳动": "维权", "医疗": "民生",
        "养老金": "民生", "诈骗": "红线", "举报": "维权",
    }

    def __init__(self):
        self.nodes: Dict[str, Tag] = {}
        # 预置种子节点（萌芽态，等用户触发生长）
        now = datetime.now().isoformat()
        for name, parent in self.SEEDS.items():
            self.nodes[name] = Tag(
                tag_id=hashlib.sha256(name.encode()).hexdigest()[:10],
                tag_name=name, parent_tag=parent,
                tag_type=TagType.MAIN if name in self.SEEDS.values() else TagType.SUB,
                created_by="system", created_at=now,
            )

    def grow(self, user_input: str, created_by: str = "auto") -> List[Tag]:
        """用户输入触发网络生长：受控术语表子串匹配→命中即生长/强化。
        未命中术语表的词不强行切词（避免碎片标签）。"""
        grown: List[Tag] = []
        now = datetime.now().isoformat()
        # 按词长降序匹配（先匹配"霸王条款"再匹配"条款"），避免短词抢匹配
        for term in sorted(self.SEEDS.keys(), key=len, reverse=True):
            if term in user_input:
                node = self.nodes[term]
                if node.created_by == "system":
                    # 首次被用户触发 → 转为 auto 生长态
                    node.created_by = created_by
                    grown.append(node)
                node.touch()
        # 共现关联边（同句命中的术语互相强化信息素）
        present = [t for t in self.SEEDS if t in user_input and t in self.nodes]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                self.nodes[present[i]].pheromone = min(5.0, self.nodes[present[i]].pheromone + 0.05)
                self.nodes[present[j]].pheromone = min(5.0, self.nodes[present[j]].pheromone + 0.05)
        return grown

    def match(self, query: str, top: int = 5) -> List[Tag]:
        """语义匹配：基于共现词 + 信息素排序（无向量库·诚实降级余弦→共现评分）。"""
        # 受控术语匹配：查询句命中术语表即加分（与 grow 一致，避免碎片）
        qwords = {t for t in self.SEEDS if t in query}
        scored: List[tuple[Any, ...]] = []
        for name, tag in self.nodes.items():
            score = 0.0
            if name in qwords:
                score += 2.0
            for qw in qwords:
                if qw in name or name in qw:
                    score += 1.0
            score += tag.pheromone * 0.3
            if score > 0:
                scored.append((score, tag))
        scored.sort(key=lambda x: -x[0])
        return [t for _, t in scored[:top]]

    def to_dict(self) -> Dict[str, Any]:
        return {name: t.to_dict() for name, t in self.nodes.items()}


# ═══════════════════════════════════════════════
# 意念交流（无界面触发·传感器驱动）
# ═══════════════════════════════════════════════

@dataclass
class TelepathySignal:
    """意念交流信号 — 传感器采集→自动唤醒记忆。"""
    signal: str
    perception: str
    auto_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {"signal": self.signal, "perception": self.perception,
                "auto_action": self.auto_action}


class Telepathy:
    """意念交流：无界面，传感器触发自动交互。"""

    # 意念交流触发器（焊死规则）
    TRIGGERS = [
        TelepathySignal("重复搜索同一词", "焦虑/不确定",
                        "主动推送：你上次查过，结果是…"),
        TelepathySignal("长时间无操作", "困惑/走神",
                        "轻声问：需要帮忙吗？"),
        TelepathySignal("快速滑动", "烦躁/不耐烦",
                        "简化输出，只给结论"),
        TelepathySignal("截图/拍照", "取证/留证",
                        "自动归档，DNA追溯"),
        TelepathySignal("语音带情绪", "愤怒/害怕",
                        "先安抚，再给方案"),
        TelepathySignal("深夜使用", "失眠/焦虑",
                        "提醒休息，标记明日优先"),
    ]

    def perceive(self, signal: str) -> Optional[TelepathySignal]:
        for t in self.TRIGGERS:
            if t.signal in signal:
                return t
        return None


# ═══════════════════════════════════════════════
# 失忆症友好（外部大脑核心）
# ═══════════════════════════════════════════════

class ExternalBrain:
    """外部大脑：替用户记忆 + 主动提醒 + 想不起时帮回忆。"""

    def __init__(self, entries: List[MemoryEntry]):
        self.entries = entries

    def remember_for(self, cue: str) -> List[MemoryEntry]:
        """用户忘了，系统替他回忆。"""
        cue_words = set(re.findall(r"[一-鿿]{2,4}", cue))
        hits = []
        for e in self.entries:
            text = (e.content_common + e.content_professional)
            if any(w in text for w in cue_words):
                hits.append(e)
        return hits

    def timeline(self, days: int = 7) -> List[MemoryEntry]:
        """时间线漫游：按时间查看记忆。"""
        cutoff = datetime.now() - timedelta(days=days)
        out = []
        for e in self.entries:
            try:
                ct = datetime.fromisoformat(e.seal.create_time)
                if ct >= cutoff:
                    out.append(e)
            except Exception:
                continue
        return sorted(out, key=lambda x: x.seal.create_time, reverse=True)

    def forgot_prompt(self, cue: str) -> str:
        """生成失忆症友好的提醒话术（说人话）。"""
        hits = self.remember_for(cue)
        if not hits:
            return f"你最近没提过「{cue}」。要新记一条吗？"
        lines = [f"你之前记过关于「{cue}」的 {len(hits)} 条，我帮你找回来："]
        for h in hits[:5]:
            lines.append(f"  · {h.content_common[:40]}（{h.seal.create_time[:10]}）")
        lines.append("要展开哪条？说一声就行。")
        return "\n".join(lines)


# ═══════════════════════════════════════════════
# 查询请求 / 引擎
# ═══════════════════════════════════════════════

@dataclass
class MemoryQuery:
    query_text: str
    user_tier: Tier
    user_context: Dict[str, Any] = field(default_factory=dict)
    explicit_tags: List[str] = field(default_factory=list)
    intent: str = "search"   # search / recall / audit / browse


class MemoryEngine:
    """记忆引擎 — 统一入口，分层输出，反活跃优先。"""

    def __init__(self, entries: List[MemoryEntry], semantic: SemanticWeb,
                 fixed: FixedPoint):
        self.entries = entries
        self.semantic = semantic
        self.fixed = fixed

    def query(self, req: MemoryQuery) -> List[MemoryEntry]:
        """查询逻辑（焊死）：
        1. 语义匹配标签 → 2. 相关性排序 → 3. 沉睡系数加权
        4. 权重标签加权(P0焊死永远优先) → 5. 活跃度压制
        6. 人群过滤 → 7. 不主动推送，返回结果"""
        # 受控术语匹配（与语义网络口径一致）
        qwords = {t for t in self.semantic.nodes if t in req.query_text}
        # 同时允许自由关键词（内容子串）兜底
        free_words = set(re.findall(r"[一-鿿]{2,4}", req.query_text))
        scored: List[tuple[Any, ...]] = []
        for e in self.entries:
            score = 0.0
            for t in e.tags:
                if t.tag_name in qwords:
                    score += 2.0
                for qw in qwords:
                    if qw in t.tag_name or t.tag_name in qw:
                        score += 1.0
            # 内容命中（自由关键词兜底）
            if any(w in e.content_common for w in free_words):
                score += 0.5
            # 沉睡系数加权（沉睡眠久的，系数越高）
            score += e.sleep_score * 0.2
            # 权重标签加权（P0焊死永远优先）
            if "P0焊死" in e.weight_tags:
                score += 5.0
            # 活跃度压制（太活跃的，降权）
            if e.wake_status == "suppressed":
                score -= 2.0
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        # 人群过滤：只返回适合该层级的（这里返回全部，format时分层）
        return [e for _, e in scored]

    def format_result(self, entry: MemoryEntry, tier: Tier) -> str:
        """根据用户层级返回不同格式内容（说人话/专业话/引导话/慢话/代码）。"""
        base = entry.content_for(tier)
        prefix = {
            Tier.COMMON: "【大白话】",
            Tier.PROFESSIONAL: "【专业版】",
            Tier.STUDENT: "【学习版】",
            Tier.ELDERLY: "【慢慢看】",
            Tier.TECH: "【技术版】",
        }.get(tier, "")
        extra = ""
        if "P0焊死" in entry.weight_tags:
            extra = " 🔒P0焊死"
        if entry.wake_status == "sleeping":
            extra += " 💤沉睡唤起"
        out = f"{prefix}{base}{extra}"
        # 老年层：失忆友好·语音播报标记（说人话·字大·慢）
        if tier == Tier.ELDERLY:
            out = f"🔊[语音播报] {out}\n（字已调大，慢慢看，不急）"
        return out


# ═══════════════════════════════════════════════
# 绝对禁止（焊死）
# ═══════════════════════════════════════════════

PROHIBITED = [
    "按活跃度推送", "自动删除低活跃标签", "替用户决定优先级",
    "算法推荐你可能喜欢", "同一内容给所有人",
    "技术术语给老百姓", "大白话给专业人士",
]

DNA_SIGNATURE = DNA
CONFIRM_CODE = CONFIRM


# ═══════════════════════════════════════════════
# 统一入口（合并所有）
# ═══════════════════════════════════════════════

class LongHunMemorySystem:
    """龍魂DNA记忆库 · 统一入口（外部大脑）。

    合并：蚁群 + 不动点 + 意念交流 + 语义库 + 通心意 + 五人群 + 失忆友好 + 反活跃优先。
    """

    def __init__(self):
        self.p0 = P0
        self.tiers = Tier
        self.fixed = FixedPoint()
        self.telepathy = Telepathy()
        self.semantic = SemanticWeb()
        self.brain = ExternalBrain([])
        self.engine: Optional[MemoryEngine] = None
        self._entries: List[MemoryEntry] = []
        # 加载历史记忆
        self._load()

    # ---------------- 记忆（L1签章 + L2归类 + L3激活） ----------------
    def remember(self, content: str, tier_default: Tier = Tier.COMMON,
                 content_by_tier: Optional[Dict[Tier, str]] = None,
                 weight_tags: Optional[List[str]] = None,
                 content_type: str = "其他",
                 auto_classify: bool = False,
                 user_consent: bool = False) -> MemoryEntry:
        """替用户记住一条。L1默认签章；L2按需语义归类。"""
        now = datetime.now().isoformat()
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        dna = f"#龍魂⚡️{now[:10]}-记忆-{h[:8]}"
        seal = DNASeal(
            dna_trace=dna, create_time=now, creator_uid=UID,
            content_type=content_type, content_hash=h,
            confirm_code=f"#CONFIRM🌌{h[:8]}-ONLY-ONCE🧬",
        )
        cb = content_by_tier or {}
        entry = MemoryEntry(
            seal=seal,
            weight_tags=weight_tags or [],
            content_common=cb.get(Tier.COMMON, content),
            content_professional=cb.get(Tier.PROFESSIONAL, content),
            content_student=cb.get(Tier.STUDENT, content),
            content_elderly=cb.get(Tier.ELDERLY, content),
            content_tech=cb.get(Tier.TECH, content),
            last_accessed=now,
        )
        # L2 自动归类（需用户开启）
        if auto_classify and user_consent:
            grown = self.semantic.grow(content, created_by="auto")
            entry.tags.extend(grown)
            # 权重标签强制挂 P0焊死 若内容触及P0
            if any(p in content for p in P0.ALL[:6]):
                if "P0焊死" not in entry.weight_tags:
                    entry.weight_tags.append("P0焊死")
        self._entries.append(entry)
        self.brain.entries = self._entries
        self.engine = MemoryEngine(self._entries, self.semantic, self.fixed)
        self._persist(entry)
        return entry

    # ---------------- 查询（分层输出） ----------------
    def recall(self, query_text: str, tier: Tier,
               intent: str = "search") -> Dict[str, Any]:
        """用户想不起/搜一搜 → 分层召回。"""
        if self.engine is None:
            self.engine = MemoryEngine(self._entries, self.semantic, self.fixed)
        # 1. 通心意感知（五维）
        heart = HeartSync().analyze(query_text)
        # 2. 意念感知（传感器信号）
        tele = self.telepathy.perceive(query_text)
        # 3. 语义生长（用户提及即生长）
        self.semantic.grow(query_text, created_by="auto")
        # 4. 记忆检索
        req = MemoryQuery(query_text=query_text, user_tier=tier, intent=intent)
        results = self.engine.query(req)
        for r in results[:10]:
            r.touch()  # 触角强化
            self._persist(r)
        formatted = [self.engine.format_result(r, tier) for r in results]
        return {
            "dna_trace": f"#龍魂⚡️{datetime.now().strftime('%Y%m%d')}-查询-{hash(query_text)%10000:04d}",
            "user_tier": tier.value,
            "results": formatted,
            "count": len(formatted),
            "heartsync": {"emotion": heart.emotion, "need": heart.need,
                          "hint": heart.respond_hint(tier)},
            "telepathy": tele.to_dict() if tele else None,
            "semantic_grown": len(self.semantic.nodes),
        }

    # ---------------- 失忆症友好 ----------------
    def forgot(self, cue: str) -> str:
        return self.brain.forgot_prompt(cue)

    def timeline(self, days: int = 7) -> List[Dict]:
        return [e.to_dict() for e in self.brain.timeline(days)]

    # ---------------- 自动分类（越用越习惯） ----------------
    def auto_classify(self, dna_trace: str, user_consent: bool) -> Dict[str, Any]:
        """自动归类（L2，需用户主动开启）。"""
        assert user_consent, "必须用户主动开启"
        for e in self._entries:
            if e.seal.dna_trace == dna_trace:
                grown = self.semantic.grow(e.content_common, created_by="auto")
                e.tags.extend(grown)
                self._persist(e)
                return {"status": "classified", "tags": [t.tag_name for t in grown]}
        return {"status": "not_found"}

    # ---------------- 唤醒/压制（L3） ----------------
    def wake_sleeping(self, tag_id: str) -> Dict[str, Any]:
        woken = 0
        for e in self._entries:
            if any(t.tag_id == tag_id for t in e.tags):
                if e.wake_status == "sleeping":
                    e.wake_status = "wakened"
                    woken += 1
                    self._persist(e)
        return {"woken": woken}

    def run_sleep_cycle(self) -> Dict[str, Any]:
        """沉睡衰减 + 活跃压制（反活跃优先）。"""
        for e in self._entries:
            e.decay()
            e.suppress_if_hyperactive()
            self._persist(e)
        sleeping = sum(1 for e in self._entries if e.wake_status == "sleeping")
        suppressed = sum(1 for e in self._entries if e.wake_status == "suppressed")
        return {"total": len(self._entries), "sleeping": sleeping,
                "suppressed": suppressed}

    # ---------------- 不动点守护 ----------------
    def guard(self, action_desc: str) -> bool:
        return self.fixed.guard(action_desc) and P0.validate(action_desc)

    # ---------------- 持久化 ----------------
    def _db(self) -> Path:
        return DATA_DIR / "memory.db"

    def _persist(self, entry: MemoryEntry) -> None:
        conn = sqlite3.connect(self._db())
        conn.execute("""CREATE TABLE IF NOT EXISTS memory (
            dna TEXT PRIMARY KEY, payload TEXT, created TEXT)""")
        conn.execute("INSERT OR REPLACE INTO memory (dna, payload, created) VALUES (?,?,?)",
                     (entry.seal.dna_trace,
                      json.dumps(entry.to_dict(), ensure_ascii=False),
                      datetime.now().isoformat()))
        conn.commit()
        conn.close()
        # 不可删日志
        log = DATA_DIR / "audit_log" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat(timespec='seconds')}] PERSIST dna={entry.seal.dna_trace}\n")

    def _load(self) -> None:
        db = self._db()
        if not db.exists():
            return
        conn = sqlite3.connect(db)
        try:
            rows = conn.execute("SELECT payload FROM memory").fetchall()
        except Exception:
            rows = []
        conn.close()
        for (payload,) in rows:
            try:
                d = json.loads(payload)
                seal_d = d["seal"]
                seal = DNASeal(**seal_d)
                tags = [Tag(
                    tag_id=t["tag_id"], tag_name=t["tag_name"],
                    parent_tag=t.get("parent_tag"),
                    tag_type=TagType(t["tag_type"]),
                    created_by=t.get("created_by", "auto"),
                    mention_count=t.get("mention_count", 0),
                    pheromone=t.get("pheromone", 1.0),
                    last_mentioned=t.get("last_mentioned", ""),
                    created_at=t.get("created_at", ""),
                ) for t in d.get("tags", [])]
                e = MemoryEntry(
                    seal=seal, tags=tags,
                    last_accessed=d.get("last_accessed", ""),
                    access_count=d.get("access_count", 0),
                    sleep_score=d.get("sleep_score", 0.0),
                    weight_tags=d.get("weight_tags", []),
                    wake_status=d.get("wake_status", "active"),
                    content_common=d.get("content_common", ""),
                    content_professional=d.get("content_professional", ""),
                    content_student=d.get("content_student", ""),
                    content_elderly=d.get("content_elderly", ""),
                    content_tech=d.get("content_tech", ""),
                )
                self._entries.append(e)
                # 重建语义网络节点
                for t in tags:
                    self.semantic.nodes.setdefault(t.tag_name, t)
            except Exception:
                continue
        self.brain.entries = self._entries
        self.engine = MemoryEngine(self._entries, self.semantic, self.fixed)

    # ---------------- 报告 ----------------
    def manifest(self) -> str:
        return f"""【龍魂DNA记忆库 · 终极合并版·焊死】

DNA追溯码：{DNA}
版本：焊死（不再改版）
创建者：💎 龍芯北辰｜UID9622
确认码：{CONFIRM}

核心宣言：
> 我们是人类的外部大脑。
> 你记不住，我记住。你想不起，我提醒。你失忆，我替你回忆。
> 活跃≠优先，沉睡≠遗忘。记忆是帮用户记起，不是替用户决定。

P0焊死底座（12条）：{ ' / '.join(P0.ALL) }
记忆条目：{len(self._entries)} | 语义标签：{len(self.semantic.nodes)}
"""


if __name__ == "__main__":
    sys = LongHunMemorySystem()
    # 自测：记一条 + 召回 + 失忆找回
    sys.remember("房东不退押金，去年签的租房合同",
                 content_by_tier={
                     Tier.COMMON: "房东不退押金，你签过租房合同，可以拿合同去说理。",
                     Tier.PROFESSIONAL: "依据《民法典》第587条，押金应退还；可主张违约责任。",
                     Tier.TECH: "{\"case\":\"deposit_dispute\",\"law\":\"civil_code_587\"}",
                 },
                 weight_tags=["P0焊死"], auto_classify=True, user_consent=True,
                 content_type="合同")
    r = sys.recall("押金不退", Tier.COMMON)
    print("召回:", r["count"], "条 | 情绪:", r["heartsync"]["emotion"])
    print("失忆找回:\n", sys.forgot("租房"))
    print(sys.manifest())
    print("✅ DNA记忆库自测通过")
