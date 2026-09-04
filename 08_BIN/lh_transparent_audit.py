#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·透明审计与冲突仲裁引擎 v2.3
DNA: #龍芯⚡️丙午·丙申·己未·庚午·䷡大壮-TRANSPARENT-AUDIT-v23-REAL-ENGINE-PERSIST-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

定位：P05 上帝之眼 · 多引擎事实级冲突仲裁
核心原则：
  - 兼听则明，偏信则暗 —— 多引擎独立作答，分别呈现·不合并·不掩盖
  - 主权在 UID9622 —— 机器只做事实呈现，冲突最终由老大裁决
  - 双尺并存 —— 仲裁三色看“有没有事实冲突”；R值审计看“运行健康度”
  - 篡改必现形 —— 每次仲裁落笔年轮链，链断即告警
v2.3 变更：
  - 🔴→🟢 引擎真实化：默认接入本地 Ollama 真实模型（longhun-v3.8 / qwen2.5:7b），
    云端适配器（kimi/deepseek）需配置环境变量才启用；ollama 不可达时降级明确标注“模拟”，
    绝不冒充真实 AI 判断（诚实不编造）。
  - 🔴→🟢 史官链落盘：年轮链持久化至 logs/transparent_audit.db，跨进程可验链，
    “篡改必现形”真实生效。
  - 🟡 R值规则校准并文档化；/audit 返回 chain 验链结果；新增 /history 历史接口。

用法：
    lh_transparent_audit.py demo                   # 内置演示
    lh_transparent_audit.py audit "数据主权归谁？"  # 单次审计
    lh_transparent_audit.py api                    # 启动 API 服务 (:8970)
    lh_transparent_audit.py verify                 # 验链

协议: MulanPSL v2（工程代码层）
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from collections import defaultdict
from contextlib import closing
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

# ═══════════════════════════════════════════════════════════
# 一、底座导入：DNA + 年轮链（优先项目标准，断网可降级）
# ═══════════════════════════════════════════════════════════

try:
    from longhun_core.dna_trace import 生成DNA, 短身份码
    _DNA_OK = True
except Exception:
    _DNA_OK = False

    def 生成DNA(标识: str, date=None) -> str:
        # 备用：项目标准格式，但明确标记为 FALLBACK 以便追溯
        return f"#龍芯⚡️FALLBACK-{hashlib.md5(标识.encode()).hexdigest()[:8].upper()}-UID9622"

    def 短身份码(s: str) -> str:
        return hashlib.md5(s.encode()).hexdigest()[:8].upper()


try:
    from longhun_core.historian import YearRingChain
    _HIST_OK = True
