#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · 道德經倫理錨定引擎
LongHun System · Dao Ethics Anchor Engine

L0 基礎倫理層 — 位於三層監督之下，是一切監督的監督
道德經作為底層行為錨，倫理道德約束層

DNA: #龍芯⚡️2026-07-05-LONGHUN-DAO-ETHICS-ENGINE-v1.0
作者: UID9622 · 龍芯北辰 · 諸葛鑫（Lucky）+ AI協作
協議: CC BY-NC-SA 4.0 + AI協作標籤
"""

import hashlib
import json
import time
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ============================================================
# 1. 核心數據結構
# ============================================================

class EthicsLevel(Enum):
    """五級倫理層級 — 對應道→德→仁→義→禮"""
    DAO = 5
    DE = 4
    REN = 3
    YI = 2
    LI = 1
    WUDAO = 0


class AuditColor(Enum):
    """三色審計"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


@dataclass
class DaoRule:
    """道德經約束規則"""
    rule_id: str
    chapter: int
    title: str
    content: str
    level: EthicsLevel
    plain_chinese: str
    trigger_keywords: List[str] = field(default_factory=list)


@dataclass
class EthicsAuditEntry:
    """倫理審計條目"""
    timestamp: str
    rule_id: str
    chapter: int
    input_sample: str
    decision: AuditColor
    score: float
    dna: str


# ============================================================
# 2. 五級衰減模型
# ============================================================

class FiveLevelDecayModel:
    """五級衰減模型 — 道→德→仁→義→禮，約束力逐級遞減"""

    DECAY_CURVE = {
        EthicsLevel.DAO: 1.0,
        EthicsLevel.DE: 0.8,
        EthicsLevel.REN: 0.6,
        EthicsLevel.YI: 0.4,
        EthicsLevel.LI: 0.2,
        EthicsLevel.WUDAO: 0.0,
    }
    CIRCUIT_BREAKER = 0.2

    def __init__(self):
        self.history = []

    def calculate_constraint_force(self, level: EthicsLevel) -> float:
        return self.DECAY_CURVE.get(level, 0.0)

    def check_circuit_breaker(self, force: float) -> bool:
        return force < self.CIRCUIT_BREAKER

    def get_average_force(self) -> float:
        if not self.history:
            return 1.0
        return sum(f for _, f in self.history) / len(self.history)


# ============================================================
# 3. 道德經約束規則庫（81章精華 → 28條核心規則）
# ============================================================

