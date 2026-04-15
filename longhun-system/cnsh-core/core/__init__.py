"""
CNSH-64 · Cultural-Normative Symbolic Hierarchy
Author: 诸葛鑫 (UID9622) · 龍魂系统
DNA: #ZHUGEXIN⚡️2026-03-23-CNSH-CORE-INIT

核心类型定义与枚举。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class State(Enum):
    """8 基础状态 · 对应先天八卦"""
    INITIATION  = ("s1", "☰ 乾", "Origin/Launch")
    FOUNDATION  = ("s2", "☷ 坤", "Stability/Base")
    TRIGGER     = ("s3", "☳ 震", "Activation")
    PROPAGATION = ("s4", "☴ 巽", "Diffusion")
    RISK        = ("s5", "☵ 坎", "Danger/Crisis")
    AWARENESS   = ("s6", "☲ 離", "Perception")
    BOUNDARY    = ("s7", "☶ 艮", "Constraint/Limit")
    COOPERATION = ("s8", "☱ 兌", "Collaboration")

    def __init__(self, sid: str, iching: str, semantic: str):
        self.sid      = sid
        self.iching   = iching
        self.semantic = semantic


class Action(Enum):
    EXECUTE     = "execute"
    CONDITIONAL = "conditional"
    BLOCK       = "block"


class AuditColor(Enum):
    GREEN  = "🟢"
    YELLOW = "🟡"
    RED    = "🔴"


@dataclass
class CompositeState:
    """64态复合状态 = State × State"""
    primary:   State
    secondary: State

    @property
    def index(self) -> int:
        states = list(State)
        return states.index(self.primary) * 8 + states.index(self.secondary)

    def __str__(self) -> str:
        return f"({self.primary.name}, {self.secondary.name})"


@dataclass
class Event:
    content:   str
    user_id:   str
    timestamp: str
    metadata:  dict = field(default_factory=dict)


@dataclass
class Decision:
    composite_state: CompositeState
    risk_score:      float
    action:          Action
    audit_color:     AuditColor
    dna_trace:       str
    explanation:     str
    ethical_pass:    bool
    blocked_rules:   list = field(default_factory=list)
