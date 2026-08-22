#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·酉时·䷜坎-KNOWLEDGE-HUB-API-v1.0-7d3a1e9b
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 知识中枢面板后端 API · 按钮不再死
"""
龍魂·知识中枢 API 后端 v1.0
────────────────────────────
端口: 8766
端点:
  GET  /v1/li/status      — 系统实时状态 (CPU/内存/磁盘/GPU/进程)
  POST /v1/li/chat        — 官网AI聊天机器人 (JSON: {"message": "..."})
  POST /v1/li/mine/scan   — 触发 Library 矿场勘探
  GET  /v1/li/mine/status — 矿场状态
  POST /v1/li/crawl       — 触发知识爬取
  POST /v1/li/index       — 触发索引重建
  GET  /v1/li/models      — 模型状态列表
  GET  /v1/li/logs        — 最近活动日志

启动: python3 bin/lh_knowledge_hub_api.py
部署: launchd → com.longhun.knowledge-hub-api.plist
nginx: location /api/v1/li/ → http://127.0.0.1:8766/v1/li/
"""
import os, sys, json, time, subprocess, glob, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
def _collect_macos(info: dict):
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


def _collect_linux(info: dict):
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
    stats = {
        "articles": 0,
        "categories": 0,
        "sources": 0,
        "train_data": 0,
        "graph_nodes": 0,
        "graph_edges": 0,
        "mineable_files": 0,
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
# POST /v1/li/chat — 官网AI聊天机器人
# ═══════════════════════════════════════════════
import re as _re

# M8 隐私出域闸门（精简版，来自观澜路由器）
_PRIVACY_PATTERNS = [
    (r'\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]', '身份证'),
    (r'1[3-9]\d{9}', '手机号'),
    (r'\d{16,19}', '银行卡号'),
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '邮箱'),
]

# 对话历史（最多保留最近20条，重启清空）
_CHAT_HISTORY: list = []

# 系统提示词
_SYSTEM_PROMPT = """你是龍魂系统的官方AI助手，运行在 uid9622.cn 上。
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
- 本地AI引擎优先，云端仅为增强

回复风格：直接、简洁、有料。用中文。"""


def _privacy_scan(text: str) -> str:
    """M8隐私出域闸门：脱敏敏感信息"""
    for pattern, name in _PRIVACY_PATTERNS:
        if _re.search(pattern, text):
            text = _re.sub(pattern, f'[***{name}***]', text)
    return text


class ChatRequest(BaseModel):
    message: str = ""


@app.post("/v1/li/chat")
async def chat(req: ChatRequest):
    """官网聊天机器人端点"""
    global _CHAT_HISTORY
    t0 = time.time()
    message = req.message

    if not message or not message.strip():
        return {"reply": "你好，请问有什么可以帮你的？", "model": "system", "dna": "", "time_ms": 0}

    # M8 隐私扫描
    safe_msg = _privacy_scan(message.strip())

    # 构建对话上下文（最近6轮）
    context_msgs = []
    for h in _CHAT_HISTORY[-6:]:
        context_msgs.append({"role": "user", "content": h["user"]})
        context_msgs.append({"role": "assistant", "content": h["assistant"]})

    # Ollama 调用
    try:
        prompt = f"""{_SYSTEM_PROMPT}

用户问题：{safe_msg}

请直接回答。"""
        r = subprocess.run(
            ["ollama", "run", "longhun:latest", prompt],
            capture_output=True, text=True, timeout=30,
        )
        reply = r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None
        model = "longhun:latest"
    except subprocess.TimeoutExpired:
        reply = None
        model = "timeout"
    except FileNotFoundError:
        reply = None
        model = "unavailable"
    except Exception as e:
        reply = None
        model = f"error:{str(e)[:50]}"

    # 断路器：longhun挂了试 qwen2.5
    if reply is None and model != "unavailable":
        try:
            r = subprocess.run(
                ["ollama", "run", "qwen2.5:1.5b", safe_msg],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0 and r.stdout.strip():
                reply = r.stdout.strip()
                model = "qwen2.5:1.5b (fallback)"
        except Exception:
            pass

    # 最终兜底
    if reply is None:
        reply = "龍魂引擎暂时无法响应，请稍后再试。如果问题紧急，可直接联系 UID9622。"
        model = "fallback:offline"

    # 记录历史
    _CHAT_HISTORY.append({"user": safe_msg, "assistant": reply, "ts": int(time.time())})
    if len(_CHAT_HISTORY) > 40:
        # 原地截断避免作用域问题
        while len(_CHAT_HISTORY) > 20:
            _CHAT_HISTORY.pop(0)

    elapsed_ms = int((time.time() - t0) * 1000)
    dna = hashlib.md5(f"{safe_msg}{reply}{int(t0)}".encode()).hexdigest()[:8]

    return {
        "reply": reply,
        "model": model,
        "dna": f"#龍芯⚡️CHAT-{dna}",
        "time_ms": elapsed_ms,
    }


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
    import uvicorn
    _log("启动", "知识中枢 API v1.0 · :8766", "ok")
    uvicorn.run(app, host="127.0.0.1", port=8766, log_level="warning")
