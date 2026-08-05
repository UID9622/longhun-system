#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊申·泽地萃-PROTOCOL-SERVER-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
🐉 龍魂 · 协议动态索引服务 v1.0

功能：
  1. 扫描 ~/longhun-system/01_protocols/ 所有 .md 文件
  2. 解析元数据（DNA、CONFIRM、Version、Status、Depends On等）
  3. 提供 REST API（/api/protocols, /api/protocols/{id}, /api/stats）
  4. 支持搜索、过滤、分页
  5. 自动增量刷新（每60秒）
  6. 手动刷新 /api/refresh

用法：
  python3 bin/lh_protocol_server.py [--port 8910] [--host 0.0.0.0]
  lh proto-serve --port 8910
"""

import os
import sys
import json
import re
import time
import threading
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import argparse

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
PROTOCOL_DIR = PROJECT_ROOT / "01_protocols"
SKILL_DIR = PROJECT_ROOT / "01_技能庫"
BIN_DIR = PROJECT_ROOT / "bin"
DATA_DIR = PROJECT_ROOT / "data"
CACHE_FILE = DATA_DIR / "protocol_cache.json"

# ============================================================
# 解析器
# ============================================================

def parse_markdown_metadata(content: str) -> Dict[str, Any]:
    """从 Markdown 内容中提取元数据"""
    metadata = {
        "title": "",
        "dna": "",
        "confirm": "",
        "version": "",
        "status": "active",
        "level": "",
        "category": "",
        "depends_on": [],
        "tags": [],
        "description": ""
    }

    lines = content.split("\n")

    # 检测 YAML frontmatter
    in_yaml = False
    yaml_lines = []
    for line in lines:
        if line.strip() == "---":
            in_yaml = not in_yaml
            continue
        if in_yaml:
            yaml_lines.append(line)

    for line in yaml_lines:
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == "title":
                metadata["title"] = val
            elif key == "DNA" or key == "dna":
                metadata["dna"] = val
            elif key == "CONFIRM" or key == "confirm":
                metadata["confirm"] = val
            elif key == "Version" or key == "version":
                metadata["version"] = val
            elif key == "Status" or key == "status":
                metadata["status"] = val
            elif key == "Level" or key == "level":
                metadata["level"] = val
            elif key == "Category" or key == "category":
                metadata["category"] = val
            elif key == "Depends On" or key == "depends_on":
                deps = [d.strip() for d in val.split(",") if d.strip()]
                metadata["depends_on"] = deps
            elif key == "Tags" or key == "tags":
                tags = [t.strip() for t in val.split(",") if t.strip()]
                metadata["tags"] = tags

    # 如果 title 为空，从第一行提取
    if not metadata["title"]:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                metadata["title"] = stripped[2:].strip()
                break

    # 从行内提取 DNA/CONFIRM
    if not metadata["dna"]:
        for line in lines:
            m = re.search(r'DNA:\s*(#龍芯[^\n]+)', line)
            if m:
                metadata["dna"] = m.group(1).strip()
                break
    if not metadata["confirm"]:
        for line in lines:
            m = re.search(r'(#CONFIRM[^\n]+)', line)
            if m:
                metadata["confirm"] = m.group(1).strip()
                break

    # 提取描述：第一个非空非标题非元数据行
    if not metadata["description"]:
        skip_prefixes = ("#", "-", "DNA:", "创建者:", "协议:", "CONFIRM:", "GPG:", "```")
        for line in lines:
            stripped = line.strip()
            if stripped and not any(stripped.startswith(p) for p in skip_prefixes):
                metadata["description"] = stripped[:200]
                break

    return metadata


# 类别关键词
CAT_KEYWORDS = {
    "governance": ["治理", "govern", "audit", "熔断", "GATE", "闸口", "德本", "底线",
                   "离火", "P05", "P13", "P15", "P72", "persona", "人格"],
    "security": ["安全", "security", "vuln", "漏洞", "威胁", "threat", "crypto",
                 "GPG", "签名", "防篡改", "encrypt", "渗透"],
    "privacy": ["隐私", "privacy", "数据", "data", "主权", "sovereignty", "个人信息"],
    "audit": ["审计", "audit", "三色", "three.color", "P05"],
    "deploy": ["部署", "deploy", "鲲鹏", "docker", "systemd", "launchd", "health"],
    "culture": ["文化", "culture", "道德经", "五行", "八卦", "洛书", "CNSH", "龙", "龍"],
    "skill": ["技能", "skill", "引擎", "engine", "pipeline", "router", "trainer",
              "detector", "orchestrator", "agent", "guard", "colony"],
    "visual": ["视觉", "visual", "颜色", "color", "渲染", "render", "面板",
               "portal", "dashboard", "动画"],
}

def detect_category(filepath: str, title: str) -> str:
    t = (filepath + " " + title).lower()
    for cat, kws in CAT_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in t:
                return cat
    return "other"

def detect_level(filepath: str, title: str) -> str:
    t = (filepath + " " + title).upper()
    if any(x in t for x in ["P0", "ETERNAL", "宪法", "永恒", "天条"]):
        return "P0"
    if any(x in t for x in ["L0", "NEURAL", "CNSH_SEMANTIC", "底座"]):
        return "L0"
    if any(x in t for x in ["V1.0", "V1.", "P1", "核心"]):
        return "L1"
    return "L2"


def scan_protocols() -> List[Dict]:
    """扫描协议目录，返回所有协议元数据"""
    protocols = []
    if not PROTOCOL_DIR.exists():
        return protocols

    for md_file in PROTOCOL_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            meta = parse_markdown_metadata(content)
            rel_path = str(md_file.relative_to(PROJECT_ROOT))

            meta["id"] = md_file.stem
            meta["path"] = rel_path
            meta["filename"] = md_file.name
            meta["hash"] = hashlib.md5(content.encode()).hexdigest()[:8]
            meta["size"] = md_file.stat().st_size
            meta["updated_at"] = datetime.fromtimestamp(
                md_file.stat().st_mtime
            ).isoformat()

            if not meta["level"]:
                meta["level"] = detect_level(rel_path, meta["title"])
            if not meta["category"]:
                meta["category"] = detect_category(rel_path, meta["title"])
            if not meta["status"]:
                meta["status"] = "active"

            protocols.append(meta)
        except Exception as e:
            print(f"⚠️ 解析失败 {md_file}: {e}")
            continue

    return protocols


def scan_root_docs() -> List[Dict]:
    """扫描根目录关键文档"""
    root_dirs = [
        PROJECT_ROOT,
        PROJECT_ROOT / ".codebuddy",
        PROJECT_ROOT / ".codebuddy" / "rules",
    ]
    root_files = []
    key_names = [
        "CONSTITUTION.md", "P0_ETERNAL_LOCK.md", "GOVERNANCE.md",
        "GENTLEMANS_PROTOCOL.md", "PRIVACY_POLICY.md", "AGENTS.md",
        "STATE.md", "MANIFESTO.md", "STANDARD.md", "SECURITY.md",
        "CODE_OF_CONDUCT.md", "TERMS_OF_SERVICE.md", "CHANGELOG.md",
        "ROADMAP.md", "README.md", "QUICKSTART.md", "INSTALL.md",
        "CONTRIBUTING.md", "ATTRIBUTION.md",
    ]
    codebuddy_key = [
        "COMMAND_INDEX.md", "CODEBUDDY.md", "cnsh_semantic_protocol.md",
        "longhun_neural_net.json",
    ]
    rules_key = [
        "ALIGNMENT-RULES-v2.2.md",
        "cloudbase-development-rules.md",
    ]

    for fname in key_names:
        fp = PROJECT_ROOT / fname
        if fp.exists():
            root_files.append({
                "id": fp.stem,
                "file": fname,
                "path": str(fp.relative_to(PROJECT_ROOT)),
                "title": fname,
                "level": detect_level(fname, ""),
                "category": "root",
                "size": fp.stat().st_size,
            })

    for fname in codebuddy_key:
        fp = PROJECT_ROOT / ".codebuddy" / fname
        if fp.exists():
            root_files.append({
                "id": fp.stem,
                "file": fname,
                "path": str(fp.relative_to(PROJECT_ROOT)),
                "title": fname,
                "level": "P0" if fname.endswith(".md") else "L0",
                "category": "codebuddy",
            })

    for fname in rules_key:
        fp = PROJECT_ROOT / ".codebuddy" / "rules" / fname
        if fp.exists():
            root_files.append({
                "id": fp.stem,
                "file": fname,
                "path": str(fp.relative_to(PROJECT_ROOT)),
                "title": fname,
                "level": "P0",
                "category": "rules",
            })

    return root_files


def scan_skills() -> List[Dict]:
    """扫描技能目录"""
    skills = []
    if not SKILL_DIR.exists():
        return skills
    for f in SKILL_DIR.rglob("*.md"):
        try:
            rel = str(f.relative_to(PROJECT_ROOT))
            skills.append({
                "id": f.stem,
                "file": f.name,
                "path": rel,
                "title": f.stem,
                "level": "L2",
                "category": "skill",
                "size": f.stat().st_size,
            })
        except:
            pass
    return skills


# ============================================================
# 缓存管理
# ============================================================

def load_cache() -> Dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(data: Dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="龍魂协议动态索引",
    description="动态扫描 01_protocols/ 目录，提供协议元数据 API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局缓存
protocol_cache = {
    "data": [],
    "roots": [],
    "skills": [],
    "last_scan": None,
    "hash": None
}


def refresh_cache():
    """刷新缓存（扫描目录）"""
    global protocol_cache
    protocols = scan_protocols()
    roots = scan_root_docs()
    skills = scan_skills()

    protocol_cache["data"] = protocols
    protocol_cache["roots"] = roots
    protocol_cache["skills"] = skills
    protocol_cache["last_scan"] = datetime.now().isoformat()
    protocol_cache["hash"] = hashlib.md5(
        json.dumps(protocols, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    # 保存到文件缓存
    save_cache({
        "protocols": protocols,
        "root_docs": roots,
        "skills": skills,
        "total_protocols": len(protocols),
        "total_root": len(roots),
        "total_skills": len(skills),
        "total_all": len(protocols) + len(roots) + len(skills),
        "last_scan": protocol_cache["last_scan"],
        "hash": protocol_cache["hash"]
    })

    print(f"🔄 协议缓存刷新: {len(protocols)} 协议 + {len(roots)} 根文档 + {len(skills)} 技能")


def periodic_refresh():
    """定时刷新（每60秒）"""
    while True:
        time.sleep(60)
        try:
            refresh_cache()
        except Exception as e:
            print(f"⚠️ 定时刷新失败: {e}")


# 启动时初始化
refresh_cache()
# 启动后台定时刷新线程
thread = threading.Thread(target=periodic_refresh, daemon=True)
thread.start()


# ============================================================
# API 端点
# ============================================================

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "protocols_count": len(protocol_cache["data"]),
        "roots_count": len(protocol_cache["roots"]),
        "skills_count": len(protocol_cache["skills"]),
        "last_scan": protocol_cache["last_scan"]
    }


@app.get("/api/stats")
async def stats():
    data = protocol_cache["data"]
    levels = {}
    categories = {}
    statuses = {}

    for p in data:
        lv = p.get("level", "other")
        levels[lv] = levels.get(lv, 0) + 1
        cat = p.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
        st = p.get("status", "active")
        statuses[st] = statuses.get(st, 0) + 1

    return {
        "total_protocols": len(data),
        "total_roots": len(protocol_cache["roots"]),
        "total_skills": len(protocol_cache["skills"]),
        "total_all": len(data) + len(protocol_cache["roots"]) + len(protocol_cache["skills"]),
        "levels": levels,
        "categories": categories,
        "statuses": statuses,
        "last_scan": protocol_cache["last_scan"]
    }


@app.get("/api/protocols")
async def list_protocols(
    q: Optional[str] = Query(None, description="搜索关键词"),
    level: Optional[str] = Query(None, description="按层级过滤"),
    category: Optional[str] = Query(None, description="按分类过滤"),
    status: Optional[str] = Query(None, description="按状态过滤"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    data = list(protocol_cache["data"])

    if q:
        q_lower = q.lower()
        data = [p for p in data if
                q_lower in p.get("title", "").lower() or
                q_lower in p.get("description", "").lower() or
                q_lower in p.get("dna", "").lower() or
                q_lower in p.get("filename", "").lower() or
                q_lower in p.get("path", "").lower()]

    if level:
        data = [p for p in data if p.get("level") == level]
    if category:
        data = [p for p in data if p.get("category") == category]
    if status:
        data = [p for p in data if p.get("status") == status]

    total = len(data)
    data = data[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": data,
        "last_scan": protocol_cache["last_scan"]
    }


@app.get("/api/roots")
async def list_roots():
    return {
        "data": protocol_cache["roots"],
        "last_scan": protocol_cache["last_scan"]
    }


@app.get("/api/skills")
async def list_skills(
    q: Optional[str] = Query(None, description="搜索关键词"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    data = list(protocol_cache["skills"])
    if q:
        q_lower = q.lower()
        data = [s for s in data if q_lower in s.get("file", "").lower() or q_lower in s.get("path", "").lower()]
    total = len(data)
    data = data[offset:offset + limit]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": data,
        "last_scan": protocol_cache["last_scan"]
    }


@app.get("/api/protocols/{protocol_id}")
async def get_protocol(protocol_id: str):
    for p in protocol_cache["data"]:
        if p.get("id") == protocol_id or p.get("filename") == protocol_id:
            file_path = PROTOCOL_DIR / p["path"]
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    p_resp = dict(p)
                    p_resp["content"] = content
                    return p_resp
                except:
                    p_resp = dict(p)
                    p_resp["content"] = ""
                    return p_resp
    raise HTTPException(status_code=404, detail="Protocol not found")


@app.post("/api/refresh")
async def refresh():
    refresh_cache()
    return {
        "status": "refreshed",
        "count": len(protocol_cache["data"])
    }


@app.get("/api/dashboard")
async def dashboard():
    """返回仪表盘所需的全量数据（前端一次请求）"""
    data = protocol_cache["data"]
    levels = {}
    categories = {}
    for p in data:
        lv = p.get("level", "other")
        levels[lv] = levels.get(lv, 0) + 1
        cat = p.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "protocols": data,
        "roots": protocol_cache["roots"],
        "skills": protocol_cache["skills"],
        "total_protocols": len(data),
        "total_roots": len(protocol_cache["roots"]),
        "total_skills": len(protocol_cache["skills"]),
        "total_all": len(data) + len(protocol_cache["roots"]) + len(protocol_cache["skills"]),
        "levels": levels,
        "categories": categories,
        "last_scan": protocol_cache["last_scan"]
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂协议动态索引服务")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8910, help="监听端口")
    parser.add_argument("--scan", action="store_true", help="只扫描并输出JSON，不启动服务")
    args = parser.parse_args()

    if args.scan:
        protocols = scan_protocols()
        print(json.dumps(protocols, ensure_ascii=False, indent=2))
        return

    print(f"🐉 龍魂协议动态索引服务 v1.0")
    print(f"📂 扫描目录: {PROTOCOL_DIR}")
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"📊 API: /api/protocols, /api/stats, /api/refresh, /api/dashboard")
    print(f"📋 API 文档: http://{args.host}:{args.port}/docs")
    print("-" * 50)
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
