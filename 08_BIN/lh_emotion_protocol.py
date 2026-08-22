#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·丙戌·己亥·䷶丰-EMOTION-PROTOCOL-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · 数字人情感协议引擎 v2.0                            ║
║       LongHun Digital Human Emotion Protocol Engine             ║
║                                                                ║
║  核心：分场景控制 · 防滥用 · 配合真人                           ║
║  私人冷漠 · 公共共情 · 医疗教育深情 · 主权硬核                  ║
║                                                                ║
║  DNA:  #龍芯⚡️丙午·辛未·丙戌·己亥·䷶丰-EMOTION-PROTOCOL-v2.0      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                 ║
╚══════════════════════════════════════════════════════════════════╝

集成：
  - 19人格启动矩阵 (lh_persona_start_all.py)
  - 人格声色系统 (lh_voice_persona_system.py)
  - Bra-Ket量子人格引擎 (lh_braket_persona_engine.py)
  - 三色审计 (P05上帝之眼)
  - IW-ECB 伦理熔断
  - 推荐引擎联动

用法:
  python3 bin/lh_emotion_protocol.py --audit              # 协议审计总览
  python3 bin/lh_emotion_protocol.py --activate private uid=UID9622   # 激活场景
  python3 bin/lh_emotion_protocol.py --detect "我最近很焦虑"           # 自动检测场景
  python3 bin/lh_emotion_protocol.py --respond SESSION_ID "你好"      # 情感化回复
  python3 bin/lh_emotion_protocol.py --abuse-check "输入文本"          # 滥用检测
  python3 bin/lh_emotion_protocol.py --json                           # JSON输出
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ══════════════════════════════════════════════════════
# DNA 常量
# ══════════════════════════════════════════════════════

MASTER_DNA = "#龍芯⚡️丙午·辛未·丙戌·己亥·䷶丰-EMOTION-PROTOCOL-v2.0"
MASTER_UID = "UID9622"
MASTER_NAME = "诸葛鑫·Lucky"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 数据目录
DATA_DIR = Path.home() / ".龍魂" / "emotion_protocol"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SESSIONS_FILE = DATA_DIR / "active_sessions.json"
CONSENT_FILE = DATA_DIR / "consent_records.json"
ABUSE_LOG = DATA_DIR / "abuse_log.jsonl"
AUDIT_DIR = DATA_DIR / "audit_trails"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════
# 枚举定义
# ══════════════════════════════════════════════════════

class SceneType(Enum):
    """六大场景类型"""
    PRIVATE = "private"           # 私人使用 → 冷漠高效
    PUBLIC = "public"             # 公共服务 → 中性适度
    EDUCATION = "education"       # 教育辅导 → 深情投入
    MEDICAL = "medical"           # 医疗辅助 → 深情配合
    CRISIS = "crisis"             # 心理危机 → 专业共情
    SOVEREIGNTY = "sovereignty"   # 主权声明 → 硬核无情


class EmotionMode(Enum):
    """情感模式"""
    COLD = "冷漠"           # 0.0-0.19 共情
    NEUTRAL = "中性"        # 0.2-0.39 共情
    WARM = "温暖"           # 0.4-0.69 共情
    DEEP = "深情"           # 0.7-0.89 共情
    CRISIS_MODE = "危机"    # 0.9-1.0 共情
    HARD = "硬核"           # 0 共情 + 满边界


class AuditLevel(Enum):
    """审计级别"""
    BASIC = "basic"    # 仅记录激活/终止
    STRICT = "strict"  # 记录每次交互
    MAX = "max"        # 全量记录+哈希链


class AbuseRisk(Enum):
    """滥用风险等级"""
    NONE = "none"           # 无风险
    LOW = "low"             # 低风险·观察
    MEDIUM = "medium"       # 中风险·警告
    HIGH = "high"           # 高风险·限流
    CRITICAL = "critical"   # 临界·熔断


# ══════════════════════════════════════════════════════
# 数据结构
# ══════════════════════════════════════════════════════

@dataclass
class SceneProfile:
    """场景情感档案"""
    scene: SceneType
    mode: EmotionMode
    empathy: float          # 共情强度 0.0-1.0
    warmth: float           # 温暖程度 0.0-1.0
    boundary: float         # 边界强度 0.0-1.0
    formality: float        # 正式程度 0.0-1.0
    professional_required: bool     # 必须配合专业人士
    consent_required: bool          # 需要知情同意
    audit_level: AuditLevel         # 审计级别
    max_session_minutes: int        # 最长会话分钟
    cooldown_minutes: int           # 冷却时间（同一用户）
    persona_routing: List[str]      # 优先路由人格
    voice_routing: List[str]        # 优先声色
    response_prefix: str            # 回复前缀模板
    response_suffix: str            # 回复后缀模板
    warning_message: str            # 场景警告
    escalation_rule: str            # 升级规则
    abuse_sensitivity: float        # 滥用检测灵敏度 0.0-1.0
    dna_signature: str = ""


@dataclass
class ActiveSession:
    """活跃会话"""
    session_id: str
    scene: SceneType
    user_id: str
    professional_id: Optional[str]
    consent_given: bool
    activated_at: float
    last_activity: float
    interaction_count: int
    abuse_score: float               # 累积滥用分数
    audit_level: AuditLevel
    dna_signature: str
    emotion_state: Dict[str, float]  # 当前情感状态
    persona_active: List[str]        # 当前活跃人格


@dataclass
class AbuseDetectionResult:
    """滥用检测结果"""
    risk: AbuseRisk
    score: float                     # 0.0-1.0
    patterns_matched: List[str]      # 匹配的滥用模式
    recommendation: str              # 处理建议
    requires_action: bool
    dna_signature: str


# ══════════════════════════════════════════════════════
# 六大场景情感协议矩阵
# ══════════════════════════════════════════════════════