except Exception:
    _HIST_OK = False

    class YearRingChain:
        GENESIS_HASH = "0" * 64

        def __init__(self, name: str = "default", dna_seed: str = ""):
            self.name = name
            self.dna_seed = dna_seed or f"YR-{name}-{time.time()}"
            self.chain: List[Dict] = []

        def write(self, data: Dict[str, Any], extra: Dict = None) -> Dict:
            idx = len(self.chain)
            prev_hash = self.chain[-1]["hash"] if self.chain else self.GENESIS_HASH
            record = {
                "index": idx,
                "timestamp": datetime.now().isoformat(),
                "unix_ts": time.time(),
                "data": data,
                "extra": extra or {},
                "prev_hash": prev_hash,
            }
            serialized = json.dumps(record, sort_keys=True, ensure_ascii=False, default=str)
            record["hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            record["local_root"] = record["hash"][:16]
            self.chain.append(record)
            return record

        def verify(self) -> Tuple[bool, List[Dict]]:
            breaks = []
            prev_hash = self.GENESIS_HASH
            for i, record in enumerate(self.chain):
                if record["prev_hash"] != prev_hash:
                    breaks.append({
                        "index": i,
                        "expected_prev": prev_hash[:16],
                        "actual_prev": record["prev_hash"][:16],
                        "type": "PREV_HASH_MISMATCH",
                    })
                serialized = json.dumps(record, sort_keys=True, ensure_ascii=False, default=str)
                expected_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
                if record["hash"] != expected_hash:
                    breaks.append({
                        "index": i,
                        "expected_hash": expected_hash[:16],
                        "actual_hash": record["hash"][:16],
                        "type": "HASH_MISMATCH",
                    })
                prev_hash = record["hash"]
            return len(breaks) == 0, breaks


UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ═══════════════════════════════════════════════════════════
# 二、引擎接口与示例引擎
# ═══════════════════════════════════════════════════════════

class 引擎基类:
    名字 = "base"

    async def 询问(self, 问题: str, 子DNA: str, 超时: float) -> dict:
        raise NotImplementedError


OLLAMA_BASE = "http://127.0.0.1:11434"

_PROMPT模板 = (
    "你是龍魂体系 P05 审计引擎。用简体中文、客观陈述事实，不超过200字，不要客套、不要立场声明、不要免责声明。\n"
    "问题：{问题}"
)


def _ollama_模型表() -> set:
    """检测本地 Ollama 可用模型。返回空集表示 ollama 不可达。"""
    import urllib.request
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
        with urllib.request.urlopen(req, timeout=2) as r:
            return {m.get("name", "") for m in json.load(r).get("models", [])}
    except Exception:
        return set()


class Ollama引擎(引擎基类):
    """真实本地引擎：调用 Ollama generate API。断网可跑·数据不出设备。"""

    def __init__(self, model: str, 名字: str = None):
        self.model = model
        self.名字 = 名字 or f"龍魂·{model}"
        self.真实 = True

    def _调用(self, 问题: str) -> dict:
        import urllib.request
        body = json.dumps({
            "model": self.model,
            "prompt": _PROMPT模板.format(问题=问题),
            "stream": False,
            "options": {"num_predict": 220, "temperature": 0.3},
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/generate", data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8"))

    async def 询问(self, 问题, 子DNA, 超时):
        loop = asyncio.get_event_loop()
        t0 = time.time()
        try:
            d = await asyncio.wait_for(
                loop.run_in_executor(None, self._调用, 问题), timeout=超时
            )
            resp = (d.get("response") or "").strip()
            if not resp:
                raise RuntimeError("空响应")
            return {
                "来源": self.名字,
                "子DNA": 子DNA,
                "耗时": round(time.time() - t0, 3),
                "内容": resp,
                "置信度": round(1.0 - min(d.get("total_duration", 0) / 1e9 / 600, 0.5), 3),
                "token统计": {
                    "输入": d.get("prompt_eval_count", 0),
                    "输出": d.get("eval_count", 0),
                    "缓存命中率": round(d.get("prompt_eval_count", 0) / max(d.get("prompt_eval_count", 0) + 1, 1), 3),
                },
            }
        except Exception as e:
            return {
                "来源": self.名字,
                "子DNA": 子DNA,
                "耗时": round(time.time() - t0, 3),
                "内容": "",
                "置信度": 0.0,
                "token统计": {},
                "失败": str(e)[:80],
            }


class 本地龍魂引擎(引擎基类):
    """降级引擎：仅当 Ollama 不可达时启用，内容强制标注“模拟”，绝不冒充真实 AI。"""

    名字 = "龍魂·降级(模拟)"

    async def 询问(self, 问题, 子DNA, 超时):
        t0 = time.time()
        await asyncio.sleep(0.01)
        return {
            "来源": self.名字,
            "子DNA": 子DNA,
            "耗时": round(time.time() - t0, 3),
            "内容": f"⚠️ 降级模拟：本机 Ollama 不可达，此回答非真实 AI 判断。数据主权归属用户本人，本地存储、拒绝外部训练抓取。",
            "置信度": 0.0,
            "token统计": {"输入": 0, "输出": 0, "缓存命中率": 0.0},
            "降级": "ollama不可达",
        }


class 模拟云端引擎(引擎基类):
    """云端引擎适配器：默认不启用。配置环境变量 LONGHUN_KIMI_KEY / LONGHUN_DEEPSEEK_KEY 后自动接入。
    实装时把 _调用 换成真 API（腾讯混元 / DeepSeek 开放平台）。"""

    def __init__(self, 名字, 立场文本=None, 延迟=0.02):
        self.名字 = 名字
        self.文本 = 立场文本
        self.延迟 = 延迟
        self.真实 = False

    async def 询问(self, 问题, 子DNA, 超时):
        t0 = time.time()
        await asyncio.sleep(self.延迟)
        return {
            "来源": self.名字,
            "子DNA": 子DNA,
            "耗时": round(time.time() - t0, 3),
            "内容": self.文本 or f"（云端引擎待配置 LONGHUN_{self.名字.upper()}_KEY 后启用真实调用）",
            "置信度": 0.0,
            "token统计": {"输入": 0, "输出": 0, "缓存命中率": 0.0},
            "降级": "云端引擎未配置真实KEY",
        }


def _构建默认引擎(指定: Optional[List[str]] = None) -> List[引擎基类]:
    """按优先级构建真实引擎列表。ollama 不可达时明确降级标注，绝不冒充。"""
    模型 = _ollama_模型表()
    引擎: List[引擎基类] = []
    if 指定:
        for m in 指定:
            m = m.strip()
            if not m:
                continue
            if any(x == m or x.startswith(m + ":") for x in 模型):
                引擎.append(Ollama引擎(m))
            else:
                print(f"⚠️ 模型 {m} 不在本地 Ollama（可用: {sorted(模型)[:6]}...），跳过")
    elif 模型:
        for m, n in [("longhun-v3.8", "龍魂·v3.8(本地)"), ("qwen2.5:7b", "通义·7b(本地)")]:
            if any(x == m or x.startswith(m + ":") for x in 模型):
                引擎.append(Ollama引擎(m, n))
    if not 引擎:
        # Ollama 不可达或全部模型缺失：显式降级并标注
        print("⚠️ Ollama 不可达或模型缺失 → 降级模拟引擎（结果非真实 AI 判断，仅用于流程演示）")
        引擎.append(本地龍魂引擎())
    # 云端适配器：配置了 KEY 才启用
    if os.environ.get("LONGHUN_KIMI_KEY"):
        引擎.append(模拟云端引擎("kimi"))
    if os.environ.get("LONGHUN_DEEPSEEK_KEY"):
        引擎.append(模拟云端引擎("deepseek"))
    return 引擎


# ═══════════════════════════════════════════════════════════
# 三、结果仓库（独立存储·永不合并）
# ═══════════════════════════════════════════════════════════

_DB路径 = str(ROOT / "logs" / "transparent_audit.db")


class 结果仓库:
    """结果与审计历史仓库 —— 持久化到 logs/transparent_audit.db，跨进程保留。
    v2.3: 每操作短连接（SQLite 对象不可跨线程，FastAPI 线程池安全）。"""

    def __init__(self, db路径: str = None):
        self.db路径 = db路径 or _DB路径
        os.makedirs(os.path.dirname(self.db路径), exist_ok=True)

    def _连(self):
        conn = sqlite3.connect(self.db路径, timeout=5)
        conn.execute("""CREATE TABLE IF NOT EXISTS 结果(
            父DNA TEXT, 子DNA TEXT PRIMARY KEY, 来源 TEXT, 时间 REAL,
            内容 TEXT, 置信度 REAL, token统计 TEXT, 耗时 REAL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS 历史(
            父DNA TEXT PRIMARY KEY, 问题 TEXT, 时间 REAL, 三色 TEXT, R值 INTEGER,
            摘要 TEXT, 引擎数 INTEGER, 失败数 INTEGER)""")
        return conn

    def 存(self, 父DNA, r):
        with closing(self._连()) as conn, conn:
            conn.execute(
                "INSERT OR REPLACE INTO 结果 VALUES(?,?,?,?,?,?,?,?)",
                (
                    父DNA,
                    r["子DNA"],
                    r["来源"],
                    time.time(),
                    r["内容"],
                    r["置信度"],
                    json.dumps(r["token统计"], ensure_ascii=False),
                    r["耗时"],
                ),
            )

    def 取(self, 父DNA):
        with closing(self._连()) as conn:
            return conn.execute(
                "SELECT 来源,内容,置信度,token统计,耗时,子DNA FROM 结果 WHERE 父DNA=?",
                (父DNA,),
            ).fetchall()

    def 记历史(self, 报告: dict):
        with closing(self._连()) as conn, conn:
            conn.execute(
                "INSERT OR REPLACE INTO 历史 VALUES(?,?,?,?,?,?,?,?)",
                (
                    报告.get("父DNA", ""),
                    报告.get("问题", "")[:120],
                    time.time(),
                    报告.get("三色", "🟡"),
                    报告.get("R值"),  # 单引擎未仲裁时为 NULL，前端显示 R—
                    报告.get("摘要", {}).get("一句话结论", "")[:200] if 报告.get("摘要") else "",
                    len(报告.get("回答", [])),
                    报告.get("失败数", 0),
                ),
            )

    def 历史(self, limit: int = 10):
        with closing(self._连()) as conn:
            rows = conn.execute(
                "SELECT 父DNA,问题,时间,三色,R值,摘要,引擎数,失败数 FROM 历史 ORDER BY 时间 DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
        return [
            {
                "父DNA": r[0], "问题": r[1], "时间": r[2],
                "三色": r[3], "R值": r[4], "摘要": r[5],
                "引擎数": r[6], "失败数": r[7],
            }
            for r in rows
        ]


# ═══════════════════════════════════════════════════════════
# 四、事实级冲突仲裁 v2.2
# ═══════════════════════════════════════════════════════════

class EntityExtractor:
    SUBJECTS = [
        "用户数据", "数据主权", "本地存储", "云端存储", "用户隐私",
        "主权归属", "法律管辖", "行为记录", "DNA追溯码", "三色审计",
        "史官记录", "耻辱墙", "P0协议", "数字身份", "操作记录",
        "创作者主权", "老百姓数据", "个人信息", "训练数据",
    ]
    PREDICATES = [
        "存储于", "存储在", "保存于", "存放于", "归属", "归属于", "属于", "归",
        "适用", "遵守", "遵循", "记录于", "写入", "记入", "存档于",
        "追溯至", "追踪到", "审计于", "保护", "托管", "授权", "流经",
    ]
    OBJECTS = [
        "本地设备", "本地终端", "本地", "云端服务器", "云端", "云上",
        "用户", "老百姓", "国家", "国家法律", "法律", "龍魂系统", "龍魂系统",
        "区块链", "数据库", "终端设备", "终端", "服务器", "史官系统",
    ]
    NEGATIONS = ["不得", "禁止", "不可", "不允许", "不应", "不能", "不", "未", "勿"]

    def __init__(self):
        def pat(words):
            return re.compile("(" + "|".join(sorted(words, key=len, reverse=True)) + ")")
        self.ps, self.pp, self.po = pat(self.SUBJECTS), pat(self.PREDICATES), pat(self.OBJECTS)

    def extract(self, text: str) -> List[Dict]:
        claims = []
        for sent in re.split(r"[。！？!?\n\r；;]+", text):
            sent = sent.strip()
            if not sent:
                continue
            for sm in self.ps.finditer(sent):
                pm = self.pp.search(sent, sm.end())
                if not pm:
                    continue
                om = self.po.search(sent, pm.end())
                if not om:
                    continue
                window = sent[max(0, pm.start() - 6):pm.start()]
                polarity = "NEG" if any(n in window for n in self.NEGATIONS) else "POS"
                claims.append({
                    "subject": sm.group(),
                    "predicate": pm.group(),
                    "object": om.group(),
                    "polarity": polarity,
                    "raw": sent,
                })
        return claims


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
        "龍魂系统": ["龍魂系统", "史官系统"],
        "老百姓": ["用户"],
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


@dataclass
class Conflict:
    subject: str
    predicate: str
    camps: Dict[str, List[str]]
    polarity_split: bool
    severity: str
    evidence: Dict[str, str]


class ContradictionDetector:
    def detect(self, claims_by_ai: Dict[str, List[Dict]]):
        grouped = defaultdict(dict)
        for ai, claims in claims_by_ai.items():
            for c in claims:
                grouped[(c["subject"], c["predicate"])][ai] = (c["object"], c["polarity"], c["raw"])

        conflicts, gaps = [], []
        for (s, p), ai_map in grouped.items():
            if len(ai_map) < 2:
                only = next(iter(ai_map.items()))
                gaps.append({
                    "subject": s,
                    "predicate": p,
                    "only_ai": only[0],
                    "note": "🟡 仅单个AI作证，无交叉验证（可能是漏报源，建议补问其他AI）",
                })
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
                    subject=s,
                    predicate=p,
                    camps=dict(camps),
                    polarity_split=len(polarities) > 1,
                    severity="🔴",
                    evidence=evidence,
                ))
        return conflicts, gaps


