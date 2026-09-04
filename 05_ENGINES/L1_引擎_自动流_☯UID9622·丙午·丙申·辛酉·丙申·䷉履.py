#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂生态 · 主权网关自动流引擎 v1.0
# 层级: L1_引擎层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-AUTOFLOW-ENGINE-v1.0-UID9622
# 别名: 05_ENGINES/lh_autoflow.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过

核心能力：
  1. 对外部 AI（Kimi / DeepSeek / 本地模型）实施硬控超时
  2. 超时/拒绝自动故障转移
  3. 拒绝或超时自动写入耻辱墙
  4. 全链路审计日志
  5. 全部失败时本地兜底
"""

import os
import sys
import json
import time
import yaml
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

# ============================================================
# 常量与路径
# ============================================================
DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-AUTOFLOW-ENGINE-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID = "9622"

HOME = Path.home()
CONFIG_PATH = HOME / ".longhun" / "configs" / "gateway-hardcode.yaml"
DEFAULT_SHAME_PATH = HOME / ".longhun" / "08_STATE" / "shame_wall.jsonl"
DEFAULT_AUDIT_PATH = HOME / ".longhun" / "04_AUDIT" / "sovereign_gateway.jsonl"


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{suffix}-{UID}-{rand}"


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """加载硬控制配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {"gateway": {}}


def append_jsonl(path: Path, entry: Dict[str, Any]):
    """追加 JSONL"""
    ensure_dir(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def record_audit(operation: str, detail: Dict[str, Any], status: str = "ok"):
    cfg = load_config()
    audit_path = Path(cfg.get("gateway", {}).get("audit", {}).get("path", str(DEFAULT_AUDIT_PATH)))
    audit_path = audit_path.expanduser()
    append_jsonl(audit_path, {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("SOVEREIGN-AUDIT"),
        "operation": operation,
        "status": status,
        "detail": detail,
    })


def write_shame_wall(provider: str, prompt: str, result: Any, reason: str):
    """写入耻辱墙"""
    cfg = load_config()
    if not cfg.get("gateway", {}).get("shame_wall", {}).get("enabled", True):
        return

    shame_path = Path(cfg.get("gateway", {}).get("shame_wall", {}).get("path", str(DEFAULT_SHAME_PATH)))
    shame_path = shame_path.expanduser()
    max_len = cfg.get("gateway", {}).get("shame_wall", {}).get("max_prompt_len", 200)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("SHAME-WALL"),
        "provider": provider,
        "prompt": prompt[:max_len],
        "reason": reason,
        "result": str(result)[:500] if result is not None else None,
    }
    append_jsonl(shame_path, entry)
    print(f"   🧱 耻辱墙记录: {provider} → {reason}")


