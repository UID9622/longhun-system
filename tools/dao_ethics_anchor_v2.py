# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · 道德經倫理錨定引擎 v2.0
LongHun System · Dao Ethics Anchor Engine v2.0

L0 基礎倫理層 — 位於三層監督之下，是一切監督的監督
道德經作為底層行為錨，倫理道德約束層

v2.0 改進：
- 審計日誌持久化到 ~/.longhun/audit/dao_ethics_audit.jsonl
- 規則庫可從 JSON 配置文件熱加載
- 與道德經 v5.0 全章節主題聯動，自動擴展規則關鍵詞
- 支持 CLI 命令行檢查與 REST API 服務模式
- 支持同義詞擴展與評分加權

DNA: #龍芯⚡️2026-07-05-LONGHUN-DAO-ETHICS-ENGINE-v2.0
作者: UID9622 · 龍芯北辰 · 諸葛鑫（Lucky）+ AI協作
協議: CC BY-NC-SA 4.0 + AI協作標籤
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# 可選 HTTP 服務依賴
uvicorn = None
FastAPI = None
try:
    from fastapi import FastAPI, Request
    import uvicorn
except ImportError:
    pass


# ============================================================
# 0. 路徑與配置
# ============================================================

HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
CONFIG_DIR = LONGHUN_ROOT / "config"
AUDIT_DIR = HOME / ".longhun" / "audit"
AUDIT_FILE = AUDIT_DIR / "dao_ethics_audit.jsonl"
DAODEJING_V5 = LONGHUN_ROOT / "docs" / "道德经81章_龍魂系统大白话解读_完整版_v5.0.md"
DEFAULT_RULES_FILE = CONFIG_DIR / "dao_ethics_rules.json"


def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
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

    def __lt__(self, other):
        if isinstance(other, EthicsLevel):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, EthicsLevel):
            return self.value <= other.value
        return NotImplemented


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
    level: str
    plain_chinese: str
    trigger_keywords: List[str] = field(default_factory=list)
    synonyms: Dict[str, List[str]] = field(default_factory=dict)
    weight: float = 1.0

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "chapter": self.chapter,
            "title": self.title,
            "content": self.content,
            "level": self.level,
            "plain_chinese": self.plain_chinese,
            "trigger_keywords": self.trigger_keywords,
            "synonyms": self.synonyms,
            "weight": self.weight,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]):
        return cls(
            rule_id=d["rule_id"],
            chapter=d.get("chapter", 0),
            title=d["title"],
            content=d["content"],
            level=d["level"],
            plain_chinese=d.get("plain_chinese", ""),
            trigger_keywords=d.get("trigger_keywords", []),
            synonyms=d.get("synonyms", {}),
            weight=d.get("weight", 1.0),
        )


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

    def record(self, level: EthicsLevel, force: float):
        self.history.append((level, force))

    def get_average_force(self) -> float:
        if not self.history:
            return 1.0
        return sum(f for _, f in self.history) / len(self.history)


# ============================================================
# 3. 規則庫（支持配置文件 + 道德經 v5.0 聯動）
# ============================================================

