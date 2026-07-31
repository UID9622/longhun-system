# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · ANTENNA-8GATE v1 vs v2 精简基准 (6次推理)
# DNA：#龍芯⚡️丙午·乙未·丙申·申时·☲离-BENCH-V1V2-SLIM-a1b2c3d4
# ============================================================
import sys, os, time, json, numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
sys.path.insert(0, os.path.join(BASE, 'scheduler'))
import requests
from antenna_mesh import AntennaMesh, Bagua
from antenna_mesh_v2 import AntennaMeshV2, Bagua as BaguaV2

def to_v2_bagua(b: Bagua) -> BaguaV2:
    """转换 v1 Bagua → v2 Bagua"""
    return BaguaV2(b.value)

OLLAMA = "http://localhost:11434"
MODEL = "longhun-v4.1.1-bind:latest"

def chat(prompt, max_tok=256):
    r = requests.post(f"{OLLAMA}/api/chat", json={
        "model": MODEL, "stream": False,
        "messages": [{"role":"system","content":"龍魂助手，简洁回答"},
                     {"role":"user","content":prompt}],
        "options": {"temperature":0.7,"num_predict":max_tok}
    }, timeout=180)
    d = r.json()
    return {"tokens": d.get("eval_count",0), "content": d.get("message",{}).get("content","")}

def v1_run(mesh, query):
    vec = np.zeros(128); chars = [ord(c)%256 for c in query[:512]]
    vec[:len(chars)] = np.array(chars)/255.0
    if '代码' in query: tg = Bagua.离
    elif '状态' in query or '怎么' in query: tg = Bagua.乾
    else: tg = Bagua.兑
    t0=time.time(); out,s=mesh.inference(vec,tg); r=chat(query)
    lat=(time.time()-t0)*1000
    return lat, r["tokens"], s['skip_rate'], s['nodes_active']

def v2_run(mesh, query):
    if '代码' in query: tg = Bagua.离
    elif '状态' in query or '怎么' in query: tg = Bagua.乾
    else: tg = Bagua.兑
    t0=time.time(); emb,s=mesh.inference(query, to_v2_bagua(tg)); r=chat(query)
    lat=(time.time()-t0)*1000
    return lat, r["tokens"], s['skip_rate'], s['nodes_active'], s.get('encoder_stats',{})

TESTS = [
    ("冷启动", "当前系统运行状态如何？"),
    ("重复查询", "当前系统运行状态如何？"),  # same
    ("语义相似", "帮我看看系统现在怎么样了"),
]

print("="*60)
print("ANTENNA-8GATE v1 vs v2 精简基准 (6次推理)")
print(f"模型: {MODEL}")
print("="*60)

mesh1 = AntennaMesh(nodes_per_bagua=4, dim=128)
mesh2 = AntennaMeshV2(nodes_per_bagua=16, dim=4096, memory_per_node=64)

for label, query in TESTS:
    print(f"\n[{label}] {query[:45]}...")
    
    lat1, tok1, sk1, ac1 = v1_run(mesh1, query)
    lat2, tok2, sk2, ac2, enc = v2_run(mesh2, query)
    
    print(f"  v1: {lat1:.0f}ms | {tok1}tok | 跳{sk1*100:.1f}% | 激活{ac1}/32节点")
    print(f"  v2: {lat2:.0f}ms | {tok2}tok | 跳{sk2*100:.1f}% | 激活{ac2}/128节点 | 缓存命中:{enc.get('hit_rate',0)*100:.0f}%")

print("\n"+"="*60)
print(f"v2编码器: {mesh2.encoder.get_stats()}")

# 简单对比
skips1 = sum(n.gate.skip_count for n in mesh1.nodes.values())
act1 = sum(n.gate.active_count for n in mesh1.nodes.values())
skips2 = sum(n.gate.skip_count for n in mesh2.nodes.values())
act2 = sum(n.gate.active_count for n in mesh2.nodes.values())
sr1 = skips1/(skips1+act1)*100 if (skips1+act1)>0 else 0
sr2 = skips2/(skips2+act2)*100 if (skips2+act2)>0 else 0
print(f"v1总跳过率: {sr1:.1f}% | v2总跳过率: {sr2:.1f}% | 提升: +{sr2-sr1:.1f}%")
print(f"v2节点数: {len(mesh2.nodes)} (v1的{len(mesh2.nodes)//len(mesh1.nodes)}倍)")
print("✅ 完成")
