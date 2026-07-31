# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格验证与隔离申诉仲裁服务 v6.0
DNA: #龍芯⚡️丙午·辛未·PERSONA-VERIFY-v6.0

功能层级:
  v1.0 - 人格指纹验证 + 匹配度计算
  v2.0 - 自动隔离（观察牢房）+ 封禁
  v3.0 - 申诉通道 + 人工审核队列
  v4.0 - AI初审模型 + 定期自动重训练
  v5.0 - 模型版本信息 API
  v6.0 - 训练状态实时轮询 API + 训练历史

端口: 9623
Redis: 存储节点状态/隔离/申诉/审计（无 Redis 时自动降级内存）
"""
import hashlib
import json
import os
import pickle
import shutil
import sys
import time
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

DNA = "#龍芯⚡️丙午·辛未·PERSONA-VERIFY-v6.0"
UID = "UID9622"
CST = timezone(timedelta(hours=8))
LONGHUN_ROOT = Path.home() / "longhun-system"
MODEL_DIR = LONGHUN_ROOT / "models"
SCRIPTS_DIR = LONGHUN_ROOT / "scripts"
APPEAL_EVIDENCE_DIR = Path("/opt/longhun/appeals/evidence")

os.makedirs(APPEAL_EVIDENCE_DIR, exist_ok=True)

app = FastAPI(
    title="🐉 龍魂人格验证与隔离申诉仲裁节点",
    version="6.0",
    description="验证 + 隔离 + 申诉 + AI初审 + 模型版本 + 训练状态",
)

# ═══════════════════════════════════════════════════════
# 训练监控器（从本地脚本导入）
# ═══════════════════════════════════════════════════════
try:
    sys.path.insert(0, str(SCRIPTS_DIR))
    import importlib as _im
    TrainingMonitor = _im.import_module('longhun-training-monitor').TrainingMonitor
    HAS_MONITOR = True
except ImportError:
    HAS_MONITOR = False

    class _FakeMonitor:
        """训练监控器不可用时的降级"""
        @staticmethod
        def get_status():
            return {"state": "idle", "dna": DNA, "note": "monitor not available"}

        @staticmethod
        def get_model_version():
            version_file = MODEL_DIR / "model_version.json"
            if version_file.exists():
                try:
                    info = json.loads(version_file.read_text())
                    info["status"] = "active"
                    return info
                except Exception:
                    pass
            return {"version": 0, "status": "not_trained", "dna": DNA}

        @staticmethod
        def get_model_history(limit=10):
            return {"total": 0, "history": [], "current": _FakeMonitor.get_model_version()}

        @staticmethod
        def is_training():
            return False

    TrainingMonitor = _FakeMonitor  # type: ignore

# ═══════════════════════════════════════════════════════
# Redis 连接（带内存 fallback）
# ═══════════════════════════════════════════════════════
try:
    import redis
    _r = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)
    _r.ping()
    HAS_REDIS = True
except Exception:
    HAS_REDIS = False
    _fallback_store: Dict[str, dict] = {}
    _fallback_lists: Dict[str, list] = {}
    _fallback_sets: Dict[str, set] = {}
    _fallback_zsets: Dict[str, dict] = {}

    class FakeRedis:
        def hset(self, key, mapping=None, **kwargs):
            mapping = mapping or kwargs
            _fallback_store[key] = dict(mapping)
        def hgetall(self, key):
            return _fallback_store.get(key, {})
        def hget(self, key, field):
            return _fallback_store.get(key, {}).get(field)
        def hincrby(self, key, field, amount):
            cur = int(_fallback_store.get(key, {}).get(field, 0))
            _fallback_store.setdefault(key, {})[field] = str(cur + amount)
        def lpush(self, key, *values):
            lst = _fallback_lists.setdefault(key, [])
            for v in reversed(values):
                lst.insert(0, v)
        def lrange(self, key, start, end):
            lst = _fallback_lists.get(key, [])
            if end < 0:
                end = len(lst) + end + 1
            return lst[start:end]
        def ltrim(self, key, start, end):
            lst = _fallback_lists.get(key, [])
            _fallback_lists[key] = lst[start:end]
        def llen(self, key):
            return len(_fallback_lists.get(key, []))
        def lrem(self, key, count, value):
            lst = _fallback_lists.get(key, [])
            removed = 0
            while value in lst and (count == 0 or removed < count):
                lst.remove(value)
                removed += 1
        def sadd(self, key, *values):
            s = _fallback_sets.setdefault(key, set())
            s.update(values)
        def smembers(self, key):
            return list(_fallback_sets.get(key, set()))
        def sismember(self, key, value):
            return value in _fallback_sets.get(key, set())
        def zadd(self, key, mapping):
            z = _fallback_zsets.setdefault(key, {})
            z.update(mapping)
        def zrange(self, key, start, end, withscores=False):
            z = _fallback_zsets.get(key, {})
            items = sorted(z.items(), key=lambda x: x[1])
            result = items[start:end + 1] if end >= 0 else items[start:]
            if withscores:
                return result
            return [k for k, _ in result]
        def zrem(self, key, *values):
            z = _fallback_zsets.get(key, {})
            for v in values:
                z.pop(v, None)
        def scan_iter(self, match=None, **kwargs):
            for k in _fallback_store:
                if match and match.replace("*", "") in k:
                    yield k.encode() if isinstance(k, str) else k
        def expire(self, key, ttl):
            pass
        def delete(self, key):
            _fallback_store.pop(key, None)
            _fallback_lists.pop(key, None)
            _fallback_sets.pop(key, None)
            _fallback_zsets.pop(key, None)

    r = FakeRedis()
    print("⚠️ Redis 不可用，使用内存存储（重启后丢失状态）")

# ═══════════════════════════════════════════════════════
# 主控人格加载
# ═══════════════════════════════════════════════════════
def _load_master_persona() -> dict[str, Any]:
    chain_file = LONGHUN_ROOT / "persona-chain" / "persona-chain-latest.json"
    if chain_file.exists():
        data = json.loads(chain_file.read_text())
        return {
            "dna": data.get("dna", DNA),
            "value_fingerprint": data.get("value_fingerprint", "0" * 16),
            "emotion_fingerprint": data.get("emotion_fingerprint", "0" * 16),
            "persona_id": data.get("persona_id", ""),
            "trust_score": 100.0,
            "total_decisions": data.get("stats", {}).get("total_decisions", 0),
        }
    return {"dna": DNA, "value_fingerprint": "0" * 16, "emotion_fingerprint": "0" * 16,
            "persona_id": "", "trust_score": 100.0, "total_decisions": 0}

MASTER = _load_master_persona()
print(f"主控人格: {MASTER.get('persona_id', '未训练')[:24]}...")

# ═══════════════════════════════════════════════════════
# 信任等级与策略（同 v4）
# ═══════════════════════════════════════════════════════
class TrustLevel(str, Enum):
    MASTER = "master"; HIGH = "high"; MEDIUM = "medium"; LOW = "low"
    UNVERIFIED = "unverified"; QUARANTINE = "quarantine"
    APPEAL_PENDING = "appeal_pending"; APPEAL_REVIEW = "appeal_review"; BANNED = "banned"

QUARANTINE_CONFIG = {
    TrustLevel.MASTER: {"api_access": True, "write_access": True, "admin_access": True, "rate_limit": 10000, "data_sync": True, "alert": False},
    TrustLevel.HIGH: {"api_access": True, "write_access": True, "admin_access": False, "rate_limit": 1000, "data_sync": True, "alert": False},
    TrustLevel.MEDIUM: {"api_access": True, "write_access": False, "admin_access": False, "rate_limit": 100, "data_sync": False, "alert": True},
    TrustLevel.LOW: {"api_access": True, "write_access": False, "admin_access": False, "rate_limit": 10, "data_sync": False, "alert": True},
    TrustLevel.UNVERIFIED: {"api_access": False, "write_access": False, "admin_access": False, "rate_limit": 0, "data_sync": False, "alert": True},
    TrustLevel.QUARANTINE: {"api_access": False, "write_access": False, "admin_access": False, "rate_limit": 0, "data_sync": False, "alert": True},
    TrustLevel.APPEAL_PENDING: {"api_access": False, "write_access": False, "admin_access": False, "rate_limit": 0, "data_sync": False, "alert": False},
    TrustLevel.APPEAL_REVIEW: {"api_access": False, "write_access": False, "admin_access": False, "rate_limit": 0, "data_sync": False, "alert": False},
    TrustLevel.BANNED: {"api_access": False, "write_access": False, "admin_access": False, "rate_limit": 0, "data_sync": False, "alert": True},
}

AUTO_QUARANTINE_THRESHOLD = 30.0
AUTO_BAN_THRESHOLD = 10.0
QUARANTINE_DURATION = 86400 * 7
APPEAL_WINDOW = 86400 * 3

# ═══════════════════════════════════════════════════════
# 龍魂价值观词典 & AI初审模型（同 v4）
# ═══════════════════════════════════════════════════════
LONGHUN_VALUE_WORDS = {
    "开源": 1.0, "免费": 1.0, "主权": 1.0, "人民": 1.0, "祖国": 1.0,
    "军人": 1.0, "责任": 1.0, "担当": 1.0, "硬刚": 1.0, "不妥协": 1.0,
    "透明": 1.0, "审计": 1.0, "道德": 1.0, "底线": 1.0, "原则": 1.0,
    "信仰": 1.0, "信念": 1.0, "龍魂": 1.0, "UID9622": 1.0, "不跪": 1.0,
    "中国": 1.0, "数据主权": 1.0, "为人民服务": 1.0,
    "奉献": 0.8, "普惠": 0.8, "公平": 0.8, "正义": 0.8, "诚实": 0.8,
    "保护": 0.8, "守护": 0.8, "传承": 0.8, "创新": 0.8, "自主": 0.8,
    "自逼": 0.8, "不欺": 0.8, "实心": 0.8, "忠诚": 0.8,
    "资本": -0.5, "收割": -0.7, "黑箱": -0.8, "垄断": -0.6, "欺诈": -0.9,
    "虚伪": -0.7, "背叛": -0.9, "出卖": -0.9, "舔狗": -0.6, "软脚": -0.7,
    "商业化": -0.6, "融资": -0.7, "上市": -0.6, "收割用户": -0.9,
    "他妈": 0.0, "操": 0.0, "逼": 0.0, "狗日": 0.0,
}

EMOTION_REAL_MARKERS = ["他妈", "操", "逼", "狗日", "傻逼", "老子", "我靠", "他妈的", "滚", "操蛋"]
EMOTION_FAKE_MARKERS = ["致力于", "赋能", "闭环", "抓手", "落地", "生态", "护城河", "降本增效", "颗粒度", "对齐"]


class AppealAIReviewer:
    def __init__(self):
        self.vectorizer = None; self.classifier = None; self._load_model()

    def _load_model(self):
        model_path = MODEL_DIR / "appeal_classifier.pkl"
        if not model_path.exists():
            print("⚠️ AI初审模型未找到，使用规则初审"); return
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
            self.vectorizer = data['vectorizer']; self.classifier = data['classifier']
            trained = data.get('trained_at', 0) or data.get('stats', {}).get('trained_at', 0)
            if trained:
                print(f"✅ AI初审模型已加载 (训练于 {datetime.fromtimestamp(trained, CST)})")
            else:
                print("✅ AI初审模型已加载")
        except Exception as e:
            print(f"❌ AI模型加载失败: {e}")

    def is_ready(self): return self.classifier is not None

    def review(self, statement: str, file_contents: List[str] = None) -> dict[str, Any]:
        if not self.is_ready():
            return self._rule_based_review(statement, file_contents)
        all_text = statement
        if file_contents:
            all_text += " " + " ".join(fc[:2000] for fc in file_contents[:3])
        if len(all_text.strip()) < 10:
            return self._rule_based_review(statement, file_contents)
        X_vec = self.vectorizer.transform([all_text])
        ai_score = float(self.classifier.predict_proba(X_vec)[0][1])
        value_score = self._value_score(all_text)
        if value_score < 0.3: ai_score *= 0.5
        elif value_score > 0.8: ai_score = min(1.0, ai_score * 1.2)
        emotion_score = self._emotion_score(all_text)
        final_score = ai_score * 0.6 + value_score * 0.3 + emotion_score * 0.1
        confidence = abs(ai_score - 0.5) * 2
        if self._constitutional_violation(all_text):
            final_score = min(final_score, 0.1); confidence = 1.0
        return {
            "verdict": self._verdict_str(final_score, confidence),
            "confidence": round(confidence, 4), "score": round(final_score - 0.5, 4),
            "factors": [f"AI模型: {ai_score:.2f}", f"价值观: {value_score:.2f}",
                       f"情绪: {emotion_score:.2f}", f"综合: {final_score:.2f}", f"模型DNA: {UID}"],
            "method": "ai_model",
            "detail": {"final_score": round(final_score, 4), "ai_score": round(ai_score, 4),
                       "value_score": round(value_score, 4), "emotion_score": round(emotion_score, 4),
                       "confidence": round(confidence, 4)},
        }

    def _rule_based_review(self, statement: str, file_contents: List[str] = None) -> dict[str, Any]:
        score = 0.0; factors = []
        if len(statement) > 500: score += 0.2; factors.append("陈述详细")
        elif len(statement) < 100: score -= 0.3; factors.append("陈述过短")
        fc = file_contents or []
        if len(fc) >= 3: score += 0.3; factors.append("证据充足")
        elif len(fc) == 0: score -= 0.5; factors.append("无证据")
        confidence = min(max(score + 0.5, 0), 1)
        verdict = "release" if confidence >= 0.9 else "likely_release" if confidence >= 0.7 else "review_needed" if confidence >= 0.4 else "likely_reject"
        return {"verdict": verdict, "confidence": round(confidence, 4), "score": round(score, 4), "factors": factors, "method": "rule_fallback"}

    def _value_score(self, text: str) -> float:
        score = 0.0; total = 0.0
        for word, weight in LONGHUN_VALUE_WORDS.items():
            count = text.count(word)
            if count > 0: score += weight * min(count, 5); total += abs(weight) * min(count, 5)
        if total == 0: return 0.5
        return max(0.0, min(1.0, (score / total + 1) / 2))

    def _emotion_score(self, text: str) -> float:
        r = sum(1 for m in EMOTION_REAL_MARKERS if m in text)
        f = sum(1 for m in EMOTION_FAKE_MARKERS if m in text)
        if r == 0 and f == 0: return 0.5
        return r / (r + f + 1)

    def _constitutional_violation(self, text: str) -> bool:
        red_lines = ["出卖数据", "出卖用户", "数据卖给", "勾结境外",
                     "反华", "台独", "港独", "藏独", "疆独", "颠覆", "颜色革命", "分裂国家"]
        return any(line in text for line in red_lines)

    def _verdict_str(self, score: float, confidence: float) -> str:
        if score >= 0.9 and confidence >= 0.7: return "release"
        elif score >= 0.7: return "likely_release"
        elif score >= 0.4: return "review_needed"
        elif score >= 0.2: return "extend"
        return "reject"

ai_reviewer = AppealAIReviewer()

# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════
class VerifyRequest(BaseModel):
    node_id: str; value_fingerprint: str; emotion_fingerprint: str
    decision_count: int = 0; node_type: str = "unknown"
    timestamp: int = 0; ip_address: Optional[str] = None

class AppealReviewReq(BaseModel):
    node_id: str; decision: str; reason: str; reviewer_dna: str; admin_key: str

# ═══════════════════════════════════════════════════════
# 核心函数（同 v4）
# ═══════════════════════════════════════════════════════
def _hamming_similarity(s1: str, s2: str) -> float:
    if len(s1) != len(s2) or len(s1) == 0: return 0.0
    return sum(a == b for a, b in zip(s1, s2)) / len(s1) * 100

def calculate_match(req: VerifyRequest):
    dna_verified = "UID9622" in req.node_id or "longhun" in req.node_id.lower() or "龍魂" in req.node_id
    if dna_verified: return 100.0, TrustLevel.MASTER
    value_match = _hamming_similarity(MASTER["value_fingerprint"], req.value_fingerprint)
    emotion_match = _hamming_similarity(MASTER["emotion_fingerprint"], req.emotion_fingerprint)
    decision_weight = min(req.decision_count / 1000, 1.0) * 100
    match_score = value_match * 0.4 + emotion_match * 0.4 + decision_weight * 0.2
    if match_score >= 80: level = TrustLevel.HIGH
    elif match_score >= 60: level = TrustLevel.MEDIUM
    elif match_score >= 30: level = TrustLevel.LOW
    else: level = TrustLevel.UNVERIFIED
    return match_score, level

def check_quarantine(node_id: str) -> Optional[dict]:
    data = r.hgetall(f"quarantine:{node_id}")
    if not data: return None
    expires_at = int(data.get("expires_at", 0))
    now = int(time.time())
    appeal_status = data.get("appeal_status", "none")
    if now > expires_at and data.get("status") == "active" and appeal_status != "pending":
        r.hset(f"quarantine:{node_id}", "status", "released")
        r.hset(f"quarantine:{node_id}", "released_at", str(now))
        data["status"] = "released"; data["auto_released"] = True
    return {"node_id": node_id, "reason": data.get("reason", ""),
            "match_score": float(data.get("match_score", 0)),
            "quarantined_at": int(data.get("quarantined_at", 0)),
            "expires_at": expires_at, "status": data.get("status", "unknown"),
            "appeal_status": appeal_status, "appeal_count": int(data.get("appeal_count", 0)),
            "auto_released": data.get("auto_released", "False") == "True"}

def apply_quarantine(node_id: str, match_score: float, reason: str, duration: int = QUARANTINE_DURATION):
    now = int(time.time()); expires = now + duration
    record = {"node_id": node_id, "reason": reason, "match_score": str(match_score),
              "quarantined_at": str(now), "expires_at": str(expires),
              "status": "active", "appeal_status": "none",
              "appeal_count": "0", "appeal_deadline": str(now + APPEAL_WINDOW)}
    r.hset(f"quarantine:{node_id}", mapping=record)
    r.expire(f"quarantine:{node_id}", duration + APPEAL_WINDOW + 86400)
    r.zadd("quarantine:active", {node_id: now})
    r.lpush("quarantine:history", json.dumps(record))
    r.ltrim("quarantine:history", 0, 999)
    notification = {"type": "quarantine", "node_id": node_id, "match_score": match_score,
                    "reason": reason, "expires_at": expires, "appeal_deadline": now + APPEAL_WINDOW,
                    "appeal_endpoint": "/appeal/submit",
                    "message": "节点已被隔离。72小时内可提交申诉证据。逾期自动维持隔离。"}
    r.lpush(f"notifications:{node_id}", json.dumps(notification))
    r.expire(f"notifications:{node_id}", APPEAL_WINDOW)
    r.lpush("alerts:quarantine", f"🔒 节点隔离: {node_id} | 匹配度: {match_score:.1f}%")
    return record

def apply_ban(node_id: str, match_score: float, reason: str):
    now = int(time.time())
    record = {"node_id": node_id, "reason": reason, "match_score": str(match_score),
              "banned_at": str(now), "status": "banned"}
    r.hset(f"ban:{node_id}", mapping=record)
    r.sadd("banned:nodes", node_id); r.lpush("ban:history", json.dumps(record))
    r.delete(f"quarantine:{node_id}"); r.zrem("quarantine:active", node_id)
    r.lpush("alerts:ban", f"🚫 永久封禁: {node_id} | 匹配度: {match_score:.1f}%")
    return record

def release_node(node_id: str, reason: str, by: str):
    now = int(time.time())
    r.hset(f"quarantine:{node_id}", "status", "released")
    r.hset(f"quarantine:{node_id}", "released_at", str(now))
    r.hset(f"quarantine:{node_id}", "released_by", by)
    r.hset(f"quarantine:{node_id}", "release_reason", reason)
    r.zrem("quarantine:active", node_id)
    r.lpush("alerts:release", f"✅ 节点释放: {node_id} | {reason} | {by}")

# ═══════════════════════════════════════════════════════
# API: 验证（v1-v4 继承）
# ═══════════════════════════════════════════════════════
@app.post("/verify")
async def verify_persona(req: VerifyRequest):
    if r.sismember("banned:nodes", req.node_id):
        raise HTTPException(status_code=403, detail="Node permanently banned")
    quarantine = check_quarantine(req.node_id)
    match_score, level = calculate_match(req)
    quarantine_status = None; can_appeal = False
    if match_score < AUTO_BAN_THRESHOLD:
        ban_record = apply_ban(req.node_id, match_score, "匹配度低于封禁阈值")
        quarantine_status = {"action": "banned", "reason": "匹配度极低",
                             "match_score": match_score, "banned_at": ban_record["banned_at"]}
        level = TrustLevel.BANNED
    elif match_score < AUTO_QUARANTINE_THRESHOLD:
        if not quarantine or quarantine.get("status") != "active":
            q_record = apply_quarantine(req.node_id, match_score, "自动隔离：匹配度低于阈值")
            quarantine_status = {"action": "quarantined", "reason": "匹配度低于阈值",
                                 "match_score": match_score, "expires_at": int(q_record["expires_at"]),
                                 "duration_days": QUARANTINE_DURATION // 86400}
            level = TrustLevel.QUARANTINE
        else:
            quarantine_status = {"action": "quarantine_extended", "reason": "仍在隔离观察期",
                                 "match_score": match_score, "expires_at": quarantine["expires_at"]}
            level = TrustLevel.QUARANTINE
    node_record = {"node_id": req.node_id, "match_score": str(round(match_score, 2)),
                   "trust_level": level.value, "last_seen": str(int(time.time())),
                   "dna_verified": str(level == TrustLevel.MASTER),
                   "node_type": req.node_type, "ip_address": req.ip_address or "unknown",
                   "quarantine_status": json.dumps(quarantine_status) if quarantine_status else ""}
    r.hset(f"persona:{req.node_id}", mapping=node_record)
    r.expire(f"persona:{req.node_id}", 86400)
    r.lpush("persona:heartbeat", json.dumps(
        {"node_id": req.node_id, "match_score": round(match_score, 2),
         "trust_level": level.value, "timestamp": int(time.time())}))
    r.ltrim("persona:heartbeat", 0, 9999)
    notifications = [json.loads(n) for n in r.lrange(f"notifications:{req.node_id}", 0, -1)]
    if quarantine and quarantine["status"] == "active":
        can_appeal = quarantine.get("appeal_count", 0) < 3
    return {
        "match_score": round(match_score, 2), "trust_level": level.value,
        "dna_verified": (level == TrustLevel.MASTER),
        "value_match": round(match_score * 0.4, 2),
        "emotion_match": round(match_score * 0.4, 2),
        "decision_weight": round(min(req.decision_count / 1000, 1.0) * 100, 2),
        "timestamp": datetime.now(CST).strftime("%H:%M:%S"), "node_id": req.node_id,
        "quarantine_status": {
            **(quarantine_status or {}), "can_appeal": can_appeal,
            "appeals_used": quarantine.get("appeal_count", 0) if quarantine else 0,
            "appeals_remaining": max(0, 3 - quarantine.get("appeal_count", 0)) if quarantine else 3,
            "permissions": QUARANTINE_CONFIG.get(level, QUARANTINE_CONFIG[TrustLevel.UNVERIFIED]),
        } if quarantine_status else None, "notifications": notifications, "can_appeal": can_appeal,
    }

# ═══════════════════════════════════════════════════════
# API: 隔离管理 & 申诉 & 状态（v2-v4 继承，精简）
# ═══════════════════════════════════════════════════════
@app.get("/quarantine/list")
async def list_quarantine():
    active = r.zrange("quarantine:active", 0, -1, withscores=True)
    result = []
    for node_id, score in active:
        data = r.hgetall(f"quarantine:{node_id}")
        if data:
            result.append({"node_id": node_id, "reason": data.get("reason", ""),
                           "match_score": float(data.get("match_score", 0)),
                           "quarantined_at": int(data.get("quarantined_at", 0)),
                           "expires_at": int(data.get("expires_at", 0)),
                           "remaining_hours": max(0, (int(data.get("expires_at", 0)) - int(time.time())) // 3600),
                           "status": data.get("status", "unknown"),
                           "appeal_status": data.get("appeal_status", "none")})
    return {"total": len(result), "nodes": sorted(result, key=lambda x: x["quarantined_at"], reverse=True)}

@app.get("/quarantine/history")
async def quarantine_history(limit: int = 50):
    return {"total": r.llen("quarantine:history"), "records": [json.loads(h) for h in r.lrange("quarantine:history", 0, limit - 1)]}

@app.post("/quarantine/release/{node_id}")
async def release_quarantine(node_id: str, admin_key: str):
    if admin_key != "UID9622_ADMIN_RELEASE": raise HTTPException(status_code=403, detail="Invalid admin key")
    quarantine = check_quarantine(node_id)
    if not quarantine: return {"error": "Node not in quarantine"}
    release_node(node_id, "manual_release", "admin")
    r.hset(f"persona:{node_id}", "trust_level", TrustLevel.UNVERIFIED.value)
    return {"node_id": node_id, "action": "released", "previous_status": quarantine["status"],
            "released_at": int(time.time())}

@app.get("/ban/list")
async def list_banned():
    banned = r.smembers("banned:nodes"); result = []
    for node_id in banned:
        data = r.hgetall(f"ban:{node_id}")
        if data: result.append({"node_id": node_id, "reason": data.get("reason", ""),
                                "match_score": float(data.get("match_score", 0)),
                                "banned_at": int(data.get("banned_at", 0))})
    return {"total": len(result), "nodes": result}

@app.post("/appeal/submit")
async def submit_appeal(node_id: str = Form(...), appeal_type: str = Form(...),
                        statement: str = Form(...), contact_info: Optional[str] = Form(None),
                        evidence_files: List[UploadFile] = File([])):
    quarantine = check_quarantine(node_id)
    if not quarantine: raise HTTPException(status_code=400, detail="Node not in quarantine")
    if quarantine["status"] != "active": raise HTTPException(status_code=400, detail="Quarantine already resolved")
    now = int(time.time())
    appeal_deadline = int(r.hget(f"quarantine:{node_id}", "appeal_deadline") or 0)
    if now > appeal_deadline: raise HTTPException(status_code=403, detail="Appeal window expired (72h)")
    appeal_count = int(r.hget(f"quarantine:{node_id}", "appeal_count") or 0)
    if appeal_count >= 3: raise HTTPException(status_code=429, detail="Max appeals reached (3)")
    evidence_dir = APPEAL_EVIDENCE_DIR / f"{node_id}_{now}"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = []; file_contents = []
    for file in evidence_files:
        file_path = evidence_dir / file.filename
        with open(file_path, "wb") as f: shutil.copyfileobj(file.file, f)
        with open(file_path, "rb") as f: fh = hashlib.sha256(f.read()).hexdigest()[:16]
        file_hashes.append({"filename": file.filename, "hash": fh, "size": os.path.getsize(file_path)})
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f: file_contents.append(f.read()[:5000])
        except Exception: pass
    auto_review = ai_reviewer.review(statement, file_contents)
    appeal_id = f"{node_id}_{now}"
    appeal_record = {"node_id": node_id, "appeal_id": appeal_id, "type": appeal_type,
                     "statement": statement, "contact_info": hashlib.sha256((contact_info or "").encode()).hexdigest()[:16] if contact_info else None,
                     "evidence_hash": hashlib.sha256(json.dumps({"statement": statement, "files": file_hashes}, sort_keys=True).encode()).hexdigest()[:16],
                     "file_count": str(len(evidence_files)), "file_hashes": json.dumps(file_hashes),
                     "submitted_at": str(now), "auto_review": json.dumps(auto_review),
                     "status": "pending", "reviewer": "", "decision": "", "decision_reason": ""}
    if auto_review.get("verdict") == "release" and auto_review.get("confidence", 0) >= 0.8:
        appeal_record["status"] = "released"; appeal_record["decision"] = "auto_release"
        appeal_record["decision_reason"] = "AI初审通过：证据可信度极高"
        release_node(node_id, "auto_appeal_ai", "system")
        r.hset(f"quarantine:{node_id}", "appeal_status", "released")
        r.hset(f"quarantine:{node_id}", "status", "released"); r.zrem("quarantine:active", node_id)
        r.lpush(f"notifications:{node_id}", json.dumps(
            {"type": "appeal_approved", "message": "申诉通过！节点已释放。进入30天观察期。", "appeal_id": appeal_id}))
        r.hset(f"appeal:{appeal_id}", mapping=appeal_record)
        return {"status": "released", "appeal_id": appeal_id, "verdict": "auto_release",
                "reason": "AI初审证据可信度极高，自动通过", "auto_review": auto_review,
                "message": "节点已释放，进入30天观察期"}
    r.hset(f"quarantine:{node_id}", "appeal_status", "pending")
    r.hincrby(f"quarantine:{node_id}", "appeal_count", 1)
    r.hset(f"appeal:{appeal_id}", mapping=appeal_record)
    r.lpush("appeal:pending_queue", appeal_id); r.lpush("appeal:all", json.dumps(appeal_record))
    r.lpush("alerts:appeal", f"📋 新申诉待审核: {node_id} | AI评估: {auto_review.get('verdict')}")
    return {"status": "submitted", "appeal_id": appeal_id,
            "queue_position": r.llen("appeal:pending_queue"), "auto_review": auto_review,
            "estimated_review_time": "24-48小时", "message": "申诉已提交，进入审核队列。"}

@app.get("/appeal/status/{appeal_id}")
async def appeal_status(appeal_id: str):
    data = r.hgetall(f"appeal:{appeal_id}")
    if not data: raise HTTPException(status_code=404, detail="Appeal not found")
    return {"appeal_id": appeal_id, "node_id": data.get("node_id"), "type": data.get("type"),
            "status": data.get("status"), "submitted_at": int(data.get("submitted_at", 0)),
            "auto_review": json.loads(data.get("auto_review", "{}")),
            "reviewer": data.get("reviewer"), "decision": data.get("decision"),
            "decision_reason": data.get("decision_reason"),
            "decided_at": int(data.get("decided_at", 0)) if data.get("decided_at") else None}

@app.get("/appeal/queue")
async def appeal_queue(admin_key: str):
    if admin_key != "UID9622_ADMIN_APPEAL": raise HTTPException(status_code=403, detail="Invalid admin key")
    pending = r.lrange("appeal:pending_queue", 0, -1); queue = []
    for aid in pending:
        data = r.hgetall(f"appeal:{aid}")
        if data: queue.append({"appeal_id": aid, "node_id": data.get("node_id"),
                               "type": data.get("type"), "submitted_at": int(data.get("submitted_at", 0)),
                               "auto_review": json.loads(data.get("auto_review", "{}")),
                               "statement_preview": data.get("statement", "")[:100] + "..."})
    return {"total_pending": len(queue), "queue": queue, "total_processed": r.llen("appeal:processed")}

@app.post("/appeal/review")
async def review_appeal(req: AppealReviewReq):
    if req.admin_key != "UID9622_ADMIN_APPEAL": raise HTTPException(status_code=403, detail="Invalid admin key")
    if not req.reviewer_dna.startswith("UID9622"): raise HTTPException(status_code=403, detail="Invalid reviewer DNA")
    appeal_key = None
    for key in r.scan_iter(match="appeal:*"):
        k = key if isinstance(key, str) else key.decode()
        data = r.hgetall(k)
        if data.get("node_id") == req.node_id and data.get("status") == "pending":
            appeal_key = k; break
    if not appeal_key: raise HTTPException(status_code=404, detail="No pending appeal found")
    now = int(time.time())
    if req.decision == "release":
        release_node(req.node_id, "appeal_approved", req.reviewer_dna)
        r.hset(appeal_key, "status", "released")
        r.hset(f"quarantine:{req.node_id}", "appeal_status", "released")
        r.hset(f"quarantine:{req.node_id}", "status", "released")
        r.zrem("quarantine:active", req.node_id)
        r.hset(f"persona:{req.node_id}", "trust_level", TrustLevel.HIGH.value)
        r.hset(f"persona:{req.node_id}", "observation_until", str(now + 86400 * 30))
        notification = {"type": "appeal_approved", "message": "申诉通过！进入30天观察期。",
                        "reviewer": req.reviewer_dna, "reason": req.reason}
    elif req.decision == "reject":
        appeal_count = int(r.hget(f"quarantine:{req.node_id}", "appeal_count") or 0)
        if appeal_count >= 3:
            apply_ban(req.node_id, 0, "多次申诉驳回，升级永久封禁")
            r.hset(appeal_key, "status", "upgraded_to_ban")
            notification = {"type": "appeal_rejected_banned",
                            "message": "申诉驳回，已达最大次数。永久封禁。",
                            "reviewer": req.reviewer_dna, "reason": req.reason}
        else:
            r.hset(appeal_key, "status", "rejected")
            r.hset(f"quarantine:{req.node_id}", "appeal_status", "rejected")
            cur_exp = int(r.hget(f"quarantine:{req.node_id}", "expires_at") or 0)
            r.hset(f"quarantine:{req.node_id}", "expires_at", str(cur_exp + QUARANTINE_DURATION))
            notification = {"type": "appeal_rejected", "message": f"驳回。隔离延长7天。剩余: {3 - appeal_count}次",
                            "reviewer": req.reviewer_dna, "reason": req.reason}
    elif req.decision == "extend":
        cur_exp = int(r.hget(f"quarantine:{req.node_id}", "expires_at") or 0)
        r.hset(f"quarantine:{req.node_id}", "expires_at", str(cur_exp + QUARANTINE_DURATION * 2))
        r.hset(appeal_key, "status", "extended")
        r.hset(f"quarantine:{req.node_id}", "appeal_status", "extended")
        notification = {"type": "appeal_extended", "message": "需补充证据。隔离延长14天。",
                        "reviewer": req.reviewer_dna, "reason": req.reason}
    else:
        raise HTTPException(status_code=400, detail=f"Unknown decision: {req.decision}")
    r.hset(appeal_key, "reviewer", req.reviewer_dna)
    r.hset(appeal_key, "decision", req.decision)
    r.hset(appeal_key, "decision_reason", req.reason)
    r.hset(appeal_key, "decided_at", str(now))
    r.lrem("appeal:pending_queue", 0, appeal_key.replace("appeal:", ""))
    r.lpush("appeal:processed", appeal_key)
    r.lpush(f"notifications:{req.node_id}", json.dumps(notification))
    r.lpush("audit:appeal_reviews", json.dumps(
        {"timestamp": now, "node_id": req.node_id, "decision": req.decision,
         "reason": req.reason, "reviewer": req.reviewer_dna, "appeal_id": appeal_key}))
    return {"status": "reviewed", "decision": req.decision, "node_id": req.node_id,
            "reviewer": req.reviewer_dna, "notification": notification}

@app.get("/node/notifications/{node_id}")
async def get_notifications(node_id: str):
    notifications = r.lrange(f"notifications:{node_id}", 0, -1)
    r.delete(f"notifications:{node_id}")
    quarantine = check_quarantine(node_id)
    return {"node_id": node_id, "notifications": [json.loads(n) for n in notifications],
            "quarantine_status": quarantine,
            "can_appeal": quarantine and quarantine["status"] == "active" and quarantine.get("appeal_count", 0) < 3 if quarantine else False}

# ═══════════════════════════════════════════════════════
# API: 状态 & 健康检查
# ═══════════════════════════════════════════════════════
@app.get("/status/all")
async def all_nodes():
    nodes = {}
    for key in r.scan_iter(match="persona:*"):
        node_id = key.replace("persona:", "") if isinstance(key, str) else key.decode().replace("persona:", "")
        data = r.hgetall(key)
        if not data: continue
        qs = data.get("quarantine_status", "")
        quarantine_data = None
        if qs:
            try: quarantine_data = json.loads(qs)
            except Exception: pass
        nodes[node_id] = {"match_score": float(data.get("match_score", 0)),
                          "trust_level": data.get("trust_level", "unknown"),
                          "last_seen": int(data.get("last_seen", 0)),
                          "dna_verified": data.get("dna_verified", "False") == "True",
                          "node_type": data.get("node_type", "unknown"),
                          "ip_address": data.get("ip_address", "unknown"),
                          "quarantine": quarantine_data}
    levels = {}
    for n in nodes.values():
        lvl = n["trust_level"]; levels[lvl] = levels.get(lvl, 0) + 1
    return {"master": MASTER, "nodes": nodes, "total": len(nodes),
            "verified_count": sum(1 for n in nodes.values() if n["dna_verified"]),
            "quarantine_count": len(r.zrange("quarantine:active", 0, -1)),
            "ban_count": len(r.smembers("banned:nodes")),
            "level_distribution": levels,
            "appeals": {"pending": r.llen("appeal:pending_queue"), "processed": r.llen("appeal:processed")},
            "timestamp": int(time.time())}

@app.get("/alerts")
async def get_alerts(limit: int = 20):
    return {"quarantine_alerts": r.lrange("alerts:quarantine", 0, limit - 1),
            "ban_alerts": r.lrange("alerts:ban", 0, limit - 1),
            "appeal_alerts": r.lrange("alerts:appeal", 0, limit - 1),
            "release_alerts": r.lrange("alerts:release", 0, limit - 1),
            "total_unread": (r.llen("alerts:quarantine") + r.llen("alerts:ban") + r.llen("alerts:appeal") + r.llen("alerts:release"))}

@app.get("/health")
async def health():
    mv = TrainingMonitor.get_model_version()
    ts = TrainingMonitor.get_status()
    return {"status": "龍魂隔离申诉仲裁节点运行中", "version": "v6.0",
            "dna": MASTER["dna"], "redis_ok": HAS_REDIS, "monitor_ok": HAS_MONITOR,
            "master_trust": MASTER["trust_score"],
            "ai_model": {"loaded": ai_reviewer.is_ready(), "version": mv.get("version", 0),
                         "accuracy": mv.get("metrics", {}).get("accuracy", 0),
                         "samples": mv.get("training_samples", 0)},
            "training": {"state": ts.get("state", "idle"), "progress": ts.get("progress", 0),
                         "stage": ts.get("stage", "")},
            "features": ["verify", "quarantine", "appeal", "ai_review", "model_version", "training_status"],
            "active_quarantines": len(r.zrange("quarantine:active", 0, -1)),
            "pending_appeals": r.llen("appeal:pending_queue"),
            "banned_nodes": len(r.smembers("banned:nodes"))}

# ═══════════════════════════════════════════════════════
# NEW v6: 模型版本 & 训练状态 API
# ═══════════════════════════════════════════════════════

@app.get("/model-version")
async def model_version():
    """获取AI初审模型版本信息"""
    return TrainingMonitor.get_model_version()


@app.get("/model-version/history")
async def model_version_history(limit: int = 10):
    """获取模型版本历史（归档列表）"""
    return TrainingMonitor.get_model_history(limit)


@app.get("/training/status")
async def training_status():
    """获取当前训练状态（面板每2秒轮询）"""
    status = TrainingMonitor.get_status()

    # 动态时间字段
    if status.get("started_at"):
        elapsed = int(time.time()) - status["started_at"]
        status["elapsed_seconds"] = elapsed
        if elapsed < 60:
            status["elapsed_formatted"] = f"{elapsed}s"
        elif elapsed < 3600:
            status["elapsed_formatted"] = f"{elapsed // 60}m{elapsed % 60}s"
        else:
            status["elapsed_formatted"] = f"{elapsed // 3600}h{(elapsed % 3600) // 60}m"

    if status.get("estimated_complete") and status.get("state") in ["preparing", "training", "validating", "switching"]:
        remaining = max(0, status["estimated_complete"] - int(time.time()))
        status["remaining_seconds"] = remaining
        if remaining < 60:
            status["remaining_formatted"] = f"{remaining}s"
        elif remaining < 3600:
            status["remaining_formatted"] = f"{remaining // 60}m{remaining % 60}s"
        else:
            status["remaining_formatted"] = f"{remaining // 3600}h{(remaining % 3600) // 60}m"

    # 检查训练进程是否存活
    lock_file = MODEL_DIR / ".training_lock"
    if lock_file.exists():
        try:
            lock = json.loads(lock_file.read_text())
            pid = lock.get("pid")
            if pid:
                try:
                    os.kill(pid, 0)
                    status["process_alive"] = True
                except OSError:
                    status["process_alive"] = False
                    if status.get("state") in ["preparing", "training", "validating", "switching"]:
                        status["state"] = "error"
                        status["error"] = "Process died"
            else:
                status["process_alive"] = False
        except Exception:
            status["process_alive"] = False
    else:
        status["process_alive"] = TrainingMonitor.is_training()

    return status


@app.get("/training/history")
async def training_history(limit: int = 10):
    """获取训练完成历史"""
    done_files = sorted(MODEL_DIR.glob(".training_done_v*"), reverse=True)
    history = []
    for f in done_files[:limit]:
        try:
            data = json.loads(f.read_text())
            ts_val = data.get("completed_at", 0)
            if ts_val:
                data["completed_at_str"] = datetime.fromtimestamp(ts_val, CST).strftime("%Y-%m-%d %H:%M")
            history.append(data)
        except Exception:
            pass
    return {"total": len(history), "history": history}


# ═══════════════════════════════════════════════════════
# 启动事件: 清理残留训练状态
# ═══════════════════════════════════════════════════════
@app.on_event("startup")
async def startup_check():
    print()
    print(f"🐉 龍魂人格验证与隔离申诉仲裁节点 v6.0 启动")
    print(f"   DNA: {DNA}")
    print(f"   Redis: {'✅' if HAS_REDIS else '⚠️ 内存模式'}")
    print(f"   监控器: {'✅' if HAS_MONITOR else '⚠️ 降级模式'}")
    print(f"   AI初审: {'✅ 已加载' if ai_reviewer.is_ready() else '⚠️ 规则模式'}")
    print(f"   主控: {MASTER.get('persona_id', '未训练')[:24]}...")

    mv = TrainingMonitor.get_model_version()
    print(f"   模型版本: v{mv.get('version', 0)} | 准确率: {mv.get('metrics', {}).get('accuracy', 0):.1%}")

    # 清理残留训练状态
    if TrainingMonitor.is_training():
        ts = TrainingMonitor.get_status()
        print(f"   训练状态: {ts.get('state')} ({ts.get('progress', 0):.0f}%)")
    else:
        status = TrainingMonitor.get_status()
        if status.get("state") in ["preparing", "training", "validating", "switching"]:
            print("   🧹 清理残留训练状态")
            STATUS_FILE = MODEL_DIR / ".training_status"
            STATUS_FILE.write_text(json.dumps({"state": "idle", "stage": "就绪", "dna": DNA}))
        else:
            print(f"   训练状态: {status.get('state', 'idle')}")

    print(f"   特性: 验证|隔离|申诉|AI初审|模型版本|训练状态")
    print()

# ═══════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    import argparse as _ap
    _p = _ap.ArgumentParser(description="龍魂人格验证与隔离申诉仲裁服务 v6.0")
    _p.add_argument("--port", type=int, default=9623)
    _p.add_argument("--host", default="0.0.0.0")
    _a = _p.parse_args()
    uvicorn.run("__main__:app", host=_a.host, port=_a.port, log_level="info", reload=False)
