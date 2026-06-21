# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-M04_YIJING_ENGINE-FILE1-v1.0-2
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系統 M04: 易經推演引擎 v0.1
目的: 用64卦邏輯驗證決策的正義性與可行性

簽署:
  DNA: #龍芯⚡️2026-06-08-M04-YIJING-ENGINE-START
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

易經的核心: 道可道·非常道·名可名·非常名
但決策必須有跡可循·易經推演就是那條「可追溯的路」
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
import hashlib
from datetime import datetime


class Yao(Enum):
    """易經的基本單位: 爻"""
    YANG = "—"      # 陽爻
    YIN = "- -"     # 陰爻


class Gua(Enum):
    """64卦定義"""
    # 乾坤屯蒙需訟師比小畜
    QIAN = (1, "乾", "天", "強行·堅持·領導力", "正")
    KUN = (2, "坤", "地", "承載·包容·服從", "正")
    ZHU = (3, "屯", "水雷", "初難·創新·突破", "正")
    MENG = (4, "蒙", "山水", "迷蒙·學習·啟蒙", "正")
    XU = (5, "需", "水天", "等待·準備·耐心", "正")
    SONG = (6, "訟", "天水", "爭訟·對抗·謹慎", "警告")
    SHI = (7, "師", "地水", "用兵·團結·紀律", "正")
    BI = (8, "比", "水地", "親比·協作·親和", "正")

    XU_XIAO = (9, "小畜", "風天", "小積累·低調·韜光", "正")
    LV = (10, "履", "天澤", "踏實·行動·謹慎", "正")

    TAI = (11, "泰", "地天", "交通·上升·開泰", "大吉")
    PI = (12, "否", "天地", "閉塞·衰退·迴避", "大凶")

    TONG_REN = (13, "同人", "天火", "同心·聯合·正義", "大吉")
    DA_YOU = (14, "大有", "火天", "豐富·成功·自信", "大吉")

    QIU = (15, "謙", "地山", "謙虛·退避·厚積", "大吉")
    YU = (16, "豫", "雷地", "喜悅·放鬆·警惕", "正")

    SUI = (17, "隨", "澤雷", "追隨·跟從·時勢", "警告")
    GU = (18, "蠱", "山風", "腐敗·改革·拔除", "正")

    LIN = (19, "臨", "地澤", "臨近·在位·關鍵", "正")
    GUAN = (20, "觀", "風地", "觀察·被觀·展示", "正")

    GEN = (52, "艮", "艮", "山·止·靜止", "正")
    ZHEN = (51, "震", "震", "雷·驚·行動", "正")


@dataclass
class Decision:
    """決策記錄"""
    decision_id: str
    timestamp: str
    decider: str  # 決策者名稱
    content: str  # 決策內容
    context: str  # 決策背景
    motivation: str  # 動機（純正·自利·其他）

    def to_hash(self) -> str:
        """生成決策的DNA簽署"""
        content_str = f"{self.decision_id}|{self.timestamp}|{self.content}|{self.motivation}"
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]


