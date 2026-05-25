#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 CNSH 可執行框架 v1.0
DNA: #龍芯⚡️2026-05-25-CNSH-RUNTIME-COMPLETE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心公式: Route = f(Intent, Context, DNA)

包含：
  - 路由器（v1.0-v2.0）
  - 三色審計（天道系統）
  - 多人格並行
  - DNA校驗
  - L1快車道快取
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math

# ════════════════════════════════════════════════════════════════
# 第一部分：意圖定義與人格映射
# ════════════════════════════════════════════════════════════════

class IntentType(Enum):
    """龍魂七大意圖類型"""
    EMOTION    = "emotion"      # 情緒/日常   → P02宝宝
    STRATEGY   = "strategy"     # 戰略推演    → P01諸葛亮
    AUDIT      = "audit"        # 審計整理    → P03雯雯
    TECH       = "tech"         # 代碼技術    → P04魯班
    RISK       = "risk"         # 風險識別    → P05上帝之眼 (P0)
    MATH       = "math"         # 數學計算    → P06數學大師
    PERMISSION = "permission"   # 權限分配    → P13姜子牙
    UNKNOWN    = "unknown"      # 不確定      → P02先接住


class AuditColor(Enum):
    """三色審計"""
    GREEN = "🟢"   # 通過
    YELLOW = "🟡"  # 警告
    RED = "🔴"     # 熔斷


# 觸發詞表（P0永恆級·不可刪）
SCENE_KEYWORDS = {
    IntentType.EMOTION:    ["不搞了", "算了", "心累", "煩", "宝宝", "冷冰冰"],
    IntentType.STRATEGY:   ["怎麼做", "下一步", "方向", "推演", "值不值", "要不要"],
    IntentType.AUDIT:      ["整理", "格式", "審計", "對不對", "檢查", "雯雯"],
    IntentType.TECH:       ["代碼", "報錯", "能跑嗎", "魯班", "實現", "debug"],
    IntentType.RISK:       ["坑", "陷阱", "風險", "安全嗎", "靠譜嗎", "有問題嗎"],
    IntentType.MATH:       ["權重", "算法", "公式", "計算", "數學", "歸一化"],
    IntentType.PERMISSION: ["姜子牙", "分配", "權限", "封神"],
}

# 人格映射：(人格名, 數學核心, 優先級)
PERSONA_MAP = {
    IntentType.EMOTION:    ("P02·宝宝",     ["概率論"],            3),
    IntentType.STRATEGY:   ("P01·諸葛亮",   ["優化論", "概率論"],   1),
    IntentType.AUDIT:      ("P03·雯雯",     ["信息論"],            2),
    IntentType.TECH:       ("P04·魯班",     ["線性代數", "優化論"], 2),
    IntentType.RISK:       ("P05·上帝之眼", ["概率論", "信息論"],   0),
    IntentType.MATH:       ("P06·數學大師", ["線性代數", "優化論"], 2),
    IntentType.PERMISSION: ("P13·姜子牙",   ["信息論"],            1),
    IntentType.UNKNOWN:    ("P02·宝宝",     ["概率論"],            3),
}

VALID_DNA = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
P0_TRIGGERS = ["坑", "陷阱", "風險", "安全嗎", "靠譜嗎", "有問題嗎"]


# ════════════════════════════════════════════════════════════════
# 第二部分：路由結果數據結構
# ════════════════════════════════════════════════════════════════

@dataclass
class RouteResult:
    """v1.0 路由結果"""
    intent:     IntentType
    persona:    str
    math_core:  List[str]
    priority:   int       # 0=P0最高 → 3=普通
    dna_valid:  bool
    confidence: float
    reason:     str
    timestamp:  str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VectorRouteResult:
    """v1.1 向量路由結果"""
    intent: IntentType
    score: float
    anchor: str


@dataclass
class ParallelRouteResult:
    """v1.2 多人格並行結果"""
    primary_intent: IntentType
    secondary_intent: IntentType
    primary_persona: str
    secondary_persona: str
    reason: str


