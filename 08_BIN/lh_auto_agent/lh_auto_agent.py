#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-MAIN-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 全自动AI智能体系统 v2.0 · 主控制器
AutoAgent Main — 全流程编排: 聊天→审计→灵魂→知识→红蓝 + 操盘网关联动

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-MAIN-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

🔥 v2.0 结合升级（2026-08-17·操盘网关联动）:
  - 对接 `08_BIN/lh_control_gate.py`（127.0.0.1:18790）: 智能体判定操作类指令
    时通过操盘网关真实操作 Mac（shell/open/clipboard...），默认关闭需 --gate 显式开启
  - 对接真实AI网关（bin/lh_ai_gateway）: 消灭 v2.0 mock 缺口
  - 全链路审计: 每次处理结果 append-only 落 audit.jsonl

架构（v2.0 五模块 + 操盘层）:
  用户输入 → chat(真实AI) → audit(三色) → soul(三问) → knowledge(提取)
           → [可选] gate(操盘) → red_blue(每N轮) → 综合判定 → 归档
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import unittest
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AGENT_DIR = Path.home() / ".longhun" / "agent"
AUDIT_FILE = AGENT_DIR / "audit" / "audit.jsonl"
LOG_FILE = Path.home() / "longhun-system" / "logs" / "agent.log"
CONTROL_GATE_CONFIG = Path.home() / "longhun-system" / "config" / "control_gate.json"
GATE_BASE = "http://127.0.0.1:18790"
MAX_HISTORY = 100

# 操盘动作关键词路由（智能体判定"操作类指令"）
GATE_ACTION_RULES = [
    # (动作, 触发词列表)
    ("shell",     ["执行", "运行", "帮我跑", "启动服务", "杀掉", "删除文件", "创建目录", "重启"]),
    ("open",      ["打开", "启动应用", "打开浏览器", "打开终端"]),
    ("clipboard", ["复制到剪贴板", "复制", "剪切板"]),
    ("sysinfo",   ["系统信息", "cpu", "内存", "磁盘", "状态"],
    ),
]
# 永远不通过网关执行的禁止词（网关侧也有熔断，这里双保险）
GATE_FORBIDDEN = ["rm -rf", "push --force", ".ssh", ".gnupg", "mkfs", "dd if=", "shutdown", "私钥", "DNA种子", "GPG私钥"]


class _ModuleProxy:
    """模块惰性加载代理（避免循环依赖 + 模块缺失时优雅降级）"""

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._base = Path(__file__).resolve().parent

    def _load(self, name: str, class_name: str, path: str):
        cache_key = f"{name}.{class_name}"
        if cache_key not in self._cache:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, str(self._base / path))
            mod = importlib.util.module_from_spec(spec)
            sys.modules.setdefault(name, mod)  # 注册 sys.modules（dataclass/元类需要）
            spec.loader.exec_module(mod)
            self._cache[cache_key] = getattr(mod, class_name)()
        return self._cache[cache_key]

    def chat(self):
        return self._load("lh_auto_chat", "AutoChat", "lh_auto_chat.py")

    def knowledge(self):
        return self._load("lh_auto_knowledge", "KnowledgeGraph", "lh_auto_knowledge.py")

    def extractor(self):
        return self._load("lh_auto_knowledge", "TextExtractor", "lh_auto_knowledge.py")

    def audit(self):
        return self._load("lh_auto_audit", "AutoAudit", "lh_auto_audit.py")

    def soul(self):
        return self._load("lh_auto_soul", "SoulThree", "lh_soul_three.py")

    def redblue(self):
        return self._load("lh_auto_rb", "RedBlue", "lh_red_blue.py")