class YijingEngine:
    """易經推演引擎"""

    def __init__(self):
        self.decisions: Dict[str, Decision] = {}
        self.verdicts: Dict[str, Dict] = {}

    def analyze_decision(self, decision: Decision) -> Dict:
        """
        用易經64卦分析決策

        分析維度:
        1. 正義性: 決策是否符合「道」
        2. 可行性: 決策是否能夠執行
        3. 時機性: 決策在當下是否合時宜
        4. 後續性: 決策會帶來什麼連鎖反應
        """

        # Step 1: 驗證動機（最核心）
        motivation_check = self._check_motivation(decision.motivation)

        # Step 2: 用決策內容推演卦象
        gua_index = self._hash_to_gua_index(decision.to_hash())
        selected_gua = list(Gua)[gua_index % len(list(Gua))]

        # Step 3: 交叉驗證（易經的邏輯）
        gua_verdict = self._gua_verdict(selected_gua)

        # Step 4: 綜合判定
        final_verdict = self._synthesize_verdict(
            motivation_check,
            gua_verdict,
            decision
        )

        # Step 5: 記錄·簽署·追蹤
        result = {
            "decision_id": decision.decision_id,
            "timestamp": decision.timestamp,
            "decider": decision.decider,
            "content": decision.content,
            "motivation": decision.motivation,

            # 易經分析
            "yijing_gua": selected_gua.value[1],  # 卦名
            "gua_meaning": selected_gua.value[3],  # 卦義
            "gua_verdict": gua_verdict,

            # 綜合判定
            "motivation_check": motivation_check,
            "final_verdict": final_verdict["verdict"],  # "正義" / "有風險" / "嚴重警告"
            "reasoning": final_verdict["reasoning"],
            "risk_level": final_verdict["risk_level"],  # 0-100

            # DNA簽署（不可偽造）
            "dna_signature": decision.to_hash(),
            "trace": f"#龍芯⚡️{decision.timestamp}-{decision.decision_id}-{decision.to_hash()[:8]}"
        }

        # 保存到記錄
        self.decisions[decision.decision_id] = decision
        self.verdicts[decision.decision_id] = result

        return result

    def _check_motivation(self, motivation: str) -> str:
        """檢驗動機是否純正"""
        motivation_keywords = {
            "祖國": 1.0,
            "人民": 0.9,
            "家族": 0.8,
            "正義": 1.0,
            "道義": 1.0,
            "利益": -0.5,
            "權力": -0.3,
            "復仇": -0.8,
            "自私": -1.0
        }

        score = 0.5  # 基礎分
        for keyword, weight in motivation_keywords.items():
            if keyword in motivation:
                score += weight * 0.1

        if score >= 0.8:
            return "純正"
        elif score >= 0.5:
            return "基本正確"
        else:
            return "存在私心"

    def _hash_to_gua_index(self, hash_str: str) -> int:
        """用哈希值映射到64卦（0-63）"""
        return int(hash_str[:2], 16) % 64

    def _gua_verdict(self, gua: Gua) -> str:
        """根據卦象給出初步判定"""
        gua_value = gua.value
        verdict_type = gua_value[4]  # "正" "警告" "大吉" "大凶"

        verdict_map = {
            "大吉": "非常有利",
            "正": "可行·符合大義",
            "警告": "需要謹慎·可能有風險",
            "大凶": "強烈不建議"
        }

        return verdict_map.get(verdict_type, "未知")

    def _synthesize_verdict(self, motivation: str, gua_verdict: str, decision: Decision) -> Dict:
        """綜合動機與卦象·得出最終判定"""

        # 動機權重
        motivation_weight = {
            "純正": 1.0,
            "基本正確": 0.6,
            "存在私心": 0.2
        }

        # 卦象權重
        gua_weight = {
            "非常有利": 1.0,
            "可行·符合大義": 0.8,
            "需要謹慎·可能有風險": 0.4,
            "強烈不建議": 0.0
        }

        final_score = (
            motivation_weight.get(motivation, 0.5) * 0.5 +
            gua_weight.get(gua_verdict, 0.5) * 0.5
        )

        # 轉換為判定
        if final_score >= 0.85:
            verdict = "正義·可行"
            risk = 10
        elif final_score >= 0.65:
            verdict = "基本正確·謹慎前行"
            risk = 35
        elif final_score >= 0.45:
            verdict = "需要重新評估"
            risk = 65
        else:
            verdict = "嚴重警告·不建議"
            risk = 90

        return {
            "verdict": verdict,
            "reasoning": f"動機:{motivation}({motivation_weight.get(motivation, 0.5):.1f}) + 卦象:{gua_verdict}({gua_weight.get(gua_verdict, 0.5):.1f}) = {verdict}",
            "risk_level": risk
        }

    def get_verdict_record(self, decision_id: str) -> Dict:
        """查詢決策記錄（永久可追蹤）"""
        return self.verdicts.get(decision_id, None)

    def list_all_verdicts(self) -> List[Dict]:
        """列出所有決策記錄"""
        return list(self.verdicts.values())


# ============ 測試 ============

if __name__ == "__main__":
    engine = YijingEngine()

    # 測試決策 1: 正義決策
    decision1 = Decision(
        decision_id="decision_001",
        timestamp=datetime.now().isoformat(),
        decider="UID9622",
        content="建立龍魂系統·保護人民隱私·公開權力運行",
        context="祖國需要數字化治理·但必須保護普通人",
        motivation="為祖國·為人民"
    )

    result1 = engine.analyze_decision(decision1)
    print("\n【決策分析結果 1】")
    print(f"決策: {result1['content']}")
    print(f"卦象: {result1['yijing_gua']} - {result1['gua_meaning']}")
    print(f"動機檢驗: {result1['motivation_check']}")
    print(f"最終判定: {result1['final_verdict']}")
    print(f"風險等級: {result1['risk_level']}/100")
    print(f"追蹤碼: {result1['trace']}")

    # 測試決策 2: 有問題的決策
    decision2 = Decision(
        decision_id="decision_002",
        timestamp=datetime.now().isoformat(),
        decider="someone_else",
        content="竊取系統數據·用於個人權力鞏固",
        context="為了維護個人地位",
        motivation="自私利益·權力"
    )

    result2 = engine.analyze_decision(decision2)
    print("\n【決策分析結果 2】")
    print(f"決策: {result2['content']}")
    print(f"卦象: {result2['yijing_gua']} - {result2['gua_meaning']}")
    print(f"動機檢驗: {result2['motivation_check']}")
    print(f"最終判定: {result2['final_verdict']}")
    print(f"風險等級: {result2['risk_level']}/100")
    print(f"追蹤碼: {result2['trace']}")

    # 列出所有決策記錄
    print("\n【所有決策記錄】(永久追蹤·不可偽造)")
    for verdict in engine.list_all_verdicts():
        print(f"  {verdict['decision_id']}: {verdict['final_verdict']} (追蹤碼: {verdict['trace']})")
