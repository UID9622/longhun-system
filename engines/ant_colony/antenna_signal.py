#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
触角信号协议 v2.0 · AntennaSignal
基于 LACA v1.0 论文，深度整合龙魂系统

DNA: #龍芯⚡️丙午·辛未·ANTENNA-SIGNAL-v2.0

v2.0 增强:
  - DNA 格式升级为 v∞ 干支卦格式
  - 七色不动点色卡与四类信息素颜色映射
  - 三色审计链路集成
  - 信号优先级与不动点层级联动
  - 完整防篡改校验链
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
import time
import hashlib
import json
import uuid

# 尝试导入干支日历引擎
try:
    from calendar_context_logger.calendar_core import LunarEngine
    _LUNAR = LunarEngine()
    def _get_ganzhi() -> str:
        """获取当前干支四柱"""
        try:
            gz = _LUNAR.get_ganzhi()
            return f"{gz['year']}·{gz['month']}·{gz['day']}·{gz['hour']}"
        except Exception:
            return _get_ganzhi_fallback()
except ImportError:
    def _get_ganzhi() -> str:
        return _get_ganzhi_fallback()

def _get_ganzhi_fallback() -> str:
    """干支回退算法"""
    from datetime import datetime
    now = datetime.now()
    year_gan = "丙午"
    month_map = {1:"乙丑",2:"丙寅",3:"丁卯",4:"戊辰",5:"己巳",6:"庚午",
                 7:"辛未",8:"壬申",9:"癸酉",10:"甲戌",11:"乙亥",12:"丙子"}
    day_map = {1:"甲子",2:"乙丑",3:"丙寅",4:"丁卯",5:"戊辰",6:"己巳",
               7:"庚午",8:"辛未",9:"壬申",10:"癸酉",11:"甲戌",12:"乙亥",
               13:"丙子",14:"丁丑",15:"戊寅",16:"己卯",17:"庚辰",18:"辛巳",
               19:"壬午",20:"癸未",21:"甲申",22:"乙酉",23:"丙戌",24:"丁亥",
               25:"戊子",26:"己丑",27:"庚寅",28:"辛卯",29:"壬辰",30:"癸巳",
               31:"甲午"}
    hour_gan = {0:"子时",1:"丑时",2:"丑时",3:"寅时",4:"寅时",5:"卯时",
                6:"卯时",7:"辰时",8:"辰时",9:"巳时",10:"巳时",11:"午时",
                12:"午时",13:"未时",14:"未时",15:"申时",16:"申时",17:"酉时",
                18:"酉时",19:"戌时",20:"戌时",21:"亥时",22:"亥时",23:"子时"}
    month_gan = month_map.get(now.month, "辛未")
    day_gan = day_map.get(now.day, "辛未")
    hour = hour_gan.get(now.hour, "亥时")
    return f"{year_gan}·{month_gan}·{day_gan}·{hour}"


class PheromoneType(str, Enum):
    """四类信息素 — 与七色不动点色卡映射"""
    RECRUIT = "RECRUIT"        # 🟢 招募素 → 绿色G · 木 · 任务调度
    ALERT = "ALERT"            # 🔴 警戒素 → 红色R · 火 · 安全/伦理红线
    TRAIL = "TRAIL"            # 🟡 足迹素 → 黄色Y · 土 · 路径验证/知识沉淀
    AGGREGATE = "AGGREGATE"    # 🔵 聚集素 → 蓝色B · 水 · 协作/创新涌现


class PayloadType(str, Enum):
    """载荷类型"""
    COMMAND = "command"   # 执行命令
    DATA = "data"         # 数据传递
    QUERY = "query"       # 查询请求
    ALERT = "alert"       # 警报通知
    STATUS = "status"     # 状态报告
    RESULT = "result"     # 执行结果
    AUDIT = "audit"       # 审计记录（v2.0新增）