@dataclass
class AuditResult:
    """v2.0 三色審計結果"""
    color: AuditColor
    reasons: List[str]
    requires_confirm_dna: bool


# ════════════════════════════════════════════════════════════════
# 第三部分：v1.0 關鍵詞路由器
# ════════════════════════════════════════════════════════════════

class CNSHRouterV10:
    """CNSH 路由器 v1.0 - 關鍵詞 + DNA 校驗 + L1 快車道"""

    def __init__(self):
        self.session_history = []
        self.route_cache = {}

    def route(self, text: str, dna: str = "") -> RouteResult:
        """核心路由函數：Route = f(Intent, Context, DNA)"""

        dna_valid = (dna.strip() == VALID_DNA)

        # L1 快車道
        cache_key = hashlib.md5(text.encode()).hexdigest()[:8]
        if cache_key in self.route_cache:
            r = self.route_cache[cache_key]
            r.reason = f"[快車道] {r.reason}"
            return r

        # 意圖解析 (Scoring 機制)
        scores = {}
        for itype, kws in SCENE_KEYWORDS.items():
            s = sum(1 for kw in kws if kw in text)
            if s > 0:
                scores[itype] = s

        if scores:
            intent = max(scores, key=scores.get)
            conf = min(1.0, scores[intent] / 3.0 + 0.4)
        else:
            intent, conf = IntentType.UNKNOWN, 0.5

        persona, math_cores, priority = PERSONA_MAP[intent]

        result = RouteResult(
            intent=intent,
            persona=persona,
            math_core=list(math_cores),
            priority=priority,
            dna_valid=dna_valid,
            confidence=conf,
            reason=self._reason(intent, conf)
        )

        self.route_cache[cache_key] = result
        self.session_history.append({"text": text, "route": intent.value, "timestamp": datetime.now().isoformat()})
        return result

    def _reason(self, intent: IntentType, conf: float) -> str:
        labels = {
            IntentType.EMOTION:    "偵測到情緒信號·P02宝宝先接住",
            IntentType.STRATEGY:   "需要多路徑推演·諸葛亮出馬",
            IntentType.AUDIT:      "結構整理需求·雯雯質檢",
            IntentType.TECH:       "技術執行任務·魯班落地",
            IntentType.RISK:       "🔴風險信號·上帝之眼三色掃描",
            IntentType.MATH:       "數學計算需求·大師歸一化",
            IntentType.PERMISSION: "權限分配任務·姜子牙守門",
            IntentType.UNKNOWN:    "意圖不明·宝宝先接住再確認",
        }
        return f"{labels[intent]} (置信度:{conf:.0%})"

    def explain(self, r: RouteResult) -> str:
        p_labels = ["🔴 P0緊急","🟠 P1高","🟡 P2中","🟢 P3普通"]
        p = p_labels[min(r.priority, 3)]
        dna = "✅ DNA已驗證" if r.dna_valid else "⚠️ 訪客模式"
        return (
            f"路由 → {r.persona}\n"
            f"數學核心：{' + '.join(r.math_core)}\n"
            f"優先級：{p} | {dna}\n"
            f"理由：{r.reason}"
        )


# ════════════════════════════════════════════════════════════════
# 第四部分：v1.1 向量嵌入路由器（簡化版）
# ════════════════════════════════════════════════════════════════

class SimpleEmbedder:
    """占位 Embedder：用 hash trick 保證可執行"""
    def embed(self, text: str) -> List[float]:
        v = [0.0] * 64
        for ch in text:
            v[ord(ch) % 64] += 1.0
        norm = math.sqrt(sum(x*x for x in v)) or 1.0
        return [x / norm for x in v]