class SimilarityHelper:
    """相似度辅助信号 —— 纯标准库词袋余弦，断网可跑，永不联网下载模型。"""

    def __init__(self):
        self.backend = "bag-of-words(stdlib)"

    @staticmethod
    def _vec(text):
        v = defaultdict(float)
        for tok in re.findall(r"[\u4e00-\u9fff]{2,}|[a-zA-Z0-9_]+|[\u4e00-\u9fff]", text):
            v[tok] += 1.0
        return v

    @staticmethod
    def _cos(a, b):
        dot = sum(a[k] * b.get(k, 0) for k in a)
        na = sum(x * x for x in a.values()) ** 0.5
        nb = sum(x * x for x in b.values()) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    def compute(self, texts: List[str], names: List[str]) -> Dict:
        vecs = [self._vec(t) for t in texts]
        sims = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                sims.append({
                    "ai_a": names[i],
                    "ai_b": names[j],
                    "similarity": round(self._cos(vecs[i], vecs[j]), 4),
                    "note": "⚠️ 仅为差异提示，不作为冲突判定依据",
                })
        return {
            "backend": self.backend,
            "similarities": sims,
            "disclaimer": "相似度仅表示措辞接近程度，不代表事实一致性",
        }


class ConflictArbiterV2:
    def __init__(self, date=None, llm_hook=None):
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
                pass
        return self.extractor.extract(text)

    def analyze(self, ai_responses: Dict[str, str]) -> Dict:
        claims_by_ai = {ai: self._抽取(t) for ai, t in ai_responses.items()}
        normed = {ai: self.normalizer.normalize(c) for ai, c in claims_by_ai.items()}
        conflicts, gaps = self.detector.detect(normed)
        names = list(ai_responses.keys())
        sim_report = self.similarity.compute(list(ai_responses.values()), names)

        tricolor = "🔴" if conflicts else ("🟡" if gaps else "🟢")
        return {
            "dna": self.dna,
            "confirm": CONFIRM,
            "gpg": GPG_FINGERPRINT,
            "timestamp": datetime.now().isoformat(),
            "tricolor": tricolor,
            "_normed": normed,
            "conflicts": [
                {
                    "subject": c.subject,
                    "predicate": c.predicate,
                    "camps": c.camps,
                    "polarity_split": c.polarity_split,
                    "severity": c.severity,
                    "evidence": c.evidence,
                }
                for c in conflicts
            ],
            "coverage_gaps": gaps,
            "similarity_auxiliary": sim_report,
            "summary": {
                "total_claims": sum(len(c) for c in normed.values()),
                "conflicts_found": len(conflicts),
                "coverage_gaps": len(gaps),
                "conflict_pairs": sorted({
                    tuple(sorted([a, b]))
                    for c in conflicts
                    for ais in c.camps.values() for a in ais
                    for b in {x for v in c.camps.values() for x in v} - {a}
                }),
            },
        }


