#!/usr/bin/env python3
"""
🐉 龍魂操作台 MVP v1.1 · UID9622 调试
FastAPI 后端：统一 API 入口，串接 10 个 Skill 与预定义工作流。
"""
import json
import os
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
import httpx

# 将专案根目录加入路径
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api import skill_wrappers, foundation_wrappers, system_monitor, behavior_wrappers
from skills.registry import LonghunSkillRegistry, CLOUD_SKILL_IDS, CLOUD_DEFAULT_PORTS
from tongxinyi_gate import TongxinyiGate

from sovereignty.portal import model_router
from sovereignty.portal.longhun_crypto import (
    LonghunCryptoError,
    NonceCache,
    make_envelope,
    open_envelope,
)

LONGHUN_EXECUTOR_SECRET = os.getenv("LONGHUN_EXECUTOR_SECRET", "")
_SECURE_NONCE_CACHE = NonceCache()
_LOCAL_GATEWAY_LOG = Path.home() / "cnsh" / "logs"

# 统一技能注册表
_SKILL_REGISTRY = LonghunSkillRegistry()

def _get_registry():
    return _SKILL_REGISTRY


def _secure_log(entry: dict):
    _LOCAL_GATEWAY_LOG.mkdir(parents=True, exist_ok=True)
    path = _LOCAL_GATEWAY_LOG / f"longhun_secure_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = uuid.uuid4().hex[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


app = FastAPI(
    title="龍魂操作台 MVP v1.1",
    description="UID9622 龍魂技能统一调度 API",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "LONGHUN_CORS_ORIGINS",
        "https://longhun888.com,http://localhost:3000,http://127.0.0.1:3000",
    ).split(","),
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-DNA-Token", "X-Executor-UID"],
)

# 静态资源：操作台 UI + 技能文件
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
app.mount("/skill-assets", StaticFiles(directory=str(ROOT / "skills")), name="skill-assets")
app.mount("/docs-assets", StaticFiles(directory=str(ROOT / "docs")), name="docs-assets")

WORKFLOWS_PATH = Path(__file__).parent / "workflows" / "skill-workflows.json"
WORKFLOWS = json.loads(WORKFLOWS_PATH.read_text(encoding="utf-8"))["workflows"]

def _build_skill_metadata():
    """从统一注册表构建 control-panel 使用的 SKILL_METADATA。"""
    registry = _get_registry()
    metadata = {}
    for sk in registry.list_skills():
        sk_id = sk["id"]
        meta = {
            "name": sk["name"],
            "version": sk["version"],
            "description": sk["description"],
            "type": sk["type"],
            "scope": sk["scope"],
            "source": sk["source"],
            "scripts": sk["scripts"],
            "path": sk["path"],
            "dna": sk.get("dna"),
            "cloud_port": sk.get("cloud_port"),
        }
        # html 类型补充静态资源 URL
        if sk["type"] == "html" and sk_id.startswith("skill-"):
            meta["url"] = f"/skill-assets/html-skills/{sk_id}.html"
        metadata[sk_id] = meta
    return metadata


SKILL_METADATA = _build_skill_metadata()

# 通心译前置翻译闸门（所有带 task 的请求默认先翻译）
_TONGXINYI_GATE = TongxinyiGate(SKILL_METADATA)
TONGXINYI_GATE_ENABLED = os.getenv("TONGXINYI_GATE_ENABLED", "true").lower() == "true"


