# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂引擎主控 · Web 仪表盘后端 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-WEB-v1.0-9E8D7C6B
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

启动:
  python3 bin/lh_ctl_web.py --host 127.0.0.1 --port 9630
  或: lh web
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request, send_from_directory

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_ctl_config import load_config, logs_dir, state_dir, project_root

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-WEB-v1.0-9E8D7C6B"

app = Flask(__name__)
if HAS_CORS:
    CORS(app)


def _now() -> str:
    return datetime.now(CST).isoformat()


def _job_id() -> str:
    return f"lh-web-{_now()[:10]}-{datetime.now(CST).strftime('%H%M%S')}-{uuid.uuid4().hex[:6]}"


def _read_jsonl(path: Path, limit: int = 100) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    records: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records[-limit:]


def _load_registry() -> Optional[Dict[str, Any]]:
    cfg = load_config()
    p = project_root(cfg) / "data" / "notion_sync" / "engines" / "engine_registry.json"
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_integrity_index() -> Dict[str, Dict[str, Any]]:
    cfg = load_config()
    p = project_root(cfg) / "data" / "notion_sync" / "engines" / "integrity_report.json"
    idx: Dict[str, Dict[str, Any]] = {}
    if not p.exists():
        return idx
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for r in data.get("results", []):
        path = r.get("path", "")
        if path:
            idx[path] = r
    return idx


def _calc_health(result: Dict[str, Any]) -> int:
    passed = result.get("passed", False)
    issues = result.get("issues", [])
    severity = result.get("severity", "unknown")
    score = 100
    if not passed:
        if severity == "critical":
            score -= 30
        elif severity == "high":
            score -= 20
        else:
            score -= 10
    score -= len(issues) * 5
    return max(0, min(100, score))


def _avg_health(registry: Dict[str, Any]) -> int:
    engines = registry.get("engines", [])
    if not engines:
        return 0
    integrity = _load_integrity_index()
    total = sum(_calc_health(integrity.get(e.get("path", ""), {})) for e in engines)
    return round(total / len(engines))


def _aggregate_jobs(cfg: Dict[str, Any]) -> Dict[str, Any]:
    jobs = _read_jsonl(state_dir(cfg) / "job_history.jsonl", limit=1000)
    by_command: Dict[str, int] = {}
    by_status = {"success": 0, "failed": 0}
    for j in jobs:
        cmd = j.get("command", "unknown")
        by_command[cmd] = by_command.get(cmd, 0) + 1
        if j.get("exit_code") == 0:
            by_status["success"] += 1
        else:
            by_status["failed"] += 1
    return {"total": len(jobs), "by_command": by_command, "by_status": by_status, "recent": jobs[-20:][::-1]}


def _load_video_metrics() -> Dict[str, Any]:
    cfg = load_config()
    metrics_path = project_root(cfg) / "videos" / "metrics.json"
    index_path = project_root(cfg) / "videos" / "index.json"
    metrics: Dict[str, Any] = {}
    if metrics_path.exists():
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    videos_total = 0
    by_style: Dict[str, int] = {}
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                idx = json.load(f)
                videos_total = idx.get("total_videos", 0)
                by_style = idx.get("styles", {})
        except (json.JSONDecodeError, IOError):
            pass

    daily_sorted = sorted(metrics.get("daily", {}).items())
    recent_comments = []
    for vid, vm in metrics.get("videos", {}).items():
        for c in vm.get("comments", []):
            recent_comments.append({**c, "video_id": vid})
    recent_comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return {
        "engagement": metrics.get("totals", {"views": 0, "downloads": 0, "shares": 0, "comments": 0, "videos": 0}),
        "videos_total": videos_total,
        "by_style": by_style,
        "daily": [
            {"date": d, "views": v.get("views", 0), "downloads": v.get("downloads", 0),
             "shares": v.get("shares", 0), "comments": v.get("comments", 0),
             "videos": v.get("videos", 0)}
            for d, v in daily_sorted
        ],
        "recent_comments": recent_comments[:10],
    }


# ═══════════════════════════════════════════════════════════
# API Routes
# ═══════════════════════════════════════════════════════════