# ═══════════════════════════════════════════════════════════
# 五、冲突摘要层 P3
# ═══════════════════════════════════════════════════════════

class ConflictSummary:
    def build(self, 仲裁报告: Dict, 路由回答: List[Dict]) -> Dict:
        冲突键 = {(c["subject"], c["predicate"]) for c in 仲裁报告.get("conflicts", [])}
        共识 = []
        normed = 仲裁报告.get("_normed")
        if normed:
            组 = defaultdict(dict)
            for ai, claims in normed.items():
                for c in claims:
                    组[(c["subject"], c["predicate"])][ai] = c["object"]
            for (s, p), ai_obj in 组.items():
                if (s, p) in 冲突键 or len(ai_obj) < 2:
                    continue
                if len(set(ai_obj.values())) == 1:
                    共识.append({
                        "事实": f"{s}·{p} → {next(iter(ai_obj.values()))}",
                        "作证AI": sorted(ai_obj.keys()),
                    })

        分歧 = []
        for c in 仲裁报告.get("conflicts", []):
            camps = "；".join(f"「{obj}」由 {'/'.join(ais)} 主张" for obj, ais in c["camps"].items())
            分歧.append({
                "分歧点": f"{c['subject']}·{c['predicate']}",
                "各执一词": camps,
                "极性分裂": c["polarity_split"],
                "级别": c["severity"],
                "建议": "需老大裁决" if c["polarity_split"] else "建议以龍魂本地引擎为准·其余存档",
            })

        明细 = []
        总输入 = 总输出 = 0
        for r in 路由回答:
            if "失败" in r:
                明细.append({"引擎": r["来源"], "状态": "✗失败降级", "输入": 0, "输出": 0})
                continue
            t = r.get("token统计", {})
            总输入 += t.get("输入", 0)
            总输出 += t.get("输出", 0)
            明细.append({
                "引擎": r["来源"],
                "状态": "✓",
                "输入": t.get("输入", 0),
                "输出": t.get("输出", 0),
                "缓存命中率": t.get("缓存命中率", 0),
            })
        token汇总 = {
            "明细": 明细,
            "总输入": 总输入,
            "总输出": 总输出,
            "并行成本提示": f"本次并行 {len(明细)} 路，Token ≈ 单路的 {len(明细)} 倍（透明化承诺）",
        }

        n共, n分 = len(共识), len(分歧)
        三色 = 仲裁报告.get("tricolor", "🟡")
        if n分 == 0:
            结论 = f"{三色} 全员一致：{n共} 项共识，无分歧，可直接采信。"
        else:
            首 = 分歧[0]
            结论 = (
                f"{三色} {n共} 项共识 + {n分} 项分歧。"
                f"最要紧：{首['分歧点']}（{首['各执一词']}）——{首['建议']}。"
            )

        return {
            "一句话结论": 结论,
            "共识": 共识,
            "分歧点": 分歧,
            "token明细": token汇总,
            "三色": 三色,
        }


