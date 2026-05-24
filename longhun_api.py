#!/usr/bin/env python3
from flask import Flask, request, jsonify
from empower_engine_v2 import LonghunEngine
import json
import datetime
from pathlib import Path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

engine = LonghunEngine()
BASE_DIR = Path.home() / "longhun-system"
LOG_DIR = BASE_DIR / "logs"
CONFIG_PATH = BASE_DIR / "config.json"


def _audit_token() -> str:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8")).get(
                "audit_token", "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
            )
        except json.JSONDecodeError:
            pass
    return "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

@app.route('/')
def root():
    return jsonify({
        "service": "龍魂赋能引擎API",
        "version": "v1.5",
        "uid": "9622",
        "dna": "#龍芯⚡️2026-05-17-API",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "status": "running"
    })

@app.route('/identify', methods=['POST'])
def identify():
    data = request.get_json(force=True)
    text = data.get("text", "")
    if not text or len(text) > 5000:
        return jsonify({"error": "文本为空或超限（5000字）"}), 400
    result = engine.full_process(text)
    log_entry = {
        "time": datetime.datetime.now().isoformat(),
        "ip": request.remote_addr,
        "endpoint": "/identify",
        "input_hash": result["input_length"]
    }
    with open(LOG_DIR / "api_access.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    return jsonify(result)

@app.route('/audit-log', methods=['GET'])
def audit_log():
    token = request.headers.get("X-Longhun-Token")
    if token != _audit_token():
        return jsonify({"error": "无权审计"}), 403
    log_file = LOG_DIR / "engine_audit.jsonl"
    if not log_file.exists():
        return jsonify({"logs": []})
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    logs = [json.loads(l) for l in lines[-50:]]
    return jsonify({"logs": logs, "count": len(lines)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