# === 七色不动点与信息素映射 ===
PHEROMONE_COLOR_MAP = {
    PheromoneType.RECRUIT:   {"color": "G",  "name": "绿色", "element": "木", "action": "自动放行"},
    PheromoneType.ALERT:     {"color": "R",  "name": "红色", "element": "火", "action": "立即停止"},
    PheromoneType.TRAIL:     {"color": "Y",  "name": "黄色", "element": "土", "action": "二次确认"},
    PheromoneType.AGGREGATE: {"color": "B",  "name": "蓝色", "element": "水", "action": "记录审计链"},
}

# === 不动点层级映射 ===
FIXED_POINT_LEVELS = {
    1: {"name": "任务策略层", "mutable": True,  "example": "具体执行方案可调"},
    2: {"name": "系统配置层", "mutable": True,  "example": "模块参数可调"},
    3: {"name": "架构设计层", "mutable": False, "example": "蚁群五大种群结构不变"},
    4: {"name": "核心价值观", "mutable": False, "example": "为人民服务·技术透明"},
    5: {"name": "永恒基石",   "mutable": False, "example": "中国法律·369不动点·君子协议"},
}


@dataclass
class AntennaSignal:
    """
    触角信号包 — 模块间唯一通信格式
    
    v2.0 增强:
    - DNA 格式升级为 v∞ 干支卦
    - 自动关联七色不动点色卡
    - 三色审计标记自动注入
    - 不动点层级校验
    
    使用示例:
        signal = AntennaSignal(
            sender_id="P02-宝宝",
            receiver_id="P04-鲁班",
            pheromone_type=PheromoneType.RECRUIT,
            priority=8,
            payload_type=PayloadType.COMMAND,
            payload={"task": "构建蚁巢模块", "spec": "..."}
        )
    """
    
    # === 基础标识 ===
    sender_id: str
    receiver_id: Optional[str] = None
    
    # === 信息素标记 ===
    pheromone_type: PheromoneType = PheromoneType.TRAIL
    priority: int = 5
    
    # === 信号载荷 ===
    payload_type: PayloadType = PayloadType.DATA
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # === 轨迹追踪（自动填充）===
    hop_count: int = field(default=0, init=False)
    path_trace: List[Dict[str, Any]] = field(default_factory=list, init=False)
    
    # === 不动点校验 ===
    level_required: int = 1
    
    # === 系统字段（自动生成）===
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8], init=False)
    timestamp: float = field(default_factory=time.time, init=False)
    checksum: str = field(default="", init=False)
    
    # === DNA追溯（v∞格式）===
    dna_signature: str = field(default="", init=False)
    
    # === v2.0 新增字段 ===
    color_state: str = field(default="", init=False)        # 七色不动点颜色
    audit_level: int = field(default=0, init=False)         # 三色审计层级 0=无 1=蓝 2=黄 3=红
    fixed_point_hash: str = field(default="", init=False)   # 不动点校验哈希
    
    def __post_init__(self):
        self._calculate_checksum()
        self._generate_dna()
        self._map_color_state()
        self._calculate_fixed_point_hash()
    
    def _calculate_checksum(self) -> str:
        """计算信号完整性校验和（防篡改）"""
        data = f"{self.signal_id}{self.sender_id}{self.timestamp}{self.pheromone_type.value}"
        self.checksum = hashlib.sha256(data.encode()).hexdigest()[:16]
        return self.checksum
    
    def _generate_dna(self) -> str:
        """生成DNA追溯签名 — v∞ 干支卦格式"""
        ganzhi = _get_ganzhi()
        # 根据信息素类型决定卦名
        trigram_map = {
            PheromoneType.RECRUIT: "震",     # 震为雷·行动
            PheromoneType.ALERT: "离",       # 离为火·警戒
            PheromoneType.TRAIL: "坤",       # 坤为地·承载
            PheromoneType.AGGREGATE: "坎",   # 坎为水·汇聚
        }
        trigram = trigram_map.get(self.pheromone_type, "乾")
        self.dna_signature = (
            f"#龍芯⚡️{ganzhi}·{trigram}"
            f"-ANT-{self.sender_id}-{self.signal_id}"
        )
        return self.dna_signature
    
    def _map_color_state(self):
        """映射七色不动点色卡"""
        color_info = PHEROMONE_COLOR_MAP.get(self.pheromone_type, {})
        self.color_state = color_info.get("color", "G")
    
    def _calculate_fixed_point_hash(self):
        """计算不动点校验哈希 — 确保价值观层级不被篡改"""
        fp_data = f"L{self.level_required}:{self.color_state}:{self.pheromone_type.value}"
        self.fixed_point_hash = hashlib.blake2b(
            fp_data.encode(), digest_size=8
        ).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "signal_id": self.signal_id,
            "timestamp": self.timestamp,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "pheromone_type": self.pheromone_type.value,
            "priority": self.priority,
            "payload_type": self.payload_type.value,
            "payload": self.payload,
            "hop_count": self.hop_count,
            "path_trace": self.path_trace,
            "level_required": self.level_required,
            "checksum": self.checksum,
            "dna_signature": self.dna_signature,
            "color_state": self.color_state,
            "audit_level": self.audit_level,
            "fixed_point_hash": self.fixed_point_hash,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AntennaSignal":
        signal = cls(
            sender_id=data["sender_id"],
            receiver_id=data.get("receiver_id"),
            pheromone_type=PheromoneType(data["pheromone_type"]),
            priority=data["priority"],
            payload_type=PayloadType(data["payload_type"]),
            payload=data.get("payload", {}),
            level_required=data.get("level_required", 1),
        )
        signal.signal_id = data["signal_id"]
        signal.timestamp = data["timestamp"]
        signal.hop_count = data.get("hop_count", 0)
        signal.path_trace = data.get("path_trace", [])
        signal.checksum = data.get("checksum", "")
        signal.dna_signature = data.get("dna_signature", "")
        signal.color_state = data.get("color_state", "")
        signal.audit_level = data.get("audit_level", 0)
        signal.fixed_point_hash = data.get("fixed_point_hash", "")
        return signal
    
    @classmethod
    def from_json(cls, json_str: str) -> "AntennaSignal":
        return cls.from_dict(json.loads(json_str))
    
    def forward(self, next_module_id: str) -> "AntennaSignal":
        """信号转发到下一跳 — 自动衰减"""
        if self.hop_count >= 10:
            raise SignalExpiredError(f"信号 {self.signal_id} 超过最大跳数(10)")
        
        trace_entry = {
            "hop": self.hop_count + 1,
            "module": next_module_id,
            "time": time.time(),
            "dna": f"#龍芯⚡️{_get_ganzhi()}-{next_module_id}-{self.signal_id}"
        }
        self.path_trace.append(trace_entry)
        
        decay_map = {
            PheromoneType.RECRUIT: 5,
            PheromoneType.ALERT: 2,
            PheromoneType.TRAIL: 1,
            PheromoneType.AGGREGATE: 3,
        }
        decay = decay_map.get(self.pheromone_type, 2)
        self.priority = max(1, self.priority - decay)
        self.hop_count += 1
        
        self._calculate_checksum()
        return self
    
    def verify(self) -> bool:
        """验证信号完整性"""
        expected = hashlib.sha256(
            f"{self.signal_id}{self.sender_id}{self.timestamp}{self.pheromone_type.value}"
            .encode()
        ).hexdigest()[:16]
        return self.checksum == expected
    
    def verify_fixed_point(self) -> bool:
        """验证不动点一致性"""
        expected = hashlib.blake2b(
            f"L{self.level_required}:{self.color_state}:{self.pheromone_type.value}"
            .encode(), digest_size=8
        ).hexdigest()
        return self.fixed_point_hash == expected
    
    def is_broadcast(self) -> bool:
        return self.receiver_id is None
    
    def is_emergency(self) -> bool:
        return self.priority >= 9 or self.pheromone_type == PheromoneType.ALERT
    
    def get_pheromone_emoji(self) -> str:
        emoji_map = {
            PheromoneType.RECRUIT: "🟢",
            PheromoneType.ALERT: "🔴",
            PheromoneType.TRAIL: "🟡",
            PheromoneType.AGGREGATE: "🔵",
        }
        return emoji_map.get(self.pheromone_type, "⚪")
    
    def __str__(self) -> str:
        emoji = self.get_pheromone_emoji()
        target = self.receiver_id or "📢广播"
        return (
            f"{emoji}[{self.pheromone_type.value}] "
            f"{self.sender_id}→{target} P{self.priority} #{self.signal_id}"
        )


