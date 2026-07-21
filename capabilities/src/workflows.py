#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 人格工作流
DNA:#龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-WORKFLOWS-FILE3-v1.0

定义人格组合工作流：不同人格按阶段协作完成任务。
"""
import json
from pathlib import Path
from datetime import datetime

from config import Config
from persona_matrix import PersonaMatrix


class WorkflowEngine:
    """人格工作流引擎。"""

    def __init__(self):
        self.matrix = PersonaMatrix()
        self.dna = "#龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-WORKFLOWS-v1.0"

    def tech_doc(self, topic, model_caller=None):
        """
        工作流：宝宝 + 诸葛 + 鲁班 自动生成技术文档。

        阶段 1：诸葛构思文档大纲（战略/规划）
        阶段 2：宝宝审计大纲（安全/底线/主权）
        阶段 3：鲁班实现正文（工程/代码/实现）
        阶段 4：诸葛最终定稿（战略统合）
        """
        team = self.matrix.build_team(["诸葛", "宝宝", "鲁班"])
        if len(team) < 3:
            return {"status": "failed", "error": f"人格团队组建失败: {team}"}

        zhuge = next(p for p in team if "诸葛" in p.get("name", ""))
        baobao = next(p for p in team if "宝宝" in p.get("name", ""))
        luban = next(p for p in team if "鲁班" in p.get("name", ""))

        result = {
            "workflow": "tech-doc",
            "topic": topic,
            "team": [{"code": p.get("code"), "name": p.get("name"), "role": p.get("role")} for p in team],
            "stages": [],
            "dna": self.dna,
        }

        # Stage 1: 诸葛出大纲
        outline_prompt = (
            f"请为技术主题「{topic}」撰写一份详细的中文技术文档大纲。\n"
            "要求：\n"
            "1. 包含背景、目标、核心概念、架构设计、实现步骤、验证方法；\n"
            "2. 每个章节给出 2-3 个要点；\n"
            "3. 输出纯文本大纲，不要冗余修饰。"
        )
        outline = self._call_persona(zhuge, outline_prompt, model_caller)
        result["stages"].append({
            "stage": 1,
            "persona": zhuge.get("name"),
            "action": "构思大纲",
            "output": outline,
        })

        # Stage 2: 宝宝审计大纲
        audit_prompt = (
            f"你是安全审计人格。以下是一份关于「{topic}」的技术文档大纲，\n"
            "请从数据主权、安全底线、合规性、对外泄露风险四个维度进行审计，\n"
            "指出需要补充或修改的地方，并给出修改建议。\n\n"
            f"大纲：\n{outline}"
        )
        audit = self._call_persona(baobao, audit_prompt, model_caller)
        result["stages"].append({
            "stage": 2,
            "persona": baobao.get("name"),
            "action": "审计大纲",
            "output": audit,
        })

        # Stage 3: 鲁班写正文
        write_prompt = (
            f"请基于以下大纲和审计意见，撰写「{topic}」的完整技术文档正文。\n"
            "要求：\n"
            "1. 使用中文，技术准确；\n"
            "2. 包含必要的代码示例、配置片段或命令；\n"
            "3. 结构清晰，段落分明；\n"
            "4. 不要重复审计意见，只输出文档正文。\n\n"
            f"大纲：\n{outline}\n\n"
            f"审计意见：\n{audit}"
        )
        body = self._call_persona(luban, write_prompt, model_caller)
        result["stages"].append({
            "stage": 3,
            "persona": luban.get("name"),
            "action": "撰写正文",
            "output": body,
        })

        # Stage 4: 诸葛定稿
        final_prompt = (
            f"请对以下关于「{topic}」的技术文档进行最终统合与定稿。\n"
            "要求：\n"
            "1. 检查结构完整性和逻辑一致性；\n"
            "2. 添加一段 200 字以内的执行摘要；\n"
            "3. 输出最终文档（包含执行摘要 + 正文）。\n\n"
            f"待统合正文：\n{body}"
        )
        final_doc = self._call_persona(zhuge, final_prompt, model_caller)
        result["stages"].append({
            "stage": 4,
            "persona": zhuge.get("name"),
            "action": "最终定稿",
            "output": final_doc,
        })

        # 保存最终文档
        output_dir = Config.project_root / "output" / "persona_docs"
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_topic = "".join(c if c.isalnum() or c in "_-" else "_" for c in topic)[:50]
        filename = f"tech_doc_{safe_topic}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        output_path = output_dir / filename
        output_path.write_text(
            f"# {topic}\n\n"
            f"**生成时间**: {datetime.now().isoformat()}\n"
            f"**工作流**: 宝宝 + 诸葛 + 鲁班\n"
            f"**DNA**: {self.dna}\n\n"
            f"{final_doc}\n",
            encoding="utf-8"
        )
        result["output_path"] = str(output_path)
        result["status"] = "success"
        return result

    def _call_persona(self, persona, prompt, model_caller=None):
        """调用本地模型，带上人格 system prompt。"""
        if model_caller is None:
            return self._fallback_generate(persona, prompt)

        system_prompt = self.matrix.get_system_prompt(persona)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        try:
            response = model_caller(messages)
            return response
        except Exception as e:
            return f"[调用失败: {e}]"

    def _fallback_generate(self, persona, prompt):
        """Fallback：本地没有可用模型时返回模拟输出。"""
        return (
            f"【{persona.get('name')} 模拟输出】\n"
            f"我已以 {persona.get('role')} 的角色处理该任务。\n"
            f"由于本地模型未启动，这里返回结构化占位内容。\n"
            f"任务摘要：{prompt[:80]}..."
        )
