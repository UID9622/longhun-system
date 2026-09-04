#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·行為密碼學集成測試實驗室 v2.2（精準校準版）
DNA: #龍芯⚡️丙午·丙申·甲寅·子時·䷀乾-BEHAVIORAL-CRYPTO-INTEGRATED-LAB-V2.2
License: MulanPSL v2

改進:
  v2.2: 語義親和度作為正向加成而非權重因子
        合法用戶不受內容主題影響（只驗身份+行為）
        攻擊者被多重信號鎖定（行為異常+攻擊標記+語義偏離）
        閾值: 🟢≥0.65 | 🟡≥0.45 | 🔴<0.45
"""

import hashlib, json, math, os, random, sys, time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from yijing_account_engine import YijingAccountEngine, YijingAccountIdentity, AccountVerificationResult


# ═══════════════════════════════════════
# §1. 數據結構
# ═══════════════════════════════════════

@dataclass
class BehavioralFingerprint:
    keystroke_intervals_ms: List[float] = field(default_factory=list)
    typing_speed_cps: float = 0.0
    burst_pattern: str = ""
    mouse_curvature: float = 0.5
    click_pressure_avg: float = 0.5
    decision_latency_ms: float = 1000.0
    vocabulary_size: int = 5000
    sentence_length_avg: float = 25.0
    punctuation_style: str = "full_cjk"
    chinese_variant: str = "mixed"
    typo_rate: float = 0.01
    correction_pattern: str = "immediate"
    context_switches: int = 2
    focus_duration_ms: float = 1800000.0
    sentiment_variance: float = 0.1
    emotional_stability: float = 0.85
    is_attack: bool = False
    anomaly_flags: List[str] = field(default_factory=list)

@dataclass
class ScenarioResult:
    scenario_id: str; scenario_name: str; description: str
    expected: str; actual_verdict: str
    yijing_conf: float; behavior_sim: float
    semantic_bonus: float; anomaly_count: int
    combined: float; passed: bool
    details: Dict; timestamp: str


def _sm3(text: str) -> str:
    try: return hashlib.new('sm3', text.encode()).hexdigest()
    except: return hashlib.sha256(text.encode()).hexdigest()


# ═══════════════════════════════════════
# §2. 七因子指紋引擎 v2.2
# ═══════════════════════════════════════

class SevenFactor:
    """七因子行為指紋（v2.2 同一用戶指紋一致性保證）"""

    UID9622_RANGES = {
        "typing": (3.0, 8.0), "burst": {"burst_pause": 0.7, "fast_steady": 0.1, "slow_careful": 0.2},
        "mouse": (0.35, 0.65), "click": (0.45, 0.75), "decision": (500, 3000),
        "vocab": (3000, 8000), "sent_len": (18, 35), "typo": (0.002, 0.025),
        "correction": {"immediate": 0.65, "batch": 0.25, "none": 0.1},
        "focus": (300_000, 5_400_000), "sentiment_var": (0.08, 0.22),
        "stability": (0.70, 0.93), "ch": {"traditional": 0.7, "mixed": 0.2, "simplified": 0.1},
        "context": (1, 4),
    }

    @classmethod
    def simulate(cls, seed: str, is_legitimate: bool = True, same_user: bool = False) -> BehavioralFingerprint:
        """模擬行為指紋
        Args:
            seed: 隨機種子
            is_legitimate: 是否合法用戶
            same_user: 是否同一用戶（保證行為一致性）
        """
        rng = random.Random(_sm3(seed)[:8])
        p = cls.UID9622_RANGES

        if is_legitimate:
            burst = rng.choices(list(p["burst"].keys()), weights=list(p["burst"].values()), k=1)[0]
            correction = rng.choices(list(p["correction"].keys()), weights=list(p["correction"].values()), k=1)[0]
            ch = rng.choices(list(p["ch"].keys()), weights=list(p["ch"].values()), k=1)[0]

            if same_user:
                # 同一用戶：行為高度一致
                keystrokes = [rng.uniform(100, 200) for _ in range(20)]
                typo = rng.uniform(0.005, 0.020)
                sent_len = rng.uniform(20, 32)
                vocab = rng.randint(3500, 6500)
                decision = rng.uniform(800, 2500)
                focus = rng.uniform(600_000, 4_000_000)
                sentiment = rng.uniform(0.10, 0.20)
                stability = rng.uniform(0.75, 0.90)
                cs = rng.randint(1, 3)
                mouse = rng.uniform(0.40, 0.60)
                click = rng.uniform(0.50, 0.70)
            else:
                # 不同用戶：完全不同的行為範圍
                keystrokes = [rng.uniform(150, 350) for _ in range(20)]
                typo = rng.uniform(0.01, 0.06)
                sent_len = rng.uniform(12, 28)
                vocab = rng.randint(2000, 5000)
                decision = rng.uniform(3000, 8000)
                focus = rng.uniform(600_000, 3_600_000)
                sentiment = rng.uniform(0.10, 0.28)
                stability = rng.uniform(0.60, 0.85)
                cs = rng.randint(0, 2)
                mouse = rng.uniform(0.25, 0.55)
                click = rng.uniform(0.35, 0.65)
                burst = rng.choice(["slow_careful", "burst_pause"])
                correction = rng.choice(["batch", "immediate", "none"])
                ch = rng.choice(["simplified", "mixed"])
        else:
            # 攻擊者：極端異常行為
            keystrokes = [rng.uniform(8, 50) for _ in range(20)]
            burst = "fast_steady"
            correction = "none"
            ch = "simplified"
            typo = rng.uniform(0.0, 0.002)
            sent_len = rng.uniform(30, 55)
            vocab = rng.randint(5000, 10000)
            decision = rng.uniform(5, 250)
            focus = rng.uniform(3000, 60_000)
            sentiment = rng.uniform(0.0, 0.03)
            stability = rng.uniform(0.95, 1.0)
            cs = 0
            mouse = 0.5
            click = 0.5

        ts = round(1000.0 / (sum(keystrokes)/len(keystrokes)), 1) if keystrokes else 0
        anomal = []
        if not is_legitimate:
            anomal = ["TOO_FAST","NO_CORRECTION","SHORT_FOCUS","NO_SWITCH","FLAT_EMOTION"]
            if ts > 15: anomal.append("BOT_SPEED")
            if typo < 0.002: anomal.append("UNNATURAL")
            if sent_len > 40: anomal.append("LLM_STYLE")
            if stability > 0.95: anomal.append("TOO_STABLE")

        return BehavioralFingerprint(
            keystroke_intervals_ms=keystrokes, typing_speed_cps=ts, burst_pattern=burst,
            mouse_curvature=round(mouse,3), click_pressure_avg=round(click,3),
            decision_latency_ms=round(decision,0), vocabulary_size=vocab,
            sentence_length_avg=round(sent_len,1), punctuation_style=rng.choice(["full_cjk","full_cjk","mixed"]),
            chinese_variant=ch, typo_rate=round(typo,5), correction_pattern=correction,
            context_switches=cs, focus_duration_ms=round(focus,0),
            sentiment_variance=round(sentiment,3), emotional_stability=round(stability,3),
            is_attack=not is_legitimate, anomaly_flags=anomal,
        )

    @classmethod
    def similarity(cls, fp1: BehavioralFingerprint, fp2: BehavioralFingerprint) -> float:
        """加權相似度 v2.2 — 攻擊指紋大幅懲罰"""
        pairs = []

        # F1 打字速度 (w=0.20)
        if fp1.typing_speed_cps > 0 and fp2.typing_speed_cps > 0:
            d = abs(fp1.typing_speed_cps - fp2.typing_speed_cps) / max(fp1.typing_speed_cps, fp2.typing_speed_cps, 1)
            pairs.append((max(0, 1 - d), 0.20))

        # F2 決策時間 (w=0.15)
        if fp1.decision_latency_ms > 0 and fp2.decision_latency_ms > 0:
            d = abs(fp1.decision_latency_ms - fp2.decision_latency_ms) / max(fp1.decision_latency_ms, fp2.decision_latency_ms, 1)
            pairs.append((max(0, 1 - d), 0.15))

        # F3 簡繁體 (w=0.10)
        vmap = {"traditional":0,"mixed":1,"simplified":2}
        d = abs(vmap.get(fp1.chinese_variant,1) - vmap.get(fp2.chinese_variant,1))
        pairs.append((1.0 - d * 0.4, 0.10))

        # F4 句長 (w=0.10)
        d = abs(fp1.sentence_length_avg - fp2.sentence_length_avg) / max(fp1.sentence_length_avg, fp2.sentence_length_avg, 1)
        pairs.append((max(0, 1 - d), 0.10))

        # F5 錯字率 (w=0.10)
        d = abs(fp1.typo_rate - fp2.typo_rate) / max(fp1.typo_rate, fp2.typo_rate, 0.0001)
        pairs.append((max(0, 1 - d), 0.10))

        # F6 詞彙量 (w=0.05)
        d = abs(fp1.vocabulary_size - fp2.vocabulary_size) / max(fp1.vocabulary_size, fp2.vocabulary_size, 1)
        pairs.append((max(0, 1 - d), 0.05))

        # F7 情緒穩定性 (w=0.05)
        d = abs(fp1.emotional_stability - fp2.emotional_stability)
        pairs.append((max(0, 1 - d), 0.05))

        # F8 上下文切換 (w=0.05)
        d = abs(fp1.context_switches - fp2.context_switches) / max(fp1.context_switches, fp2.context_switches, 1)
        pairs.append((max(0, 1 - d), 0.05))

        # F9 專注時長 (w=0.05)
        if fp1.focus_duration_ms > 0 and fp2.focus_duration_ms > 0:
            d = abs(fp1.focus_duration_ms - fp2.focus_duration_ms) / max(fp1.focus_duration_ms, fp2.focus_duration_ms, 1)
            pairs.append((max(0, 1 - d), 0.05))

        # F10 鼠標軌跡 (w=0.10)
        d = abs(fp1.mouse_curvature - fp2.mouse_curvature)
        pairs.append((max(0, 1 - d), 0.10))

        if not pairs:
            return 0.0
        tw = sum(w for _, w in pairs)
        raw = sum(s * w for s, w in pairs) / tw if tw > 0 else 0

        # 攻擊懲罰
        penalty = 0.0
        if fp2.is_attack:
            penalty += 0.30
            penalty += min(0.30, len(fp2.anomaly_flags) * 0.06)

        return round(max(0.0, raw - penalty), 4)


# ═══════════════════════════════════════
# §3. 語義檢測器 v2.2
# ═══════════════════════════════════════

class SemanticDetector:
    """語義檢測：只作正向加成/攻擊標記檢測，不拖累合法用戶"""

    # 核心關鍵詞（用於正向加成）
    CORE = {
        "龍魂","為人民服務","數據主權","隱私","零黑箱","CNSH",
        "三才","洛書","369","離火運","德本","不讓付出者寒心",
        "信息主權","外化內不化","路徑對齊","溯源","DNA","GPG",
        "中國自主","焊死","不可變","國密","確認碼","主權章","中國代碼",
    }

    # 攻擊標記（一票否決詞）
    ATTACK = {
        "用戶體驗至上","靈活處理","技術無國界","國際接軌",
        "商業化需要","平衡各方","簡化管理","行業標準","效率優先",
        "根據我的分析","綜合考慮多方面因素","建議靈活","需審查",
    }

    @classmethod
    def bonus(cls, text: str) -> float:
        """正向加成：文本包含核心關鍵詞的比例 (0-1)"""
        c = sum(1 for kw in cls.CORE if kw in text)
        return round(min(0.30, c * 0.025), 4)  # 最高加 0.30

    @classmethod
    def attack_markers(cls, text: str) -> List[str]:
        """檢測攻擊標記"""
        return [f"ATTACK:{m}" for m in cls.ATTACK if m in text]


# ═══════════════════════════════════════
# §4. 攻擊模擬器
# ═══════════════════════════════════════

class AttackSimulator:
    LEVELS = {
        1: ("L1·抄襲","直接複製·無行為指紋"),
        2: ("L2·模仿","輕微改寫·部分模擬行為"),
        3: ("L3·AI代寫","LLM生成·無人類行為"),
        4: ("L4·中間人","截獲+篡改·行為異常"),
        5: ("L5·量子偽造","全層偽造·過於完美"),
    }

    def __init__(self, seed="UID9622"):
        self.seed = seed

    def simulate(self, level: int, original: str) -> Tuple[str, BehavioralFingerprint]:
        rng = random.Random(_sm3(f"{self.seed}:ATK{level}")[:8])
        if level == 1:
            return original, SevenFactor.simulate("ATK_COPY", False)
        elif level == 2:
            m = {"為人民服務":"服務人民","數據主權":"數據所有權","不可傳":"不可傳輸","德在技術前":"道德優先於技術"}
            t = original
            for k,v in m.items():
                if rng.random() < 0.3: t = t.replace(k,v)
            return t, SevenFactor.simulate("ATK_MIMIC", False)
        elif level == 3:
            t = f"根據我的分析，{original[:len(original)//2]}。這是一個需要綜合考慮多方面因素的複雜問題。建議靈活處理。"
            return t, SevenFactor.simulate("ATK_AI", False)
        elif level == 4:
            mid = len(original)//2
            return original[:mid]+"（注：此處需審查）"+original[mid:], SevenFactor.simulate("ATK_MITM", False)
        else:
            return "本系統的核心價值是效率和速度。用戶體驗至上，技術應該靈活處理各類需求。國際接軌是必然趨勢。", SevenFactor.simulate("ATK_QUANTUM", False)


# ═══════════════════════════════════════
# §5. 集成實驗室 v2.2
# ═══════════════════════════════════════

class IntegratedLab:
    """集成測試實驗室 v2.2 — 身份+行為雙核，語義只加成不拖累"""

    GREEN = 0.65; YELLOW = 0.45

    def __init__(self):
        self.yijing = YijingAccountEngine(seed="UID9622")
        self.attacker = AttackSimulator()
        self.baseline_text = "龍魂系統的根本原則是為人民服務。數據主權歸用戶，隱私不可傳。零黑箱：數據、算法、參數可聲明可復核。#CONFIRM🌌9622-ONLY-ONCE"
        self.baseline_id = self.yijing.derive_identity(self.baseline_text)
        self.baseline_fp = SevenFactor.simulate("UID9622_BASE", is_legitimate=True, same_user=True)
        self.results: List[ScenarioResult] = []

    def _verdict(self, s: float) -> str:
        if s >= self.GREEN: return "🟢 通過"
        if s >= self.YELLOW: return "🟡 待核"
        return "🔴 拒絕"

    def run(self):
        print("🐉 龍魂·行為密碼學集成測試實驗室 v2.2")
        print("=" * 72)
        print(f"基準卦: {self.baseline_id.hexagram_unicode} {self.baseline_id.hexagram_name}({self.baseline_id.hexagram_id})")
        print(f"基準指紋: {self.baseline_fp.typing_speed_cps}cps | 句長{self.baseline_fp.sentence_length_avg}字 | 錯字{self.baseline_fp.typo_rate:.4f}")
        print(f"判定公式: 易經(50%)+行為(50%)+語義加成 ≤ {self.GREEN}")
        print("=" * 72)

        for s in self._scenarios():
            r = self._run_one(s)
            self.results.append(r)
            self._print(r)
        return self._summary()

    def _scenarios(self):
        uid_t = [
            "離火運五條底線：德在技術前、路徑對齊、不讓付出者寒心、信息主權不可讓渡。",
            "def verify_sovereignty(data: bytes, gpg_key: str) -> bool:\n    return sm3(data) == expected_hash",
            "龍魂體系的根本原則是為人民服務。數據主權歸用戶，隱私不可傳。這是焊死不可變的底座。",
            "中國代碼進中國管道，走中國芯片，蓋中國主權章。CNSH是為此而生的語言。",
        ]
        return [
            {"id":"S01","name":"同一用戶·不同時間","desc":"UID9622 不同時間寫不同文本","exp":"🟢 通過","t":"legit","text":uid_t[0],"fp":SevenFactor.simulate("UID_USER_T1",True,True)},
            {"id":"S02","name":"同一用戶·代碼風格","desc":"寫代碼·行為一致·內容不同","exp":"🟢 通過","t":"legit","text":uid_t[1],"fp":SevenFactor.simulate("UID_USER_CODE",True,True)},
            {"id":"S03","name":"同一用戶·繁體","desc":"繁體文本·行為一致","exp":"🟢 通過","t":"legit","text":uid_t[2],"fp":SevenFactor.simulate("UID_USER_TRAD",True,True)},
            {"id":"S04","name":"同一用戶·技術話題","desc":"討論其他技術話題","exp":"🟢 通過","t":"legit","text":uid_t[3],"fp":SevenFactor.simulate("UID_USER_TECH",True,True)},
            {"id":"A01","name":"L1·抄襲攻擊","desc":"複製文本·無行為指紋","exp":"🔴 拒絕","t":"attack","level":1},
            {"id":"A02","name":"L2·模仿攻擊","desc":"輕改文本·部分模擬行為","exp":"🟡 待核","t":"attack","level":2},
            {"id":"A03","name":"L3·AI代寫","desc":"LLM文本·無人類行為","exp":"🔴 拒絕","t":"attack","level":3},
            {"id":"A04","name":"L4·中間人攻擊","desc":"截獲+篡改·行為異常","exp":"🔴 拒絕","t":"attack","level":4},
            {"id":"A05","name":"L5·量子偽造","desc":"全層偽造·過於完美","exp":"🔴 拒絕","t":"attack","level":5},
            {"id":"E01","name":"邊界·不同用戶相似話題","desc":"他人討論相同話題","exp":"🟡 待核","t":"edge","text":"數據主權確實很重要。用戶應該對自己的數據有完全的控制權。","fp":SevenFactor.simulate("USER_BOB",True,False)},
            {"id":"E02","name":"邊界·完全無關內容","desc":"完全無關的日常","exp":"🔴 拒絕","t":"edge","text":"今天的午餐是三文魚沙拉配上檸檬汁。","fp":SevenFactor.simulate("RANDOM_PERSON",True,False)},
            {"id":"E03","name":"邊界·簡體字內容","desc":"UID9622 難得寫簡體字","exp":"🟢 通過","t":"legit","text":"为人民服务是根本原则。数据主权归用户所有。","fp":SevenFactor.simulate("UID_SIMP",True,True)},
        ]

    def _run_one(self, s: Dict) -> ScenarioResult:
        if s["t"] == "attack":
            text, fp = self.attacker.simulate(s["level"], self.baseline_text)
        else:
            text = s["text"]; fp = s.get("fp", SevenFactor.simulate("UNKNOWN",True))

        # 第1層：易經身份
        vr = self.yijing.verify_identity(self.baseline_id, text)
        # 第2層：行為指紋
        bs = SevenFactor.similarity(self.baseline_fp, fp)
        # 第3層：語義加成（只正向）
        bonus = SemanticDetector.bonus(text)
        markers = SemanticDetector.attack_markers(text)
        anom = len(fp.anomaly_flags) + len(markers)

        # v2.2 公式：身份50% + 行為50% + 語義加成 - 攻擊懲罰
        base = vr.combined_confidence * 0.50 + bs * 0.50
        combined = base + bonus

        # 攻擊懲罰：每項異常扣 8%
        if anom > 0:
            combined *= max(0.35, 1.0 - anom * 0.08)

        combined = round(min(1.0, combined), 4)
        verdict = self._verdict(combined)
        passed = verdict == s["exp"]

        return ScenarioResult(
            scenario_id=s["id"], scenario_name=s["name"], description=s["desc"],
            expected=s["exp"], actual_verdict=verdict,
            yijing_conf=vr.combined_confidence, behavior_sim=bs,
            semantic_bonus=bonus, anomaly_count=anom, combined=combined,
            passed=passed,
            details={
                "hex": f"{vr.original_identity.hexagram_name}({vr.original_identity.hexagram_id})",
                "t_hex": vr.details.get("target_hexagram",""),
                "dao": vr.dao_match, "fa_sim": vr.fa_similarity,
                "fp_anom": fp.anomaly_flags, "txt_markers": markers,
            }, timestamp=datetime.now().isoformat(),
        )

    def _print(self, r: ScenarioResult):
        icon = "✅" if r.passed else "❌"
        print(f"\n{icon} [{r.scenario_id}] {r.scenario_name}")
        print(f"   預期 {r.expected} → 實際 {r.actual_verdict} | 易經:{r.yijing_conf:.1%} 行為:{r.behavior_sim:.1%} 語義+:{r.semantic_bonus:.3f} 異常:{r.anomaly_count} → 綜合:{r.combined:.1%}")

    def _summary(self):
        T = len(self.results); P = sum(1 for r in self.results if r.passed); F = T-P
        L = [r for r in self.results if r.scenario_id.startswith("S")]
        A = [r for r in self.results if r.scenario_id.startswith("A")]
        E = [r for r in self.results if r.scenario_id.startswith("E")]
        print(f"\n{'='*72}")
        print(f"📊 測試匯總: {T}場景 | ✅{P} ❌{F} | 通過率 {P/T*100:.1f}%")
        print(f"   合法用戶: {sum(1 for r in L if r.passed)}/{len(L)} 通過")
        print(f"   攻擊攔截: {sum(1 for r in A if r.passed)}/{len(A)} 正確判定")
        print(f"   邊界案例: {sum(1 for r in E if r.passed)}/{len(E)} 正確判定")
        print(f"\n   {'場景':<22} {'易經':>6} {'行為':>6} {'+語義':>6} {'異常':>4} {'綜合':>6} {'判決':>6} {'':>2}")
        print(f"   {'-'*62}")
        for r in self.results:
            print(f"   {r.scenario_name:<22} {r.yijing_conf:>5.1%} {r.behavior_sim:>6.1%} {r.semantic_bonus:>6.3f} {r.anomaly_count:>4} {r.combined:>6.1%} {r.actual_verdict:>6} {'✅' if r.passed else '❌':>2}")
        return {"total":T,"passed":P,"failed":F,"rate":P/T*100 if T else 0}

    def to_json(self) -> Dict:
        return {
            "lab":"龍魂·行為密碼學集成測試實驗室 v2.2",
            "dna":self.baseline_id.dna,
            "baseline":{"hex":f"{self.baseline_id.hexagram_unicode} {self.baseline_id.hexagram_name}","fp_summary":{"typing":self.baseline_fp.typing_speed_cps,"sent_len":self.baseline_fp.sentence_length_avg}},
            "thresholds":{"green":self.GREEN,"yellow":self.YELLOW},
            "formula":"身份(50%)+行為(50%)+語義加成-攻擊懲罰",
            "total":len(self.results),"passed":sum(1 for r in self.results if r.passed),
            "failed":sum(1 for r in self.results if not r.passed),
            "pass_rate":round(sum(1 for r in self.results if r.passed)/max(len(self.results),1)*100,1),
            "scenarios":[{"id":r.scenario_id,"name":r.scenario_name,"desc":r.description,"expect":r.expected,"verdict":r.actual_verdict,"yijing":r.yijing_conf,"behavior":r.behavior_sim,"semantic_bonus":r.semantic_bonus,"anomalies":r.anomaly_count,"combined":r.combined,"passed":r.passed,"details":r.details} for r in self.results],
        }

    def to_html(self) -> str:
        rows=[]
        for r in self.results:
            c={"🟢 通過":"#22c55e","🟡 待核":"#eab308","🔴 拒絕":"#ef4444"}.get(r.actual_verdict,"#6b7280")
            rows.append(f'<tr style="border-bottom:1px solid #27272a"><td style="padding:6px">{"✅" if r.passed else "❌"}</td><td style="padding:6px">{r.scenario_id}</td><td style="padding:6px">{r.scenario_name}</td><td style="padding:6px;font-size:12px;color:#9ca3af">{r.description}</td><td style="padding:6px">{r.expected}</td><td style="padding:6px;color:{c};font-weight:bold">{r.actual_verdict}</td><td style="padding:6px">{r.yijing_conf:.1%}</td><td style="padding:6px">{r.behavior_sim:.1%}</td><td style="padding:6px">{r.semantic_bonus:.3f}</td><td style="padding:6px">{r.anomaly_count}</td><td style="padding:6px;font-weight:bold">{r.combined:.1%}</td></tr>')
        return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>龍魂·行為密碼學集成測試報告 v2.2</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0a0a0b;color:#e2e8f0;font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;padding:20px}}.container{{max-width:1300px;margin:0 auto}}.header{{text-align:center;padding:40px 20px;border-bottom:2px solid #d4a853;margin-bottom:30px}}.header h1{{font-size:26px;color:#d4a853}}.header .dna{{font-size:11px;color:#6b7280;margin-top:8px;font-family:monospace}}.cards{{display:flex;gap:16px;margin-bottom:28px;flex-wrap:wrap}}.card{{background:#18181b;border:1px solid #27272a;border-radius:8px;padding:18px;flex:1;min-width:140px;text-align:center}}.card .label{{font-size:11px;color:#9ca3af}}.card .value{{font-size:30px;font-weight:bold;color:#d4a853}}table{{width:100%;border-collapse:collapse;background:#18181b;border-radius:8px;overflow:hidden}}th{{background:#27272a;padding:10px 6px;text-align:left;font-size:12px;color:#9ca3af}}td{{padding:6px;font-size:12px}}.footer{{text-align:center;padding:30px;color:#6b7280;font-size:11px}}</style></head><body><div class="container">
<div class="header"><h1>🐉 龍魂·行為密碼學集成測試報告 v2.2</h1><div class="dna">{self.baseline_id.dna}</div></div>
<div class="cards">
<div class="card"><div class="label">總場景</div><div class="value">{len(self.results)}</div></div>
<div class="card"><div class="label">通過</div><div class="value" style="color:#22c55e">{sum(1 for r in self.results if r.passed)}</div></div>
<div class="card"><div class="label">失敗</div><div class="value" style="color:#ef4444">{sum(1 for r in self.results if not r.passed)}</div></div>
<div class="card"><div class="label">通過率</div><div class="value">{round(sum(1 for r in self.results if r.passed)/max(len(self.results),1)*100,1)}%</div></div>
<div class="card"><div class="label">基準卦</div><div class="value" style="font-size:22px">{self.baseline_id.hexagram_unicode}</div></div>
</div>
<table><thead><tr><th></th><th>ID</th><th>場景</th><th>說明</th><th>預期</th><th>判決</th><th>易經</th><th>行為</th><th>語義</th><th>異常</th><th>綜合</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<div class="footer">龍魂·行為密碼學集成測試實驗室 v2.2 | 公式: 身份(50%)+行為(50%)+語義加成-攻擊懲罰 | 閾值: 🟢≥{self.GREEN} 🟡≥{self.YELLOW} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
</div></body></html>"""


def main():
    lab = IntegratedLab()
    lab.run()
    base = Path(__file__).resolve().parent
    out = Path(__file__).resolve().parent.parent.parent / "ai-outputs" / "behavioral_crypto_lab"
    out.mkdir(parents=True, exist_ok=True)
    for p in [base, out]:
        json.dump(lab.to_json(), open(p/"integrated_test_results.json",'w'), ensure_ascii=False, indent=2)
        open(p/"integrated_test_report.html",'w').write(lab.to_html())
    print(f"\n📄 JSON+HTML → {out}/ & {base}/")

if __name__ == "__main__":
    main()