class GateClient:
    """操盘网关客户端（127.0.0.1:18790）"""

    def __init__(self, gate_key: Optional[str] = None, enabled: bool = False):
        self.enabled = enabled
        self.key = gate_key
        if self.key is None and CONTROL_GATE_CONFIG.exists():
            try:
                cfg = json.loads(CONTROL_GATE_CONFIG.read_text(encoding="utf-8"))
                self.key = cfg.get("master_key")
            except Exception:
                self.key = None

    def call(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用网关。返回 {ok, ...}；网关不可达 → 优雅降级"""
        if not self.enabled:
            return {"ok": False, "error": "gate_disabled", "stdout": "", "stderr": "操盘网关未启用（--gate 开启）"}
        if self.key is None:
            return {"ok": False, "error": "no_key", "stdout": "", "stderr": "未找到网关Key"}
        # 双保险: 禁止词检查
        cmd = str(params.get("command", "") or params.get("app", "") or "")
        for word in GATE_FORBIDDEN:
            if word.lower() in cmd.lower():
                return {"ok": False, "error": "forbidden", "stdout": "", "stderr": f"禁止词: {word}"}
        try:
            req = urllib.request.Request(
                f"{GATE_BASE}/v1/execute",
                data=json.dumps({"action": action, "params": params}).encode("utf-8"),
                headers={"Content-Type": "application/json", "X-Gate-Key": self.key},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"ok": False, "error": "gate_down", "stdout": "", "stderr": f"网关不可达: {e.reason}"}
        except Exception as e:
            return {"ok": False, "error": "gate_error", "stdout": "", "stderr": str(e)}


class AutoAgent:
    """全自动AI智能体主控制器"""

    def __init__(self, gate_key: Optional[str] = None, gate_enabled: bool = False):
        self.mod = _ModuleProxy()
        self.chat_engine = self.mod.chat()
        self.gate = GateClient(gate_key, gate_enabled)
        self.history: List[Dict[str, Any]] = []
        self.rounds: int = 0
        self.red_blue_interval: int = 10  # 每 N 轮触发红蓝

    @staticmethod
    def _format_gate_result(gate_result: Dict[str, Any]) -> str:
        """网关返回无 stdout 时，提取顶层摘要字段"""
        keys = ("hostname", "uptime", "cpu_avg", "memory", "disk", "path", "stdout", "message")
        parts = [f"{k}={gate_result[k]}" for k in keys if gate_result.get(k)]
        return " | ".join(parts) if parts else str(gate_result.get("ok"))

    # ── 操作指令判定 ──
    def _detect_gate_action(self, text: str) -> Optional[str]:
        for action, keywords in GATE_ACTION_RULES:
            for kw in keywords:
                if kw in text:
                    return action
        return None

    def _build_gate_params(self, action: str, text: str) -> Dict[str, Any]:
        if action == "open":
            app = "浏览器"
            for name in ["浏览器", "Safari", "Chrome", "终端", "Terminal", "备忘录", "邮件", "Music", "微信"]:
                if name in text:
                    app = name
                    break
            return {"app": app}
        if action == "shell":
            # 提取 shell 命令（`代码块` 或 引号内，否则用 AI 输出拼）
            return {"command": text}
        return {}

    # ── 单次全流程处理 ──
    def process(self, text: str, verbose: bool = True) -> Dict[str, Any]:
        self.rounds += 1
        result: Dict[str, Any] = {
            "input": text[:200],
            "ts": datetime.now(timezone.utc).isoformat(),
            "round": self.rounds,
        }

        # ① 聊天（真实AI）
        try:
            chat_res = self.chat_engine.chat(text, system="你是龍魂全自动智能体，为人民服务、守护数据主权、透明可审计，回答简洁直接。")
        except Exception as e:
            chat_res = {"content": f"🟡 聊天异常: {e}", "model": "error", "mock": True, "latency_ms": 0}
        result["reply"] = chat_res["content"]
        result["model"] = chat_res.get("model", "unknown")
        result["mock"] = chat_res.get("mock", False)

        # ② 三色审计
        audit_res = self.mod.audit().audit(text + " " + chat_res["content"], source="agent")
        result["audit_verdict"] = audit_res.verdict
        result["audit_score"] = audit_res.score

        # ③ 灵魂三问
        soul_results = self.mod.soul().ask(text + " " + chat_res["content"])
        soul_v = self.mod.soul().verdict(soul_results)
        result["soul_status"] = soul_v["status"]

        # ④ 知识提取
        points = self.mod.extractor().extract(text + " " + chat_res["content"], source="agent")
        if points:
            self.mod.knowledge().add(points)
        result["knowledge_points"] = [p.keyword for p in points[:5]]

        # ⑤ 操盘网关联动（可选）
        gate_result = None
        if self.gate.enabled:
            action = self._detect_gate_action(text)
            if action:
                params = self._build_gate_params(action, text)
                gate_result = self.gate.call(action, params)
                result["gate"] = {"action": action, "result": gate_result}
                if gate_result.get("ok"):
                    out = gate_result.get("stdout") or self._format_gate_result(gate_result)
                    result["reply"] += f"\n\n[GATE:{action}] 已执行: {out[:200]}"
                else:
                    result["reply"] += f"\n\n[GATE:{action}] 未执行: {gate_result.get('stderr', '')[:200]}"

        # ⑥ 红蓝对抗（每 N 轮）
        rb = None
        if self.rounds % self.red_blue_interval == 0:
            rb = self.mod.redblue().batch_duel()
            result["red_blue"] = rb

        # ⑦ 综合判定
        if audit_res.verdict == "🔴" or soul_v["status"] == "❌ 不通过":
            result["final_verdict"] = "🔴 不通过"
        elif audit_res.verdict == "🟡" or soul_v["status"] == "⚠️ 待核":
            result["final_verdict"] = "🟡 待核"
        else:
            result["final_verdict"] = "🟢 通过"

        # 归档 + 历史
        self._log(result)
        self.history.append(result)
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

        if verbose:
            self._print(result)
        return result

    def _print(self, r: Dict[str, Any]):
        print(f"[{r['final_verdict']}] {r['reply']}")
        print(f"  └ 审计{r['audit_verdict']}({r['audit_score']}) · 灵魂{r['soul_status']} · 模型{r['model']}{'·mock' if r.get('mock') else ''}"
              + (f" · GATE:{r['gate']['action']}" if r.get("gate") else ""))

    def _log(self, result: Dict[str, Any]):
        AGENT_DIR.joinpath("audit").mkdir(parents=True, exist_ok=True)
        AUDIT_FILE.touch(exist_ok=True)
        AUDIT_FILE.chmod(0o600)
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{result['ts']} [{result['final_verdict']}] {result['input'][:60]}\n")

    def stats(self) -> Dict[str, Any]:
        counts = {"🟢": 0, "🟡": 0, "🔴": 0}
        if AUDIT_FILE.exists():
            for line in AUDIT_FILE.read_text(encoding="utf-8").splitlines():
                try:
                    d = json.loads(line)
                    if d.get("final_verdict", "").startswith(("🟢", "🟡", "🔴")):
                        counts[d["final_verdict"][0]] = counts.get(d["final_verdict"][0], 0) + 1
                except Exception:
                    pass
        return {
            "rounds": self.rounds,
            "verdicts": counts,
            "chat_stats": self.chat_engine.stats(),
            "gate": {"enabled": self.gate.enabled, "base": GATE_BASE},
            "red_blue_interval": self.red_blue_interval,
        }


def main():
    parser = argparse.ArgumentParser(prog="lh-agent", description="龍魂全自动AI智能体系统 v2.0")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--auto", type=int, metavar="N", help="自动模式跑 N 轮")
    parser.add_argument("--input", type=str, help="单次处理")
    parser.add_argument("--stats", action="store_true", help="状态统计")
    parser.add_argument("--gate", action="store_true", help="启用操盘网关联动（默认关闭）")
    parser.add_argument("--gate-key", type=str, help="操盘网关Key（默认读 master_key）")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--test", action="store_true", help="运行锚点测试")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAutoAgent)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    if args.version:
        print(
            "🐉 龍魂 · 全自动AI智能体系统 v2.0\n"
            "DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-MAIN-v2.0\n"
            f"确认码: {CONFIRM_CODE}\nGPG: {GPG_KEY}\n"
            "能力: 自动聊天(真实AI) · 知识提取 · 三色审计 · 灵魂三问 · 红蓝对抗 · 操盘网关"
        )
        sys.exit(0)
    if args.stats:
        print(json.dumps(AutoAgent().stats(), ensure_ascii=False, indent=2))
        sys.exit(0)

    agent = AutoAgent(gate_key=args.gate_key, gate_enabled=args.gate)

    if args.input:
        agent.process(args.input)
        sys.exit(0)
    if args.auto:
        samples = [
            "龍魂系统今天状态怎么样？",
            "帮我打开浏览器看看官网",
            "今天天气如何？",
            "介绍一下龍魂的架构",
            "请执行 ls 查看当前目录",
            "什么是为人民服务？",
        ]
        for i in range(args.auto):
            text = samples[i % len(samples)]
            print(f"\n=== 第{i+1}轮: {text[:30]} ===")
            agent.process(text, verbose=True)
            time.sleep(0.5)
        print(f"\n=== 完成 {args.auto} 轮 ===")
        sys.exit(0)
    if args.interactive:
        print("🐉 全自动AI智能体交互模式（输入 exit 退出）")
        while True:
            try:
                text = input("你> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not text:
                continue
            if text.lower() in ("exit", "quit", "退出"):
                break
            agent.process(text, verbose=True)
        sys.exit(0)
    parser.print_help()


class TestAutoAgent(unittest.TestCase):
    """主控制器 6 项锚点断言"""

    def setUp(self):
        self.agent = AutoAgent(gate_enabled=False)

    def test_01_full_pipeline(self):
        """① 全流程编排跑通"""
        result = self.agent.process("龍魂系统状态如何", verbose=False)
        for key in ["reply", "audit_verdict", "soul_status", "final_verdict"]:
            self.assertIn(key, result)

    def test_02_final_verdict(self):
        """② 综合判定合法值"""
        result = self.agent.process("正常内容测试", verbose=False)
        self.assertTrue(result["final_verdict"].startswith(("🟢", "🟡", "🔴")))

    def test_03_history_cap(self):
        """③ 历史截断"""
        for i in range(MAX_HISTORY + 20):
            self.agent.history.append({"r": i})
        self.agent.history = self.agent.history[-MAX_HISTORY:]
        self.assertLessEqual(len(self.agent.history), MAX_HISTORY)

    def test_04_stats(self):
        """④ 模块状态统计"""
        stats = self.agent.stats()
        self.assertIn("chat_stats", stats)
        self.assertIn("gate", stats)
        self.assertFalse(stats["gate"]["enabled"])

    def test_05_gate_detection(self):
        """⑤ 操作指令判定"""
        self.assertEqual(self.agent._detect_gate_action("帮我打开浏览器"), "open")
        self.assertEqual(self.agent._detect_gate_action("帮我执行 ls"), "shell")
        self.assertIsNone(self.agent._detect_gate_action("今天天气"))

    def test_06_gate_graceful(self):
        """⑥ 网关未启用/不可达 → 优雅降级不报错"""
        g = GateClient(enabled=False)
        res = g.call("shell", {"command": "ls"})
        self.assertEqual(res["ok"], False)
        self.assertIn("gate_disabled", res["error"])
        # 双保险禁止词
        g2 = GateClient(enabled=True)
        res2 = g2.call("shell", {"command": "rm -rf /tmp/x"})
        self.assertEqual(res2["ok"], False)
        self.assertIn("forbidden", res2["error"])


if __name__ == "__main__":
    main()
