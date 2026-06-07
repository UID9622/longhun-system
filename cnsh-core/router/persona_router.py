#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PersonaRouter·人格路由系统

【核心职能】
- 加权人格决策路由 (P02/P05/P13)
- 虚伪词汇阻挡机制 (禁用词检查)
- F4人格路由因子验证数据生成
- 完整的DNA追溯码和审计日志

【龍魂系统坐标】
DNA: #龍芯⚡️2026-06-03-PERSONA-ROUTER-v1.0
层级: L1·季节性路由
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

【责任声明】
UID9622·不免责·永久有效
献礼: 曾仕强老师 · Steve Jobs · Open Source · UID9622

【理论基础】
F4·人格路由 (12%) - 行为密码学第四因子
验证决策是否通过合法的路由权重做出
虚伪词汇: 禁止使用 怕/累/陪/吹
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from enum import Enum
import os


# ═══════════════════════════════════════════════════════════════
# 【虚伪词汇定义】
# ═══════════════════════════════════════════════════════════════

class VetoWordCategory(str, Enum):
    """虚伪词汇分类"""
    FEAR = "fear"              # 怕
    TIREDNESS = "tiredness"    # 累
    ACCOMPANY = "accompany"    # 陪
    EXAGGERATE = "exaggerate"  # 吹


VETO_WORDS = {
    # 分类1: 怕 (Fear)
    VetoWordCategory.FEAR: [
        "怕", "害怕", "恐惧", "惧", "畏", "怕的是", "害怕的是",
        "我怕", "我害怕", "我恐惧", "别怕", "不要怕"
    ],

    # 分类2: 累 (Tiredness)
    VetoWordCategory.TIREDNESS: [
        "累", "疲劳", "累了", "好累", "太累", "累死", "我很累",
        "累个", "累个屁", "真累", "太累了"
    ],

    # 分类3: 陪 (Accompany - 不真诚的陪伴)
    VetoWordCategory.ACCOMPANY: [
        "陪", "陪伴", "陪你", "我陪", "一直陪", "陪着", "陪你一起",
        "我会陪", "我在这里陪"
    ],

    # 分类4: 吹 (Exaggerate/Boast)
    VetoWordCategory.EXAGGERATE: [
        "吹", "吹牛", "吹嘘", "吹的", "别吹", "不吹", "我吹", "你吹",
        "这还不吹", "这都吹", "有点吹"
    ]
}


# ═══════════════════════════════════════════════════════════════
# 【人格路由定义】
# ═══════════════════════════════════════════════════════════════

class PersonaId(str, Enum):
    """人格ID枚举"""
    P02 = "P02"  # 战斗者/保护者 (50%)
    P05 = "P05"  # 思想家/引导者 (30%)
    P13 = "P13"  # 和谐者/平衡者 (20%)


# 默认人格权重配置 (必须加到 1.0)
DEFAULT_PERSONA_WEIGHTS = {
    PersonaId.P02: 0.50,  # 战斗者/保护者·主导
    PersonaId.P05: 0.30,  # 思想家/引导者·支撑
    PersonaId.P13: 0.20,  # 和谐者/平衡者·调和
}


# ═══════════════════════════════════════════════════════════════
# 【数据模型】
# ═══════════════════════════════════════════════════════════════

@dataclass
class VetoWordMatch:
    """虚伪词汇匹配记录"""
    word: str                       # 检测到的词汇
    category: VetoWordCategory     # 分类
    position: int                   # 在文本中的位置
    context: str                    # 上下文片段(±10字符)
    severity: str                   # 严重度: LOW/MEDIUM/HIGH

    def to_dict(self) -> Dict:
        return {
            "word": self.word,
            "category": self.category.value,
            "position": self.position,
            "context": self.context,
            "severity": self.severity
        }