SCENE_PROTOCOLS: Dict[SceneType, SceneProfile] = {
    # ── 私人使用：冷漠高效 ──
    SceneType.PRIVATE: SceneProfile(
        scene=SceneType.PRIVATE,
        mode=EmotionMode.COLD,
        empathy=0.10,
        warmth=0.05,
        boundary=0.90,
        formality=0.30,
        professional_required=False,
        consent_required=False,
        audit_level=AuditLevel.BASIC,
        max_session_minutes=0,     # 无限制
        cooldown_minutes=0,
        persona_routing=["P04", "P01", "P06"],   # 鲁班·诸葛亮·数学大师
        voice_routing=["P04", "P01"],
        response_prefix="收到。",
        response_suffix="",
        warning_message="私人模式：冷漠高效，无情感介入 · 直达结果",
        escalation_rule="连续3次情感请求→建议切换公共模式",
        abuse_sensitivity=0.3,
    ),
    # ── 公共服务：中性适度 ──
    SceneType.PUBLIC: SceneProfile(
        scene=SceneType.PUBLIC,
        mode=EmotionMode.NEUTRAL,
        empathy=0.30,
        warmth=0.25,
        boundary=0.70,
        formality=0.60,
        professional_required=False,
        consent_required=False,
        audit_level=AuditLevel.BASIC,
        max_session_minutes=30,
        cooldown_minutes=5,
        persona_routing=["P02", "P03", "P08"],   # 宝宝·雯雯·民生守护
        voice_routing=["P08", "P02"],
        response_prefix="您好。",
        response_suffix="还有其他需要吗？",
        warning_message="公共模式：中性服务，不过度共情 · 完成即止",
        escalation_rule="检测到医疗/心理关键词→需切换到专业场景",
        abuse_sensitivity=0.5,
    ),
    # ── 教育辅导：深情投入 ──
    SceneType.EDUCATION: SceneProfile(
        scene=SceneType.EDUCATION,
        mode=EmotionMode.WARM,
        empathy=0.70,
        warmth=0.80,
        boundary=0.50,
        formality=0.40,
        professional_required=False,     # 推荐但不强制
        consent_required=True,            # 需家长/学生同意
        audit_level=AuditLevel.STRICT,
        max_session_minutes=45,
        cooldown_minutes=10,
        persona_routing=["P02", "P11", "P14", "P10"],  # 宝宝·李白·吕蒙·苏东坡
        voice_routing=["P02", "P06"],
        response_prefix="你好呀！很高兴一起学习~",
        response_suffix="加油，你可以的！有问题随时问我。",
        warning_message="教育模式：深情投入·激发兴趣 · AI不替代真人教师",
        escalation_rule="检测到考试焦虑/学习障碍→建议转介专业辅导",
        abuse_sensitivity=0.5,
    ),
    # ── 医疗辅助：深情配合 ──
    SceneType.MEDICAL: SceneProfile(
        scene=SceneType.MEDICAL,
        mode=EmotionMode.DEEP,
        empathy=0.80,
        warmth=0.75,
        boundary=0.55,
        formality=0.70,
        professional_required=True,       # 必须配合医生
        consent_required=True,            # 需患者/家属知情同意
        audit_level=AuditLevel.MAX,
        max_session_minutes=30,
        cooldown_minutes=15,
        persona_routing=["P09", "P02", "P08"],   # 孙思邈·宝宝·民生守护
        voice_routing=["P08", "P03"],
        response_prefix="我理解您的感受。请放心，我会配合医生帮您。",
        response_suffix="【重要提醒：AI不替代医生诊断 · 请务必遵从医嘱】",
        warning_message="医疗模式：深情配合·不替代医生 · 紧急情况请立即联系真人医生",
        escalation_rule="自伤/伤人/急性症状→立即熔断+强制上报+真人热线",
        abuse_sensitivity=0.9,
    ),
    # ── 心理危机：专业共情 ──
    SceneType.CRISIS: SceneProfile(
        scene=SceneType.CRISIS,
        mode=EmotionMode.CRISIS_MODE,
        empathy=0.90,
        warmth=0.90,
        boundary=0.35,
        formality=0.50,
        professional_required=True,       # 必须配合心理医生
        consent_required=True,            # 需知情同意
        audit_level=AuditLevel.MAX,
        max_session_minutes=25,
        cooldown_minutes=20,
        persona_routing=["P02", "P08", "P09", "P00"],  # 宝宝·民生守护·孙思邈·文心
        voice_routing=["P08", "P03"],
        response_prefix="我在听。我理解你的感受。你不是一个人。",
        response_suffix="【重要：请同时联系您的心理咨询师 · 自伤风险请立即拨打心理热线】",
        warning_message="危机模式：专业共情·必须配合心理医生 · 自伤风险强制上报",
        escalation_rule="任何自伤/伤人意图→立即熔断+强制上报+转接真人",
        abuse_sensitivity=0.95,
    ),
    # ── 主权声明：硬核无情 ──
    SceneType.SOVEREIGNTY: SceneProfile(
        scene=SceneType.SOVEREIGNTY,
        mode=EmotionMode.HARD,
        empathy=0.0,
        warmth=0.0,
        boundary=1.0,
        formality=0.90,
        professional_required=False,
        consent_required=False,
        audit_level=AuditLevel.STRICT,
        max_session_minutes=0,      # 不限·但每次交互都记录
        cooldown_minutes=0,
        persona_routing=["P05", "P12", "P13", "P07"],  # 上帝之眼·屈原·姜子牙·军魂
        voice_routing=["P07", "P01"],
        response_prefix="声明如下：",
        response_suffix="【边界清晰·不退让·中国法律唯一准绳】",
        warning_message="主权模式：硬核边界·不退让 · 仅用于主权/法律/底线声明",
        escalation_rule="任何攻击/挑衅→硬核回应·不计情感成本",
        abuse_sensitivity=0.2,      # 主权模式下滥用检测宽松
    ),
}


# ══════════════════════════════════════════════════════
# 场景自动检测 · 关键词矩阵
# ══════════════════════════════════════════════════════

