#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三色知识库 API 接口层
DNA: #龍芯⚡️2026-04-08-KNOWLEDGE-API-v1.0

集成Claude MVP API，提供:
- 知识源管理
- 碎片采集
- 碎片查询/重组
- 隔离区管理
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加bin目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from knowledge_collector import KnowledgeCollector, DNACompatibilityChecker

app = Flask(__name__)
CORS(app)

# 初始化采集器
collector = KnowledgeCollector()
checker = DNACompatibilityChecker()


@app.route('/')
def index():
    """API根"""
    return jsonify({
        "name": "三色知识库 API",
        "version": "v1.0",
        "dna": "#龍芯⚡️2026-04-08-KNOWLEDGE-API-v1.0",
        "endpoints": {
            "GET /sources": "获取所有知识源",
            "GET /sources/<category>": "获取分类知识源",
            "POST /ingest": "摄入内容并碎片化",
            "GET /fragments": "获取碎片列表",
            "GET /search": "搜索碎片",
            "GET /stats": "获取统计",
            "GET /quarantine": "获取隔离区内容"
        }
    })


@app.route('/sources')
def get_sources():
    """获取所有知识源"""
    return jsonify(collector.sources)


@app.route('/sources/<category>')
def get_category_sources(category: str):
    """获取分类知识源"""
    sources = collector.sources.get("sources", {})
    if category in sources:
        return jsonify(sources[category])
    return jsonify({"error": "分类不存在"}), 404


@app.route('/ingest', methods=['POST'])
def ingest():
    """
    摄入内容并碎片化
    
    POST参数:
    - content: 内容文本
    - source_id: 来源ID
    - source_url: 来源URL
    - source_title: 来源标题
    - category: 分类
    - palace: 宫位(1-9)
    """
    data = request.json
    
    required = ['content', 'source_id', 'category']
    for field in required:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400
    
    fragments = collector.ingest(
        content=data['content'],
        source_id=data['source_id'],
        source_url=data.get('source_url', ''),
        source_title=data.get('source_title', ''),
        category=data['category'],
        palace=data.get('palace', 5)
    )
    
    # 保存
    collector.save_fragments(fragments)
    
    return jsonify({
        "success": True,
        "fragments_count": len(fragments),
        "indexed": sum(1 for f in fragments if f.status == 'indexed'),
        "quarantined": sum(1 for f in fragments if f.status == 'quarantined'),
        "fragments": [f.to_dict() for f in fragments]
    })


@app.route('/fragments')
def get_fragments():
    """获取碎片列表"""
    category = request.args.get('category')
    frag_type = request.args.get('type')
    min_score = float(request.args.get('min_score', 0.6))
    limit = int(request.args.get('limit', 50))
    
    results = []
    for filepath in collector.indexed_dir.glob("*.json"):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if data.get("compatibility_score", 0) < min_score:
                continue
            if category and data.get("category") != category:
                continue
            if frag_type and data.get("type") != frag_type:
                continue
                
            results.append(data)
    
    results = sorted(results, key=lambda x: x.get("compatibility_score", 0), reverse=True)
    
    return jsonify({
        "total": len(results),
        "returned": min(limit, len(results)),
        "fragments": results[:limit]
    })


@app.route('/search')
def search():
    """搜索碎片"""
    keyword = request.args.get('q', '')
    min_score = float(request.args.get('min_score', 0.5))
    limit = int(request.args.get('limit', 20))
    
    if not keyword:
        return jsonify({"error": "缺少搜索关键词 q"}), 400
    
    results = collector.search_fragments(keyword, min_score)
    
    return jsonify({
        "keyword": keyword,
        "total": len(results),
        "results": results[:limit]
    })


