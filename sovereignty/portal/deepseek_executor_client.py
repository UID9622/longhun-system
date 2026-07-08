# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-03-ENGINE-DEEPSEEK_EXECUTOR_CLIENT-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DeepSeek 执行器客户端

用于外部调用者构造加密请求并解密响应。

用法示例:
    client = DeepSeekExecutorClient(
        executor_url="https://longhun888.com/executor",
        secret=os.getenv("LONGHUN_EXECUTOR_SECRET"),
        token=os.getenv("EXECUTOR_TOKEN"),
    )
    resp = client.execute(route="chat", payload={"messages": [{"role": "user", "content": "你好"}]})
    print(resp)

DNA: #龍芯⚡️20260628-DEEPSEEK-EXECUTOR-CLIENT-v1.0
"""

import os
from typing import Any, Dict, Optional

import requests

from sovereignty.portal.longhun_crypto import (
    LonghunCryptoError,
    decrypt_payload,
    make_envelope,
    open_envelope,
)


class DeepSeekExecutorClient:
    def __init__(
        self,
        executor_url: str,
        secret: str,
        token: str,
        timeout: int = 120,
    ):
        self.executor_url = executor_url.rstrip("/")
        self.secret = secret
        self.token = token
        self.timeout = timeout

    def execute(
        self,
        route: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        envelope = make_envelope({"route": route, "payload": payload}, self.secret)
        resp = requests.post(
            f"{self.executor_url}/execute",
            json=envelope,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                **(headers or {}),
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()
        resp_envelope = resp.json()
        return open_envelope(resp_envelope, self.secret, ttl=300)

    def health(self) -> Dict[str, Any]:
        resp = requests.get(f"{self.executor_url}/health", timeout=10)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:9453"
    secret = os.getenv("LONGHUN_EXECUTOR_SECRET", "")
    token = os.getenv("EXECUTOR_TOKEN", "")
    if not secret or not token:
        print("请先设置 LONGHUN_EXECUTOR_SECRET 和 EXECUTOR_TOKEN")
        raise SystemExit(1)

    client = DeepSeekExecutorClient(url, secret, token)
    print("[health]", client.health())
    print("[execute]", client.execute("echo", {"message": "龍魂 DeepSeek 执行器测试"}))