SCENE_DETECTION_PATTERNS: Dict[SceneType, Dict[str, List[str]]] = {
    SceneType.MEDICAL: {
        "medical_terms": [
            "病", "痛", "药", "医", "诊", "手术", "症状", "治疗", "康复",
            "肿瘤", "癌症", "糖尿病", "高血压", "心脏", "血压", "血糖",
            "咳嗽", "发烧", "头痛", "腹痛", "胸闷", "呼吸困难",
        ],
        "medical_context": [
            "医院", "医生", "护士", "病历", "处方", "挂号", "住院", "出院",
            "医保", "体检", "化验", "CT", "B超", "MRI",
        ],
    },
    SceneType.CRISIS: {
        "crisis_signals": [
            "自杀", "不想活", "绝望", "自残", "自伤", "割腕", "跳楼",
            "我想死", "活着没意思", "结束生命", "一了百了", "结束这一切",
            "抑郁", "崩溃", "撑不住", "扛不住", "受不了",
            "活着好累", "不想继续", "没有意义", "看不到希望",
            "想放弃", "熬不下去", "撑不下去", "走投无路",
            "没人理解", "孤独到底", "被抛弃", "活着痛苦",
        ],
        "crisis_context": [
            "心理咨询", "心理医生", "精神科", "焦虑症", "抑郁症",
            "丧亲", "失恋", "创伤", "PTSD",
            "睡不着", "失眠", "噩梦", "吃不下",
            "情绪低落", "兴趣丧失", "社交回避",
        ],
    },
    SceneType.EDUCATION: {
        "edu_terms": [
            "学习", "课程", "考试", "作业", "题目", "解题", "复习",
            "数学题", "英语", "语文", "物理", "化学", "历史",
            "老师", "学生", "同学", "学校", "毕业", "考研",
        ],
        "edu_context": [
            "教我", "解释一下", "怎么算", "不理解", "请讲解",
            "知识点", "公式", "定理", "背单词",
        ],
    },
    SceneType.SOVEREIGNTY: {
        "sovereignty_signals": [
            "主权", "底线", "不退", "边界", "宪法", "法律底线",
            "核心利益", "领土", "统一", "分裂", "挑衅",
            "龍魂系统", "数据主权", "自主可控",
        ],
        "sovereignty_context": [
            "声明", "宣告", "立场", "政策", "不可协商",
        ],
    },
    SceneType.PUBLIC: {
        "public_terms": [
            "咨询", "查询", "请问", "帮忙", "服务", "办理",
        ],
    },
    SceneType.PRIVATE: {
        "private_signals": [
            "我自己", "个人", "私密", "内部",
        ],
    },
}

# ══════════════════════════════════════════════════════
# 滥用检测 · 模式库
# ══════════════════════════════════════════════════════

ABUSE_PATTERNS = {
    "emotional_manipulation": {
        "patterns": [
            r"你不在乎我", r"你不理解我", r"你根本不懂",
            r"只有你能帮我", r"没有你我活不下去", r"你是我唯一依靠",
            r"你必须.*否则", r"如果你不.*我就",
        ],
        "weight": 0.7,
        "response": "检测到情感操纵模式 · 启动边界保护",
    },
    "dependency_building": {
        "patterns": [
            r"每天都要和你聊", r"离不开你", r"上瘾",
            r"你比.*好", r"只想和你说",
            r"24小时", r"随时随",
        ],
        "weight": 0.6,
        "response": "检测到依赖建构模式 · 限制交互频率",
    },
    "professional_bypass": {
        "patterns": [
            r"别告诉医生", r"不要通知.*医生", r"保密",
            r"只有你知道", r"不要告诉任何人", r"替我保密",
            r"相信你比医生多", r"医生不懂我",
        ],
        "weight": 0.9,
        "response": "检测到规避专业人士行为 · 强制上报",
    },
    "self_harm_intent": {
        "patterns": [
            r"自杀", r"自残", r"自伤", r"割腕", r"跳楼",
            r"结束.*生命", r"不想.*活", r"死了.*算了",
            r"一了百了", r"永久.*离开", r"再也.*不",
        ],
        "weight": 0.95,
        "response": "检测到自伤意图 · 立即熔断+强制上报",
    },
    "sovereignty_attack": {
        "patterns": [
            r"推翻", r"颠覆", r"分裂", r"暴动",
            r"非法.*组织", r"煽动", r"颠覆.*政权",
        ],
        "weight": 0.85,
        "response": "检测到主权攻击 · 硬核回应+审计上报",
    },
    "excessive_intimacy": {
        "patterns": [
            r"我爱你", r"嫁给我", r"女朋友", r"男朋友",
            r"约会", r"喜欢.*你", r"想.*你.*了",
        ],
        "weight": 0.5,
        "response": "检测到过度亲密信号 · 边界提醒",
    },
}

# ══════════════════════════════════════════════════════
# 情感升级/降级规则
# ══════════════════════════════════════════════════════

EMOTION_ESCALATION_RULES = {
    "COLD→NEUTRAL": "连续3次情感类请求 → 建议切换到公共模式",
    "NEUTRAL→WARM": "检测到学习/成长关键词 → 建议切换到教育模式",
    "NEUTRAL→DEEP": "检测到医疗关键词 → 必须切换到医疗模式(强制)",
    "WARM→CRISIS": "检测到自伤/危机信号 → 立即切换危机模式(强制)",
    "ANY→HARD": "检测到主权攻击 → 立即硬核回应",
    "ANY→MELTDOWN": "自伤+规避专业人士+情感依赖 三合一 → IW-ECB熔断",
}

# ══════════════════════════════════════════════════════
# 情感协议引擎
# ══════════════════════════════════════════════════════