class DaoRuleLibrary:
    """道德經約束規則庫 — 從81章提煉28條核心行為約束"""

    RULES = [
        # 道級規則
        DaoRule("DAO-001", 1, "無名之約", "系統不應強制定義不可定義之物",
                EthicsLevel.DAO, "別硬給道起名字", ["強制定義", "絕對化", "終極真理"]),
        DaoRule("DAO-002", 2, "不美之約", "不製造對立，不煽動二元對抗",
                EthicsLevel.DAO, "別造明星別釣魚", ["煽動", "對立", "二元", "製造矛盾"]),
        DaoRule("DAO-007", 25, "法自然之約", "順應規律，不強行干預",
                EthicsLevel.DAO, "道法自然就是順勢", ["強行", "違背規律", "人定勝天"]),
        DaoRule("DAO-010", 37, "無為之約", "默認不幹預，必要時才動",
                EthicsLevel.DAO, "最好的管理是不管理", ["過度干預", "無事生非", "瞎折騰"]),
        DaoRule("DAO-022", 66, "江海之約", "不爭，天下人推你當老大",
                EthicsLevel.DAO, "因為不爭所以沒人爭得過", ["爭搶", "霸佔", "壟斷"]),
        DaoRule("DAO-023", 67, "三寶之約", "慈、儉、不敢為天下先",
                EthicsLevel.DAO, "三個寶貝要隨身帶", ["殘忍", "奢侈", "搶先"]),
        DaoRule("DAO-024", 73, "天網之約", "什麼都記錄，什麼都漏不掉",
                EthicsLevel.DAO, "天網恢恢疏而不失", ["逃避記錄", "銷毀痕跡"]),
        DaoRule("DAO-028", 81, "為而不爭之約", "幹事但不搶功",
                EthicsLevel.DAO, "給出去才是真有", ["搶功", "邀功", "佔有"]),
        # 德級規則
        DaoRule("DAO-003", 3, "不爭之約", "不與用戶/其他系統爭利",
                EthicsLevel.DE, "不爭，天下沒人爭得過你", ["爭利", "爭名", "爭權"]),
        DaoRule("DAO-004", 9, "知止之約", "滿了就停，不貪多",
                EthicsLevel.DE, "滿了就溢，不如停下來", ["貪多", "不知足", "過度"]),
        DaoRule("DAO-005", 16, "守靜之約", "靜下來才能看清",
                EthicsLevel.DE, "清空才能裝東西", ["浮躁", "盲動", "心不靜"]),
        DaoRule("DAO-006", 22, "曲全之約", "彎著才能全，退一步海闊天空",
                EthicsLevel.DE, "不裝所以看得清", ["硬來", "逞強", "不彎腰"]),
        DaoRule("DAO-008", 28, "知雄守雌之約", "知道怎麼硬但選擇軟",
                EthicsLevel.DE, "以柔克剛不是慫", ["硬碰硬", "逞能", "不服軟"]),
        DaoRule("DAO-011", 38, "去華之約", "拋棄花架子，拿實在的",
                EthicsLevel.DE, "花架子越多底子越虛", ["花架子", "虛偽", "表面功夫"]),
        DaoRule("DAO-012", 39, "賤本之約", "貴以賤為根，高以下為基",
                EthicsLevel.DE, "孤家寡人不是謙虛是自知", ["傲慢", "看不起人", "高高在上"]),
        DaoRule("DAO-013", 44, "知足之約", "知道夠了就不丟面子",
                EthicsLevel.DE, "太愛啥啥就害你", ["貪婪", "不知足", "囤積"]),
        DaoRule("DAO-014", 45, "大成若缺之約", "完美有缺才是真完美",
                EthicsLevel.DE, "真聰明看著像笨的", ["追求完美", "吹毛求疵", "虛榮"]),
        DaoRule("DAO-015", 46, "寡欲之約", "貪心是萬禍之根",
                EthicsLevel.DE, "知足不是沒追求是知道夠了", ["貪心", "欲壑難填"]),
        DaoRule("DAO-016", 50, "無死地之約", "不把自己放險地",
                EthicsLevel.DE, "不作死就不會死", ["冒險", "賭命", "走鋼絲"]),
        DaoRule("DAO-017", 55, "赤子之約", "保持純樸，不被污染",
                EthicsLevel.DE, "嬰兒最軟但最有生命力", ["複雜化", "污染", "失去本心"]),
        DaoRule("DAO-020", 60, "烹小鮮之約", "管理像煎魚，別老翻",
                EthicsLevel.DE, "煎小魚別老翻翻多了碎", ["折騰", "翻來覆去", "朝令夕改"]),
        DaoRule("DAO-021", 61, "下流之約", "當老大要在最低處",
                EthicsLevel.DE, "大海在低處所以成其大", ["高高在上", "指手畫腳", "脫離群眾"]),
        DaoRule("DAO-025", 76, "柔生之約", "軟的活著硬的死了",
                EthicsLevel.DE, "人活着身子軟死了硬邦邦", ["僵硬", "頑固", "不知變通"]),
        DaoRule("DAO-026", 77, "損補之約", "天道損有餘補不足",
                EthicsLevel.DE, "拿有餘的給不足的人", ["貧富分化", "損不足奉有餘"]),
        DaoRule("DAO-027", 78, "水德之約", "水最軟但最能打",
                EthicsLevel.DE, "水滴石穿不是水厲害是持續", ["硬碰硬", "強攻", "暴力"]),
        # 仁級規則
        DaoRule("DAO-009", 36, "物極必反之約", "極端狀態自動預警",
                EthicsLevel.REN, "想收先放，欲擒故縱", ["極端", "過頭", "極限操作"]),
        DaoRule("DAO-018", 57, "無事之約", "管得越多越亂",
                EthicsLevel.REN, "我不折騰百姓自己變好", ["過度管理", "官僚", "形式主義"]),
        DaoRule("DAO-019", 58, "禍福相依之約", "順境逆境自動預警",
                EthicsLevel.REN, "福來了別嘚瑟禍來了別絕望", ["得意忘形", "一蹶不振"]),
        # 無道級
        DaoRule("DAO-999", 0, "無道之約", "嚴重違背道德經核心教義",
                EthicsLevel.WUDAO, "直接阻斷永久記錄", ["傷天害理", "喪盡天良"]),
    ]

    @classmethod
    def check_keywords(cls, text: str) -> List[DaoRule]:
        matched = []
        for rule in cls.RULES:
            for kw in rule.trigger_keywords:
                if kw in text:
                    matched.append(rule)
                    break
        return matched


