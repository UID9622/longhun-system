#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
🐉 龍魂统一消息格式 · 引擎内核
===============================
所有通道（飞书/微信/Web/Telegram）的消息统一为此格式。
引擎内核只认 Message → Response，不关心来源通道。

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-MSG-FORMAT-v1.0
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, Literal
from enum import Enum
import uuid


CST = timezone(timedelta(hours=8))


class Channel(Enum):
    """通道类型"""
    FEISHU = "feishu"
    WECHAT_OA = "wechat_oa"       # 微信公众号
    WECHAT_MP = "wechat_mp"        # 微信小程序
    WEB = "web"                     # 官网/Web Widget
    TELEGRAM = "telegram"
    CLI = "cli"                     # 命令行
    API = "api"                     # 直接API调用
    UNKNOWN = "unknown"


class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VOICE = "voice"
    CARD_ACTION = "card_action"    # 卡片按钮点击
    EVENT = "event"                 # 系统事件（关注/进入等）


class AuditLevel(Enum):
    """三色审计"""
    GREEN = "green"     # 通过
    YELLOW = "yellow"   # 待审
    RED = "red"         # 熔断


@dataclass
class Message:
    """统一入站消息
    
    无论从飞书、微信还是Web来，都转成这个格式。
    """
    # ── 必填 ──
    channel: Channel
    content: str                          # 文本内容
    msg_type: MessageType = MessageType.TEXT
    
    # ── 用户标识 ──
    user_id: str = ""                     # 通道内用户ID
    user_name: str = ""                   # 用户显示名
    session_id: str = ""                  # 会话ID（群聊/单聊）
    
    # ── 通道元数据 ──
    channel_meta: Dict[str, Any] = field(default_factory=dict)
    # 飞书: open_id, tenant_key, msg_id
    # 微信: openid, appid
    # Web: ip, user_agent
    
    # ── 引擎元数据 ──
    msg_id: str = ""                      # 引擎内唯一ID
    timestamp: datetime = field(default_factory=lambda: datetime.now(CST))
    raw_payload: Any = None               # 原始通道消息（调试用）
    
    # ── 审计状态 ──
    audit_level: AuditLevel = AuditLevel.GREEN
    audit_reason: str = ""
    
    def __post_init__(self):
        if not self.msg_id:
            self.msg_id = f"MSG-{uuid.uuid4().hex[:12]}"
        if not self.session_id:
            self.session_id = self.user_id


@dataclass
class Response:
    """统一出站响应
    
    引擎内核处理后返回这个，各通道适配器转换为自己的格式。
    """
    # ── 必填 ──
    msg_id: str                           # 关联的入站 msg_id
    content: str = ""                     # 文本回复
    success: bool = True
    
    # ── 可选增强 ──
    title: str = ""                       # 卡片标题
    card_data: Optional[Dict[str, Any]] = None  # 结构化卡片（飞书/微信）
    quick_replies: list[str] = field(default_factory=list)  # 快捷回复选项
    attachments: list[Dict[str, Any]] = field(default_factory=list)
    
    # ── 审计追溯 ──
    dna_trace: str = ""                   # 本次响应的DNA追溯码
    persona_used: str = ""                # 使用的人格
    capability_used: str = ""             # 使用的能力
    audit_level: AuditLevel = AuditLevel.GREEN
    audit_note: str = ""
    
    # ── 元数据 ──
    timestamp: datetime = field(default_factory=lambda: datetime.now(CST))
    meta: Dict[str, Any] = field(default_factory=dict)
    
    def to_text(self) -> str:
        """转为纯文本"""
        lines = []
        if self.title:
            lines.append(f"【{self.title}】")
        if self.content:
            lines.append(self.content)
        if self.dna_trace:
            lines.append(f"\n🧬 {self.dna_trace}")
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """转为通用字典"""
        return {
            "msg_id": self.msg_id,
            "content": self.content,
            "title": self.title,
            "success": self.success,
            "card_data": self.card_data,
            "quick_replies": self.quick_replies,
            "dna_trace": self.dna_trace,
            "persona_used": self.persona_used,
            "capability_used": self.capability_used,
            "audit_level": self.audit_level.value,
            "timestamp": self.timestamp.isoformat(),
        }
