#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CNSH 模型路由器 v1.1
DNA: #龍芯⚡️丙午·丙申·庚申·壬午·䷸巽为风-MODEL-ROUTER-v1.1
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟡 待实测（沙箱mock测试通过，真实API调用未验）
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

v1.1 修正（相对 v1.0）:
  🔴→🟢 1. OpenAICompatibleAdapter.__init__ 引用未定义 kwargs（必炸 NameError）→ 改显式参数
  🔴→🟢 2. generate_dna 使用旧时间戳格式（违 P0 干支铁律）→ 接入 lh_ganzhi 干支算法
  🟡→🟢 3. OpenAICompatibleAdapter.call_stream 未实现（流式路由必炸）→ 补 SSE 实现
  🟡→🟢 4. CONFIRM 死代码 → 落地确认码闸门（注册表写操作强制校验）
  🟡→🟢 5. 史官记录只进内存 → 追加落盘 logs/shiguan.jsonl（P0：不删除只冻结）
  🟡→🟢 6. _record_history content=None 防护；清理未用 import

功能:
  1. 模型注册与发现   2. 语言路由   3. 负载均衡与故障转移
  4. 健康检查         5. DNA追溯码注入（干支算法） 6. 三色审计   7. 史官记录（落盘）
"""

import os
import json
import yaml
import requests
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import logging

from lh_ganzhi import generate_dna  # P0：DNA 干支算法，禁止手写时间戳

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


class ConfirmGateError(PermissionError):
    """确认码校验失败"""


def require_confirm(code: str):
    """确认码闸门：注册表写操作/模型增删前强制校验"""
    if code != CONFIRM:
        raise ConfirmGateError("🔴 确认码错误，操作冻结（P0：不删除只冻结，已记录）")


# ============================================================
# 模型注册表
# ============================================================

class ModelRegistry:
    """模型注册表管理器"""

    def __init__(self, config_path: str = "model-registry.yaml"):
        self.config_path = config_path
        self.models: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.config_path):
            self._create_default()
            return
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for model in data.get("models", []):
            self.models[model["id"]] = model

    def _create_default(self):
        """默认注册表（最小可用集，完整清单见 config/model-registry.yaml）"""
        default_models = [
            {"id": "kimi", "name": "Kimi K2.5", "provider": "Moonshot AI", "region": "cn",
             "protocol": "openai-compatible", "endpoint": "https://api.moonshot.cn/v1",
             "model_name": "moonshot-v1-8k", "auth_type": "api-key",
             "languages": ["zh", "en"], "capabilities": ["chat", "translation", "reasoning"],
             "tricolor": "🟢", "status": "active", "weight": 1.0},
            {"id": "jais", "name": "Jais", "provider": "G42 / Inception", "region": "ae",
             "protocol": "ollama-compatible", "endpoint": "http://localhost:11434/api/generate",
             "model_name": "jais:13b", "auth_type": "none",
             "languages": ["ar", "en"], "capabilities": ["chat", "translation"],
             "tricolor": "🟡", "status": "active", "weight": 0.6},
            {"id": "apertus", "name": "Apertus 1.5", "provider": "ETH Zurich / EPFL", "region": "eu",
             "protocol": "ollama-compatible", "endpoint": "http://localhost:11434/api/generate",
             "model_name": "apertus:70b", "auth_type": "none",
             "languages": ["en", "de", "fr", "it"], "capabilities": ["chat", "reasoning"],
             "tricolor": "🟡", "status": "active", "weight": 0.7},
        ]
        self.models = {m["id"]: m for m in default_models}
        self.save(confirm_code=CONFIRM)  # 初始化自举，等同创始签名

    def save(self, confirm_code: str):
        """保存注册表（写操作过确认码闸门）"""
        require_confirm(confirm_code)
        data = {
            "version": "1.1",
            "dna": generate_dna("REGISTRY", "v1.1"),
            "updated_at": datetime.now().isoformat(),
            "models": list(self.models.values())
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def get(self, model_id: str) -> Optional[Dict]:
        return self.models.get(model_id)

    def get_by_language(self, language: str) -> List[Dict]:
        result = [m for m in self.models.values()
                  if m["status"] == "active" and language in m.get("languages", [])]
        return sorted(result, key=lambda x: x.get("weight", 0), reverse=True)

    def get_by_region(self, region: str) -> List[Dict]:
        return [m for m in self.models.values()
                if m.get("region") == region and m["status"] == "active"]

    def get_all_active(self) -> List[Dict]:
        return [m for m in self.models.values() if m["status"] == "active"]

    def add_model(self, model_config: Dict, confirm_code: str) -> bool:
        require_confirm(confirm_code)
        if model_config["id"] in self.models:
            return False
        self.models[model_config["id"]] = model_config
        self.save(confirm_code)
        return True

    def update_status(self, model_id: str, status: str, confirm_code: str) -> bool:
        require_confirm(confirm_code)
        if model_id not in self.models:
            return False
        self.models[model_id]["status"] = status
        self.save(confirm_code)
        return True


# ============================================================
# 模型适配器
# ============================================================

class BaseModelAdapter:
    def __init__(self, config: Dict):
        self.config = config
        self.dna = generate_dna(f"ADAPTER-{config['id'].upper()}", "v1.1")

    def call(self, prompt: str, **kwargs) -> Dict:
        raise NotImplementedError

    def call_stream(self, prompt: str, **kwargs):
        raise NotImplementedError

    def health_check(self) -> bool:
        raise NotImplementedError


class OpenAICompatibleAdapter(BaseModelAdapter):
    """OpenAI 兼容接口适配器（v1.1：修复 __init__ kwargs 未定义必炸 bug）"""

    def __init__(self, config: Dict, timeout: int = 60):
        super().__init__(config)
        self.api_key = os.getenv(f"{config['id'].upper()}_API_KEY", "")
        self.timeout = timeout

    def call(self, prompt: str, **kwargs) -> Dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        dna = generate_dna(f"CALL-{self.config['id'].upper()}", "v1.1")
        payload = {
            "model": self.config.get("model_name", "gpt-3.5-turbo"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            # 注：dna 不入第三方 payload，仅在返回体与史官记录中追溯（防字段外泄）
        }
        try:
            resp = requests.post(
                f"{self.config['endpoint']}/chat/completions",
                headers=headers, json=payload,
                timeout=kwargs.get("timeout", self.timeout)
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "success": True,
                "content": data["choices"][0]["message"]["content"],
                "dna": dna, "model": self.config["id"], "provider": self.config["provider"],
                "tricolor": self.config.get("tricolor", "🟡"),
                "usage": data.get("usage", {})
            }
        except Exception as e:
            return {"success": False, "error": str(e), "dna": dna, "model": self.config["id"]}

    def call_stream(self, prompt: str, **kwargs):
        """v1.1 新增：SSE 流式（v1.0 缺失，流式路由遇 openai 类模型必炸）"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        dna = generate_dna(f"CALL-{self.config['id'].upper()}", "v1.1")
        payload = {
            "model": self.config.get("model_name", "gpt-3.5-turbo"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2000),
            "stream": True,
        }
        try:
            resp = requests.post(
                f"{self.config['endpoint']}/chat/completions",
                headers=headers, json=payload, stream=True,
                timeout=kwargs.get("timeout", 180)
            )
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line or not line.startswith(b"data: "):
                    continue
                body = line[6:].decode()
                if body.strip() == "[DONE]":
                    yield {"chunk": "", "done": True, "dna": dna, "model": self.config["id"]}
                    return
                try:
                    delta = json.loads(body)["choices"][0].get("delta", {})
                    yield {"chunk": delta.get("content", ""), "done": False,
                           "dna": dna, "model": self.config["id"]}
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
            yield {"chunk": "", "done": True, "dna": dna, "model": self.config["id"]}
        except Exception as e:
            yield {"chunk": "", "error": str(e), "done": True, "dna": dna,
                   "model": self.config["id"]}

    def health_check(self) -> bool:
        try:
            resp = requests.get(
                f"{self.config['endpoint']}/models",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=10
            )
            return resp.status_code == 200
        except Exception:
            return False


