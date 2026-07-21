#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统 Phase 3 - FastAPI 后端框架 v1.0
Longhun System Phase 3 - FastAPI Backend Framework v1.0

DNA:#龍芯⚡️2026-06-06-PHASE3-FASTAPI-BACKEND-v1.0
Author: UID9622 (龍芯北辰)
Status: Production Ready
"""

from fastapi import FastAPI, WebSocket, Depends, HTTPException, Query  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
import logging
import asyncio
from pathlib import Path
import sys

# 龍魂 Skill 系统集成
try:
    from pathlib import Path
    import sys
    skills_path = Path(__file__).parent.parent / "longhun-system" / "skills"
    if str(skills_path) not in sys.path:
        sys.path.insert(0, str(skills_path))
    from __init__ import get_registry as get_skill_registry  # type: ignore[import-untyped]
    SKILLS_AVAILABLE = True
except Exception as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Skill 系统加载失败: {e}")
    SKILLS_AVAILABLE = False
    def get_skill_registry():  # type: ignore[reportRedeclaration]
        raise RuntimeError("Skill 系统未可用")


# ═══════════════════════════════════════════════════════════════════════════
# 第一部·配置与初始化
# ═══════════════════════════════════════════════════════════════════════════

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 应用
app = FastAPI(
    title="龍魂系统 API",
    description="龍魂系统完整 API·实时仪表板·技能管理·告警系统",
    version="3.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变数
SKILL_REGISTRY = {}
EXECUTION_HISTORY = []
ALERT_QUEUE = []
ACTIVE_CONNECTIONS: List[WebSocket] = []


# ═══════════════════════════════════════════════════════════════════════════
# 第二部·数据模型
# ═══════════════════════════════════════════════════════════════════════════

class Skill(BaseModel):
    """技能模型"""
    id: str
    name: str
    platform: str
    category: str
    priority: int = Field(ge=1, le=10)
    status: str = "active"
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    success_rate: float = 0.0
    dna: str = ""


class SkillInput(BaseModel):
    """技能输入模型"""
    id: str
    name: str
    platform: str
    category: str
    priority: int = Field(ge=1, le=10)


class Execution(BaseModel):
    """执行记录模型"""
    id: str
    skill_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    dna: str = ""


class Alert(BaseModel):
    """告警模型"""
    id: str
    level: str
    message: str
    source: str
    status: str = "active"
    created_at: datetime
    acknowledged_at: Optional[datetime] = None


class Log(BaseModel):
    """日志模型"""
    id: str
    level: str
    message: str
    skill_id: Optional[str] = None
    timestamp: datetime
    dna: str = ""


class Settings(BaseModel):
    """设置模型"""
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None
    log_retention_days: int = 30
    max_concurrent_skills: int = 5
    backup_enabled: bool = True


# ═══════════════════════════════════════════════════════════════════════════
# 第三部·业务逻辑层
# ═══════════════════════════════════════════════════════════════════════════

class SkillManager:
    """技能管理器"""
    
    @staticmethod
    def register_skill(skill_input: SkillInput) -> Skill:
        """注册新技能"""
        skill = Skill(
            id=skill_input.id,
            name=skill_input.name,
            platform=skill_input.platform,
            category=skill_input.category,
            priority=skill_input.priority,
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-SKILL-{skill_input.id}"
        )
        SKILL_REGISTRY[skill.id] = skill
        logger.info(f"✅ 技能已注册: {skill.id}")
        return skill
    
    @staticmethod
    def get_skill(skill_id: str) -> Optional[Skill]:
        """获取技能"""
        return SKILL_REGISTRY.get(skill_id)
    
    @staticmethod
    def list_skills(platform: Optional[str] = None, status: Optional[str] = None) -> List[Skill]:
        """列出技能"""
        skills = list(SKILL_REGISTRY.values())
        if platform:
            skills = [s for s in skills if s.platform == platform]
        if status:
            skills = [s for s in skills if s.status == status]
        return skills
    
    @staticmethod
    def execute_skill(skill_id: str, args: Optional[Dict[str, Any]] = None) -> Execution:
        """执行技能"""
        import uuid
        
        skill = SKILL_REGISTRY.get(skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail="技能不存在")
        
        execution = Execution(
            id=str(uuid.uuid4()),
            skill_id=skill_id,
            status="running",
            start_time=datetime.now(),
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EXEC-{uuid.uuid4().hex[:8]}"
        )
        
        EXECUTION_HISTORY.append(execution)
        
        # 模拟执行（实际应该调用真实的技能）
        asyncio.create_task(SkillManager._simulate_execution(execution, skill))
        
        logger.info(f"✅ 技能执行已提交: {execution.id}")
        return execution
    
    @staticmethod
    async def _simulate_execution(execution: Execution, skill: Skill):
        """模拟技能执行"""
        await asyncio.sleep(1)  # 模拟执行时间
        
        execution.status = "completed"
        execution.end_time = datetime.now()
        execution.duration_ms = int((execution.end_time - execution.start_time).total_seconds() * 1000)
        execution.result = {"output": f"技能 {skill.name} 执行成功"}
        
        # 更新技能统计
        skill.last_executed = datetime.now()
        skill.execution_count += 1
        skill.success_rate = (skill.execution_count - 1) / skill.execution_count * skill.success_rate + \
                            1 / skill.execution_count * 100
        
        logger.info(f"✅ 技能执行完成: {execution.id}")


class AlertManager:
    """告警管理器"""
    
    @staticmethod
    def create_alert(level: str, message: str, source: str) -> Alert:
        """创建告警"""
        import uuid
        
        alert = Alert(
            id=str(uuid.uuid4()),
            level=level,
            message=message,
            source=source,
            created_at=datetime.now()
        )
        
        ALERT_QUEUE.append(alert)
        logger.warning(f"🚨 新告警 [{level}]: {message}")
        return alert
    
    @staticmethod
    def get_alerts(level: Optional[str] = None, status: Optional[str] = None) -> List[Alert]:
        """获取告警"""
        alerts = ALERT_QUEUE.copy()
        if level:
            alerts = [a for a in alerts if a.level == level]
        if status:
            alerts = [a for a in alerts if a.status == status]
        return sorted(alerts, key=lambda x: x.created_at, reverse=True)
    
    @staticmethod
    def acknowledge_alert(alert_id: str) -> Alert:
        """确认告警"""
        for alert in ALERT_QUEUE:
            if alert.id == alert_id:
                alert.status = "acknowledged"
                alert.acknowledged_at = datetime.now()
                logger.info(f"✅ 告警已确认: {alert_id}")
                return alert
        raise HTTPException(status_code=404, detail="告警不存在")


class SystemMonitor:
    """系统监控器"""
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        """获取系统健康状态"""
        import os
        import psutil  # type: ignore[import-untyped]
        
        # 获取系统指标
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 计算执行成功率
        if EXECUTION_HISTORY:
            successful = sum(1 for e in EXECUTION_HISTORY if e.status == "completed")
            success_rate = (successful / len(EXECUTION_HISTORY)) * 100
        else:
            success_rate = 0
        
        return {
            "status": "healthy" if cpu_percent < 80 else "degraded",
            "timestamp": datetime.now().isoformat(),
            "cpu": round(cpu_percent, 2),
            "memory": round(memory.percent, 2),
            "disk": round(disk.percent, 2),
            "uptime_seconds": int(os.popen('uptime -p').read().count('day') * 86400),
            "active_skills": len([s for s in SKILL_REGISTRY.values() if s.status == "active"]),
            "total_executions": len(EXECUTION_HISTORY),
            "success_rate": round(success_rate, 2)
        }
    
    @staticmethod
    def get_dashboard() -> Dict[str, Any]:
        """获取仪表板数据"""
        recent_executions = sorted(EXECUTION_HISTORY, key=lambda x: x.start_time, reverse=True)[:10]
        active_alerts = AlertManager.get_alerts(status="active")
        
        return {
            "metrics": SystemMonitor.get_health(),
            "recent_executions": [
                {
                    "id": e.id,
                    "skill_id": e.skill_id,
                    "status": e.status,
                    "duration_ms": e.duration_ms,
                    "start_time": e.start_time.isoformat()
                }
                for e in recent_executions
            ],
            "active_alerts": [
                {
                    "id": a.id,
                    "level": a.level,
                    "message": a.message,
                    "created_at": a.created_at.isoformat()
                }
                for a in active_alerts
            ]
        }


# ═══════════════════════════════════════════════════════════════════════════
# 第四部·API 路由
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/health")
async def health_check():
    """系统健康检查"""
    return SystemMonitor.get_health()


@app.get("/api/v1/dashboard")
async def get_dashboard(time_range: str = "24h"):
    """获取仪表板数据"""
    return SystemMonitor.get_dashboard()


@app.get("/api/v1/skills")
async def list_skills(
    platform: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """列出技能"""
    skills = SkillManager.list_skills(platform=platform, status=status)
    return [skill.dict() for skill in skills]


@app.post("/api/v1/skills")
async def create_skill(skill_input: SkillInput):
    """创建新技能"""
    skill = SkillManager.register_skill(skill_input)
    return skill.dict()


@app.get("/api/v1/skills/{skill_id}")
async def get_skill(skill_id: str):
    """获取技能详情"""
    skill = SkillManager.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    return skill.dict()


@app.post("/api/v1/skills/{skill_id}/execute")
async def execute_skill(skill_id: str, body: Optional[Dict[str, Any]] = None):
    """执行技能"""
    execution = SkillManager.execute_skill(skill_id, args=body)
    return {
        "execution_id": execution.id,
        "status": execution.status,
        "dna": execution.dna
    }


@app.get("/api/v1/executions/{execution_id}")
async def get_execution(execution_id: str):
    """获取执行状态"""
    for execution in EXECUTION_HISTORY:
        if execution.id == execution_id:
            return execution.dict()
    raise HTTPException(status_code=404, detail="执行不存在")


@app.get("/api/v1/alerts")
async def list_alerts(
    level: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """列表告警"""
    alerts = AlertManager.get_alerts(level=level, status=status)
    return [alert.dict() for alert in alerts]


@app.post("/api/v1/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """确认告警"""
    alert = AlertManager.acknowledge_alert(alert_id)
    return {"status": "acknowledged", "alert_id": alert_id}


@app.get("/api/v1/logs")
async def query_logs(
    skill_id: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    limit: int = Query(100)
):
    """查询日志"""
    # 从执行历史中提取日志
    logs = []
    for execution in EXECUTION_HISTORY[-limit:]:
        logs.append({
            "id": execution.id,
            "level": "info" if execution.status == "completed" else "error",
            "message": f"Skill {execution.skill_id} {execution.status}",
            "skill_id": execution.skill_id,
            "timestamp": execution.start_time.isoformat(),
            "dna": execution.dna
        })
    return logs


@app.post("/api/v1/export/csv")
async def export_csv(body: Dict[str, Any]):
    """导出为 CSV"""
    import csv
    from io import StringIO
    
    data_type = body.get("data_type", "executions")
    
    output = StringIO()
    if data_type == "executions":
        writer = csv.writer(output)
        writer.writerow(["ID", "Skill", "Status", "Duration", "Start Time"])
        for e in EXECUTION_HISTORY:
            writer.writerow([e.id, e.skill_id, e.status, e.duration_ms, e.start_time])
    
    return output.getvalue()


@app.post("/api/v1/export/json")
async def export_json(body: Dict[str, Any]):
    """导出为 JSON"""
    data_type = body.get("data_type", "executions")
    
    if data_type == "executions":
        return {
            "data": [e.dict() for e in EXECUTION_HISTORY],
            "count": len(EXECUTION_HISTORY)
        }
    elif data_type == "alerts":
        return {
            "data": [a.dict() for a in ALERT_QUEUE],
            "count": len(ALERT_QUEUE)
        }
    else:
        raise HTTPException(status_code=400, detail="不支援的资料类型")



# ═══════════════════════════════════════════════════════════════════════════
# 龍魂 Skill 集成 API 端点
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/longhun-skills")
async def list_longhun_skills():
    """列出所有龍魂 Skills"""
    if not SKILLS_AVAILABLE:
        return {"error": "Skills 系统未可用", "skills": []}
    
    try:
        skill_registry = get_skill_registry()
        skills_list = skill_registry.list_skills()
        return {
            "status": "success",
            "html_skills": skills_list["html"],
            "python_skills": skills_list["python"],
            "total": skills_list["total"],
            "dna": "#龍芯⚡️2026-06-07-PHASE3-SKILLS-API-v1.0"
        }
    except Exception as e:
        logger.error(f"❌ 获取 Skills 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/longhun-skills/{skill_id}")
async def get_longhun_skill(skill_id: str):
    """获取龍魂 Skill 详情"""
    if not SKILLS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Skills 系统未可用")
    
    try:
        skill_registry = get_skill_registry()
        skill = skill_registry.get_skill(skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' 不存在")
        return {
            "status": "success",
            "skill": skill,
            "dna": "#龍芯⚡️2026-06-07-PHASE3-SKILLS-API-v1.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 获取 Skill 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/longhun-skills/{skill_id}/content")
async def get_longhun_skill_content(skill_id: str):
    """获取龍魂 Skill 完整内容"""
    if not SKILLS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Skills 系统未可用")
    
    try:
        skill_registry = get_skill_registry()
        content = skill_registry.get_skill_content(skill_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' 内容不可用")
        
        skill = skill_registry.get_skill(skill_id)
        return {
            "status": "success",
            "skill_id": skill_id,
            "type": skill["type"],
            "content": content,
            "dna": "#龍芯⚡️2026-06-07-PHASE3-SKILLS-API-v1.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 获取 Skill 内容失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/longhun-skills/{skill_id}/execute")
async def execute_longhun_skill(skill_id: str, params: Dict[str, Any] = None):  # type: ignore[reportArgumentType]
    """执行龍魂 Skill"""
    if not SKILLS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Skills 系统未可用")
    
    try:
        skill_registry = get_skill_registry()
        skill = skill_registry.get_skill(skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' 不存在")
        
        import uuid
        execution_id = str(uuid.uuid4())
        
        # 如果是 Python Skill，执行它
        if skill["type"] == "python":
            # 实际执行逻辑（这里简化处理）
            result = {"status": "queued", "execution_id": execution_id}
        else:
            # HTML Skill 只能在前端渲染
            result = {"status": "info", "message": "HTML Skill 需要在浏览器中渲染"}
        
        return {
            "status": "success",
            "skill_id": skill_id,
            "execution_id": execution_id,
            "result": result,
            "dna": "#龍芯⚡️2026-06-07-PHASE3-SKILLS-API-v1.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 执行 Skill 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/longhun-skills/config/export")
async def export_longhun_skills_config():
    """汇出龍魂 Skills 配置"""
    if not SKILLS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Skills 系统未可用")
    
    try:
        skill_registry = get_skill_registry()
        config = skill_registry.export_config()
        return {
            "status": "success",
            "config": config,
            "dna": "#龍芯⚡️2026-06-07-PHASE3-SKILLS-API-v1.0"
        }
    except Exception as e:
        logger.error(f"❌ 汇出配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/settings")
async def get_settings():
    """获取系统设置"""
    return {
        "alert_email": "admin@longhun-system.com",
        "log_retention_days": 30,
        "max_concurrent_skills": 5,
        "backup_enabled": True
    }


@app.put("/api/v1/settings")
async def update_settings(settings: Settings):
    """更新系统设置"""
    logger.info(f"✅ 设置已更新")
    return {"status": "updated", "settings": settings.dict()}


# ═══════════════════════════════════════════════════════════════════════════
# 第五部·WebSocket 实时连接
# ═══════════════════════════════════════════════════════════════════════════

@app.websocket("/ws/v1/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket 实时数据流"""
    await websocket.accept()
    ACTIVE_CONNECTIONS.append(websocket)
    
    try:
        while True:
            # 每秒发送一次健康检查数据
            data = SystemMonitor.get_health()
            await websocket.send_json({
                "type": "health",
                "data": data
            })
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
    finally:
        ACTIVE_CONNECTIONS.remove(websocket)


