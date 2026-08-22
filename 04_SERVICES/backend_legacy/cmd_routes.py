#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·命令总目 API — 鲲鹏统一入口
DNA: #龍芯⚡️丙午·乙未·癸卯·戊午·䷚颐-CMD-ROUTES-v1.0-9A3F2B1C

所有 AI（CodeBuddy/Kimi/Ollama/任何国产AI）查询命令的统一入口。
部署在鲲鹏 9622 端口，通过 nginx 反代对外。

端点:
  GET /api/cmd          — 命令总目摘要 (JSON)
  GET /api/cmd/index.md — 完整 COMMAND_INDEX.md (Markdown raw)
  GET /api/cmd/quick    — 三秒速查表 (JSON)
  GET /api/cmd/ports    — 服务端口速查 (JSON)
  GET /api/cmd/category/{name} — 分类命令详情 (JSON)
  GET /api/cmd/search?q= — 搜索命令 (JSON)
"""

from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter(tags=["命令总目"])

# ── 命令总目数据（单一真相来源）──
# 新增/修改脚本时 → 同步更新此处 + 本地 .codebuddy/COMMAND_INDEX.md

COMMAND_DATA = {
    "version": "1.0",
    "updated": "2026-07-28",
    "dna": "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-COMMAND-INDEX-v1.0",
    "principle": "鲲鹏是唯一真实入口，Notion 是镜像",
    "quick": [
        {"action": "进菜单", "cmd": "lh", "note": "交互控制台，8大类"},
        {"action": "搜", "cmd": "lh search \"关键词\"", "note": "Bing→缓存→审计"},
        {"action": "做视频", "cmd": "lh video --script 稿.txt", "note": "v3.0·AI配图"},
        {"action": "做3D", "cmd": "lh 3d --input 图.png", "note": "图生三维"},
        {"action": "看状态", "cmd": "lh status", "note": "模型Val·引擎·告警"},
        {"action": "审计", "cmd": "lh audit", "note": "全系统安全"},
        {"action": "签名", "cmd": "python3 bin/lh_gpg_sign.py sign .", "note": "GPG分离签名"},
        {"action": "推远端", "cmd": "python3 bin/lh_auto_cannon.py", "note": "GitHub+Gitee+GitCode"},
        {"action": "同步鲲鹏", "cmd": "bash deploy/sync-to-kunpeng.sh", "note": "→ 119.13.90.27"},
        {"action": "SSH鲲鹏", "cmd": "ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27", "note": "密钥优先"},
    ],
    "categories": {
        "日常交互": {
            "desc": "日常最常用的交互命令",
            "commands": [
                {"cmd": "lh", "note": "交互控制台（8大类菜单）"},
                {"cmd": "lh --dashboard", "note": "人格仪表盘"},
                {"cmd": "lh --audit", "note": "一键审计"},
                {"cmd": "lh --push", "note": "推远端"},
                {"cmd": "lh --health", "note": "引擎健康"},
                {"cmd": "lh --console", "note": "Web操作台"},
            ]
        },
        "搜索 & 知识": {
            "desc": "搜索和知识查询",
            "commands": [
                {"cmd": "lh search \"关键词\"", "note": "→ bin/lh_search_engine.py"},
            ]
        },
        "多媒体": {
            "desc": "视频、3D等多媒体的生成和查看",
            "commands": [
                {"cmd": "lh video --script 稿.txt", "note": "→ bin/lh_video_studio.py"},
                {"cmd": "lh video --list", "note": "→ bin/lh_video_index.py"},
                {"cmd": "lh 3d --input 图.png", "note": "→ bin/lh_3d_pipeline.py"},
            ]
        },
        "审计 & 安全": {
            "desc": "安全审计、健康检查、自愈",
            "commands": [
                {"cmd": "lh audit", "note": "→ bin/lh_full_system_audit.py"},
                {"cmd": "python3 bin/lh_deben_audit.py scan", "note": "德本五问"},
                {"cmd": "python3 bin/lh_memory_load.py", "note": "焊死记忆加载"},
                {"cmd": "python3 bin/lh_system_eval.py", "note": "健康评分"},
                {"cmd": "python3 bin/lh_self-heal.py", "note": "自助修复"},
                {"cmd": "python3 bin/longhun_self_check_v1.0.py", "note": "系统自检"},
            ]
        },
        "GPG 签名": {
            "desc": "🔥焊死·所有发布前必须签名",
            "commands": [
                {"cmd": "python3 bin/lh_gpg_sign.py sign <路径>", "note": "签名"},
                {"cmd": "python3 bin/lh_gpg_sign.py sign --force .", "note": "强制全签"},
                {"cmd": "python3 bin/lh_gpg_sign.py verify <文件>", "note": "验证"},
                {"cmd": "python3 bin/lh_gpg_sign.py scan <目录>", "note": "扫描未签名"},
            ],
            "gpg_key": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        },
        "部署 & 同步": {
            "desc": "代码同步、部署、健康检查",
            "commands": [
                {"cmd": "bash deploy/sync-to-kunpeng.sh", "note": "代码同步鲲鹏"},
                {"cmd": "bash deploy/deploy-now.sh", "note": "一键部署"},
                {"cmd": "bash deploy/scripts/health_check.sh", "note": "鲲鹏健康检查(Bark)"},
                {"cmd": "bash deploy/scripts/monitor_setup.sh", "note": "systemd+监控"},
                {"cmd": "python3 bin/lh_auto_cannon.py", "note": "Git全量推送"},
            ]
        },
        "模型训练": {
            "desc": "LoRA训练、数据准备、模型运行",
            "commands": [
                {"cmd": "python3 bin/lh_lora_trainer_v4.py", "note": "MLX LoRA训练"},
                {"cmd": "python3 bin/lh_download_v40_bases.py", "note": "数据拉取"},
                {"cmd": "ollama run longhun-v3.7", "note": "主力模型(Qwen2.5-1.5B)"},
                {"cmd": "ollama run longhun-v4.0", "note": "新底座(Llama-3.1-8B)"},
            ]
        },
        "记忆 & 日志": {
            "desc": "记忆层查看和统计",
            "commands": [
                {"cmd": "lh memory --today", "note": "今日执行日志"},
                {"cmd": "lh memory --summary", "note": "记忆层统计"},
                {"cmd": "lh logs --tail 20", "note": "聚合日志"},
            ]
        },
        "运维": {
            "desc": "服务启停、定时任务、仪表盘",
            "commands": [
                {"cmd": "bash bin/start_all.sh", "note": "一键启动所有服务"},
                {"cmd": "bash bin/refresh-longhun.sh", "note": "刷新龍魂环境"},
                {"cmd": "lh schedule list", "note": "定时任务"},
                {"cmd": "lh web", "note": "仪表盘 → :9630"},
            ]
        },
    },
    "ports": [
        {"port": 9630, "service": "Web仪表盘", "location": "Mac"},
        {"port": 9631, "service": "搜索引擎", "location": "Mac"},
        {"port": 8766, "service": "知识中枢", "location": "Mac"},
        {"port": 8771, "service": "统一记忆", "location": "Mac"},
        {"port": 8773, "service": "统一记忆", "location": "鲲鹏"},
        {"port": 8781, "service": "军团指挥", "location": "Mac"},
        {"port": 8788, "service": "视频画廊", "location": "Mac"},
        {"port": 8899, "service": "价格审计", "location": "Mac"},
        {"port": 9622, "service": "龍魂统一后端(含命令总目)", "location": "鲲鹏"},
        {"port": 9677, "service": "蚁群HTTP", "location": "Mac"},
        {"port": 18775, "service": "底座痕迹采集", "location": "Mac"},
    ],
    "changelog": [
        {"date": "2026-07-28", "change": "命令总目 v1.0 上线鲲鹏", "affected": "全部"},
        {"date": "2026-07-28", "change": "GPG签名引擎上线", "affected": "lh_gpg_sign.py"},
        {"date": "2026-07-28", "change": "命令总目从本地迁至鲲鹏统一入口", "affected": "架构"},
    ],
}

# ── Markdown 内容（从 .codebuddy/COMMAND_INDEX.md 同步）──
CMD_INDEX_PATH = Path(__file__).resolve().parent.parent / ".codebuddy" / "COMMAND_INDEX.md"


def _load_markdown() -> str:
    """加载 COMMAND_INDEX.md 的原始 markdown 内容。"""
    if CMD_INDEX_PATH.exists():
        return CMD_INDEX_PATH.read_text(encoding="utf-8")
    return "# 命令总目暂未同步\n请将 COMMAND_INDEX.md 同步到鲲鹏的 .codebuddy/ 目录。\n"


# ═══════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════


@router.get("/cmd")
async def cmd_index():
    """命令总目完整摘要 (JSON)。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **COMMAND_DATA,
    }


