#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统 · Skill 管理核心
Longhun System · Skill Management Core

DNA:#龍芯⚡️2026-06-07-SKILLS-MANAGER-v1.0
责任: UID9622·不免责
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class SkillRegistry:
    """Skill 注册和管理系统"""

    def __init__(self):
        self.skills: Dict[str, Dict] = {}
        self.base_dir = Path(__file__).parent
        self.html_skills_dir = self.base_dir / "html-skills"
        self.py_skills_dir = self.base_dir / "py-skills"
        self.load_all_skills()

    def load_all_skills(self) -> None:
        """加载所有可用 Skills"""
        self._load_html_skills()
        self._load_py_skills()

    def _load_html_skills(self) -> None:
        """加载 HTML Skills"""
        if self.html_skills_dir.exists():
            for html_file in self.html_skills_dir.glob("skill-*.html"):
                skill_name = html_file.stem
                self.skills[skill_name] = {
                    "name": skill_name,
                    "type": "html",
                    "path": str(html_file),
                    "filename": html_file.name,
                    "loaded_at": datetime.now().isoformat()
                }

    def _load_py_skills(self) -> None:
        """加载 Python Skills"""
        if self.py_skills_dir.exists():
            for py_file in self.py_skills_dir.glob("skill-*.py"):
                skill_name = py_file.stem
                self.skills[skill_name] = {
                    "name": skill_name,
                    "type": "python",
                    "path": str(py_file),
                    "filename": py_file.name,
                    "loaded_at": datetime.now().isoformat()
                }

    def get_skill(self, skill_id: str) -> Optional[Dict]:
        """获取指定 Skill"""
        return self.skills.get(skill_id)

    def list_skills(self) -> Dict[str, List[Dict]]:
        """列表所有 Skills"""
        html_skills = [s for s in self.skills.values() if s["type"] == "html"]
        py_skills = [s for s in self.skills.values() if s["type"] == "python"]
        return {
            "html": html_skills,
            "python": py_skills,
            "total": len(self.skills)
        }

    def get_skill_content(self, skill_id: str) -> Optional[str]:
        """读取 Skill 内容"""
        skill = self.get_skill(skill_id)
        if not skill:
            return None

        try:
            with open(skill["path"], "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading skill: {str(e)}"

    def export_config(self) -> Dict:
        """汇出 Skill 配置"""
        return {
            "dna": "#龍芯⚡️2026-06-07-SKILLS-MANAGER-v1.0",
            "timestamp": datetime.now().isoformat(),
            "skills": self.list_skills(),
            "metadata": {
                "author": "Longhun System",
                "status": "🟢 active",
                "total_skills": len(self.skills)
            }
        }


# 全域 Skill 注册表
_global_registry = None

def get_registry() -> SkillRegistry:
    """取得全域 Skill 注册表"""
    global _global_registry
    if _global_registry is None:
        _global_registry = SkillRegistry()
    return _global_registry

def list_skills() -> Dict:
    """列出所有可用 Skills"""
    return get_registry().list_skills()

def get_skill_content(skill_id: str) -> Optional[str]:
    """取得 Skill 内容"""
    return get_registry().get_skill_content(skill_id)
