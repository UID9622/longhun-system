#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
DeepSeek-V3 API 调用封装（龍魂适配版）
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-DeepSeek适配-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
精修(2026-09-03·深度学习代码精修): 本文件降级为 lh_model.generate 的底层委派库
  · 调用入口唯一化: lh model run / lh model api（lh.py SUB_DISPATCH 'model'）
  · 禁止直接 python3 deepseek_api.py 裸调（__main__ 示例已归一移除）· 逻辑不变·向后兼容
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


# ---------- 统一入口指引（2026-09-03·深度学习代码精修） ----------
# 本文件为底层委派库，不再提供独立 CLI 示例。调用统一走:
#   lh model run "<prompt>" --engine deepseek      # DeepSeek 单轮推理
#   lh model api                                  # 双端状态（deepseek/ollama）
#   from lh_model import generate                 # Python 层统一推理入口(auto 降级链)
if __name__ == "__main__":
    import sys
    print("  ⚠️ deepseek_api.py 已归一为 lh_model 底层库（深度学习代码精修 v1.0）")
    print("     请使用统一入口: lh model run '<prompt>' --engine deepseek  |  lh model api")
    sys.exit(2)