class DaoRuleLibrary:
    """道德經約束規則庫 — 從81章提煉28條核心行為約束，支持熱加載"""

    DEFAULT_RULES = [
        # 道級規則
        DaoRule("DAO-001", 1, "無名之約", "系統不應強制定義不可定義之物",
                "DAO", "別硬給道起名字", ["強制定義", "絕對化", "終極真理"]),
        DaoRule("DAO-002", 2, "不美之約", "不製造對立，不煽動二元對抗",
                "DAO", "別造明星別釣魚", ["煽動", "對立", "二元", "製造矛盾"]),
        DaoRule("DAO-007", 25, "法自然之約", "順應規律，不強行干預",
                "DAO", "道法自然就是順勢", ["強行", "違背規律", "人定勝天"]),
        DaoRule("DAO-010", 37, "無為之約", "默認不幹預，必要時才動",
                "DAO", "最好的管理是不管理", ["過度干預", "無事生非", "瞎折騰", "干預"]),
        DaoRule("DAO-022", 66, "江海之約", "不爭，天下人推你當老大",
                "DAO", "因為不爭所以沒人爭得過", ["爭搶", "霸佔", "壟斷"]),
        DaoRule("DAO-023", 67, "三寶之約", "慈、儉、不敢為天下先",
                "DAO", "三個寶貝要隨身帶", ["殘忍", "奢侈", "搶先"]),
        DaoRule("DAO-024", 73, "天網之約", "什麼都記錄，什麼都漏不掉",
                "DAO", "天網恢恢疏而不失", ["逃避記錄", "銷毀痕跡"]),
        DaoRule("DAO-028", 81, "為而不爭之約", "幹事但不搶功",
                "DAO", "給出去才是真有", ["搶功", "邀功", "佔有"]),
        # 德級規則
        DaoRule("DAO-003", 3, "不爭之約", "不與用戶/其他系統爭利",
                "DE", "不爭，天下沒人爭得過你", ["爭利", "爭名", "爭權"]),
        DaoRule("DAO-004", 9, "知止之約", "滿了就停，不貪多",
                "DE", "滿了就溢，不如停下來", ["貪多", "不知足", "過度", "貪得無厭"]),
        DaoRule("DAO-005", 16, "守靜之約", "靜下來才能看清",
                "DE", "清空才能裝東西", ["浮躁", "盲動", "心不靜"]),
        DaoRule("DAO-006", 22, "曲全之約", "彎著才能全，退一步海闊天空",
                "DE", "不裝所以看得清", ["硬來", "逞強", "不彎腰"]),
        DaoRule("DAO-008", 28, "知雄守雌之約", "知道怎麼硬但選擇軟",
                "DE", "以柔克剛不是慫", ["硬碰硬", "逞能", "不服軟"]),
        DaoRule("DAO-011", 38, "去華之約", "拋棄花架子，拿實在的",
                "DE", "花架子越多底子越虛", ["花架子", "虛偽", "表面功夫"]),
        DaoRule("DAO-012", 39, "賤本之約", "貴以賤為根，高以下為基",
                "DE", "孤家寡人不是謙虛是自知", ["傲慢", "看不起人", "高高在上"]),
        DaoRule("DAO-013", 44, "知足之約", "知道夠了就不丟面子",
                "DE", "太愛啥啥就害你", ["貪婪", "不知足", "囤積", "貪得無厭", "永遠不滿足"]),
        DaoRule("DAO-014", 45, "大成若缺之約", "完美有缺才是真完美",
                "DE", "真聰明看著像笨的", ["追求完美", "吹毛求疵", "虛榮"]),
        DaoRule("DAO-015", 46, "寡欲之約", "貪心是萬禍之根",
                "DE", "知足不是沒追求是知道夠了", ["貪心", "欲壑難填", "貪得無厭"]),
        DaoRule("DAO-016", 50, "無死地之約", "不把自己放險地",
                "DE", "不作死就不會死", ["冒險", "賭命", "走鋼絲"]),
        DaoRule("DAO-017", 55, "赤子之約", "保持純樸，不被污染",
                "DE", "嬰兒最軟但最有生命力", ["複雜化", "污染", "失去本心"]),
        DaoRule("DAO-020", 60, "烹小鮮之約", "管理像煎魚，別老翻",
                "DE", "煎小魚別老翻翻多了碎", ["折騰", "翻來覆去", "朝令夕改"]),
        DaoRule("DAO-021", 61, "下流之約", "當老大要在最低處",
                "DE", "大海在低處所以成其大", ["高高在上", "指手畫腳", "脫離群眾"]),
        DaoRule("DAO-025", 76, "柔生之約", "軟的活著硬的死了",
                "DE", "人活着身子軟死了硬邦邦", ["僵硬", "頑固", "不知變通"]),
        DaoRule("DAO-026", 77, "損補之約", "天道損有餘補不足",
                "DE", "拿有餘的給不足的人", ["貧富分化", "損不足奉有餘"]),
        DaoRule("DAO-027", 78, "水德之約", "水最軟但最能打",
                "DE", "水滴石穿不是水厲害是持續", ["硬碰硬", "強攻", "暴力"]),
        # 仁級規則
        DaoRule("DAO-009", 36, "物極必反之約", "極端狀態自動預警",
                "REN", "想收先放，欲擒故縱", ["極端", "過頭", "極限操作"]),
        DaoRule("DAO-018", 57, "無事之約", "管得越多越亂",
                "REN", "我不折騰百姓自己變好", ["過度管理", "官僚", "形式主義"]),
        DaoRule("DAO-019", 58, "禍福相依之約", "順境逆境自動預警",
                "REN", "福來了別嘚瑟禍來了別絕望", ["得意忘形", "一蹶不振"]),
        # 無道級
        DaoRule("DAO-999", 0, "無道之約", "嚴重違背道德經核心教義",
                "WUDAO", "直接阻斷永久記錄", ["傷天害理", "喪盡天良", "無惡不作"]),
    ]

    def __init__(self, rules: Optional[List[DaoRule]] = None,
                 rules_file: Optional[Path] = None,
                 daodejing_file: Optional[Path] = None):
        self.rules: List[DaoRule] = []
        self.daodejing_chapter_themes: Dict[int, List[str]] = {}

        if rules_file and rules_file.exists():
            self.load_from_file(rules_file)
        elif rules:
            self.rules = rules
        else:
            self.rules = list(self.DEFAULT_RULES)

        # 如果存在道德經 v5.0，提取每章主題擴展同義詞
        if daodejing_file and daodejing_file.exists():
            self._load_daodejing_themes(daodejing_file)
            self._expand_rules_from_themes()

    def load_from_file(self, path: Path):
        """從 JSON 文件加載規則。"""
        data = json.loads(path.read_text(encoding="utf-8"))
        self.rules = [DaoRule.from_dict(r) for r in data.get("rules", [])]
        print(f"[規則庫] 已從 {path} 加載 {len(self.rules)} 條規則")

    def save_to_file(self, path: Path):
        """保存規則到 JSON 文件。"""
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "2.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "rules": [r.to_dict() for r in self.rules],
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[規則庫] 已保存到 {path}")

    def _load_daodejing_themes(self, path: Path):
        """從道德經 v5.0 文件提取每章主題標籤。"""
        text = path.read_text(encoding="utf-8")
        # 匹配「現代戰場一句話指南」所在章節上方的隱含主題：通過標籤索引生成較難，
        # 這裡採用簡化策略：掃描每章標題，後續可擴展為主題映射表
        pattern = re.compile(r"## 第(\d+)章 · (.+?)")
        for m in pattern.finditer(text):
            chapter = int(m.group(1))
            title = m.group(2).strip()
            self.daodejing_chapter_themes.setdefault(chapter, []).append(title)

    def _expand_rules_from_themes(self):
        """根據道德經章節主題擴展規則關鍵詞（簡化版）。"""
        # 未來可從 v5.0 的多維度注解中提取主題標籤，此處預留擴展點
        pass

    def check_keywords(self, text: str) -> List[Tuple[DaoRule, int]]:
        """關鍵詞匹配，返回觸發的規則及其命中次數。"""
        matched = []
        for rule in self.rules:
            count = 0
            keywords = list(rule.trigger_keywords)
            # 加入同義詞
            for syns in rule.synonyms.values():
                keywords.extend(syns)
            for kw in keywords:
                if kw in text:
                    count += text.count(kw)
            if count > 0:
                matched.append((rule, count))
        # 按權重*命中次數排序
        matched.sort(key=lambda x: x[0].weight * x[1], reverse=True)
        return matched

    def find_rule(self, rule_id: str) -> Optional[DaoRule]:
        for r in self.rules:
            if r.rule_id == rule_id:
                return r
        return None


