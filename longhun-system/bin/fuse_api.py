#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字根熔断规则 · API层
DNA: #龍芯⚡️2026-04-08-FUSE-API-v1.0

读取已有规则，不新建数据库
- 从 algo_db.jsonl 读取数字根规则
- 从 index.jsonl 读取Notion索引
- 从 memory.jsonl 读取系统记忆
"""

import json
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = Path.home() / "longhun-system"
ALGO_DB = BASE / "logs" / "algo_db.jsonl"
INDEX_DB = BASE / "notion-index" / "out" / "index.jsonl"
MEMORY_DB = BASE / "memory.jsonl"


def load_algo_db():
    """读取算法元数据库（只读）"""
    algorithms = {}
    if ALGO_DB.exists():
        with open(ALGO_DB, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        name = data.get('name', '')
                        family = data.get('family', '')
                        algorithms[name] = data
                        if family:
                            if family not in algorithms:
                                algorithms[family] = []
                            algorithms[family].append(data)
                    except:
                        pass
    return algorithms


def load_index_count():
    """统计Notion索引数量"""
    count = 0
    databases = 0
    pages = 0
    if INDEX_DB.exists():
        with open(INDEX_DB, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
                    try:
                        data = json.loads(line)
                        item_type = data.get('item', {}).get('type', '')
                        if item_type == 'database':
                            databases += 1
                        elif item_type == 'page':
                            pages += 1
                    except:
                        pass
    return {"total": count, "databases": databases, "pages": pages}


def load_memory_count():
    """统计记忆条数"""
    count = 0
    if MEMORY_DB.exists():
        with open(MEMORY_DB, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
    return count


@app.route('/')
def index():
    """API根"""
    return jsonify({
        "name": "数字根熔断规则 · 第一道闸门",
        "version": "v1.0",
        "dna": "#龍芯⚡️2026-04-08-FUSE-API-v1.0",
        "data_sources": {
            "algo_db": str(ALGO_DB),
            "index_db": str(INDEX_DB),
            "memory_db": str(MEMORY_DB)
        },
        "endpoints": [
            "GET /fuse/digital_root - 数字根熔断规则",
            "GET /fuse/check?n=123 - 计算数字根并分类",
            "GET /stats - 统计所有数据源",
            "GET /archive/list - 可归档历史版本列表"
        ]
    })


@app.route('/fuse/digital_root')
def get_digital_root_rules():
    """获取数字根熔断规则（从已有algo_db读取）"""
    algo_db = load_algo_db()
    rule = algo_db.get('digital_root_369', {})
    
    return jsonify({
        "rule_name": "数字根熔断规则 · 第一道闸门",
        "source": "algo_db.jsonl (只读)",
        "formulas": rule.get('formulas', []),
        "variables": rule.get('variables', {}),
        "functions": rule.get('functions', []),
        "classification": {
            "CYCLE_369": "最高共振态 (3,6,9)",
            "EXPO_248": "指数增长态 (2,4,8)",
            "LINEAR_123": "线性常态 (1,2,3,4,5,7)"
        },
        "fuse_conditions": {
            "🔴 熔断": "DR ∉ {3,6,9} 且 触发P0条件",
            "🟡 待审": "DR ∈ {2,4,8} 需二次确认",
            "🟢 通过": "DR ∈ {3,6,9} 最高共振"
        }
    })


@app.route('/fuse/check')
def check_digital_root():
    """计算数字根并给出熔断判定"""
    n = request.args.get('n', '')
    
    try:
        n = int(n)
        if n <= 0:
            return jsonify({"error": "请输入正整数"}), 400
    except:
        return jsonify({"error": "无效输入"}), 400
    
    # 计算数字根
    dr = 1 + ((n - 1) % 9)
    
    # 分类
    if dr in [3, 6, 9]:
        category = "CYCLE_369"
        verdict = "🟢 通过"
        fuse_action = "放行"
    elif dr in [2, 4, 8]:
        category = "EXPO_248"
        verdict = "🟡 待审"
        fuse_action = "二次确认"
    else:
        category = "LINEAR_123"
        verdict = "🔴 熔断"
        fuse_action = "停止+记录"
    
    return jsonify({
        "input": n,
        "digital_root": dr,
        "category": category,
        "verdict": verdict,
        "fuse_action": fuse_action,
        "formula": f"DR({n}) = 1 + (({n}-1) % 9) = {dr}"
    })


@app.route('/stats')
def get_stats():
    """获取所有数据源统计"""
    index_stats = load_index_count()
    memory_count = load_memory_count()
    
    # 统计算法族
    algo_db = load_algo_db()
    families = set()
    for key, val in algo_db.items():
        if isinstance(val, dict):
            families.add(val.get('family', ''))
    
    return jsonify({
        "digital_root_fuse": "🟢 已接入 · 第一道闸门",
        "sources": {
            "notion_index": {
                "file": str(INDEX_DB),
                "total_entries": index_stats["total"],
                "databases": index_stats["databases"],
                "pages": index_stats["pages"],
                "status": "✅ 只读"
            },
            "memory_jsonl": {
                "file": str(MEMORY_DB),
                "total_entries": memory_count,
                "status": "✅ 只读"
            },
            "algo_db": {
                "file": str(ALGO_DB),
                "families": list(families),
                "status": "✅ 只读"
            }
        },
        "note": "所有数据源均为只读，不写入新数据"
    })


@app.route('/archive/list')
def list_archivable():
    """列出可归档的历史版本"""
    archive_candidates = []
    
    # 检查大文件
    if MEMORY_DB.exists():
        size_mb = MEMORY_DB.stat().st_size / (1024 * 1024)
        if size_mb > 0.5:  # 超过500KB建议归档
            archive_candidates.append({
                "file": "memory.jsonl",
                "size_mb": round(size_mb, 2),
                "reason": "超过500KB，建议按月份归档",
                "action": "archive_by_month"
            })
    
    return jsonify({
        "archive_candidates": archive_candidates,
        "archive_location": "~/longhun-system/archive/",
        "policy": "历史版本可封存，但不删除"
    })


if __name__ == '__main__':
    print("🚀 启动数字根熔断规则API (端口 8003)")
    print("📊 数据源:")
    print(f"   - algo_db.jsonl: {load_algo_db().get('digital_root_369') and '✅' or '❌'}")
    print(f"   - index.jsonl: {load_index_count()['total']} 条")
    print(f"   - memory.jsonl: {load_memory_count()} 条")
    app.run(host='0.0.0.0', port=8003, debug=True)