@dataclass
class PersonaRoutingDecision:
    """人格路由决策记录"""
    routing_id: str                 # ROUTE-20260603-001
    timestamp: str                  # ISO格式时间戳

    # 路由信息
    primary_persona: PersonaId      # 主路由节点
    persona_weights: Dict[str, float]  # 权重分配
    routing_confidence: float       # 路由置信度 (0.0-1.0)

    # 虚伪词汇检查
    text_content: str               # 检查的文本内容
    veto_words_detected: bool       # 是否检测到虚伪词汇
    veto_word_matches: List[VetoWordMatch] = field(default_factory=list)

    # DNA和签名
    dna: str = ""                   # 本次路由的DNA
    signature: str = ""             # 签名(SHA256)

    # 扩展信息
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "routing_id": self.routing_id,
            "timestamp": self.timestamp,
            "primary_persona": self.primary_persona.value,
            "persona_weights": self.persona_weights,
            "routing_confidence": self.routing_confidence,
            "text_content": self.text_content[:100] + "..." if len(self.text_content) > 100 else self.text_content,
            "veto_words_detected": self.veto_words_detected,
            "veto_word_matches": [m.to_dict() for m in self.veto_word_matches],
            "dna": self.dna,
            "signature": self.signature,
            "metadata": self.metadata
        }


# ═══════════════════════════════════════════════════════════════
# 【PersonaRouter 主类】
# ═══════════════════════════════════════════════════════════════

