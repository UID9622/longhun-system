# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 本地法律引擎 API 服务
DNA: #龍芯⚡️2026-06-29-LONGHUN-LEGAL-ENGINE-API-v1.0

本地服务，端口 9634。其他模块可以通过 HTTP 或 import 引用。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "cnsh-core"))

from legal_engine import 加载法律库, 解释问题

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("❌ 需要先安装 flask: pip install flask")
    sys.exit(1)

app = Flask(__name__)
法律库 = 加载法律库()


@app.route("/")
def index():
    return "🐉 龍魂本地法律引擎已启动。POST /query 进行法律咨询。"


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json(force=True)
    问题 = data.get("question", "").strip()
    语气 = data.get("tone", "大白话")
    if not 问题:
        return jsonify({"error": "请输入问题"}), 400
    结果 = 解释问题(问题, 法律库, 语气=语气)
    return jsonify(结果)


@app.route("/laws", methods=["GET"])
def list_laws():
    """列出全部法条，供本地引用"""
    laws = []
    for 分类, 数据 in 法律库["categories"].items():
        for 法条 in 数据.get("laws", []):
            laws.append({
                "category": 分类,
                **法条,
            })
    return jsonify({"total": len(laws), "laws": laws})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "dna": "#龍芯⚡️2026-06-29-LONGHUN-LEGAL-ENGINE-API-v1.0"})


def 启动服务(端口: int = 9634):
    print(f"🐉 龍魂本地法律引擎已启动: http://127.0.0.1:{端口}/")
    app.run(host="127.0.0.1", port=端口, debug=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9634)
    args = parser.parse_args()
    启动服务(args.port)