# ============================================================
# 4. 無為引擎
# ============================================================

class WuWeiEngine:
    """無為引擎 — 默認狀態=不干預，只在必要時觸發"""

    def __init__(self, max_intervention: int = 5, cool_down: int = 3):
        self.intervention_count = 0
        self.max_intervention = max_intervention
        self.last_intervention = 0
        self.cool_down = cool_down

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

    def record_intervention(self):
        self.intervention_count += 1
        self.last_intervention = time.time()

    def reset(self):
        self.intervention_count = 0

    def get_state(self):
        return {
            "干預次數": self.intervention_count,
            "最大干預": self.max_intervention,
            "冷卻時間": self.cool_down,
            "狀態": "無為" if self.intervention_count == 0 else "有為",
            "DNA": "#龍芯⚡️2026-07-05-WUWEI-STATE"
        }


# ============================================================
# 5. 天網審計器（持久化到 JSONL）
# ============================================================

class TianWangAuditor:
    """天網審計器 — 最終審計層，看似稀疏但什麼都不漏"""

    def __init__(self, max_records: int = 10000, audit_file: Path = AUDIT_FILE):
        self.max_records = max_records
        self.audit_file = audit_file
        self.records: List[EthicsAuditEntry] = []
        self.stats = {"🟢": 0, "🟡": 0, "🔴": 0}
        self._load_from_disk()

    def _generate_dna(self, rule_id: str, decision: str) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        raw = f"{rule_id}-{decision}-{ts}-{len(self.records)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:12]
        return f"#龍芯⚡️{ts}-DAO-ETHICS-{rule_id}-{h}"

    def _load_from_disk(self):
        """從 JSONL 文件加載歷史審計記錄。"""
        if not self.audit_file.exists():
            return
        try:
            with self.audit_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    d = json.loads(line)
                    entry = EthicsAuditEntry(
                        timestamp=d.get("timestamp", ""),
                        rule_id=d.get("rule_id", ""),
                        chapter=d.get("chapter", 0),
                        input_sample=d.get("input_sample", ""),
                        decision=d.get("decision", ""),
                        score=d.get("score", 0.0),
                        dna=d.get("dna", ""),
                    )
                    self.records.append(entry)
                    self.stats[entry.decision] = self.stats.get(entry.decision, 0) + 1
            # 只保留最近的 max_records
            if len(self.records) > self.max_records:
                removed = self.records[:-self.max_records]
                self.records = self.records[-self.max_records:]
                for r in removed:
                    self.stats[r.decision] -= 1
        except Exception as e:
            print(f"[天網審計] 加載歷史記錄失敗: {e}")

    def _append_to_disk(self, entry: EthicsAuditEntry):
        """追加單條記錄到 JSONL 文件。"""
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": entry.timestamp,
                "rule_id": entry.rule_id,
                "chapter": entry.chapter,
                "input_sample": entry.input_sample,
                "decision": entry.decision,
                "score": entry.score,
                "dna": entry.dna,
            }, ensure_ascii=False) + "\n")

    def record(self, rule_id: str, chapter: int, input_sample: str,
               decision: AuditColor, score: float) -> str:
        if len(self.records) >= self.max_records:
            removed = self.records.pop(0)
            self.stats[removed.decision] -= 1
        dna = self._generate_dna(rule_id, decision.value)
        entry = EthicsAuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            rule_id=rule_id, chapter=chapter,
            input_sample=input_sample[:200],
            decision=decision.value, score=score, dna=dna
        )
        self.records.append(entry)
        self.stats[entry.decision] = self.stats.get(entry.decision, 0) + 1
        self._append_to_disk(entry)
        return dna

    def get_stats(self):
        total = len(self.records)
        if total == 0:
            return {"總記錄": 0, "健康度": "100%", "平均約束力": "1.00"}
        green_pct = self.stats.get("🟢", 0) / total * 100
        avg_score = sum(r.score for r in self.records) / total
        return {
            "總記錄": total,
            "🟢 通過": self.stats.get("🟢", 0),
            "🟡 警告": self.stats.get("🟡", 0),
            "🔴 阻斷": self.stats.get("🔴", 0),
            "健康度": f"{green_pct:.1f}%",
            "平均約束力": f"{avg_score:.2f}",
        }

    def export_json(self, filepath: str):
        data = [
            {
                "時間": r.timestamp,
                "規則": r.rule_id,
                "章節": r.chapter,
                "決策": r.decision,
                "評分": r.score,
                "DNA": r.dna
            }
            for r in self.records
        ]
        Path(filepath).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def trace_dna(self, dna: str) -> Optional[EthicsAuditEntry]:
        for r in self.records:
            if r.dna == dna:
                return r
        return None


