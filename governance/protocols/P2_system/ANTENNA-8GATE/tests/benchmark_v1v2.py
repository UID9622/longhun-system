# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · ANTENNA-8GATE v1 vs v2 全面基准测试
# DNA：#龍芯⚡️丙午·乙未·丙申·未时·☲离-BENCHMARK-V1V2-SEMANTIC-a1b2c3d4
# 创建者：诸葛鑫（UID9622）
# 协议：CC BY-NC-SA 4.0
# ============================================================

import sys, os, time, json, hashlib
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
sys.path.insert(0, os.path.join(BASE, 'scheduler'))

import numpy as np
import requests
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field

# v1 (旧)
from antenna_mesh import AntennaMesh, Bagua
from wuxing_scheduler import WuxingScheduler, WuxingTask, Wuxing
# v2 (新)
from antenna_mesh_v2 import AntennaMeshV2

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "longhun-v4.1.1-bind:latest"
SYSTEM_PROMPT = "你是龍魂系统助手，UID9622专属。简洁直接回答。"

# 四组测试用例
BENCH_SETS = {
    "冷启动": [
        ("状态查询", "当前系统运行状态如何？"),
        ("代码生成", "用Python实现二分查找算法"),
        ("安全审计", "检测以下代码的安全漏洞"),
    ],
    "重复查询": [  # 跟上面完全一样
        ("状态查询", "当前系统运行状态如何？"),
        ("代码生成", "用Python实现二分查找算法"),
    ],
    "语义相似": [
        ("状态查询-变体", "帮我看看系统现在怎么样了"),
        ("代码生成-变体", "请写一个Python的binary search"), 
    ],
    "全新话题": [
        ("完全不同", "今天天气真不错"),
        ("完全不同", "推荐一本好书"),
    ],
}

@dataclass
class Result:
    label: str
    mode: str
    query: str
    latency_ms: float
    tokens: int
    tps: float
    mesh_skip_rate: float
    mesh_active_nodes: int
    mesh_total_nodes: int
    encoder_hit: bool = False
    success: bool = True
    error: str = ""


def ollama_available():
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return r.status_code == 200
    except:
        return False


def ollama_chat(prompt: str, max_tokens: int = 256) -> Dict[str, Any]:
    resp = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": max_tokens}
        },
        timeout=180
    )
    resp.raise_for_status()
    data = resp.json()
    return {"content": data.get("message", {}).get("content", ""),
            "tokens": data.get("eval_count", 0)}


def run_v1_test(label: str, query: str, results: List[Result]):
    """旧版：ord(c)%256 编码 32节点"""
    mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
    vec = np.zeros(128)
    chars = [ord(c) % 256 for c in query[:512]]
    vec[:len(chars)] = np.array(chars) / 255.0
    
    if any(k in query for k in ['安全','漏洞','检测']):
        tg = Bagua.艮
    elif any(k in query for k in ['代码','Python','实现','写','binary','search','排序']):
        tg = Bagua.离
    elif any(k in query for k in ['状态','运行','看看','怎么']):
        tg = Bagua.乾
    else:
        tg = Bagua.兑
    
    t0 = time.time()
    out, stats = mesh.inference(vec, tg)
    try:
        r = ollama_chat(query)
    except Exception as e:
        results.append(Result(label, "v1基准", query, 0, 0, 0, stats['skip_rate'],
                     stats['nodes_active'], stats['nodes_total'], False, False, str(e)))
        return
    lat = (time.time() - t0) * 1000
    results.append(Result(label, "v1基准", query, lat, r["tokens"],
                 r["tokens"]/(lat/1000) if lat>0 else 0,
                 stats['skip_rate'], stats['nodes_active'], stats['nodes_total']))


def run_v2_test(label: str, query: str, mesh: AntennaMeshV2, results: List[Result], 
                is_first_pass: bool):
    """新版：Ollama Embedding 512节点"""
    if any(k in query for k in ['安全','漏洞','检测']):
        tg = Bagua.艮
    elif any(k in query for k in ['代码','Python','实现','写','binary','search','排序']):
        tg = Bagua.离
    elif any(k in query for k in ['状态','运行','看看','怎么']):
        tg = Bagua.乾
    else:
        tg = Bagua.兑
    
    t0 = time.time()
    embedding, stats = mesh.inference(query, tg)
    try:
        r = ollama_chat(query)
    except Exception as e:
        results.append(Result(label, "v2语义", query, 0, 0, 0, stats['skip_rate'],
                     stats['nodes_active'], stats['nodes_total'], False, False, str(e)))
        return
    lat = (time.time() - t0) * 1000
    enc_hit = stats.get('encoder_stats', {}).get('hit_rate', 0) > 0.5
    results.append(Result(label, "v2语义", query, lat, r["tokens"],
                 r["tokens"]/(lat/1000) if lat>0 else 0,
                 stats['skip_rate'], stats['nodes_active'], stats['nodes_total'], enc_hit))


