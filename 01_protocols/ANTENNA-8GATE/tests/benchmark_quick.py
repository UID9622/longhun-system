# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · ANTENNA-8GATE 快速基准测试 (8次推理)
# DNA：#龍芯⚡️丙午·乙未·丙申·午时·☰乾-BENCHMARK-QUICK-v1.0-8a2b3c4d
# 创建者：诸葛鑫（UID9622）
# 协议：CC BY-NC-SA 4.0
# ============================================================

import sys, os, time, json
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
sys.path.insert(0, os.path.join(BASE, 'scheduler'))
sys.path.insert(0, os.path.join(BASE, 'connector'))

import numpy as np
import requests
from typing import Dict, List
from dataclasses import dataclass, field

from antenna_mesh import AntennaMesh, Bagua
from wuxing_scheduler import WuxingScheduler, WuxingTask, Wuxing

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "longhun-v4.1.1-bind:latest"
SYSTEM_PROMPT = "你是龍魂系统助手，UID9622专属。简洁直接回答。"

# 快速版：2个用例 × 4种模式 = 8次推理
QUICK_INPUTS = [
    ("短问答", "系统当前状态如何？"),
    ("中等推理", "用Python写一个快速排序函数，带注释。"),
]

@dataclass
class BenchResult:
    mode: str
    query_type: str
    query: str
    latency_ms: float
    tokens_generated: int
    tokens_per_sec: float
    antenna_stats: Dict = field(default_factory=dict)
    wuxing_name: str = ""
    success: bool = True
    error: str = ""

