#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 冲突仲裁引擎 v2.0（事实级仲裁 · 实测修复版）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

v1.0 → v2.0：余弦相似度主判 → 实体抽取 + 断言归一化 + 矛盾检测
本版对设计稿的额外修复（实测驱动）：
  R1 抽取：笛卡尔积误配 → 按位置就近配对（主语→其后最近谓语→其后最近宾语）
  R2 新增极性检测：不/未/禁止/不得 → polarity=NEG，同值不同极性也算🔴冲突
  R3 冲突去重：按 (主语,谓语) 聚合成"取值阵营"，不再 O(n²) 刷AI对
  R4 相似度：sentence_transformers 缺失时自动降级纯stdlib词袋余弦（辅助信号永可用）
  R5 DNA：手写生辰干支=🔴违规 → 一律走 dna_trace.生成DNA() 算法签名
  R6 覆盖率信号：仅单个AI对某(主语,谓语)作证 → 🟡 提示（可能是漏报源）
"""

import re
import sys
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

# --- DNA 算法签名（禁止手写干支） ---
try:
    sys.path.insert(0, "/mnt/agents/output/龍魂低算力内核/core")
    from longhun_core.dna_trace import 生成DNA, 短身份码
    _DNA_OK = True
except Exception:
    _DNA_OK = False
    def 生成DNA(标识, date=None):
        return f"#龍芯⚡️FALLBACK-{hashlib.md5(标识.encode()).hexdigest()[:8].upper()}-UID9622"
    def 短身份码(s):
        return hashlib.md5(s.encode()).hexdigest()[:8].upper()

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# 1. 实体抽取器（位置就近配对版）
# ============================================================

class EntityExtractor:
    SUBJECTS = ["用户数据", "数据主权", "本地存储", "云端存储", "用户隐私",
                "主权归属", "法律管辖", "行为记录", "DNA追溯码", "三色审计",
                "史官记录", "耻辱墙", "P0协议", "数字身份", "操作记录"]
    PREDICATES = ["存储于", "存储在", "保存于", "存放于", "归属", "归属于", "属于", "归",
                  "适用", "遵守", "遵循", "记录于", "写入", "记入", "存档于",
                  "追溯至", "追踪到", "审计于", "保护", "托管", "授权"]
    OBJECTS = ["本地设备", "本地终端", "本地", "云端服务器", "云端", "云上",
               "用户", "国家", "国家法律", "法律", "龙魂系统", "区块链",
               "数据库", "终端设备", "终端", "服务器", "史官系统"]
    NEGATIONS = ["不得", "禁止", "不可", "不允许", "不应", "不能", "不", "未", "勿"]

    def __init__(self):
        # 长词优先，避免"本地"抢先匹配掉"本地设备"
        def pat(words):
            return re.compile('(' + '|'.join(sorted(words, key=len, reverse=True)) + ')')
        self.ps, self.pp, self.po = pat(self.SUBJECTS), pat(self.PREDICATES), pat(self.OBJECTS)

    def extract(self, text: str) -> List[Dict]:
        claims = []
        for sent in re.split(r'[。！？!?\n\r；;]+', text):
            sent = sent.strip()
            if not sent:
                continue
            for sm in self.ps.finditer(sent):
                # 主语之后最近的谓语
                pm = self.pp.search(sent, sm.end())
                if not pm:
                    continue
                # 谓语之后最近的宾语
                om = self.po.search(sent, pm.end())
                if not om:
                    continue
                # 极性窗口：谓语前6字内是否出现否定词
                window = sent[max(0, pm.start() - 6):pm.start()]
                polarity = "NEG" if any(n in window for n in self.NEGATIONS) else "POS"
                claims.append({
                    "subject": sm.group(), "predicate": pm.group(),
                    "object": om.group(), "polarity": polarity,
                    "raw": sent,
                })
        return claims

# ============================================================
# 2. 断言归一化器
# ============================================================

class AssertionNormalizer:
    PRED_SYN = {
        "存储于": ["存储在", "保存于", "存放于"],
        "归属": ["归属于", "属于", "归"],
        "适用": ["遵守", "遵循"],
        "记录于": ["写入", "记入", "存档于"],
        "追溯至": ["追踪到"],
    }
    OBJ_SYN = {
        "本地": ["本地设备", "本地终端", "终端", "终端设备"],
        "云端": ["云端服务器", "云上", "服务器"],
        "国家": ["国家法律"],
        "龙魂系统": ["史官系统"],
    }

    def normalize(self, claims: List[Dict]) -> List[Dict]:
        out = []
        for c in claims:
            out.append({
                "subject": c["subject"],
                "predicate": self._map(c["predicate"], self.PRED_SYN),
                "object": self._map(c["object"], self.OBJ_SYN),
                "polarity": c["polarity"],
                "raw": c["raw"],
            })
        return out

    @staticmethod
    def _map(word, table):
        for canon, syns in table.items():
            if word == canon or word in syns:
                return canon
        return word

# ============================================================
# 3. 矛盾检测器（阵营聚合 + 极性）
# ============================================================

@dataclass
class Conflict:
    subject: str
    predicate: str
    camps: Dict[str, List[str]]   # 取值 → [AI名单]
    polarity_split: bool
    severity: str
    evidence: Dict[str, str]      # AI → 原句

class ContradictionDetector:
    def detect(self, claims_by_ai: Dict[str, List[Dict]]):
        grouped = defaultdict(dict)  # (s,p) → ai → (object, polarity, raw)
        for ai, claims in claims_by_ai.items():
            for c in claims:
                grouped[(c["subject"], c["predicate"])][ai] = (c["object"], c["polarity"], c["raw"])

        conflicts, gaps = [], []
        for (s, p), ai_map in grouped.items():
            if len(ai_map) < 2:
                only = next(iter(ai_map.items()))
                gaps.append({"subject": s, "predicate": p, "only_ai": only[0],
                             "note": "🟡 仅单个AI作证，无交叉验证"})
                continue
            camps = defaultdict(list)
            polarities = set()
            evidence = {}
            for ai, (obj, pol, raw) in ai_map.items():
                camps[obj].append(ai)
                polarities.add(pol)
                evidence[ai] = raw
            if len(camps) > 1 or len(polarities) > 1:
                conflicts.append(Conflict(
                    subject=s, predicate=p, camps=dict(camps),
                    polarity_split=len(polarities) > 1,
                    severity="🔴", evidence=evidence,
                ))
        return conflicts, gaps

# ============================================================
# 4. 相似度辅助信号（纯stdlib兜底，永远可用）
# ============================================================

class SimilarityHelper:
    def __init__(self):
        self.backend = "bag-of-words(stdlib)"
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.backend = "sentence-transformers"
        except Exception:
            pass

    @staticmethod
    def _vec(text):
        v = defaultdict(float)
        for tok in re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z0-9_]+|[\u4e00-\u9fff]', text):
            v[tok] += 1.0
        return v

    @staticmethod
    def _cos(a, b):
        dot = sum(a[k] * b.get(k, 0) for k in a)
        na = sum(x * x for x in a.values()) ** 0.5
        nb = sum(x * x for x in b.values()) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    def compute(self, texts: List[str], names: List[str]) -> Dict:
        sims = []
        if self.model is not None:
            import numpy as np
            emb = self.model.encode(texts)
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    sims.append({"ai_a": names[i], "ai_b": names[j],
                                 "similarity": float(np.dot(emb[i], emb[j]) /
                                 (np.linalg.norm(emb[i]) * np.linalg.norm(emb[j])))})
        else:
            vecs = [self._vec(t) for t in texts]
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    sims.append({"ai_a": names[i], "ai_b": names[j],
                                 "similarity": round(self._cos(vecs[i], vecs[j]), 4)})
        for s in sims:
            s["note"] = "⚠️ 仅为差异提示，不作为冲突判定依据"
        return {"backend": self.backend, "similarities": sims,
                "disclaimer": "相似度仅表示措辞接近程度，不代表事实一致性"}

# ============================================================
# 5. 主仲裁器 v2.0
# ============================================================

class ConflictArbiterV2:
    def __init__(self, date=None, llm_hook=None):
        """llm_hook: 可插拔LLM断言抽取器，签名 f(text)->List[{subject,predicate,object,polarity?,raw?}]
        返回None/异常 → 自动回退规则抽取（断网可跑铁律）"""
        self.extractor = EntityExtractor()
        self.normalizer = AssertionNormalizer()
        self.detector = ContradictionDetector()
        self.similarity = SimilarityHelper()
        self.llm_hook = llm_hook
        self.dna = 生成DNA("CONFLICT-ARBITER-V2", date)

    def _抽取(self, text: str) -> List[Dict]:
        if self.llm_hook is not None:
            try:
                claims = self.llm_hook(text)
                if claims:
                    for c in claims:
                        c.setdefault("polarity", "POS")
                        c.setdefault("raw", text.strip()[:80])
                    return claims
            except Exception:
                pass  # 静默回退规则抽取
        return self.extractor.extract(text)

    def analyze(self, ai_responses: Dict[str, str]) -> Dict:
        claims_by_ai = {ai: self._抽取(t) for ai, t in ai_responses.items()}
        normed = {ai: self.normalizer.normalize(c) for ai, c in claims_by_ai.items()}
        conflicts, gaps = self.detector.detect(normed)
        names = list(ai_responses.keys())
        sim_report = self.similarity.compute(list(ai_responses.values()), names)

        tricolor = "🔴" if conflicts else ("🟡" if gaps else "🟢")
        return {
            "dna": self.dna, "confirm": CONFIRM, "gpg": GPG,
            "timestamp": datetime.now().isoformat(),
            "tricolor": tricolor,
            "_normed": normed,
            "conflicts": [{
                "subject": c.subject, "predicate": c.predicate,
                "camps": c.camps, "polarity_split": c.polarity_split,
                "severity": c.severity, "evidence": c.evidence,
            } for c in conflicts],
            "coverage_gaps": gaps,
            "similarity_auxiliary": sim_report,
            "summary": {
                "total_claims": sum(len(c) for c in normed.values()),
                "conflicts_found": len(conflicts),
                "coverage_gaps": len(gaps),
                "conflict_pairs": sorted({tuple(sorted([a, b]))
                                          for c in conflicts
                                          for ais in c.camps.values() for a in ais
                                          for b in {x for v in c.camps.values() for x in v} - {a}}),
            },
        }

    def render(self, result: Dict) -> str:
        L = [f"\n🐉 冲突仲裁 v2.0 报告 · {result['tricolor']}", "=" * 56]
        if result["conflicts"]:
            L.append(f"🔴 事实冲突 {len(result['conflicts'])} 项：")
            for c in result["conflicts"]:
                camps = " vs ".join(f"{obj}（{'/'.join(ais)}）" for obj, ais in c["camps"].items())
                pol = " ＋极性分裂" if c["polarity_split"] else ""
                L.append(f"  📌 {c['subject']}·{c['predicate']}：{camps}{pol}")
        else:
            L.append("✅ 未发现事实级冲突")
        for g in result["coverage_gaps"]:
            L.append(f"  {g['note']}：{g['subject']}·{g['predicate']}（仅 {g['only_ai']}）")
        L.append(f"辅助信号后端: {result['similarity_auxiliary']['backend']}"
                 f"（{result['similarity_auxiliary']['disclaimer']}）")
        L.append(f"断言 {result['summary']['total_claims']} 条 · 冲突 {result['summary']['conflicts_found']} 项")
        L.append(f"🧬 {result['dna']}")
        return "\n".join(L)
