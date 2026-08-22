#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-AI-PROVIDERS-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 CNSH IDE · 国产 AI 多厂商路由

支持通过官方 API 接入：
  - Kimi（月之暗面）
  - 通义千问（阿里 DashScope）
  - DeepSeek
  - 智谱 AI（GLM-4）
  - 字节豆包（Ark）
  - 文心一言（百度千帆）—— TODO
  - 讯飞星火 —— TODO
  - 腾讯混元 —— TODO

设计原则：
  1. API Key 由用户本地配置提供，绝不写死在仓库。
  2. 默认 OpenAI 兼容接口优先，降低接入成本。
  3. 无 key 时自动进入模拟模式，不影响 IDE 基本使用。
"""

import os
import json
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Callable

# 优先使用 requests；未安装时提供降级提示
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None  # type: ignore[assignment]
    HAS_REQUESTS = False

# 请求异常类型（requests 缺失时降级为 Exception，避免 except 子句引用未绑定模块）
HTTP_EXCEPTIONS = requests.exceptions.RequestException if HAS_REQUESTS else Exception  # type: ignore[union-attr]


# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════

@dataclass
class AIProviderConfig:
    name: str
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    enabled: bool = False
    extra: Optional[Dict] = None

    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


@dataclass
class ChatMessage:
    role: str  # system / user / assistant
    content: str


# ═══════════════════════════════════════════════════════
# 基类
# ═══════════════════════════════════════════════════════

class BaseAIProvider(ABC):
    """AI 厂商抽象基类"""

    def __init__(self, config: AIProviderConfig):
        self.config = config

    @property
    def ready(self) -> bool:
        return bool(self.config.api_key)

    @abstractmethod
    def chat(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        """发起对话，返回模型回复文本"""
        pass

    def ask(self, prompt: str, system: str = "你是一个 helpful 的 CNSH 中文编程助手。") -> str:
        """单轮问答快捷方式"""
        messages = [
            ChatMessage(role="system", content=system),
            ChatMessage(role="user", content=prompt),
        ]
        return self.chat(messages)


class MockProvider(BaseAIProvider):
    """无 key 或测试时的模拟提供者"""

    def chat(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        user_msg = messages[-1].content if messages else ""
        return f"[模拟AI理解] {user_msg[:80]}"


# ═══════════════════════════════════════════════════════
# OpenAI 兼容接口（Kimi / 通义 / DeepSeek / 智谱 / 豆包）
# ═══════════════════════════════════════════════════════

class OpenAICompatibleProvider(BaseAIProvider):
    """OpenAI 兼容 REST 接口通用实现"""

    def chat(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        if not HAS_REQUESTS:
            return "[错误] 未安装 requests，无法调用真实 AI"
        if not self.ready:
            return "[错误] 该厂商 API Key 未配置"

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
        }

        resp = None
        try:
            assert requests is not None  # HAS_REQUESTS=True 时 import 必成功
            resp = requests.post(
                f"{self.config.base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except HTTP_EXCEPTIONS as e:
            return f"[AI 请求失败] {type(e).__name__}: {e}"
        except (KeyError, IndexError) as e:
            return f"[AI 响应解析失败] {e}: {getattr(resp, 'text', '')[:200]}"


class OllamaProvider(BaseAIProvider):
    """本地 Ollama 模型服务

    默认地址：http://127.0.0.1:11434
    无需 API Key，零后续费用，适合个人开发者与离线环境。
    """

    @property
    def ready(self) -> bool:
        """通过检测 Ollama 服务是否可用来判断"""
        if not HAS_REQUESTS:
            return False
        try:
            assert requests is not None  # HAS_REQUESTS=True 时 import 必成功
            resp = requests.get(f"{self.config.base_url.rstrip('/')}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def _has_model(self, model_name: str) -> bool:
        if not HAS_REQUESTS:
            return False
        try:
            assert requests is not None  # HAS_REQUESTS=True 时 import 必成功
            resp = requests.get(f"{self.config.base_url.rstrip('/')}/api/tags", timeout=5)
            data = resp.json()
            available = [m.get("name", "") for m in data.get("models", [])]
            # 支持 name 或 name:tag 匹配
            return any(m == model_name or m.startswith(model_name + ":") for m in available)
        except Exception:
            return False

    def chat(self, messages: List[ChatMessage], temperature: float = 0.7) -> str:
        if not HAS_REQUESTS:
            return "[错误] 未安装 requests，无法连接本地模型"
        if not self.ready:
            return "[错误] Ollama 本地服务未启动，请运行：ollama serve"

        model = self.config.model or "longhun-v43:latest"
        if not self._has_model(model):
            return f"[错误] Ollama 中未找到模型 '{model}'，请先执行：ollama pull {model}"

        # 取最后一条 user 消息作为 prompt，系统消息作为 system
        system_msg = ""
        user_msg = ""
        for m in messages:
            if m.role == "system":
                system_msg = m.content
            elif m.role == "user":
                user_msg = m.content

        if not user_msg and messages:
            user_msg = messages[-1].content

        payload = {
            "model": model,
            "prompt": user_msg,
            "system": system_msg,
            "stream": False,
            "options": {"temperature": temperature},
        }

        resp = None
        try:
            assert requests is not None  # HAS_REQUESTS=True 时 import 必成功
            resp = requests.post(
                f"{self.config.base_url.rstrip('/')}/api/generate",
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "[错误] Ollama 返回为空")
        except HTTP_EXCEPTIONS as e:
            return f"[本地模型请求失败] {type(e).__name__}: {e}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"[本地模型响应解析失败] {e}: {getattr(resp, 'text', '')[:200]}"


# ═══════════════════════════════════════════════════════
# 厂商预设
# ═══════════════════════════════════════════════════════

PROVIDER_PRESETS: Dict[str, Dict] = {
    "kimi": {
        "name": "Kimi（月之暗面）",
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
    },
    "tongyi": {
        "name": "通义千问（阿里）",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo",
    },
    "deepseek": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-v4-flash",
    },
    "zhipu": {
        "name": "智谱 AI",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4",
    },
    "doubao": {
        "name": "字节豆包（Ark）",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-lite-4k",
    },
    "wenxin": {
        "name": "文心一言（百度千帆）",
        "base_url": "TODO",
        "model": "TODO",
    },
    "xinghuo": {
        "name": "讯飞星火",
        "base_url": "TODO",
        "model": "TODO",
    },
    "hunyuan": {
        "name": "腾讯混元",
        "base_url": "TODO",
        "model": "TODO",
    },
    "local": {
        "name": "本地模型 (Ollama)",
        "base_url": "http://127.0.0.1:11434",
        "model": "longhun-v43:latest",
    },
}


def build_provider(key: str, config: AIProviderConfig) -> BaseAIProvider:
    """根据 key 创建对应 provider 实例"""
    if key == "local":
        return OllamaProvider(config)
    if key in ("kimi", "tongyi", "deepseek", "zhipu", "doubao"):
        return OpenAICompatibleProvider(config)
    if key in ("wenxin", "xinghuo", "hunyuan"):
        return MockProvider(config)  # 待实现
    return MockProvider(config)


# ═══════════════════════════════════════════════════════
# 路由器
# ═══════════════════════════════════════════════════════

class AIRouter:
    """多厂商 AI 路由

    配置文件位置：~/.cnsh/ai_config.json
    示例：
    {
      "default": "kimi",
      "providers": {
        "kimi": {
          "api_key": "sk-xxx",
          "model": "moonshot-v1-8k",
          "enabled": true
        },
        "deepseek": {
          "api_key": "sk-xxx",
          "enabled": true
        }
      }
    }
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or (Path.home() / ".cnsh" / "ai_config.json")
        self.providers: Dict[str, BaseAIProvider] = {}
        self.default_key: str = "mock"
        self.last_loaded_at: Optional[str] = None
        self._load()

    @staticmethod
    def _env_key_for(provider_key: str) -> str:
        """从环境变量读取对应厂商的 API key"""
        env_map = {
            "kimi": ["KIMI_API_KEY"],
            "tongyi": ["TONGYI_API_KEY", "DASHSCOPE_API_KEY"],
            "deepseek": ["DEEPSEEK_API_KEY"],
            "zhipu": ["ZHIPU_API_KEY"],
            "doubao": ["DOUBAO_API_KEY", "ARK_API_KEY"],
            "wenxin": ["WENXIN_API_KEY", "QIANFAN_API_KEY"],
            "xinghuo": ["XINGHUO_API_KEY", "SPARK_API_KEY"],
            "hunyuan": ["HUNYUAN_API_KEY"],
        }
        for env_name in env_map.get(provider_key, []):
            value = os.environ.get(env_name, "").strip()
            if value:
                return value
        return ""

    def _load(self):
        """从本地配置文件加载，并允许环境变量覆盖 key"""
        raw = {}
        if self.config_path.exists():
            try:
                raw = json.loads(self.config_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, IOError) as e:
                print(f"[CNSH AI] 读取配置失败: {e}", file=__import__("sys").stderr)

        self.default_key = raw.get("default", "")
        user_providers = raw.get("providers", {})

        for key, preset in PROVIDER_PRESETS.items():
            user_cfg = user_providers.get(key, {})
            # 优先级：配置文件 > 环境变量 > 空
            api_key = user_cfg.get("api_key", "") or self._env_key_for(key)
            cfg = AIProviderConfig(
                name=preset["name"],
                api_key=api_key,
                base_url=user_cfg.get("base_url", preset["base_url"]),
                model=user_cfg.get("model", preset["model"]),
                enabled=user_cfg.get("enabled", False) or bool(api_key),
            )
            self.providers[key] = build_provider(key, cfg)

        # 始终保留 mock
        self.providers["mock"] = MockProvider(AIProviderConfig(name="模拟模式", enabled=True))

        # 默认厂商选择：用户指定 > 本地模型 > 第一个可用的云厂商 > mock
        if self.default_key and self.default_key in self.providers and self.providers[self.default_key].ready:
            pass  # 用户指定且可用，保持不变
        else:
            candidates = ["local"] + [k for k in PROVIDER_PRESETS if k != "local"]
            chosen = None
            for key in candidates:
                if key in self.providers and self.providers[key].ready:
                    chosen = key
                    break
            self.default_key = chosen if chosen else "mock"

        self.last_loaded_at = datetime.now().isoformat()

    def reload(self) -> bool:
        """热重载配置文件，返回是否成功"""
        try:
            self._load()
            return True
        except Exception as e:
            print(f"[CNSH AI] 热重载失败: {e}", file=__import__("sys").stderr)
            return False

    def ask(self, prompt: str, provider_key: Optional[str] = None, system: Optional[str] = None) -> str:
        """使用指定或默认厂商进行单轮问答"""
        key = provider_key or self.default_key
        if key not in self.providers:
            key = "mock"
        provider = self.providers[key]
        if not provider.ready:
            provider = self.providers["mock"]
        return provider.ask(prompt, system=system or "你是一个 helpful 的 CNSH 中文编程助手。")

    def list_providers(self) -> List[Dict]:
        """列出所有厂商状态（脱敏）"""
        result = []
        for key, p in self.providers.items():
            cfg = p.config
            masked_key = ""
            if cfg.api_key:
                if len(cfg.api_key) <= 8:
                    masked_key = "***"
                else:
                    masked_key = cfg.api_key[:4] + "..." + cfg.api_key[-4:]
            result.append({
                "key": key,
                "name": cfg.name,
                "model": cfg.model,
                "base_url": cfg.base_url,
                "enabled": cfg.enabled,
                "ready": p.ready,
                "is_default": key == self.default_key,
                "api_key_masked": masked_key,
            })
        return result

    def get_default(self) -> Dict:
        """返回默认厂商信息"""
        p = self.providers.get(self.default_key)
        return {
            "key": self.default_key,
            "name": p.config.name if p else "",
            "ready": p.ready if p else False,
        }

    def save_config(self, config_data: Dict) -> bool:
        """保存用户配置到本地文件"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(json.dumps(config_data, ensure_ascii=False, indent=2), encoding="utf-8")
            self._load()
            return True
        except IOError as e:
            print(f"[CNSH AI] 保存配置失败: {e}", file=__import__("sys").stderr)
            return False


# ═══════════════════════════════════════════════════════
# 便捷：生成单例与 CNSH 兼容回调
# ═══════════════════════════════════════════════════════

_default_router: Optional[AIRouter] = None


def get_router(config_path: Optional[Path] = None) -> AIRouter:
    global _default_router
    if _default_router is None or config_path:
        _default_router = AIRouter(config_path)
    return _default_router


def make_cnsh_ai_callback(router: Optional[AIRouter] = None) -> Callable[[str], str]:
    """生成一个可被 CNSH 解释器调用的 ask(prompt) -> answer 函数"""
    r = router or get_router()

    def ask(prompt: str) -> str:
        return r.ask(prompt)

    return ask


# 兼容无参数直接测试
if __name__ == "__main__":
    router = get_router()
    print("默认厂商:", router.get_default())
    print("厂商列表:", json.dumps(router.list_providers(), ensure_ascii=False, indent=2))
    print("测试调用:", router.ask("把 CNSH 编译成 Python"))
