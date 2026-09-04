#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂·剪贴板本地代理 (Windows) v1.0
=======================================
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷖剥-CLIPBOARD-AGENT-WIN-V1.0-P1

功能:
  - 监听 Windows 剪贴板变化
  - SM4-CBC 加密后通过 WebSocket 上传到龍魂剪贴板容器中心
  - 本地不保留原文；可选「占位替换」模式规避输入法回传
  - 断线自动重连、请求频率限制、DNA 追溯

依赖:
  - websockets, gmssl
  - pyperclip（首选）或 pywin32（备用）

用法:
  set LONGHUN_CLIPBOARD_TOKEN=#龍芯⚡️...
  python3 08_BIN\\lh_clipboard_agent_win.py
"""

import argparse
import asyncio
import hashlib
import json
import os
import ssl
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ganzhi_dna_engine import DNA生成

try:
    from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
    GMSSL_AVAILABLE = True
except Exception:
    GMSSL_AVAILABLE = False

from lh_clipboard_queue import ClipQueue

CST = timezone(timedelta(hours=8))

# Windows 剪贴板后端：优先 pyperclip，其次 win32clipboard
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except Exception:
    PYPERCLIP_AVAILABLE = False

try:
    import win32clipboard
    import win32con
    WIN32_AVAILABLE = True
except Exception:
    WIN32_AVAILABLE = False


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _derive_key(token: str) -> bytes:
    return hashlib.sha256(token.encode("utf-8")).digest()[:16]


def _sm4_encrypt(plaintext: str, token: str) -> str:
    if not GMSSL_AVAILABLE:
        raise RuntimeError("gmssl 未安装，无法加密")
    key = _derive_key(token)
    iv = os.urandom(16)
    crypt = CryptSM4()
    crypt.set_key(key, SM4_ENCRYPT)
    cipher = crypt.crypt_cbc(iv, plaintext.encode("utf-8"))
    return (iv + cipher).hex()


def _get_clipboard() -> str:
    """读取 Windows 剪贴板文本。"""
    if WIN32_AVAILABLE:
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                data = data.decode("mbcs", errors="ignore")
            else:
                data = ""
            win32clipboard.CloseClipboard()
            return data
        except Exception:
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass
    if PYPERCLIP_AVAILABLE:
        try:
            return pyperclip.paste() or ""
        except Exception:
            return ""
    return ""


def _set_clipboard(text: str) -> bool:
    """写入 Windows 剪贴板文本。"""
    if WIN32_AVAILABLE:
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            return True
        except Exception:
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass
    if PYPERCLIP_AVAILABLE:
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    return False


class ClipboardAgentWin:
    def __init__(
        self,
        hub_url: str,
        token: str,
        no_encrypt: bool = False,
        placeholder: bool = False,
        placeholder_text: str = "📦 内容已归档至龍魂系统",
        poll_interval: float = 1.0,
        insecure: bool = False,
    ):
        self.hub_url = hub_url
        self.token = token
        self.no_encrypt = no_encrypt
        self.placeholder = placeholder
        self.placeholder_text = placeholder_text
        self.poll_interval = poll_interval
        self.insecure = insecure

        self.last_content = ""
        self.last_hash = ""
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = True
        self.reconnect_delay = 1.0
        self.queue = ClipQueue()
        self.agent_dna = DNA生成(
            模块="CLIPBOARD",
            动作="AGENT-WIN",
            版本="V1.0",
            级别="P1",
        )

    def _content_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _ssl_context(self) -> Optional[ssl.SSLContext]:
        if not self.hub_url.startswith("wss://"):
            return None
        if self.insecure:
            return ssl._create_unverified_context()
        return ssl.create_default_context()

    async def _connect(self) -> bool:
        try:
            extra = {
                "X-Developer-DNA": self.token,
                "X-Agent-DNA": self.agent_dna,
            }
            self.websocket = await websockets.connect(
                self.hub_url,
                additional_headers=extra,
                ssl=self._ssl_context(),
                ping_interval=30,
                ping_timeout=10,
            )
            await self.websocket.send(
                json.dumps({"action": "ping", "developer_dna": self.token}, ensure_ascii=False)
            )
            resp = json.loads(await asyncio.wait_for(self.websocket.recv(), timeout=5))
            if resp.get("status") == "pong":
                print(f"[{_now()}] ✅ 已连接容器中心: {self.hub_url}")
                print(f"[{_now()}]    HUB DNA: {resp.get('dna', 'unknown')}")
                self.reconnect_delay = 1.0
                return True
        except Exception as e:
            print(f"[{_now()}] ❌ 连接失败: {e}")
        return False

    async def _ensure_connection(self) -> bool:
        if self.websocket is not None:
            try:
                pong = await self.websocket.ping()
                await asyncio.wait_for(pong, timeout=3)
                return True
            except Exception:
                self.websocket = None

        if self.websocket is None:
            connected = await self._connect()
            if not connected:
                await asyncio.sleep(min(self.reconnect_delay, 60))
                self.reconnect_delay *= 1.5
                return False
        return True

    def _build_payload(self, content: str) -> dict:
        payload = {
            "action": "save",
            "developer_dna": self.token,
            "source": "windows_clipboard",
            "timestamp": _now(),
        }
        if self.no_encrypt:
            payload["content"] = content
        else:
            payload["content_encrypted"] = _sm4_encrypt(content, self.token)
        return payload

    async def _send_payload(self, payload: dict) -> dict:
        await self.websocket.send(json.dumps(payload, ensure_ascii=False))
        resp = await asyncio.wait_for(self.websocket.recv(), timeout=10)
        return json.loads(resp)

    async def _startup_drain(self) -> None:
        try:
            await self._drain_queue()
        except Exception as e:
            print(f"[{_now()}] ⚠️ 启动时队列补发异常: {e}")

    async def _drain_queue(self) -> None:
        if self.queue.size() == 0:
            return
        connected = await self._ensure_connection()
        if not connected:
            return
        items = self.queue.dequeue(batch_size=20)
        if not items:
            return
        success_ids = []
        fail_ids = []
        for item in items:
            try:
                result = await self._send_payload(item["payload"])
                if result.get("status") == "success":
                    success_ids.append(item["id"])
                else:
                    fail_ids.append(item["id"])
            except Exception:
                fail_ids.append(item["id"])
        if success_ids:
            self.queue.ack(success_ids)
        if fail_ids:
            self.queue.nack(fail_ids)
        if success_ids:
            print(f"[{_now()}] 📤 离线队列补发成功 {len(success_ids)} 条，失败 {len(fail_ids)} 条")

    async def _handle_new_content(self, content: str) -> None:
        current_hash = self._content_hash(content)
        if current_hash == self.last_hash:
            return

        original = content
        if self.placeholder:
            _set_clipboard(self.placeholder_text)
            print(f"[{_now()}] 🛡️ 占位替换已触发，原文已发往容器")

        payload = self._build_payload(original)
        connected = await self._ensure_connection()
        if not connected:
            self.queue.enqueue(payload, source="windows_clipboard")
            pending = self.queue.size()
            print(f"[{_now()}] ⚠️ 容器离线，已加密缓存到本地队列（{len(original)} 字符，队列 {pending} 条）")
            if self.placeholder:
                _set_clipboard(original)
            return

        await self._drain_queue()

        try:
            result = await self._send_payload(payload)
            if result.get("status") == "success":
                action = result.get("action", "saved")
                dna = result.get("dna", "")
                count = result.get("copy_count", 1)
                print(f"[{_now()}] ✅ 已归档 ({action}) | 复制{count}次 | {dna[:50]}...")
            elif result.get("status") == "rate_limited":
                print(f"[{_now()}] ⚠️ 上传频率受限，已跳过")
            else:
                print(f"[{_now()}] ⚠️ 归档失败: {result.get('message')}")
        except Exception as e:
            print(f"[{_now()}] ❌ 发送异常: {e}")
            self.websocket = None
            self.queue.enqueue(payload, source="windows_clipboard")
            if self.placeholder:
                _set_clipboard(original)
            return

        if self.placeholder:
            self.last_content = self.placeholder_text
            self.last_hash = self._content_hash(self.placeholder_text)
        else:
            self.last_content = original
            self.last_hash = current_hash

    async def run(self):
        if not self.token:
            print(f"[{_now()}] ❌ 请设置 LONGHUN_CLIPBOARD_TOKEN 或通过 --token 传入")
            sys.exit(1)

        if not self.no_encrypt and not GMSSL_AVAILABLE:
            print(f"[{_now()}] ❌ gmssl 未安装，无法启用 SM4 加密。请 pip install gmssl 或加 --no-encrypt 调试")
            sys.exit(1)

        if not WIN32_AVAILABLE and not PYPERCLIP_AVAILABLE:
            print(f"[{_now()}] ❌ 未找到剪贴板后端，请安装 pyperclip: pip install pyperclip")
            sys.exit(1)

        print("🐉 龍魂·剪贴板本地代理 (Windows)")
        print(f"   AGENT DNA: {self.agent_dna}")
        print(f"   容器中心: {self.hub_url}")
        print(f"   剪贴板后端: {'win32clipboard' if WIN32_AVAILABLE else 'pyperclip'}")
        print(f"   加密模式: {'明文调试' if self.no_encrypt else 'SM4-CBC'}")
        print(f"   占位替换: {'开启' if self.placeholder else '关闭'}")
        print(f"   离线缓存: {self.queue.size()} 条待补发")
        print(f"   当前时间: {_now()}")
        print("   🟢 监听中... (Ctrl+C 退出)\n")

        self.last_content = _get_clipboard()
        self.last_hash = self._content_hash(self.last_content)

        asyncio.create_task(self._startup_drain())

        loop_count = 0
        while self.running:
            try:
                current = _get_clipboard()
                if current and current != self.last_content:
                    await self._handle_new_content(current)

                loop_count += 1
                if loop_count % max(1, int(30 / self.poll_interval)) == 0:
                    await self._drain_queue()

                await asyncio.sleep(self.poll_interval)
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                print(f"[{_now()}] ⚠️ 主循环异常: {e}")
                await asyncio.sleep(5)

        if self.queue.size() > 0:
            print(f"[{_now()}] 📤 退出前补发离线队列 {self.queue.size()} 条...")
            await self._drain_queue()

        if self.websocket:
            await self.websocket.close()
        print(f"\n[{_now()}] 👋 代理已退出")


def main():
    parser = argparse.ArgumentParser(description="龍魂·剪贴板本地代理 (Windows)")
    parser.add_argument(
        "--hub",
        default=os.environ.get("LONGHUN_CLIPBOARD_HUB", "ws://127.0.0.1:8765"),
        help="容器中心 WebSocket 地址",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("LONGHUN_CLIPBOARD_TOKEN", ""),
        help="开发者 DNA / token",
    )
    parser.add_argument("--no-encrypt", action="store_true", help="明文调试模式")
    parser.add_argument("--placeholder", action="store_true", help="占位替换模式")
    parser.add_argument("--placeholder-text", default="📦 内容已归档至龍魂系统")
    parser.add_argument("--interval", type=float, default=1.0, help="轮询间隔（秒）")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="连接 wss:// 时跳过证书校验（仅用于自签名证书测试）",
    )
    args = parser.parse_args()

    agent = ClipboardAgentWin(
        hub_url=args.hub,
        token=args.token,
        no_encrypt=args.no_encrypt,
        placeholder=args.placeholder,
        placeholder_text=args.placeholder_text,
        poll_interval=args.interval,
        insecure=args.insecure,
    )
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