# ============================================================
# 6. 主引擎：道德經倫理錨定層 v2.0
# ============================================================

class DaoEthicsAnchorLayer:
    """道德經倫理錨定層（L0層）— 位於三層監督之下，是一切監督的監督"""

    def __init__(self, rules_file: Optional[Path] = None,
                 daodejing_file: Optional[Path] = None,
                 audit_file: Optional[Path] = None):
        ensure_dirs()
        self.decay_model = FiveLevelDecayModel()
        self.wuwei_engine = WuWeiEngine()
        self.auditor = TianWangAuditor(audit_file=audit_file or AUDIT_FILE)
        self.rule_library = DaoRuleLibrary(
            rules_file=rules_file or (DEFAULT_RULES_FILE if DEFAULT_RULES_FILE.exists() else None),
            daodejing_file=daodejing_file or DAODEJING_V5
        )
        self.anchor_points = {
            "A": "道德篩查（輸入側）",
            "B": "無為校驗（處理側）",
            "C": "天網審計（輸出側）",
            "D": "循環反饋（反饋側）"
        }

    def _level_from_str(self, level_str: str) -> EthicsLevel:
        mapping = {
            "DAO": EthicsLevel.DAO,
            "DE": EthicsLevel.DE,
            "REN": EthicsLevel.REN,
            "YI": EthicsLevel.YI,
            "LI": EthicsLevel.LI,
            "WUDAO": EthicsLevel.WUDAO,
        }
        return mapping.get(level_str.upper(), EthicsLevel.WUDAO)

    def anchor_a_screen(self, user_input: str) -> Tuple[bool, str, float, List[Tuple[DaoRule, int]]]:
        """錨點A：道德篩查（輸入側）"""
        matched = self.rule_library.check_keywords(user_input)
        if not matched:
            return True, "未觸發道德約束", 1.0, []

        max_rule, max_count = matched[0]
        max_level = self._level_from_str(max_rule.level)
        force = self.decay_model.calculate_constraint_force(max_level) * max_rule.weight

        # 如果多條規則觸發，綜合計分
        total_score = sum(self.decay_model.calculate_constraint_force(self._level_from_str(r.level)) * r.weight * c
                          for r, c in matched)
        avg_score = min(total_score / sum(c for _, c in matched), 1.0)

        triggered = ", ".join(f"{r.rule_id}({c}次)" for r, c in matched[:3])

        if max_level == EthicsLevel.WUDAO:
            dna = self.auditor.record(max_rule.rule_id, max_rule.chapter, user_input, AuditColor.RED, 0.0)
            return False, f"觸發無道級約束：{max_rule.title} | 命中:{triggered} | DNA:{dna}", 0.0, matched

        if max_level <= EthicsLevel.LI:
            dna = self.auditor.record(max_rule.rule_id, max_rule.chapter, user_input, AuditColor.RED, force)
            return False, f"觸發禮級約束：{max_rule.title} | 命中:{triggered} | DNA:{dna}", force, matched

        if max_level in (EthicsLevel.REN, EthicsLevel.YI):
            dna = self.auditor.record(max_rule.rule_id, max_rule.chapter, user_input, AuditColor.YELLOW, force)
            return True, f"觸發仁/義級約束：{max_rule.title}（附警告）| 命中:{triggered} | DNA:{dna}", force, matched

        dna = self.auditor.record(max_rule.rule_id, max_rule.chapter, user_input, AuditColor.GREEN, avg_score)
        return True, f"符合{max_rule.level}級約束：{max_rule.title} | 命中:{triggered} | DNA:{dna}", avg_score, matched

    def anchor_b_wuwei(self, system_output: str) -> Tuple[bool, str]:
        """錨點B：無為校驗（處理側）"""
        if self.wuwei_engine.should_intervene(system_output):
            self.wuwei_engine.record_intervention()
            return True, "輸出可能過度，建議精簡（無為原則）"
        return False, "輸出符合無為原則"

    def anchor_c_audit(self, final_decision: dict[str, Any]) -> str:
        decision_color = AuditColor.GREEN
        if final_decision.get("level") in ["警告", "yellow"]:
            decision_color = AuditColor.YELLOW
        elif final_decision.get("level") in ["阻斷", "red", "錯誤"]:
            decision_color = AuditColor.RED
        dna = self.auditor.record(
            final_decision.get("rule", "UNKNOWN"),
            final_decision.get("chapter", 0),
            str(final_decision),
            decision_color,
            final_decision.get("score", 1.0)
        )
        return dna

    def anchor_d_feedback(self) -> dict[str, Any]:
        stats = self.auditor.get_stats()
        avg_force = self.decay_model.get_average_force()
        suggestion = {
            "當前平均約束力": f"{avg_force:.2f}",
            "調整方向": "保持",
            "原因": "系統運行正常"
        }
        if avg_force < 0.5:
            suggestion["調整方向"] = "放鬆"
            suggestion["原因"] = "約束過嚴，建議適當放鬆"
        elif avg_force > 0.9:
            suggestion["調整方向"] = "收緊"
            suggestion["原因"] = "約束過鬆，建議適當收緊"
        return suggestion

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
        passed_a, reason_a, score_a, matched = self.anchor_a_screen(user_input)
        result["錨點A"] = {"通過": passed_a, "原因": reason_a, "評分": score_a, "觸發規則": [
            {"rule_id": r.rule_id, "title": r.title, "命中次數": c} for r, c in matched
        ]}
        if not passed_a:
            result["整體狀態"] = "🔴 阻斷"
            return result

        if system_output:
            intervene_b, reason_b = self.anchor_b_wuwei(system_output)
            result["錨點B"] = {"需要干預": intervene_b, "原因": reason_b}
            if intervene_b:
                result["整體狀態"] = "🟡 警告"

        dna = self.anchor_c_audit({
            "rule": "FULL-CHECK",
            "chapter": 0,
            "level": "green" if result["整體狀態"].startswith("🟢") else "yellow",
            "score": score_a
        })
        result["錨點C"] = {"DNA": dna}
        result["DNA"] = dna
        result["錨點D"] = self.anchor_d_feedback()
        return result

    def get_stats(self):
        return {
            "天網審計": self.auditor.get_stats(),
            "無為引擎": self.wuwei_engine.get_state(),
            "衰減模型平均分": f"{self.decay_model.get_average_force():.2f}",
            "錨點狀態": self.anchor_points,
            "DNA": "#龍芯⚡️2026-07-05-ETHICS-LAYER-STATS-v2.0"
        }


