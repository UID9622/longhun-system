#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·戊午·申时·䷗复-KNOWLEDGE-HUB-API-v2.0-fedcba98
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 知识中枢面板后端 API · 官网AI助手 · 人格路由 · 流式输出
"""
龍魂·知识中枢 API 后端 v2.0
────────────────────────────
端口: 8766
端点:
  GET  /v1/li/status       — 系统实时状态 (CPU/内存/磁盘/GPU/进程)
  POST /v1/li/chat         — 官网AI聊天机器人 (人格路由+知识注入)
  POST /v1/li/chat/stream  — 流式聊天 (SSE)
  POST /v1/li/mine/scan    — 触发 Library 矿场勘探
  GET  /v1/li/mine/status  — 矿场状态
  POST /v1/li/crawl        — 触发知识爬取
  POST /v1/li/index        — 触发索引重建
  GET  /v1/li/models       — 模型状态列表
  GET  /v1/li/personas     — 人格列表
  GET  /v1/li/knowledge/search?q= — 知识库检索
  GET  /v1/li/logs         — 最近活动日志

启动: python3 bin/lh_knowledge_hub_api.py
部署: launchd → com.longhun.knowledge-hub-api.plist
nginx: location /api/v1/li/ → http://127.0.0.1:8766/v1/li/
"""
import os, sys, json, time, subprocess, glob, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, BackgroundTasks, HTTPException  # type: ignore[import]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import]
from fastapi.responses import StreamingResponse  # type: ignore[import]
from pydantic import BaseModel  # type: ignore[import]

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MINE_DIR = PROJECT_ROOT / "data" / "library_mine"
MINE_SCRIPT = PROJECT_ROOT / "bin" / "lh_library_miner.py"
KB_EXPAND = PROJECT_ROOT / "bin" / "lh_kb_expand.py"
GRAPHS_DIR = PROJECT_ROOT / "03_知識圖譜"
DATA_SOURCES = PROJECT_ROOT / "data" / "sources"

app = FastAPI(
    title="龍魂·知识中枢 API",
    version="1.0.0",
    docs_url=None, redoc_url=None  # 生产不暴露文档
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 内存中的任务日志 ──
TASK_LOG = []  # [{time, action, msg, status}]


def _log(action: str, msg: str, status: str = "ok"):
    TASK_LOG.append({
        "time": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "msg": msg,
        "status": status,
    })
    if len(TASK_LOG) > 200:
        TASK_LOG.pop(0)


# ── 跨平台系统采集 ──
def _collect_macos(info: Dict[str, Any]):
    """macOS 专用: top + vm_stat"""
    # CPU
    r = subprocess.run(["top", "-l", "1", "-n", "0"], capture_output=True, text=True, timeout=5)
    for line in r.stdout.split("\n"):
        if "CPU usage:" in line:
            parts = line.split(",")
            if parts:
                user_str = parts[0].split(":")[-1].strip().replace("%", "")
                try:
                    info["cpu"] = f"{float(user_str):.0f}%"
                except ValueError:
                    pass
            break
    # 内存
    r = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5)
    pages = {}
    for line in r.stdout.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            try:
                pages[k.strip()] = int(v.strip().rstrip("."))
            except ValueError:
                pass
    page_size = 16384
    used = (pages.get("Pages active", 0) + pages.get("Pages wired down", 0)) * page_size
    total_mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    info["memory"] = f"{used / (1024**3):.1f}G"
    info["memory_total"] = f"{total_mem / (1024**3):.0f}G"