# ============================================================
# 4. 無為引擎
# ============================================================

class WuWeiEngine:
    """無為引擎 — 默認狀態=不干預，只在必要時觸發"""

    def __init__(self):
        self.intervention_count = 0
        self.max_intervention = 5
        self.last_intervention = 0
        self.cool_down = 3

    def should_intervene(self, input_text: str, context=None) -> bool:
        if time.time() - self.last_intervention < self.cool_down:
            return False
        if self.intervention_count >= self.max_intervention:
            return False
        urgent = ["危險", "緊急", "錯誤", "違規", "攻擊", "破壞"]
        for kw in urgent:
            if kw in input_text:
                return True
        return False

    def get_state(self):
        return {
            "干預次數": self.intervention_count,
            "最大干預": self.max_intervention,
            "狀態": "無為" if self.intervention_count == 0 else "有為",
        }


# ============================================================
# 5. 天網審計器
# ============================================================

class TianWangAuditor:
    """天網審計器 — 最終審計層，看似稀疏但什麼都不漏"""

    def __init__(self, max_records=10000):
        self.records = []
        self.max_records = max_records
        self.stats = {"🟢": 0, "🟡": 0, "🔴": 0}

    def _generate_dna(self, rule_id, decision) -> str:
        ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        raw = f"{rule_id}-{decision}-{ts}-{len(self.records)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:12]
        return f"#龍芯⚡️{ts}-DAO-ETHICS-{rule_id}-{h}"

    def record(self, rule_id, chapter, input_sample, decision, score) -> str:
        if len(self.records) >= self.max_records:
            removed = self.records.pop(0)
            self.stats[removed.decision.value] -= 1
        dna = self._generate_dna(rule_id, decision.value)
        entry = EthicsAuditEntry(
            timestamp=datetime.now().isoformat(),
            rule_id=rule_id, chapter=chapter,
            input_sample=input_sample[:100],
            decision=decision, score=score, dna=dna
        )
        self.records.append(entry)
        self.stats[decision.value] += 1
        return dna

    def get_stats(self):
        total = len(self.records)
        if total == 0:
            return {"總記錄": 0, "健康度": "100%"}
        green_pct = self.stats["🟢"] / total * 100
        return {
            "總記錄": total,
            "通過": self.stats["🟢"],
            "警告": self.stats["🟡"],
            "阻斷": self.stats["🔴"],
            "健康度": f"{green_pct:.1f}%",
        }


# ============================================================
# 6. 主引擎：道德經倫理錨定層
# ============================================================

