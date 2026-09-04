#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂引擎 · 通道基类
=======================
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
所有通道适配器的基类。实现接收→转换→调用引擎→转换→发送。

DNA: #龍芯⚡️丙午·乙未·甲子·申时·䷄需-CHANNEL-BASE-v1.0
"""

from __future__ import annotations
import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

# 确保引擎包可导入
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from 引擎.message import Message, Response, Channel


class ChannelAdapter(ABC):
    """通道适配器基类

    每个通道只需要实现:
    1. to_message()  — 把通道消息转成统一 Message
    2. send()        — 把统一 Response 发回通道
    3. run()         — 启动服务（HTTP/WebSocket/轮询等）
    """

    channel_type: Channel

    def __init__(self, engine=None):
        from 引擎.engine_core import LonghunEngine
        self.engine = engine or LonghunEngine()

    @abstractmethod
    def to_message(self, raw: Any) -> Message:
        """将通道原始消息转为统一 Message"""
        ...

    @abstractmethod
    def send(self, response: Response, target: Any = None):
        """将统一 Response 发回通道"""
        ...

    def handle(self, raw: Any) -> Optional[Response]:
        """标准处理流程: 转换 → 引擎处理 → 发送 → 返回响应"""
        msg = self.to_message(raw)
        response = self.engine.process(msg)
        self.send(response, raw)
        return response

    @abstractmethod
    def run(self, **kwargs):
        """启动通道服务"""
        ...

    def health(self) -> Dict[str, Any]:
        return {
            "channel": self.channel_type.value,
            "engine": self.engine.get_health(),
        }


class SimpleChannelAdapter(ChannelAdapter):
    """极简单通道：只需实现 to_message 和 send"""

    channel_type: Channel = Channel.UNKNOWN

    def to_message(self, raw: str) -> Message:
        return Message(
            channel=self.channel_type,
            content=raw,
        )

    def send(self, response: Response, target: Any = None):
        print(response.to_text())

    def run(self, **kwargs):
        print(f"🐉 通道 {self.channel_type.value} 启动 · 交互模式")
        print("输入消息，回车发送。输入 q 退出。\n")
        while True:
            try:
                text = input("> ").strip()
                if text.lower() in ("q", "quit", "exit"):
                    break
                if text:
                    response = self.handle(text)
            except (KeyboardInterrupt, EOFError):
                break
        print("\n👋 通道已关闭")
