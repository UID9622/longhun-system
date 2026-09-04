#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷏豫-AI-ADAPTERS-v1.0-7d3f1a2b
# 创建者: 诸葛鑫（UID9622）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 adapter 契约落地 🟡 ollama 实测待跑 🔴 无
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · AI 模型适配器 v1.0（Harness 哲学落地：一切模型皆插件）

对齐 DeepSeek Harness「Model + Harness = Agent」，把模型调用抽成统一 adapter 契约：
每个模型 = 一个插件（id/check/chat/chat_stream），可热插拔、可注册进 PluginKit。

落地适配器:
  - ollama  —— 本地模型（零密钥·免费·龍魂主力 longhun-v4.0）
  - deepseek—— OpenAI 兼容（复用 lh_ai_gateway 配置）
  - kimi    —— OpenAI 兼容（复用网关）
  - openai  —— OpenAI 兼容（复用网关）
  - claude  —— Anthropic 格式（复用网关）
  - hunyuan —— 腾讯混元（复用网关）

统一调用: call_any(adapter_id, prompt, ...) / call_any_stream(...)
插件化:   as_plugins() → PluginKit 可直接装载的插件列表

用法:
  python3 bin/lh_ai_adapters.py --list
  python3 bin/lh_ai_adapters.py --call ollama --prompt "你好" --model longhun-v4.0
  python3 bin/lh_ai_adapters.py --call deepseek --prompt "翻译成中文"
  python3 bin/lh_ai_adapters.py --stream ollama --prompt "流式测试"
  python3 bin/lh_ai_adapters.py --plugin-demo     # PluginKit 装载 ollama 插件并调用