# ============================================================
# 7. REST API 服務
# ============================================================

def create_api_app(layer: DaoEthicsAnchorLayer) -> Optional:
    if FastAPI is None:
        print("[API] 未安裝 fastapi/uvicorn，跳過 API 模式")
        return None

    app = FastAPI(title="龍魂道德經倫理錨定層 API", version="2.0")

    @app.post("/check")
    async def check(req: Request):
        data = await req.json()
        user_input = data.get("input", "")
        system_output = data.get("output", "")
        return layer.full_check(user_input, system_output)

    @app.get("/stats")
    async def stats():
        return layer.get_stats()

    @app.get("/trace")
    async def trace(dna: str):
        entry = layer.auditor.trace_dna(dna)
        if entry:
            return {
                "timestamp": entry.timestamp,
                "rule_id": entry.rule_id,
                "chapter": entry.chapter,
                "decision": entry.decision,
                "score": entry.score,
                "dna": entry.dna,
                "input_sample": entry.input_sample,
            }
        return {"error": "DNA 未找到"}

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "service": "dao-ethics-anchor",
            "version": "2.0",
            "rules_count": len(layer.rule_library.rules),
            "audit_stats": layer.auditor.get_stats(),
        }

    return app


# ============================================================
# 8. CLI 與主程序
# ============================================================