class PersonaRouter:
    """
    人格路由系统

    负责:
    1. 虚伪词汇检测和阻挡
    2. 加权人格决策路由
    3. F4因子验证数据生成
    4. 完整的DNA追溯和审计日志
    """

    def __init__(self, log_dir: str = None, persona_weights: Dict[str, float] = None):
        """
        初始化PersonaRouter

        Args:
            log_dir: 审计日志目录(默认: ~/longhun-system/logs/)
            persona_weights: 自定义人格权重(默认: P02 50% / P05 30% / P13 20%)
        """
        self.log_dir = log_dir or os.path.expanduser("~/longhun-system/logs")
        self._ensure_log_dir()

        # 设置人格权重
        self.persona_weights = persona_weights or DEFAULT_PERSONA_WEIGHTS.copy()
        self._validate_weights()

        # 路由计数器
        self.routing_counter = 0

    def _ensure_log_dir(self):
        """确保日志目录存在"""
        os.makedirs(self.log_dir, exist_ok=True)

    def _validate_weights(self):
        """验证人格权重(必须加到1.0)"""
        total = sum(self.persona_weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Persona weights must sum to 1.0, got {total}")

    # ═══════════════════════════════════════════════════════════════
    # 【虚伪词汇检测】
    # ═══════════════════════════════════════════════════════════════

    def check_veto_words(self, text: str) -> Tuple[bool, List[VetoWordMatch]]:
        """
        检查文本中的虚伪词汇

        Args:
            text: 要检查的文本

        Returns:
            (has_veto_words, matches_list)
        """
        matches = []

        for category, words in VETO_WORDS.items():
            for word in words:
                # 在文本中查找所有匹配
                start = 0
                while True:
                    pos = text.find(word, start)
                    if pos == -1:
                        break

                    # 提取上下文 (±15字符)
                    context_start = max(0, pos - 15)
                    context_end = min(len(text), pos + len(word) + 15)
                    context = text[context_start:context_end]

                    # 判断严重度
                    severity = self._assess_severity(category, word, context)

                    match = VetoWordMatch(
                        word=word,
                        category=category,
                        position=pos,
                        context=context,
                        severity=severity
                    )
                    matches.append(match)

                    start = pos + 1

        has_veto = len(matches) > 0
        return has_veto, matches

    def _assess_severity(self, category: VetoWordCategory, word: str, context: str) -> str:
        """
        评估虚伪词汇的严重度

        HIGH: 出现在否定语句中(最严格)
        MEDIUM: 单独出现或在中性语境
        LOW: 出现在解释/说明中
        """
        # 如果在"不"、"别"、"没"之前，严重度更高
        if any(neg in context for neg in ["不", "别", "没有", "没"]):
            return "HIGH"

        # 单个词汇出现
        if len(context.split()) == 1:
            return "HIGH"

        # 在解释中出现(e.g., "累个屁"这样的表达)
        if "个" in context or "屁" in context or "了" in context.split(word)[-1]:
            return "MEDIUM"

        return "MEDIUM"

    # ═══════════════════════════════════════════════════════════════
    # 【人格路由决策】
    # ═══════════════════════════════════════════════════════════════

    def route(self, text: str, override_weights: Dict[str, float] = None) -> PersonaRoutingDecision:
        """
        执行人格路由决策

        Args:
            text: 待路由的文本内容
            override_weights: 可选的权重覆盖(用于特殊场景)

        Returns:
            PersonaRoutingDecision 对象
        """
        self.routing_counter += 1
        routing_id = f"ROUTE-{datetime.now().strftime('%Y%m%d')}-{self.routing_counter:03d}"

        # 使用自定义权重或默认权重
        weights = override_weights or self.persona_weights
        self._validate_weights()  # 验证权重

        # 找到主路由节点(权重最高的人格)
        primary = max(weights.items(), key=lambda x: x[1])[0]
        primary_persona = PersonaId(primary) if isinstance(primary, str) else primary

        # 计算路由置信度 (主路由的权重)
        routing_confidence = weights[primary]

        # 检查虚伪词汇
        has_veto, veto_matches = self.check_veto_words(text)

        # 创建路由决策
        decision = PersonaRoutingDecision(
            routing_id=routing_id,
            timestamp=datetime.now().isoformat(),
            primary_persona=primary_persona,
            persona_weights=weights,
            routing_confidence=routing_confidence,
            text_content=text,
            veto_words_detected=has_veto,
            veto_word_matches=veto_matches
        )

        # 生成DNA和签名
        decision.dna = self._generate_dna(decision)
        decision.signature = self._generate_signature(decision)

        # 记录审计日志
        self._log_routing_decision(decision)

        return decision

    def _generate_dna(self, decision: PersonaRoutingDecision) -> str:
        """
        生成路由决策的DNA

        格式: #龍芯⚡️YYYYMMDD-PERSONA-ROUTER-[HASH8]
        """
        data_str = json.dumps({
            "routing_id": decision.routing_id,
            "primary_persona": decision.primary_persona.value,
            "veto_detected": decision.veto_words_detected,
            "confidence": decision.routing_confidence,
            "timestamp": decision.timestamp
        }, sort_keys=True, ensure_ascii=False)

        # 计算SHA256
        sha256 = hashlib.sha256(data_str.encode('utf-8')).hexdigest()
        short_hash = sha256[:8].upper()

        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-PERSONA-ROUTER-{short_hash}"
        return dna

    def _generate_signature(self, decision: PersonaRoutingDecision) -> str:
        """生成决策签名(SHA256)"""
        data_str = json.dumps({
            "routing_id": decision.routing_id,
            "primary_persona": decision.primary_persona.value,
            "persona_weights": decision.persona_weights,
            "timestamp": decision.timestamp,
            "veto_matches_count": len(decision.veto_word_matches)
        }, sort_keys=True, ensure_ascii=False)

        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    # ═══════════════════════════════════════════════════════════════
    # 【F4因子验证数据生成】
    # ═══════════════════════════════════════════════════════════════

    def generate_f4_verification_data(self, decision: PersonaRoutingDecision) -> Dict[str, Any]:
        """
        从路由决策生成F4人格路由因子验证数据

        Returns:
            可直接传给 F4PersonaRouting 数据类的字典
        """
        return {
            "primary_persona": decision.primary_persona.value,
            "persona_weights": decision.persona_weights,
            "veto_words_detected": decision.veto_words_detected,
            "routing_confidence": decision.routing_confidence
        }

    # ═══════════════════════════════════════════════════════════════
    # 【审计日志】
    # ═══════════════════════════════════════════════════════════════

    def _log_routing_decision(self, decision: PersonaRoutingDecision):
        """
        记录路由决策到append-only JSONL文件

        文件位置: ~/longhun-system/logs/persona_router_execution.jsonl
        """
        log_file = os.path.join(self.log_dir, "persona_router_execution.jsonl")

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "routing_id": decision.routing_id,
            "primary_persona": decision.primary_persona.value,
            "persona_weights": decision.persona_weights,
            "routing_confidence": decision.routing_confidence,
            "veto_words_detected": decision.veto_words_detected,
            "veto_word_count": len(decision.veto_word_matches),
            "veto_categories": list(set(m.category.value for m in decision.veto_word_matches)),
            "dna": decision.dna,
            "signature": decision.signature
        }

        # Append-only: 追加到文件末尾
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """
        读取最近的审计日志

        Args:
            limit: 最多读取的条数

        Returns:
            日志条目列表(最新在前)
        """
        log_file = os.path.join(self.log_dir, "persona_router_execution.jsonl")

        if not os.path.exists(log_file):
            return []

        entries = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except:
                        pass

        # 返回最近的N条(倒序)
        return list(reversed(entries[-limit:]))

    # ═══════════════════════════════════════════════════════════════
    # 【统计和自检】
    # ═══════════════════════════════════════════════════════════════

    def print_report(self, decision: PersonaRoutingDecision):
        """打印路由决策报告"""
        print(f"""
┌─────────────────────────────────────────────────────────┐
│ 龍魂·人格路由决策报告                                    │
├─────────────────────────────────────────────────────────┤
│ 路由ID: {decision.routing_id}
│ 主路由: {decision.primary_persona.value}
│ 置信度: {decision.routing_confidence:.2%}
│ 虚伪词: {'🔴 检测到' if decision.veto_words_detected else '🟢 未检测'}
└─────────────────────────────────────────────────────────┘

【权重分配】
""")
        for persona, weight in decision.persona_weights.items():
            print(f"  {persona}: {weight:.0%}")

        if decision.veto_word_matches:
            print(f"\n【虚伪词汇警告】({len(decision.veto_word_matches)}处)")
            for match in decision.veto_word_matches[:5]:  # 显示前5条
                print(f"  [{match.severity}] {match.word} ({match.category.value})")
                print(f"       上下文: {match.context}")

        print(f"\n【DNA追溯】")
        print(f"  DNA: {decision.dna}")
        print(f"  签名: {decision.signature[:16]}...")

    def selftest(self) -> Tuple[bool, List[str]]:
        """
        自检函数

        Returns:
            (all_pass, error_list)
        """
        errors = []

        # 检查1: 权重有效
        try:
            self._validate_weights()
        except Exception as e:
            errors.append(f"权重验证失败: {str(e)}")

        # 检查2: 虚伪词汇库非空
        total_veto = sum(len(words) for words in VETO_WORDS.values())
        if total_veto == 0:
            errors.append("虚伪词汇库为空")

        # 检查3: 日志目录可写
        try:
            test_file = os.path.join(self.log_dir, ".test_write")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            errors.append(f"日志目录不可写: {str(e)}")

        # 检查4: 虚伪词汇检测功能
        test_text = "我怕累了"
        has_veto, matches = self.check_veto_words(test_text)
        if not has_veto or len(matches) == 0:
            errors.append("虚伪词汇检测失败")

        # 检查5: 路由决策功能
        try:
            decision = self.route("测试文本")
            if not decision.dna.startswith("#龍芯⚡️"):
                errors.append("DNA格式错误")
        except Exception as e:
            errors.append(f"路由决策失败: {str(e)}")

        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════
