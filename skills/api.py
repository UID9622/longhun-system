#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统 · Skill API 服务
Longhun System · Skill API Service

DNA:#龍芯⚡️2026-06-07-SKILL-API-FILE2-v1.0
责任: UID9622·不免责
"""

from fastapi import FastAPI, HTTPException
from . import get_registry, list_skills, get_skill_content

# 建立 FastAPI 应用
app = FastAPI(
    title="🐉 龍魂 Skill API",
    description="Skill 管理和执行 API",
    version="1.0.0"
)

@app.get("/api/v1/skills")
async def get_all_skills():
    """获取所有可用的 Skills"""
    return {
        "status": "success",
        "data": list_skills(),
        "dna": "#龍芯⚡️2026-06-07-SKILL-API-v1.0"
    }

@app.get("/api/v1/skills/{skill_id}")
async def get_skill_details(skill_id: str):
    """获取指定 Skill 的详细信息"""
    registry = get_registry()
    skill = registry.get_skill(skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")

    return {
        "status": "success",
        "data": skill,
        "dna": "#龍芯⚡️2026-06-07-SKILL-API-v1.0"
    }

@app.get("/api/v1/skills/{skill_id}/content")
async def get_skill_full_content(skill_id: str):
    """获取 Skill 的完整内容"""
    registry = get_registry()
    skill = registry.get_skill(skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")

    content = get_skill_content(skill_id)
    if not content:
        raise HTTPException(status_code=500, detail="Failed to read skill content")

    return {
        "status": "success",
        "skill_id": skill_id,
        "type": skill["type"],
        "content_length": len(content),
        "preview": content[:500] if len(content) > 500 else content,
        "dna": "#龍芯⚡️2026-06-07-SKILL-API-v1.0"
    }

@app.post("/api/v1/skills/{skill_id}/execute")
async def execute_skill(skill_id: str, params: dict = None):
    """执行 Python Skill"""
    registry = get_registry()
    skill = registry.get_skill(skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")

    if skill["type"] != "python":
        raise HTTPException(status_code=400, detail="Only Python skills can be executed")

    return {
        "status": "queued",
        "skill_id": skill_id,
        "message": f"Skill '{skill_id}' execution queued",
        "dna": "#龍芯⚡️2026-06-07-SKILL-API-v1.0"
    }

@app.get("/api/v1/skills/config/export")
async def export_skills_config():
    """汇出所有 Skills 配置"""
    registry = get_registry()
    return {
        "status": "success",
        "data": registry.export_config(),
        "dna": "#龍芯⚡️2026-06-07-SKILL-API-v1.0"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    registry = get_registry()
    skills_count = len(registry.skills)

    return {
        "status": "healthy",
        "service": "longhun-skills-api",
        "skills_loaded": skills_count,
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