def summarize(results: List[Result]) -> Dict[str, Any]:
    modes = ["v1基准", "v2语义"]
    summary = {}
    for mode in modes:
        mr = [r for r in results if r.mode == mode and r.success]
        if not mr:
            summary[mode] = {"count": 0}; continue
        lats = [r.latency_ms for r in mr]
        toks = [r.tokens for r in mr]
        skips = [r.mesh_skip_rate * 100 for r in mr]
        summary[mode] = {
            "count": len(mr),
            "avg_latency_ms": round(sum(lats)/len(lats), 1),
            "total_tokens": sum(toks),
            "tps_avg": round(sum(toks)/sum(lats)*1000, 1) if sum(lats)>0 else 0,
            "skip_rate_pct": round(sum(skips)/len(skips), 1),
        }
    return summary


def main():
    print("=" * 65)
    print("ANTENNA-8GATE v1 vs v2 全面基准")
    print("=" * 65)
    
    ok = ollama_available()
    print(f"Ollama: {'🟢' if ok else '🔴'} | 模型: {MODEL_NAME}")
    if not ok:
        print("🔴 Ollama 不可用"); return
    
    all_results: List[Result] = []
    mesh_v2 = AntennaMeshV2(nodes_per_bagua=32, dim=4096, memory_per_node=64)
    
    total_queries = sum(len(qs) for qs in BENCH_SETS.values())
    q_count = 0
    
    for set_name, queries in BENCH_SETS.items():
        print(f"\n--- {set_name} ---")
        for qtype, query in queries:
            q_count += 1
            print(f"\n[{q_count}/{total_queries}] [{set_name}] {qtype}: {query[:45]}...")
            
            # v1
            run_v1_test(set_name, query, all_results)
            r1 = all_results[-1]
            print(f"  [v1] {r1.latency_ms:.0f}ms | {r1.tokens}tok | 跳{r1.mesh_skip_rate*100:.0f}% | {r1.mesh_active_nodes}/{r1.mesh_total_nodes}节点")
            
            # v2
            is_first = set_name == "冷启动"
            run_v2_test(set_name, query, mesh_v2, all_results, is_first)
            r2 = all_results[-1]
            print(f"  [v2] {r2.latency_ms:.0f}ms | {r2.tokens}tok | 跳{r2.mesh_skip_rate*100:.0f}% | {r2.mesh_active_nodes}/{r2.mesh_total_nodes}节点 | 缓存:{'✓' if r2.encoder_hit else '✗'}")
    
    # 汇总
    all_s = summarize(all_results)
    print("\n" + "=" * 65)
    print("汇总报告")
    print("=" * 65)
    print(f"{'模式':<12} {'平均延迟':>10} {'Token/s':>8} {'跳过率':>8} {'样本':>5}")
    print("-" * 50)
    for m in ["v1基准", "v2语义"]:
        s = all_s[m]
        print(f"{m:<12} {s['avg_latency_ms']:>8.0f}ms {s['tps_avg']:>6.1f} {s['skip_rate_pct']:>6.1f}% {s['count']:>4}")
    
    # 分场景
    print(f"\n{'场景':<12} {'v1跳%':>8} {'v2跳%':>8} {'v2缓存':>8}")
    print("-" * 42)
    for set_name in BENCH_SETS:
        v1r = [r for r in all_results if r.label == set_name and r.mode == "v1基准" and r.success]
        v2r = [r for r in all_results if r.label == set_name and r.mode == "v2语义" and r.success]
        v1_skip = sum(r.mesh_skip_rate*100 for r in v1r)/len(v1r) if v1r else 0
        v2_skip = sum(r.mesh_skip_rate*100 for r in v2r)/len(v2r) if v2r else 0
        v2_cache = sum(1 for r in v2r if r.encoder_hit)/len(v2r)*100 if v2r else 0
        print(f"{set_name:<12} {v1_skip:>7.1f}% {v2_skip:>7.1f}% {v2_cache:>6.0f}%")
    
    v1_avg = all_s["v1基准"]["skip_rate_pct"]
    v2_avg = all_s["v2语义"]["skip_rate_pct"]
    improvement = v2_avg - v1_avg
    print(f"\n📊 跳过率提升: {v1_avg:.1f}% → {v2_avg:.1f}% (+{improvement:.1f}%)")
    
    # 保存报告
    report = {
        "status": "complete",
        "v1": all_s["v1基准"],
        "v2": all_s["v2语义"],
        "improvement_pct": round(improvement, 1),
        "raw": [
            {"label": r.label, "mode": r.mode, "query": r.query[:40], 
             "latency_ms": round(r.latency_ms,1), "tokens": r.tokens,
             "skip_pct": round(r.mesh_skip_rate*100,1), "enc_hit": r.encoder_hit,
             "success": r.success}
            for r in all_results
        ]
    }
    rpath = os.path.join(BASE, "tests", "benchmark_v1v2_report.json")
    with open(rpath, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"报告: {rpath}")


if __name__ == "__main__":
    main()