@app.route('/recombine', methods=['POST'])
def recombine():
    """
    碎片重组
    
    POST参数:
    - fragment_ids: 碎片ID列表
    - operation: 操作类型 (concat|merge|intersect)
    - context: 重组上下文
    """
    data = request.json
    fragment_ids = data.get('fragment_ids', [])
    operation = data.get('operation', 'concat')
    context = data.get('context', '')
    
    if len(fragment_ids) < 2:
        return jsonify({"error": "至少需要2个碎片"}), 400
    
    # 加载碎片
    fragments = []
    for fid in fragment_ids:
        filepath = collector.indexed_dir / f"{fid}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                fragments.append(json.load(f))
    
    # 执行重组
    if operation == 'concat':
        # 串联
        combined_content = '，'.join([f['content'] for f in fragments])
    elif operation == 'merge':
        # 融合（去重合并）
        contents = [f['content'] for f in fragments]
        combined_content = ' '.join(list(set(contents)))
    else:
        combined_content = ' '.join([f['content'] for f in fragments])
    
    # DNA验证
    dna_result = checker.check(combined_content, 'general')
    
    return jsonify({
        "success": True,
        "operation": operation,
        "context": context,
        "combined_content": combined_content,
        "source_fragments": len(fragments),
        "dna_check": dna_result
    })


@app.route('/stats')
def stats():
    """获取统计"""
    base_stats = collector.get_stats()
    
    # 分类统计
    category_stats = {}
    for filepath in collector.indexed_dir.glob("*.json"):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cat = data.get('category', 'unknown')
            if cat not in category_stats:
                category_stats[cat] = {"count": 0, "avg_score": 0, "total_score": 0}
            category_stats[cat]["count"] += 1
            category_stats[cat]["total_score"] += data.get('compatibility_score', 0)
    
    for cat in category_stats:
        count = category_stats[cat]["count"]
        total = category_stats[cat]["total_score"]
        category_stats[cat]["avg_score"] = round(total / count, 2) if count > 0 else 0
        del category_stats[cat]["total_score"]
    
    return jsonify({
        "overview": base_stats,
        "by_category": category_stats,
        "sources": collector.sources.get('stats', {})
    })


@app.route('/quarantine')
def get_quarantine():
    """获取隔离区内容"""
    limit = int(request.args.get('limit', 20))
    
    results = []
    for filepath in collector.quarantine_dir.glob("*.json"):
        with open(filepath, 'r', encoding='utf-8') as f:
            results.append(json.load(f))
    
    return jsonify({
        "total_quarantined": len(results),
        "fragments": results[:limit]
    })


@app.route('/quarantine/<fragment_id>/review', methods=['POST'])
def review_quarantine(fragment_id: str):
    """审核隔离区碎片"""
    data = request.json
    action = data.get('action')  # approve | reject
    reason = data.get('reason', '')
    
    filepath = collector.quarantine_dir / f"{fragment_id}.json"
    if not filepath.exists():
        return jsonify({"error": "碎片不存在"}), 404
    
    with open(filepath, 'r', encoding='utf-8') as f:
        fragment = json.load(f)
    
    if action == 'approve':
        # 移入索引区
        fragment['status'] = 'approved'
        fragment['status_reason'] = f"人工审核通过: {reason}"
        new_path = collector.indexed_dir / f"{fragment_id}.json"
    else:
        # 拒绝，留在隔离区
        fragment['status'] = 'rejected'
        fragment['status_reason'] = f"人工审核拒绝: {reason}"
        new_path = filepath
    
    with open(new_path, 'w', encoding='utf-8') as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)
    
    if action == 'approve' and filepath != new_path:
        filepath.unlink()  # 删除原文件
    
    return jsonify({
        "success": True,
        "action": action,
        "fragment_id": fragment_id
    })


@app.route('/dna/check', methods=['POST'])
def dna_check():
    """DNA兼容度检测"""
    data = request.json
    content = data.get('content', '')
    category = data.get('category', 'general')
    
    if not content:
        return jsonify({"error": "缺少content字段"}), 400
    
    result = checker.check(content, category)
    
    return jsonify({
        "content": content[:100] + "..." if len(content) > 100 else content,
        "category": category,
        "dna_result": result
    })


if __name__ == '__main__':
    print("🚀 启动三色知识库 API (端口 8002)")
    app.run(host='0.0.0.0', port=8002, debug=True)
