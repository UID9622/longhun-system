#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 客户端（龍魂底座专用）
- 直接调用 https://api.deepseek.com/v1/chat/completions
- 不使用 OpenAI 兼容层，Base URL 显式写死
- 支持流式/非流式、对话历史、工具调用占位
- 所有调用带 DNA 追溯

DNA: #龍芯⚡️2026-07-01-DEEPSEEK-CLIENT-v1.0
"""
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import requests

BASE_URL = "https://api.deepseek.com"
CHAT_ENDPOINT = f"{BASE_URL}/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"


@dataclass
class DeepSeekMessage:
    role: str
    content: str


@dataclass
class DeepSeekResponse:
    text: str
    model: str
    usage: dict[str, int]
    finish_reason: str
    raw: dict[str, Any]


class DeepSeekClient:
    """DeepSeek API 龍魂底座客户端。"""

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.chat_endpoint = f"{self.base_url}/v1/chat/completions"
        self.model = model
        if not self.api_key:
            raise RuntimeError("DeepSeek API Key 未提供。请设置 DEEPSEEK_API_KEY 环境变量或直接传入 api_key。")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def generate_dna(tag: str = "DEEPSEEK-CALL") -> str:
        ts = time.strftime("%Y%m%d%H%M%S%f")
        h = hashlib.sha256(f"{tag}:{ts}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-{tag}-{h}"

    def chat(
        self,
        messages: list[dict[str, str] | DeepSeekMessage],
        model: str | None = None,
        temperature: float = 1.0,
        max_tokens: int | None = None,
        stream: bool = False,
        **extra: Any,
    ) -> DeepSeekResponse | Iterator[str]:
        """非流式返回完整响应；流式返回逐字迭代器。"""
        payload_messages = []
        for m in messages:
            if isinstance(m, DeepSeekMessage):
                payload_messages.append({"role": m.role, "content": m.content})
            else:
                payload_messages.append({"role": m["role"], "content": m["content"]})

        payload: dict[str, Any] = {
            "model": model or self.model,
            "messages": payload_messages,
            "temperature": temperature,
            "stream": stream,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload.update(extra)

        resp = requests.post(
            self.chat_endpoint,
            headers=self._headers(),
            json=payload,
            stream=stream,
            timeout=(10, 120),
        )
        resp.raise_for_status()

        if stream:
            return self._stream(resp)

        data = resp.json()
        choice = data["choices"][0]
        return DeepSeekResponse(
            text=choice["message"]["content"],
            model=data.get("model", ""),
            usage=data.get("usage", {}),
            finish_reason=choice.get("finish_reason", ""),
            raw=data,
        )

    def _stream(self, resp: requests.Response) -> Iterator[str]:
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            data_str = line[len("data: "):]
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content
            except Exception:
                continue

    def quick_ask(self, prompt: str, **kwargs: Any) -> DeepSeekResponse:
        """单轮问答快捷入口。"""
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def explain_for_role(
        self,
        content: str,
        role: str = "普通人",
        intent: str = "綜合審核",
        context: dict[str, Any] | None = None,
    ) -> str:
        """调用 DeepSeek 生成指定角色的白话解释。"""
        role_prompts = {
            "普通人": "用生活大白话讲清楚",
            "醫生": "用医疗/专业场景类比",
            "教師": "用教学、备课、家校沟通场景讲",
            "學生": "用学生听得懂的例子",
            "老人": "慢一点、具体一点，像跟长辈聊天",
            "工人/農民": "用干活、种地、做工的经验比喻",
        }
        style = role_prompts.get(role, role_prompts["普通人"])
        ctx = json.dumps(context, ensure_ascii=False, indent=2) if context else "（无额外上下文）"
        prompt = (
            f"你是龍智守的{role}版解释员。{style}。\n"
            f"用户意图：{intent}\n"
            f"原始审核结果：\n{ctx}\n\n"
            f"请用一段 150 字以内的{role}版大白话，给出结论和实用建议。不要套话，像人说话。"
        )
        r = self.quick_ask(prompt, temperature=0.7, max_tokens=400)
        return r.text


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DeepSeek API 龍魂底座客户端")
    parser.add_argument("prompt", nargs="+", help="提问内容")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--stream", action="store_true", help="流式输出")
    parser.add_argument("--system", default=None, help="系统提示词")
    args = parser.parse_args()

    client = DeepSeekClient(model=args.model)
    messages: list[dict[str, str]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": " ".join(args.prompt)})

    dna = client.generate_dna()
    print(f"DNA: {dna}")

    if args.stream:
        for token in client.chat(messages, temperature=args.temperature, max_tokens=args.max_tokens, stream=True):
            print(token, end="", flush=True)
        print()
    else:
        r = client.chat(messages, temperature=args.temperature, max_tokens=args.max_tokens)
        print(f"Model: {r.model}")
        print(f"Usage: {r.usage}")
        print("---")
        print(r.text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
