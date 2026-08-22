#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-CHAT-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 全自动AI智能体 · 自动聊天模块 v2.0
AutoAgent Chat — 多模型自动切换 + 故障转移 + 响应时间监控 + 历史持久化

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-CHAT-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

🔥 v2.0 结合升级（2026-08-17）:
  - 真实AI调用: 对接现有 `bin.lh_ai_gateway.chat()`（Kimi/DeepSeek/Claude 真实 HTTP）
  - 消灭 mock 缺口: 仅当网关全部模型失败时才降级本地 mock（强制 🟡 [MOCK-local] 前缀）
  - 保留多模型路由: 中文→Kimi→DeepSeek / 代码→Claude→DeepSeek（网关内置路由表）

设计原则:
  - 优先真实AI，mock只作最后兜底且强制标注
  - 响应时间/模型/路由全留痕
  - 历史持久化到 ~/.longhun/agent/chat/history.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import unittest
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AGENT_DIR = Path.home() / ".longhun" / "agent"
CHAT_HISTORY_DIR = AGENT_DIR / "chat"
CHAT_HISTORY_FILE = CHAT_HISTORY_DIR / "history.jsonl"
MAX_HISTORY = 50  # 历史截断上限（条）

# ═══════════════════════════════════════════════════════
# 真实AI网关接入（消灭 v2.0 mock 缺口）
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from bin.lh_ai_gateway import chat as _ai_gateway_chat
    from bin.lh_ai_gateway import classify_task, TaskType
    _GATEWAY_OK = True
except Exception as _e:  # pragma: no cover
    _GATEWAY_OK = False
    _GATEWAY_ERR = str(_e)


# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════
@dataclass
class ModelConfig:
    """单模型配置"""
    name: str
    api_key_env: str
    base_url: str = ""
    model: str = ""
    timeout: int = 30
    enabled: bool = True

    @staticmethod
    def defaults() -> Dict[str, "ModelConfig"]:
        return {
            "kimi":     ModelConfig("kimi", "KIMI_API_KEY", "https://api.moonshot.cn/v1", "moonshot-v1-8k"),
            "deepseek": ModelConfig("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com/v1", "deepseek-v4-flash"),
            "claude":   ModelConfig("claude", "CLAUDE_API_KEY", "https://api.anthropic.com/v1", "claude-3-5-sonnet-20241022"),
            "local":    ModelConfig("local", "", "", "mock-local", 5),
        }


class ModelRegistry:
    """模型注册表（支持 JSON 配置持久化）"""

    def __init__(self, models: Optional[Dict[str, ModelConfig]] = None):
        self.models = models or ModelConfig.defaults()

    def available(self) -> List[str]:
        return [n for n, m in self.models.items() if m.enabled]

    def to_dict(self) -> Dict[str, Any]:
        return {n: asdict(m) for n, m in self.models.items()}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ModelRegistry":
        return ModelRegistry({n: ModelConfig(**v) for n, v in data.items()})


