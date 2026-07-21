#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 64卦审计引擎 API
DNA: #龍芯⚡️2026-06-29-64GUA-AUDIT-API-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬64GUA-API-001 ✅

端点：
  POST /audit/run      传入8维度指标，返回审计结果
  GET  /audit/status   查看引擎状态
  GET  /audit/history  查看最近审计记录
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List

from flask import Flask, request, jsonify

sys.path.insert(0, str(Path(__file__).parent))
from gua_audit_engine import GuaAuditEngine


# ============================================================
# 配置
# ============================================================

AUDIT_LOG_DIR = Path.home() / ".龍魂" / "audit"
AUDIT_LOG_FILE = AUDIT_LOG_DIR / "audit_log.jsonl"
HISTORY_LIMIT = 100

AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
engine = GuaAuditEngine()


# ============================================================
# 审计日志写入（三色审计系统对接）
# ============================================================

def write_audit_log(record: Dict):
    """写入三色审计日志到 ~/.龍魂/audit/audit_log.jsonl"""
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_recent_history(limit: int = 50) -> List[Dict]:
    """加载最近审计记录"""
    if not AUDIT_LOG_FILE.exists():
        return []
    lines = []
    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    lines.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return lines[-limit:]


# ============================================================
# Flask 路由
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({
        "status": "🟢",
        "service": "64卦审计引擎API",
        "version": "v1.0",
        "dna": "#龍芯⚡️2026-06-29-64GUA-AUDIT-API-v1.0"
    })


@app.route("/audit/run", methods=["POST"])
def audit_run():
    """
    执行64卦审计
    请求体：{
        "metrics": {
            "innovation": 0-100,
            "support": 0-100,
            "response": 0-100,
            "optimization": 0-100,
            "risk_control": 0-100,
            "communication": 0-100,
            "defense": 0-100,
            "collaboration": 0-100
        },
        "context": "部署新功能"  // 可选
    }
    """
    data = request.get_json(force=True, silent=True) or {}
    metrics = data.get("metrics")
    context = data.get("context", "")

    if not metrics:
        return jsonify({"error": "缺少 metrics 字段"}), 400

    try:
        result = engine.calculate_gua(metrics, context=context)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"审计计算异常: {e}"}), 500

    record = result.to_dict()
    record["context"] = context
    record["trigger"] = request.headers.get("X-Trigger", "api")

    # 写入三色审计日志
    write_audit_log(record)

    return jsonify(record)


@app.route("/audit/status", methods=["GET"])
def audit_status():
    """查看审计引擎状态"""
    history = load_recent_history(limit=HISTORY_LIMIT)
    color_counts = {"🟢": 0, "🟡": 0, "🔴": 0}
    for r in history:
        color = r.get("audit_color")
        if color in color_counts:
            color_counts[color] += 1

    return jsonify({
        "status": "🟢",
        "service": "64卦审计引擎",
        "total_audits": len(history),
        "color_distribution": color_counts,
        "log_file": str(AUDIT_LOG_FILE),
        "dna": "#龍芯⚡️2026-06-29-64GUA-AUDIT-API-v1.0"
    })


@app.route("/audit/history", methods=["GET"])
def audit_history():
    """查看最近审计记录"""
    limit = min(int(request.args.get("limit", 20)), HISTORY_LIMIT)
    color = request.args.get("color", None)

    history = load_recent_history(limit=HISTORY_LIMIT)
    if color:
        history = [r for r in history if r.get("audit_color") == color]

    return jsonify({
        "count": len(history[-limit:]),
        "records": history[-limit:]
    })


# ============================================================
# CLI 入口
# ============================================================

def main():
    port = int(os.environ.get("GUA_AUDIT_PORT", "9623"))
    print(f"""
╔══════════════════════════════════════════╗
║   龍魂64卦审计引擎 API v1.0              ║
║   Port: {port:<5}                            ║
║   DNA: #龍芯⚡️2026-06-29-64GUA-AUDIT-API-v1.0 ║
╚══════════════════════════════════════════╝
端点:
  GET  /health
  POST /audit/run
  GET  /audit/status
  GET  /audit/history
""")
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