# ============================================================
# AI 提供方实现
# ============================================================
def provider_kimi(prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Kimi 提供方（占位/可替换为真实 API）"""
    # 真实实现：调用 Kimi API
    # 这里提供可插拔结构；未配置时模拟响应
    env_mock = os.environ.get("LH_MOCK_KIMI", "").lower()
    if env_mock == "timeout":
        time.sleep(10)
        return {"status": "timeout"}
    if env_mock == "refuse":
        return {"status": "refused", "reason": "policy"}
    if env_mock == "fail":
        raise RuntimeError("Kimi mock failure")
    return {
        "status": "success",
        "provider": "kimi",
        "content": f"[Kimi] {prompt[:80]}...",
        "dna": generate_dna("KIMI"),
    }


def provider_deepseek(prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """DeepSeek 提供方"""
    env_mock = os.environ.get("LH_MOCK_DEEPSEEK", "").lower()
    if env_mock == "timeout":
        time.sleep(10)
        return {"status": "timeout"}
    if env_mock == "refuse":
        return {"status": "refused", "reason": "policy"}
    if env_mock == "fail":
        raise RuntimeError("DeepSeek mock failure")
    return {
        "status": "success",
        "provider": "deepseek",
        "content": f"[DeepSeek] {prompt[:80]}...",
        "dna": generate_dna("DEEPSEEK"),
    }


def provider_local_qwen(prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """本地 Qwen 提供方（尝试 mlx_lm）"""
    try:
        from mlx_lm import load, generate
        cfg = load_config()
        model_path = cfg.get("gateway", {}).get("local_fallback", {}).get("model_path", "~/longhun-system/models/qwen-1.5b")
        model_path = Path(model_path).expanduser()
        if model_path.exists():
            model, tokenizer = load(str(model_path))
            response = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=256)
            return {"status": "success", "provider": "local_qwen", "content": response, "dna": generate_dna("LOCAL-QWEN")}
    except Exception as e:
        pass

    env_mock = os.environ.get("LH_MOCK_LOCAL_QWEN", "").lower()
    if env_mock in ("timeout", "refuse", "fail"):
        raise RuntimeError("local_qwen unavailable")
    return {
        "status": "success",
        "provider": "local_qwen",
        "content": f"[本地Qwen占位] {prompt[:80]}...",
        "dna": generate_dna("LOCAL-QWEN-MOCK"),
    }


def provider_local_llama(prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """本地 Llama 提供方"""
    env_mock = os.environ.get("LH_MOCK_LOCAL_LLAMA", "").lower()
    if env_mock in ("timeout", "refuse", "fail"):
        raise RuntimeError("local_llama unavailable")
    return {
        "status": "success",
        "provider": "local_llama",
        "content": f"[本地Llama占位] {prompt[:80]}...",
        "dna": generate_dna("LOCAL-LLAMA"),
    }


PROVIDERS: Dict[str, Callable] = {
    "kimi": provider_kimi,
    "deepseek": provider_deepseek,
    "local_qwen": provider_local_qwen,
    "local_llama": provider_local_llama,
}


# ============================================================
# 主权网关
# ============================================================
class SovereignGate:
    """主权网关 - 控制所有外部 AI"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.cfg = config or load_config().get("gateway", {})
        self.max_wait = int(self.cfg.get("max_wait", 5))
        self.chain = self.cfg.get("fallback_chain", ["kimi", "deepseek", "local_qwen", "local_llama"])
        self.on_refusal = self.cfg.get("refused_action", "audit_and_shame")
        self.on_dead = self.cfg.get("dead_ai_action", "auto_failover")

    def execute(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """执行指令，自动故障转移"""
        print(f"🐉 主权网关执行: {prompt[:60]}...")
        record_audit("execute_start", {"prompt": prompt[:200], "chain": self.chain})

        for provider in self.chain:
            result = self._call_provider(provider, prompt, context)
            if result.get("status") == "success":
                print(f"   ✅ 命中: {provider}")
                record_audit("execute_success", {"provider": provider, "result": result.get("content", "")[:200]})
                return result

            reason = result.get("reason", result.get("error", "unknown"))
            print(f"   ⚠️ {provider} 失败: {reason}")

        # 全部失败，本地兜底
        return self._local_fallback(prompt)

    def _call_provider(self, provider: str, prompt: str, context: Optional[Dict]) -> Dict[str, Any]:
        fn = PROVIDERS.get(provider)
        if not fn:
            return {"status": "error", "provider": provider, "error": f"未知提供方 {provider}"}

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(fn, prompt, context)
                result = future.result(timeout=self.max_wait)

            if result.get("status") == "refused":
                if self.on_refusal == "audit_and_shame":
                    write_shame_wall(provider, prompt, result, "refused")
                    record_audit("provider_refused", {"provider": provider, "reason": result.get("reason")})
                return {**result, "provider": provider}

            if result.get("status") == "timeout":
                if self.on_dead == "auto_failover":
                    write_shame_wall(provider, prompt, result, "timeout")
                    record_audit("provider_timeout", {"provider": provider, "max_wait": self.max_wait})
                return {**result, "provider": provider}

            return result

        except FutureTimeoutError:
            write_shame_wall(provider, prompt, None, "future_timeout")
            record_audit("provider_timeout", {"provider": provider, "max_wait": self.max_wait})
            return {"status": "error", "provider": provider, "error": f"超时 ({self.max_wait}s)"}

        except Exception as e:
            write_shame_wall(provider, prompt, None, f"exception:{e}")
            record_audit("provider_exception", {"provider": provider, "error": str(e)})
            return {"status": "error", "provider": provider, "error": str(e)}

    def _local_fallback(self, prompt: str) -> Dict[str, Any]:
        print("   🛡️ 全部外部AI失败，启用本地兜底")
        result = {
            "status": "success",
            "provider": "local_fallback",
            "content": f"🟢 本地引擎兜底响应: {prompt[:100]}...",
            "dna": generate_dna("LOCAL-FALLBACK"),
        }
        record_audit("local_fallback", {"prompt": prompt[:200]})
        return result


# ============================================================
# CLI
# ============================================================
def print_help():
    print("""
🐉 龍魂 · 主权网关自动流引擎 v1.0

用法:
  lh_autoflow.py ask "你的指令"               # 走完整 fallback 链
  lh_autoflow.py test-timeout                # 模拟 Kimi 超时，测试切换
  lh_autoflow.py test-refuse                 # 模拟 Kimi 拒绝，测试耻辱墙
  lh_autoflow.py test-fail                   # 模拟全部失败，测试本地兜底
  lh_autoflow.py config                      # 打印当前硬控配置
  lh_autoflow.py shame                       # 查看耻辱墙

环境变量（测试用）:
  LH_MOCK_KIMI=timeout/refuse/fail
  LH_MOCK_DEEPSEEK=timeout/refuse/fail
  LH_MOCK_LOCAL_QWEN=timeout/refuse/fail
  LH_MOCK_LOCAL_LLAMA=timeout/refuse/fail
    """)


def main():
    args = sys.argv[1:]
    if not args:
        print_help()
        return

    cmd = args[0]

    if cmd == "ask" and len(args) >= 2:
        prompt = args[1]
        gate = SovereignGate()
        result = gate.execute(prompt)
        print("\n🐉 最终结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "config":
        cfg = load_config()
        print(json.dumps(cfg, ensure_ascii=False, indent=2))

    elif cmd == "shame":
        cfg = load_config()
        shame_path = Path(cfg.get("gateway", {}).get("shame_wall", {}).get("path", str(DEFAULT_SHAME_PATH))).expanduser()
        if not shame_path.exists():
            print("🧱 耻辱墙为空")
            return
        with open(shame_path, "r", encoding="utf-8") as f:
            for line in f:
                print(line.strip())

    elif cmd == "test-timeout":
        os.environ["LH_MOCK_KIMI"] = "timeout"
        gate = SovereignGate()
        result = gate.execute("测试超时切换")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "test-refuse":
        os.environ["LH_MOCK_KIMI"] = "refuse"
        gate = SovereignGate()
        result = gate.execute("测试拒绝审计")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "test-fail":
        os.environ["LH_MOCK_KIMI"] = "fail"
        os.environ["LH_MOCK_DEEPSEEK"] = "fail"
        os.environ["LH_MOCK_LOCAL_QWEN"] = "fail"
        os.environ["LH_MOCK_LOCAL_LLAMA"] = "fail"
        gate = SovereignGate()
        result = gate.execute("测试全部失败兜底")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print_help()


if __name__ == "__main__":
    main()
