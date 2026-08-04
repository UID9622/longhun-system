#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-AGENT-BASE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · PersonaAgent 智能体基类 v1.0                        ║
║                                                                  ║
║  标准 Agent 接口：observe → think → act → communicate            ║
║  20 人格统一基类 · 状态管理 · DNA 追溯 · 消息收发                ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-AGENT-BASE-v1.0  ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                  ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  from engines.lh_persona_agent import PersonaAgent, AgentState, AgentMessage
  
  class MyPersona(PersonaAgent):
      def think(self, observation: dict[str, Any]) -> dict[str, Any]:
          ...
      def act(self, decision: dict[str, Any]) -> dict[str, Any]:
          ...
"""

import hashlib
import json
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

SYSTEM_ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════
# 基础类型
# ═══════════════════════════════════════════════════════════════

class AgentState(Enum):
    """智能体状态"""
    IDLE = "idle"           # 空闲·等待任务
    OBSERVING = "observing" # 观察中·收集信息
    THINKING = "thinking"   # 思考中·推理决策
    ACTING = "acting"       # 执行中·落地动作
    WAITING = "waiting"     # 等待中·等待其他智能体响应
    DONE = "done"           # 完成
    ERROR = "error"         # 出错
    MELTDOWN = "meltdown"   # 熔断


@dataclass
class AgentMessage:
    """智能体间消息"""
    msg_id: str
    sender: str            # 发送者 persona_code 如 "P01"
    recipient: str         # 接收者 persona_code 或 "BROADCAST"
    msg_type: str          # task/query/response/alert/observation/decision
    content: dict          # 消息体
    priority: int = 3      # 1=紧急 2=高 3=普通 4=低
    reply_to: Optional[str] = None  # 回复哪条消息
    dna: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    ttl: int = 300         # 秒·超时自动丢弃
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
    
    @classmethod
    def from_json(cls, s: str) -> "AgentMessage":
        return cls(**json.loads(s))


@dataclass
class AgentContext:
    """智能体运行时上下文"""
    persona_code: str
    session_id: str
    state: AgentState = AgentState.IDLE
    task_queue: List[AgentMessage] = field(default_factory=list)
    observation: dict[str, Any] = field(default_factory=dict)
    working_memory: dict[str, Any] = field(default_factory=dict)
    last_decision: dict[str, Any] = field(default_factory=dict)
    last_action: dict[str, Any] = field(default_factory=dict)
    history: List[dict] = field(default_factory=list)
    dna_chain: List[str] = field(default_factory=list)
    error_count: int = 0
    meltdown_threshold: int = 3
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════════════
# PersonaAgent 基类
# ═══════════════════════════════════════════════════════════════

class PersonaAgent(ABC):
    """龍魂智能体基类 — 所有人格执行器继承此类
    
    标准生命周期:
      observe() → think() → act() → [communicate()] → done
    
    每个智能体:
      - 有独立身份 (persona_code, dna)
      - 有自己的 SYSTEM_PROMPT
      - 有自己的能力列表 (capabilities)
      - 可以收发消息 (send_message / receive_message)
      - 有状态机 (idle → observing → thinking → acting → done)
      - 所有动作绑 DNA 追溯
    """
    
    # ── 子类必须覆写 ──
    PERSONA_CODE: str = ""          # 如 "P01"
    PERSONA_NAME: str = ""          # 如 "诸葛亮"
    PERSONA_NAME_EN: str = ""       # 如 "Zhuge Liang"
    ROLE: str = ""                  # 职能标签
    MOTTO: str = ""                 # 座右铭
    TRUST_LEVEL: str = "L3"        # 信任级别
    
    # ── 子类应覆写 ──
    TRIGGERS: List[str] = []
    SYSTEM_PROMPT: str = ""
    capabilities: List[str] = []
    
    # ── 运行时注入 ──
    _message_bus: Optional[Any] = None   # InterAgentBus 引用
    _blackboard: Optional[Any] = None    # SharedBlackboard 引用
    
    def __init__(self):
        self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.PERSONA_CODE}-AGENT-v1.0"
        self.ctx = AgentContext(persona_code=self.PERSONA_CODE, session_id=str(uuid.uuid4())[:8])
        self.system_root = SYSTEM_ROOT
        self._handlers: Dict[str, Callable] = {}
        self._register_default_handlers()
    
    # ── 身份 ──
    
    @property
    def persona_code(self) -> str:
        return self.PERSONA_CODE
    
    @property
    def persona_name(self) -> str:
        return self.PERSONA_NAME
    
    @property
    def state(self) -> AgentState:
        return self.ctx.state
    
    @state.setter
    def state(self, v: AgentState):
        old = self.ctx.state
        self.ctx.state = v
        if old != v:
            self._log_event("state_change", {"from": old.value, "to": v.value})
    
    # ── DNA 追溯 ──
    
    def _gen_dna(self, action: str) -> str:
        """生成操作 DNA"""
        now = datetime.now()
        raw = f"{self.PERSONA_CODE}:{action}:{now.isoformat()}:{uuid.uuid4().hex[:6]}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{now.strftime('%Y%m%d%H%M%S')}-{self.PERSONA_CODE}-{action}-{h}"
    
    def _log_event(self, event: str, detail: dict[str, Any]):
        """记录事件到历史"""
        entry = {
            "ts": datetime.now().isoformat(),
            "event": event,
            "persona": self.PERSONA_CODE,
            "dna": self._gen_dna(event),
            "detail": detail,
        }
        self.ctx.history.append(entry)
        self.ctx.dna_chain.append(entry["dna"])
    
    # ── 消息处理 ──
    
    def _register_default_handlers(self):
        """注册默认消息处理器"""
        self._handlers = {
            "task": self._handle_task,
            "query": self._handle_query,
            "observation": self._handle_observation,
            "alert": self._handle_alert,
            "response": self._handle_response,
        }
    
    def _handle_task(self, msg: AgentMessage) -> dict[str, Any]:
        """处理任务消息 → 触发标准循环"""
        return self.run(task=msg.content)
    
    def _handle_query(self, msg: AgentMessage) -> dict[str, Any]:
        """处理查询消息"""
        self.ctx.observation.update(msg.content)
        decision = self.think(self.ctx.observation)
        return self.act(decision)
    
    def _handle_observation(self, msg: AgentMessage) -> dict[str, Any]:
        """处理观察消息"""
        self.ctx.observation.update(msg.content)
        return {"status": "observed", "persona": self.PERSONA_CODE}
    
    def _handle_alert(self, msg: AgentMessage) -> dict[str, Any]:
        """处理告警消息"""
        # 高优先级告警 → 中断当前任务
        if msg.priority <= 2:
            self.ctx.working_memory["alert"] = msg.content
            decision = self.think({"alert": msg.content, **self.ctx.observation})
            return self.act(decision)
        return {"status": "alert_queued", "persona": self.PERSONA_CODE}
    
    def _handle_response(self, msg: AgentMessage) -> dict[str, Any]:
        """处理响应消息"""
        self.ctx.working_memory[f"response_{msg.sender}"] = msg.content
        return {"status": "response_received", "from": msg.sender}
    
    # ── 消息收发 ──
    
    def send_message(self, recipient: str, msg_type: str, content: dict[str, Any],
                     priority: int = 3, reply_to: str = None) -> AgentMessage:
        """发送消息到其他智能体"""
        msg = AgentMessage(
            msg_id=str(uuid.uuid4())[:12],
            sender=self.PERSONA_CODE,
            recipient=recipient,
            msg_type=msg_type,
            content=content,
            priority=priority,
            reply_to=reply_to,
            dna=self._gen_dna(f"msg_to_{recipient}"),
        )
        self._log_event("send_message", {
            "to": recipient, "type": msg_type, "msg_id": msg.msg_id
        })
        # 如果连接了消息总线，通过总线发送
        if self._message_bus:
            self._message_bus.send(msg)
        return msg
    
    def receive_message(self, msg: AgentMessage) -> Optional[dict]:
        """接收并处理消息"""
        self._log_event("receive_message", {
            "from": msg.sender, "type": msg.msg_type, "msg_id": msg.msg_id
        })
        handler = self._handlers.get(msg.msg_type)
        if handler:
            return handler(msg)
        return {"status": "unhandled", "type": msg.msg_type}
    
    def has_messages(self) -> bool:
        """是否有待处理消息"""
        return len(self.ctx.task_queue) > 0
    
    def process_queue(self) -> List[dict]:
        """处理消息队列中所有消息"""
        results = []
        while self.ctx.task_queue:
            msg = self.ctx.task_queue.pop(0)
            result = self.receive_message(msg)
            if result:
                results.append(result)
        return results
    
    # ── 标准生命周期 ──
    
    def observe(self) -> dict[str, Any]:
        """观察阶段：收集环境信息和上下文
        
        子类可覆写以增加特定领域的观察逻辑。
        """
        self.state = AgentState.OBSERVING
        self._log_event("observe_start", {})
        
        observation = {
            "persona": self.PERSONA_CODE,
            "timestamp": datetime.now().isoformat(),
            "working_memory": dict(self.ctx.working_memory),
            "task_queue_len": len(self.ctx.task_queue),
            "state": self.state.value,
        }
        
        # 从黑板读取共享上下文（如果连接）
        if self._blackboard:
            observation["blackboard"] = self._blackboard.read_all(self.PERSONA_CODE)
        
        self.ctx.observation = observation
        self._log_event("observe_done", {"keys": list(observation.keys())})
        return observation
    
    @abstractmethod
    def think(self, observation: dict[str, Any]) -> dict[str, Any]:
        """思考阶段：推理决策（子类必须实现）
        
        Args:
            observation: observe() 的输出
            
        Returns:
            decision: {action, reasoning, confidence, ...}
        """
        pass
    
    @abstractmethod
    def act(self, decision: dict[str, Any]) -> dict[str, Any]:
        """执行阶段：落地动作（子类必须实现）
        
        Args:
            decision: think() 的输出
            
        Returns:
            result: {status, output, dna, ...}
        """
        pass
    
    def run(self, task: dict[str, Any] = None) -> dict[str, Any]:
        """完整执行一次标准循环: observe → think → act
        
        Args:
            task: 可选·外部注入的任务
            
        Returns:
            result: 执行结果
        """
        try:
            # 1. 观察
            if task:
                self.ctx.observation.update(task)
            observation = self.observe()
            
            # 2. 思考
            self.state = AgentState.THINKING
            decision = self.think(observation)
            self.ctx.last_decision = decision
            
            # 3. 执行
            self.state = AgentState.ACTING
            result = self.act(decision)
            self.ctx.last_action = result
            
            self.state = AgentState.DONE
            self.ctx.error_count = 0
            result["dna"] = self._gen_dna("run")
            result["persona"] = self.PERSONA_CODE
            return result
            
        except Exception as e:
            self.ctx.error_count += 1
            if self.ctx.error_count >= self.ctx.meltdown_threshold:
                self.state = AgentState.MELTDOWN
                self._log_event("meltdown", {"error": str(e), "count": self.ctx.error_count})
                return {"status": "meltdown", "error": str(e), "persona": self.PERSONA_CODE}
            
            self.state = AgentState.ERROR
            self._log_event("error", {"error": str(e)})
            return {"status": "error", "error": str(e), "persona": self.PERSONA_CODE}
    
    # ── 协作 ──
    
    def collaborate(self, target_persona: str, task: dict[str, Any],
                    wait_for_response: bool = True) -> Optional[dict]:
        """请求另一个智能体协作
        
        Args:
            target_persona: 目标人格代码
            task: 任务内容
            wait_for_response: 是否等待响应
            
        Returns:
            响应内容（如果 wait_for_response=True 且有响应）
        """
        msg = self.send_message(target_persona, "task", task)
        
        if wait_for_response:
            # 等待响应（简化实现：轮询黑板）
            for _ in range(30):  # 最多等30秒
                if self._blackboard:
                    response = self._blackboard.read(
                        f"response:{msg.msg_id}", self.PERSONA_CODE
                    )
                    if response:
                        return response
                time.sleep(0.1)
        
        return None
    
    # ── 工具方法 ──
    
    def get_status(self) -> dict[str, Any]:
        """获取智能体状态报告"""
        return {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "role": self.ROLE,
            "state": self.state.value,
            "capabilities": self.capabilities,
            "triggers": self.TRIGGERS,
            "dna": self.dna,
            "session_id": self.ctx.session_id,
            "error_count": self.ctx.error_count,
            "history_len": len(self.ctx.history),
            "queue_len": len(self.ctx.task_queue),
        }
    
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return self.SYSTEM_PROMPT
    
    def get_capabilities(self) -> List[str]:
        """获取能力列表"""
        return self.capabilities
    
    def reset(self):
        """重置智能体状态"""
        self.ctx = AgentContext(
            persona_code=self.PERSONA_CODE,
            session_id=str(uuid.uuid4())[:8],
        )
        self.state = AgentState.IDLE
        self._log_event("reset", {})
    
    def __repr__(self) -> str:
        return f"<PersonaAgent {self.PERSONA_CODE} {self.PERSONA_NAME} [{self.state.value}]>"


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def agent_dna_hash(persona_code: str, action: str, data: str = "") -> str:
    """生成智能体操作DNA哈希"""
    now = datetime.now()
    raw = f"{persona_code}:{action}:{now.isoformat()}:{data}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now.strftime('%Y%m%d%H%M%S')}-{persona_code}-{action}-{h}"


# ═══════════════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 创建一个测试智能体
    class TestAgent(PersonaAgent):
        PERSONA_CODE = "TEST"
        PERSONA_NAME = "测试智能体"
        PERSONA_NAME_EN = "TestAgent"
        ROLE = "testing"
        MOTTO = "测试一切"
        capabilities = ["test"]
        
        def think(self, observation: dict[str, Any]) -> dict[str, Any]:
            return {"action": "echo", "reasoning": "test think", "confidence": 1.0}
        
        def act(self, decision: dict[str, Any]) -> dict[str, Any]:
            return {"status": "done", "output": "test act", "decision": decision}
    
    agent = TestAgent()
    print(f"✅ PersonaAgent 基类自检通过: {agent}")
    print(f"   状态: {agent.state.value}")
    print(f"   DNA: {agent.dna}")
    
    result = agent.run({"task": "test"})
    print(f"   运行结果: {result['status']}")
    print(f"   事件数: {len(agent.ctx.history)}")
    
    status = agent.get_status()
    print(f"   状态报告: {json.dumps(status, ensure_ascii=False, indent=2)}")