@router.get("/cmd/index.md")
async def cmd_markdown():
    """完整 COMMAND_INDEX.md 原始内容。"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        content=_load_markdown(),
        media_type="text/markdown; charset=utf-8",
    )


@router.get("/cmd/quick")
async def cmd_quick():
    """三秒速查表。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": "龍魂·三秒速查",
        "commands": COMMAND_DATA["quick"],
    }


@router.get("/cmd/ports")
async def cmd_ports():
    """服务端口速查。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": "龍魂·服务端口",
        "ports": COMMAND_DATA["ports"],
    }


@router.get("/cmd/category/{name}")
async def cmd_category(name: str):
    """按分类查询命令详情。"""
    cat = COMMAND_DATA["categories"].get(name)
    if not cat:
        # 模糊匹配
        for key in COMMAND_DATA["categories"]:
            if name in key:
                cat = COMMAND_DATA["categories"][key]
                break
        if not cat:
            raise HTTPException(
                status_code=404,
                detail={
                    "ok": False,
                    "error": f"未知分类: {name}",
                    "available": list(COMMAND_DATA["categories"].keys()),
                },
            )
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": name,
        **cat,
    }


@router.get("/cmd/search")
async def cmd_search(q: str = Query(..., description="搜索关键词")):
    """搜索命令。在所有命令中模糊匹配。"""
    results = []
    keyword = q.lower()

    # 搜索快速表
    for item in COMMAND_DATA["quick"]:
        if keyword in item["action"] or keyword in item["cmd"].lower() or keyword in item.get("note", ""):
            results.append({"source": "quick", **item})

    # 搜索分类
    for cat_name, cat_data in COMMAND_DATA["categories"].items():
        for cmd in cat_data["commands"]:
            if (keyword in cmd["cmd"].lower() or
                keyword in cmd.get("note", "").lower() or
                keyword in cat_name.lower() or
                keyword in cat_data.get("desc", "").lower()):
                results.append({"source": cat_name, **cmd})

    # 搜索端口
    for port in COMMAND_DATA["ports"]:
        if (keyword in str(port["port"]) or
            keyword in port["service"].lower() or
            keyword in port["location"].lower()):
            results.append({"source": "ports", **port})

    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": q,
        "count": len(results),
        "results": results,
    }


@router.get("/cmd/categories")
async def cmd_categories():
    """列出所有分类名称。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "categories": list(COMMAND_DATA["categories"].keys()),
    }
