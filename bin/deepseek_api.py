#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek-V3 API 调用封装（龙魂适配版）
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-DeepSeek适配-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import json
import requests
from typing import List, Dict, Optional, Generator


class DeepSeekClient:
    """DeepSeek-V3 客户端（支持本地vLLM和官方API）"""

    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        model: str = "deepseek-ai/DeepSeek-V3",
        timeout: int = 120
    ):
        # 优先使用环境变量
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "http://localhost:8000/v1")
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.model = model
        self.timeout = timeout

        # 判断是本地还是云端
        self.is_local = "localhost" in self.base_url or "127.0.0.1" in self.base_url

    def _headers(self) -> Dict:
        headers = {"Content-Type": "application/json"}
        if not self.is_local and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """同步对话"""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs
        }

        response = requests.post(
            url,
            headers=self._headers(),
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> Generator[str, None, None]:
        """流式对话（逐字输出）"""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs
        }

        response = requests.post(
            url,
            headers=self._headers(),
            json=payload,
            stream=True,
            timeout=self.timeout
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get('choices', [{}])[0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue

    def count_tokens(self, text: str) -> int:
        """估算Token数量（中文约1字=1token，英文约0.75词=1token）"""
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_words = len(text.split()) - chinese_chars
        return chinese_chars + int(english_words * 1.33) + 5


# ---------- 使用示例 ----------
if __name__ == "__main__":
    # 初始化客户端
    client = DeepSeekClient()

    # 1. 同步对话
    messages = [
        {"role": "system", "content": "你是龙魂系统的AI助手，回答要直接、真实、不虚伪。"},
        {"role": "user", "content": "介绍一下DeepSeek-V3的特点"}
    ]
    response = client.chat(messages)
    print(response['choices'][0]['message']['content'])

    # 2. 流式对话
    print("\n--- 流式输出 ---")
    for chunk in client.chat_stream(messages):
        print(chunk, end="", flush=True)
    print()