@app.route("/")
def index():
    cfg = load_config()
    dashboard_html = cfg.get("web", {}).get("dashboard_html", "portal/dashboard/index.html")
    p = project_root(cfg) / dashboard_html
    if p.exists():
        return send_from_directory(str(p.parent), p.name)
    return "<h1>龍魂引擎主控</h1><p>仪表盘 HTML 未找到</p>", 404


@app.route("/api/health")
def api_health():
    return jsonify({"ok": True, "dna": DNA, "time": _now()})


@app.route("/api/status")
def api_status():
    registry = _load_registry()
    if not registry:
        return jsonify({"error": "注册表不存在"}), 404

    integrity_index = _load_integrity_index()
    engines = []
    for eng in registry.get("engines", []):
        path = eng.get("path", "")
        health = _calc_health(integrity_index.get(path, {}))
        engines.append({
            "id": eng.get("id"),
            "name": eng.get("name"),
            "category": eng.get("category"),
            "subcategory": eng.get("subcategory"),
            "type": eng.get("type"),
            "status": eng.get("status"),
            "lines": eng.get("lines"),
            "health": health,
            "description": eng.get("description", "")[:120],
            "dna": eng.get("dna", ""),
        })

    return jsonify({
        "total": len(engines),
        "generated_at": registry.get("generated_at"),
        "engines": engines,
    })


@app.route("/api/logs")
def api_logs():
    cfg = load_config()
    limit = request.args.get("tail", 50, type=int)
    d = state_dir(cfg)
    jobs = _read_jsonl(d / "job_history.jsonl", limit=limit)
    return jsonify({"total": len(jobs), "jobs": jobs})


@app.route("/api/jobs")
def api_jobs():
    return api_logs()


@app.route("/api/metrics")
def api_metrics():
    cfg = load_config()
    registry = _load_registry()
    engines = {
        "total": registry.get("total_engines", 0) if registry else 0,
        "by_category": registry.get("stats", {}).get("by_category", {}) if registry else {},
        "by_type": registry.get("stats", {}).get("by_type", {}) if registry else {},
        "avg_health": _avg_health(registry) if registry else 0,
    }
    return jsonify({
        "engines": engines,
        "jobs": _aggregate_jobs(cfg),
        "videos": _load_video_metrics(),
        "time": _now(),
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json() or {}
    command = data.get("command")
    args = data.get("args", {})

    if command not in ("search", "video", "distill", "audit", "3d"):
        return jsonify({"error": f"不支持的命令: {command}"}), 400

    cfg = load_config()
    script = project_root(cfg) / "bin" / "lh_ctl.py"
    if not script.exists():
        return jsonify({"error": "lh_ctl.py 不存在"}), 500

    job = {
        "job_id": _job_id(),
        "command": command,
        "args": args,
        "started_at": _now(),
        "status": "running",
    }

    def run_in_thread():
        cmd = [sys.executable, str(script), command]
        if command == "search":
            cmd.append(args.get("query", ""))
        elif command == "video":
            if args.get("script"):
                cmd.extend(["--script", args["script"]])
            if args.get("style"):
                cmd.extend(["--style", args["style"]])
            if args.get("name"):
                cmd.extend(["--name", args["name"]])
        elif command == "distill":
            if args.get("mock"):
                cmd.append("--mock")
        elif command == "3d":
            if args.get("input"):
                cmd.extend(["--input", args["input"]])
            if args.get("category"):
                cmd.extend(["--category", args["category"]])
            if args.get("style"):
                cmd.extend(["--style", args["style"]])
        # audit 无需额外参数
        subprocess.run(cmd, cwd=project_root(cfg), capture_output=True, text=True)

    t = threading.Thread(target=run_in_thread, daemon=True)
    t.start()

    return jsonify({"ok": True, "job": job})


# ═══════════════════════════════════════════════════════════
# Entry
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂引擎主控 Web 仪表盘")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=9630, help="监听端口")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    args = parser.parse_args()

    print(f"\n{DNA}\n")
    print(f"🌐 启动仪表盘: http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=False)


if __name__ == "__main__":
    main()
