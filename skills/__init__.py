#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · Skill 注册管理核心
LongHun System · Skill Registry Core

DNA:#龍芯⚡️2026-06-16-SKILL-REGISTRY-FILE1-v2.0
责任: UID9622·不免责

提供统一接口：
- get_registry()   取得 SkillRegistry 单例
- list_skills()    列出所有已注册 Skills（分 html / python）
- get_skill_content(skill_id) 读取 Skill 原始内容
- execute_skill(skill_id, params) 执行 Python Skill（沙盒队列）
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any

__all__ = [
    "SkillRegistry",
    "get_registry",
    "list_skills",
    "get_skill_content",
    "execute_skill",
]


class SkillRegistry:
    """Skill 注册表：自动扫描 html-skills/ 与 py-skills/ 目录。"""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.resolve()
        self.skills: Dict[str, Dict[str, Any]] = {}
        self._scan_skills()

    def _scan_skills(self):
        """扫描 html-skills 与 py-skills 目录并建立注册表。"""
        # 目录对应的类型与名称前缀
        skill_dirs = [
            (self.base_dir / "html-skills", "html", "HTML 互动工具"),
            (self.base_dir / "py-skills", "python", "Python 工程工具"),
        ]

        for directory, skill_type, category in skill_dirs:
            if not directory.is_dir():
                continue

            for filepath in sorted(directory.iterdir()):
                if filepath.is_dir():
                    continue
                ext = filepath.suffix.lower()
                if ext not in (".html", ".py"):
                    continue

                skill_id = filepath.stem
                # 从档名提取编号与名称，例如 skill-1-algorithmic-art
                parts = skill_id.split("-", 2)
                number = parts[1] if len(parts) > 1 else ""
                name = parts[2] if len(parts) > 2 else skill_id

                self.skills[skill_id] = {
                    "id": skill_id,
                    "type": skill_type,
                    "category": category,
                    "number": number,
                    "name": name,
                    "filename": filepath.name,
                    "path": str(filepath.relative_to(self.base_dir)),
                    "size": filepath.stat().st_size,
                }

    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 取得 Skill 元数据。"""
        return self.skills.get(skill_id)

    def get_skill_content(self, skill_id: str) -> Optional[str]:
        """读取指定 Skill 的完整原始内容。"""
        skill = self.get_skill(skill_id)
        if not skill:
            return None
        filepath = self.base_dir / skill["path"]
        try:
            return filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

    def export_config(self) -> Dict[str, Any]:
        """汇出所有 Skills 配置。"""
        return {
            "total": len(self.skills),
            "skills": list(self.skills.values()),
            "dna": "#龍芯⚡️2026-06-16-SKILL-REGISTRY-v2.0",
        }


# 单例快取
_registry_instance: Optional[SkillRegistry] = None


def get_registry() -> SkillRegistry:
    """取得 SkillRegistry 单例。"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = SkillRegistry()
    return _registry_instance


def list_skills() -> Dict[str, Any]:
    """列出所有 Skills，按 html / python 分类。"""
    registry = get_registry()
    html = [s for s in registry.skills.values() if s["type"] == "html"]
    python = [s for s in registry.skills.values() if s["type"] == "python"]
    return {
        "html": html,
        "python": python,
        "total": len(registry.skills),
    }


def get_skill_content(skill_id: str) -> Optional[str]:
    """取得指定 Skill 的完整内容。"""
    return get_registry().get_skill_content(skill_id)


def execute_skill(skill_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    执行 Python Skill。目前采用子进程方式启动，避免影响主进程。
    未来可扩展为真正的沙盒执行环境。
    """
    registry = get_registry()
    skill = registry.get_skill(skill_id)
    if not skill:
        return {"status": "error", "message": f"Skill '{skill_id}' not found"}
    if skill["type"] != "python":
        return {"status": "error", "message": "Only Python skills can be executed"}

    filepath = registry.base_dir / skill["path"]
    env = os.environ.copy()
    if params:
        env["LONGHUN_SKILL_PARAMS"] = json.dumps(params, ensure_ascii=False)

    try:
        result = subprocess.run(
            ["python3", str(filepath)],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=str(registry.base_dir),
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "skill_id": skill_id,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "skill_id": skill_id, "message": "execution timeout"}
    except Exception as exc:
        return {"status": "error", "skill_id": skill_id, "message": str(exc)}