@app.get("/")
def index():
    return {"message": "龍魂操作台 MVP v1.1", "dna": #龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-FILE1-FILE1-FILE1-v1.1-1"}


@app.get("/api/health")
def health():
    return {"状态": "ok", "uid": "9622", "panel_version": "1.1.0"}


@app.get("/api/secure/health")
def secure_health():
    """执行器健康检查：确认安全解密通道就绪。"""
    return {
        "状态": "ok",
        "channel": "secure",
        "secret_configured": bool(LONGHUN_EXECUTOR_SECRET),
        "dna": _dna("SECURE-HEALTH"),
    }


@app.post("/api/secure/execute")
async def secure_execute(request: Request):
    """
    仅接受来自 DeepSeek 执行器的加密请求。
    解密后按 route 派发：chat / skill / echo
    """
    dna = _dna("SECURE-EXECUTE")
    client_host = request.client.host if request.client else "unknown"

    if not LONGHUN_EXECUTOR_SECRET:
        _secure_log({"ts": _now(), "dna": dna, "event": "secret_missing", "tricolor": "🔴"})
        raise HTTPException(status_code=503, detail="执行器密钥未配置")

    try:
        envelope = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="请求体不是有效 JSON")

    # 解密 + 校验 HMAC / 时间戳 / 重放
    try:
        plain = open_envelope(envelope, LONGHUN_EXECUTOR_SECRET, _SECURE_NONCE_CACHE, ttl=300)
    except LonghunCryptoError as e:
        _secure_log({
            "ts": _now(), "dna": dna, "event": "envelope_verify_failed",
            "client": client_host, "error": str(e), "tricolor": "🔴",
        })
        raise HTTPException(status_code=403, detail=f"信封校验失败: {e}")

    route = plain.get("route", "")
    payload = plain.get("payload", {})
    meta = plain.get("meta", {})

    result = {}
    tricolor = "🟢"

    try:
        if route == "echo":
            result = {"echo": payload}

        elif route == "chat":
            chat_req = model_router.ChatRequest(**payload)
            result = model_router.chat(chat_req)

        elif route == "skill":
            skill_id = payload.get("skill_id")
            if not skill_id or skill_id not in SKILL_METADATA:
                raise ValueError(f"无效或未知的 skill_id: {skill_id}")
            skill_payload = payload.get("payload", {})
            result = await skill_wrappers.run_skill(skill_id, skill_payload)

        else:
            raise ValueError(f"未知 route: {route}")
    except Exception as e:
        tricolor = "🔴"
        result = {"error": str(e)}

    _secure_log({
        "ts": _now(), "dna": dna, "event": "secure_execute",
        "client": client_host, "route": route,
        "executor_dna": meta.get("executor_dna"),
        "tricolor": tricolor,
    })

    response_payload = {
        "status": "ok" if tricolor == "🟢" else "error",
        "route": route,
        "result": result,
        "dna": dna,
        "ts": _now(),
    }
    return make_envelope(response_payload, LONGHUN_EXECUTOR_SECRET)


@app.get("/api/skills")
def list_skills():
    return {"skills": [{"id": k, **v} for k, v in SKILL_METADATA.items()]}


@app.get("/api/skills/registry")
def skill_registry():
    """返回统一注册表全景图。"""
    return {
        "total": len(SKILL_METADATA),
        "skills": [{"id": k, **v} for k, v in SKILL_METADATA.items()],
        "dna": "#龍芯⚡️2026-06-23-LONGHUN-CONTROL-PANEL-v1.2",
    }


@app.get("/api/skills/assessment")
def skill_assessment():
    """返回所有技能的自评报告（活跃度、健康度、孤独度、建议）。"""
    report_path = ROOT / "docs" / "module-self-assessment.json"
    try:
        if not report_path.exists():
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "module_self_assessment.py")],
                capture_output=True,
                text=True,
                timeout=60,
            )
        return json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"自评报告生成失败: {e}")


@app.post("/api/tongxinyi/translate")
async def tongxinyi_translate(request: Request):
    """通心译前置翻译：把用户输入转化为可执行意图骨架 + 三色审计。"""
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    text = 载荷.get("text", 载荷.get("task", ""))
    uid = 载荷.get("uid", "UID9622")
    if not text:
        raise HTTPException(status_code=400, detail="缺少 text 或 task 字段")
    if not TONGXINYI_GATE_ENABLED:
        raise HTTPException(status_code=503, detail="通心译闸门已关闭")
    return {
        "状态": "success",
        "通心译": _TONGXINYI_GATE.translate(text, uid),
    }