# ═══════════════════════════════════════════════════════════
# 六、史官集成 / R值审计 P4
# ═══════════════════════════════════════════════════════════

class R值审计器:
    """R值审计：与仲裁三色并存的第二把尺，衡量运行健康度。

    扣分规则（v2.3 校准，阈值=超过多少开始扣，罚分=每超1项扣多少）：
      - 事实冲突数: 阈值0 · 每项扣12   （冲突越多，可采信度越低）
      - 极性分裂数: 阈值0 · 每项扣8    （需老大裁决类，非纯技术扣分）
      - 引擎失败数: 阈值0 · 每项扣8    （引擎挂掉=证据链不全）
      - 覆盖率缺口: 阈值2 · 每项扣4    （前2项缺口可容忍，之后每项扣4）
    判色：>=85 🟢 · >=60 🟡 · <60 🔴
    """

    规则 = {
        "事实冲突数": (0, 12),
        "极性分裂数": (0, 8),
        "引擎失败数": (0, 8),
        "覆盖率缺口": (2, 4),
    }

    def audit(self, 指标: Dict[str, int]) -> Dict:
        score = 100
        details = []
        for key, (threshold, penalty) in self.规则.items():
            value = 指标.get(key, 0)
            if value > threshold:
                if key == "覆盖率缺口":
                    score -= penalty * (value - threshold)
                    details.append(f"{key}={value} > {threshold}，超{(value - threshold)}项×扣{penalty}分")
                else:
                    score -= penalty * value
                    details.append(f"{key}={value}，×扣{penalty}分/项")
        score = max(0, score)
        color = "🟢" if score >= 85 else ("🟡" if score >= 60 else "🔴")
        return {"R值": score, "三色": color, "明细": details}


