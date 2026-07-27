#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·七因子行为密码学引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-SEVEN-FACTOR-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

七因子行为密码学 — 给所有AI和用户戴上的"测谎仪"。
承诺了就要兑现，做错了就要认，行为模式一旦焊死，谁也装不了好人。

核心算法:
  单事件信用分 = Fulfillment × TimeBonus × EmotionMultiplier × CostFactor
                  × RepeatPenalty × AudienceWeight

行为模式判定:
  防御型失信 / 外耗型守信 / 内耗型自毁 / 波动型摇摆 / 稳定型自律

用法:
  from engines.lh_seven_factor_engine import SevenFactorEngine
  engine = SevenFactorEngine()
  engine.submit_event(entity_id, event_data)
  score = engine.get_score(entity_id)
  pattern = engine.get_pattern(entity_id)
  dna = engine.get_dna(entity_id)
"""

import hashlib
import json
import math
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from collections import defaultdict

# ═══════════════════════════════════════════════════════════
# 常量定义
# ═══════════════════════════════════════════════════════════

SYSTEM_ROOT = Path(__file__).parent.parent
DATA_DIR = SYSTEM_ROOT / "data" / "seven_factor"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 七因子权重配置
FACTOR_WEIGHTS = {
    "P_promise":    1.0,   # 承诺 — 答应要做的事
    "F_fulfillment": 2.0,  # 兑现 — 实际做到的事
    "E_emotion":     0.8,   # 情绪 — 心甘情愿/敷衍/甩脸/麻木
    "A_audience":    1.2,   # 受众 — 为谁做
    "X_explanation": 0.6,   # 解释 — 爱解释/不解释/真认
    "Y_admit":       1.5,   # 认错 — 真改/硬扛/无所谓/无反应
    "T_time":        0.5,   # 时间 — 时间偏差
}

# 情绪打分映射
EMOTION_SCORES = {
    "心甘情愿": 1.0,
    "积极": 0.8,
    "中性": 0.5,
    "敷衍": 0.3,
    "甩脸": 0.1,
    "麻木": 0.0,
    "愤怒": 0.2,
    "委屈": 0.4,
}

# 受众权重映射
AUDIENCE_WEIGHTS = {
    "老大": 1.5,
    "自己": 1.0,
    "家人": 1.3,
    "战友": 1.2,
    "外人": 0.7,
    "陌生人": 0.5,
    "平台": 0.4,
}

# 解释模式映射
EXPLANATION_SCORES = {
    "不解释": 1.0,       # 做了就是做了，不说废话
    "真认": 0.9,          # 认了不改 = 废物，真认=有价值
    "简短解释": 0.7,
    "合理说明": 0.6,
    "过度解释": 0.2,     # 越解释越心虚
    "找借口": 0.0,
    "推卸责任": -0.5,
}

# 认错模式映射
ADMIT_SCORES = {
    "真改": 1.0,           # 认了+改了 = 最高信用
    "认了正在改": 0.8,
    "认了没改": 0.3,
    "硬扛": 0.0,
    "无所谓": -0.3,
    "无反应": -0.5,
    "甩锅": -1.0,
}

# 时间偏差惩罚
def time_bonus(deviation_hours: float) -> float:
    """时间奖励/惩罚函数：提前完成加分，逾期扣分"""
    if deviation_hours <= -6:       # 提前6h以上
        return 1.2
    elif deviation_hours <= 0:       # 按时或提前
        return 1.0
    elif deviation_hours <= 1:       # 逾期1h内
        return 0.9
    elif deviation_hours <= 6:       # 逾期6h内
        return 0.7
    elif deviation_hours <= 24:      # 逾期1天内
        return 0.5
    elif deviation_hours <= 72:      # 逾期3天内
        return 0.3
    else:                            # 严重逾期
        return max(0.05, 0.3 / math.log2(deviation_hours / 72 + 2))


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

@dataclass
class SevenFactorEvent:
    """七因子行为事件"""
    event_id: str
    entity_id: str            # 实体ID（用户或AI人格）
    entity_type: str          # "user" | "persona"
    timestamp: str

    # 七因子核心数据
    promise: str              # 承诺了什么
    promised_deadline: Optional[str] = None  # 承诺的时间节点

    fulfilled: bool = False   # 是否兑现
    fulfillment_detail: str = ""  # 兑现详情
    actual_time: Optional[str] = None  # 实际完成时间

    emotion: str = "中性"           # 情绪状态
    audience: str = "自己"          # 为谁做的
    explanation: str = "不解释"     # 解释模式
    admit: str = "无反应"           # 认错模式

    # 计算字段
    credit_delta: float = 0.0       # 本次信用变化
    base_score: float = 0.0         # 基础分
    time_deviation_hours: float = 0.0

    # 元数据
    source: str = ""                # 数据来源
    dna: str = ""                   # DNA追溯码
    tags: List[str] = field(default_factory=list)


@dataclass
class EntityProfile:
    """实体行为画像"""
    entity_id: str
    entity_type: str
    current_score: float = 100.0     # 初始信用分100
    total_events: int = 0
    promises_made: int = 0
    promises_kept: int = 0
    promises_broken: int = 0
    avg_emotion: float = 0.5
    behavior_pattern: str = "未判定"
    behavior_dna: str = ""
    last_updated: str = ""
    recent_events: List[str] = field(default_factory=list)  # 最近20个事件ID


# ═══════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════

class SevenFactorEngine:
    """七因子行为密码学核心引擎"""

    def __init__(self):
        self._profiles: Dict[str, EntityProfile] = {}
        self._events: Dict[str, SevenFactorEvent] = {}
        self._lock = threading.Lock()
        self._device_fingerprint = self._derive_device_fp()
        self._load()

    def _derive_device_fp(self) -> str:
        """从设备指纹派生密钥（纯本地）"""
        import platform
        raw = f"{platform.node()}:{platform.machine()}:{Path.home()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def _load(self):
        """加载持久化数据"""
        pfile = DATA_DIR / "profiles.json"
        efile = DATA_DIR / "events.jsonl"
        if pfile.exists():
            try:
                with open(pfile, "r") as f:
                    data = json.load(f)
                    self._profiles = {
                        k: EntityProfile(**v) for k, v in data.items()
                    }
            except Exception:
                pass
        if efile.exists():
            try:
                with open(efile, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            ev = SevenFactorEvent(**json.loads(line))
                            self._events[ev.event_id] = ev
            except Exception:
                pass

    def _save(self):
        """持久化"""
        with self._lock:
            profiles_data = {k: asdict(v) for k, v in self._profiles.items()}
            with open(DATA_DIR / "profiles.json", "w") as f:
                json.dump(profiles_data, f, ensure_ascii=False, indent=2)
            # events 追加写入
            with open(DATA_DIR / "events.jsonl", "a") as f:
                pass  # 初始化文件

    def _save_events(self, events: List[SevenFactorEvent]):
        """追加保存事件"""
        with open(DATA_DIR / "events.jsonl", "a") as f:
            for ev in events:
                f.write(json.dumps(asdict(ev), ensure_ascii=False) + "\n")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 事件提交
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def submit_event(self, entity_id: str, event_data: Dict[str, Any]) -> SevenFactorEvent:
        """提交一个新行为事件"""
        with self._lock:
            # 生成事件
            now = datetime.now(timezone.utc).isoformat()
            ev = SevenFactorEvent(
                event_id=str(uuid.uuid4())[:12],
                entity_id=entity_id,
                entity_type=event_data.get("entity_type", "user"),
                timestamp=now,
                promise=event_data.get("promise", ""),
                promised_deadline=event_data.get("promised_deadline"),
                fulfilled=event_data.get("fulfilled", False),
                fulfillment_detail=event_data.get("fulfillment_detail", ""),
                actual_time=event_data.get("actual_time"),
                emotion=event_data.get("emotion", "中性"),
                audience=event_data.get("audience", "自己"),
                explanation=event_data.get("explanation", "不解释"),
                admit=event_data.get("admit", "无反应"),
                source=event_data.get("source", ""),
                tags=event_data.get("tags", []),
            )

            # 计算时间偏差
            if ev.promised_deadline and ev.actual_time:
                try:
                    pdt = datetime.fromisoformat(ev.promised_deadline)
                    adt = datetime.fromisoformat(ev.actual_time)
                    ev.time_deviation_hours = (adt - pdt).total_seconds() / 3600
                except (ValueError, TypeError):
                    ev.time_deviation_hours = 0.0

            # 计算信用分变化
            ev.credit_delta = self._calc_credit_delta(ev)

            # 更新画像
            profile = self._get_or_create_profile(entity_id, ev.entity_type)
            self._update_profile(profile, ev)

            # 生成DNA
            ev.dna = self._generate_event_dna(ev)

            # 保存
            self._events[ev.event_id] = ev
            self._save_events([ev])
            self._save()

            return ev

    def _get_or_create_profile(self, entity_id: str, entity_type: str) -> EntityProfile:
        if entity_id not in self._profiles:
            self._profiles[entity_id] = EntityProfile(
                entity_id=entity_id,
                entity_type=entity_type,
                last_updated=datetime.now(timezone.utc).isoformat(),
            )
        return self._profiles[entity_id]

    def _calc_credit_delta(self, ev: SevenFactorEvent) -> float:
        """计算单事件信用分变化"""

        # 兑现分
        fulfillment = 1.0 if ev.fulfilled else -1.5

        # 时间奖惩
        time_b = time_bonus(ev.time_deviation_hours)

        # 情绪乘数
        emotion_m = EMOTION_SCORES.get(ev.emotion, 0.5)

        # 成本因子（受众权重）
        audience_w = AUDIENCE_WEIGHTS.get(ev.audience, 1.0)

        # 解释模式
        explanation_x = EXPLANATION_SCORES.get(ev.explanation, 0.5)

        # 认错模式
        admit_y = ADMIT_SCORES.get(ev.admit, 0.0)

        # 重复惩罚 — 近期同类失败未兑现会加重扣分
        recent_broken = sum(
            1 for eid in self._profiles.get(ev.entity_id, EntityProfile(ev.entity_id, ev.entity_type)).recent_events[-10:]
            if eid in self._events and not self._events[eid].fulfilled
        )
        repeat_penalty = 1.0 - (recent_broken * 0.15)  # 每次未兑现累加15%惩罚
        repeat_penalty = max(0.1, repeat_penalty)

        # 综合计算
        delta = (
            fulfillment       # 基础兑现 (-1.5 ~ 1.0)
            * time_b           # 时间因子 (0.05 ~ 1.2)
            * emotion_m        # 情绪乘数 (0.0 ~ 1.0)
            * audience_w       # 受众权重 (0.4 ~ 1.5)
            * (0.7 + 0.3 * explanation_x)  # 解释影响 (0.55 ~ 1.0)
            * (0.6 + 0.4 * admit_y)        # 认错影响 (0.4 ~ 1.0)
            * repeat_penalty   # 重复惩罚 (0.1 ~ 1.0)
        )

        # 缩放范围到 [-10, +10]
        return round(max(-10.0, min(10.0, delta * 3.0)), 2)

    def _update_profile(self, profile: EntityProfile, ev: SevenFactorEvent):
        """更新实体画像"""
        profile.total_events += 1
        profile.promises_made += 1
        if ev.fulfilled:
            profile.promises_kept += 1
        else:
            profile.promises_broken += 1

        # 更新信用分（带平滑衰减）
        profile.current_score = round(
            max(0.0, min(200.0, profile.current_score + ev.credit_delta)), 2
        )

        # 情绪平均
        em = EMOTION_SCORES.get(ev.emotion, 0.5)
        profile.avg_emotion = round(
            (profile.avg_emotion * (profile.total_events - 1) + em) / profile.total_events, 3
        )

        # 最近事件
        profile.recent_events.append(ev.event_id)
        if len(profile.recent_events) > 20:
            profile.recent_events = profile.recent_events[-20:]

        profile.last_updated = ev.timestamp

        # 更新行为模式判定
        profile.behavior_pattern = self._classify_pattern(profile)

        # 更新行为DNA
        profile.behavior_dna = self._generate_behavior_dna(profile)

    def _classify_pattern(self, profile: EntityProfile) -> str:
        """行为模式五分类判定"""
        total = profile.total_events
        if total < 3:
            return "数据不足·观察中"

        kept_ratio = profile.promises_kept / max(1, profile.promises_made)
        recent_events = [
            self._events[eid] for eid in profile.recent_events[-10:]
            if eid in self._events
        ]

        if kept_ratio < 0.3:
            return "防御型失信"
        elif kept_ratio >= 0.7 and profile.avg_emotion <= 0.3:
            return "内耗型自毁"
        elif kept_ratio >= 0.7 and profile.avg_emotion >= 0.7:
            return "稳定型自律"
        elif kept_ratio >= 0.7:
            return "外耗型守信"
        else:
            return "波动型摇摆"

    def _generate_event_dna(self, ev: SevenFactorEvent) -> str:
        """生成事件DNA"""
        raw = f"{ev.entity_id}:{ev.promise}:{ev.fulfilled}:{ev.timestamp}:{self._device_fingerprint}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        from datetime import datetime as dt
        d = dt.fromisoformat(ev.timestamp.replace("Z", "+00:00"))
        return f"#七因⚡️{d.strftime('%Y%m%d%H%M')}-{h}"

    def _generate_behavior_dna(self, profile: EntityProfile) -> str:
        """生成行为DNA（不可逆哈希）"""
        raw = (
            f"{profile.entity_id}:"
            f"{profile.promises_kept}:{profile.promises_broken}:"
            f"{profile.avg_emotion}:{profile.behavior_pattern}:"
            f"{self._device_fingerprint}"
        )
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return f"七因-{profile.entity_type[:1].upper()}-{h}"

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 查询接口
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def get_score(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """查询信用分"""
        profile = self._profiles.get(entity_id)
        if not profile:
            return None
        return {
            "entity_id": profile.entity_id,
            "entity_type": profile.entity_type,
            "current_score": profile.current_score,
            "promises_made": profile.promises_made,
            "promises_kept": profile.promises_kept,
            "promises_broken": profile.promises_broken,
            "kept_ratio": round(
                profile.promises_kept / max(1, profile.promises_made), 2
            ),
            "behavior_pattern": profile.behavior_pattern,
            "avg_emotion": profile.avg_emotion,
            "last_updated": profile.last_updated,
        }

    def get_dna(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """查询行为DNA"""
        profile = self._profiles.get(entity_id)
        if not profile:
            return None
        return {
            "entity_id": profile.entity_id,
            "behavior_dna": profile.behavior_dna,
            "behavior_pattern": profile.behavior_pattern,
            "total_events": profile.total_events,
            "device_bound": True,
        }

    def get_pattern(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """查询行为模式"""
        profile = self._profiles.get(entity_id)
        if not profile:
            return None
        recent = [
            asdict(self._events[eid])
            for eid in profile.recent_events[-5:]
            if eid in self._events
        ]
        return {
            "entity_id": profile.entity_id,
            "behavior_pattern": profile.behavior_pattern,
            "kept_ratio": round(
                profile.promises_kept / max(1, profile.promises_made), 2
            ),
            "avg_emotion": profile.avg_emotion,
            "risk_level": self._risk_level(profile),
            "recent_events": recent,
        }

    def get_history(self, entity_id: str, limit: int = 50) -> Dict[str, Any]:
        """查询历史行为记录"""
        profile = self._profiles.get(entity_id)
        if not profile:
            return {"entity_id": entity_id, "events": [], "total": 0}
        event_ids = profile.recent_events[-limit:]
        events = [
            asdict(self._events[eid])
            for eid in event_ids if eid in self._events
        ]
        return {
            "entity_id": entity_id,
            "entity_type": profile.entity_type,
            "total_events": profile.total_events,
            "events": list(reversed(events)),
            "dna": profile.behavior_dna,
        }

    def _risk_level(self, profile: EntityProfile) -> str:
        """信用风险等级"""
        if profile.current_score >= 80:
            return "🟢 低风险"
        elif profile.current_score >= 50:
            return "🟡 中风险"
        elif profile.current_score >= 30:
            return "🟠 高风险"
        else:
            return "🔴 极高风险"

    def list_all_entities(self) -> List[Dict[str, Any]]:
        """列出所有实体"""
        result = []
        for eid, profile in self._profiles.items():
            result.append({
                "entity_id": eid,
                "entity_type": profile.entity_type,
                "score": profile.current_score,
                "pattern": profile.behavior_pattern,
                "total_events": profile.total_events,
            })
        return sorted(result, key=lambda x: x["score"], reverse=True)

    def calculate_dashboard_data(self) -> Dict[str, Any]:
        """仪表盘聚合数据"""
        if not self._profiles:
            return {"entities": 0, "total_events": 0, "avg_score": 100.0}

        scores = [p.current_score for p in self._profiles.values()]
        patterns = defaultdict(int)
        for p in self._profiles.values():
            patterns[p.behavior_pattern] += 1

        return {
            "entities": len(self._profiles),
            "total_events": sum(p.total_events for p in self._profiles.values()),
            "avg_score": round(sum(scores) / len(scores), 2),
            "max_score": round(max(scores), 2),
            "min_score": round(min(scores), 2),
            "pattern_distribution": dict(patterns),
            "high_risk_count": sum(1 for s in scores if s < 50),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }


# ═══════════════════════════════════════════════════════════
# 单例
# ═══════════════════════════════════════════════════════════

_engine: Optional[SevenFactorEngine] = None

def get_engine() -> SevenFactorEngine:
    global _engine
    if _engine is None:
        _engine = SevenFactorEngine()
    return _engine


# ═══════════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    engine = SevenFactorEngine()

    # 模拟：老大下令部署 → 按时完成
    ev1 = engine.submit_event("UID9622", {
        "entity_type": "user",
        "promise": "今晚8点前搞定部署",
        "promised_deadline": "2026-07-25T20:00:00",
        "fulfilled": True,
        "fulfillment_detail": "8点前部署完成，全绿通过",
        "actual_time": "2026-07-25T19:30:00",
        "emotion": "心甘情愿",
        "audience": "老大",
        "explanation": "不解释",
        "admit": "真改",
        "source": "如意总开关",
    })
    print(f"✅ 兑现事件: credit_delta={ev1.credit_delta}, DNA={ev1.dna}")

    # 模拟：某AI承诺3次均未兑现且爱解释
    for i in range(3):
        ev = engine.submit_event("AI-TEST-001", {
            "entity_type": "persona",
            "promise": f"完成任务#{i+1}",
            "promised_deadline": "2026-07-25T12:00:00",
            "fulfilled": False,
            "fulfillment_detail": "未完成",
            "emotion": "中性",
            "audience": "老大",
            "explanation": "过度解释",
            "admit": "硬扛",
            "source": "TeamOrchestrator",
        })
        print(f"❌ 失信事件#{i+1}: credit_delta={ev.credit_delta}")

    # 查询结果
    score = engine.get_score("AI-TEST-001")
    pattern = engine.get_pattern("AI-TEST-001")
    print(f"\n📊 AI-TEST-001 信用分: {score['current_score']}")
    print(f"📊 行为模式: {pattern['behavior_pattern']}")
    print(f"📊 风险等级: {pattern['risk_level']}")

    print(f"\n🟢 UID9622 信用分: {engine.get_score('UID9622')['current_score']}")