@app.post("/api/skills/dispatch")
async def dispatch_skill(request: Request):
    """根据任务描述，推荐并派发最合适的技能。"""
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    task = 载荷.get("task", "").lower()
    if not task:
        raise HTTPException(status_code=400, detail="缺少 task 字段")

    # 简单关键词匹配打分：支持整词、2-4 字滑动窗口
    raw = task.replace("，", " ").replace("。", " ").replace("、", " ")
    words = [w.strip() for w in raw.split() if len(w.strip()) >= 2]
    # 添加 2-3 字滑动窗口，用于中文子串匹配
    ngrams = set()
    for w in words:
        for i in range(len(w) - 1):
            ngrams.add(w[i:i+2])
        for i in range(len(w) - 2):
            ngrams.add(w[i:i+3])
    keywords = set(words) | ngrams

    scored = []
    for sk_id, 元数据 in SKILL_METADATA.items():
        文本 = f"{sk_id} {元数据.get('name', '')} {元数据.get('description', '')}".lower()
        score = 0
        for kw in keywords:
            if kw in 文本:
                score += len(kw)  # 长词匹配权重更高
        if score > 0:
            scored.append((score, sk_id, 元数据))
    scored.sort(key=lambda x: x[0], reverse=True)

    top = scored[:5]
    return {
        "task": task,
        "recommended": [
            {"id": sk_id, "name": 元数据.get("name"), "type": 元数据.get("type"), "score": score}
            for score, sk_id, 元数据 in top
        ],
        "total_matches": len(scored),
        "run_url_template": f"/api/skills/{{skill_id}}/run",
    }


@app.post("/api/skills/council")
async def skill_council(request: Request):
    """
    模块议事厅：让多个相关技能就同一任务“发言”。
    返回每个候选技能的意见、健康度、孤独度和建议。
    """
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    task = 载荷.get("task", "").lower()
    if not task:
        raise HTTPException(status_code=400, detail="缺少 task 字段")

    # 复用 dispatch 的打分逻辑
    raw = task.replace("，", " ").replace("。", " ").replace("、", " ")
    words = [w.strip() for w in raw.split() if len(w.strip()) >= 2]
    ngrams = set()
    for w in words:
        for i in range(len(w) - 1):
            ngrams.add(w[i:i+2])
        for i in range(len(w) - 2):
            ngrams.add(w[i:i+3])
    keywords = set(words) | ngrams

    scored = []
    for sk_id, 元数据 in SKILL_METADATA.items():
        文本 = f"{sk_id} {元数据.get('name', '')} {元数据.get('description', '')}".lower()
        score = 0
        for kw in keywords:
            if kw in 文本:
                score += len(kw)
        if score > 0:
            scored.append((score, sk_id, 元数据))
    scored.sort(key=lambda x: x[0], reverse=True)

    # 加载自评报告
    assessment_map = {}
    report_path = ROOT / "docs" / "module-self-assessment.json"
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            for item in report.get("skills", []):
                assessment_map[item["id"]] = item
        except Exception:
            pass

    opinions = []
    for score, sk_id, 元数据 in scored[:5]:
        assessment = assessment_map.get(sk_id, {})
        opinions.append({
            "id": sk_id,
            "name": 元数据.get("name"),
            "type": 元数据.get("type"),
            "score": score,
            "opinion": 元数据.get("description", "该模块暂无意见"),
            "health": assessment.get("health", "未知"),
            "loneliness": assessment.get("loneliness", "未知"),
            "recommendation": assessment.get("recommendation", "保持观察"),
        })

    return {
        "task": task,
        "opinions": opinions,
        "total_matches": len(scored),
        "dna": "#龍芯⚡️2026-06-23-LONGHUN-SKILL-COUNCIL-v1.0",
    }