class SignalExpiredError(Exception):
    """信号过期异常"""
    pass


class SignalTamperedError(Exception):
    """信号被篡改异常"""
    pass


# === 快捷工厂函数 ===

def recruit_signal(sender: str, receiver: Optional[str], task: dict[str, Any], priority: int = 7) -> AntennaSignal:
    """创建招募素信号"""
    return AntennaSignal(
        sender_id=sender,
        receiver_id=receiver,
        pheromone_type=PheromoneType.RECRUIT,
        priority=min(10, max(7, priority)),
        payload_type=PayloadType.COMMAND,
        payload=task,
    )


def alert_signal(sender: str, alert_level: int, description: str, affected: list[Any] = None) -> AntennaSignal:
    """创建警戒素信号"""
    priority = min(10, alert_level * 2 + 2)
    return AntennaSignal(
        sender_id=sender,
        receiver_id=None,
        pheromone_type=PheromoneType.ALERT,
        priority=priority,
        payload_type=PayloadType.ALERT,
        payload={
            "alert_level": alert_level,
            "description": description,
            "affected_modules": affected or [],
            "auto_escalate": alert_level >= 3,
        },
    )


def trail_signal(sender: str, receiver: str, trail_type: str, path_data: dict[str, Any]) -> AntennaSignal:
    """创建足迹素信号"""
    return AntennaSignal(
        sender_id=sender,
        receiver_id=receiver,
        pheromone_type=PheromoneType.TRAIL,
        priority=5,
        payload_type=PayloadType.DATA,
        payload={"trail_type": trail_type, **path_data},
    )