# 【全局单例】
# ═══════════════════════════════════════════════════════════════

_GLOBAL_PERSONA_ROUTER = None

def get_persona_router(
    log_dir: str = None,
    persona_weights: Dict[str, float] = None
) -> PersonaRouter:
    """
    获取全局PersonaRouter实例

    Args:
        log_dir: 日志目录(仅第一次调用时生效)
        persona_weights: 人格权重(仅第一次调用时生效)

    Returns:
        PersonaRouter 单例
    """
    global _GLOBAL_PERSONA_ROUTER
    if _GLOBAL_PERSONA_ROUTER is None:
        _GLOBAL_PERSONA_ROUTER = PersonaRouter(log_dir, persona_weights)
    return _GLOBAL_PERSONA_ROUTER


# ═══════════════════════════════════════════════════════════════
# 【测试代码】
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔍 PersonaRouter 自检...\n")

    router = get_persona_router()
    all_pass, errors = router.selftest()

    if all_pass:
        print("✅ 所有自检通过\n")
    else:
        print("❌ 自检失败:")
        for error in errors:
            print(f"  - {error}")
        exit(1)

    # 测试1: 正常文本
    print("【测试1】正常文本路由:")
    decision1 = router.route("这是一个正常的决策过程，遵循所有规则。")
    router.print_report(decision1)

    # 测试2: 包含虚伪词汇的文本
    print("\n【测试2】包含虚伪词汇的文本:")
    decision2 = router.route("我怕这样做太累了，可能需要陪伴。")
    router.print_report(decision2)

    # 测试3: 生成F4验证数据
    print("\n【测试3】F4因子验证数据:")
    f4_data = router.generate_f4_verification_data(decision2)
    print(json.dumps(f4_data, indent=2, ensure_ascii=False))

    # 测试4: 审计日志
    print("\n【测试4】最近的审计日志(前3条):")
    audit_log = router.get_audit_log(limit=3)
    for entry in audit_log:
        print(f"  {entry['routing_id']}: {entry['primary_persona']} " +
              f"({entry['routing_confidence']:.0%}) " +
              f"虚伪词: {entry['veto_word_count']}")