def _run_subprocess_skill(skill_id: str, skill_dir: Path, scripts: List[str], 载荷: Dict[str, Any], shell: bool = False) -> Dict[str, Any]:
    """以子进程方式运行外部 Python / Shell 技能。"""
    if shell:
        candidates = [s for s in scripts if s.endswith(".sh")]
        cmd_prefix = ["bash"]
        run_type = "shell"
    else:
        candidates = [s for s in scripts if s.endswith(".py")]
        cmd_prefix = [sys.executable]
        run_type = "python"

    if not candidates:
        raise HTTPException(status_code=500, detail=f"No {'shell' if shell else 'python'} script found for skill {skill_id}")

    script_path = skill_dir / "scripts" / candidates[0]
    args = 载荷.get("args", [])
    if not isinstance(args, list):
        args = [str(args)]

    env = os.environ.copy()
    params_json = json.dumps(载荷, ensure_ascii=False)
    env["LONGHUN_SKILL_PARAMS"] = params_json
    env["LONGHUN_SKILL_ID"] = skill_id

    try:
        proc = subprocess.run(
            cmd_prefix + [str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(script_path.parent),
            env=env,
        )
        return {
            "状态": "success" if proc.returncode == 0 else "error",
            "skill_id": skill_id,
            "type": run_type,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"状态": "error", "skill_id": skill_id, "error": "execution timeout (60s)"}
    except Exception as e:
        return {"状态": "error", "skill_id": skill_id, "error": str(e)}


@app.post("/api/skills/{skill_id}/run")
async def run_skill_endpoint(skill_id: str, request: Request):
    if skill_id not in SKILL_METADATA:
        raise HTTPException(status_code=404, detail=f"Skill {skill_id} not found")
    元数据 = SKILL_METADATA[skill_id]
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass

    # 通心译闸门：如果请求体带 task/text，先翻译再执行
    通心译结果 = None
    if TONGXINYI_GATE_ENABLED:
        待译文本 = 载荷.get("task") or 载荷.get("text")
        if 待译文本:
            通心译结果 = _TONGXINYI_GATE.translate(str(待译文本), 载荷.get("uid", "UID9622"))

    sk_type = 元数据.get("type", "")
    sk_source = 元数据.get("source", "")

    结果 = None

    # 内置 Python Skill（skill-6 到 skill-10）：继续走 skill_wrappers
    if sk_type == "python" and skill_id.startswith("skill-") and sk_source == "internal":
        结果 = await skill_wrappers.run_skill(skill_id, 载荷)

    # HTML Skill 直接返回渲染地址
    elif sk_type == "html":
        结果 = {"状态": "success", "skill_id": skill_id, "type": "html", "url": 元数据.get("url")}

    else:
        # 外部 Python / Shell / Cloud 技能：通过 scripts/ 子进程派发
        scripts = 元数据.get("scripts", [])
        skill_path = Path(元数据["path"])

        # Cloud 技能优先尝试 CLI 模式（不直接启动独立服务）
        if skill_id in CLOUD_SKILL_IDS and scripts:
            # 注入端口环境变量，便于 cloud 脚本在 standalone 模式下使用
            env_port = 元数据.get("cloud_port")
            if env_port:
                os.environ[f"LONGHUN_{skill_id.replace('-', '_').upper()}_PORT"] = str(env_port)
            结果 = _run_subprocess_skill(skill_id, skill_path, scripts, 载荷, shell=False)

        elif sk_type in ("python", "mixed") and scripts:
            结果 = _run_subprocess_skill(skill_id, skill_path, scripts, 载荷, shell=False)

        elif sk_type in ("shell", "mixed") and scripts:
            结果 = _run_subprocess_skill(skill_id, skill_path, scripts, 载荷, shell=True)

        else:
            # 纯文档 / 语义技能：返回元数据供上层决策
            结果 = {
                "状态": "success",
                "skill_id": skill_id,
                "type": sk_type or "kimi-skill",
                "metadata": 元数据,
                "note": "该技能为文档/语义技能，无可直接执行的脚本，需通过 Kimi 主控调用。",
            }

    if 通心译结果 is not None:
        结果["通心译"] = 通心译结果

    return 结果


@app.get("/api/workflows")
def list_workflows():
    摘要列表 = []
    for 工作流 in WORKFLOWS:
        摘要列表.append({
            "id": 工作流["id"],
            "name": 工作流["name"],
            "description": 工作流["description"],
            "step_count": len(工作流["steps"]),
        })
    return {"workflows": 摘要列表}


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    for 工作流 in WORKFLOWS:
        if 工作流["id"] == workflow_id:
            return 工作流
    raise HTTPException(status_code=404, detail="Workflow not found")


@app.post("/api/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: str, request: Request):
    工作流 = next((w for w in WORKFLOWS if w["id"] == workflow_id), None)
    if not 工作流:
        raise HTTPException(status_code=404, detail="Workflow not found")

    覆盖载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict) and "载荷" in 请求体:
            覆盖载荷 = 请求体["载荷"]
    except Exception:
        pass

    结果列表 = []
    for 索引, 步骤 in enumerate(工作流["steps"]):
        if "foundation" in 步骤:
            动作 = 步骤["foundation"]
            载荷 = 步骤.get("载荷", {})
            if 动作 in 覆盖载荷:
                载荷 = {**载荷, **覆盖载荷[动作]}
            结果 = foundation_wrappers.run_foundation(动作, 载荷)
            结果列表.append({"步骤": 索引 + 1, "foundation": 动作, "结果": 结果})
        else:
            skill = 步骤["skill"]
            动作 = 步骤.get("动作", "run")
            载荷 = 步骤.get("载荷", {})
            if skill in 覆盖载荷:
                载荷 = {**载荷, **覆盖载荷[skill]}

            if 动作 == "render":
                结果列表.append({"步骤": 索引 + 1, "skill": skill, "动作": "render", "url": SKILL_METADATA[skill].get("url")})
            else:
                结果 = await skill_wrappers.run_skill(skill, 载荷)
                结果列表.append({"步骤": 索引 + 1, "skill": skill, "动作": "run", "结果": 结果})

    return {"workflow_id": workflow_id, "name": 工作流["name"], "结果列表": 结果列表}


# ===== 底座能力联动 API =====

@app.get("/api/foundation")
def list_foundation_apis():
    return {
        "apis": [
            {"path": "/api/audit/integrated", "method": "POST", "desc": "融合审计：system/script"},
            {"path": "/api/shield/{动作}", "method": "POST", "desc": "龍盾：check/analyze/validate"},
            {"path": "/api/cnsh/align", "method": "POST", "desc": "CNSH 对齐检查"},
            {"path": "/api/cnsh/script-manager", "method": "POST", "desc": "全脚本扫描"},
            {"path": "/api/指令/execute", "method": "POST", "desc": "执行 @shield.check 等 DNA 指令"},
        ]
    }


@app.post("/api/audit/integrated")
async def audit_integrated(request: Request):
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    模式 = 载荷.get("模式", "system")
    目标 = 载荷.get("file")
    return foundation_wrappers.run_integrated_audit(模式=模式, target_file=目标)


@app.post("/api/shield/{动作}")
async def shield_action(动作: str, request: Request):
    if 动作 not in ("check", "analyze", "validate"):
        raise HTTPException(status_code=400, detail="动作 must be check/analyze/validate")
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    文件名 = 载荷.get("file", "shield_test_example.py")
    选项 = 载荷.get("选项", [])
    return foundation_wrappers.run_shield(动作, 文件名, 选项)


@app.post("/api/cnsh/align")
async def cnsh_align(request: Request):
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    文本 = 载荷.get("文本", "")
    上下文 = 载荷.get("上下文", "stdin")
    return foundation_wrappers.run_cnsh_align(文本, 上下文)


@app.post("/api/cnsh/script-manager")
def cnsh_script_manager():
    return foundation_wrappers.run_script_manager()


@app.post("/api/research/光刻机瓶颈推演")
async def 光刻机瓶颈推演(request: Request):
    """运行龍魂光刻机瓶颈推演引擎：五行决策 + CNSH建模 + 压缩加密"""
    脚本路径 = Path("/Users/zuimeidedeyihan/longhun-system/cnsh/research/光刻机瓶颈推演引擎.py")
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    参数 = 载荷.get("args", [])
    try:
        进程 = subprocess.run(
            [sys.executable, str(脚本路径)] + 参数,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(脚本路径.parent),
        )
        return {
            "状态": "success",
            "类型": "kimi-python",
            "returncode": 进程.returncode,
            "stdout": 进程.stdout,
            "stderr": 进程.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"状态": "error", "错误": "execution timeout (120s)"}
    except Exception as e:
        return {"状态": "error", "错误": str(e)}


@app.post("/api/指令/execute")
async def instruction_execute(request: Request):
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass
    指令 = 载荷.get("指令", "")
    return foundation_wrappers.run_instruction(指令)


# ===== 生态实时仪表盘 API =====

@app.get("/api/system/状态")
def system_status():
    """返回本机资源、模块入口、生态拓扑。"""
    return system_monitor.get_system_status()


@app.get("/ecosystem-dashboard")
def ecosystem_dashboard():
    """跳转到生态仪表盘页面。"""
    return RedirectResponse(url="/static/ecosystem-dashboard.html")


# ===== 龍魂公民画像引擎（亮灯功能）API =====

@app.get("/api/behavior/{uid}/profile")
def behavior_profile(uid: str):
    """获取用户六大维度画像与亮灯设置。"""
    try:
        return {"状态": "success", "uid": uid, "profile": behavior_wrappers.获取画像(uid)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/behavior/{uid}/display")
def behavior_display(uid: str):
    """获取用户选择对外展示的亮灯信息。"""
    try:
        return {"状态": "success", "uid": uid, "display": behavior_wrappers.获取亮灯展示(uid)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/behavior/{uid}/record")
async def behavior_record(uid: str, request: Request):
    """记录一条行为。请求体：{类型, 名称, 权重?, 真实度?, 连续天数?}"""
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass

    类型 = 载荷.get("类型", 载荷.get("type", "")).strip()
    名称 = 载荷.get("名称", 载荷.get("name", "")).strip()
    if not 类型 or not 名称:
        raise HTTPException(status_code=400, detail="缺少 类型 和 名称 字段")

    try:
        结果 = behavior_wrappers.记录行为(
            用户ID=uid,
            类型=类型,
            名称=名称,
            权重=载荷.get("权重", 载荷.get("weight")),
            真实度=载荷.get("真实度", 载荷.get("authenticity")),
            连续天数=载荷.get("连续天数", 载荷.get("days")),
        )
        return 结果
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/behavior/{uid}/light")
async def behavior_light(uid: str, request: Request):
    """设置维度亮灯开关。请求体：{维度, 开关} 或 {dimension, on}"""
    载荷 = {}
    try:
        请求体 = await request.json()
        if isinstance(请求体, dict):
            载荷 = 请求体
    except Exception:
        pass

    维度 = 载荷.get("维度", 载荷.get("dimension", "")).strip()
    开关 = 载荷.get("开关", 载荷.get("on"))
    if not 维度 or 开关 is None or not isinstance(开关, bool):
        raise HTTPException(status_code=400, detail="缺少 维度 和 开关(boolean) 字段")

    try:
        return behavior_wrappers.设置亮灯(uid, 维度, 开关)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 云端 Skill 反向代理（解决 8443 端口冲突）=====

_CLOUD_PREFIXES = {
    "longhun-cloud-panel": ("panel", CLOUD_DEFAULT_PORTS["longhun-cloud-panel"]),
    "longhun-cloud-deploy": ("deploy", CLOUD_DEFAULT_PORTS["longhun-cloud-deploy"]),
    "longhun-cloud-mcp": ("mcp", CLOUD_DEFAULT_PORTS["longhun-cloud-mcp"]),
    "longhun-cloud-notion": ("notion", CLOUD_DEFAULT_PORTS["longhun-cloud-notion"]),
    "longhun-cloud-kimi": ("kimi", CLOUD_DEFAULT_PORTS["longhun-cloud-kimi"]),
}


def _build_cloud_routes():
    """动态注册云端 Skill 反向代理路由。"""
    for skill_id, (prefix, port) in _CLOUD_PREFIXES.items():
        # 使用闭包捕获 prefix/port
        async def _proxy(request: Request, prefix=prefix, port=port):
            path = request.path_params.get("path", "")
            target_url = f"http://127.0.0.1:{port}/{prefix}/{path}"
            method = request.method
            headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
            try:
                body = await request.body()
            except Exception:
                body = b""
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.request(method, target_url, headers=headers, content=body)
                return StreamingResponse(
                    content=response.iter_bytes(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except httpx.ConnectError:
                raise HTTPException(status_code=503, detail=f"云端 Skill {prefix} 未启动 (端口 {port})")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"代理失败: {e}")

        app.get(f"/{prefix}/{{path:path}}", name=f"proxy_{prefix}_get")(_proxy)
        app.post(f"/{prefix}/{{path:path}}", name=f"proxy_{prefix}_post")(_proxy)
        app.put(f"/{prefix}/{{path:path}}", name=f"proxy_{prefix}_put")(_proxy)
        app.delete(f"/{prefix}/{{path:path}}", name=f"proxy_{prefix}_delete")(_proxy)


_build_cloud_routes()


if __name__ == "__main__":

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9622, reload=False)