class QuickBenchmark:
    def __init__(self):
        self.ollama_ok = self._check_ollama()

    def _check_ollama(self):
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False

    def _chat(self, prompt: str, max_tokens: int = 256) -> Dict:
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
        content = data.get("message", {}).get("content", "")
        tokens = data.get("eval_count", 0)
        return {"content": content, "tokens": tokens}

    def _vec(self, text): 
        chars = [ord(c) % 256 for c in text[:512]]
        v = np.zeros(128)
        v[:len(chars)] = np.array(chars) / 255.0
        return v

    def _bagua(self, text):
        if any(k in text for k in ['安全','主权','泄露','底线']): return Bagua.艮
        if any(k in text for k in ['代码','函数','Python','写']): return Bagua.离
        if any(k in text for k in ['状态','检查','检测']): return Bagua.乾
        return Bagua.离

    def _wuxing(self, text):
        for w, words in {
            Wuxing.木: ['过滤','清洗','安全','防护','泄露','底线'],
            Wuxing.火: ['调度','紧急','状态','检查'],
            Wuxing.土: ['转化','解释','含义','哲学'],
            Wuxing.金: ['代码','函数','写','生成','Python'],
            Wuxing.水: ['存储','持久','保存'],
        }.items():
            if any(kw in text for kw in words): return w
        return Wuxing.离

    def run(self):
        print("=" * 60)
        print(f"ANTENNA-8GATE 快速基准 | 模型: {MODEL_NAME}")
        print(f"Ollama: {'🟢' if self.ollama_ok else '🔴'} | {len(QUICK_INPUTS)}用例×4模式=8次推理")
        print("=" * 60)

        if not self.ollama_ok:
            print("\n🔴 Ollama 不可用")
            return {"status": "unavailable"}

        mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
        sched = WuxingScheduler()
        results = []

        for qi, (qtype, query) in enumerate(QUICK_INPUTS):
            print(f"\n[{qi+1}/{len(QUICK_INPUTS)}] {qtype}: {query[:50]}...")

            # 1) Baseline
            t0 = time.time()
            r = self._chat(query)
            lat = (time.time() - t0) * 1000
            results.append(BenchResult("baseline", qtype, query, lat, r["tokens"], 
                          r["tokens"]/(lat/1000) if lat>0 else 0, success=True))
            print(f"  [基准] {lat:.0f}ms | {r['tokens']}tok")

            # 2) Antenna
            t0 = time.time()
            vec = self._vec(query)
            tg = self._bagua(query)
            _, astats = mesh.inference(vec, tg)
            r = self._chat(query)
            lat = (time.time() - t0) * 1000
            results.append(BenchResult("antenna", qtype, query, lat, r["tokens"],
                          r["tokens"]/(lat/1000) if lat>0 else 0, astats, success=True))
            print(f"  [蚁触] {lat:.0f}ms | {r['tokens']}tok | 跳{astats['skip_rate']*100:.0f}%")

            # 3) Wuxing
            t0 = time.time()
            wx = self._wuxing(query)
            sched.submit(WuxingTask(f"q-{qi}", wx, 0, np.zeros(128)))
            time.sleep(0.01)
            r = self._chat(query)
            lat = (time.time() - t0) * 1000
            results.append(BenchResult("wuxing", qtype, query, lat, r["tokens"],
                          r["tokens"]/(lat/1000) if lat>0 else 0, wuxing_name=wx.name, success=True))
            print(f"  [五行] {lat:.0f}ms | {r['tokens']}tok | {wx.name}")

            # 4) Full stack
            t0 = time.time()
            wx = self._wuxing(query)
            sched.submit(WuxingTask(f"fs-{qi}", wx, 0, np.zeros(128)))
            time.sleep(0.01)
            vec = self._vec(query)
            tg = self._bagua(query)
            _, astats = mesh.inference(vec, tg)
            r = self._chat(query)
            lat = (time.time() - t0) * 1000
            results.append(BenchResult("full_stack", qtype, query, lat, r["tokens"],
                          r["tokens"]/(lat/1000) if lat>0 else 0, astats, wx.name, success=True))
            print(f"  [全栈] {lat:.0f}ms | {r['tokens']}tok | 跳{astats['skip_rate']*100:.0f}% | {wx.name}")

        sched.stop_all()

        # Report
        summary = {}
        for mode in ["baseline", "antenna", "wuxing", "full_stack"]:
            mr = [r for r in results if r.mode == mode and r.success]
            if not mr:
                summary[mode] = {"count": 0}; continue
            lats = [r.latency_ms for r in mr]
            toks = sum(r.tokens_generated for r in mr)
            skips = [r.antenna_stats.get('skip_rate',0) for r in mr if r.antenna_stats]
            summary[mode] = {
                "count": len(mr),
                "avg_latency_ms": round(sum(lats)/len(lats), 1),
                "min_ms": round(min(lats), 1),
                "max_ms": round(max(lats), 1),
                "total_tokens": toks,
                "tps": round(toks/sum(lats)*1000, 1) if sum(lats)>0 else 0,
                "skip_pct": round(sum(skips)/len(skips)*100, 1) if skips else 0,
            }

        bl_avg = summary["baseline"]["avg_latency_ms"]
        print("\n" + "=" * 60)
        print("快速基准报告")
        print("=" * 60)
        print(f"{'模式':<20} {'平均延迟':>10} {'Token/s':>8} {'跳过率':>7}")
        print("-" * 50)
        for m in ["baseline", "antenna", "wuxing", "full_stack"]:
            s = summary[m]
            label = {"baseline":"纯Ollama","antenna":"蚁触+Ollama","wuxing":"五行+Ollama","full_stack":"全栈"}[m]
            print(f"{label:<20} {s['avg_latency_ms']:>8.0f}ms {s['tps']:>6.1f} {s['skip_pct']:>5.1f}%")

        print(f"\n相对基准额外开销:")
        for m in ["antenna", "wuxing", "full_stack"]:
            s = summary[m]
            diff = s["avg_latency_ms"] - bl_avg
            pct = diff / bl_avg * 100 if bl_avg > 0 else 0
            label = {"antenna":"蚁触","wuxing":"五行","full_stack":"全栈"}[m]
            print(f"  {label}: +{diff:.1f}ms ({pct:+.1f}%)")

        full_skip = summary["full_stack"].get("skip_pct", 0)
        print(f"\n📊 蚁触理论节能: {full_skip:.1f}% 跳过率 → ~{full_skip:.1f}% 计算节省")

        report = {"status": "complete", "model": MODEL_NAME, "summary": summary}
        rpath = os.path.join(BASE, "tests", "benchmark_report.json")
        with open(rpath, 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n报告: {rpath}")
        return report

if __name__ == "__main__":
    QuickBenchmark().run()
