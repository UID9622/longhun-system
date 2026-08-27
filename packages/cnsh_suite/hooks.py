# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 钩子 · 三色审计审批门
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-HOOKS-UID9622
"""

import json
from typing import Dict, Any
from .core import Hook, CNSHError, CNSHErrorCode, generate_dna, write_shame_wall

class TricolorGate(Hook):
    name = "tricolor_gate"
    description = "三色审计审批门 - 拦截不合格内容"
    priority = 100

    def __init__(self):
        self._engine = None

    def set_engine(self, engine):
        self._engine = engine

    def run(self, context: Dict) -> Dict:
        """执行审批"""
        tool_call = context.get("tool_call", {})
        session = context.get("session", {})

        # 豁免DNA工具和审计工具（避免递归）
        tool_name = tool_call.get("name", "")
        if tool_name in ["dna_generator", "tricolor_auditor"]:
            return {"kind": "allow"}

        # 对CNSH执行器进行审计
        if tool_name == "cnsh_executor":
            script = tool_call.get("arguments", {}).get("script", "")
            if not script:
                script = tool_call.get("arguments", {}).get("file", "")

            if self._engine:
                try:
                    result = self._engine.execute_tool("tricolor_auditor", content=script, context="cnsh_script")
                    if not result.get("passed", True):
                        dna = generate_dna("GATE-REJECT")
                        write_shame_wall(
                            f"CNSH脚本审计拒绝: {result.get('reason', '不合规')}",
                            dna,
                            {"score": result.get("score"), "tool": tool_name}
                        )
                        return {
                            "kind": "deny",
                            "reason": f"🔴 三色审计拒绝: {result.get('reason', '内容不合规')}"
                        }
                    if result.get("tricolor") == "🟡":
                        return {
                            "kind": "warn",
                            "reason": f"🟡 三色审计警告: {result.get('reason', '风险')}"
                        }
                except Exception:
                    return {"kind": "allow"}  # 审计失败时放行

        return {"kind": "allow"}
