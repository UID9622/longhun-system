#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 人格矩阵
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-PERSONA-MATRIX-v1.0

读取现有人格注册表，实现任务路由、人格组合、左右互搏。
"""
import json
from pathlib import Path
from datetime import datetime

from config import Config


PERSONA_REGISTRY = Path.home() / "longhun-system" / "persona" / "persona_registry.json"


class PersonaMatrix:
    """人格矩阵：加载、路由、组合、执行。"""

    def __init__(self, registry_path=None):
        self.registry_path = Path(registry_path) if registry_path else PERSONA_REGISTRY
        self.registry = self._load_registry()
        self.dna = "#龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-PERSONA-MATRIX-v1.0"

    def _load_registry(self):
        if not self.registry_path.exists():
            return {"personas": {}}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_personas(self):
        """列出所有人格。"""
        result = []
        for code, info in self.registry.get("personas", {}).items():
            result.append({
                "code": code,
                "name": info.get("name"),
                "name_en": info.get("name_en"),
                "role": info.get("role"),
                "triggers": info.get("triggers", []),
                "weight": info.get("weight"),
                "status": info.get("status"),
            })
        return result

    def find_persona(self, query):
        """根据名称/别名/编码查找人格。"""
        query = query.lower()
        personas = self.registry.get("personas", {})
        for code, info in personas.items():
            candidates = [
                code.lower(),
                info.get("name", "").lower(),
                info.get("name_en", "").lower(),
                info.get("alias", "").lower(),
            ]
            if any(query in c for c in candidates):
                return {**info, "code": code}
        return None

    def route(self, task):
        """根据任务关键词匹配最适合的人格组合。"""
        task_lower = task.lower()
        scored = []
        for code, info in self.registry.get("personas", {}).items():
            score = 0
            triggers = info.get("triggers", [])
            for trig in triggers:
                if trig.lower() in task_lower:
                    score += 1
            if score > 0:
                scored.append((score, code, info))
        scored.sort(reverse=True)
        return [{"code": c, "name": i.get("name"), "role": i.get("role"), "score": s}
                for s, c, i in scored[:5]]

    def build_team(self, names):
        """根据人格名组合团队。"""
        team = []
        for name in names:
            p = self.find_persona(name)
            if p:
                team.append(p)
        return team

    def get_system_prompt(self, persona):
        """根据人格生成 system prompt。"""
        name = persona.get("name", "龍魂人格")
        role = persona.get("role", "助手")
        motto = persona.get("motto", "")
        return (
            f"你是龍魂人格「{name}」，角色定位：{role}。\n"
            f"座右铭：{motto}\n"
            f"请始终以该人格的视角、语气和专业能力回答问题。"
        )