def cosine_sim(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0


class CNSHRouterV11:
    """CNSH 路由器 v1.1 - 向量相似度路由"""

    INTENT_ANCHORS: Dict[IntentType, List[str]] = {
        IntentType.RISK: [
            "這句話在問有沒有坑或風險",
            "需要安全性與風險評估"
        ],
        IntentType.STRATEGY: [
            "這句話在問下一步怎麼做",
            "需要推演方向與決策"
        ],
        IntentType.TECH: [
            "這句話在問代碼實現或報錯",
            "需要工程落地與調試"
        ],
        IntentType.AUDIT: [
            "這句話在要整理格式或審計檢查",
            "需要結構化與校對"
        ],
        IntentType.MATH: [
            "這句話在問公式權重算法怎麼計算",
            "需要數學推導與歸一化"
        ],
        IntentType.EMOTION: [
            "這句話在表達情緒或需要安撫",
            "需要先接住再確認"
        ],
    }

    def __init__(self):
        self.embedder = SimpleEmbedder()
        self._anchor_vectors = []
        for itype, anchors in self.INTENT_ANCHORS.items():
            for a in anchors:
                self._anchor_vectors.append((itype, a, self.embedder.embed(a)))

    def route(self, text: str) -> VectorRouteResult:
        v = self.embedder.embed(text)
        best_intent, best_anchor, best_score = IntentType.UNKNOWN, "", 0.0
        for itype, anchor, av in self._anchor_vectors:
            s = cosine_sim(v, av)
            if s > best_score:
                best_intent, best_anchor, best_score = itype, anchor, s

        if best_score < 0.30:
            return VectorRouteResult(IntentType.UNKNOWN, best_score, best_anchor)
        return VectorRouteResult(best_intent, best_score, best_anchor)


# ════════════════════════════════════════════════════════════════
# 第五部分：v1.2 多人格並行路由
# ════════════════════════════════════════════════════════════════

class CNSHRouterV12:
    """CNSH 路由器 v1.2 - 多人格並行"""

    def __init__(self, vector_router: CNSHRouterV11):
        self.vr = vector_router

    def route_dual(self, text: str) -> ParallelRouteResult:
        """返回主+協作兩個人格"""
        r1 = self.vr.route(text)
        primary = r1.intent

        # 協作補位規則
        if primary == IntentType.STRATEGY:
            secondary, reason = IntentType.TECH, "主為推演，協作為落地"
        elif primary == IntentType.TECH:
            secondary, reason = IntentType.AUDIT, "主為落地，協作為質檢"
        elif primary == IntentType.RISK:
            secondary, reason = IntentType.AUDIT, "主為風險，協作為審計整理"
        elif primary == IntentType.MATH:
            secondary, reason = IntentType.STRATEGY, "主為計算，協作為決策推演"
        else:
            secondary, reason = IntentType.STRATEGY, "默認補位為推演協作"

        return ParallelRouteResult(
            primary_intent=primary,
            secondary_intent=secondary,
            primary_persona=PERSONA_MAP.get(primary, ("P02·宝宝", [], 3))[0],
            secondary_persona=PERSONA_MAP.get(secondary, ("P02·宝宝", [], 3))[0],
            reason=reason,
        )


# ════════════════════════════════════════════════════════════════
# 第六部分：v2.0 天道三色審計門
# ════════════════════════════════════════════════════════════════

class TiandaoAuditGateV20:
    """CNSH 路由器 v2.0 - 三色審計接入（P0 風險自動升級）"""

    def audit(self, text: str, dna_valid: bool) -> AuditResult:
        reasons = []

        # P0 直達
        hit_p0 = any(t in text for t in P0_TRIGGERS)
        if hit_p0:
            reasons.append("命中 P0 風險觸發詞")

        # DNA 驗證
        if not dna_valid:
            reasons.append("DNA 未驗證：僅允許訪客模式輸出")

        # 三色判定
        if hit_p0 and not dna_valid:
            return AuditResult(AuditColor.RED, reasons + ["P0 風險 + 未驗證 DNA，觸發熔斷"], True)
        if hit_p0 and dna_valid:
            return AuditResult(AuditColor.YELLOW, reasons + ["P0 風險：允許繼續，但必須先給出風險清單與緩解方案"], False)

        return AuditResult(AuditColor.GREEN, ["未命中風險升級條件"], False)


# ════════════════════════════════════════════════════════════════
# 第七部分：完整的 CNSH Runtime 整合器
# ════════════════════════════════════════════════════════════════

@dataclass
class CNSHContext:
    """龍魂執行上下文"""
    user_id: str = "UID9622"
    dna: str = VALID_DNA
    session_id: str = field(default_factory=lambda: hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:8])
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    messages: List[Dict] = field(default_factory=list)