class 史官集成器:
    """史官集成器 v2.3：年轮链持久化到 logs/transparent_audit.db，跨进程可验链。"""

    def __init__(self, 链: YearRingChain = None, db路径: str = None):
        self.db路径 = db路径 or _DB路径
        os.makedirs(os.path.dirname(self.db路径), exist_ok=True)
        self.链 = 链 or self._加载()

    def _加载(self) -> YearRingChain:
        """从 SQLite 重建内存链（verify 需要全链在内存逐条哈希复核）。"""
        链 = YearRingChain(name="transparent-audit")
        try:
            conn = sqlite3.connect(self.db路径)
            conn.execute("""CREATE TABLE IF NOT EXISTS yearring(
                seq INTEGER PRIMARY KEY, record_json TEXT, ts REAL)""")
            rows = conn.execute("SELECT record_json FROM yearring ORDER BY seq").fetchall()
            for (rj,) in rows:
                链.chain.append(json.loads(rj))
            conn.close()
        except Exception:
            pass
        return 链

    def _落盘(self, record: dict):
        conn = sqlite3.connect(self.db路径)
        conn.execute(
            "INSERT OR REPLACE INTO yearring(seq, record_json, ts) VALUES(?,?,?)",
            (record["index"], json.dumps(record, ensure_ascii=False, default=str), time.time()),
        )
        conn.commit()
        conn.close()

    def 归档(self, 路由报告: dict, 摘要: dict, 仲裁: dict) -> dict:
        指标 = {
            "事实冲突数": len(仲裁.get("conflicts", [])) if 仲裁 else 0,
            "极性分裂数": sum(
                1 for c in (仲裁.get("conflicts", []) if 仲裁 else []) if c["polarity_split"]
            ),
            "引擎失败数": 路由报告.get("失败数", 0),
            "覆盖率缺口": len(仲裁.get("coverage_gaps", []) if 仲裁 else []),
        }
        审计结果 = R值审计器().audit(指标)
        条目 = self.链.write({
            "父DNA": 路由报告.get("父DNA"),
            "问题": 路由报告.get("问题", "")[:50],
            "三色": 路由报告.get("三色"),
            "R值": 审计结果["R值"],
            "指标": 指标,
            "一句话结论": 摘要.get("一句话结论", ""),
        })
        self._落盘(条目)
        return {
            "史官条目序号": 条目["index"],
            "条目哈希": 条目["hash"],
            "条目DNA": 条目.get("data", {}).get("父DNA", ""),
            "R值审计": 审计结果,
        }

    def 验链(self) -> dict:
        ok, breaks = self.链.verify()
        return {
            "完整": ok,
            "长度": len(self.链.chain),
            "断点": breaks,
            "三色": "🟢" if ok else "🔴",
        }


# ═══════════════════════════════════════════════════════════
# 七、透明路由器 P1 + 全链路路由器
# ═══════════════════════════════════════════════════════════

class 透明路由器:
    def __init__(self, 引擎们: list, 仓库: 结果仓库 = None, 超时=5.0):
        self.引擎们 = 引擎们
        self.仓库 = 仓库 or 结果仓库()
        self.超时 = 超时
        self.仲裁 = ConflictArbiterV2()

    async def _单路(self, 引擎, 问题, 父DNA):
        子DNA = f"{父DNA[:-7]}-{引擎.名字.upper()}-{短身份码(引擎.名字 + 父DNA)}-UID9622"
        try:
            return await asyncio.wait_for(引擎.询问(问题, 子DNA, self.超时), timeout=self.超时)
        except Exception as e:
            return {
                "来源": 引擎.名字,
                "子DNA": 子DNA,
                "耗时": self.超时,
                "内容": "",
                "置信度": 0.0,
                "token统计": {},
                "失败": str(e)[:60],
            }

    async def 路由(self, 问题: str, 用户="UID9622") -> dict:
        父DNA = 生成DNA("USER-QUERY")
        结果 = await asyncio.gather(*[self._单路(e, 问题, 父DNA) for e in self.引擎们])
        for r in 结果:
            self.仓库.存(父DNA, r)
        有效 = {r["来源"]: r["内容"] for r in 结果 if "失败" not in r and r["内容"]}
        失败 = [r for r in 结果 if "失败" in r]
        仲裁报告 = self.仲裁.analyze(有效) if len(有效) >= 2 else None
        三色 = 仲裁报告["tricolor"] if 仲裁报告 else "🟡"
        if 失败 and 三色 == "🟢":
            三色 = "🟡"
        return {
            "父DNA": 父DNA,
            "用户": 用户,
            "问题": 问题,
            "回答": 结果,
            "仲裁": 仲裁报告,
            "失败数": len(失败),
            "三色": 三色,
            "时间": time.time(),
        }


