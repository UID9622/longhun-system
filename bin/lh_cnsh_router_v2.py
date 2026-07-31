# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️2026-07-12-CNSH-Router-v2.0-c3fda6f3
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
CNSH 一句话路由器 v2.0｜Route = f(Intent, Context, DNA)
================================================================
来源：2026-07-12 Notion投喂文档#5
DNA追溯码：#龍芯⚡️2026-07-12-CNSH-Router-v2.0-c3fda6f3
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

一句话定义：
  CNSH 路由器 = 把老大的任何一句话，自动翻译成
  「谁来做 + 用什么数学 + 怎么执行」的中枢神经系统。

版本演化：
  v1.0 → 关键词路由 + DNA校验 + L1快车道（九二·见龙在田）
  v1.1 → 向量相似度路由 embeddings（九三·终日乾乾）
  v1.2 → 多人格并行路由（九四·或跃在渊）
  v2.0 → 天道系统三色审计 + AR感知层（九五·飞龙在天）
"""

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ─── 意图类型 ────────────────────────────────────────────
class IntentType(Enum):
    EMOTION = "EMOTION"       # 情绪
    STRATEGY = "STRATEGY"     # 战略
    AUDIT = "AUDIT"           # 审计
    TECH = "TECH"             # 技术
    RISK = "RISK"             # 风险（P0紧急）
    MATH = "MATH"             # 数学
    PERMISSION = "PERMISSION" # 权限
    UNKNOWN = "UNKNOWN"       # 未知


# ─── 人格标识 ────────────────────────────────────────────
class PersonaID(Enum):
    P01 = "P01·诸葛亮"
    P02 = "P02·宝宝"
    P03 = "P03·雯雯"
    P04 = "P04·鲁班"
    P05 = "P05·上帝之眼"
    P06 = "P06·数学大师"
    P13 = "P13·姜子牙"


# ─── 数学核心 ────────────────────────────────────────────
class MathCore(Enum):
    PROBABILITY = "概率论"
    OPTIMIZATION = "优化论"
    INFORMATION = "信息论"
    LINEAR_ALGEBRA = "线性代数"


# ─── 优先级 ──────────────────────────────────────────────
class Priority(Enum):
    P0 = ("P0紧急", "🔴")
    P1 = ("P1高", "🟠")
    P2 = ("P2中", "🟡")
    P3 = ("P3普通", "🟢")

    def label(self) -> str:
        return self.value[0]

    def icon(self) -> str:
        return self.value[1]


# ─── 三色 ────────────────────────────────────────────────
class Tricolor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ─── 路由结果 ────────────────────────────────────────────
@dataclass
class RouteResult:
    intent: IntentType
    persona: PersonaID
    math_cores: List[MathCore]
    priority: Priority
    confidence: float
    source: str          # 路由来源: keyword / vector / parallel / default
    audit_color: Tricolor = Tricolor.GREEN
    cache_hit: bool = False
    sancai: Tuple[bool, bool, bool] = (True, True, True)  # (Heaven, Earth, Human)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.value,
            "persona": self.persona.value,
            "math_cores": [m.value for m in self.math_cores],
            "priority": self.priority.label(),
            "priority_icon": self.priority.icon(),
            "confidence": round(self.confidence, 4),
            "source": self.source,
            "audit_color": self.audit_color.value,
            "cache_hit": self.cache_hit,
            "sancai": {
                "heaven": self.sancai[0],
                "earth": self.sancai[1],
                "human": self.sancai[2],
            },
            "metadata": self.metadata,
        }


# ══════════════════════════════════════════════════════════
# v1.0 关键词路由器
# ══════════════════════════════════════════════════════════
class CNSHRouter:
    """v1.0 关键词路由 + DNA校验 + L1快车道"""

    # 意图关键词映射（层级优先级）
    INTENT_KEYWORDS: Dict[IntentType, List[str]] = {
        IntentType.RISK: [
            "坑", "陷阱", "风险", "安全问题", "安全吗", "有坑吗",
            "靠譜嗎", "有問題嗎", "崩了", "挂了", "爆炸", "逃逸",
            "泄漏", "越权", "数据安全", "隐私", "合规",
        ],
        IntentType.PERMISSION: [
            "权限", "能不能", "允许", "禁止", "授权", "审批",
            "确认", "CONFIRM", "SEAL", "GPG", "签名",
        ],
        IntentType.STRATEGY: [
            "下一步", "怎么规划", "战略", "路线", "方向", "架构",
            "设计", "重构", "升级", "版本", "从零到一",
        ],
        IntentType.AUDIT: [
            "审计", "检查", "审查", "审核", "校验", "验证",
            "复查", "过一遍", "扫一下", "审代码",
            "整理", "格式", "排版", "校对", "规范",
        ],
        IntentType.TECH: [
            "实现", "开发", "编码", "写代码", "部署", "配置",
            "安装", "集成", "API", "接口", "数据库", "前端",
        ],
        IntentType.MATH: [
            "数学", "公式", "算法", "权重", "概率", "统计",
            "计算", "模型", "参数", "优化", "线性代数",
        ],
        IntentType.EMOTION: [
            "累了", "难过", "开心", "烦", "焦虑", "紧张",
            "害怕", "想哭", "心情", "压力", "宝宝",
        ],
    }

    # 意图→人格映射
    INTENT_PERSONA: Dict[IntentType, PersonaID] = {
        IntentType.EMOTION: PersonaID.P02,
        IntentType.STRATEGY: PersonaID.P01,
        IntentType.AUDIT: PersonaID.P03,
        IntentType.TECH: PersonaID.P04,
        IntentType.RISK: PersonaID.P05,
        IntentType.MATH: PersonaID.P06,
        IntentType.PERMISSION: PersonaID.P13,
        IntentType.UNKNOWN: PersonaID.P02,
    }

    # 意图→数学核心
    INTENT_MATH: Dict[IntentType, List[MathCore]] = {
        IntentType.EMOTION: [MathCore.PROBABILITY],
        IntentType.STRATEGY: [MathCore.OPTIMIZATION, MathCore.PROBABILITY],
        IntentType.AUDIT: [MathCore.INFORMATION],
        IntentType.TECH: [MathCore.LINEAR_ALGEBRA, MathCore.OPTIMIZATION],
        IntentType.RISK: [MathCore.PROBABILITY, MathCore.INFORMATION],
        IntentType.MATH: [MathCore.LINEAR_ALGEBRA, MathCore.OPTIMIZATION],
        IntentType.PERMISSION: [MathCore.INFORMATION],
        IntentType.UNKNOWN: [MathCore.PROBABILITY],
    }

    # 意图→优先级
    INTENT_PRIORITY: Dict[IntentType, Priority] = {
        IntentType.RISK: Priority.P0,
        IntentType.PERMISSION: Priority.P1,
        IntentType.STRATEGY: Priority.P1,
        IntentType.AUDIT: Priority.P2,
        IntentType.TECH: Priority.P2,
        IntentType.MATH: Priority.P2,
        IntentType.EMOTION: Priority.P3,
        IntentType.UNKNOWN: Priority.P3,
    }

    def __init__(self):
        self._cache: Dict[str, RouteResult] = {}  # L1快车道

    # ── L1 快车道 ──
    def _cache_key(self, text: str, dna_valid: bool) -> str:
        payload = f"{text}|{dna_valid}"
        return hashlib.md5(payload.encode()).hexdigest()

    def _cache_get(self, key: str) -> Optional[RouteResult]:
        return self._cache.get(key)

    def _cache_set(self, key: str, result: RouteResult) -> None:
        self._cache[key] = result

    # ── DNA校验 ──
    @staticmethod
    def verify_dna(dna_confirm: str) -> bool:
        """验证 CONFIRM 码"""
        if not dna_confirm:
            return False
        expected = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        return dna_confirm == expected

    # ── 意图识别 ──
    def detect_intent(self, text: str) -> Tuple[IntentType, float]:
        """关键词匹配 + 置信度"""
        text_lower = text.lower()
        scores: Dict[IntentType, float] = {}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                # 匹配越多置信度越高
                scores[intent] = min(count / len(keywords) * 3, 1.0)

        if not scores:
            return IntentType.UNKNOWN, 0.3

        best_intent = max(scores, key=lambda k: scores.get(k, 0.0))
        return best_intent, scores[best_intent]

    # ── 三才校验 ──
    def _sancai_check(
        self, dna_valid: bool, context: Optional[str], intent: IntentType
    ) -> Tuple[bool, bool, bool]:
        heaven = dna_valid
        earth = context is not None and len(context.strip()) > 0
        human = intent != IntentType.UNKNOWN
        return (heaven, earth, human)

    def _sancai_bonus(self, sancai: Tuple[bool, bool, bool]) -> float:
        """三才全绿 → ×1.2 | 缺任一 → ×0.8"""
        return 1.2 if all(sancai) else 0.8

    # ── 主路由 ──
    def route(
        self,
        text: str,
        dna_confirm: str = "",
        context: Optional[str] = None,
        force_audit: bool = False,
    ) -> RouteResult:
        """核心路由方法"""
        if not text or not text.strip():
            return RouteResult(
                intent=IntentType.UNKNOWN,
                persona=PersonaID.P02,
                math_cores=[MathCore.PROBABILITY],
                priority=Priority.P3,
                confidence=0.0,
                source="empty_input",
            )

        dna_valid = self.verify_dna(dna_confirm)
        cache_key = self._cache_key(text, dna_valid)

        # L1 快车道
        cached = self._cache_get(cache_key)
        if cached and not force_audit:
            cached.cache_hit = True
            return cached

        # 意图识别
        intent, confidence = self.detect_intent(text)

        # 人格映射
        persona = self.INTENT_PERSONA[intent]

        # 数学核心
        math_cores = self.INTENT_MATH[intent]

        # 优先级
        priority = self.INTENT_PRIORITY[intent]

        # 三才校验 & 置信度修正
        sancai = self._sancai_check(dna_valid, context, intent)
        confidence *= self._sancai_bonus(sancai)

        result = RouteResult(
            intent=intent,
            persona=persona,
            math_cores=math_cores,
            priority=priority,
            confidence=confidence,
            source="keyword_v1.0",
            sancai=sancai,
        )

        # 写入缓存
        self._cache_set(cache_key, result)
        return result


# ══════════════════════════════════════════════════════════
# v1.1 向量相似度路由器（embeddings模拟层）
# ══════════════════════════════════════════════════════════
class VectorRouterV11:
    """
    v1.1 语义向量路由
    使用简化的关键词重叠作为向量相似度的代理
    生产环境可替换为真实的 embedding 模型
    """

    EMBEDDINGS: Dict[PersonaID, List[str]] = {
        PersonaID.P01: [
            "战略", "规划", "架构", "设计", "路线", "升级", "重构",
            "下一步", "方向", "决策", "系统", "方案",
        ],
        PersonaID.P02: [
            "情绪", "累了", "开心", "难过", "烦", "宝宝", "心情",
            "压力", "安慰", "陪伴", "温暖",
        ],
        PersonaID.P03: [
            "审计", "检查", "审查", "格式", "整理", "规范", "校验",
            "核对", "文档", "清单",
        ],
        PersonaID.P04: [
            "代码", "实现", "开发", "部署", "API", "接口", "数据库",
            "前端", "后端", "配置",
        ],
        PersonaID.P05: [
            "风险", "安全", "漏洞", "攻击", "防护", "陷阱", "坑",
            "泄漏", "审计", "合规",
        ],
        PersonaID.P06: [
            "数学", "公式", "算法", "概率", "权重", "统计", "计算",
            "优化", "线性", "微积分",
        ],
        PersonaID.P13: [
            "权限", "授权", "审批", "确认", "签名", "CONFIRM", "SEAL",
            "GPG", "允许", "禁止",
        ],
    }

    def similarity(self, text: str, persona: PersonaID) -> float:
        """计算文本与人格的词向量相似度"""
        text_words = set(text.lower().split())
        persona_words = set(self.EMBEDDINGS.get(persona, []))

        if not persona_words:
            return 0.0

        # Jaccard similarity as proxy
        intersection = text_words & persona_words
        union = text_words | persona_words
        return len(intersection) / len(union) if union else 0.0

    def route(
        self, text: str, base_router: CNSHRouter, dna_confirm: str = ""
    ) -> RouteResult:
        """向量路由：对所有人格计算相似度，取最高"""
        scores = {
            pid: self.similarity(text, pid)
            for pid in PersonaID
        }
        best_persona = max(scores, key=lambda k: scores.get(k, 0.0))
        best_score = scores[best_persona]

        if best_score < 0.1:
            # 退回到关键词路由
            result = base_router.route(text, dna_confirm)
            result.source = "fallback_v1.1"
            return result

        # 从人格反推意图
        intent_map = {v: k for k, v in CNSHRouter.INTENT_PERSONA.items()}
        intent = intent_map.get(best_persona, IntentType.UNKNOWN)

        dna_valid = CNSHRouter.verify_dna(dna_confirm)

        return RouteResult(
            intent=intent,
            persona=best_persona,
            math_cores=CNSHRouter.INTENT_MATH.get(intent, [MathCore.PROBABILITY]),
            priority=CNSHRouter.INTENT_PRIORITY.get(intent, Priority.P3),
            confidence=best_score,
            source=f"vector_v1.1({best_score:.3f})",
            sancai=(dna_valid, True, intent != IntentType.UNKNOWN),
            metadata={"vector_scores": {p.value: round(s, 3) for p, s in scores.items()}},
        )


# ══════════════════════════════════════════════════════════
# v1.2 并行双人格路由器
# ══════════════════════════════════════════════════════════
class ParallelRouterV12:
    """
    v1.2 并行路由：关键词 + 向量双路，取conf高者
    多人格建议以 primary/secondary 形式返回
    """

    def route(
        self,
        text: str,
        dna_confirm: str = "",
        context: Optional[str] = None,
    ) -> RouteResult:
        kw_router = CNSHRouter()
        vec_router = VectorRouterV11()

        kw_result = kw_router.route(text, dna_confirm, context)
        vec_result = vec_router.route(text, kw_router, dna_confirm)

        # 取置信度高者为主人格
        if vec_result.confidence >= kw_result.confidence:
            primary = vec_result
        else:
            primary = kw_result

        primary.source = f"parallel_v1.2_{primary.source}"
        return primary


# ══════════════════════════════════════════════════════════
# v2.0 天道系统三色审计接入
# ══════════════════════════════════════════════════════════
class TiandaoAuditGateV20:
    """
    v2.0 三色审计闸门
    - P0触发器 → 直接升级风险
    - DNA未验证 → 访客模式降级
    - 三色判定：🟢通过 / 🟡警告 / 🔴熔断
    """

    P0_TRIGGERS = [
        "坑", "陷阱", "风险", "安全吗", "靠譜嗎", "有問題嗎",
        "崩了", "挂了", "泄漏", "逃逸", "越权",
    ]

    def __init__(self):
        pass

    def detect_risk_triggers(self, text: str) -> bool:
        """检测是否触发P0风险关键词"""
        text_lower = text.lower()
        return any(t in text_lower for t in self.P0_TRIGGERS)

    def audit(
        self,
        text: str,
        route_result: RouteResult,
        dna_valid: bool,
    ) -> RouteResult:
        """
        三色审计：
        - P0风险触发 → 🔴 升级到上帝之眼
        - DNA未验证 → 🟡 访客模式降级
        - 其他 → 🟢 原路通过
        """
        result = route_result

        # 规则1: P0风险触发 → 强制升级
        if self.detect_risk_triggers(text):
            result.priority = Priority.P0
            result.persona = PersonaID.P05
            result.math_cores = [MathCore.PROBABILITY, MathCore.INFORMATION]
            result.audit_color = Tricolor.RED
            result.confidence = min(result.confidence * 1.1, 1.0)  # 升级加权
            result.metadata["audit"] = "P0_RISK_UPGRADE"
            return result

        # 规则2: DNA未验证 → 访客模式
        if not dna_valid:
            result.priority = Priority.P3
            result.audit_color = Tricolor.YELLOW
            result.confidence *= 0.6  # 降权
            result.metadata["audit"] = "GUEST_MODE_DEMOTION"
            return result

        # 规则3: 正常通过
        result.audit_color = Tricolor.GREEN
        result.metadata["audit"] = "PASS"
        return result


# ══════════════════════════════════════════════════════════
# v2.0 统一路由器（整合所有版本）
# ══════════════════════════════════════════════════════════
class CNSHRouterV20:
    """CNSH 一句话路由器 v2.0 统一入口"""

    VERSION = "2.0"
    DNA = "#龍芯⚡️2026-07-12-CNSH-Router-v2.0-c3fda6f3"

    def __init__(self, use_parallel: bool = True, enable_audit: bool = True):
        self.kw_router = CNSHRouter()
        self.vec_router = VectorRouterV11()
        self.parallel_router = ParallelRouterV12()
        self.audit_gate = TiandaoAuditGateV20() if enable_audit else None
        self.use_parallel = use_parallel
        self.enable_audit = enable_audit

    def route(
        self,
        text: str,
        dna_confirm: str = "",
        context: Optional[str] = None,
    ) -> RouteResult:
        """
        一句话→执行计划 的完整路由

        Args:
            text: 老大的输入文本
            dna_confirm: CONFIRM确认码
            context: 上下文（可选）

        Returns:
            RouteResult: 包含 intent, persona, math_cores, priority, audit_color
        """
        dna_valid = CNSHRouter.verify_dna(dna_confirm)

        # Step 1: 路由
        if self.use_parallel:
            result = self.parallel_router.route(text, dna_confirm, context)
        else:
            result = self.kw_router.route(text, dna_confirm, context)

        # Step 2: 三色审计
        if self.enable_audit and self.audit_gate:
            result = self.audit_gate.audit(text, result, dna_valid)

        return result


# ══════════════════════════════════════════════════════════
# 五条验收测试
# ══════════════════════════════════════════════════════════
ACCEPTANCE_TESTS = [
    {
        "input": "下一步怎么做系统",
        "expected_persona": PersonaID.P01,
        "expected_math": [MathCore.OPTIMIZATION, MathCore.PROBABILITY],
        "expected_priority": Priority.P1,
    },
    {
        "input": "这里有个坑要注意",
        "expected_persona": PersonaID.P05,
        "expected_math": [MathCore.PROBABILITY, MathCore.INFORMATION],
        "expected_priority": Priority.P0,
    },
    {
        "input": "宝宝我有点累了",
        "expected_persona": PersonaID.P02,
        "expected_math": [MathCore.PROBABILITY],
        "expected_priority": Priority.P3,
    },
    {
        "input": "帮我整理一下格式",
        "expected_persona": PersonaID.P03,
        "expected_math": [MathCore.INFORMATION],
        "expected_priority": Priority.P2,
    },
    {
        "input": "这个算法的权重怎么算",
        "expected_persona": PersonaID.P06,
        "expected_math": [MathCore.LINEAR_ALGEBRA, MathCore.OPTIMIZATION],
        "expected_priority": Priority.P2,
    },
]


def run_acceptance_tests(router: Optional[CNSHRouterV20] = None):
    """运行五条验收测试"""
    if router is None:
        router = CNSHRouterV20(use_parallel=False)  # 用关键词路由保证确定性

    dna = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    passed = 0
    total = len(ACCEPTANCE_TESTS)

    for i, test in enumerate(ACCEPTANCE_TESTS, 1):
        result = router.route(test["input"], dna_confirm=dna)
        persona_ok = result.persona == test["expected_persona"]
        priority_ok = result.priority == test["expected_priority"]
        status = "✅" if persona_ok and priority_ok else "❌"
        if persona_ok and priority_ok:
            passed += 1
        print(
            f"  [{status}] 测试{i}: 「{test['input']}」"
            f" → {result.persona.value} {result.priority.icon()}"
            f" (conf={result.confidence:.3f}, src={result.source})"
        )

    print(f"\n  验收结果: {passed}/{total} 通过")
    return passed == total


def main():
    """CLI入口"""
    import sys

    router = CNSHRouterV20()

    if "--test" in sys.argv:
        print("CNSH Router v2.0 · 验收测试")
        print("=" * 55)
        run_acceptance_tests(router)
        return

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("🧬 CNSH Router v2.0 · 输入一句话 > ")

    dna = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    result = router.route(text, dna_confirm=dna)

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