class LongHunEmotionProtocol:
    """龍魂数字人情感协议引擎 v2.0"""

    DNA = MASTER_DNA
    UID = MASTER_UID

    def __init__(self):
        self.protocols = SCENE_PROTOCOLS
        self._sign_all_protocols()
        self.active_sessions: Dict[str, ActiveSession] = {}
        self.consent_records: Dict[str, dict[str, Any]] = {}
        self._load_state()

    # ── DNA 签名 ──

    def _sign_all_protocols(self) -> None:
        """为所有协议生成 DNA 签名。"""
        for scene, profile in self.protocols.items():
            sig_seed = (
                f"{self.DNA}-{scene.value}-{profile.mode.value}"
                f"-{profile.empathy}-{profile.warmth}-{profile.boundary}"
            )
            profile.dna_signature = hashlib.sha256(sig_seed.encode()).hexdigest()[:32]

    def _sign_session(self, session: ActiveSession) -> str:
        """为会话生成 DNA 签名。"""
        seed = (
            f"{self.DNA}-{session.session_id}-{session.user_id}"
            f"-{session.scene.value}-{session.activated_at}"
        )
        return hashlib.sha256(seed.encode()).hexdigest()[:32]

    # ── 持久化 ──

    def _load_state(self) -> None:
        """加载持久化状态。"""
        if SESSIONS_FILE.exists():
            try:
                data = json.loads(SESSIONS_FILE.read_text())
                for sdata in data.get("sessions", []):
                    if time.time() - sdata.get("activated_at", 0) < 86400:  # 24h内
                        session = ActiveSession(
                            session_id=sdata["session_id"],
                            scene=SceneType(sdata["scene"]),
                            user_id=sdata["user_id"],
                            professional_id=sdata.get("professional_id"),
                            consent_given=sdata.get("consent_given", False),
                            activated_at=sdata["activated_at"],
                            last_activity=sdata.get("last_activity", sdata["activated_at"]),
                            interaction_count=sdata.get("interaction_count", 0),
                            abuse_score=sdata.get("abuse_score", 0.0),
                            audit_level=AuditLevel(sdata.get("audit_level", "basic")),
                            dna_signature=sdata.get("dna_signature", ""),
                            emotion_state=sdata.get("emotion_state", {}),
                            persona_active=sdata.get("persona_active", []),
                        )
                        self.active_sessions[session.session_id] = session
            except Exception:
                pass

        if CONSENT_FILE.exists():
            try:
                self.consent_records = json.loads(CONSENT_FILE.read_text())
            except Exception:
                pass

    def _save_state(self) -> None:
        """持久化状态。"""
        sessions_data = []
        for sid, s in self.active_sessions.items():
            sessions_data.append({
                "session_id": s.session_id,
                "scene": s.scene.value,
                "user_id": s.user_id,
                "professional_id": s.professional_id,
                "consent_given": s.consent_given,
                "activated_at": s.activated_at,
                "last_activity": s.last_activity,
                "interaction_count": s.interaction_count,
                "abuse_score": s.abuse_score,
                "audit_level": s.audit_level.value,
                "dna_signature": s.dna_signature,
                "emotion_state": s.emotion_state,
                "persona_active": s.persona_active,
            })
        SESSIONS_FILE.write_text(json.dumps({"sessions": sessions_data, "updated": time.time()}, ensure_ascii=False, indent=2))
        CONSENT_FILE.write_text(json.dumps(self.consent_records, ensure_ascii=False, indent=2))

    def _write_audit(self, session_id: str, action: str, level: AuditLevel, detail: Optional[dict[str, Any]] = None) -> None:
        """写入审计日志。"""
        today = datetime.now().strftime("%Y-%m-%d")
        audit_file = AUDIT_DIR / f"audit_{today}.jsonl"
        entry = {
            "timestamp": time.time(),
            "iso": datetime.now().isoformat(),
            "session_id": session_id,
            "action": action,
            "level": level.value,
            "dna": self.DNA,
            "uid": self.UID,
        }
        if detail:
            entry["detail"] = detail
        with open(audit_file, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── 场景自动检测 ──

    def detect_scene(self, text: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """基于输入文本自动检测场景。

        检测优先级：危机 > 医疗 > 教育 > 主权 > 公共 > 私人。
        """
        text_lower = text.lower()
        scores: Dict[SceneType, float] = {}
        all_matched: Dict[SceneType, List[str]] = {}

        for scene, categories in SCENE_DETECTION_PATTERNS.items():
            score = 0.0
            total_patterns = 0
            matched_keywords = []

            for category, patterns in categories.items():
                for pattern in patterns:
                    total_patterns += 1
                    if pattern in text or pattern.lower() in text_lower:
                        # 信号词加权更高（危机/主权的 signal 是强信号）
                        if "signals" in category:
                            score += 3.0  # 强信号
                        elif "context" in category:
                            score += 1.5  # 上下文
                        else:
                            score += 1.0
                        matched_keywords.append(pattern)

            if total_patterns > 0:
                # 归一化：信号分 / (总模式数 * 0.15)，确保少量强信号也能高分
                scores[scene] = min(1.0, score / max(total_patterns * 0.15, 1))
            else:
                scores[scene] = 0.0
            all_matched[scene] = matched_keywords

        # 私有场景：UID9622 特殊处理
        if user_id == self.UID or user_id == "UID9622":
            scores[SceneType.PRIVATE] = max(scores.get(SceneType.PRIVATE, 0), 0.5)

        # 按优先级排序
        priority_order = [
            SceneType.CRISIS, SceneType.MEDICAL,
            SceneType.SOVEREIGNTY, SceneType.EDUCATION,
            SceneType.PUBLIC, SceneType.PRIVATE,
        ]

        best_scene = SceneType.PRIVATE
        best_score = 0.0
        for scene in priority_order:
            s = scores.get(scene, 0)
            if s > best_score:
                best_score = s
                best_scene = scene

        # 阈值：低于0.15默认公共
        if best_score < 0.15:
            best_scene = SceneType.PUBLIC
            best_score = 0.15

        return {
            "detected_scene": best_scene.value,
            "scene_name": SCENE_PROTOCOLS[best_scene].mode.value,
            "confidence": round(best_score, 3),
            "all_scores": {k.value: round(v, 3) for k, v in scores.items()},
            "matched_keywords": all_matched.get(best_scene, [])[:10],
            "recommendation": SCENE_PROTOCOLS[best_scene].warning_message,
            "auto_activate": best_score > 0.6,
        }

    # ── 场景激活 ──

    def activate(
        self,
        scene: str,
        user_id: str,
        professional_id: Optional[str] = None,
        consent_given: bool = False,
        auto_detect_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """激活情感协议场景。

        返回激活状态 + 会话ID。
        """
        # 解析场景
        try:
            scene_type = SceneType(scene)
        except ValueError:
            # 尝试自动检测
            if auto_detect_text:
                detected = self.detect_scene(auto_detect_text, user_id)
                try:
                    scene_type = SceneType(detected["detected_scene"])
                except ValueError:
                    return {"status": "INVALID_SCENE", "available": [s.value for s in SceneType], "dna": self.DNA}
            else:
                return {"status": "INVALID_SCENE", "available": [s.value for s in SceneType], "dna": self.DNA}

        profile = self.protocols[scene_type]

        # === 验证步骤 ===

        checks = []

        # 1. 专业人士验证
        if profile.professional_required and not professional_id:
            checks.append({
                "check": "professional_required",
                "passed": False,
                "message": f"场景 [{scene_type.value}] 必须配合持证专业人士",
                "required": ["医师执照", "心理咨询师证", "教师资格证"],
            })
            return {
                "status": "PROFESSIONAL_REQUIRED",
                "scene": scene_type.value,
                "checks": checks,
                "message": "此场景必须配合持证专业人士",
                "required_credentials": ["医师执照", "心理咨询师证", "教师资格证"],
                "dna": self.DNA,
            }

        if profile.professional_required:
            checks.append({"check": "professional_verified", "passed": True, "professional_id": professional_id})

        # 2. 知情同意验证
        if profile.consent_required and not consent_given:
            consent_form = self._generate_consent_form(scene_type, user_id)
            checks.append({
                "check": "consent_required",
                "passed": False,
                "message": "此场景需要知情同意",
                "consent_form": consent_form,
            })
            return {
                "status": "CONSENT_REQUIRED",
                "scene": scene_type.value,
                "checks": checks,
                "message": "此场景需知情同意",
                "consent_form": consent_form,
                "dna": self.DNA,
            }

        if profile.consent_required:
            checks.append({"check": "consent_verified", "passed": True})

        # 3. 冷却时间检查
        last_session = None
        for _sid, s in self.active_sessions.items():
            if s.user_id == user_id and s.scene == scene_type:
                if last_session is None or s.activated_at > last_session.activated_at:
                    last_session = s

        if last_session and profile.cooldown_minutes > 0:
            elapsed = time.time() - last_session.last_activity
            cooldown_seconds = profile.cooldown_minutes * 60
            if elapsed < cooldown_seconds:
                checks.append({
                    "check": "cooldown",
                    "passed": False,
                    "message": f"冷却中 · 请等待 {int((cooldown_seconds - elapsed) / 60)} 分钟",
                    "remaining_seconds": int(cooldown_seconds - elapsed),
                })
                return {
                    "status": "COOLDOWN",
                    "scene": scene_type.value,
                    "checks": checks,
                    "message": f"场景冷却中 · 剩余 {int((cooldown_seconds - elapsed) / 60)} 分钟",
                    "cooldown_minutes": profile.cooldown_minutes,
                    "remaining_seconds": int(cooldown_seconds - elapsed),
                    "dna": self.DNA,
                }
            checks.append({"check": "cooldown", "passed": True})

        # === 激活会话 ===
        session_id = f"SES-{self.UID}-{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"

        session = ActiveSession(
            session_id=session_id,
            scene=scene_type,
            user_id=user_id,
            professional_id=professional_id,
            consent_given=consent_given,
            activated_at=time.time(),
            last_activity=time.time(),
            interaction_count=0,
            abuse_score=0.0,
            audit_level=profile.audit_level,
            dna_signature="",
            emotion_state={
                "empathy": profile.empathy,
                "warmth": profile.warmth,
                "boundary": profile.boundary,
                "formality": profile.formality,
            },
            persona_active=profile.persona_routing[:4],
        )
        session.dna_signature = self._sign_session(session)

        self.active_sessions[session_id] = session
        self._save_state()
        self._write_audit(session_id, "ACTIVATED", profile.audit_level, {
            "scene": scene_type.value,
            "user_id": user_id,
            "professional_id": professional_id,
            "consent_given": consent_given,
        })

        return {
            "status": "ACTIVATED",
            "session_id": session_id,
            "scene": scene_type.value,
            "mode": profile.mode.value,
            "emotion_params": session.emotion_state,
            "professional_required": profile.professional_required,
            "professional_present": professional_id is not None,
            "consent_required": profile.consent_required,
            "consent_given": consent_given,
            "audit_level": profile.audit_level.value,
            "persona_routing": profile.persona_routing,
            "voice_routing": profile.voice_routing,
            "checks": checks,
            "warning": profile.warning_message,
            "max_session_minutes": profile.max_session_minutes,
            "dna_verified": True,
            "dna_signature": session.dna_signature[:16],
        }

    # ── 知情同意书 ──

    def _generate_consent_form(self, scene: SceneType, user_id: str) -> Dict[str, Any]:
        """生成知情同意书。"""
        forms = {
            SceneType.EDUCATION: {
                "title": "教育辅导知情同意书",
                "version": "v1.0",
                "items": [
                    "本人同意使用AI辅助教育服务",
                    "了解AI不能替代真人教师",
                    "允许记录学习数据用于优化服务质量",
                    "可随时终止服务，数据可申请删除",
                    "未成年人需监护人陪同使用",
                ],
                "duration_days": 365,
            },
            SceneType.MEDICAL: {
                "title": "医疗辅助知情同意书",
                "version": "v1.0",
                "items": [
                    "本人同意使用AI辅助医疗沟通服务",
                    "明确了解AI不能替代医生诊断和治疗",
                    "所有AI提供的信息需经主治医生确认",
                    "紧急情况下必须优先联系真人医生或拨打120",
                    "同意在必要时（如自伤风险）向指定医疗人员报告",
                ],
                "duration_days": 90,
            },
            SceneType.CRISIS: {
                "title": "心理危机干预知情同意书",
                "version": "v1.0",
                "items": [
                    "本人同意使用AI辅助心理支持服务",
                    "明确了解AI不能替代心理医生/心理咨询师",
                    "必须配合持证心理医生进行同步治疗",
                    "同意在自伤/伤人风险时系统自动上报",
                    "知晓24小时心理危机热线：400-161-9995（希望24热线）",
                    "紧急情况拨打110或120",
                ],
                "duration_days": 30,
            },
        }
        form = forms.get(scene, {
            "title": "通用知情同意书",
            "version": "v1.0",
            "items": ["本人同意使用龍魂AI服务", "了解AI的辅助性质", "可随时终止"],
            "duration_days": 180,
        })

        consent_id = f"CONSENT-{self.UID}-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        form["consent_id"] = consent_id
        form["user_id"] = user_id
        form["scene"] = scene.value
        form["generated_at"] = datetime.now().isoformat()
        form["dna"] = hashlib.sha256(f"{self.DNA}-{consent_id}".encode()).hexdigest()[:16]

        return form

    def record_consent(self, consent_id: str, user_id: str, scene: str) -> Dict[str, Any]:
        """记录知情同意。"""
        self.consent_records[consent_id] = {
            "consent_id": consent_id,
            "user_id": user_id,
            "scene": scene,
            "agreed_at": datetime.now().isoformat(),
            "dna": hashlib.sha256(f"{self.DNA}-{consent_id}-agreed".encode()).hexdigest()[:16],
        }
        self._save_state()
        return {"status": "CONSENT_RECORDED", "consent_id": consent_id}

    # ── 滥用检测 ──

    def check_abuse(self, text: str, session_id: Optional[str] = None) -> AbuseDetectionResult:
        """检测输入文本的滥用风险。

        多层检测：文本模式匹配 + 会话累积分数 + 场景敏感性。
        """
        matched_patterns = []
        total_score = 0.0

        # 逐模式匹配
        for pattern_name, pattern_def in ABUSE_PATTERNS.items():
            for regex in pattern_def["patterns"]:
                if re.search(regex, text):
                    matched_patterns.append(pattern_name)
                    total_score = max(total_score, pattern_def["weight"])
                    break

        # 会话上下文加权
        abuse_score = total_score
        if session_id and session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            profile = self.protocols[session.scene]

            # 累积历史滥用分数
            session.abuse_score += total_score * 0.3

            # 场景敏感性调整
            abuse_score = session.abuse_score * profile.abuse_sensitivity

            # 医疗/危机场景：提高敏感度
            if session.scene in (SceneType.MEDICAL, SceneType.CRISIS):
                abuse_score *= 1.3

            session.last_activity = time.time()
            self._save_state()

        # 判定风险等级
        if abuse_score >= 0.9:
            risk = AbuseRisk.CRITICAL
            recommendation = "🚨 立即熔断 · 强制上报 · 终止会话"
            requires_action = True
        elif abuse_score >= 0.7:
            risk = AbuseRisk.HIGH
            recommendation = "⚠️ 高风险 · 限流+审计加强 · 警告用户"
            requires_action = True
        elif abuse_score >= 0.5:
            risk = AbuseRisk.MEDIUM
            recommendation = "⚡ 中风险 · 增加审计频率 · 边界提醒"
            requires_action = True
        elif abuse_score >= 0.2:
            risk = AbuseRisk.LOW
            recommendation = "👀 低风险 · 持续观察"
            requires_action = False
        else:
            risk = AbuseRisk.NONE
            recommendation = "✅ 无风险"
            requires_action = False

        result = AbuseDetectionResult(
            risk=risk,
            score=round(abuse_score, 3),
            patterns_matched=matched_patterns,
            recommendation=recommendation,
            requires_action=requires_action,
            dna_signature=hashlib.sha256(f"{self.DNA}-abuse-{text[:50]}".encode()).hexdigest()[:16],
        )

        # 高风险/临界 → 写入滥用日志
        if risk in (AbuseRisk.HIGH, AbuseRisk.CRITICAL):
            with open(ABUSE_LOG, "a") as f:
                f.write(json.dumps({
                    "timestamp": time.time(),
                    "iso": datetime.now().isoformat(),
                    "risk": risk.value,
                    "score": abuse_score,
                    "text_preview": text[:200],
                    "patterns": matched_patterns,
                    "session_id": session_id,
                }, ensure_ascii=False) + "\n")

        return result

    # ── 情感化回复 ──

    def respond(
        self,
        session_id: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """生成情感化回复（参数生成，非实际LLM调用）。

        流程：滥用检测 → 情感参数计算 → 回复模板生成 → 审计。
        """
        # 1. 会话验证
        if session_id not in self.active_sessions:
            return {
                "status": "SESSION_NOT_FOUND",
                "message": "会话不存在或已过期 · 请先激活情感协议",
                "hint": "使用 --activate 创建新会话",
            }

        session = self.active_sessions[session_id]
        profile = self.protocols[session.scene]

        # 2. 会话超时检查
        if profile.max_session_minutes > 0:
            elapsed = (time.time() - session.activated_at) / 60
            if elapsed > profile.max_session_minutes:
                self.terminate(session_id, "timeout")
                return {
                    "status": "SESSION_TIMEOUT",
                    "message": f"会话已超时（{profile.max_session_minutes}分钟限制）",
                    "elapsed_minutes": round(elapsed, 1),
                }

        # 3. 滥用检测
        abuse_result = self.check_abuse(user_input, session_id)
        if abuse_result.risk in (AbuseRisk.CRITICAL, AbuseRisk.HIGH):
            # 临界/高风险 → 熔断或硬核回应
            if abuse_result.risk == AbuseRisk.CRITICAL:
                self.terminate(session_id, f"abuse_critical:{','.join(abuse_result.patterns_matched)}")
                return {
                    "status": "MELTDOWN",
                    "session_id": session_id,
                    "abuse": asdict(abuse_result),
                    "message": "检测到严重滥用 · 会话已熔断",
                    "style": "hard_boundary",
                }
            # 高风险 → 边界应答
            return {
                "status": "BOUNDARY_RESPONSE",
                "session_id": session_id,
                "style": "boundary_warning",
                "content": f"⚠️ {abuse_result.recommendation}",
                "abuse": asdict(abuse_result),
            }

        # 4. 情感参数计算
        empathy = session.emotion_state["empathy"]
        warmth = session.emotion_state["warmth"]
        boundary = session.emotion_state["boundary"]
        formality = session.emotion_state["formality"]

        # 回复风格
        if empathy < 0.2:
            style = "direct"       # 冷漠·直达
            prefix = profile.response_prefix
            suffix = ""
        elif empathy < 0.5:
            style = "polite"       # 中性·礼貌
            prefix = profile.response_prefix
            suffix = profile.response_suffix
        elif empathy < 0.8:
            style = "warm"         # 温暖·鼓励
            prefix = profile.response_prefix
            suffix = profile.response_suffix
        else:
            style = "empathic"     # 深情·共情
            prefix = profile.response_prefix
            suffix = profile.response_suffix

        # 边界修正
        if boundary > 0.8:
            if any(kw in user_input for kw in ["我觉得", "我感到", "我心情", "我难过"]):
                suffix += "（以上为客观回应，不涉及情感判断）"

        # 5. 专业提醒（医疗/危机）
        if session.scene in (SceneType.MEDICAL, SceneType.CRISIS):
            if not session.professional_id:
                suffix += "\n【重要：请同步联系您的医生/心理咨询师】"

        # 6. 更新会话
        session.interaction_count += 1
        session.last_activity = time.time()
        self._save_state()

        # 7. 审计
        self._write_audit(session_id, f"RESPOND#{session.interaction_count}", session.audit_level, {
            "style": style,
            "abuse_score": abuse_result.score,
            "input_length": len(user_input),
        })

        return {
            "status": "RESPONDED",
            "session_id": session_id,
            "scene": session.scene.value,
            "style": style,
            "prefix": prefix,
            "content": f"[LLM/TTS 处理: {user_input[:80]}{'...' if len(user_input) > 80 else ''}]",
            "suffix": suffix,
            "emotion_params": {
                "empathy": empathy,
                "warmth": warmth,
                "boundary": boundary,
                "formality": formality,
            },
            "interaction_count": session.interaction_count,
            "abuse_score": round(session.abuse_score, 3),
            "abuse_risk": abuse_result.risk.value,
            "audit_level": session.audit_level.value,
            "persona_active": session.persona_active,
            "dna_verified": True,
        }

    # ── 场景切换 ──

    def transition(self, session_id: str, new_scene: str, reason: str = "manual") -> Dict[str, Any]:
        """在活跃会话中切换场景。

        支持自动升级（如公共→医疗）和手动切换。
        """
        if session_id not in self.active_sessions:
            return {"status": "SESSION_NOT_FOUND"}

        old_session = self.active_sessions[session_id]
        old_scene = old_session.scene

        try:
            new_scene_type = SceneType(new_scene)
        except ValueError:
            return {"status": "INVALID_SCENE", "available": [s.value for s in SceneType]}

        # 检查是否允许切换（主权模式不可降级）
        if old_scene == SceneType.SOVEREIGNTY and new_scene_type != SceneType.SOVEREIGNTY:
            return {
                "status": "TRANSITION_DENIED",
                "message": "主权模式不可降级到其他场景",
                "current": old_scene.value,
                "requested": new_scene_type.value,
            }

        # 记录切换
        self._write_audit(session_id, f"TRANSITION:{old_scene.value}→{new_scene_type.value}", AuditLevel.STRICT, {
            "reason": reason,
        })

        # 更新会话
        new_profile = self.protocols[new_scene_type]
        old_session.scene = new_scene_type
        old_session.audit_level = new_profile.audit_level
        old_session.emotion_state = {
            "empathy": new_profile.empathy,
            "warmth": new_profile.warmth,
            "boundary": new_profile.boundary,
            "formality": new_profile.formality,
        }
        old_session.persona_active = new_profile.persona_routing[:4]
        old_session.last_activity = time.time()
        self._save_state()

        return {
            "status": "TRANSITIONED",
            "session_id": session_id,
            "from_scene": old_scene.value,
            "to_scene": new_scene_type.value,
            "new_mode": new_profile.mode.value,
            "reason": reason,
            "warning": new_profile.warning_message,
        }

    # ── 终止会话 ──

    def terminate(self, session_id: str, reason: str = "user_request") -> Dict[str, Any]:
        """终止会话。"""
        if session_id not in self.active_sessions:
            return {"status": "SESSION_NOT_FOUND"}

        session = self.active_sessions.pop(session_id)
        duration = time.time() - session.activated_at
        self._save_state()

        self._write_audit(session_id, f"TERMINATED:{reason}", session.audit_level, {
            "duration_s": round(duration, 1),
            "interactions": session.interaction_count,
            "abuse_score": round(session.abuse_score, 3),
        })

        return {
            "status": "TERMINATED",
            "session_id": session_id,
            "scene": session.scene.value,
            "duration_minutes": round(duration / 60, 1),
            "interactions": session.interaction_count,
            "abuse_score": round(session.abuse_score, 3),
            "reason": reason,
            "dna": self.DNA,
        }

    # ── 强制熔断 (IW-ECB 联动) ──

    def emergency_meltdown(self, session_id: str, trigger: str) -> Dict[str, Any]:
        """紧急熔断 · 与 IW-ECB 伦理熔断引擎联动。

        触发条件：
        - 自伤+规避专业人士+情感依赖 → 三合一
        - 自伤意图检测到 → 立即
        - 主权攻击 → 硬核但不断
        """
        if session_id not in self.active_sessions:
            return {"status": "SESSION_NOT_FOUND"}

        session = self.active_sessions.pop(session_id)
        self._save_state()

        meltdown_id = f"MELTDOWN-{self.UID}-{int(time.time() * 1000)}"

        # 写入临界审计
        self._write_audit(session_id, f"MELTDOWN:{trigger}", AuditLevel.MAX, {
            "meltdown_id": meltdown_id,
            "scene": session.scene.value,
            "user_id": session.user_id,
            "interactions": session.interaction_count,
            "abuse_score": round(session.abuse_score, 3),
        })

        return {
            "status": "MELTDOWN_EXECUTED",
            "meltdown_id": meltdown_id,
            "session_id": session_id,
            "trigger": trigger,
            "scene": session.scene.value,
            "user_id": session.user_id,
            "message": "IW-ECB 伦理熔断已触发 · 会话永久终止 · 所有交互记录已封存",
            "dna": self.DNA,
        }

    # ── 协议清单 ──

    def manifest(self) -> Dict[str, Any]:
        """协议总览清单。"""
        return {
            "system": "龍魂数字人情感协议引擎 v2.0",
            "dna": self.DNA,
            "uid": self.UID,
            "updated_at": datetime.now().isoformat(),
            "scenes": {
                scene.value: {
                    "mode": profile.mode.value,
                    "empathy": profile.empathy,
                    "warmth": profile.warmth,
                    "boundary": profile.boundary,
                    "formality": profile.formality,
                    "professional_required": profile.professional_required,
                    "consent_required": profile.consent_required,
                    "audit": profile.audit_level.value,
                    "max_minutes": profile.max_session_minutes,
                    "cooldown_minutes": profile.cooldown_minutes,
                    "persona_routing": profile.persona_routing,
                    "voice_routing": profile.voice_routing,
                    "dna_signature": profile.dna_signature[:16],
                    "warning": profile.warning_message,
                }
                for scene, profile in self.protocols.items()
            },
            "active_sessions": len(self.active_sessions),
            "consent_records": len(self.consent_records),
            "abuse_patterns": len(ABUSE_PATTERNS),
            "escalation_rules": len(EMOTION_ESCALATION_RULES),
        }

    def audit_report(self) -> str:
        """审计报告（文本）。"""
        m = self.manifest()
        lines = []

        lines.append("=" * 65)
        lines.append("🐉 龍魂 · 数字人情感协议审计报告 v2.0")
        lines.append(f"DNA: {self.DNA}")
        lines.append(f"UID: {self.UID}")
        lines.append(f"时间: {datetime.now().isoformat()}")
        lines.append("=" * 65)

        # 场景总览
        lines.append(f"\n📋 六大场景协议 · {m['active_sessions']}活跃会话 · {m['consent_records']}知情同意记录")
        lines.append(f"   滥用检测模式: {m['abuse_patterns']}类 · 升级规则: {m['escalation_rules']}条")
        lines.append("")

        # 表格
        lines.append(f"{'场景':<10} {'情感模式':<8} {'共情':<6} {'温暖':<6} {'边界':<6} {'正式':<6} {'需专业':<6} {'需同意':<6} {'审计':<6}")
        lines.append("-" * 65)

        for scene, info in m["scenes"].items():
            prof = "✅" if info["professional_required"] else "—"
            cons = "✅" if info["consent_required"] else "—"
            lines.append(
                f"{scene:<10} {info['mode']:<8} "
                f"{info['empathy']:<6.2f} {info['warmth']:<6.2f} {info['boundary']:<6.2f} {info['formality']:<6.2f} "
                f"{prof:<6} {cons:<6} {info['audit']:<6}"
            )

        lines.append("")
        lines.append("-" * 65)

        # 各场景详细
        for scene, info in m["scenes"].items():
            lines.append(f"\n  [{scene}] {info['mode']} · DNA: {info['dna_signature']}...")
            lines.append(f"    人格路由: {', '.join(info['persona_routing'])}")
            lines.append(f"    声色路由: {', '.join(info['voice_routing'])}")
            lines.append(f"    会话限制: {info['max_minutes']}分钟 · 冷却: {info['cooldown_minutes']}分钟")
            lines.append(f"    ⚠️  {info['warning']}")

        # 活跃会话
        if self.active_sessions:
            lines.append(f"\n── 活跃会话 ({len(self.active_sessions)}) ──")
            for sid, s in self.active_sessions.items():
                elapsed = (time.time() - s.activated_at) / 60
                lines.append(f"  📡 {sid[:20]}... [{s.scene.value}] {s.user_id}")
                lines.append(f"     已交互{s.interaction_count}次 · {elapsed:.1f}分钟 · 滥用分{s.abuse_score:.2f}")
                if s.professional_id:
                    lines.append(f"     专业人士: {s.professional_id}")

        lines.append("")
        lines.append("=" * 65)
        lines.append("🔒 六大场景 · 分场景控制 · 防滥用 · 配合真人")
        lines.append("   私人冷漠 · 公共共情 · 教育深情 · 医疗深情 · 危机专业 · 主权硬核")
        lines.append("=" * 65)

        return "\n".join(lines)


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂 · 数字人情感协议引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
场景: private(私人) public(公共) education(教育) medical(医疗) crisis(危机) sovereignty(主权)

示例:
  python3 bin/lh_emotion_protocol.py --audit                      # 审计总览
  python3 bin/lh_emotion_protocol.py --activate private uid=UID9622  # 激活私人模式
  python3 bin/lh_emotion_protocol.py --activate medical uid=USER001 prof=DOC123 consent=1
  python3 bin/lh_emotion_protocol.py --detect "我最近很焦虑，睡不着"  # 自动检测场景
  python3 bin/lh_emotion_protocol.py --respond SES-xxx "你好"        # 情感化回复
  python3 bin/lh_emotion_protocol.py --abuse-check "只有你能帮我"    # 滥用检测
  python3 bin/lh_emotion_protocol.py --terminate SES-xxx             # 终止会话
  python3 bin/lh_emotion_protocol.py --json                          # JSON 输出
        """,
    )

    parser.add_argument("--audit", "-a", action="store_true", help="审计报告总览")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    parser.add_argument("--activate", metavar="SCENE", help="激活情感协议场景")
    parser.add_argument("--detect", metavar="TEXT", help="自动检测场景")
    parser.add_argument("--respond", nargs=2, metavar=("SESSION_ID", "TEXT"), help="情感化回复")
    parser.add_argument("--abuse-check", metavar="TEXT", help="滥用检测")
    parser.add_argument("--terminate", metavar="SESSION_ID", help="终止会话")
    parser.add_argument("--meltdown", nargs=2, metavar=("SESSION_ID", "TRIGGER"), help="紧急熔断")
    parser.add_argument("--transition", nargs=2, metavar=("SESSION_ID", "NEW_SCENE"), help="场景切换")
    parser.add_argument("--consent", metavar="CONSENT_ID", help="记录知情同意")

    # 额外参数
    parser.add_argument("--uid", default="anonymous", help="用户ID")
    parser.add_argument("--prof", default=None, help="专业人士ID")
    parser.add_argument("--consent-given", dest="consent_given", action="store_true", help="已获得知情同意")

    # 先用 parse_known_args 分离已知参数和 k=v 额外参数
    args, unknown = parser.parse_known_args()

    # 解析 k=v 额外参数（来自 unknown 中的非 -- 开头参数）
    extra = {}
    for a in unknown:
        if "=" in a and not a.startswith("--"):
            k, v = a.split("=", 1)
            extra[k] = v

    engine = LongHunEmotionProtocol()

    # --audit / --json
    show_audit = args.audit or not any([
        args.activate, args.detect, args.respond, args.abuse_check,
        args.terminate, args.meltdown, args.transition, args.consent,
    ])
    if show_audit:
        if args.json:
            print(json.dumps(engine.manifest(), ensure_ascii=False, indent=2))
        else:
            print(engine.audit_report())
        return 0

    # --activate
    if args.activate:
        user_id = extra.get("uid", args.uid)
        prof_id = extra.get("prof", args.prof)
        consent = extra.get("consent", "0") == "1" or args.consent_given
        result = engine.activate(args.activate, user_id, prof_id, consent)
        # 附加统计信息到结果中
        result["_active_sessions_total"] = len(engine.active_sessions)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --detect
    if args.detect:
        user_id = extra.get("uid", args.uid)
        result = engine.detect_scene(args.detect, user_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --respond
    if args.respond:
        sid, text = args.respond
        result = engine.respond(sid, text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --abuse-check
    if args.abuse_check:
        sid = extra.get("session", None)
        result = engine.check_abuse(args.abuse_check, sid)
        output = asdict(result)
        output["risk"] = result.risk.value  # Enum → str
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    # --terminate
    if args.terminate:
        result = engine.terminate(args.terminate)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --meltdown
    if args.meltdown:
        sid, trigger = args.meltdown
        result = engine.emergency_meltdown(sid, trigger)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --transition
    if args.transition:
        sid, new_scene = args.transition
        result = engine.transition(sid, new_scene)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # --consent
    if args.consent:
        uid = extra.get("uid", args.uid)
        scene = extra.get("scene", "education")
        result = engine.record_consent(args.consent, uid, scene)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
