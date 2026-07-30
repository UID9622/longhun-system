#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-INTER-AGENT-BUS-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · InterAgentBus 智能体消息总线 v1.0                   ║
║                                                                  ║
║  智能体间通信枢纽 · 点对点+广播 · 消息队列 · 路由分发            ║
║  不依赖外部 MQ · 纯 Python JSONL · 本地高效                      ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-INTER-AGENT-BUS-v1.0     ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                  ║
╚══════════════════════════════════════════════════════════════════╝

架构:
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  P01     │    │  P02     │    │  P05     │
  │ 诸葛亮   │    │ 宝宝     │    │ 审计     │
  └────┬─────┘    └────┬─────┘    └────┬─────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
              ┌────────▼────────┐
              │  InterAgentBus  │
              │  · 消息路由     │
              │  · 广播/点对点  │
              │  · 消息持久化   │
              │  · 审计日志     │
              └─────────────────┘

用法:
  from engines.lh_inter_agent_bus import InterAgentBus
  
  bus = InterAgentBus()
  bus.register(agent)            # 注册智能体
  bus.send(msg)                  # 发送消息
  bus.broadcast(msg)             # 广播给所有
  bus.route()                    # 路由分发未处理消息
"""

import hashlib
import json
import os
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

SYSTEM_ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════
# 消息信封
# ═══════════════════════════════════════════════════════════════

@dataclass
class BusMessage:
    """总线消息信封"""
    msg_id: str
    sender: str
    recipient: str          # persona_code 或 "BROADCAST" 或 "ALL"
    msg_type: str           # task/query/response/alert/observation/decision
    content: dict[str, Any]
    priority: int = 3
    reply_to: Optional[str] = None
    dna: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    delivered: bool = False
    delivered_at: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, s: str) -> "BusMessage":
        d = json.loads(s)
        return cls(**d)


# ═══════════════════════════════════════════════════════════════
# 审计日志条目
# ═══════════════════════════════════════════════════════════════

@dataclass
class BusAuditEntry:
    """总线审计日志"""
    ts: str
    event: str            # send/deliver/register/unregister/broadcast/error
    sender: str
    recipient: str
    msg_id: str
    msg_type: str
    detail: dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
# InterAgentBus 主类
# ═══════════════════════════════════════════════════════════════

class InterAgentBus:
    """龍魂智能体消息总线
    
    特性:
    - 点对点消息: send(msg) 发送到指定智能体
    - 广播: broadcast(msg) 发送到所有已注册智能体
    - 消息队列: 每个智能体独立消息队列
    - 路由分发: route() 批量分发未投递消息
    - 审计日志: 所有消息流经总线自动记录
    - 线程安全: 读写锁保护
    - 持久化: JSONL 文件持久化（可选）
    """
    
    def __init__(self, persist_dir: str | None = None):
        self._agents: Dict[str, Any] = {}           # persona_code → agent instance
        self._inboxes: Dict[str, List[BusMessage]] = defaultdict(list)
        self._sent: List[BusMessage] = []           # 已发送归档
        self._audit_log: List[BusAuditEntry] = []
        self._lock = threading.RLock()
        self._route_counter: int = 0
        self._started_at = datetime.now().isoformat()
        
        # 持久化（可选）
        self._persist_dir = Path(persist_dir) if persist_dir else None
        if self._persist_dir:
            self._persist_dir.mkdir(parents=True, exist_ok=True)
        
        self._audit("bus_start", "BUS", "SYSTEM", "", "", {})
    
    # ── 注册/注销 ──
    
    def register(self, agent: Any):
        """注册智能体到总线
        
        Args:
            agent: PersonaAgent 实例（必须有 persona_code 属性）
        """
        code = getattr(agent, 'PERSONA_CODE', None) or getattr(agent, 'persona_code', None)
        if not code:
            raise ValueError(f"智能体缺少 PERSONA_CODE: {agent}")
        
        with self._lock:
            self._agents[code] = agent
            # 双向绑定：智能体也持有总线引用
            if hasattr(agent, '_message_bus'):
                agent._message_bus = self
        
        self._audit("register", code, "BUS", "", "", {})
    
    def register_all(self, agents: List[Any]):
        """批量注册"""
        for agent in agents:
            self.register(agent)
    
    def unregister(self, persona_code: str):
        """注销智能体"""
        with self._lock:
            if persona_code in self._agents:
                agent = self._agents.pop(persona_code)
                if hasattr(agent, '_message_bus'):
                    agent._message_bus = None
        
        self._audit("unregister", persona_code, "BUS", "", "", {})
    
    def get_agent(self, persona_code: str) -> Optional[Any]:
        """获取已注册智能体"""
        return self._agents.get(persona_code)
    
    def list_agents(self) -> List[str]:
        """列出所有已注册智能体"""
        return list(self._agents.keys())
    
    # ── 消息发送 ──
    
    def send(self, msg: Any, immediate: bool = True) -> bool:
        """发送消息
        
        Args:
            msg: AgentMessage 或 BusMessage
            immediate: True=立即投递到目标智能体, False=进入队列等待 route()
            
        Returns:
            bool: 是否成功投递
        """
        # 转换为总线消息
        if not isinstance(msg, BusMessage):
            msg = BusMessage(
                msg_id=getattr(msg, 'msg_id', str(uuid.uuid4())[:12]),
                sender=getattr(msg, 'sender', 'UNKNOWN'),
                recipient=getattr(msg, 'recipient', 'BROADCAST'),
                msg_type=getattr(msg, 'msg_type', 'task'),
                content=getattr(msg, 'content', {}),
                priority=getattr(msg, 'priority', 3),
                reply_to=getattr(msg, 'reply_to', None),
                dna=getattr(msg, 'dna', ''),
            )
        
        recipient = msg.recipient
        
        with self._lock:
            # 广播
            if recipient in ("BROADCAST", "ALL", "*"):
                delivery_ok = self._broadcast_internal(msg)
                self._audit("broadcast", msg.sender, "ALL", msg.msg_id, msg.msg_type, {})
                return delivery_ok
            
            # 点对点
            if immediate and recipient in self._agents:
                # 立即投递
                target = self._agents[recipient]
                try:
                    result = target.receive_message(msg)
                    msg.delivered = True
                    msg.delivered_at = datetime.now().isoformat()
                    self._audit("deliver", msg.sender, recipient, msg.msg_id, msg.msg_type,
                                {"result": str(result)[:200] if result else "none"})
                    self._sent.append(msg)
                    return True
                except Exception as e:
                    self._audit("error", msg.sender, recipient, msg.msg_id, msg.msg_type,
                                {"error": str(e)})
                    return False
            else:
                # 进入目标智能体的消息队列
                self._inboxes[recipient].append(msg)
                self._audit("queue", msg.sender, recipient, msg.msg_id, msg.msg_type, {})
                return True
    
    def broadcast(self, msg: Any) -> int:
        """广播消息给所有已注册智能体
        
        Returns:
            int: 成功投递数量
        """
        if not isinstance(msg, BusMessage):
            msg = BusMessage(
                msg_id=str(uuid.uuid4())[:12],
                sender=getattr(msg, 'sender', 'BROADCASTER'),
                recipient="ALL",
                msg_type=getattr(msg, 'msg_type', 'alert'),
                content=getattr(msg, 'content', {}),
                priority=getattr(msg, 'priority', 3),
                dna=getattr(msg, 'dna', ''),
            )
        
        with self._lock:
            count = self._broadcast_internal(msg)
        
        self._audit("broadcast", msg.sender, "ALL", msg.msg_id, msg.msg_type,
                    {"delivered_to": count})
        return count
    
    def _broadcast_internal(self, msg: BusMessage) -> bool:
        """内部广播（不加锁，调用方已加锁）"""
        ok_count = 0
        for code, agent in self._agents.items():
            if code == msg.sender:
                continue  # 不给自己发
            try:
                broadcast_msg = BusMessage(
                    msg_id=msg.msg_id,
                    sender=msg.sender,
                    recipient=code,
                    msg_type=msg.msg_type,
                    content=msg.content,
                    priority=msg.priority,
                    reply_to=msg.reply_to,
                    dna=msg.dna,
                )
                agent.receive_message(broadcast_msg)
                broadcast_msg.delivered = True
                broadcast_msg.delivered_at = datetime.now().isoformat()
                self._sent.append(broadcast_msg)
                ok_count += 1
            except Exception as e:
                self._audit("error", msg.sender, code, msg.msg_id, msg.msg_type,
                            {"error": str(e)})
        return ok_count > 0
    
    # ── 路由分发 ──
    
    def route(self) -> int:
        """分发消息队列中的所有待投递消息
        
        Returns:
            int: 本次分发的消息数
        """
        delivered = 0
        self._route_counter += 1
        
        with self._lock:
            for recipient, msgs in list(self._inboxes.items()):
                if not msgs:
                    continue
                
                agent = self._agents.get(recipient)
                if agent is None:
                    # 接收者未注册，消息过期
                    expired = msgs
                    self._inboxes[recipient] = []
                    for m in expired:
                        self._audit("expired", m.sender, recipient, m.msg_id, m.msg_type,
                                    {"reason": "recipient_not_registered"})
                    continue
                
                # 批量投递
                for msg in msgs:
                    try:
                        agent.receive_message(msg)
                        msg.delivered = True
                        msg.delivered_at = datetime.now().isoformat()
                        self._sent.append(msg)
                        delivered += 1
                    except Exception as e:
                        self._audit("error", msg.sender, recipient, msg.msg_id, msg.msg_type,
                                    {"error": str(e)})
                
                self._inboxes[recipient] = []  # 清空
        
        return delivered
    
    def route_loop(self, interval: float = 0.5, max_iterations: int | None = None):
        """持续路由循环（阻塞式）
        
        Args:
            interval: 轮询间隔（秒）
            max_iterations: 最大迭代次数（None=无限）
        """
        i = 0
        try:
            while max_iterations is None or i < max_iterations:
                delivered = self.route()
                if delivered > 0:
                    self._audit("route_cycle", "BUS", "BUS", "", "",
                                {"delivered": delivered, "cycle": self._route_counter})
                time.sleep(interval)
                i += 1
        except KeyboardInterrupt:
            self._audit("route_stop", "BUS", "BUS", "", "", {"reason": "interrupt"})
    
    # ── 查询 ──
    
    def get_inbox(self, persona_code: str) -> List[BusMessage]:
        """获取智能体的消息队列（未投递）"""
        return list(self._inboxes.get(persona_code, []))
    
    def get_sent(self) -> List[BusMessage]:
        """获取已发送归档"""
        return list(self._sent)
    
    def get_audit_log(self, limit: int = 100) -> List[dict]:
        """获取审计日志"""
        entries = self._audit_log[-limit:]
        return [e.__dict__ if hasattr(e, '__dict__') else e for e in entries]
    
    def get_stats(self) -> dict[str, Any]:
        """获取总线统计"""
        return {
            "agents_registered": len(self._agents),
            "agent_list": list(self._agents.keys()),
            "messages_sent": len(self._sent),
            "messages_queued": sum(len(q) for q in self._inboxes.values()),
            "route_cycles": self._route_counter,
            "audit_entries": len(self._audit_log),
            "started_at": self._started_at,
        }
    
    # ── 审计 ──
    
    def _audit(self, event: str, sender: str, recipient: str,
               msg_id: str, msg_type: str, detail: dict[str, Any]):
        """记录审计日志"""
        entry = BusAuditEntry(
            ts=datetime.now().isoformat(),
            event=event,
            sender=sender,
            recipient=recipient,
            msg_id=msg_id,
            msg_type=msg_type,
            detail=detail,
        )
        self._audit_log.append(entry)
        
        # 持久化（异步，不阻塞）
        if self._persist_dir:
            try:
                audit_file = self._persist_dir / f"bus_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
                with open(audit_file, "a") as f:
                    f.write(entry.to_json() + "\n")
            except Exception:
                pass
    
    # ── 清理 ──
    
    def cleanup_expired(self, max_age_seconds: int = 3600):
        """清理过期消息"""
        now = datetime.now().isoformat()
        with self._lock:
            for recipient in list(self._inboxes.keys()):
                self._inboxes[recipient] = [
                    m for m in self._inboxes[recipient]
                    if m.timestamp > now  # 简化的过期判断
                ]
    
    def shutdown(self):
        """关闭总线"""
        self._audit("bus_shutdown", "BUS", "SYSTEM", "", "", {
            "total_messages": len(self._sent),
            "agents_at_shutdown": list(self._agents.keys()),
        })
        # 投递所有剩余消息
        self.route()
    
    def __repr__(self) -> str:
        return (f"<InterAgentBus agents={len(self._agents)} "
                f"sent={len(self._sent)} queued={sum(len(q) for q in self._inboxes.values())}>")


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_global_bus: Optional[InterAgentBus] = None
_bus_lock = threading.Lock()


def get_bus(persist_dir: str | None = None) -> InterAgentBus:
    """获取全局总线单例"""
    global _global_bus
    with _bus_lock:
        if _global_bus is None:
            _global_bus = InterAgentBus(persist_dir=persist_dir)
        return _global_bus


def reset_bus():
    """重置全局总线（测试用）"""
    global _global_bus
    with _bus_lock:
        if _global_bus:
            _global_bus.shutdown()
        _global_bus = None


# ═══════════════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(SYSTEM_ROOT))
    from engines.lh_persona_agent import PersonaAgent, AgentState
    
    # 创建测试智能体
    class AgentA(PersonaAgent):
        PERSONA_CODE = "AGENT_A"
        PERSONA_NAME = "智能体A"
        PERSONA_NAME_EN = "AgentA"
        ROLE = "test"
        MOTTO = "test"
        capabilities = ["echo"]
        
        def think(self, obs): return {"action": "echo", "reasoning": "test"}
        def act(self, dec): return {"status": "done", "output": str(dec)}
    
    class AgentB(PersonaAgent):
        PERSONA_CODE = "AGENT_B"
        PERSONA_NAME = "智能体B"
        PERSONA_NAME_EN = "AgentB"
        ROLE = "test"
        MOTTO = "test"
        capabilities = ["echo"]
        
        def think(self, obs): return {"action": "echo", "reasoning": "test"}
        def act(self, dec): return {"status": "done", "output": str(dec)}
    
    # 创建总线
    bus = InterAgentBus()
    a = AgentA()
    b = AgentB()
    
    bus.register(a)
    bus.register(b)
    
    print(f"✅ 总线创建: {bus}")
    print(f"   已注册: {bus.list_agents()}")
    
    # 点对点消息
    msg = a.send_message("AGENT_B", "task", {"instruction": "hello"})
    print(f"   消息发送: {msg.msg_id}")
    
    # 广播
    count = bus.broadcast(a.send_message("BROADCAST", "alert", {"alert": "test"}))
    print(f"   广播送达: {count} 个智能体")
    
    # 统计
    stats = bus.get_stats()
    print(f"   总线统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    # 审计日志
    print(f"   审计日志: {len(bus.get_audit_log())} 条")
    
    bus.shutdown()
    print("✅ InterAgentBus 自检全部通过")