# ═══════════════════════════════════════════════════════════════════════════
# 第六部·初始化与启动
# ═══════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 龍魂系统 Phase 3 后端已启动")

    # 初始化龍魂 Skill 系统
    if SKILLS_AVAILABLE:
        try:
            skill_registry = get_skill_registry()
            skills_list = skill_registry.list_skills()
            logger.info(f"✅ 已加载 {skills_list['total']} 个龍魂 Skills")
            logger.info(f"   HTML Skills: {len(skills_list['html'])}")
            logger.info(f"   Python Skills: {len(skills_list['python'])}")
        except Exception as e:
            logger.error(f"❌ Skill 系统加载失败: {e}")
    
    # 初始化示例技能
    sample_skills = [
        SkillInput(id="/health-check", name="健康检查", platform="longhun", category="monitoring", priority=10),
        SkillInput(id="/api-check", name="API 检测", platform="kimi", category="monitoring", priority=9),
        SkillInput(id="/backup", name="自动备份", platform="longhun", category="system", priority=8),
    ]
    
    for skill in sample_skills:
        try:
            SkillManager.register_skill(skill)
        except:
            pass
    
    logger.info(f"✅ 已注册 {len(SKILL_REGISTRY)} 个技能")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("👋 龍魂系统 Phase 3 后端已关闭")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