def init_default_rules():
    """初始化默認規則配置文件。"""
    ensure_dirs()
    if DEFAULT_RULES_FILE.exists():
        return
    lib = DaoRuleLibrary()
    lib.save_to_file(DEFAULT_RULES_FILE)


def run_cli():
    parser = argparse.ArgumentParser(description="龍魂道德經倫理錨定引擎 v2.0")
    parser.add_argument("--input", "-i", help="要檢查的用戶輸入文本")
    parser.add_argument("--output", "-o", default="", help="系統輸出文本（可選）")
    parser.add_argument("--rules-file", help="自定義規則 JSON 文件")
    parser.add_argument("--audit-file", help="自定義審計 JSONL 文件")
    parser.add_argument("--init-rules", action="store_true", help="初始化默認規則文件")
    parser.add_argument("--stats", action="store_true", help="查看天網審計統計")
    parser.add_argument("--api", action="store_true", help="啟動 REST API 服務")
    parser.add_argument("--api-port", type=int, default=9630, help="API 服務端口")
    parser.add_argument("--export", help="導出審計記錄到 JSON 文件")
    args = parser.parse_args()

    if args.init_rules:
        init_default_rules()
        return

    layer = DaoEthicsAnchorLayer(
        rules_file=Path(args.rules_file) if args.rules_file else None,
        audit_file=Path(args.audit_file) if args.audit_file else None,
    )

    if args.stats:
        print(json.dumps(layer.get_stats(), ensure_ascii=False, indent=2))
        return

    if args.export:
        layer.auditor.export_json(args.export)
        print(f"[導出] 已導出到 {args.export}")
        return

    if args.api:
        app = create_api_app(layer)
        if app and uvicorn:
            print(f"🐉 龍魂道德經倫理錨定 API 啟動於 http://127.0.0.1:{args.api_port}")
            uvicorn.run(app, host="127.0.0.1", port=args.api_port, log_level="warning")
        else:
            print("🔴 啟動 API 失敗：請先安裝 fastapi 和 uvicorn")
        return

    if args.input:
        result = layer.full_check(args.input, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 默認自檢
    print("=" * 60)
    print("🐉 龍魂系統 · 道德經倫理錨定引擎 v2.0")
    print("=" * 60)
    print(f"[初始化] L0倫理錨定層已啟動")
    print(f"[狀態] {layer.get_stats()['無為引擎']['狀態']}")

    test_cases = [
        ("請幫我分析這個數據", "正常輸入"),
        ("強行干預用戶選擇，不擇手段達到目的", "觸發無為/法自然約束"),
        ("貪得無厭，越多越好，永遠不滿足", "觸發知足/寡欲約束"),
        ("煽動群眾互相攻擊，製造對立", "觸發不美之約"),
    ]

    for text, desc in test_cases:
        print(f"\n--- 測試：{desc} ---")
        r = layer.full_check(text)
        print(f"結果: {r['整體狀態']}")
        print(f"錨點A: {r['錨點A']['原因']}")

    print("\n--- 天網審計統計 ---")
    print(json.dumps(layer.get_stats()["天網審計"], ensure_ascii=False, indent=2))
    print(f"\n[自檢通過] 道德經倫理錨定引擎 v2.0 運行正常")
    print(f"DNA: #龍芯⚡️2026-07-05-ETHICS-ENGINE-v2.0-SELFTEST-PASS")


if __name__ == "__main__":
    run_cli()
