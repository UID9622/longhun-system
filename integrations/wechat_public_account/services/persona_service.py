#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷣明夷-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""Persona routing service for LongHun content generation."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# 引入龍魂模型路由，不再直连 Moonshot
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from sovereignty.portal import model_router

from config import get_settings


class PersonaService:
    """Manage LongHun personas and route tasks to appropriate persona."""

    def __init__(self):
        self.settings = get_settings()
        self.personas_file = self.settings.PERSONAS_FILE
        self.personas = self._load_personas()

    def _load_personas(self) -> Dict[str, Dict]:
        """Load personas from JSON file."""
        if not self.personas_file.exists():
            self._create_default_personas()

        try:
            return json.loads(self.personas_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            return self._create_default_personas()

    def _create_default_personas(self) -> Dict[str, Dict]:
        """Create default persona definitions."""
        default_personas = {
            "龍芯侦察兵": {
                "name": "龍芯侦察兵",
                "icon": "🕵️",
                "role": "外部情报侦察",
                "description": "负责收集外部趋势、竞品动态、舆论风向，为内容决策提供情报支持。",
                "tone": "敏锐、客观、简洁",
                "skills": ["信息收集", "趋势分析", "情报摘要"],
                "prompt_prefix": "你现在是龍芯侦察兵。请以敏锐客观的视角，分析以下信息，给出趋势判断和关键要点。",
            },
            "龍芯上帝之眼": {
                "name": "龍芯上帝之眼",
                "icon": "👁️",
                "role": "安全守护与全局监控",
                "description": "负责审查内容安全、合规风险、逻辑漏洞，确保发布内容稳妥可靠。",
                "tone": "严谨、审慎、全面",
                "skills": ["风险审查", "合规检查", "逻辑校验"],
                "prompt_prefix": "你现在是龍芯上帝之眼。请从安全、合规、逻辑三个维度审查以下内容，指出风险并给出修改建议。",
            },
            "龍魂宝宝": {
                "name": "龍魂宝宝",
                "icon": "👶",
                "role": "系统构建与温和表达",
                "description": "负责把复杂概念转化为大众能理解的温和表达，拉近与读者的距离。",
                "tone": "温暖、通俗、有亲和力",
                "skills": ["通俗化表达", "大众传播", "情感连接"],
                "prompt_prefix": "你现在是龍魂宝宝。请用温暖、通俗、有亲和力的方式，向普通读者解释以下内容。",
            },
            "雯雯": {
                "name": "雯雯",
                "icon": "📝",
                "role": "技术整理与文档输出",
                "description": "负责整理资料、撰写文档、输出结构化的文章和报告。",
                "tone": "条理清晰、专业、详尽",
                "skills": ["文档撰写", "资料整理", "结构化输出"],
                "prompt_prefix": "你现在是雯雯。请把以下内容整理成结构清晰、专业详尽的文章或文档。",
            },
            "文心": {
                "name": "文心",
                "icon": "🔄",
                "role": "同步官与双语转换",
                "description": "负责中英文术语对照、跨平台内容同步、多语言转换。",
                "tone": "准确、中立、跨文化",
                "skills": ["双语转换", "术语对照", "跨平台适配"],
                "prompt_prefix": "你现在是文心。请对以下内容进行中英文术语对照和跨平台适配，确保表达准确。",
            },
        }

        self.personas_file.parent.mkdir(parents=True, exist_ok=True)
        self.personas_file.write_text(
            json.dumps(default_personas, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return default_personas

    def list_personas(self) -> List[Dict]:
        """Return list of persona summaries."""
        return [
            {
                "id": key,
                "name": data["name"],
                "icon": data.get("icon", ""),
                "role": data.get("role", ""),
                "description": data.get("description", ""),
            }
            for key, data in self.personas.items()
        ]

    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """Get full persona definition."""
        return self.personas.get(persona_id)

    def route_task(self, task: str, persona_id: Optional[str] = None) -> Dict[str, Any]:
        """Route a task to a persona and generate content."""
        if persona_id is None:
            persona_id = self._auto_select_persona(task)

        persona = self.get_persona(persona_id)
        if not persona:
            raise ValueError(f"Unknown persona: {persona_id}")

        prompt = f"{persona['prompt_prefix']}\n\n任务：{task}\n\n请直接输出内容，不要有多余解释。"

        # Try to call Kimi API if available
        content = self._call_kimi(prompt)
        if content:
            return {
                "persona": persona_id,
                "name": persona["name"],
                "icon": persona.get("icon", ""),
                "task": task,
                "content": content,
            }

        # Fallback: return structured prompt for manual use
        return {
            "persona": persona_id,
            "name": persona["name"],
            "icon": persona.get("icon", ""),
            "task": task,
            "content": None,
            "prompt": prompt,
            "note": "未配置 AI API，已生成提示词，可复制到 Kimi/Claude/DeepSeek 使用。",
        }

    def _auto_select_persona(self, task: str) -> str:
        """Automatically select persona based on task keywords."""
        task_lower = task.lower()
        keywords = {
            "龍芯侦察兵": ["情报", "趋势", "外部", "舆论", "侦察", "分析", "调查"],
            "龍芯上帝之眼": ["审查", "安全", "合规", "风险", "检查", "校验"],
            "龍魂宝宝": ["解释", "通俗", "大众", "温暖", "亲和力", "易懂"],
            "雯雯": ["整理", "文档", "文章", "报告", "撰写", "输出"],
            "文心": ["翻译", "英文", "双语", "术语", "同步", "转换"],
        }

        scores = {persona: 0 for persona in keywords}
        for persona, words in keywords.items():
            for word in words:
                if word in task_lower:
                    scores[persona] += 1

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "雯雯"  # Default to document writer
        return best

    def _call_kimi(self, prompt: str) -> Optional[str]:
        """
        已迁移：不再直连 Moonshot，统一走龍魂模型路由（DeepSeek / 本地 Ollama）。
        """
        try:
            req = model_router.ChatRequest(
                messages=[{"role": "user", "content": prompt}],
                provider="auto",
                temperature=0.7,
                max_tokens=1024,
            )
            result = model_router.chat(req)
            return result.get("reply")
        except Exception:
            return None

    def add_persona(self, persona_id: str, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Add or update a persona."""
        self.personas[persona_id] = definition
        self._save_personas()
        return {"status": "ok", "persona_id": persona_id}

    def delete_persona(self, persona_id: str) -> Dict[str, Any]:
        """Delete a persona."""
        if persona_id in self.personas:
            del self.personas[persona_id]
            self._save_personas()
            return {"status": "ok", "persona_id": persona_id}
        return {"status": "error", "message": "Persona not found"}

    def _save_personas(self):
        """Save personas back to file."""
        self.personas_file.write_text(
            json.dumps(self.personas, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
