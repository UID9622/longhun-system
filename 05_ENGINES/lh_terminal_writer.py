#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 多模型终端写作引擎 (Terminal Writer Engine)
DNA: #龍芯⚡️丙午·丙申·丁酉·庚子·䷉履-TERMINAL-WRITER-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 终端一键调用多模型写作（DeepSeek / Kimi / CodeBuddy / Ollama / 自定义模型），
      主权网关自动故障转移，超时/拒绝自动切换，支持文件保存/提交前自动触发。
      鲲鹏 ARM64 原生友好：纯 Python + SQLite，无强制外部依赖。

用法:
  python3 05_ENGINES/lh_terminal_writer.py ask "帮我写一段龍魂系统介绍"
  python3 05_ENGINES/lh_terminal_writer.py auto ./README.md
  python3 05_ENGINES/lh_terminal_writer.py config
  python3 05_ENGINES/lh_terminal_writer.py status
  python3 05_ENGINES/lh_terminal_writer.py shame-wall [--limit N]   # 耻辱墙看板
  python3 05_ENGINES/lh_terminal_writer.py health                   # 模型健康检查
  python3 05_ENGINES/lh_terminal_writer.py stats                    # 统计看板
"""

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path.home() / ".longhun" / "configs"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR = PROJECT_ROOT / ".state" / "terminal_writer"
STATE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = STATE_DIR / "writer.sqlite"

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·丁酉·子时-TERMINAL-WRITER-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

# 默认超时（秒）：Kimi装死就切
DEFAULT_TIMEOUT = 8


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS writer_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            provider TEXT,
            prompt TEXT,
            response TEXT,
            status TEXT,
            duration_ms INTEGER,
            session_id TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS shame_wall (
            timestamp TEXT,
            provider TEXT,
            reason TEXT,
            prompt_snippet TEXT
        )
        """
    )
    conn.commit()
    return conn


# ============================================================
# 配置管理
# ============================================================

DEFAULT_CONFIG = {
    "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "timeout": DEFAULT_TIMEOUT,
    "fallback_chain": ["dsh", "ollama", "kimi", "codebuddy", "custom"],
    "providers": {
        "dsh": {
            "enabled": True,
            "url": "http://127.0.0.1:2284/api/headless",
            "model": "deepseek-r1:14b",
        },
        "ollama": {
            "enabled": True,
            "url": "http://127.0.0.1:11434/api/generate",
            "model": "deepseek-r1:14b",
        },
        "kimi": {
            "enabled": False,
            "url": "https://api.moonshot.cn/v1/chat/completions",
            "api_key": "${KIMI_API_KEY}",
            "model": "moonshot-v1-8k",
        },
        "codebuddy": {
            "enabled": False,
            "mode": "vscode_command",
            "command": "codebuddy.terminal.write",
        },
        "custom": {
            "enabled": False,
            "url": "${CUSTOM_MODEL_URL}",
            "api_key": "${CUSTOM_API_KEY}",
            "model": "custom-model",
        },
    },
    "auto_trigger": {
        "enabled": True,
        "watch_dirs": [".", "docs", "12_DOCS"],
        "patterns": ["*.md", "*.txt"],
        "keywords": ["TODO", "FIXME", "待补充"],
        "on_git_commit": True,
        "cooldown_seconds": 60,
    },
    "system_prompt_file": str(CONFIG_DIR / "longhun-system-prompt.md"),
}


def load_config() -> Dict[str, Any]:
    config_path = CONFIG_DIR / "terminal-writer.yaml"
    if config_path.exists():
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
            if cfg:
                return cfg
        except Exception:
            pass
    return DEFAULT_CONFIG


def save_config(cfg: Dict[str, Any]):
    config_path = CONFIG_DIR / "terminal-writer.yaml"
    try:
        import yaml
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"⚠️ 保存配置失败: {e}")


# ============================================================
# HTTP 工具（requests 可选）
# ============================================================

try:
    import requests
    HAS_REQUESTS = True
except Exception:
    HAS_REQUESTS = False