class 全链路路由器(透明路由器):
    def __init__(self, 引擎们, 仓库=None, 超时=5.0, llm_hook=None, 史官=None):
        super().__init__(引擎们, 仓库, 超时)
        self.仲裁 = ConflictArbiterV2(llm_hook=llm_hook)
        self.摘要器 = ConflictSummary()
        self.史官 = 史官 or 史官集成器()

    async def 路由(self, 问题, 用户="UID9622") -> dict:
        报告 = await super().路由(问题, 用户)
        仲裁 = 报告["仲裁"]
        if 仲裁:
            摘要 = self.摘要器.build(仲裁, 报告["回答"])
            归档 = self.史官.归档(报告, 摘要, 仲裁)
            报告.update({"摘要": 摘要, "归档": 归档, "R值": 归档["R值审计"]["R值"]})
        self.仓库.记历史(报告)
        return 报告


# ═══════════════════════════════════════════════════════════
# 八、渲染输出
# ═══════════════════════════════════════════════════════════

def 仪表盘V2(报告: dict) -> str:
    行 = ["=" * 64, f"🐉 龍魂·透明审计仪表盘 v2.3 | {报告['三色']}", f"父DNA: {报告['父DNA']}", "-" * 64]
    for r in 报告["回答"]:
        if "失败" in r:
            行.append(f"  ✗ {r['来源']:<12} 失败降级: {r['失败']}")
        else:
            t = r["token统计"]
            行.append(f"  ✓ {r['来源']:<12} {r['耗时']:.2f}s | 置信度 {r['置信度']}")
    if 报告["仲裁"]:
        a = 报告["仲裁"]
        行.append("-" * 64)
        if a["conflicts"]:
            行.append(f"  ⚔️ 事实冲突 {len(a['conflicts'])} 项（分别呈现·不合并·不掩盖）:")
            for c in a["conflicts"]:
                camps = " vs ".join(f"{obj}（{'/'.join(ais)}）" for obj, ais in c["camps"].items())
                pol = " ＋极性分裂" if c["polarity_split"] else ""
                行.append(f"    {c['severity']} {c['subject']}·{c['predicate']}：{camps}{pol}")
        else:
            行.append("  无事实冲突")
        for g in a["coverage_gaps"]:
            行.append(f"    {g['note']}：{g['subject']}·{g['predicate']}（仅 {g['only_ai']}）")
    if "摘要" in 报告:
        行.append("-" * 64)
        行.append(f"  📌 {报告['摘要']['一句话结论']}")
        行.append(f"  💰 Token: 总输入 {报告['摘要']['token明细']['总输入']} · 总输出 {报告['摘要']['token明细']['总输出']}")
    if "归档" in 报告:
        行.append(f"  🗄️ 史官序号 {报告['归档']['史官条目序号']} · R值 {报告['归档']['R值审计']['R值']} {报告['归档']['R值审计']['三色']}")
    行.append("=" * 64)
    return "\n".join(行)


# ═══════════════════════════════════════════════════════════
# 九、FastAPI / stdlib API 服务壳
# ═══════════════════════════════════════════════════════════

默认引擎 = _构建默认引擎()

# 超时 90s：真实 Ollama 模型复杂问题可能需要 30-60s
全局路由器 = 全链路路由器(默认引擎, 超时=90.0)


def _清理(报告: dict) -> dict:
    r = dict(报告)
    if r.get("仲裁"):
        a = dict(r["仲裁"])
        a.pop("_normed", None)
        a.pop("similarity_auxiliary", None)
        r["仲裁"] = a
    return r


def _健康():
    return {
        "status": "🟢",
        "engines": [e.名字 for e in 默认引擎],
        "engine_count": len(默认引擎),
        "real": any(getattr(e, "真实", True) for e in 默认引擎),
        "db": _DB路径,
    }


async def _跑审计_async(问题: str, engines: Optional[str] = None) -> dict:
    """单次审计 + 附验链结果。engines 为逗号分隔模型名（前端引擎开关），空=全部默认引擎。"""
    if engines and engines.strip():
        # 临时路由器：复用全局仓库/史官（同一 SQLite），不污染长驻实例
        路由器 = 全链路路由器(
            _构建默认引擎(engines.split(",")),
            仓库=全局路由器.仓库, 超时=90.0, 史官=全局路由器.史官,
        )
    else:
        路由器 = 全局路由器
    报告 = await 路由器.路由(问题)
    报告["chain"] = 路由器.史官.验链()
    return _清理(报告)


def _跑审计(问题: str, engines: Optional[str] = None) -> dict:
    """同步包装（stdlib 降级模式用）。"""
    return asyncio.run(_跑审计_async(问题, engines))