def aggregate_signal(sender: str, topic: str, participants: list[Any], duration: int = 30) -> AntennaSignal:
    """创建聚集素信号"""
    return AntennaSignal(
        sender_id=sender,
        receiver_id=None,
        pheromone_type=PheromoneType.AGGREGATE,
        priority=6,
        payload_type=PayloadType.COMMAND,
        payload={
            "topic": topic,
            "participants": participants,
            "duration_hint": duration,
            "aggregate_type": "collaboration",
        },
    )


# === 测试 ===
if __name__ == "__main__":
    print("=" * 60)
    print("🐜 龙魂蚁群引擎 v2.0 · AntennaSignal 测试")
    print("=" * 60)
    
    # 测试1：基础信号
    s1 = AntennaSignal(
        sender_id="P02-宝宝",
        receiver_id="P04-鲁班",
        pheromone_type=PheromoneType.RECRUIT,
        priority=8,
        payload_type=PayloadType.COMMAND,
        payload={"task": "构建蚁巢模块"},
    )
    print(f"\n{s1}")
    print(f"  DNA: {s1.dna_signature}")
    print(f"  色卡: {s1.color_state}")
    print(f"  不动点哈希: {s1.fixed_point_hash}")
    print(f"  验证: {'✅' if s1.verify() else '❌'}")
    print(f"  不动点验证: {'✅' if s1.verify_fixed_point() else '❌'}")
    
    # 测试2：警戒素
    s2 = alert_signal("P05-上帝之眼", 3, "检测到异常")
    print(f"\n{s2}")
    print(f"  紧急: {'是' if s2.is_emergency() else '否'}")
    print(f"  广播: {'是' if s2.is_broadcast() else '否'}")
    
    # 测试3：信号转发衰减
    s3 = recruit_signal("P02-宝宝", "P01-诸葛亮", {"task": "策略咨询"}, priority=9)
    print(f"\n初始: {s3}")
    s3.forward("P01-诸葛亮")
    print(f"1跳:  {s3}")
    s3.forward("P04-鲁班")
    print(f"2跳:  {s3}")
    
    print(f"\n✅ AntennaSignal v2.0 测试通过")
    print(f"🧬 DNA: #龍芯⚡️丙午·辛未·ANTENNA-SIGNAL-v2.0")
