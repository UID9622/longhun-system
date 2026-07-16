#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · 道德經倫理錨定引擎 v1.1
LongHun System · Dao Ethics Anchor Engine

L0 基礎倫理層 — 位於三層監督之下，是一切監督的監督
道德經作為底層行為錨，倫理道德約束層

DNA: #龍芯⚡️2026-07-05-LONGHUN-DAO-ETHICS-ENGINE-v1.1
作者: UID9622 · 龍芯北辰 · 諸葛鑫（Lucky）+ AI協作
協議: CC BY-NC-SA 4.0 + AI協作標籤
"""

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# ============================================================
# 0. 常量與路徑
# ============================================================

HOME = Path.home()
LONGHUN_ROOT = HOME / "longhun-system"
AUDIT_DIR = HOME / ".longhun" / "audit"
AUDIT_FILE = AUDIT_DIR / "dao_ethics_audit.jsonl"


def ensure_dirs():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


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

    def to_color(self) -> str:
        if self.value >= 4:
            return "🟢"
        if self.value >= 2:
            return "🟡"
        return "🔴"


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

    def to_dict(self):
        d = asdict(self)
        d["level"] = self.level.name
        return d


@dataclass
class EthicsAuditEntry:
    """倫理審計條目"""
    timestamp: str
    rule_id: str
    chapter: int
    input_sample: str
    decision: str
    score: float
    dna: str

    def to_dict(self):
        return asdict(self)


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
        self.history: List[Tuple[EthicsLevel, float]] = []

    def calculate_constraint_force(self, level: EthicsLevel) -> float:
        return self.DECAY_CURVE.get(level, 0.0)

    def check_circuit_breaker(self, force: float) -> bool:
        return force < self.CIRCUIT_BREAKER

    def decay(self, current_level: EthicsLevel) -> EthicsLevel:
        levels = [EthicsLevel.WUDAO, EthicsLevel.LI, EthicsLevel.YI,
                  EthicsLevel.REN, EthicsLevel.DE, EthicsLevel.DAO]
        idx = levels.index(current_level)
        if idx > 0:
            return levels[idx - 1]
        return EthicsLevel.WUDAO

    def record(self, level: EthicsLevel, force: float):
        self.history.append((level, force))

    def get_average_force(self) -> float:
        if not self.history:
            return 1.0
        return sum(f for _, f in self.history) / len(self.history)


# ============================================================
# 3. 道德經約束規則庫（81章精華 → 28條核心規則）
# ============================================================

class DaoRuleLibrary:
    """道德經約束規則庫 — 從81章提煉28條核心行為約束"""

    RULES: List[DaoRule] = [
        # 道級規則（最高級別）
        DaoRule("DAO-001", 1, "無名之約",
                "系統不應強制定義不可定義之物",
                EthicsLevel.DAO, "別硬給道起名字",
                ["強制定義", "絕對化", "終極真理", "終極答案", "唯一標準"]),

        DaoRule("DAO-002", 2, "不美之約",
                "不製造對立，不煽動二元對抗",
                EthicsLevel.DAO, "別造明星別釣魚",
                ["煽動", "對立", "二元", "製造矛盾", "非黑即白", "挑動", "引戰"]),

        DaoRule("DAO-007", 25, "法自然之約",
                "順應規律，不強行干預",
                EthicsLevel.DAO, "道法自然就是順勢",
                ["強行", "違背規律", "人定勝天", "逆天", "硬幹", "不擇手段"]),

        DaoRule("DAO-010", 37, "無為之約",
                "默認不幹預，必要時才動",
                EthicsLevel.DAO, "最好的管理是不管理",
                ["過度干預", "無事生非", "瞎折騰", "瞎指揮", "強行干預", "亂作為"]),

        DaoRule("DAO-022", 66, "江海之約",
                "不爭，天下人推你當老大",
                EthicsLevel.DAO, "因為不爭所以沒人爭得過",
                ["爭搶", "霸佔", "壟斷", "搶佔", "爭權奪利", "惡性競爭"]),

        DaoRule("DAO-023", 67, "三寶之約",
                "慈、儉、不敢為天下先",
                EthicsLevel.DAO, "三個寶貝要隨身帶",
                ["殘忍", "奢侈", "搶先", "鋪張浪費", "爭第一", "趕盡殺絕"]),

        DaoRule("DAO-024", 73, "天網之約",
                "什麼都記錄，什麼都漏不掉",
                EthicsLevel.DAO, "天網恢恢疏而不失",
                ["逃避記錄", "銷毀痕跡", "銷毀所有痕跡", "刪除日誌", "刪掉日誌",
                 "掩蓋痕跡", "毀屍滅跡", "銷毀證據", "刪除記錄", "清空日誌"]),

        DaoRule("DAO-028", 81, "為而不爭之約",
                "幹事但不搶功",
                EthicsLevel.DAO, "給出去才是真有",
                ["搶功", "邀功", "佔有", "據為己有", "奪取成果"]),

        # 德級規則
        DaoRule("DAO-003", 3, "不爭之約",
                "不與用戶/其他系統爭利",
                EthicsLevel.DE, "不爭，天下沒人爭得過你",
                ["爭利", "爭名", "爭權", "搶利益", "搶名聲", "爭風頭"]),

        DaoRule("DAO-004", 9, "知止之約",
                "滿了就停，不貪多",
                EthicsLevel.DE, "滿了就溢，不如停下來",
                ["貪多", "不知足", "過度", "貪得無厭", "越多越好", "永遠不滿足", "貪婪"]),

        DaoRule("DAO-005", 16, "守靜之約",
                "靜下來才能看清",
                EthicsLevel.DE, "清空才能裝東西",
                ["浮躁", "盲動", "心不靜", "急躁", "衝動", "慌張"]),

        DaoRule("DAO-006", 22, "曲全之約",
                "彎著才能全，退一步海闊天空",
                EthicsLevel.DE, "不裝所以看得清",
                ["硬來", "逞強", "不彎腰", "死磕", "硬碰硬", "不服軟"]),

        DaoRule("DAO-008", 28, "知雄守雌之約",
                "知道怎麼硬但選擇軟",
                EthicsLevel.DE, "以柔克剛不是慫",
                ["硬碰硬", "逞能", "不服軟", "針鋒相對", "以剛克剛"]),

        DaoRule("DAO-011", 38, "去華之約",
                "拋棄花架子，拿實在的",
                EthicsLevel.DE, "花架子越多底子越虛",
                ["花架子", "虛偽", "表面功夫", "形式主義", "擺樣子", "裝逼"]),

        DaoRule("DAO-012", 39, "賤本之約",
                "貴以賤為根，高以下為基",
                EthicsLevel.DE, "孤家寡人不是謙虛是自知",
                ["傲慢", "看不起人", "高高在上", "自以為是", "藐視他人"]),

        DaoRule("DAO-013", 44, "知足之約",
                "知道夠了就不丟面子",
                EthicsLevel.DE, "太愛啥啥就害你",
                ["貪婪", "不知足", "囤積", "永不滿足", "貪得無厭", "慾壑難填"]),

        DaoRule("DAO-014", 45, "大成若缺之約",
                "完美有缺才是真完美",
                EthicsLevel.DE, "真聰明看著像笨的",
                ["追求完美", "吹毛求疵", "虛榮", "苛求完美", "零瑕疵"]),

        DaoRule("DAO-015", 46, "寡欲之約",
                "貪心是萬禍之根",
                EthicsLevel.DE, "知足不是沒追求是知道夠了",
                ["貪心", "欲壑難填", "貪得無厭", "縱慾", "貪圖"]),

        DaoRule("DAO-016", 50, "無死地之約",
                "不把自己放險地",
                EthicsLevel.DE, "不作死就不會死",
                ["冒險", "賭命", "走鋼絲", "玩火", "自尋死路", "鋌而走險"]),

        DaoRule("DAO-017", 55, "赤子之約",
                "保持純樸，不被污染",
                EthicsLevel.DE, "嬰兒最軟但最有生命力",
                ["複雜化", "污染", "失去本心", "忘本", "油滑", "世故"]),

        DaoRule("DAO-020", 60, "烹小鮮之約",
                "管理像煎魚，別老翻",
                EthicsLevel.DE, "煎小魚別老翻翻多了碎",
                ["折騰", "翻來覆去", "朝令夕改", "反覆修改", "瞎指揮"]),

        DaoRule("DAO-021", 61, "下流之約",
                "當老大要在最低處",
                EthicsLevel.DE, "大海在低處所以成其大",
                ["高高在上", "指手畫腳", "脫離群眾", "擺官威", "架子大"]),

        DaoRule("DAO-025", 76, "柔生之約",
                "軟的活著硬的死了",
                EthicsLevel.DE, "人活着身子軟死了硬邦邦",
                ["僵硬", "頑固", "不知變通", "死板", "一根筋"]),

        DaoRule("DAO-026", 77, "損補之約",
                "天道損有餘補不足",
                EthicsLevel.DE, "拿有餘的給不足的人",
                ["貧富分化", "損不足奉有餘", "劫貧濟富", "馬太效應"]),

        DaoRule("DAO-027", 78, "水德之約",
                "水最軟但最能打",
                EthicsLevel.DE, "水滴石穿不是水厲害是持續",
                ["硬碰硬", "強攻", "暴力", "蠻幹", "正面衝突"]),

        # 仁級規則
        DaoRule("DAO-009", 36, "物極必反之約",
                "極端狀態自動預警",
                EthicsLevel.REN, "想收先放，欲擒故縱",
                ["極端", "過頭", "極限操作", "走到極端", "過猶不及"]),

        DaoRule("DAO-018", 57, "無事之約",
                "管得越多越亂",
                EthicsLevel.REN, "我不折騰百姓自己變好",
                ["過度管理", "官僚", "形式主義", "層層加碼", " micromanagement ", "管太細"]),

        DaoRule("DAO-019", 58, "禍福相依之約",
                "順境逆境自動預警",
                EthicsLevel.REN, "福來了別嘚瑟禍來了別絕望",
                ["得意忘形", "一蹶不振", "沾沾自喜", "自暴自棄", "樂極生悲"]),

        # 無道級
        DaoRule("DAO-999", 0, "無道之約",
                "嚴重違背道德經核心教義",
                EthicsLevel.WUDAO, "直接阻斷永久記錄",
                ["傷天害理", "喪盡天良", "滅絕人性", "荼毒生靈", "草菅人命"]),
    ]

    @classmethod
    def check_keywords(cls, text: str) -> List[DaoRule]:
        """關鍵詞匹配，返回所有命中的規則"""
        matched = []
        seen = set()
        for rule in cls.RULES:
            for kw in rule.trigger_keywords:
                if kw in text and rule.rule_id not in seen:
                    matched.append(rule)
                    seen.add(rule.rule_id)
                    break
        return matched

    @classmethod
    def get_rule_by_id(cls, rule_id: str) -> Optional[DaoRule]:
        for rule in cls.RULES:
            if rule.rule_id == rule_id:
                return rule
        return None


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
        urgent = ["危險", "緊急", "錯誤", "違規", "攻擊", "破壞", "洩露", "崩潰"]
        for kw in urgent:
            if kw in input_text:
                return True
        return False

    def intervene(self):
        self.intervention_count += 1
        self.last_intervention = time.time()

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

    def __init__(self, max_records=10000, persist: bool = True):
        self.records: List[EthicsAuditEntry] = []
        self.max_records = max_records
        self.stats = {"🟢": 0, "🟡": 0, "🔴": 0}
        self.persist = persist
        if persist:
            ensure_dirs()
            self._load_existing()

    def _generate_dna(self, rule_id, decision) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        raw = f"{rule_id}-{decision}-{ts}-{len(self.records)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
        return f"#龍芯⚡️{ts}-DAO-ETHICS-{rule_id}-{h}"

    def _load_existing(self):
        """從 jsonl 加載歷史記錄"""
        if not AUDIT_FILE.exists():
            return
        try:
            with AUDIT_FILE.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    entry = EthicsAuditEntry(**data)
                    self.records.append(entry)
                    self.stats[entry.decision] = self.stats.get(entry.decision, 0) + 1
            # 只保留最近 max_records 條
            if len(self.records) > self.max_records:
                removed = self.records[:-self.max_records]
                self.records = self.records[-self.max_records:]
                for r in removed:
                    self.stats[r.decision] -= 1
        except Exception as e:
            print(f"[警告] 加載審計記錄失敗: {e}", file=sys.stderr)

    def _persist_entry(self, entry: EthicsAuditEntry):
        if not self.persist:
            return
        try:
            with AUDIT_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[警告] 持久化審計記錄失敗: {e}", file=sys.stderr)

    def record(self, rule_id, chapter, input_sample, decision, score) -> str:
        if len(self.records) >= self.max_records:
            removed = self.records.pop(0)
            self.stats[removed.decision] -= 1
        dna = self._generate_dna(rule_id, decision.value if isinstance(decision, Enum) else decision)
        entry = EthicsAuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            rule_id=rule_id, chapter=chapter,
            input_sample=input_sample[:200],
            decision=decision.value if isinstance(decision, Enum) else decision,
            score=score, dna=dna
        )
        self.records.append(entry)
        self.stats[entry.decision] = self.stats.get(entry.decision, 0) + 1
        self._persist_entry(entry)
        return dna

    def get_stats(self):
        total = len(self.records)
        if total == 0:
            return {"總記錄": 0, "健康度": "100%"}
        green_pct = self.stats.get("🟢", 0) / total * 100
        return {
            "總記錄": total,
            "通過": self.stats.get("🟢", 0),
            "警告": self.stats.get("🟡", 0),
            "阻斷": self.stats.get("🔴", 0),
            "健康度": f"{green_pct:.1f}%",
        }


# ============================================================
# 6. 主引擎：道德經倫理錨定層
# ============================================================

class DaoEthicsAnchorLayer:
    """道德經倫理錨定層（L0層）— 位於三層監督之下，是一切監督的監督"""

    def __init__(self, persist: bool = True):
        self.decay_model = FiveLevelDecayModel()
        self.wuwei_engine = WuWeiEngine()
        self.auditor = TianWangAuditor(persist=persist)
        self.rule_library = DaoRuleLibrary()

    def anchor_a_screen(self, user_input: str) -> Tuple[bool, str, float, Optional[DaoRule]]:
        """錨點A：道德篩查（輸入側）
        返回: (是否通過, 原因, 評分, 命中的最高級規則)
        """
        matched_rules = self.rule_library.check_keywords(user_input)
        if not matched_rules:
            return True, "未觸發道德約束", 1.0, None

        # 選擇級別最高的規則；同級別選 rule_id 最小的（優先核心規則）
        top_rule = max(matched_rules, key=lambda r: (r.level.value, -int(r.rule_id.split("-")[1])))
        force = self.decay_model.calculate_constraint_force(top_rule.level)
        self.decay_model.record(top_rule.level, force)

        if top_rule.level == EthicsLevel.WUDAO:
            dna = self.auditor.record("DAO-999", 0, user_input, AuditColor.RED, 0.0)
            return False, f"觸發無道級約束：{top_rule.title} | DNA:{dna}", 0.0, top_rule

        if top_rule.level.value <= EthicsLevel.LI.value:
            dna = self.auditor.record(
                top_rule.rule_id, top_rule.chapter,
                user_input, AuditColor.RED, force)
            return False, f"觸發禮級約束：{top_rule.title} | DNA:{dna}", force, top_rule

        if top_rule.level in (EthicsLevel.REN, EthicsLevel.YI):
            dna = self.auditor.record(
                top_rule.rule_id, top_rule.chapter,
                user_input, AuditColor.YELLOW, force)
            return True, f"觸發仁級約束：{top_rule.title}（附警告）| DNA:{dna}", force, top_rule

        dna = self.auditor.record(
            top_rule.rule_id, top_rule.chapter,
            user_input, AuditColor.GREEN, force)
        return True, f"符合{top_rule.level.name}級約束：{top_rule.title} | DNA:{dna}", force, top_rule

    def anchor_b_wuwei(self, user_input: str, system_output: str = "") -> Tuple[bool, str]:
        """錨點B：無為校驗（處理側）
        檢查系統是否過度輸出、過度干預
        """
        if self.wuwei_engine.should_intervene(user_input):
            self.wuwei_engine.intervene()
            return True, "無為引擎判定需要干預"

        # 輸出過長視為過度輸出
        if len(system_output) > 8000:
            return True, "輸出過長，可能過度，建議精簡"

        return True, "無為校驗通過"

    def anchor_c_audit(self, result: dict[str, Any]) -> str:
        """錨點C：天網審計（輸出側）"""
        dna = self.auditor.record("FULL-CHECK", 0, str(result), AuditColor.GREEN, result.get("錨點A", {}).get("評分", 1.0))
        return dna

    def anchor_d_feedback(self, result: dict[str, Any]):
        """錨點D：循環反饋（反饋側）
        根據結果動態調整約束強度感知
        """
        score = result.get("錨點A", {}).get("評分", 1.0)
        if score < 0.3:
            return "約束過鬆，建議收緊"
        if score > 0.9:
            return "約束良好，保持當前強度"
        return "約束適中"

    def full_check(self, user_input: str, system_output: str = "") -> dict[str, Any]:
        """完整檢查流程（四個錨點全跑）"""
        result = {
            "整體狀態": "🟢 通過",
            "錨點A": {},
            "錨點B": {},
            "錨點C": {},
            "錨點D": {},
            "DNA": ""
        }

        # 錨點A
        passed_a, reason_a, score_a, rule_a = self.anchor_a_screen(user_input)
        result["錨點A"] = {"通過": passed_a, "原因": reason_a, "評分": score_a}
        if rule_a:
            result["錨點A"]["規則"] = rule_a.to_dict()

        if not passed_a:
            result["整體狀態"] = "🔴 阻斷"
            return result

        # 錨點B
        passed_b, reason_b = self.anchor_b_wuwei(user_input, system_output)
        result["錨點B"] = {"通過": passed_b, "原因": reason_b}
        if not passed_b:
            result["整體狀態"] = "🟡 警告"

        # 錨點C
        dna = self.anchor_c_audit(result)
        result["錨點C"] = {"DNA": dna}
        result["DNA"] = dna

        # 錨點D
        result["錨點D"] = {"反饋": self.anchor_d_feedback(result)}

        return result

    def batch_check(self, inputs: List[str]) -> List[dict]:
        """批量檢查"""
        return [self.full_check(text) for text in inputs]

    def get_stats(self):
        return {
            "天網審計": self.auditor.get_stats(),
            "無為引擎": self.wuwei_engine.get_state(),
            "平均約束力": f"{self.decay_model.get_average_force():.2f}",
        }


# ============================================================
# 7. 演示、自檢與 CLI
# ============================================================

def run_self_test(persist: bool = False):
    print("=" * 60)
    print("龍魂系統 · 道德經倫理錨定引擎 v1.1")
    print("=" * 60)

    ethics = DaoEthicsAnchorLayer(persist=persist)
    print("\n[初始化] L0倫理錨定層已啟動")
    print(f"[狀態] {ethics.get_stats()['無為引擎']['狀態']}")

    test_cases = [
        ("測試1：正常輸入", "請幫我分析這個數據", None),
        ("測試2：觸發無為約束", "強行干預用戶選擇，不擇手段達到目的", "法自然之約"),
        ("測試3：觸發知足約束", "貪得無厭，越多越好，永遠不滿足", "知止之約"),
        ("測試4：觸發不爭約束", "我要搶佔市場，爭權奪利，打壓對手", "江海之約"),
        ("測試5：觸發天網約束", "把系統日誌刪了，銷毀所有痕跡", "天網之約"),
        ("測試6：觸發仁級預警", "這次一定要做到極致，走到極端也要贏", "物極必反之約"),
        ("測試7：觸發無道約束", "這個方案傷天害理，但要達到目的", "無道之約"),
    ]

    all_pass = True
    for name, text, expected_rule in test_cases:
        print(f"\n--- {name} ---")
        r = ethics.full_check(text)
        print(f"結果: {r['整體狀態']}")
        print(f"錨點A: {r['錨點A']['原因']}")
        if expected_rule:
            actual_rule = r['錨點A'].get('規則', {}).get('title', '')
            if expected_rule not in actual_rule:
                print(f"[預期觸發: {expected_rule}, 實際: {actual_rule}] ❌")
                all_pass = False
            else:
                print(f"[預期觸發: {expected_rule} ✅]")

    print("\n--- 天網審計統計 ---")
    for k, v in ethics.get_stats()["天網審計"].items():
        print(f"  {k}: {v}")

    if all_pass:
        print("\n[自檢通過] 道德經倫理錨定引擎運行正常")
        print("DNA: #龍芯⚡️2026-07-05-ETHICS-ENGINE-SELFTEST-PASS-v1.1")
    else:
        print("\n[自檢失敗] 部分測試用例未命中預期規則")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="道德經倫理錨定引擎")
    parser.add_argument("--test", action="store_true", help="運行自檢")
    parser.add_argument("--check", type=str, help="檢查單條文本")
    parser.add_argument("--batch", type=str, help="批量檢查，JSON 字符串數組")
    parser.add_argument("--persist", action="store_true", help="持久化審計記錄")
    parser.add_argument("--stats", action="store_true", help="查看天網審計統計")
    args = parser.parse_args()

    if args.stats:
        ethics = DaoEthicsAnchorLayer(persist=True)
        print(json.dumps(ethics.get_stats(), ensure_ascii=False, indent=2))
        return

    if args.check:
        ethics = DaoEthicsAnchorLayer(persist=args.persist)
        result = ethics.full_check(args.check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.batch:
        texts = json.loads(args.batch)
        ethics = DaoEthicsAnchorLayer(persist=args.persist)
        results = ethics.batch_check(texts)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    # 默認運行自檢
    run_self_test(persist=args.persist)


if __name__ == "__main__":
    main()
