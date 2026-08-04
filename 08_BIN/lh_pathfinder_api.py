#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍魂路径规划引擎 · REST API 服务
# DNA: #龍芯⚡️丙午·癸未·丁未·离为火-路径规划-API-v4.1.5
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 锚定: 道德经第八十章【小国寡民，使有什伯之器而不用】——API 简洁即道

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, request, jsonify

# 将 engines 目录加入路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "engines"))
from lh_pathfinder_engine import (
    迪杰斯特拉, A星算法, 动态规划路径, 八卦阵寻路,
    蚁群分布式寻路, 三六九不动点校验, 多因素成本, D星精简版,
    DNA, CONFIRM,
)

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    """允许本地文件/跨域调试；生产环境经 nginx 同源后不影响。"""
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


@app.route("/health")
def health():
    return jsonify({"status": "ok", "dna": DNA, "confirm": CONFIRM, "time": _now()})


@app.route("/")
def index():
    return jsonify({
        "name": "龍魂路径规划引擎 API",
        "version": "v4.1.5",
        "dna": DNA,
        "endpoints": [
            "/health",
            "/api/plan",
            "/api/compare",
            "/api/validate",
            "/api/multifactor",
        ],
    })


@app.route("/api/plan", methods=["POST"])
def plan():
    """单算法路径规划"""
    payload = request.get_json(force=True) or {}
    地图 = payload.get("地图")
    起点 = tuple(payload.get("起点", [0, 0]))
    终点 = tuple(payload.get("终点", [0, 0]))
    算法 = payload.get("算法", "astar")
    启发类型 = payload.get("启发类型", "曼哈顿")
    人格权重 = payload.get("人格权重")

    if not 地图:
        return jsonify({"error": "缺少地图参数"}), 400

    try:
        if 算法 == "dijkstra":
            结果 = 迪杰斯特拉(地图, 起点, 终点)
        elif 算法 == "astar":
            结果 = A星算法(地图, 起点, 终点, 启发类型)
        elif 算法 == "dp":
            结果 = 动态规划路径(地图, 起点, 终点)
        elif 算法 == "bagua":
            结果 = 八卦阵寻路(地图, 起点, 终点, 人格权重)
        elif 算法 == "aco":
            参数 = payload.get("蚁群参数", {})
            结果 = 蚁群分布式寻路(地图, 起点, 终点, **参数)
        elif 算法 == "dstar":
            d星 = D星精简版(地图)
            d星.初始化(起点, 终点)
            结果 = d星.计算最短路径()
        else:
            return jsonify({"error": f"未知算法: {算法}"}), 400
        return jsonify(结果)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compare", methods=["POST"])
def compare():
    """多算法对比"""
    payload = request.get_json(force=True) or {}
    地图 = payload.get("地图")
    起点 = tuple(payload.get("起点", [0, 0]))
    终点 = tuple(payload.get("终点", [0, 0]))
    if not 地图:
        return jsonify({"error": "缺少地图参数"}), 400

    人格权重 = payload.get("人格权重", {"军事": 0.4, "历史": 0.2, "哲学": 0.1, "经济": 0.1, "政治": 0.2})
    结果集 = {
        "迪杰斯特拉": 迪杰斯特拉(地图, 起点, 终点),
        "A星": A星算法(地图, 起点, 终点, "曼哈顿"),
        "动态规划": 动态规划路径(地图, 起点, 终点),
        "八卦阵": 八卦阵寻路(地图, 起点, 终点, 人格权重),
    }
    return jsonify({"对比": 结果集, "时间": _now()})


@app.route("/api/validate", methods=["POST"])
def validate():
    """三六九不动点校验"""
    payload = request.get_json(force=True) or {}
    当前位置 = tuple(payload.get("当前位置", [0, 0]))
    起点 = tuple(payload.get("起点", [0, 0]))
    终点 = tuple(payload.get("终点", [0, 0]))
    已走路径 = [tuple(p) for p in payload.get("已走路径", [])]
    return jsonify(三六九不动点校验(当前位置, 起点, 终点, 已走路径))


@app.route("/api/multifactor", methods=["POST"])
def multifactor():
    """多因素成本计算"""
    payload = request.get_json(force=True) or {}
    距离 = float(payload.get("距离", 0))
    时间 = float(payload.get("时间", 0))
    能耗 = float(payload.get("能耗", 0))
    安全 = float(payload.get("安全", 0))
    权重 = payload.get("权重", {"距离": 0.25, "时间": 0.25, "能耗": 0.25, "安全": 0.25})
    return jsonify({"总成本": 多因素成本(距离, 时间, 能耗, 安全, 权重)})


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9650)
    args = parser.parse_args()
    print(DNA)
    print(CONFIRM)
    print(f"🧭 龍魂路径规划 API 启动: http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