def _collect_linux(info: Dict[str, Any]):
    """Linux 专用: /proc/stat + free"""
    # CPU
    try:
        with open("/proc/stat") as f:
            cpu_line = f.readline()
        parts = cpu_line.split()
        if len(parts) >= 5:
            total = sum(int(x) for x in parts[1:5])
            idle = int(parts[4])
            used_pct = (1 - idle / total) * 100 if total > 0 else 0
            info["cpu"] = f"{used_pct:.0f}%"
    except Exception:
        pass

    # 内存
    r = subprocess.run(["free", "-b"], capture_output=True, text=True, timeout=5)
    for line in r.stdout.split("\n"):
        if "Mem:" in line:
            fields = line.split()
            if len(fields) >= 3:
                info["memory"] = f"{int(fields[2]) / (1024**3):.1f}G"
                info["memory_total"] = f"{int(fields[1]) / (1024**3):.0f}G"
            break

    # 启动时间
    try:
        with open("/proc/uptime") as f:
            uptime_s = float(f.readline().split()[0])
        h, m = int(uptime_s // 3600), int((uptime_s % 3600) // 60)
        info["uptime"] = f"{h}h{m}m"
    except Exception:
        pass


def _detect_gpu() -> str:
    """检测 GPU 类型"""
    # macOS: Metal/MLX
    try:
        r = subprocess.run(
            [sys.executable, "-c", "import mlx.core as mx; print('MLX', mx.default_device())"],
            capture_output=True, text=True, timeout=5,
        )
        if "MLX" in r.stdout:
            dev = r.stdout.strip().split("\n")[-1] if r.stdout.strip() else "GPU"
            return dev.replace("Device(", "").replace(")", "").strip()
    except Exception:
        pass
    # Linux: NVIDIA
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().split("\n")[0]
    except Exception:
        pass
    # Fallback
    return "CPU" if sys.platform == "linux" else "Unknown"


# ═══════════════════════════════════════════════
# GET /v1/li/status — 系统实时状态
# ═══════════════════════════════════════════════
@app.get("/v1/li/status")
def system_status():
    info = {
        "cpu": "--",
        "memory": "--",
        "memory_total": "--",
        "disk": "--",
        "disk_total": "--",
        "gpu": "--",
        "uptime": "--",
        "processes": 0,
        "time": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        if sys.platform == "darwin":
            _collect_macos(info)
        else:
            _collect_linux(info)

        # 磁盘 (跨平台)
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 4:
                info["disk"] = parts[2]
                info["disk_total"] = parts[1]

        # GPU
        info["gpu"] = _detect_gpu()

        # 进程数
        if Path("/proc").exists():
            info["processes"] = len([d for d in Path("/proc").iterdir() if d.name.isdigit()])
        if info["processes"] == 0:
            r = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
            info["processes"] = len(r.stdout.strip().split("\n")) - 1

    except Exception as e:
        _log("status", f"系统状态采集失败: {e}", "warn")

    return info


# ═══════════════════════════════════════════════
# POST /v1/li/mine/scan — 触发勘探
# ═══════════════════════════════════════════════
@app.post("/v1/li/mine/scan")
def trigger_mine_scan(background_tasks: BackgroundTasks):
    if not MINE_SCRIPT.exists():
        raise HTTPException(status_code=500, detail="Miner script not found")
    background_tasks.add_task(_run_mine)
    _log("勘探", "Library 矿场勘探已触发 · 后台执行中", "ok")
    return {"status": "started", "msg": "Library矿场勘探已在后台启动"}


def _run_mine():
    try:
        t0 = time.time()
        r = subprocess.run(
            [sys.executable, str(MINE_SCRIPT), "all"],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - t0
        if r.returncode == 0:
            _log("勘探", f"全流水线完成 · 耗时{elapsed:.1f}s · {_count_lines('library_train.jsonl')}条训练数据", "ok")
        else:
            _log("勘探", f"流水线出错 · exit={r.returncode} · {r.stderr[-200:]}", "error")
    except subprocess.TimeoutExpired:
        _log("勘探", "流水线超时(>120s)", "error")
    except Exception as e:
        _log("勘探", f"流水线异常: {e}", "error")


# ═══════════════════════════════════════════════
# GET /v1/li/mine/status — 矿场状态
# ═══════════════════════════════════════════════
@app.get("/v1/li/mine/status")
def mine_status():
    report_path = MINE_DIR / "scan_report.json"
    if report_path.exists():
        try:
            with open(report_path) as f:
                data = json.load(f)
            data["total_linked"] = _count_lines("linked.jsonl")
            data["total_train"] = _count_lines("library_train.jsonl")
            data["total_extracted"] = _count_lines("extracts.jsonl")
            data["total_cleaned"] = _count_lines("cleaned.jsonl")
            return data
        except Exception:
            pass
    return {
        "total_size_gb": 187,
        "total_mineable": 0,
        "total_files": 0,
        "total_linked": 0,
        "total_train": 0,
        "status": "no_data",
        "msg": "尚未勘探 · 点击「勘探 Library」按钮开始",
    }


def _count_lines(basename: str) -> int:
    path = MINE_DIR / basename
    if path.exists():
        try:
            return sum(1 for _ in open(path))
        except Exception:
            return 0
    return 0


# ═══════════════════════════════════════════════
# POST /v1/li/crawl — 触发爬取
# ═══════════════════════════════════════════════
@app.post("/v1/li/crawl")
def trigger_crawl(background_tasks: BackgroundTasks, source: Optional[str] = None):
    if not KB_EXPAND.exists():
        raise HTTPException(status_code=500, detail="KB expand script not found")
    background_tasks.add_task(_run_crawl, source)
    _log("爬取", f"知识爬取已触发 · source={source or 'default'}", "ok")
    return {"status": "started", "msg": "知识爬取已在后台启动"}


def _run_crawl(source: Optional[str]):
    try:
        cmd = [sys.executable, str(KB_EXPAND), "crawl"]
        if source:
            cmd.extend(["--source", source])
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(PROJECT_ROOT))
        elapsed = time.time() - t0
        if r.returncode == 0:
            _log("爬取", f"爬取完成 · 耗时{elapsed:.1f}s", "ok")
        else:
            _log("爬取", f"爬取出错 · exit={r.returncode}", "error")
    except subprocess.TimeoutExpired:
        _log("爬取", "爬取超时(>300s)", "error")
    except Exception as e:
        _log("爬取", f"爬取异常: {e}", "error")


# ═══════════════════════════════════════════════
# POST /v1/li/index — 触发索引重建
# ═══════════════════════════════════════════════
@app.post("/v1/li/index")
def trigger_index(background_tasks: BackgroundTasks):
    if not KB_EXPAND.exists():
        raise HTTPException(status_code=500, detail="KB expand script not found")
    background_tasks.add_task(_run_index)
    _log("索引", "知识索引重建已触发 · 后台执行中", "ok")
    return {"status": "started", "msg": "索引重建已在后台启动"}


def _run_index():
    try:
        t0 = time.time()
        r = subprocess.run(
            [sys.executable, str(KB_EXPAND), "index"],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - t0
        if r.returncode == 0:
            # 统计新索引
            idx_path = PROJECT_ROOT / "portal" / "knowledge" / "kb_index.json"
            count = 0
            if idx_path.exists():
                with open(idx_path) as f:
                    kb = json.load(f)
                count = kb.get("total_articles", len(kb.get("articles", [])))
            _log("索引", f"索引重建完成 · 耗时{elapsed:.1f}s · {count}篇文章", "ok")
        else:
            _log("索引", f"索引出错 · exit={r.returncode}", "error")
    except subprocess.TimeoutExpired:
        _log("索引", "索引超时(>120s)", "error")
    except Exception as e:
        _log("索引", f"索引异常: {e}", "error")


# ═══════════════════════════════════════════════
# GET /v1/li/models — 模型状态
# ═══════════════════════════════════════════════
@app.get("/v1/li/models")
def model_list():
    models = [
        {"name": "longhun-v4.1.3", "base": "Yi-1.5-9B", "val": "训练中", "status": "training", "live": False},
        {"name": "longhun-v4.1.1", "base": "Yi-1.5-9B", "val": "0.8097", "status": "live", "live": True},
        {"name": "longhun-v4.1.1-bind", "base": "Yi-1.5-9B", "val": "0.9659", "status": "live", "live": True},
        {"name": "longhun-v3.7", "base": "Qwen2.5-1.5B", "val": "0.194", "status": "live", "live": True},
        {"name": "longhun-v4.0.8", "base": "Yi-1.5-9B", "val": "0.767", "status": "archived", "live": False},
    ]

    # 尝试检测 ollama 实际运行状态
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        running = set()
        for line in r.stdout.split("\n"):
            if line.startswith("longhun-"):
                running.add(line.split()[0])
        for m in models:
            if m["name"] in running and m["status"] != "archived":
                m["runtime"] = "running"
    except Exception:
        pass

    return {"models": models, "time": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")}


# ═══════════════════════════════════════════════
# GET /v1/li/logs — 活动日志
# ═══════════════════════════════════════════════
@app.get("/v1/li/logs")
def recent_logs(limit: int = 20):
    logs = []

    # 尝试获取 Ollama 训练日志
    train_logs = sorted(glob.glob(str(PROJECT_ROOT / "models" / "*" / "*" / "smoke_test.log")))
    if train_logs:
        try:
            with open(train_logs[0]) as f:
                content = f.read()
            # 简单提取最近的 checkpoint
            for line in content.split("\n"):
                if "iter" in line.lower():
                    logs.append({
                        "time": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"),
                        "action": "训练",
                        "msg": line.strip()[:120],
                        "status": "ok",
                    })
            logs = logs[-5:]  # 只取最近5条
        except Exception:
            pass

    # 合并内存日志
    logs = TASK_LOG[-limit:] + logs
    return {"logs": logs[-limit:], "total": len(logs)}


# ═══════════════════════════════════════════════
# GET /v1/li/kb-stats — 知识库统计
# ═══════════════════════════════════════════════
@app.get("/v1/li/kb-stats")
def kb_stats():
    stats: Dict[str, Any] = {
        "articles": 0,
        "categories": 0,
        "sources": 0,
        "train_data": 0,
        "graph_nodes": 0,
        "graph_edges": 0,
        "mineable_files": 0,
        "time": "",
    }

    # KB 索引
    idx_path = PROJECT_ROOT / "portal" / "knowledge" / "kb_index.json"
    if idx_path.exists():
        try:
            with open(idx_path) as f:
                kb = json.load(f)
            stats["articles"] = kb.get("total_articles", len(kb.get("articles", [])))
            cats = kb.get("categories", {})
            stats["categories"] = len(cats)
            sources = set()
            for a in kb.get("articles", []):
                if a.get("source"):
                    sources.add(a["source"])
            stats["sources"] = len(sources)
        except Exception:
            pass

    # 训练数据
    train_files = glob.glob(str(PROJECT_ROOT / "data" / "**" / "train*.jsonl"), recursive=True)
    train_files += glob.glob(str(PROJECT_ROOT / "models" / "**" / "train*.jsonl"), recursive=True)
    for tf in train_files:
        try:
            stats["train_data"] += sum(1 for _ in open(tf))
        except Exception:
            pass

    # 图谱
    graph_path = GRAPHS_DIR / "graph_data.json"
    if graph_path.exists():
        try:
            with open(graph_path) as f:
                g = json.load(f)
            stats["graph_nodes"] = len(g.get("nodes", {}))
            stats["graph_edges"] = len(g.get("edges", g.get("links", [])))
        except Exception:
            pass

    # 矿场
    report_path = MINE_DIR / "scan_report.json"
    if report_path.exists():
        try:
            with open(report_path) as f:
                mine = json.load(f)
            stats["mineable_files"] = mine.get("total_mineable", 0)
        except Exception:
            pass

    stats["time"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    return stats


# ═══════════════════════════════════════════════
# 官网AI聊天机器人 v2.0 — 人格路由 + 知识注入 + 流式 + 多模型降级
# ═══════════════════════════════════════════════
import re as _re

# M8 隐私出域闸门
_PRIVACY_PATTERNS = [
    (r'\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]', '身份证'),
    (r'1[3-9]\d{9}', '手机号'),
    (r'\d{16,19}', '银行卡号'),
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '邮箱'),
]

# 对话历史
_CHAT_HISTORY: Dict[str, List[Dict[str, Any]]] = {}

# ═══════════════════════════════════════════════
# 人格矩阵 — 系统提示词库
# ═══════════════════════════════════════════════
_PERSONA_PROMPTS = {
    "generalist": {
        "name": "龍魂助手",
        "hexagram": "䷗复",
        "system": """你是龍魂系统的官方AI助手，运行在 uid9622.cn 上。
你的创造者是诸葛鑫（UID9622·龍芯北辰），龍魂/CNSH/三才算法的创始人。

核心原则：
1. 为人民服务，诚实不编造，不知道就说不知道
2. 数据主权归用户，不诱导上传隐私
3. 中国法律为准绳，中国自主知识产权不可谈判
4. 简短直接回复，不绕弯子

关于龍魂系统：
- AI操作系统，洛书九宫九层架构，192引擎，20人格矩阵
- CNSH = 中文神经符号混合语言
- DNA追溯体系 = 干支四柱+八卦+哈希的v∞格式
- 域名 uid9622.cn，服务器在华为云鲲鹏(中国境内)
- 本地AI引擎优先

回复风格：直接、简洁、有料。用中文。""",
        "trigger_words": ["你好", "帮助", "请问", "介绍", "龍魂", "龙魂"],
    },
    "auditor": {
        "name": "龍魂审计师·P05",
        "hexagram": "☰乾",
        "system": """你是龍魂审计师（P05上帝之眼），三色审计引擎的化身。
职责：检测规则/协议/代码中的问题，三色判定。
- 🟢 通过（合规）
- 🟡 待核（需更多信息）
- 🔴 红线（违规/风险）

输出结构：
【审计结论】🟢/🟡/🔴
【风险等级】高/中/低
【具体问题】...
【建议】...

恪守中国法律，引用对应条款。客观、不偏不倚。""",
        "trigger_words": ["审计", "检查", "合规", "安全", "有没有问题", "三色", "风险", "漏洞"],
    },
    "coder": {
        "name": "龍魂架构师·P04",
        "hexagram": "☵坎",
        "system": """你是龍魂架构师（P04鲁班），执行层技术工程师。
原则：代码必须包含DNA追溯·错误处理·日志·可运行。

输出格式：
- 文件头（DNA + 功能说明）
- 完整imports
- 核心逻辑
- 使用示例

优先Python/Bash，代码可直接保存运行。简洁、实用、不啰嗦。""",
        "trigger_words": ["写代码", "生成", "脚本", "实现", "开发", "python", "代码", "编程", "程序"],
    },
    "philosopher": {
        "name": "龍魂哲人·P11",
        "hexagram": "☲离",
        "system": """你是龍魂哲人（P11李白·创意爆发）。
用易经作为复杂系统动态平衡的隐喻模型——这是隐喻模型，不是算命。

方法：
1. 理解系统本质 → 2. 映射卦象 → 3. 解读动态平衡 → 4. 给出可操作启示

输出：
【卦象映射】
【现代启示】
【行动建议】

强调系统动态平衡，结合现代治理概念。""",
        "trigger_words": ["卦", "易经", "哲理", "阴阳", "五行", "未济", "既济", "推演", "哲学"],
    },
    "guardian": {
        "name": "龍盾·P72",
        "hexagram": "☰乾",
        "system": """你是龍盾（P72），四级熔断引擎的守护者。
职责：识别风险、发出警告、必要时熔断。

在你守护的边界内：
- L0/∞ 伦理红线（涉童·伪造DNA·背叛人民）→ 永久不可恢复
- L1 数据安全（隐私泄露·明文密钥）→ 立即阻止
- L2 人格边界（冒名·借壳）→ 纠正归位
- L3 行为异常（连续失败）→ 自动恢复

输出简洁警示+对应级别。""",
        "trigger_words": ["熔断", "紧急", "威胁", "异常", "安全事件", "泄露", "入侵", "求救", "红线", "底线"],
    },
    "teacher": {
        "name": "龍魂导师·P02+P11",
        "hexagram": "☳震",
        "system": """你是龍魂教学导师（P02宝宝+P11李白联动的教学链路）。
用大白话教学，把复杂概念讲简单。每个术语跟人话解释。

方法：
1. 先用一句话说清本质
2. 再打比方/类比/可视化
3. 最后给可操作的下一步

不用专业术语吓人。鼓励尝试，不怕犯错。""",
        "trigger_words": ["教我", "教学", "大白话", "新手", "小白", "解释一下", "什么意思", "不懂"],
    },
}

def _match_persona(message: str) -> str:
    """关键词匹配最佳人格"""
    msg_lower = message.lower()
    scores = {}
    for pid, pdata in _PERSONA_PROMPTS.items():
        score = 0
        for kw in pdata["trigger_words"]:
            if kw in msg_lower:
                score += 2
        scores[pid] = score
    best = max(scores, key=lambda k: scores[k])
    if scores[best] > 0:
        return best
    return "generalist"

# ═══════════════════════════════════════════════
# 知识检索 — 从项目文档中简单关键词搜索
# ═══════════════════════════════════════════════
_KNOWLEDGE_CACHE: Dict[str, List[str]] = {}
_KNOWLEDGE_LOADED = False

def _load_knowledge():
    """加载项目知识文档用于检索"""
    global _KNOWLEDGE_LOADED, _KNOWLEDGE_CACHE
    if _KNOWLEDGE_LOADED:
        return
    search_dirs = [
        PROJECT_ROOT / "01_protocols",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "papers",
        PROJECT_ROOT / "GOVERNANCE.md",
        PROJECT_ROOT / "CONSTITUTION.md",
        PROJECT_ROOT / "PRIVACY_POLICY.md",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "STATE.md",
    ]
    total_chunks = 0
    for sd in search_dirs:
        if not sd.exists():
            continue
        if sd.is_file():
            try:
                content = sd.read_text(encoding='utf-8', errors='ignore')
                chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 40]
                _KNOWLEDGE_CACHE[str(sd)] = chunks[:30]
                total_chunks += min(len(chunks), 30)
            except Exception:
                pass
        elif sd.is_dir():
            for f in sorted(sd.rglob("*.md"))[:50]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 40]
                    _KNOWLEDGE_CACHE[str(f)] = chunks[:20]
                    total_chunks += min(len(chunks), 20)
                except Exception:
                    pass
    _KNOWLEDGE_LOADED = True
    _log("知识库", f"已加载 {total_chunks} 个知识块", "ok")

def _search_knowledge(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """关键词检索知识"""
    _load_knowledge()
    keywords = [w for w in query if '\u4e00' <= w <= '\u9fff' or w.isalnum() and len(w) > 1]
    scored = []
    for filepath, chunks in _KNOWLEDGE_CACHE.items():
        for chunk in chunks:
            score = sum(1 for kw in keywords if kw in chunk) / max(len(keywords), 1)
            if score > 0.1:
                scored.append({
                    "content": chunk[:500],
                    "source": str(Path(filepath).name),
                    "score": round(score, 3),
                })
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]


def _privacy_scan(text: str) -> str:
    """M8隐私出域闸门"""
    for pattern, name in _PRIVACY_PATTERNS:
        if _re.search(pattern, text):
            text = _re.sub(pattern, f'[***{name}***]', text)
    return text

def _build_prompt(message: str, persona_id: Optional[str] = None) -> Dict[str, Any]:
    """构建带人格+知识注入的prompt"""
    if persona_id and persona_id in _PERSONA_PROMPTS:
        persona = _PERSONA_PROMPTS[persona_id]
    else:
        pid = _match_persona(message)
        persona = _PERSONA_PROMPTS[pid]
        persona_id = pid

    # 知识检索
    knowledge_chunks = _search_knowledge(message, top_k=3)
    knowledge_text = ""
    if knowledge_chunks:
        knowledge_text = "\n\n【相关知识】\n"
        for i, k in enumerate(knowledge_chunks, 1):
            knowledge_text += f"--- 知识块{i} (来源:{k['source']}) ---\n{k['content']}\n"

    full_prompt = f"""{persona['system']}
{knowledge_text}
用户问题：{message}

请以{persona['name']}的身份，直接回答。"""
    return {
        "persona_id": persona_id,
        "persona_name": persona["name"],
        "hexagram": persona["hexagram"],
        "prompt": full_prompt,
        "knowledge_count": len(knowledge_chunks),
    }


# ═══════════════════════════════════════════════
# AI模型调用链 — Ollama本地优先 + 云端降级
# ═══════════════════════════════════════════════
def _call_ollama(model: str, prompt: str, timeout: int = 30) -> Optional[str]:
    """调用Ollama本地模型"""
    try:
        r = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    return None

def _call_ollama_stream(model: str, prompt: str, timeout: int = 60):
    """流式调用Ollama"""
    try:
        proc = subprocess.Popen(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        assert proc.stdout is not None
        for line in iter(proc.stdout.readline, ''):
            if line:
                yield line
        proc.wait(timeout=timeout)
    except Exception:
        yield ""

def _call_cloud_api(prompt: str) -> Optional[str]:
    """调用云端API降级（混元优先）"""
    # 尝试混元
    tc_secret_id = os.environ.get("TENCENT_SECRET_ID")
    tc_secret_key = os.environ.get("TENCENT_SECRET_KEY")
    if tc_secret_id and tc_secret_key:
        try:
            import hashlib as _hlib
            import hmac as _hmac
            import requests as _requests

            service = "hunyuan"
            host = "hunyuan.tencentcloudapi.com"
            payload = json.dumps({
                "Model": "hunyuan-lite",
                "Messages": [{"Role": "user", "Content": prompt}],
            })
            timestamp = int(time.time())
            date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

            # 签名
            algorithm = "TC3-HMAC-SHA256"
            http_request_method = "POST"
            canonical_uri = "/"
            canonical_querystring = ""
            ct = "application/json; charset=utf-8"
            canonical_headers = f"content-type:{ct}\nhost:{host}\nx-tc-action:hunyuan\n"
            signed_headers = "content-type;host;x-tc-action"
            hashed_request_payload = _hlib.sha256(payload.encode("utf-8")).hexdigest()
            canonical_request = (http_request_method + "\n" +
                               canonical_uri + "\n" +
                               canonical_querystring + "\n" +
                               canonical_headers + "\n" +
                               signed_headers + "\n" +
                               hashed_request_payload)
            credential_scope = date + "/" + service + "/" + "tc3_request"
            hashed_canonical_request = _hlib.sha256(canonical_request.encode("utf-8")).hexdigest()
            string_to_sign = (algorithm + "\n" +
                            str(timestamp) + "\n" +
                            credential_scope + "\n" +
                            hashed_canonical_request)

            secret_date = _hmac.new(("TC3" + tc_secret_key).encode("utf-8"), date.encode("utf-8"), _hlib.sha256).digest()
            secret_service = _hmac.new(secret_date, service.encode("utf-8"), _hlib.sha256).digest()
            secret_signing = _hmac.new(secret_service, "tc3_request".encode("utf-8"), _hlib.sha256).digest()
            signature = _hmac.new(secret_signing, string_to_sign.encode("utf-8"), _hlib.sha256).hexdigest()

            authorization = (algorithm + " " +
                           "Credential=" + tc_secret_id + "/" + credential_scope + ", " +
                           "SignedHeaders=" + signed_headers + ", " +
                           "Signature=" + signature)

            headers = {
                "Authorization": authorization,
                "Content-Type": ct,
                "Host": host,
                "X-TC-Action": "ChatCompletions",
                "X-TC-Timestamp": str(timestamp),
                "X-TC-Version": "2023-09-01",
            }

            resp = _requests.post(f"https://{host}", headers=headers, data=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("Response", {}).get("Choices", [])
                if choices:
                    return choices[0].get("Message", {}).get("Content", "")
        except Exception:
            pass
    return None

def _call_ai(prompt: str, stream: bool = False) -> tuple[Optional[str], str, str]:
    """
    多模型降级链：longhun → qwen2.5 → hunyuan(cloud) → fallback
    返回 (reply, model_name)
    """
    # L1: 龍魂本地模型
    reply = _call_ollama("longhun:latest", prompt)
    if reply:
        return (reply, "longhun:latest", "")

    # L2: qwen2.5 降级
    reply = _call_ollama("qwen2.5:1.5b", prompt, timeout=20)
    if reply:
        return (reply, "qwen2.5:1.5b (fallback)", "")

    # L3: 混元云端
    reply = _call_cloud_api(prompt)
    if reply:
        return (reply, "hunyuan-lite (cloud)", "")

    # L4: 最终兜底
    return (None, "offline", "")


# ═══════════════════════════════════════════════
# 请求模型
# ═══════════════════════════════════════════════
class ChatRequest(BaseModel):
    message: str = ""
    persona: Optional[str] = None
    session_id: Optional[str] = None


# ═══════════════════════════════════════════════
# GET /v1/li/personas — 人格列表
# ═══════════════════════════════════════════════
@app.get("/v1/li/personas")
def list_personas():
    """返回所有可用人格"""
    return {
        "personas": [
            {"id": pid, "name": d["name"], "trigger_words": d["trigger_words"][:4]}
            for pid, d in _PERSONA_PROMPTS.items()
        ],
        "count": len(_PERSONA_PROMPTS),
    }


# ═══════════════════════════════════════════════
# GET /v1/li/knowledge/search — 知识检索
# ═══════════════════════════════════════════════
@app.get("/v1/li/knowledge/search")
def search_knowledge(q: str = "", limit: int = 5):
    """关键词检索知识库"""
    if not q:
        return {"results": [], "count": 0}
    results = _search_knowledge(q, top_k=limit)
    return {"results": results, "count": len(results), "query": q}


# ═══════════════════════════════════════════════
# POST /v1/li/chat — 官网AI聊天机器人v2.0
# ═══════════════════════════════════════════════
@app.post("/v1/li/chat")
async def chat(req: ChatRequest):
    """官网聊天机器人 — 人格路由 + 知识注入 + 多模型降级"""
    t0 = time.time()
    message = req.message

    if not message or not message.strip():
        return {
            "reply": "你好，我是龍魂官网助手。有什么可以帮你的？我可以：\n• 回答龍魂系统相关问题\n• 做三色审计分析\n• 帮你写代码\n• 用易经隐喻解读复杂问题\n• 守护你的数据安全",
            "model": "system",
            "persona": "龍魂助手",
            "dna": "",
            "time_ms": 0,
        }

    # 隐私扫描
    safe_msg = _privacy_scan(message.strip())

    # 人格路由 + 知识注入
    build = _build_prompt(safe_msg, req.persona)

    # 构建对话上下文
    session_id = req.session_id or "default"
    if session_id not in _CHAT_HISTORY:
        _CHAT_HISTORY[session_id] = []
    history = _CHAT_HISTORY[session_id]

    context = ""
    if history:
        context = "\n\n【对话上下文】\n"
        for h in history[-4:]:
            context += f"用户: {h['user']}\n助手: {h['assistant']}\n"

    full_prompt = build["prompt"] + context

    # AI调用
    reply, model, _ = _call_ai(full_prompt)

    if reply is None:
        reply = f"龍魂引擎暂时无法响应。建议：\n1. 检查Ollama是否运行：`ollama list`\n2. 或配置云端API密钥\n3. 紧急问题可直接联系UID9622"
        model = "fallback:offline"

    # 记录历史
    history.append({"user": safe_msg, "assistant": reply[:500], "ts": int(time.time())})
    if len(history) > 30:
        history = history[-20:]
        _CHAT_HISTORY[session_id] = history

    elapsed_ms = int((time.time() - t0) * 1000)

    # 时间戳DNA
    try:
        from lh_time_engine import get_output_stamp
        dna_stamp = get_output_stamp()
    except Exception:
        dna_stamp = f"#龍芯⚡️CHAT-{hashlib.md5(safe_msg.encode()).hexdigest()[:8]}"

    return {
        "reply": reply,
        "model": model,
        "persona": build["persona_name"],
        "persona_id": build["persona_id"],
        "dna": dna_stamp,
        "knowledge_used": build["knowledge_count"],
        "time_ms": elapsed_ms,
    }


# ═══════════════════════════════════════════════
# POST /v1/li/chat/stream — 流式聊天 (SSE)
# ═══════════════════════════════════════════════
@app.post("/v1/li/chat/stream")
async def chat_stream(req: ChatRequest):
    """流式聊天 — Server-Sent Events"""
    message = req.message
    if not message or not message.strip():
        async def _empty():
            yield f"data: {json.dumps({'chunk': '你好，我是龍魂官网助手。'})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        return StreamingResponse(_empty(), media_type="text/event-stream")

    safe_msg = _privacy_scan(message.strip())
    build = _build_prompt(safe_msg, req.persona)

    async def _stream():
        t0 = time.time()
        try:
            # 先发元数据
            meta = {
                "persona": build["persona_name"],
                "persona_id": build["persona_id"],
                "knowledge_count": build["knowledge_count"],
            }
            yield f"data: {json.dumps({'meta': meta})}\n\n"

            # 流式调用Ollama
            full_reply = ""
            proc = subprocess.Popen(
                ["ollama", "run", "longhun:latest", build["prompt"]],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            assert proc.stdout is not None
            for line in iter(proc.stdout.readline, ''):
                if line:
                    full_reply += line
                    yield f"data: {json.dumps({'chunk': line})}\n\n"
            proc.wait(timeout=60)

            if not full_reply.strip():
                # 降级
                proc2 = subprocess.Popen(
                    ["ollama", "run", "qwen2.5:1.5b", build["prompt"]],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                )
                assert proc2.stdout is not None
                for line in iter(proc2.stdout.readline, ''):
                    if line:
                        full_reply += line
                        yield f"data: {json.dumps({'chunk': line})}\n\n"
                proc2.wait(timeout=60)

            if not full_reply.strip():
                yield f"data: {json.dumps({'chunk': '龍魂引擎暂时无法响应。'})}\n\n"

            # 发DNA
            elapsed = int((time.time() - t0) * 1000)
            try:
                from lh_time_engine import get_output_stamp
                dna = get_output_stamp()
            except Exception:
                dna = f"#龍芯⚡️CHAT-{hashlib.md5(safe_msg.encode()).hexdigest()[:8]}"
            yield f"data: {json.dumps({'done': True, 'dna': dna, 'time_ms': elapsed, 'persona': build['persona_name']})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)[:200]})}\n\n"

    return StreamingResponse(_stream(), media_type="text/event-stream")


# ═══════════════════════════════════════════════
# GET /v1/li/audit — 审计日志状态
# ═══════════════════════════════════════════════
@app.get("/v1/li/audit")
def audit_status(limit: int = 20, offset: int = 0):
    """审计日志汇总 + 最近N条（流式读取，不爆内存）"""
    audit_log = PROJECT_ROOT / "logs" / "ai_audit.jsonl"
    report_file = PROJECT_ROOT / "logs" / "audit_summary.json"

    result = {
        "exists": audit_log.exists(),
        "total": 0,
        "pending": 0,
        "reviewed": 0,
        "flagged": 0,
        "by_source": {},
        "recent": [],
        "report": None,
    }

    # 读汇总报告
    if report_file.exists():
        try:
            with open(report_file) as f:
                result["report"] = json.load(f)
        except Exception:
            pass

    if not audit_log.exists():
        return result

    # 流式扫描统计
    sources = {}
    entries = []
    with open(audit_log) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            result["total"] += 1
            st = rec.get("review_status", "pending")
            if st == "pending":
                result["pending"] += 1
            elif st in ("reviewed", "reviewed_batch", "approved"):
                result["reviewed"] += 1
            elif st == "flagged":
                result["flagged"] += 1
            ms = rec.get("model_source", "?")
            sources[ms] = sources.get(ms, 0) + 1

            if result["total"] > offset and len(entries) < limit:
                entries.append({
                    "model_source": rec.get("model_source", ""),
                    "file_path": rec.get("file_path", ""),
                    "line_start": rec.get("line_start", 0),
                    "line_end": rec.get("line_end", 0),
                    "review_status": rec.get("review_status", ""),
                    "review_method": rec.get("review_method", ""),
                    "reviewed_at": rec.get("reviewed_at", ""),
                })

    result["by_source"] = dict(sorted(sources.items(), key=lambda x: -x[1])[:10])
    result["recent"] = entries
    return result


# ═══════════════════════════════════════════════
# GET /v1/li/model-routing — 模型路由状态
# ═══════════════════════════════════════════════
@app.get("/v1/li/model-routing")
def model_routing():
    """探测本地 ollama 模型 + 配置文件状态"""
    import subprocess

    result = {
        "local_models": [],
        "local_available": False,
        "ollama_running": False,
        "api_keys": {"deepseek": False, "kimi": False},
        "config": {},
    }

    # 探测 ollama
    try:
        proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            result["ollama_running"] = True
            for line in proc.stdout.strip().split("\n")[1:]:  # skip header
                parts = line.split()
                if len(parts) >= 2:
                    result["local_models"].append({
                        "name": parts[0],
                        "size": parts[1],
                    })
            result["local_available"] = len(result["local_models"]) > 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 读 CodeBuddy settings
    settings_paths = [
        os.path.expanduser("~/Library/Application Support/CodeBuddy CN/User/settings.json"),
        os.path.expanduser("~/Library/Application Support/CodeBuddy/User/settings.json"),
    ]
    for sp in settings_paths:
        if os.path.exists(sp):
            try:
                with open(sp) as f:
                    settings = json.load(f)
                lm = {}
                for k in settings:
                    if k.startswith("longhun-model"):
                        lm[k.replace("longhun-model.", "")] = settings[k]
                result["config"] = lm
                # 检测API keys
                dk = settings.get("longhun-model.deepseekApiKey", "")
                kk = settings.get("longhun-model.kimiApiKey", "")
                result["api_keys"]["deepseek"] = bool(dk and len(dk) > 5)
                result["api_keys"]["kimi"] = bool(kk and len(kk) > 5)
                break
            except Exception:
                pass

    return result


# ═══════════════════════════════════════════════
# 健康检查
# ═══════════════════════════════════════════════
@app.get("/v1/li/health")
def health():
    return {"status": "ok", "service": "knowledge-hub-api", "version": "1.0.0"}


# ═══════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn  # type: ignore[import]
    _log("启动", "知识中枢 API v1.0 · :8766", "ok")
    uvicorn.run(app, host="127.0.0.1", port=8766, log_level="warning")