class CNSHRuntime:
    """龍魂完整執行時 = 路由 v1.0-v2.0 + 三色審計 + 多人格並行"""

    def __init__(self):
        self.router_v10 = CNSHRouterV10()
        self.router_v11 = CNSHRouterV11()
        self.router_v12 = CNSHRouterV12(self.router_v11)
        self.audit_gate = TiandaoAuditGateV20()
        self.context = CNSHContext()
        self.dna_chain = []

    def execute(self, text: str, dna: str = VALID_DNA) -> Dict:
        """執行完整路由+審計流程"""

        # 第一步：v1.0 基礎路由
        route_v10 = self.router_v10.route(text, dna)

        # 第二步：三色審計（v2.0）
        audit = self.audit_gate.audit(text, dna_valid=(dna == VALID_DNA))

        # 第三步：多人格併行（v1.2）
        if audit.color != AuditColor.RED:
            route_v12 = self.router_v12.route_dual(text)
        else:
            route_v12 = None

        # DNA 追溯
        execution_dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EXECUTE-{route_v10.intent.value}"
        dna_entry = {
            "timestamp": datetime.now().isoformat(),
            "dna": execution_dna,
            "input": text,
            "route": route_v10.intent.value,
            "audit_color": audit.color.value,
            "personas": [route_v10.persona] + ([route_v12.secondary_persona] if route_v12 else []),
        }
        self.dna_chain.append(dna_entry)

        # 最終輸出
        return {
            "success": audit.color != AuditColor.RED,
            "input": text,
            "route_v10": {
                "persona": route_v10.persona,
                "intent": route_v10.intent.value,
                "confidence": route_v10.confidence,
                "priority": route_v10.priority,
                "math_core": route_v10.math_core,
            },
            "parallel": {
                "primary": route_v12.primary_persona if route_v12 else None,
                "secondary": route_v12.secondary_persona if route_v12 else None,
                "reason": route_v12.reason if route_v12 else None,
            } if route_v12 else None,
            "audit": {
                "color": audit.color.value,
                "reasons": audit.reasons,
            },
            "dna": execution_dna,
        }


# ════════════════════════════════════════════════════════════════
# 測試 & 演示
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    runtime = CNSHRuntime()

    test_cases = [
        "下一步怎麼做系統",
        "這裡有個坑要注意",
        "宝宝我有點累了",
        "幫我整理一下格式",
        "這個算法的權重怎麼算",
    ]

    print("🐉 龍魂 CNSH Runtime v1.0 - 路由執行演示\n")
    print("="*60)

    for text in test_cases:
        result = runtime.execute(text, dna=VALID_DNA)
        print(f"\n📝 輸入: {text}")
        print(f"🎯 主人格: {result['route_v10']['persona']}")
        if result['parallel']:
            print(f"🤝 協作: {result['parallel']['primary']} + {result['parallel']['secondary']}")
        print(f"🔍 審計: {result['audit']['color']} {' '.join(result['audit']['reasons'][:1])}")
        print(f"📊 置信度: {result['route_v10']['confidence']:.0%}")
        print("-" * 60)

    print("\n✅ CNSH Runtime 演示完成")
    print(f"   DNA 鏈長: {len(runtime.dna_chain)} 條追溯")
    print(f"   會話 ID: {runtime.context.session_id}")