"""
import argparse
import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ============================================================
# 统一 adapter 契约（对齐 Harness 插件契约）
# ============================================================
class ModelAdapter(ABC):
    """统一模型适配器协议：id/name/version + check/chat/chat_stream。"""

    id: str = ""
    name: str = ""
    version: str = "1.0.0"
    default_model: str = ""

    @abstractmethod
    def check(self) -> bool:
        """模型是否可用（密钥/本地服务是否就绪）。"""

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], system: str = "",
             temperature: float = 0.7, model: str = "") -> Dict[str, Any]:
        """同步对话 → {"content": ..., "model": ..., "provider": ...}"""

    def chat_stream(self, messages: List[Dict[str, Any]], system: str = "",
                    temperature: float = 0.7, model: str = ""):
        """流式对话 → yield 文本块（默认退化为同步）。"""
        r = self.chat(messages, system=system, temperature=temperature, model=model)
        yield r.get("content", "")


# ============================================================
# 1. Ollama 本地适配器（零密钥 · 免费 · 龍魂主力）
# ============================================================
class OllamaAdapter(ModelAdapter):
    id = "ollama"
    name = "Ollama本地模型"
    version = "1.0.0"
    default_model = "longhun-v4.0"  # 龍魂主力底座

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def check(self) -> bool:
        try:
            import httpx
            r = httpx.get(f"{self.base_url}/api/tags", timeout=2.0)
            return r.status_code == 200
        except Exception:
            return False

    def chat(self, messages, system="", temperature=0.7, model=""):
        import httpx
        model = model or self.default_model
        msgs = ([{"role": "system", "content": system}] if system else []) + list(messages)
        payload = {"model": model, "messages": msgs, "stream": False,
                   "options": {"temperature": temperature}}
        # 600s: 容忍首次加载大模型（16GB longhun-v4.0 加载可达数分钟）
        with httpx.Client(timeout=600.0) as client:
            resp = client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return {"content": data.get("message", {}).get("content", ""),
                "model": model, "provider": "ollama", "local": True}

    def chat_stream(self, messages, system="", temperature=0.7, model=""):
        import httpx
        model = model or self.default_model
        msgs = ([{"role": "system", "content": system}] if system else []) + list(messages)
        payload = {"model": model, "messages": msgs, "stream": True,
                   "options": {"temperature": temperature}}
        with httpx.Client(timeout=300.0) as client:
            with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except Exception:
                        continue
                    chunk = data.get("message", {}).get("content", "")
                    if chunk:
                        yield chunk


# ============================================================
# 2. 云端适配器（复用 lh_ai_gateway 统一入口 · 配置共享）
# ============================================================
class _GatewayAdapter(ModelAdapter):
    """云端模型基类：复用 lh_ai_gateway 的 chat/chat_stream（含流控 100t/s）。"""

    def __init__(self, adapter_id: str, name: str, model: str = ""):
        self.id = adapter_id
        self.name = name
        self.default_model = model

    def _gw(self):
        from bin.lh_ai_gateway import chat, chat_stream, check_available
        return chat, chat_stream, check_available

    def check(self) -> bool:
        try:
            _, _, check_available = self._gw()
            avail = check_available()
            return bool(avail.get(self.id))
        except Exception:
            return False

    def chat(self, messages, system="", temperature=0.7, model=""):
        chat_fn, _, _ = self._gw()
        r = chat_fn(messages, system=system, temperature=temperature)
        return {"content": r.get("content", ""), "model": r.get("model", self.default_model),
                "provider": self.id, "local": False}

    def chat_stream(self, messages, system="", temperature=0.7, model=""):
        _, stream_fn, _ = self._gw()
        buf = []
        for chunk in stream_fn(messages, system=system, temperature=temperature):
            if chunk:
                buf.append(chunk)
                yield chunk


class DeepSeekAdapter(_GatewayAdapter):
    def __init__(self):
        super().__init__("deepseek", "DeepSeek", "deepseek-v4-flash")


class KimiAdapter(_GatewayAdapter):
    def __init__(self):
        super().__init__("kimi", "Kimi", "moonshot-v1-8k")


class OpenAIAdapter(_GatewayAdapter):
    def __init__(self):
        super().__init__("openai", "OpenAI", "gpt-4o-mini")


class ClaudeAdapter(_GatewayAdapter):
    def __init__(self):
        super().__init__("claude", "Claude", "claude-3-5-sonnet-20241022")


class HunyuanAdapter(_GatewayAdapter):
    def __init__(self):
        super().__init__("hunyuan", "腾讯混元", "hunyuan-lite")


# ============================================================
# 适配器注册表 & 统一调用
# ============================================================
ADAPTER_REGISTRY: Dict[str, Callable[[], ModelAdapter]] = {
    "ollama": OllamaAdapter,
    "deepseek": DeepSeekAdapter,
    "kimi": KimiAdapter,
    "openai": OpenAIAdapter,
    "claude": ClaudeAdapter,
    "hunyuan": HunyuanAdapter,
}


def create_adapter(adapter_id: str) -> Optional[ModelAdapter]:
    factory = ADAPTER_REGISTRY.get(adapter_id)
    return factory() if factory else None


def get_adapter(adapter_id: str) -> ModelAdapter:
    adapter = create_adapter(adapter_id)
    if not adapter:
        raise ValueError(f"❌ 未知适配器: {adapter_id}（可用: {list(ADAPTER_REGISTRY)}）")
    return adapter


def list_adapters() -> List[Dict[str, Any]]:
    """列出全部适配器与可用状态（云端状态一次取齐·避免逐个探测刷屏）。"""
    import logging
    logging.getLogger("lh_ai_gateway").setLevel(logging.WARNING)
    gw_avail: Dict[str, bool] = {}
    try:
        from bin.lh_ai_gateway import check_available
        gw_avail = check_available()
    except Exception:
        pass
    out = []
    for aid in ADAPTER_REGISTRY:
        try:
            a = create_adapter(aid)
            if isinstance(a, _GatewayAdapter):
                available = bool(gw_avail.get(aid))
            else:
                available = a.check()  # ollama 本地探测（快）
            out.append({"id": aid, "name": a.name, "version": a.version,
                        "model": a.default_model, "available": available})
        except Exception as e:
            out.append({"id": aid, "name": aid, "available": False, "error": str(e)})
    return out


def call_any(adapter_id: str, prompt: str, system: str = "",
             temperature: float = 0.7, model: str = "") -> Dict[str, Any]:
    """统一模型调用入口：prompt 字符串 → 模型响应。"""
    adapter = get_adapter(adapter_id)
    return adapter.chat([{"role": "user", "content": prompt}], system=system,
                        temperature=temperature, model=model)


# ============================================================
# PluginKit 插件化（一切模型皆插件）
# ============================================================
def as_plugins() -> List[Any]:
    """把每个 adapter 包装为 PluginKit 插件（id=lh.ai.<adapter>）。"""
    from bin.lh_harness_core import Plugin, PluginMeta

    plugins = []
    for aid in ADAPTER_REGISTRY:
        adapter = create_adapter(aid)
        meta = PluginMeta(
            id=f"lh.ai.{aid}",
            name=f"AI适配器·{adapter.name}",
            version=adapter.version,
            provides=[f"ai.adapter.{aid}"],
            subscribes=["ai.request"],
            file=__file__,
        )

        def make_on_load(adapter_inst: ModelAdapter):
            def on_load(ctx):
                ctx.provide(f"ai.adapter.{adapter_inst.id}", adapter_inst)
                return []
            return on_load

        plugins.append(Plugin(meta, make_on_load(adapter)))
    return plugins


# ============================================================
# CLI
# ============================================================
def main() -> int:
    ap = argparse.ArgumentParser(description="🐉 龍魂 AI 模型适配器 v1.0（一切模型皆插件）")
    ap.add_argument("--list", action="store_true", help="列出所有适配器与可用状态")
    ap.add_argument("--call", metavar="ADAPTER", default="", help="同步调用: --call ollama --prompt ...")
    ap.add_argument("--stream", metavar="ADAPTER", default="", help="流式调用: --stream ollama --prompt ...")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--system", default="")
    ap.add_argument("--model", default="", help="覆盖模型名（默认 adapter.default_model）")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--plugin-demo", action="store_true", help="PluginKit 装载 ollama 插件并调用")
    args = ap.parse_args()

    if args.list:
        print("🐉 AI 模型适配器清单:")
        for a in list_adapters():
            mark = "🟢 可用" if a["available"] else "🟡 未就绪"
            print(f"  {a['id']:<10} {a['name']:<14} {a['model']:<24} {mark}")
        return 0

    if args.plugin_demo:
        from bin.lh_harness_core import PluginRegistry
        print("═══ PluginKit 装载 AI 适配器插件 ═══")
        reg = PluginRegistry()
        for p in as_plugins():
            reg.register(p)
        # 只装载 ollama 插件（云端无密钥时跳过）
        for aid in ("ollama",):
            try:
                reg.load(f"lh.ai.{aid}")
                adapter = reg.plugins[f"lh.ai.{aid}"]._ctx.services.get(f"ai.adapter.{aid}")
                if adapter and adapter.check():
                    r = adapter.chat([{"role": "user", "content": "用一句话自我介绍"}],
                                     model=args.model or "")
                    print(f"  ✅ {aid} 调用成功: {r['content'][:100]}")
                else:
                    print(f"  ⚠️ {aid} 本地服务未就绪（插件已装载，调用降级跳过）")
            except Exception as e:
                print(f"  ❌ 装载失败: {e}")
        return 0

    if args.call or args.stream:
        if not args.prompt:
            print("❌ 需要 --prompt", file=sys.stderr)
            return 2
        aid = args.call or args.stream
        try:
            if args.stream:
                for chunk in get_adapter(aid).chat_stream(
                        [{"role": "user", "content": args.prompt}],
                        system=args.system, temperature=args.temperature, model=args.model):
                    print(chunk, end="", flush=True)
                print()
            else:
                r = call_any(aid, args.prompt, system=args.system,
                             temperature=args.temperature, model=args.model)
                print(f"🐉 [{aid}] {r.get('model','')}")
                print(r.get("content", ""))
        except Exception as e:
            print(f"❌ 调用失败: {e}", file=sys.stderr)
            return 1
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
