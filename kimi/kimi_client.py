#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

"""
🐉 龍魂 × Kimi API 客户端封装

功能：
  • HTTP API 调用封装
  • 错误处理和重试机制
  • 多模态请求支持（文本、图像、文件）
  • 故障转移和断路器

DNA:#龍芯⚡️2026-06-08-KIMI-CLIENT-v1.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

理论指导：曾仕强老师（永恒显示）
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# 引入龍魂模型路由，禁止直连 Moonshot
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sovereignty.portal import model_router


class KimiClient:
    """Kimi API 客户端"""

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        # 龍魂系统不再使用 KIMI_API_KEY；保留参数仅兼容旧接口
        self.api_key = api_key or os.getenv("KIMI_API_KEY") or "longhun-local"
        self.timeout = timeout
        self.max_retries = 3
        self.retry_delay = 1.0

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """已迁移：统一调用龍魂模型路由（DeepSeek / 本地 Ollama）。"""
        if method != "POST" or endpoint != "/chat/completions":
            raise ValueError(f"当前仅支持本地 /chat/completions 代理: {method} {endpoint}")

        messages = (data or {}).get("messages", [])
        temperature = (data or {}).get("temperature", 0.7)
        max_tokens = (data or {}).get("max_tokens", 4096)
        model = (data or {}).get("model")

        for attempt in range(self.max_retries):
            try:
                req = model_router.ChatRequest(
                    messages=messages,
                    provider="auto",
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                result = model_router.chat(req)
                # 包装成 OpenAI 兼容格式
                return {
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": result.get("reply", ""),
                            },
                            "finish_reason": "stop",
                            "index": 0,
                        }
                    ],
                    "model": result.get("model", "deepseek-chat"),
                    "provider": result.get("provider", "deepseek"),
                    "dna": result.get("dna"),
                }
            except Exception:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "moonshot-v1-8k",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """调用聊天完成 API"""

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if metadata:
            payload["metadata"] = metadata

        return self._make_request("POST", "/chat/completions", payload)

    def process_multimodal(
        self,
        text: str,
        images: Optional[List[str]] = None,
        files: Optional[List[str]] = None,
        model: str = "moonshot-v1-8k"
    ) -> Dict[str, Any]:
        """处理多模态请求（文本 + 图像 + 文件）"""

        messages = []
        content = [{"type": "text", "text": text}]

        # 添加图像
        if images:
            for img_url in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img_url}
                })

        # 添加文件参考
        if files:
            for file_path in files:
                content.append({
                    "type": "file",
                    "file_name": os.path.basename(file_path),
                    "file_path": file_path
                })

        messages.append({"role": "user", "content": content})

        return self.chat_completion(messages, model=model)

    def get_models(self) -> Dict[str, Any]:
        """获取可用模型列表（本地路由）"""
        return model_router.list_models()

    def health_check(self) -> bool:
        """检查本地模型路由状态"""
        try:
            status = model_router.models_status()
            return any(p["status"] == "online" for p in status.get("providers", []))
        except Exception as e:
            print(f"❌ 本地模型路由连接失败: {e}")
            return False

    def extract_response_text(self, response: Dict[str, Any]) -> str:
        """从响应中提取文本内容"""
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return ""

    def __repr__(self) -> str:
        return f"<KimiClient api_key=***...{self.api_key[-4:]} timeout={self.timeout}>"


if __name__ == "__main__":
    # 测试用例
    client = KimiClient()

    # 健康检查
    print("🔍 健康检查...")
    is_healthy = client.health_check()
    print(f"✅ Kimi API 连接正常" if is_healthy else "❌ Kimi API 连接失败")

    # 简单聊天
    print("\n💬 测试聊天...")
    response = client.chat_completion([
        {"role": "user", "content": "你好，你是谁？"}
    ])
    print(f"Kimi: {client.extract_response_text(response)}")
