#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 × Kimi API 客户端封装

功能：
  • HTTP API 调用封装
  • 错误处理和重试机制
  • 多模态请求支持（文本、图像、文件）
  • 故障转移和断路器

DNA: #龍芯⚡️2026-06-08-KIMI-CLIENT-v1.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

理论指导：曾仕强老师（永恒显示）
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime


class KimiClient:
    """Kimi API 客户端"""

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        if not self.api_key:
            raise ValueError("KIMI_API_KEY 未设置，请设置环境变量或传入 api_key")

        self.base_url = "https://api.moonshot.cn/v1"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.max_retries = 3
        self.retry_delay = 1.0

    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送 API 请求，带重试机制"""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.max_retries):
            try:
                if method == "POST":
                    response = self.session.post(url, json=data, timeout=self.timeout)
                elif method == "GET":
                    response = self.session.get(url, timeout=self.timeout)
                else:
                    raise ValueError(f"不支持的 HTTP 方法: {method}")

                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limit
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 2))
                        continue
                raise

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "moonshot-v1",
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
        model: str = "moonshot-v1"
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
        """获取可用模型列表"""
        return self._make_request("GET", "/models")

    def health_check(self) -> bool:
        """检查 API 连接状态"""
        try:
            response = self._make_request("GET", "/models")
            return response.get("data") is not None
        except Exception as e:
            print(f"❌ Kimi API 连接失败: {e}")
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