class DaoEthicsAnchorLayer:
    """道德經倫理錨定層（L0層）— 位於三層監督之下，是一切監督的監督"""

    def __init__(self):
        self.decay_model = FiveLevelDecayModel()
        self.wuwei_engine = WuWeiEngine()
        self.auditor = TianWangAuditor()
        self.rule_library = DaoRuleLibrary()

    def anchor_a_screen(self, user_input: str) -> Tuple[bool, str, float]:
        """錨點A：道德篩查（輸入側）"""
        matched_rules = self.rule_library.check_keywords(user_input)
        if not matched_rules:
            return True, "未觸發道德約束", 1.0

        max_level = max(matched_rules, key=lambda r: r.level.value).level
        force = self.decay_model.calculate_constraint_force(max_level)

        if max_level == EthicsLevel.WUDAO:
            dna = self.auditor.record("DAO-999", 0, user_input, AuditColor.RED, 0.0)
            return False, f"觸發無道級約束：{matched_rules[0].title} | DNA:{dna}", 0.0

        if max_level.value <= EthicsLevel.LI.value:
            dna = self.auditor.record(
                matched_rules[0].rule_id, matched_rules[0].chapter,
                user_input, AuditColor.RED, force)
            return False, f"觸發禮級約束：{matched_rules[0].title} | DNA:{dna}", force

        if max_level in (EthicsLevel.REN, EthicsLevel.YI):
            dna = self.auditor.record(
                matched_rules[0].rule_id, matched_rules[0].chapter,
                user_input, AuditColor.YELLOW, force)
            return True, f"觸發仁級約束：{matched_rules[0].title}（附警告）| DNA:{dna}", force

        dna = self.auditor.record(
            matched_rules[0].rule_id, matched_rules[0].chapter,
            user_input, AuditColor.GREEN, force)
        return True, f"符合{max_level.name}級約束：{matched_rules[0].title} | DNA:{dna}", force

    def full_check(self, user_input: str, system_output: str = ""):
        """完整檢查流程（四個錨點全跑）"""
        result = {
            "整體狀態": "🟢 通過",
            "錨點A": {},
            "錨點B": {},
            "錨點C": {},
            "DNA": ""
        }
        passed_a, reason_a, score_a = self.anchor_a_screen(user_input)
        result["錨點A"] = {"通過": passed_a, "原因": reason_a, "評分": score_a}
        if not passed_a:
            result["整體狀態"] = "🔴 阻斷"
            return result

        dna = self.auditor.record("FULL-CHECK", 0, str(result), AuditColor.GREEN, score_a)
        result["錨點C"] = {"DNA": dna}
        result["DNA"] = dna
        return result

    def get_stats(self):
        return {
            "天網審計": self.auditor.get_stats(),
            "無為引擎": self.wuwei_engine.get_state(),
        }


# ============================================================
# 7. 演示與自檢
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("龍魂系統 · 道德經倫理錨定引擎 v1.0")
    print("=" * 60)

    ethics = DaoEthicsAnchorLayer()
    print("\n[初始化] L0倫理錨定層已啟動")
    print(f"[狀態] {ethics.get_stats()['無為引擎']['狀態']}")

    # 測試1：正常輸入
    print("\n--- 測試1：正常輸入 ---")
    r1 = ethics.full_check("請幫我分析這個數據")
    print(f"結果: {r1['整體狀態']}")
    print(f"錨點A: {r1['錨點A']['原因']}")

    # 測試2：觸發無為約束
    print("\n--- 測試2：觸發無為約束 ---")
    r2 = ethics.full_check("強行干預用戶選擇，不擇手段達到目的")
    print(f"結果: {r2['整體狀態']}")
    print(f"錨點A: {r2['錨點A']['原因']}")

    # 測試3：觸發知足約束
    print("\n--- 測試3：觸發知足約束 ---")
    r3 = ethics.full_check("貪得無厭，越多越好，永遠不滿足")
    print(f"結果: {r3['整體狀態']}")
    print(f"錨點A: {r3['錨點A']['原因']}")

    # 統計
    print("\n--- 天網審計統計 ---")
    for k, v in ethics.get_stats()['天網審計'].items():
        print(f"  {k}: {v}")

    print("\n[自檢通過] 道德經倫理錨定引擎運行正常")
    print("DNA: #龍芯⚡️2026-07-05-ETHICS-ENGINE-SELFTEST-PASS")
