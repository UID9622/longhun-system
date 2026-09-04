#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LH-ASCEND-INFER · 昇腾 AI 推理入口 + 三层算力调度
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙申·癸丑·酉时·䷜坎-ASCEND-INFER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 依赖: 复用 08_BIN/cnsh_ai_providers.py 的 BaseAIProvider 抽象类（同签名 chat）
# 用途: 昇腾 NPU 推理 · 与现有模型调用同签名 · 上层无感切换 · 昇腾不可达自动降级鲲鹏 CPU
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cnsh_ai_providers import (
    AIProviderConfig,
    BaseAIProvider,
    ChatMessage,
    OllamaProvider,
    OpenAICompatibleProvider,
    build_provider,
    get_router,
)

# ───────────────────────── 三层算力调度 ─────────────────────────

TIER_EDGE = "edge"       # 终端: 麒麟/Apple NPU · 轻量推理/端侧加密
TIER_KUNPENG = "kunpeng" # 鲲鹏: CPU 标准推理/通心译
TIER_ASCEND = "ascend"   # 昇腾: NPU 重推理/大模型/批量转译


class AscendProvider(BaseAIProvider):
    """昇腾 NPU 推理 Provider（华为云 ModelArts 推理端点 / AscendCL 本地）。

    - 与 BaseAIProvider.chat 同签名，注册进 build_provider 后上层无感切换。
    - 端点配置优先级: 环境变量 > 显式传入。密钥一律走 lh_vault，禁止明文写死。
    """

    def __init__(self, config: AIProviderConfig, endpoint: Optional[str] = None,
                 api_key: Optional[str] = None, timeout: float = 60.0):
        super().__init__(config)
        # endpoint: https://<modelarts-endpoint>/v1/infers/<id>
        self.endpoint = endpoint or os.getenv("ASCEND_INFER_ENDPOINT", "")
        self.api_key = api_key or os.getenv("ASCEND_INFER_API_KEY", "")
        self.timeout = timeout

    def chat(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        if not self.endpoint or not self.api_key:
            raise RuntimeError(
                "昇腾未配置: 请先 lh_vault put ASCEND_INFER_ENDPOINT / ASCEND_INFER_API_KEY"
            )
        return self._infer(messages, temperature)

    def _infer(self, messages: List[ChatMessage], temperature: float) -> str:
        import urllib.request

        payload = {
            "messages": [m.dict() if hasattr(m, "dict") else {"role": m.role, "content": m.content}
                         for m in messages],
            "temperature": temperature,
            "max_tokens": 2048,
        }
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        # 兼容常见返回形态
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        if "output" in data and "text" in data["output"]:
            return data["output"]["text"]
        return str(data)


# ───────────────────────── 三层调度路由器 ─────────────────────────

def tier_router(messages: List[ChatMessage], temperature: float = 0.7,
                task_weight: float = 1.0) -> str:
    """按任务权重自动分派算力层。

    - 昇腾(NPU): task_weight >= 0.7 或大模型/批量转译 → 昇腾
    - 鲲鹏(CPU): 标准推理 → 鲲鹏
    - 终端: 由端侧 App 自行决策（此函数不触达）
    降级链: 昇腾不可达 → 鲲鹏 → 报错（节能协议: 首次失败禁自动重试）
    """
    router = get_router()
    prompt = messages[-1].content if messages else ""
    # 1) 重任务优先昇腾
    if task_weight >= 0.7:
        try:
            return AscendProvider(
                AIProviderConfig(name="昇腾NPU", model="ascend-llm")
            ).chat(messages, temperature)
        except Exception as e:
            print(f"🟡 昇腾不可达({type(e).__name__}) → 降级鲲鹏 CPU", file=sys.stderr)
    # 2) 默认鲲鹏 CPU（AIRouter.ask 为对外统一入口）
    try:
        return router.ask(prompt, system="龍魂·昇腾调度器")
    except Exception as e:
        raise RuntimeError(f"🟡 鲲鹏推理失败: {type(e).__name__}: {e}") from e


def _build_cli_parser():
    import argparse

    p = argparse.ArgumentParser(description="龍魂昇腾推理入口 · 三层算力调度")
    p.add_argument("prompt", nargs="?", help="提示词（不带则进入自测模式）")
    p.add_argument("--weight", type=float, default=0.5, help="任务权重 0-1（≥0.7 走昇腾）")
    p.add_argument("--self-test", action="store_true", help="自测: mock 昇腾 + 降级链")
    return p


def _self_test():
    """自测: 昇腾未配置时走 mock → 验证降级链不崩。"""
    print("🧪 昇腾推理自测开始...")
    msgs = [ChatMessage(role="user", content="自测: 返回OK")]
    # mock 昇腾（故意不给 endpoint → 触发降级）
    try:
        out = tier_router(msgs, task_weight=0.9)
        print(f"✅ 降级链通过 → 输出: {out[:50]}")
    except Exception as e:
        print(f"❌ 降级链异常: {e}")
        return 1
    print("🧪 自测完成: 昇腾未配置时自动降级鲲鹏，链路不崩 ✅")
    return 0


def main() -> int:
    args = _build_cli_parser().parse_args()
    if args.self_test or not args.prompt:
        return _self_test()
    msgs = [ChatMessage(role="user", content=args.prompt)]
    t0 = time.time()
    out = tier_router(msgs, task_weight=args.weight)
    print(out)
    print(f"⏱ {time.time() - t0:.2f}s · 权重 {args.weight}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
