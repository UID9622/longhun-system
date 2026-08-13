#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2
"""
🐲 龍魂·增强Agent基类 v2.0
DNA: #龍芯⚡️2026-08-04-BASE-AGENT-UID9622

融合现有 PersonaAgent + 多智能体协作语义。
每个Agent = 人格标签 + 专业职能 + 黑板读写 + 总线通信。
"""

import sys
import threading
import uuid
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable

SYSTEM_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_persona_agent import PersonaAgent, AgentState, agent_dna_hash


class LonghunAgent(ABC):
    """
    龍魂智能体基类 — 继承 PersonaAgent 语义，增加黑板+总线接口。

    子类只需实现:
      - define_system_prompt() → str
      - think(question: str, context: dict) → dict
      - act(task: str, **kwargs) → dict

    基类自动处理:
      - 黑板读写
      - 总线通信
      - 状态管理
      - DNA追溯
      - 审计日志
    """

    # 子类必须定义
    PERSONA_ID: str = ""          # 如 "P05"
    PERSONA_NAME: str = ""        # 如 "上帝之眼"
    ROLE: str = ""                # 如 "auditor"
    LAYER: str = ""               # strategic/executive/cultural/guardian/special/subsystem
    MOTTO: str = ""               # 座右铭
    EXPERTISE: str = ""           # 专长领域（一句话）

    def __init__(self, llm_client=None, blackboard=None, bus=None):
        self.llm = llm_client
        self.blackboard = blackboard
        self.bus = bus
        self._state = AgentState.IDLE
        self._lock = threading.RLock()
        self._stats = {"tasks": 0, "msgs_sent": 0, "errors": 0, "last_active": None}
        self._task_history: List[Dict] = []
        self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{self.PERSONA_ID}-{self.PERSONA_NAME}-UID9622"

    # ── 抽象方法（子类实现） ──

    @abstractmethod
    def define_system_prompt(self) -> str:
        """返回系统提示词"""
        ...

    @abstractmethod
    def think(self, question: str, context: dict = None) -> dict:
        """推理分析，返回结构化思考结果"""
        ...

    @abstractmethod
    def act(self, task: str, **kwargs) -> dict:
        """执行任务，返回执行结果"""
        ...

    # ── 统一入口 ──

    def process(self, task: str, **kwargs) -> Dict[str, Any]:
        """标准处理流程: think → act → audit"""
        with self._lock:
            self._state = AgentState.THINKING
            self._stats["last_active"] = datetime.now().isoformat()

        try:
            # 1. 读取上下文
            context = self._gather_context()
            context.update(kwargs)

            # 2. 思考
            thought = self.think(task, context)

            # 3. 执行
            result = self.act(task, thought=thought, **context)

            # 4. 汇总
            self._stats["tasks"] += 1
            self._task_history.append({
                "task": task[:200], "thought_summary": str(thought)[:200],
                "ts": datetime.now().isoformat()
            })

            return {
                "persona": self.PERSONA_ID,
                "name": self.PERSONA_NAME,
                "layer": self.LAYER,
                "status": "ok",
                "thought": thought,
                "result": result,
                "dna": self.dna,
            }
        except Exception as e:
            self._stats["errors"] += 1
            return {"persona": self.PERSONA_ID, "status": "error", "error": str(e)}
        finally:
            with self._lock:
                self._state = AgentState.IDLE

    def _gather_context(self) -> dict:
        ctx = {}
        if self.blackboard:
            try:
                ctx["blackboard_context"] = self.blackboard.get_context()
            except Exception:
                pass
        return ctx

    # ── 黑板快捷操作 ──

    def write_bb(self, key: str, data: Any) -> bool:
        if self.blackboard:
            return self.blackboard.write(key, data, agent=self.PERSONA_ID)
        return False

    def read_bb(self, key: str) -> Optional[Dict]:
        if self.blackboard:
            return self.blackboard.read(key)
        return None

    # ── 总线快捷操作 ──

    def send_to(self, target_id: str, content: Any, msg_type: str = "task") -> str:
        if self.bus:
            self._stats["msgs_sent"] += 1
            return self.bus.send(self.PERSONA_ID, target_id, content, msg_type)
        return "bus:unavailable"

    def broadcast(self, content: Any, msg_type: str = "broadcast", exclude: List[str] = None) -> List[str]:
        if self.bus:
            self._stats["msgs_sent"] += 1
            return self.bus.broadcast(self.PERSONA_ID, content, msg_type, exclude=exclude)
        return []

    # ── LLM调用 ──

    def call_llm(self, prompt: str, system: str = None) -> str:
        if self.llm is None:
            return f"[{self.PERSONA_NAME}] ⚠️ LLM未配置"
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = self.llm.chat.completions.create(
                model=getattr(self.llm, 'model', 'default'),
                messages=messages, temperature=0.3, max_tokens=4000
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[{self.PERSONA_NAME}] LLM调用失败: {e}"

    # ── 属性 ──

    @property
    def state(self) -> AgentState:
        return self._state

    @property
    def stats(self) -> Dict[str, Any]:
        return dict(self._stats)

    @property
    def task_count(self) -> int:
        return self._stats["tasks"]

    def shutdown(self):
        if self.bus:
            self.bus.unregister(self.PERSONA_ID)
        with self._lock:
            self._state = AgentState.DONE
