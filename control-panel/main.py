#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
🐉 龍魂操作台 MVP v1.1 · UID9622 调试
FastAPI 後端：統一 API 入口，串接 10 個 Skill 與預定義工作流。
"""
import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# 將專案根目錄加入路徑
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api import skill_wrappers, foundation_wrappers, system_monitor

app = FastAPI(
    title="龍魂操作台 MVP v1.1",
    description="UID9622 龍魂技能統一調度 API",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 靜態資源：操作台 UI + 技能文件
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
app.mount("/skill-assets", StaticFiles(directory=str(ROOT / "skills")), name="skill-assets")
app.mount("/docs-assets", StaticFiles(directory=str(ROOT / "docs")), name="docs-assets")

WORKFLOWS_PATH = Path(__file__).parent / "workflows" / "skill-workflows.json"
WORKFLOWS = json.loads(WORKFLOWS_PATH.read_text(encoding="utf-8"))["workflows"]

SKILL_METADATA = {
    "skill-1-algorithmic-art": {"name": "算法艺术生成器", "type": "html", "url": "/skill-assets/html-skills/skill-1-algorithmic-art.html"},
    "skill-2-brand-guidelines": {"name": "龍魂品牌指南", "type": "html", "url": "/skill-assets/html-skills/skill-2-brand-guidelines.html"},
    "skill-3-canvas-design": {"name": "画布设计工具", "type": "html", "url": "/skill-assets/html-skills/skill-3-canvas-design.html"},
    "skill-4-doc-coauthoring": {"name": "文档协作工具", "type": "html", "url": "/skill-assets/html-skills/skill-4-doc-coauthoring.html"},
    "skill-5-internal-comms": {"name": "内部通讯系统", "type": "html", "url": "/skill-assets/html-skills/skill-5-internal-comms.html"},
    "skill-6-mcp-builder": {"name": "MCP 服务器构建工具", "type": "python"},
    "skill-7-skill-creator": {"name": "技能创建框架", "type": "python"},
    "skill-8-slack-gif-creator": {"name": "Slack GIF 创建工具", "type": "python"},
    "skill-9-theme-factory": {"name": "主题工厂", "type": "python"},
    "skill-10-web-artifacts-builder": {"name": "Web 工件构建器", "type": "python"},
}


@app.get("/")
def index():
    return {"message": "龍魂操作台 MVP v1.1", "dna": "#龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-FILE1-FILE1-v1.1-1"}


@app.get("/api/health")
def health():
    return {"status": "ok", "uid": "9622", "panel_version": "1.1.0"}


@app.get("/api/skills")
def list_skills():
    return {"skills": [{"id": k, **v} for k, v in SKILL_METADATA.items()]}


@app.post("/api/skills/{skill_id}/run")
async def run_skill_endpoint(skill_id: str, request: Request):
    if skill_id not in SKILL_METADATA:
        raise HTTPException(status_code=404, detail=f"Skill {skill_id} not found")
    payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    result = await skill_wrappers.run_skill(skill_id, payload)
    return result


@app.get("/api/workflows")
def list_workflows():
    summaries = []
    for wf in WORKFLOWS:
        summaries.append({
            "id": wf["id"],
            "name": wf["name"],
            "description": wf["description"],
            "step_count": len(wf["steps"]),
        })
    return {"workflows": summaries}


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    for wf in WORKFLOWS:
        if wf["id"] == workflow_id:
            return wf
    raise HTTPException(status_code=404, detail="Workflow not found")


@app.post("/api/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: str, request: Request):
    wf = next((w for w in WORKFLOWS if w["id"] == workflow_id), None)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")

    override_payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict) and "payload" in body:
            override_payload = body["payload"]
    except Exception:
        pass

    results = []
    for idx, step in enumerate(wf["steps"]):
        if "foundation" in step:
            action = step["foundation"]
            payload = step.get("payload", {})
            if action in override_payload:
                payload = {**payload, **override_payload[action]}
            result = foundation_wrappers.run_foundation(action, payload)
            results.append({"step": idx + 1, "foundation": action, "result": result})
        else:
            skill = step["skill"]
            action = step.get("action", "run")
            payload = step.get("payload", {})
            if skill in override_payload:
                payload = {**payload, **override_payload[skill]}

            if action == "render":
                results.append({"step": idx + 1, "skill": skill, "action": "render", "url": SKILL_METADATA[skill].get("url")})
            else:
                result = await skill_wrappers.run_skill(skill, payload)
                results.append({"step": idx + 1, "skill": skill, "action": "run", "result": result})

    return {"workflow_id": workflow_id, "name": wf["name"], "results": results}


# ===== 底座能力聯動 API =====

@app.get("/api/foundation")
def list_foundation_apis():
    return {
        "apis": [
            {"path": "/api/audit/integrated", "method": "POST", "desc": "融合審計：system/script"},
            {"path": "/api/shield/{action}", "method": "POST", "desc": "龍盾：check/analyze/validate"},
            {"path": "/api/cnsh/align", "method": "POST", "desc": "CNSH 對齊檢查"},
            {"path": "/api/cnsh/script-manager", "method": "POST", "desc": "全腳本掃描"},
            {"path": "/api/instruction/execute", "method": "POST", "desc": "執行 @shield.check 等 DNA 指令"},
        ]
    }


@app.post("/api/audit/integrated")
async def audit_integrated(request: Request):
    payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    mode = payload.get("mode", "system")
    target = payload.get("file")
    return foundation_wrappers.run_integrated_audit(mode=mode, target_file=target)


@app.post("/api/shield/{action}")
async def shield_action(action: str, request: Request):
    if action not in ("check", "analyze", "validate"):
        raise HTTPException(status_code=400, detail="action must be check/analyze/validate")
    payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    file_name = payload.get("file", "shield_test_example.py")
    options = payload.get("options", [])
    return foundation_wrappers.run_shield(action, file_name, options)


@app.post("/api/cnsh/align")
async def cnsh_align(request: Request):
    payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    text = payload.get("text", "")
    context = payload.get("context", "stdin")
    return foundation_wrappers.run_cnsh_align(text, context)


@app.post("/api/cnsh/script-manager")
def cnsh_script_manager():
    return foundation_wrappers.run_script_manager()


@app.post("/api/instruction/execute")
async def instruction_execute(request: Request):
    payload = {}
    try:
        body = await request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    instruction = payload.get("instruction", "")
    return foundation_wrappers.run_instruction(instruction)


# ===== 生态实时仪表盘 API =====

@app.get("/api/system/status")
def system_status():
    """返回本机资源、模块入口、生态拓扑。"""
    return system_monitor.get_system_status()


@app.get("/ecosystem-dashboard")
def ecosystem_dashboard():
    """跳转到生态仪表盘页面。"""
    return RedirectResponse(url="/static/ecosystem-dashboard.html")


if __name__ == "__main__":
    import uvicorn, os
    port = int(os.environ.get("CONTROL_PANEL_PORT", "9622"))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)
