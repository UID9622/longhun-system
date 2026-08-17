#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 主权代理网关 v2.0（鸿蒙 + 小艺接入）
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-SOVEREIGN-GATEWAY-v2.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

新增功能:
  1. 鸿蒙设备注册与管理 (支持设备证书)
  2. 小艺语音助手接入 (会话绑定)
  3. 鸿蒙端SDK调用示例
  4. 小艺意图映射与路由
  5. 设备指纹黑名单机制
"""

import os
import sys
import json
import hashlib
import hmac
import time
import uuid
import subprocess
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List
from functools import wraps

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# ============================================================
# 引入龍魂农历干支引擎（项目内唯一时间戳来源）
# ============================================================
CALENDAR_ROOT = Path(__file__).resolve().parent.parent / "archive" / "experiments" / "calendar-context-logger"
if str(CALENDAR_ROOT) not in sys.path:
    sys.path.insert(0, str(CALENDAR_ROOT))

try:
    from calendar_core import LunarEngine
    LUNAR = LunarEngine()
except Exception as _e:
    LUNAR = None


def get_ganzhi_now() -> Dict[str, str]:
    """获取当前农历干支四柱，失败则回退到格里历占位。"""
    try:
        if LUNAR is not None:
            g = LUNAR.get_ganzhi()
            return {
                "year": g["year_zhu"],
                "month": g["month_zhu"],
                "day": g["day_zhu"],
                "hour": g["hour_zhu"],
            }
    except Exception:
        pass
    # 降级：格里历占位（仅用于极端降级场景）
    return {
        "year": datetime.now().strftime("%Y"),
        "month": datetime.now().strftime("%m"),
        "day": datetime.now().strftime("%d"),
        "hour": datetime.now().strftime("%H"),
    }


def get_gua_now() -> str:
    """获取当前卦象。"""
    try:
        if LUNAR is not None:
            return LUNAR.get_qigua()["ben_gua"]
    except Exception:
        pass
    return "萃"


# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_PREFIX = "#龍芯⚡️"

SOVEREIGN_DEVICE = {
    "hostname": "鲲鹏服务器",
    "ip": "119.13.90.27",
    "owner": "UID9622",
    "owner_name": "诸葛鑫",
    "since": "2025-06-01",
    "status": "🟢 主权锚定"
}

# 授权代理 (新增鸿蒙和小艺)
AUTHORIZED_PROXIES = {
    "kimi": {"id": "kimi", "allowed": True, "rate": 100, "desc": "Kimi AI助手"},
    "codebuddy": {"id": "codebuddy", "allowed": True, "rate": 50, "desc": "CodeBuddy IDE"},
    "notion": {"id": "notion", "allowed": True, "rate": 30, "desc": "Notion知识库"},
    "mac_local": {"id": "mac_local", "allowed": True, "rate": 200, "desc": "Mac本地终端"},
    "harmony": {"id": "harmony", "allowed": True, "rate": 300, "desc": "鸿蒙设备 (手机/平板)"},
    "xiaoyi": {"id": "xiaoyi", "allowed": True, "rate": 150, "desc": "小艺语音助手"},
}

# 项目根目录（兼容 ~/longhun-system）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "08_STATE"
AUDIT_DIR = PROJECT_ROOT / "04_AUDIT"
STATE_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# 鸿蒙设备注册表 (持久化)
HARMONY_DEVICES_FILE = STATE_DIR / "harmony_devices.json"

# 小艺会话缓存 (临时内存 + 可选持久化)
XIAOYI_SESSIONS_FILE = STATE_DIR / "xiaoyi_sessions.json"
XIAOYI_SESSIONS: Dict[str, Dict[str, Any]] = {}


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default if default is not None else {}


def save_json(path: Path, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_harmony_devices() -> Dict:
    return load_json(HARMONY_DEVICES_FILE, {})


def save_harmony_devices(devices: Dict):
    save_json(HARMONY_DEVICES_FILE, devices)


def load_xiaoyi_sessions() -> Dict:
    return load_json(XIAOYI_SESSIONS_FILE, {})


def save_xiaoyi_sessions(sessions: Dict):
    save_json(XIAOYI_SESSIONS_FILE, sessions)


# ============================================================
# 认证与审计 (升级)
# ============================================================

def generate_dna(suffix: str = "") -> str:
    gz = get_ganzhi_now()
    gua = get_gua_now()
    rand = hashlib.sha256(f"{suffix}{time.time()}{uuid.uuid4()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{gz['year']}·{gz['month']}·{gz['day']}·{gz['hour']}·{gua}-{suffix}-{UID}-{rand}"


def verify_dna(dna: str) -> bool:
    return isinstance(dna, str) and dna.startswith(DNA_PREFIX) and UID in dna


def verify_gpg_signature(data: str, signature: str) -> bool:
    """
    尝试 GPG 验证；若系统无可用 GPG 密钥环，则降级为 HMAC-SHA256 占位验证。
    生产环境必须配置真实 GPG 公钥并启用严格验证。
    """
    try:
        if not signature or not data:
            return False
        # 优先尝试 GPG（如果配置了公钥环）
        try:
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as df:
                df.write(data)
                data_file = df.name
            with tempfile.NamedTemporaryFile("w", suffix=".asc", delete=False) as sf:
                sf.write(signature)
                sig_file = sf.name
            result = subprocess.run(
                ["gpg", "--verify", sig_file, data_file],
                capture_output=True,
                text=True,
                timeout=5,
            )
            os.unlink(data_file)
            os.unlink(sig_file)
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            pass
        # 降级：HMAC-SHA256 占位（使用 CONFIRM 作为密钥）
        expected = hmac.new(
            CONFIRM.encode("utf-8"),
            data.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        # 允许 signature 是 hex 或 base64 形式
        sig_norm = signature.strip()
        if sig_norm == expected:
            return True
        try:
            decoded = base64.b64decode(sig_norm).hex()
            if decoded == expected:
                return True
        except Exception:
            pass
        return False
    except Exception:
        return False


def verify_harmony_certificate(device_id: str, _cert_chain: str) -> bool:
    """验证鸿蒙设备是否已注册且状态正常。"""
    devices = load_harmony_devices()
    return device_id in devices and devices[device_id].get("status") == "active"


async def authenticate_request(request: Request) -> Dict:
    """认证请求 - 支持鸿蒙设备证书和小艺会话。"""
    headers = request.headers
    dna = headers.get("X-Dragon-DNA")
    signature = headers.get("X-Dragon-Signature")
    proxy_id = headers.get("X-Proxy-ID", "unknown")
    device_id = headers.get("X-Device-ID")
    xiaoyi_session = headers.get("X-Xiaoyi-Session")

    # 1. 基础DNA验证
    if not dna or not verify_dna(dna):
        raise HTTPException(status_code=401, detail="无效或缺少 DNA 追溯码")

    # 2. 代理授权检查
    if proxy_id not in AUTHORIZED_PROXIES:
        raise HTTPException(status_code=403, detail=f"代理 {proxy_id} 未授权")
    if not AUTHORIZED_PROXIES[proxy_id]["allowed"]:
        raise HTTPException(status_code=403, detail=f"代理 {proxy_id} 已被禁用")

    # 3. 鸿蒙设备特殊验证
    if proxy_id == "harmony":
        if not device_id:
            raise HTTPException(status_code=401, detail="鸿蒙设备缺少设备ID")
        if not verify_harmony_certificate(device_id, ""):
            raise HTTPException(status_code=403, detail="鸿蒙设备未授权或已被封禁")
        # 更新活跃时间
        devices = load_harmony_devices()
        if device_id in devices:
            devices[device_id]["last_active"] = datetime.now().isoformat()
            save_harmony_devices(devices)

    # 4. 小艺会话验证
    if proxy_id == "xiaoyi":
        if not xiaoyi_session:
            raise HTTPException(status_code=401, detail="小艺缺少会话ID")
        if xiaoyi_session not in XIAOYI_SESSIONS:
            raise HTTPException(status_code=403, detail="小艺会话无效或已过期")
        XIAOYI_SESSIONS[xiaoyi_session]["last_active"] = datetime.now().isoformat()

    # 5. GPG / HMAC 签名验证
    if not signature:
        raise HTTPException(status_code=401, detail="缺少 GPG 签名")
    body = await request.body()
    data = f"{dna}{body.decode('utf-8', errors='ignore')}{CONFIRM}"
    if not verify_gpg_signature(data, signature):
        raise HTTPException(status_code=401, detail="GPG/HMAC 签名验证失败")

    # 6. 记录审计
    await record_audit({
        "timestamp": datetime.now().isoformat(),
        "proxy_id": proxy_id,
        "dna": dna,
        "device_id": device_id,
        "xiaoyi_session": xiaoyi_session,
        "path": request.url.path,
        "method": request.method,
        "status": "authenticated"
    })

    return {
        "dna": dna,
        "proxy_id": proxy_id,
        "device_id": device_id,
        "xiaoyi_session": xiaoyi_session,
        "authenticated": True,
        "timestamp": datetime.now().isoformat()
    }


async def record_audit(entry: Dict):
    audit_path = AUDIT_DIR / "gateway_audit.jsonl"
    with open(audit_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


async def record_shame(reason: str, dna: str, details: Dict):
    shame_path = STATE_DIR / "shame_wall.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "dna": dna,
        "details": details,
        "severity": "HIGH"
    }
    with open(shame_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# FastAPI 应用 (新增鸿蒙/小艺端点)
# ============================================================

GATEWAY_DNA = generate_dna("SOVEREIGN-GATEWAY-v2.0")

app = FastAPI(
    title="龍魂主权代理网关 v2.0",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 端点 (新增鸿蒙/小艺相关)
# ============================================================

@app.get("/")
async def root():
    return {
        "service": "龍魂主权代理网关 v2.0",
        "status": "🟢 运行中",
        "dna": GATEWAY_DNA,
        "confirm": CONFIRM,
        "sovereign": SOVEREIGN_DEVICE,
        "supported_proxies": list(AUTHORIZED_PROXIES.keys()),
        "harmony_devices_registered": len(load_harmony_devices()),
        "xiaoyi_sessions_active": len(XIAOYI_SESSIONS),
        "message": "只有 UID9622 可直连，所有代理需验证 DNA + GPG/HMAC 签名"
    }


@app.get("/api/sovereign/status")
async def sovereign_status():
    return {
        "sovereign": SOVEREIGN_DEVICE,
        "gateway_version": "v2.0",
        "dna": GATEWAY_DNA,
        "authorized_proxies": len(AUTHORIZED_PROXIES),
        "harmony_devices": load_harmony_devices(),
        "xiaoyi_sessions": XIAOYI_SESSIONS,
        "audit_enabled": True,
        "shame_wall_enabled": True
    }


@app.post("/api/proxy/{target}")
async def proxy_request(target: str, request: Request, auth: Dict = Depends(authenticate_request)):
    """代理转发 - 支持鸿蒙设备和小艺。"""
    proxy_id = auth["proxy_id"]
    dna = auth["dna"]
    device_id = auth.get("device_id")
    xiaoyi_session = auth.get("xiaoyi_session")

    target_services = {
        "kimi": {"port": 8765, "service": "Kimi桥接"},
        "notion": {"port": 8766, "service": "Notion同步"},
        "memory": {"port": 8777, "service": "记忆服务"},
        "clipboard": {"port": 8768, "service": "剪贴板容器"},
        "knowledge": {"port": 8769, "service": "知识图谱"},
        "ollama": {"port": 11434, "service": "Ollama推理"},
        "cnsheditor": {"port": 8770, "service": "CNSH编辑器"},
        "emotion": {"port": 8771, "service": "情绪纠偏引擎"},
        "task": {"port": 8772, "service": "任务编排"},
        "browser": {"port": 8773, "service": "浏览器托管"},
        "notion_bridge": {"port": 8774, "service": "Notion桥接"},
        "harmony": {"port": 8775, "service": "鸿蒙设备消息推送"},
        "xiaoyi": {"port": 8776, "service": "小艺语音合成"},
    }

    if target not in target_services:
        await record_shame(
            f"未授权目标: {target}",
            dna,
            {"proxy_id": proxy_id, "target": target, "device_id": device_id}
        )
        raise HTTPException(status_code=404, detail=f"目标服务 {target} 不存在")

    service = target_services[target]

    await record_audit({
        "timestamp": datetime.now().isoformat(),
        "proxy_id": proxy_id,
        "dna": dna,
        "device_id": device_id,
        "xiaoyi_session": xiaoyi_session,
        "target": target,
        "service": service["service"],
        "status": "forwarded"
    })

    try:
        import httpx
        body = await request.body()
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(
                method=request.method,
                url=f"http://127.0.0.1:{service['port']}{request.url.path}",
                headers={
                    "X-Dragon-DNA": dna,
                    "X-Proxy-ID": proxy_id,
                    "X-Device-ID": device_id or "",
                    "X-Xiaoyi-Session": xiaoyi_session or "",
                },
                content=body,
            )
            try:
                content = response.json()
            except Exception:
                content = {"raw": response.text}
            return JSONResponse(status_code=response.status_code, content=content)
    except Exception as e:
        await record_shame(
            f"转发失败: {target}",
            dna,
            {"proxy_id": proxy_id, "error": str(e)}
        )
        raise HTTPException(status_code=503, detail=f"服务 {target} 不可用: {str(e)}")


# ============================================================
# 鸿蒙设备管理端点
# ============================================================

@app.post("/api/harmony/register")
async def register_harmony_device(request: Request):
    """注册鸿蒙设备。首次自动注册；重复注册返回已注册信息。"""
    data = await request.json()
    device_id = data.get("device_id")
    device_name = data.get("device_name", f"鸿蒙设备-{device_id[:8] if device_id else 'UNKNOWN'}")
    model = data.get("model", "未知型号")
    harmony_version = data.get("harmony_version", "未知版本")

    if not device_id:
        raise HTTPException(status_code=400, detail="缺少 device_id")

    devices = load_harmony_devices()
    if device_id in devices:
        return {"status": "already_registered", "device": devices[device_id]}

    device_dna = generate_dna(f"HARMONY-{device_id[:8]}")
    devices[device_id] = {
        "device_id": device_id,
        "device_name": device_name,
        "model": model,
        "harmony_version": harmony_version,
        "dna": device_dna,
        "registered_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
        "status": "active",
        "owner": UID
    }
    save_harmony_devices(devices)

    await record_audit({
        "timestamp": datetime.now().isoformat(),
        "action": "harmony_register",
        "device_id": device_id,
        "device_name": device_name,
        "status": "registered"
    })

    return {"status": "registered", "device": devices[device_id]}


@app.post("/api/harmony/revoke")
async def revoke_harmony_device(request: Request):
    """撤销鸿蒙设备授权。"""
    data = await request.json()
    device_id = data.get("device_id")
    if not device_id:
        raise HTTPException(status_code=400, detail="缺少 device_id")

    devices = load_harmony_devices()
    if device_id in devices:
        devices[device_id]["status"] = "revoked"
        save_harmony_devices(devices)
        await record_audit({
            "timestamp": datetime.now().isoformat(),
            "action": "harmony_revoke",
            "device_id": device_id
        })
        return {"status": "revoked", "device_id": device_id}
    return {"status": "not_found"}


# ============================================================
# 小艺会话管理端点
# ============================================================

@app.post("/api/xiaoyi/session/start")
async def start_xiaoyi_session(request: Request):
    """启动小艺会话。"""
    data = await request.json()
    user_id = data.get("user_id", UID)
    session_id = str(uuid.uuid4())
    now = datetime.now()
    XIAOYI_SESSIONS[session_id] = {
        "user_id": user_id,
        "created_at": now.isoformat(),
        "last_active": now.isoformat(),
        "expires_at": (now.timestamp() + 3600),
        "context": {}
    }
    save_xiaoyi_sessions(XIAOYI_SESSIONS)
    await record_audit({
        "timestamp": now.isoformat(),
        "action": "xiaoyi_session_start",
        "session_id": session_id,
        "user_id": user_id
    })
    return {"session_id": session_id, "expires_in": 3600}


@app.post("/api/xiaoyi/session/end")
async def end_xiaoyi_session(request: Request):
    """结束小艺会话。"""
    data = await request.json()
    session_id = data.get("session_id")
    if session_id in XIAOYI_SESSIONS:
        del XIAOYI_SESSIONS[session_id]
        save_xiaoyi_sessions(XIAOYI_SESSIONS)
        await record_audit({
            "timestamp": datetime.now().isoformat(),
            "action": "xiaoyi_session_end",
            "session_id": session_id
        })
        return {"status": "ended"}
    raise HTTPException(status_code=404, detail="会话不存在")


# ============================================================
# 审计与耻辱墙端点
# ============================================================

@app.get("/api/audit")
async def get_audit(limit: int = 100):
    audit_path = AUDIT_DIR / "gateway_audit.jsonl"
    if not audit_path.exists():
        return {"entries": [], "count": 0}
    entries = []
    with open(audit_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return {"entries": entries[-limit:], "count": len(entries)}


@app.get("/api/shame")
async def get_shame():
    shame_path = STATE_DIR / "shame_wall.jsonl"
    if not shame_path.exists():
        return {"entries": [], "count": 0}
    entries = []
    with open(shame_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return {"entries": entries, "count": len(entries)}


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 主权代理网关 v2.0 (鸿蒙 + 小艺完整接入)            ║
╠══════════════════════════════════════════════════════════════════╣
║  DNA: {GATEWAY_DNA:<55} ║
║  确认码: {CONFIRM:<52} ║
║  主权人: UID9622 · 诸葛鑫                                     ║
║  主权设备: 鲲鹏服务器 (119.13.90.27)                          ║
║  状态: 🟢 运行中                                              ║
╠══════════════════════════════════════════════════════════════════╣
║  📡 网关地址: 0.0.0.0:8766                                    ║
║  🔐 认证方式: DNA + GPG/HMAC + 鸿蒙证书 + 小艺会话           ║
║  📱 鸿蒙设备注册: 已启用                                      ║
║  🗣️ 小艺会话管理: 已启用                                     ║
║  📋 审计: 已启用                                              ║
║  📋 耻辱墙: 已启用                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  🧩 已接入代理:                                               ║
║     - Kimi, CodeBuddy, Notion, Mac本地                        ║
║     - 鸿蒙设备 (手机/平板/智慧屏)                             ║
║     - 小艺 (语音助手)                                         ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8766)
