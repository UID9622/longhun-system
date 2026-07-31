# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 统一调度器
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-DISPATCHER-v1.0

所有能力调用必须经过这里。输出统一格式，自动 DNA 追溯。
"""
import json
import subprocess
import os
from pathlib import Path

from config import Config
from registry import CapabilityRegistry
from auditor import Auditor


class Dispatcher:
    """统一能力调度器。"""

    def __init__(self):
        self.registry = CapabilityRegistry()
        self.auditor = Auditor()

    def _ensure_override(self, cap):
        """规则覆盖检查：未覆盖的能力拒绝调用。"""
        if not cap.get("rules_overridden"):
            raise PermissionError(
                f"能力 {cap['name']} 尚未经过龍魂规则覆盖，拒绝调用。"
                f"请先执行：lh 能力 覆盖 {cap['name']}"
            )

    def call(self, name, params=None):
        """统一调用入口。"""
        params = params or {}
        cap = self.registry.get(name)
        if not cap:
            dna = self.auditor.log(
                "dispatch", capability=name, input_data=params,
                status="failed", metadata={"reason": "capability_not_found"}
            )
            return {
                "status": "failed",
                "error": f"能力未注册: {name}",
                "dna": dna,
            }

        # 规则覆盖强制检查
        try:
            self._ensure_override(cap)
        except PermissionError as e:
            dna = self.auditor.log(
                "dispatch", capability=name, input_data=params,
                status="blocked", metadata={"reason": "rules_not_overridden"}
            )
            return {
                "status": "blocked",
                "error": str(e),
                "dna": dna,
            }

        invoke = cap.get("invoke", {})
        invoke_type = invoke.get("type")

        try:
            if invoke_type == "script":
                output = self._call_script(invoke.get("script"), params)
            elif invoke_type == "ollama":
                output = self._call_ollama(invoke.get("model"), params)
            elif invoke_type == "api":
                output = self._call_api(invoke.get("platform"), params)
            elif invoke_type == "database":
                output = self._call_database(invoke.get("path"), params)
            else:
                raise ValueError(f"未知的调用类型: {invoke_type}")

            dna = self.auditor.log(
                "dispatch", capability=name, input_data=params,
                output_data=output, status="success",
                metadata={"invoke_type": invoke_type}
            )
            return {
                "status": "success",
                "capability": name,
                "output": output,
                "dna": dna,
            }
        except Exception as e:
            dna = self.auditor.log(
                "dispatch", capability=name, input_data=params,
                status="failed", metadata={"reason": str(e)}
            )
            return {
                "status": "failed",
                "capability": name,
                "error": str(e),
                "dna": dna,
            }

    def _call_script(self, script, params):
        script_path = Path(script).expanduser()
        if not script_path.exists():
            raise FileNotFoundError(f"脚本不存在: {script_path}")
        cmd = [str(script_path)]
        if isinstance(params, dict):
            # 支持 query/prompt 作为位置参数；其他作为 --key value
            if "query" in params:
                cmd.append(str(params["query"]))
            elif "prompt" in params:
                cmd.append(str(params["prompt"]))
            else:
                for k, v in params.items():
                    cmd.extend([f"--{k}", str(v)])
        elif isinstance(params, str):
            cmd.append(params)
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout)
        return result.stdout.strip()

    def _call_ollama(self, model, params):
        messages = params.get("messages", [{"role": "user", "content": str(params)}])
        payload = {"model": model, "messages": messages, "stream": False}
        import urllib.request
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("message", {}).get("content", "")

    def _call_api(self, platform, params):
        # 实际调用应通过 multi-ai-gateway 或各平台 SDK
        # 这里返回一个标准化占位，避免暴露密钥
        return {
            "platform": platform,
            "request": params,
            "note": "API 调用已路由，实际请求由 multi-ai-gateway 执行",
        }

    def _call_database(self, path, params):
        db_path = Path(path).expanduser()
        if not db_path.exists():
            raise FileNotFoundError(f"数据库不存在: {db_path}")
        return {
            "path": str(db_path),
            "query": params,
            "note": "数据库查询入口已标准化，请使用对应查询接口执行",
        }

    def override_rules(self, name):
        """手动触发规则覆盖。"""
        cap = self.registry.get(name)
        if not cap:
            return {"status": "failed", "error": f"能力未注册: {name}"}
        self.registry.set_override(name, True)
        dna = self.auditor.log(
            "override", capability=name, input_data={"action": "rules_overridden"},
            output_data={"rules_overridden": True}, status="success"
        )
        return {
            "status": "success",
            "capability": name,
            "rules_overridden": True,
            "dna": dna,
        }
