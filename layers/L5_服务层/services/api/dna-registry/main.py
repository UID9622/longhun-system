#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂统一DNA登记册 · Web API 桥接 v1.0                               ║
║     LongHun Unified DNA Registry · FastAPI Bridge                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙申·甲寅·壬申-DNA-REGISTRY-WEB-API-v1.0             ║
║  端口: 8778  本地专属 · 不对外开放                                      ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# 把 bin/ 加入路径，复用核心引擎
监管仓根 = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(监管仓根 / "bin"))

from lh_unified_dna_registry import (  # type: ignore[import-not-found]
    注册资产, 获取主DNA, 获取状态, 验证资产归属,
    加载登记册, 注册表目录, 资产类型表, 类别色,
)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-not-found]
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles  # type: ignore[import-not-found]
from pydantic import BaseModel

# ═══════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════

app = FastAPI(
    title="龍魂统一DNA登记册 API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# CORS — 本地开发用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件 — 前端口
UI目录 = 监管仓根 / "L5_服务层/services/portal/portal/dna-registry"
if UI目录.exists():
    app.mount("/static", StaticFiles(directory=str(UI目录)), name="static")


# ═══════════════════════════════════════════
# 请求模型
# ═══════════════════════════════════════════

class 注册请求(BaseModel):
    uid: str
    资产类型: str
    资产编号: str
    标签: list[str] = []
    备注: str = ""
    验证状态: str = "待验证"

class 验证请求(BaseModel):
    uid: str
    资产类型: str
    资产编号: str


# ═══════════════════════════════════════════
# 格式验证器
# ═══════════════════════════════════════════

def 验证资产编号格式(资产类型: str, 资产编号: str) -> Optional[str]:
    """P19极简审计: 验证资产编号格式。返回 None = 通过，否则返回具体修复建议。"""
    编号 = 资产编号.strip()

    if not 编号:
        return "资产编号不能为空"

    if len(编号) < 2:
        return f"资产编号太短，至少2个字符（您输入了{len(编号)}个）"

    if len(编号) > 256:
        return "资产编号过长（不超过256字符）"

    # ── phone: IMEI 14-16位纯数字 ──
    if 资产类型 == "phone":
        cleaned = 编号.upper().replace("IMEI-", "").replace("-", "").strip()
        if not cleaned.isdigit():
            return "IMEI应为纯数字（可用*#06#在拨号盘查询），您输入了非数字字符"
        if len(cleaned) < 14:
            return f"IMEI至少14位数字，您输入了{len(cleaned)}位"
        if len(cleaned) > 16:
            return f"IMEI最多16位数字，您输入了{len(cleaned)}位"

    # ── vehicle: VIN ≥8位 ──
    elif 资产类型 == "vehicle":
        cleaned = 编号.replace("-", "").replace(" ", "")
        if len(cleaned) < 8:
            return f"VIN码至少8位（标准VIN为17位），您输入了{len(cleaned)}位"

    # ── patent: ≥6位 ──
    elif 资产类型 == "patent":
        if len(编号) < 6:
            return f"专利号至少6位，您输入了{len(编号)}位"

    # ── email: @ + 有效域名 ──
    elif 资产类型 == "email":
        if "@" not in 编号:
            return "邮箱需要包含@符号"
        parts = 编号.split("@")
        if len(parts) != 2 or "." not in parts[1]:
            return "邮箱域名无效，缺少顶级域（如 .com/.cn）"

    # ── domain: 必须有. ──
    elif 资产类型 == "domain":
        if "." not in 编号:
            return "域名需要包含顶级域（如 .com/.dev），不含 http://"

    # ── wallet: ≥26位 ──
    elif 资产类型 == "wallet":
        if len(编号) < 26:
            return f"钱包地址至少26位，您输入了{len(编号)}位"

    # ── gpg: hex至少8位 ──
    elif 资产类型 == "gpg":
        hex_part = 编号.replace(" ", "").upper()
        if not all(c in "0123456789ABCDEF" for c in hex_part):
            return "GPG指纹只能包含0-9和A-F"
        if len(hex_part) < 8:
            return f"GPG指纹至少8位十六进制，您输入了{len(hex_part)}位"

    # ── 社会贡献: 必须有证据URL或可追溯标识 ──
    elif 资产类型 in ("oss_code", "tech_doc", "oss_maintain"):
        if len(编号) < 4:
            return f"贡献证据太短，至少4个字符（建议填写PR链接或Commit哈希）"

    elif 资产类型 == "community":
        if len(编号) < 2:
            return f"社区服务记录太短，至少2个字符（建议填写平台+记录ID）"

    elif 资产类型 == "welfare":
        if len(编号) < 2:
            return f"公益记录太短，至少2个字符（建议填写活动名称+时间）"

    elif 资产类型 == "intl_bridge":
        if len(编号) < 4:
            return f"国际协作证据太短，至少4个字符（建议填写项目名称+参与角色）"

    return None


# ═══════════════════════════════════════════
# 公开/私有标记
# ═══════════════════════════════════════════

公开清单文件 = 注册表目录 / "public_registry.json"

def 加载公开清单() -> Dict[str, Any]:
    if 公开清单文件.exists():
        with open(公开清单文件, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def 保存公开清单(清单: Dict[str, Any]) -> None:
    注册表目录.mkdir(parents=True, exist_ok=True)
    with open(公开清单文件, "w", encoding="utf-8") as f:
        json.dump(清单, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# API 路由
# ═══════════════════════════════════════════

@app.get("/")
async def 首页():
    """返回 DNA 登记册 Web UI"""
    index_path = UI目录 / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "DNA Registry API is running", "version": "1.0.0"}


@app.get("/api/types")
async def 获取资产类型():
    """获取所有资产类型定义"""
    类型列表 = []
    for t, info in 资产类型表.items():
        类型列表.append({
            "type": t,
            "category": info["类别"],
            "name": info["名称"],
            "verification": info["验证方式"],
            "color": 类别色[info["类别"]],
        })
    return {"types": 类型列表, "total": len(类型列表)}


@app.post("/api/register")
async def api注册(req: 注册请求):
    """注册一条资产"""
    # 格式验证
    格式错误 = 验证资产编号格式(req.资产类型, req.资产编号)
    if 格式错误:
        raise HTTPException(status_code=400, detail=格式错误)

    ok, msg, dna = 注册资产(req.uid, req.资产类型, req.资产编号, req.标签, req.备注, req.验证状态)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    登记册 = 加载登记册(req.uid)
    master = 登记册.主DNA哈希 if 登记册 else ""

    return {
        "success": True,
        "message": msg,
        "dna": dna,
        "master_dna": master,
        "asset_type": req.资产类型,
        "asset_name": 资产类型表[req.资产类型]["名称"],
        "category": 资产类型表[req.资产类型]["类别"],
    }


@app.get("/api/list/{uid}")
async def api列表(uid: str):
    """获取某人完整资产清单"""
    登记册 = 加载登记册(uid)
    if 登记册 is None:
        return {"uid": uid, "exists": False, "assets": [], "master_dna": "", "total": 0}

    资产列表 = []
    for 类型, 条目列表 in 登记册.资产清单.items():
        info = 资产类型表.get(类型, {"名称": 类型, "类别": "未知"})
        for item in 条目列表:
            资产列表.append({
                "type": 类型,
                "name": info["名称"],
                "category": info["类别"],
                "category_color": 类别色.get(info["类别"], "⚪"),
                "hash": item.资产编号哈希,
                "dna": item.DNA码,
                "tags": item.资产标签,
                "status": item.验证状态,
                "registered_at": item.登记时间,
                "ganzhi": item.登记干支,
            })

    # 按类别排序
    资产列表.sort(key=lambda x: {"物理": 0, "虚拟": 1, "身份": 2, "社会": 3}.get(x["category"], 9))

    return {
        "uid": uid,
        "exists": True,
        "master_dna": 登记册.主DNA哈希,
        "version": 登记册.版本,
        "created_at": 登记册.创建时间,
        "updated_at": 登记册.更新时间,
        "total": len(资产列表),
        "physical": sum(1 for a in 资产列表 if a["category"] == "物理"),
        "virtual": sum(1 for a in 资产列表 if a["category"] == "虚拟"),
        "identity": sum(1 for a in 资产列表 if a["category"] == "身份"),
        "social": sum(1 for a in 资产列表 if a["category"] == "社会"),
        "assets": 资产列表,
    }


@app.get("/api/master/{uid}")
async def api主DNA(uid: str):
    """获取主DNA哈希"""
    ok, msg = 获取主DNA(uid)
    if not ok:
        raise HTTPException(status_code=404, detail=msg)
    return {"uid": uid, "master_dna": msg}


@app.get("/api/status/{uid}")
async def api状态(uid: str):
    """获取登记册状态摘要"""
    ok, msg = 获取状态(uid)
    return {"uid": uid, "status": msg, "has_registry": ok}


@app.post("/api/verify")
async def api验证(req: 验证请求):
    """验证资产归属"""
    登记册 = 加载登记册(req.uid)
    if 登记册 is None:
        return {
            "verified": False,
            "message": f"UID [{req.uid}] 无登记记录",
            "is_black_box": True,
            "detail": "无DNA登记 — 此物品未上牌·黑户·无溯源链",
        }

    ok, msg = 验证资产归属(req.uid, req.资产类型, req.资产编号, 登记册)
    return {
        "verified": ok,
        "message": msg,
        "is_black_box": not ok,
        "detail": "验证失败·此物品未登记 — 可能为黑户/被盗/剽窃 请谨慎交易" if not ok else "",
    }


@app.get("/api/public")
async def api公开清单():
    """获取公开登记清单（对外验证入口）"""
    清单 = 加载公开清单()
    return {"public_entries": 清单, "total": len(清单)}


@app.post("/api/toggle-public")
async def api切换公开(uid: str = Query(...), dna: str = Query(...)):
    """切换某DNA条目的公开/私有状态"""
    清单 = 加载公开清单()
    key = f"{uid}:{dna}"
    if key in 清单:
        del 清单[key]
        action = "已设为私有"
    else:
        登记册 = 加载登记册(uid)
        if 登记册 is None:
            raise HTTPException(status_code=404, detail="UID 无登记记录")
        # 验证 DNA 存在
        found = False
        for 条目列表 in 登记册.资产清单.values():
            for item in 条目列表:
                if item.DNA码 == dna:
                    found = True
                    break
        if not found:
            raise HTTPException(status_code=404, detail="DNA码不存在")
        清单[key] = {
            "uid": uid,
            "dna": dna,
            "public_at": __import__("datetime").datetime.now().isoformat(),
        }
        action = "已设为公开"

    保存公开清单(清单)
    return {"success": True, "action": action, "public_count": len(清单)}


# ═══════════════════════════════════════════
# 启动入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("🧬 龍魂统一DNA登记册 · Web API 启动")
    print(f"   本地: http://localhost:8778")
    print(f"   API:  http://localhost:8778/api/types")
    print(f"   前端: http://localhost:8778/")
    uvicorn.run(app, host="127.0.0.1", port=8778, log_level="info")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·壬申-DNA-REGISTRY-WEB-API-v1.0
