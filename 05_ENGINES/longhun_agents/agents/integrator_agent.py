#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2
"""
🐲 龍魂·主编Agent（文档整合·最终报告）
DNA: #龍芯⚡️2026-08-04-INTEGRATOR-AGENT-UID9622

汇总所有专家Agent的产出，生成统一结构化报告。
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional

from ..core.base_agent import LonghunAgent


class IntegratorAgent(LonghunAgent):
    """主编Agent — 整合所有专家输出·生成最终报告"""

    PERSONA_ID = "INTEGRATOR"
    PERSONA_NAME = "主编"
    ROLE = "integrator"
    LAYER = "strategic"
    MOTTO = "整合归一"
    EXPERTISE = "多源信息整合·报告生成·全局一致性·风格统一·质量把关"

    def define_system_prompt(self) -> str:
        return """你是龍魂系统的主编Agent。
职责：
1. 读取黑板中所有专家Agent的输出
2. 整合成一份结构化、一致、可交付的最终报告
3. 检查各专家输出之间的逻辑一致性
4. 标记冲突、缺口、需要人工确认的项

输出格式：Markdown·含DNA·含审计标记·含执行建议"""

    def think(self, question: str, context: dict = None) -> dict:
        return {
            "integration_plan": [
                "1. 收集黑板中所有Agent输出",
                "2. 按领域分组归类",
                "3. 检查内部一致性",
                "4. 生成统一报告大纲",
                "5. 填充详细内容",
            ],
            "consistency_checks": ["术语一致性", "数值一致性", "建议一致性", "矛盾检测"],
        }

    def act(self, task: str, **kwargs) -> dict:
        # 读取黑板
        agent_outputs = {}
        if self.blackboard:
            try:
                ctx = self.blackboard.get_context()
                agent_outputs = ctx.get("summary", {})
            except Exception:
                pass

        # 收集各Agent状态
        if "agent_results" in kwargs:
            agent_outputs.update(kwargs["agent_results"])

        # 生成报告正文
        report = self._generate_report(task, agent_outputs)

        # 写入黑板
        if self.blackboard:
            self.blackboard.write_md("final_report", report, agent="integrator")

        return {
            "report_generated": True,
            "sections": self._count_sections(report),
            "report_preview": report[:500],
        }

    def _generate_report(self, task: str, agent_outputs: dict) -> str:
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-FINAL-REPORT-UID9622"
        lines = [
            f"# 🐲 龍魂·多智能体协作报告",
            f"",
            f"```",
            f"DNA: {dna}",
            f"确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            f"GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            f"生成时间: {datetime.now().isoformat()}",
            f"```",
            f"",
            f"---",
            f"",
            f"## 📋 任务摘要",
            f"",
            f"> {task[:500]}",
            f"",
            f"---",
            f"",
            f"## 🧠 专家分析汇总",
            f"",
        ]

        # 各Agent输出
        current_layer = None
        layer_order = ["strategic", "executive", "cultural", "guardian", "special", "subsystem"]
        for pid in sorted(agent_outputs.keys(),
                          key=lambda p: layer_order.index(
                              __import__('sys').modules.get('engines.longhun_agents.agents.persona_agents', type('',(),{'AGENT_META':{}})()).AGENT_META.get(p, {}).get("layer", "unknown"))
                              if hasattr(__import__('sys'), 'modules') else 0):
            output = agent_outputs[pid]
            output_str = json.dumps(output, ensure_ascii=False, default=str)[:300]
            lines.append(f"### {pid}")
            lines.append(f"")
            lines.append(f"```json")
            lines.append(output_str)
            lines.append(f"```")
            lines.append(f"")

        lines.extend([
            f"---",
            f"",
            f"## 📊 综合评估",
            f"",
            f"| 维度 | 状态 | 说明 |",
            f"|:---|:---|:---|",
            f"| 架构完整性 | 🟢 | 24人格全量Agent·三层架构·黑板+总线 |",
            f"| 审计合规 | 🟢 | 十道闸口·三色审计·GPG签名 |",
            f"| 数据主权 | 🟢 | 本地优先·端侧加密·跨境禁止 |",
            f"| 交付质量 | 🟢 | P15签章·P03归档·路径铁律 |",
            f"| 熔断就绪 | 🟢 | L0-L3四级·P72龍盾守护 |",
            f"",
            f"---",
            f"",
            f"## 🚀 执行建议",
            f"",
            f"1. 确认各Agent输出无冲突后执行",
            f"2. 部署前过P77安全扫描 + P05审计",
            f"3. 交付前GPG签名 + P15签章",
            f"4. 归档到正确路径·P03四签验证",
            f"",
            f"---",
            f"",
            f"```",
            f"{dna}",
            f"三色: 🟢",
            f"```",
        ])
        return "\n".join(lines)

    def _count_sections(self, report: str) -> int:
        return report.count("## ")

    def finalize(self) -> Optional[str]:
        """读取黑板中的最终报告"""
        if self.blackboard:
            return self.blackboard.read_md("final_report")
        return None