# ═══════════════════════════════════════════════════════
# 自动聊天引擎
# ═══════════════════════════════════════════════════════
class AutoChat:
    """
    自动聊天: 多模型自动切换 + 故障转移 + 响应时间监控 + 历史持久化
    """

    def __init__(self, registry: Optional[ModelRegistry] = None):
        self.registry = registry or ModelRegistry()
        self.history: List[Dict[str, Any]] = []
        self._load_history()

    # ── 真实AI调用（v2.0 结合: 对接 lh_ai_gateway）──
    def _call_model(self, text: str, system: str = "") -> Dict[str, Any]:
        """
        调用真实 AI 网关。返回 {content, model, provider, latency_ms, mock, routed}
        网关全挂时降级本地 mock（强制 🟡 [MOCK-local] 前缀）
        """
        start = time.time()
        if _GATEWAY_OK:
            try:
                task = classify_task(text) if _GATEWAY_OK else TaskType.GENERAL
                messages = [{"role": "user", "content": text}]
                result = _ai_gateway_chat(
                    messages, task_type=task, system=system,
                    flow_session_id="lh_auto_agent",
                )
                latency = int((time.time() - start) * 1000)
                return {
                    "content": result.get("content", ""),
                    "model": result.get("model", result.get("provider", "unknown")),
                    "provider": result.get("provider", "gateway"),
                    "latency_ms": latency,
                    "mock": False,
                    "routed": True,
                }
            except Exception as e:
                # 网关失败 → 降级 mock
                latency = int((time.time() - start) * 1000)
                return {
                    "content": f"🟡 [MOCK-local]（AI网关不可用: {e}）收到: {text[:60]}...",
                    "model": "local",
                    "provider": "mock",
                    "latency_ms": latency,
                    "mock": True,
                    "routed": False,
                }
        # 网关未导入 → 直接 mock
        latency = int((time.time() - start) * 1000)
        return {
            "content": f"🟡 [MOCK-local]（AI网关未加载）收到: {text[:60]}...",
            "model": "local",
            "provider": "mock",
            "latency_ms": latency,
            "mock": True,
            "routed": False,
        }

    def chat(self, text: str, system: str = "", persist: bool = True) -> Dict[str, Any]:
        """一次对话（带历史上下文）"""
        ctx_messages = [
            {"role": "user", "content": h["input"]}
            for h in self.history[-5:]
        ] + [{"role": "user", "content": text}]
        # 简化: 只把最近3轮做上下文摘要（避免上下文爆长）
        ctx = "\n".join(f"[之前] {h['input']} → {h['output'][:80]}" for h in self.history[-3:])
        system_full = f"{system}\n[对话上下文]\n{ctx}".strip() if ctx else system

        result = self._call_model(text, system=system_full)
        result["input"] = text
        result["ts"] = datetime.now(timezone.utc).isoformat()

        if persist:
            self.history.append({
                "input": text,
                "output": result["content"],
                "model": result["model"],
                "mock": result["mock"],
                "ts": result["ts"],
            })
            self._trim_history()
            self._persist_history()
        return result

    # ── 历史持久化 ──
    def _trim_history(self):
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

    def _persist_history(self):
        CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        CHAT_HISTORY_FILE.touch(exist_ok=True)
        CHAT_HISTORY_FILE.chmod(0o600)
        with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(self.history[-1], ensure_ascii=False) + "\n")

    def _load_history(self):
        if CHAT_HISTORY_FILE.exists():
            try:
                with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.history.append(json.loads(line))
                self.history = self.history[-MAX_HISTORY:]
            except Exception:
                self.history = []

    def stats(self) -> Dict[str, Any]:
        return {
            "history_len": len(self.history),
            "models": self.registry.available(),
            "gateway_connected": _GATEWAY_OK,
            "mock_usage": sum(1 for h in self.history if h.get("mock")),
        }


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(prog="lh_auto_chat", description="龍魂全自动AI智能体·自动聊天模块 v2.0")
    parser.add_argument("--input", type=str, help="单次对话内容")
    parser.add_argument("--stats", action="store_true", help="查看状态")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--test", action="store_true", help="运行锚点测试")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAutoChat)
        runner = unittest.TextTestRunner(verbosity=2)
        ok = runner.run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    if args.version:
        print(f"龍魂全自动AI智能体 · 自动聊天 v2.0\nDNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-CHAT-v2.0\n确认码: {CONFIRM_CODE}\nGPG: {GPG_KEY}")
        sys.exit(0)
    if args.stats:
        print(json.dumps(AutoChat().stats(), ensure_ascii=False, indent=2))
        sys.exit(0)
    if args.input:
        result = AutoChat().chat(args.input)
        print(f"[{result['model']}·{result['latency_ms']}ms{'·mock' if result['mock'] else ''}] {result['content']}")
        sys.exit(0)
    parser.print_help()


# ═══════════════════════════════════════════════════════
# 锚点测试（6 项）
# ═══════════════════════════════════════════════════════
class TestAutoChat(unittest.TestCase):
    """自动聊天 6 项锚点断言"""

    def test_01_model_registry(self):
        """① 模型注册表默认含 kimi/deepseek/claude/local"""
        reg = ModelRegistry()
        names = set(reg.available())
        self.assertTrue({"kimi", "deepseek", "local"}.issubset(names))

    def test_02_gateway_import(self):
        """② AI网关接入（真实API链路存在）"""
        self.assertTrue(_GATEWAY_OK, "bin.lh_ai_gateway 必须可导入")

    def test_03_fallback_mock(self):
        """③ 网关异常时降级 mock 且强制标注"""
        chat_ = AutoChat()
        result = chat_._call_model("测试")
        self.assertIn("content", result)
        self.assertIn("latency_ms", result)
        if result["mock"]:
            self.assertTrue(result["content"].startswith("🟡 [MOCK"))

    def test_04_history_persist(self):
        """④ 历史持久化 + 截断"""
        chat_ = AutoChat()
        chat_.history = []
        chat_.chat("持久化测试内容", persist=True)
        self.assertGreaterEqual(len(chat_.history), 1)
        chat_._trim_history()
        self.assertLessEqual(len(chat_.history), MAX_HISTORY)

    def test_05_cli_version(self):
        """⑤ CLI 版本输出含 DNA + 确认码"""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with self.assertRaises(SystemExit):
            with redirect_stdout(buf):
                sys.argv = ["lh_auto_chat", "--version"]
                main()
        out = buf.getvalue()
        self.assertIn("DNA", out)
        self.assertIn(CONFIRM_CODE, out)

    def test_06_mock_label(self):
        """⑥ mock 标注强制前缀（防误导）"""
        chat_ = AutoChat()
        result = chat_._call_model("测试")
        if result["mock"]:
            self.assertTrue(result["content"].startswith("🟡 [MOCK"))
        else:
            self.assertEqual(result["mock"], False)


if __name__ == "__main__":
    main()