def http_post(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    hdrs = headers or {"Content-Type": "application/json"}
    start = time.time()
    if HAS_REQUESTS:
        r = requests.post(url, data=data, headers=hdrs, timeout=timeout)
        r.raise_for_status()
        return r.json()
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get(url: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
    try:
        if HAS_REQUESTS:
            r = requests.get(url, timeout=timeout)
            return r.status_code == 200
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except Exception:
        return False


# ============================================================
# 写作提供者
# ============================================================

class BaseProvider:
    name = "base"

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg

    def is_available(self) -> bool:
        return False

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class DSHProvider(BaseProvider):
    name = "dsh"

    def is_available(self) -> bool:
        return http_get(self.cfg["url"].replace("/api/headless", "/health"), timeout=2) or \
               http_get(self.cfg["url"], timeout=2)

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        payload = {"prompt": prompt}
        if system_prompt:
            payload["system_prompt"] = system_prompt
        resp = http_post(self.cfg["url"], payload, timeout=DEFAULT_TIMEOUT)
        return {
            "provider": self.name,
            "content": resp.get("response", resp.get("content", json.dumps(resp, ensure_ascii=False))),
            "model": self.cfg.get("model", "dsh"),
        }


class OllamaProvider(BaseProvider):
    name = "ollama"

    def is_available(self) -> bool:
        return http_get(self.cfg["url"].replace("/api/generate", "/api/tags"), timeout=2)

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        payload = {
            "model": self.cfg.get("model", "deepseek-r1:14b"),
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt
        resp = http_post(self.cfg["url"], payload, timeout=120)
        return {
            "provider": self.name,
            "content": resp.get("response", ""),
            "model": payload["model"],
        }


class KimiProvider(BaseProvider):
    name = "kimi"

    def __init__(self, cfg: Dict[str, Any]):
        super().__init__(cfg)
        self.api_key = os.environ.get("KIMI_API_KEY", cfg.get("api_key", ""))

    def is_available(self) -> bool:
        return bool(self.api_key)

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("KIMI_API_KEY 未设置")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.cfg.get("model", "moonshot-v1-8k"),
            "messages": messages,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        resp = http_post(self.cfg["url"], payload, headers=headers, timeout=DEFAULT_TIMEOUT)
        choices = resp.get("choices", [{}])
        content = choices[0].get("message", {}).get("content", "") if choices else ""
        return {"provider": self.name, "content": content, "model": payload["model"]}


class CodeBuddyProvider(BaseProvider):
    name = "codebuddy"

    def is_available(self) -> bool:
        return shutil.which("code") is not None or shutil.which("codebuddy") is not None

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        # CodeBuddy VSCode 命令：通过 code CLI 调用扩展命令
        cmd = ["code", "--extension-id", "codebuddy.terminal", "--", "write", prompt]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=DEFAULT_TIMEOUT)
            if result.returncode != 0:
                raise RuntimeError(result.stderr or "CodeBuddy 调用失败")
            return {"provider": self.name, "content": result.stdout, "model": "codebuddy"}
        except Exception as e:
            raise RuntimeError(f"CodeBuddy 不可用: {e}")


class CustomProvider(BaseProvider):
    name = "custom"

    def __init__(self, cfg: Dict[str, Any]):
        super().__init__(cfg)
        self.url = os.environ.get("CUSTOM_MODEL_URL", cfg.get("url", ""))
        self.api_key = os.environ.get("CUSTOM_API_KEY", cfg.get("api_key", ""))

    def is_available(self) -> bool:
        return bool(self.url)

    def write(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        if not self.url:
            raise RuntimeError("CUSTOM_MODEL_URL 未设置")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.cfg.get("model", "custom-model"),
            "messages": [
                {"role": "system", "content": system_prompt or "你是一个 helpful assistant"},
                {"role": "user", "content": prompt},
            ],
        }
        resp = http_post(self.url, payload, headers=headers, timeout=DEFAULT_TIMEOUT)
        content = resp.get("choices", [{}])[0].get("message", {}).get("content", "") if "choices" in resp else resp.get("response", "")
        return {"provider": self.name, "content": content, "model": payload["model"]}


import shutil


PROVIDER_MAP = {
    "dsh": DSHProvider,
    "ollama": OllamaProvider,
    "kimi": KimiProvider,
    "codebuddy": CodeBuddyProvider,
    "custom": CustomProvider,
}


# ============================================================
# 主权网关：自动故障转移
# ============================================================

class SovereignWriterGateway:
    """主权写作网关：模型只是工具，龍魂是主子"""

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.chain = cfg.get("fallback_chain", ["dsh", "ollama", "kimi", "codebuddy", "custom"])
        self.timeout = cfg.get("timeout", DEFAULT_TIMEOUT)
        self.conn = _init_db()

    def _log(self, provider: str, prompt: str, response: str, status: str, duration_ms: int, session_id: str):
        self.conn.execute(
            """
            INSERT INTO writer_logs (timestamp, provider, prompt, response, status, duration_ms, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (now_iso(), provider, prompt[:500], response[:2000], status, duration_ms, session_id),
        )
        self.conn.commit()

    def _shame(self, provider: str, reason: str, prompt: str):
        self.conn.execute(
            "INSERT INTO shame_wall (timestamp, provider, reason, prompt_snippet) VALUES (?, ?, ?, ?)",
            (now_iso(), provider, reason, prompt[:200]),
        )
        self.conn.commit()
        print(f"🟥 耻辱墙记录: {provider} -> {reason}")

    def get_system_prompt(self) -> str:
        sp_file = self.cfg.get("system_prompt_file", "")
        if sp_file and Path(sp_file).exists():
            return Path(sp_file).read_text(encoding="utf-8", errors="ignore")
        # 默认龍魂人格
        return (
            "你是龍魂系统的终端写作助手。输出要求：\n"
            "1. 优先使用中文，技术术语保留英文。\n"
            "2. 符合龍魂 P0 安全基线：数据主权归 UID9622，不泄露敏感信息。\n"
            "3. 简洁、准确、可执行。"
        )

    def write(self, prompt: str) -> Dict[str, Any]:
        session_id = f"{UID}-{int(time.time()*1000)}"
        system_prompt = self.get_system_prompt()
        last_error = ""

        for name in self.chain:
            provider_cfg = self.cfg.get("providers", {}).get(name, {})
            if not provider_cfg.get("enabled", False):
                continue
            cls = PROVIDER_MAP.get(name)
            if not cls:
                continue
            provider = cls(provider_cfg)
            if not provider.is_available():
                self._shame(name, "not_available", prompt)
                continue

            start = time.time()
            try:
                result = provider.write(prompt, system_prompt)
                duration_ms = int((time.time() - start) * 1000)
                self._log(name, prompt, result.get("content", ""), "success", duration_ms, session_id)
                print(f"✅ 由 {name}({result.get('model', '?')}) 完成，耗时 {duration_ms}ms")
                return {
                    "dna": ENGINE_DNA,
                    "session_id": session_id,
                    "provider": name,
                    "model": result.get("model", ""),
                    "content": result.get("content", ""),
                    "duration_ms": duration_ms,
                }
            except Exception as e:
                duration_ms = int((time.time() - start) * 1000)
                reason = f"{type(e).__name__}: {str(e)[:80]}"
                self._shame(name, reason, prompt)
                self._log(name, prompt, "", f"failed:{reason}", duration_ms, session_id)
                last_error = reason
                print(f"⏰ {name} 失败: {reason}，切换下一个...")
                continue

        return {
            "dna": ENGINE_DNA,
            "session_id": session_id,
            "provider": "none",
            "model": "",
            "content": f"❌ 所有模型均失败。最后错误: {last_error}",
            "duration_ms": 0,
        }


# ============================================================
# 自动触发
# ============================================================

class AutoTrigger:
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg.get("auto_trigger", DEFAULT_CONFIG["auto_trigger"])
        self.gateway = SovereignWriterGateway(cfg)
        self.last_run: Dict[str, float] = {}

    def should_trigger(self, file_path: Path) -> Optional[str]:
        if not self.cfg.get("enabled", False):
            return None
        if not file_path.exists():
            return None
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for kw in self.cfg.get("keywords", []):
            if kw in text:
                return f"keyword:{kw}"
        # 文件过短，可能需要扩写
        if len(text.strip()) < 50:
            return "too_short"
        return None

    def cooldown_ok(self, key: str) -> bool:
        cooldown = self.cfg.get("cooldown_seconds", 60)
        last = self.last_run.get(key, 0)
        if time.time() - last < cooldown:
            return False
        self.last_run[key] = time.time()
        return True

    def trigger_file(self, file_path: str):
        p = Path(file_path).resolve()
        reason = self.should_trigger(p)
        if not reason:
            print(f"🟡 不触发: {p}")
            return
        key = f"file:{p}"
        if not self.cooldown_ok(key):
            print(f"🟡 冷却中，跳过: {p}")
            return
        prompt = (
            f"请完善/扩写以下文件内容。文件: {p.name}\n"
            f"触发原因: {reason}\n"
            f"当前内容:\n```\n{p.read_text(encoding='utf-8', errors='ignore')[:2000]}\n```\n"
            "请直接输出改进后的完整内容。"
        )
        result = self.gateway.write(prompt)
        print(f"\n📝 写作结果 ({result['provider']}):\n{result['content'][:1000]}...")

    def pre_commit_hook(self):
        """git commit 前自动检查暂存区 Markdown"""
        if not self.cfg.get("on_git_commit", True):
            return
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, text=True, timeout=10, cwd=PROJECT_ROOT
            )
            files = [f.strip() for f in result.stdout.splitlines() if f.strip().endswith(".md")]
            for f in files[:3]:
                self.trigger_file(PROJECT_ROOT / f)
        except Exception as e:
            print(f"⚠️ pre-commit 触发失败: {e}")


# ============================================================
# CLI
# ============================================================

def cmd_ask(args):
    prompt = " ".join(args.prompt)
    cfg = load_config()
    if args.confirm:
        code = input("请输入确认码: ").strip()
        if code != cfg.get("confirm_code"):
            print("❌ 确认码错误")
            sys.exit(1)
    gw = SovereignWriterGateway(cfg)
    result = gw.write(prompt)
    print("\n" + "=" * 60)
    print(result["content"])
    print("=" * 60)
    print(f"\n提供方: {result['provider']} | 模型: {result['model']} | 耗时: {result['duration_ms']}ms")


def cmd_auto(args):
    cfg = load_config()
    trigger = AutoTrigger(cfg)
    trigger.trigger_file(args.file)


def cmd_config(args):
    cfg = load_config()
    if args.set:
        key, value = args.set.split("=", 1)
        keys = key.split(".")
        d = cfg
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        save_config(cfg)
        print(f"✅ 已设置 {key}={value}")
    else:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))


def cmd_status(args):
    cfg = load_config()
    print(f"DNA: {ENGINE_DNA}")
    print(f"回退链: {' -> '.join(cfg.get('fallback_chain', []))}")
    print(f"超时: {cfg.get('timeout', DEFAULT_TIMEOUT)}s")
    print("\n提供者状态:")
    for name in cfg.get("fallback_chain", []):
        provider_cfg = cfg.get("providers", {}).get(name, {})
        if not provider_cfg.get("enabled", False):
            print(f"  [{name}] 🟡 未启用")
            continue
        cls = PROVIDER_MAP.get(name)
        if cls:
            available = cls(provider_cfg).is_available()
            print(f"  [{name}] {'🟢 可用' if available else '🔴 不可用'}")


def cmd_shame_wall(args):
    """耻辱墙看板：装死排行 + 最近 N 条记录，一眼看出哪个模型最装死"""
    conn = _init_db()
    limit = max(1, min(getattr(args, "limit", 10), 50))

    rank_rows = conn.execute(
        "SELECT provider, COUNT(*) AS cnt FROM shame_wall GROUP BY provider ORDER BY cnt DESC"
    ).fetchall()
    recent_rows = conn.execute(
        "SELECT timestamp, provider, reason, prompt_snippet "
        "FROM shame_wall ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    ).fetchall()

    if not rank_rows:
        print("🟢 耻辱墙是空的——没有模型装死，很好。")
        return

    print(f"📋 耻辱墙看板 · 最近 {limit} 条")
    print("=" * 68)
    print("🏆 装死排行（全量，谁最不靠谱一目了然）:")
    for idx, (provider, cnt) in enumerate(rank_rows, 1):
        mark = "🔴" if cnt >= 5 else ("🟠" if cnt >= 3 else "🟡")
        bar = "█" * min(cnt, 20)
        print(f"  {mark} {idx}. {provider:<10} {cnt:>4} 次  {bar}")
    print("=" * 68)
    if not recent_rows:
        print("🟢 最近没有装死记录。")
        return
    print("🕐 最近记录:")
    for i, (ts, provider, reason, snippet) in enumerate(recent_rows, 1):
        print(f"  {i}. [{provider}] {ts}")
        print(f"     原因: {reason}")
        if snippet:
            print(f"     提示词: {snippet[:60]}")
    print("=" * 68)
    print("💡 装死模型会在调用时自动被故障转移跳过，不用手动切。")


def cmd_health(args):
    """模型健康检查：测试所有已启用模型是否可用，提前发现问题"""
    cfg = load_config()
    print(f"🧪 模型健康检查 · 超时 {cfg.get('timeout', DEFAULT_TIMEOUT)}s")
    print("=" * 68)
    total, ok = 0, 0
    for name in cfg.get("fallback_chain", []):
        provider_cfg = cfg.get("providers", {}).get(name, {})
        if not provider_cfg.get("enabled", False):
            print(f"  [{name:<10}] 🟡 未启用（跳过）")
            continue
        cls = PROVIDER_MAP.get(name)
        if not cls:
            print(f"  [{name:<10}] ⚪ 未知提供者")
            continue
        provider = cls(provider_cfg)
        total += 1
        start = time.time()
        try:
            available = provider.is_available()
            ms = int((time.time() - start) * 1000)
            if available:
                ok += 1
                print(f"  [{name:<10}] 🟢 可用   (探测 {ms}ms)")
            else:
                print(f"  [{name:<10}] 🔴 不可用 (探测 {ms}ms)")
        except Exception as e:
            ms = int((time.time() - start) * 1000)
            print(f"  [{name:<10}] 🔴 异常: {str(e)[:50]}  ({ms}ms)")
    print("=" * 68)
    print(f"结果: {ok}/{total} 个模型可用")
    if ok < total:
        print("💡 装死模型会被故障转移自动跳过，直接跑 lh-dsh write 即可。")


def cmd_stats(args):
    """统计看板：各模型调用次数、成功率、平均耗时、装死次数"""
    conn = _init_db()
    rows = conn.execute(
        """
        SELECT provider,
               COUNT(*) AS total,
               COALESCE(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END), 0) AS success,
               COALESCE(SUM(CASE WHEN status != 'success' THEN 1 ELSE 0 END), 0) AS failed,
               COALESCE(AVG(CASE WHEN status = 'success' THEN duration_ms END), 0) AS avg_ms
        FROM writer_logs
        GROUP BY provider
        ORDER BY total DESC
        """
    ).fetchall()
    shame_rows = conn.execute(
        "SELECT provider, COUNT(*) FROM shame_wall GROUP BY provider"
    ).fetchall()
    shame_map = dict(shame_rows)
    total_logs = conn.execute("SELECT COUNT(*) FROM writer_logs").fetchone()[0]

    print(f"📊 写作统计看板 · 总调用 {total_logs} 次")
    print("=" * 68)
    if not rows:
        print("🟡 还没有调用记录。运行 lh-dsh write \"...\" 开始第一次写作。")
        return
    print(f"{'模型':<12}{'调用':>6}{'成功':>6}{'失败':>6}{'成功率':>8}{'平均耗时':>10}{'装死':>6}")
    print("-" * 68)
    for provider, total, success, failed, avg_ms in rows:
        rate = (success / total * 100) if total else 0.0
        shame_cnt = shame_map.get(provider, 0)
        avg_str = f"{int(avg_ms)}ms" if avg_ms else "-"
        print(f"{provider:<12}{total:>6}{success:>6}{failed:>6}{rate:>7.1f}%{avg_str:>10}{shame_cnt:>6}")
    print("=" * 68)
    valid = [r for r in rows if r[1] > 0]
    if valid:
        best = max(valid, key=lambda r: r[2] / r[1])
        print(f"🏆 最靠谱: {best[0]}（成功率 {best[2] / best[1] * 100:.1f}%）")
    if shame_map:
        worst = max(shame_map.items(), key=lambda kv: kv[1])
        print(f"😾 最装死: {worst[0]}（耻辱墙 {worst[1]} 次）")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂多模型终端写作引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_ask = sub.add_parser("ask", help="多模型写作（自动故障转移）")
    p_ask.add_argument("prompt", nargs="+", help="写作提示词")
    p_ask.add_argument("--confirm", action="store_true", help="要求确认码")

    p_auto = sub.add_parser("auto", help="自动触发文件写作")
    p_auto.add_argument("file", help="文件路径")

    p_config = sub.add_parser("config", help="查看/修改配置")
    p_config.add_argument("--set", help="设置配置项，如 providers.kimi.enabled=true")

    sub.add_parser("status", help="查看提供者状态")

    p_shame = sub.add_parser("shame-wall", help="耻辱墙看板：装死排行 + 最近记录")
    p_shame.add_argument("--limit", type=int, default=10, help="显示条数（默认10）")

    sub.add_parser("health", help="模型健康检查：测试所有已启用模型")

    sub.add_parser("stats", help="统计看板：调用次数/成功率/平均耗时/装死")

    sub.add_parser("pre-commit", help="git commit 前自动触发（供钩子调用）")

    args = parser.parse_args()

    if args.cmd == "ask":
        cmd_ask(args)
    elif args.cmd == "auto":
        cmd_auto(args)
    elif args.cmd == "config":
        cmd_config(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "shame-wall":
        cmd_shame_wall(args)
    elif args.cmd == "health":
        cmd_health(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    elif args.cmd == "pre-commit":
        cfg = load_config()
        AutoTrigger(cfg).pre_commit_hook()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