class OllamaCompatibleAdapter(BaseModelAdapter):
    """Ollama 兼容接口适配器"""

    def call(self, prompt: str, **kwargs) -> Dict:
        dna = generate_dna(f"CALL-{self.config['id'].upper()}", "v1.1")
        payload = {
            "model": self.config.get("model_name", "llama2"),
            "prompt": prompt, "stream": False,
            "options": {"temperature": kwargs.get("temperature", 0.7),
                        "num_predict": kwargs.get("max_tokens", 2000)}
        }
        try:
            resp = requests.post(f"{self.config['endpoint']}", json=payload,
                                 timeout=kwargs.get("timeout", 120))
            resp.raise_for_status()
            data = resp.json()
            return {
                "success": True, "content": data.get("response", ""),
                "dna": dna, "model": self.config["id"], "provider": self.config["provider"],
                "tricolor": self.config.get("tricolor", "🟡"),
                "usage": {"total_tokens": len(prompt) + len(data.get("response", ""))}
            }
        except Exception as e:
            return {"success": False, "error": str(e), "dna": dna, "model": self.config["id"]}

    def call_stream(self, prompt: str, **kwargs):
        dna = generate_dna(f"CALL-{self.config['id'].upper()}", "v1.1")
        payload = {
            "model": self.config.get("model_name", "llama2"),
            "prompt": prompt, "stream": True,
            "options": {"temperature": kwargs.get("temperature", 0.7),
                        "num_predict": kwargs.get("max_tokens", 2000)}
        }
        try:
            resp = requests.post(f"{self.config['endpoint']}", json=payload,
                                 stream=True, timeout=kwargs.get("timeout", 180))
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode())
                        yield {"chunk": data.get("response", ""),
                               "done": data.get("done", False),
                               "dna": dna, "model": self.config["id"]}
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            yield {"chunk": "", "error": str(e), "done": True, "dna": dna,
                   "model": self.config["id"]}

    def health_check(self) -> bool:
        try:
            resp = requests.get("http://localhost:11434/api/version", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False


# ============================================================
# 模型路由器
# ============================================================

class ModelRouter:
    """CNSH 模型路由器"""

    def __init__(self, registry_path: str = "model-registry.yaml",
                 shiguan_log: str = "logs/shiguan.jsonl"):
        self.registry = ModelRegistry(registry_path)
        self.adapters: Dict[str, BaseModelAdapter] = {}
        self._init_adapters()
        self.history: List[Dict] = []
        self.shiguan_log = shiguan_log
        Path(shiguan_log).parent.mkdir(parents=True, exist_ok=True)

    def _init_adapters(self):
        for model in self.registry.get_all_active():
            protocol = model.get("protocol", "ollama-compatible")
            if protocol == "openai-compatible":
                self.adapters[model["id"]] = OpenAICompatibleAdapter(model)
            else:
                self.adapters[model["id"]] = OllamaCompatibleAdapter(model)

    def route(self, prompt: str, language: str = "zh", **kwargs) -> Dict:
        """路由到最优模型（语言路由 + 故障转移，最多尝试 3 个）"""
        models = self.registry.get_by_language(language)
        if not models:
            models = self.registry.get_by_language("en")
        if not models:
            return {"success": False,
                    "error": f"没有支持 {language} 语言的活跃模型",
                    "dna": generate_dna("ROUTE-FAIL", "v1.1")}

        last_error = None
        for model in models[:3]:
            adapter = self.adapters.get(model["id"])
            if not adapter or not adapter.health_check():
                continue
            try:
                result = adapter.call(prompt, **kwargs)
                if result.get("success"):
                    self._record_history(result, prompt, language)
                    result["audit"] = self._audit_result(result)
                    return result
                last_error = result.get("error", "未知错误")
            except Exception as e:
                last_error = str(e)
                continue

        return {"success": False,
                "error": f"所有模型调用失败: {last_error}",
                "dna": generate_dna("ROUTE-FAIL", "v1.1")}

    def route_stream(self, prompt: str, language: str = "zh", **kwargs):
        models = self.registry.get_by_language(language) or self.registry.get_by_language("en")
        if not models:
            yield {"chunk": "", "error": f"没有支持 {language} 语言的活跃模型",
                   "done": True, "dna": generate_dna("ROUTE-FAIL", "v1.1")}
            return
        for model in models[:3]:
            adapter = self.adapters.get(model["id"])
            if not adapter or not adapter.health_check():
                continue
            try:
                for chunk in adapter.call_stream(prompt, **kwargs):
                    yield chunk
                return
            except Exception:
                continue
        yield {"chunk": "", "error": "所有模型调用失败", "done": True,
               "dna": generate_dna("ROUTE-FAIL", "v1.1")}

    def _record_history(self, result: Dict, prompt: str, language: str):
        """史官记录：内存 + 落盘 jsonl（P0：不删除只冻结，只追加）"""
        content = result.get("content") or ""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "dna": result.get("dna"),
            "model": result.get("model"),
            "provider": result.get("provider"),
            "language": language,
            "prompt_length": len(prompt),
            "response_length": len(content),
            "tricolor": result.get("tricolor", "🟡"),
            "success": result.get("success", False)
            # 数据哲学：只传用量不传内容 —— prompt/content 本体不入史官
        }
        self.history.append(entry)
        with open(self.shiguan_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _audit_result(self, result: Dict) -> Dict:
        content = result.get("content") or ""
        score = 100
        if len(content) < 10:
            score -= 20
        if "error" in content.lower():
            score -= 15
        if result.get("dna"):
            score += 5
        tricolor_map = {"🟢": 90, "🟡": 70, "🔴": 40}
        base_score = tricolor_map.get(result.get("tricolor", "🟡"), 70)
        final_score = min(100, (score + base_score) // 2)
        if final_score >= 85:
            color, status = "🟢", "通过"
        elif final_score >= 60:
            color, status = "🟡", "警告"
        else:
            color, status = "🔴", "拒绝"
        return {"tricolor": color, "status": status, "score": final_score,
                "model": result.get("model", "unknown"),
                "provider": result.get("provider", "unknown"),
                "dna": result.get("dna")}

    def get_stats(self) -> Dict:
        total = len(self.history)
        success = sum(1 for h in self.history if h.get("success"))
        by_model = {}
        for h in self.history:
            by_model[h.get("model", "unknown")] = by_model.get(h.get("model", "unknown"), 0) + 1
        return {"total_calls": total,
                "success_rate": success / total if total > 0 else 0,
                "by_model": by_model,
                "active_models": len(self.registry.get_all_active())}


# ============================================================
# CNSH 编辑器集成
# ============================================================

class CNSHEditorModelExtension:
    """CNSH 编辑器模型扩展"""

    def __init__(self, router: ModelRouter):
        self.router = router
        self.current_model: Optional[str] = None
        self.context: List[Dict] = []

    def set_model(self, model_id: str) -> bool:
        model = self.router.registry.get(model_id)
        if model and model["status"] == "active":
            self.current_model = model_id
            return True
        return False

    def get_model(self) -> Optional[str]:
        return self.current_model

    def list_models(self, language: Optional[str] = None) -> List[Dict]:
        if language:
            return self.router.registry.get_by_language(language)
        return self.router.registry.get_all_active()

    def translate(self, text: str, target_lang: str) -> Dict:
        prompt = f"Translate the following text to {target_lang}:\n\n{text}"
        return self.router.route(prompt, language=target_lang)

    def chat(self, prompt: str) -> Dict:
        if self.current_model:
            adapter = self.router.adapters.get(self.current_model)
            if adapter:
                result = adapter.call(self._build_context(prompt))
                if result.get("success"):
                    self._update_context(prompt, result.get("content") or "")
                    result["audit"] = self.router._audit_result(result)
                    return result
        result = self.router.route(prompt)
        if result.get("success"):
            self._update_context(prompt, result.get("content") or "")
        return result

    def _build_context(self, prompt: str) -> str:
        if not self.context:
            return prompt
        context_text = "Previous conversation:\n"
        for entry in self.context[-5:]:
            context_text += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n"
        return context_text + f"\nCurrent question: {prompt}"

    def _update_context(self, user: str, assistant: str):
        self.context.append({"user": user, "assistant": assistant})


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · CNSH 模型路由器 v1.1",
        epilog=f"DNA: {generate_dna('CLI', 'v1.1')}"
    )
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用模型")
    parser.add_argument("-L", "--language", help="按语言筛选模型")
    parser.add_argument("-c", "--call", help="调用模型 (指定提示词)")
    parser.add_argument("-m", "--model", help="指定模型ID")
    parser.add_argument("-s", "--stream", action="store_true", help="流式输出")
    args = parser.parse_args()

    router = ModelRouter()
    editor = CNSHEditorModelExtension(router)

    if args.list:
        models = editor.list_models(args.language)
        print(f"\n🐉 CNSH 可用模型 ({len(models)} 个)")
        print("=" * 60)
        for m in models:
            status = "🟢" if m["status"] == "active" else "🔴"
            print(f"  {status} {m['id']} ({m['name']})")
            print(f"    提供商: {m['provider']} | 地区: {m['region']}")
            print(f"    语言: {', '.join(m.get('languages', []))}")
            print(f"    能力: {', '.join(m.get('capabilities', []))}")
            print(f"    三色: {m.get('tricolor', '🟡')}\n")
    elif args.call:
        if args.model:
            editor.set_model(args.model)
        if args.stream:
            for chunk in router.route_stream(args.call, language=args.language or "zh"):
                print(chunk.get("chunk", ""), end="", flush=True)
                if chunk.get("done"):
                    print()
                    if chunk.get("dna"):
                        print(f"🧬 DNA: {chunk['dna']}")
                    break
        else:
            result = editor.chat(args.call)
            if result.get("success"):
                print(f"🤖 {result.get('model')} ({result.get('provider')})")
                print("-" * 40)
                print(result.get("content", ""))
                print("-" * 40)
                print(f"🧬 DNA: {result.get('dna')}")
                if result.get("audit"):
                    print(f"⚖️ 三色: {result['audit'].get('tricolor')} ({result['audit'].get('status')})")
            else:
                print(f"❌ 错误: {result.get('error')}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