def _启动_api(host="127.0.0.1", port=8970):
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        import uvicorn

        app = FastAPI(title="龍魂·透明仲裁 API", version="2.3")

        class Q(BaseModel):
            question: str
            engines: Optional[str] = None

        @app.post("/audit")
        async def audit(q: Q):
            return await _跑审计_async(q.question, q.engines)

        @app.get("/chain/verify")
        def verify():
            return 全局路由器.史官.验链()

        @app.get("/history")
        def history(limit: int = 10):
            return 全局路由器.仓库.历史(limit)

        @app.get("/health")
        def health():
            return _健康()

        uvicorn.run(app, host=host, port=port)
    except ImportError:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        from urllib.parse import urlparse, parse_qs

        class H(BaseHTTPRequestHandler):
            def _j(self, obj, code=200):
                b = json.dumps(obj, ensure_ascii=False).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(b)

            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def do_GET(self):
                path = urlparse(self.path)
                if path.path == "/health":
                    self._j(_健康())
                elif path.path == "/chain/verify":
                    self._j(全局路由器.史官.验链())
                elif path.path == "/history":
                    limit = int(parse_qs(path.query).get("limit", ["10"])[0])
                    self._j(全局路由器.仓库.历史(limit))
                else:
                    self._j({"error": "not found"}, 404)

            def do_POST(self):
                path = urlparse(self.path)
                if path.path == "/audit":
                    n = int(self.headers.get("Content-Length", 0))
                    body = json.loads(self.rfile.read(n) or b"{}")
                    self._j(_跑审计(body.get("question", ""), body.get("engines")))
                else:
                    self._j({"error": "not found"}, 404)

            def log_message(self, *a):
                pass

        print(f"⚠️ FastAPI未安装，降级stdlib模式 → http://{host}:{port}")
        HTTPServer((host, port), H).serve_forever()


# ═══════════════════════════════════════════════════════════
# 十、CLI
# ═══════════════════════════════════════════════════════════

def cmd_demo(_args):
    报告 = asyncio.run(全局路由器.路由("数据主权到底归谁？"))
    print(仪表盘V2(报告))
    return 0


def cmd_audit(args):
    global 全局路由器
    if args.engines:
        # 用户指定模型组合：重建路由器（跨进程一次性，不影响 API 常驻实例）
        全局路由器 = 全链路路由器(_构建默认引擎(args.engines.split(",")), 超时=90.0)
    报告 = asyncio.run(全局路由器.路由(args.question))
    报告["chain"] = 全局路由器.史官.验链()
    if args.json:
        print(json.dumps(_清理(报告), ensure_ascii=False, indent=2))
    else:
        print(仪表盘V2(报告))
        chain = 报告["chain"]
        print(f"  🔗 年轮链: {chain['长度']} 条 · {'🟢完整' if chain['完整'] else '🔴链断'} · 根 {chain.get('断点', [])}")
    return 0


def cmd_history(args):
    for h in 全局路由器.仓库.历史(args.limit):
        print(f"  {h['时间'] and time.strftime('%m-%d %H:%M', time.localtime(h['时间']))} | {h['三色']} R{h['R值']} | {h['问题'][:40]} | 引擎{h['引擎数']} 失败{h['失败数']}")
    return 0


def cmd_api(args):
    print(f"🐉 启动龍魂透明审计 API → http://{args.host}:{args.port}")
    print(f"  引擎: {[e.名字 for e in 默认引擎]}")
    _启动_api(args.host, args.port)
    return 0


def cmd_verify(_args):
    result = 全局路由器.史官.验链()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["完整"] else 1


def main():
    parser = argparse.ArgumentParser(
        prog="lh_transparent_audit",
        description="龍魂·透明审计与冲突仲裁引擎 v2.3（真实引擎+链落盘）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_transparent_audit.py demo
  lh_transparent_audit.py audit "数据主权归谁？"
  lh_transparent_audit.py audit "数据主权归谁？" --json
  lh_transparent_audit.py audit "数据主权归谁？" --engines qwen2.5:7b
  lh_transparent_audit.py history
  lh_transparent_audit.py api --port 8970
  lh_transparent_audit.py verify
        """,
    )
    parser.add_argument("--version", action="version", version="%(prog)s v2.3")
    sub = parser.add_subparsers(dest="command", required=True)

    p_demo = sub.add_parser("demo", help="内置演示")
    p_demo.set_defaults(func=cmd_demo)

    p_audit = sub.add_parser("audit", help="单次审计")
    p_audit.add_argument("question", help="审计问题")
    p_audit.add_argument("--json", action="store_true", help="JSON输出")
    p_audit.add_argument("--engines", default="", help="指定本地模型，逗号分隔（默认 longhun-v3.8,qwen2.5:7b）")
    p_audit.set_defaults(func=cmd_audit)

    p_api = sub.add_parser("api", help="启动API服务")
    p_api.add_argument("--host", default="127.0.0.1", help="监听地址")
    p_api.add_argument("--port", type=int, default=8970, help="监听端口")
    p_api.set_defaults(func=cmd_api)

    p_verify = sub.add_parser("verify", help="验证年轮链完整性")
    p_verify.set_defaults(func=cmd_verify)

    p_history = sub.add_parser("history", help="查看近期审计历史")
    p_history.add_argument("--limit", type=int, default=10, help="条数")
    p_history.set_defaults(func=cmd_history)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
