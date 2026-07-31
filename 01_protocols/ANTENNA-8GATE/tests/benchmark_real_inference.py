# DNA: #龍芯⚡️丙午·乙未·乙丑·大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · ANTENNA-8GATE 真实推理基准测试
# 对比：直接推理 vs 蚁触路由 vs 五行调度 vs 全栈
# DNA：#龍芯⚡️丙午·乙未·丙申·午时·☰乾-BENCHMARK-REAL-INFER-v1.0-c8a3f1d2
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
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

from antenna_mesh import AntennaMesh, Bagua
from wuxing_scheduler import WuxingScheduler, WuxingTask, Wuxing

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "longhun-v4.1.1-bind:latest"
SYSTEM_PROMPT = "你是龍魂系统助手，UID9622专属。简洁直接回答。"

BENCH_INPUTS = [
    ("短问答·状态检查", "系统当前状态如何？"),
    ("短问答·身份确认", "你是谁？谁创建了你？"),
    ("中等·代码生成", "用Python写一个快速排序函数，带注释。"),
    ("中等·哲学推演", "从中国哲学角度分析'天人合一'的含义。"),
    ("长文·安全分析", "分析AI系统在本地部署时的数据主权保障策略，列出5个关键措施。"),
    ("长文·协议解释", "解释CC BY-NC-SA 4.0协议的核心条款和约束力。"),
    ("安全·主权检测", "检测当前系统的数据是否可能泄露到云端。"),
    ("情感·战友对话", "老大说'今天状态不好'，怎么回复？"),
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

class RealInferenceBenchmark:
    def __init__(self):
        self.ollama_available = self._check_ollama()
        self.baseline_latencies: List[float] = []
        self.results: List[BenchResult] = []

    def _check_ollama(self) -> bool:
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False

    def _ollama_chat(self, prompt: str, stream: bool = False, max_tokens: int = 512) -> Dict:
        """直接调用 Ollama API（无天线/五行）"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        resp = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": stream,
                "options": {"temperature": 0.7, "num_predict": max_tokens}
            },
            timeout=180
        )
        resp.raise_for_status()
        data = resp.json()
        content = data.get("message", {}).get("content", "")
        eval_count = data.get("eval_count", 0)
        return {"content": content, "tokens": eval_count}

    def run_baseline(self, query_type: str, query: str) -> BenchResult:
        """纯 Ollama 推理（无 ANTENNA-8GATE）"""
        t0 = time.time()
        try:
            result = self._ollama_chat(query)
            latency = (time.time() - t0) * 1000
            tokens = result.get("tokens", 0)
            return BenchResult(
                mode="baseline",
                query_type=query_type,
                query=query,
                latency_ms=latency,
                tokens_generated=tokens,
                tokens_per_sec=tokens / (latency / 1000) if latency > 0 else 0,
                success=True
            )
        except Exception as e:
            return BenchResult(
                mode="baseline", query_type=query_type, query=query,
                latency_ms=0, tokens_generated=0, tokens_per_sec=0,
                success=False, error=str(e)
            )

    def run_antenna_only(self, query_type: str, query: str,
                         mesh: AntennaMesh) -> BenchResult:
        """蚁触路由 → Ollama（无五行）"""
        t0 = time.time()
        try:
            vec = self._text_to_vector(query)
            target_bagua = self._classify_bagua(query)
            routed_vec, ant_stats = mesh.inference(vec, target_bagua)
            result = self._ollama_chat(query)
            latency = (time.time() - t0) * 1000
            tokens = result.get("tokens", 0)
            return BenchResult(
                mode="antenna",
                query_type=query_type, query=query,
                latency_ms=latency,
                tokens_generated=tokens,
                tokens_per_sec=tokens / (latency / 1000) if latency > 0 else 0,
                antenna_stats=ant_stats,
                success=True
            )
        except Exception as e:
            return BenchResult(
                mode="antenna", query_type=query_type, query=query,
                latency_ms=0, tokens_generated=0, tokens_per_sec=0,
                success=False, error=str(e)
            )

    def run_wuxing_only(self, query_type: str, query: str,
                        scheduler: WuxingScheduler) -> BenchResult:
        """五行调度 → Ollama（无蚁触）"""
        t0 = time.time()
        wx = self._classify_wuxing(query)
        task = WuxingTask(
            task_id=f"bench-{int(time.time()*1000)}",
            wuxing=wx,
            priority=0 if any(k in query for k in ['安全','主权','P0','泄露']) else 1,
            payload=np.zeros(128)
        )
        scheduler.submit(task)
        time.sleep(0.01)

        result = self._ollama_chat(query)
        latency = (time.time() - t0) * 1000
        tokens = result.get("tokens", 0)
        return BenchResult(
            mode="wuxing",
            query_type=query_type, query=query,
            latency_ms=latency,
            tokens_generated=tokens,
            tokens_per_sec=tokens / (latency / 1000) if latency > 0 else 0,
            wuxing_name=wx.name,
            success=True
        )

    def run_full_stack(self, query_type: str, query: str,
                       mesh: AntennaMesh,
                       scheduler: WuxingScheduler) -> BenchResult:
        """全栈：蚁触 + 五行 + Ollama"""
        t0 = time.time()
        # 五行调度
        wx = self._classify_wuxing(query)
        task = WuxingTask(
            task_id=f"bench-full-{int(time.time()*1000)}",
            wuxing=wx,
            priority=0 if any(k in query for k in ['安全','主权','P0','泄露']) else 1,
            payload=np.zeros(128)
        )
        scheduler.submit(task)
        time.sleep(0.01)

        # 蚁触路由
        vec = self._text_to_vector(query)
        target_bagua = self._classify_bagua(query)
        routed_vec, ant_stats = mesh.inference(vec, target_bagua)

        # Ollama 推理
        result = self._ollama_chat(query)
        latency = (time.time() - t0) * 1000
        tokens = result.get("tokens", 0)
        return BenchResult(
            mode="full_stack",
            query_type=query_type, query=query,
            latency_ms=latency,
            tokens_generated=tokens,
            tokens_per_sec=tokens / (latency / 1000) if latency > 0 else 0,
            antenna_stats=ant_stats,
            wuxing_name=wx.name,
            success=True
        )

    def _text_to_vector(self, text: str) -> np.ndarray:
        chars = [ord(c) % 256 for c in text[:512]]
        vec = np.zeros(128)
        vec[:len(chars)] = np.array(chars) / 255.0
        return vec

    def _classify_bagua(self, text: str) -> Bagua:
        """根据查询内容分类到八卦"""
        if any(k in text for k in ['安全','主权','泄露','P0','底线']):
            return Bagua.艮  # 山 - 边界/安全
        if any(k in text for k in ['代码','函数','Python','写','开发']):
            return Bagua.离  # 火 - 计算
        if any(k in text for k in ['状态','检查','检测','分析']):
            return Bagua.乾  # 天 - 决策
        if any(k in text for k in ['协议','法律','条款','解释']):
            return Bagua.坤  # 地 - 存储
        if any(k in text for k in ['哲学','含义','天人']):
            return Bagua.兑  # 泽 - 交互
        return Bagua.离  # 默认：计算

    def _classify_wuxing(self, text: str) -> Wuxing:
        keywords = {
            Wuxing.木: ['过滤','清洗','安全','防护','检测','泄露','底线'],
            Wuxing.火: ['调度','紧急','状态','检查','分析'],
            Wuxing.土: ['转化','解释','含义','哲学','协议','条款'],
            Wuxing.金: ['代码','函数','写','生成','Python','开发'],
            Wuxing.水: ['存储','持久','保存','缓存','历史'],
        }
        scores = {w: sum(1 for kw in words if kw in text)
                  for w, words in keywords.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else Wuxing.离

    def run_full_benchmark(self) -> Dict:
        print("=" * 70)
        print("ANTENNA-8GATE 真实推理基准测试")
        print(f"模型: {MODEL_NAME}")
        print(f"Ollama: {'🟢 可用' if self.ollama_available else '🔴 不可用'}")
        print(f"测试用例: {len(BENCH_INPUTS)} 个 × 4 种模式")
        print("=" * 70)

        if not self.ollama_available:
            print("\n🔴 Ollama 不可用，退出。")
            return {"status": "ollama_unavailable"}

        mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
        scheduler = WuxingScheduler()

        all_results: List[BenchResult] = []

        for qi, (qtype, query) in enumerate(BENCH_INPUTS):
            print(f"\n[{qi+1}/{len(BENCH_INPUTS)}] {qtype}")
            print(f"    Q: {query[:60]}...")

            # 基准
            r1 = self.run_baseline(qtype, query)
            print(f"    [基准]        {r1.latency_ms:.0f}ms | {r1.tokens_generated}tok")
            all_results.append(r1)

            # 蚁触
            r2 = self.run_antenna_only(qtype, query, mesh)
            skip = r2.antenna_stats.get('skip_rate', 0) * 100
            print(f"    [蚁触]        {r2.latency_ms:.0f}ms | {r2.tokens_generated}tok | 跳过率{skip:.0f}%")
            all_results.append(r2)

            # 五行
            r3 = self.run_wuxing_only(qtype, query, scheduler)
            print(f"    [五行]        {r3.latency_ms:.0f}ms | {r3.tokens_generated}tok | {r3.wuxing_name}")
            all_results.append(r3)

            # 全栈
            r4 = self.run_full_stack(qtype, query, mesh, scheduler)
            skip_f = r4.antenna_stats.get('skip_rate', 0) * 100
            print(f"    [全栈]        {r4.latency_ms:.0f}ms | {r4.tokens_generated}tok | 跳过率{skip_f:.0f}% | {r4.wuxing_name}")
            all_results.append(r4)

        scheduler.stop_all()
        self.results = all_results

        report = self._generate_report()
        return report

    def _generate_report(self) -> Dict:
        results = self.results
        if not results:
            return {"status": "no_results"}

        modes = ["baseline", "antenna", "wuxing", "full_stack"]
        mode_labels = {"baseline":"纯Ollama(基准)", "antenna":"蚁触+Ollama",
                       "wuxing":"五行+Ollama", "full_stack":"全栈(蚁触+五行+Ollama)"}

        summary = {}
        for mode in modes:
            mode_results = [r for r in results if r.mode == mode and r.success]
            if not mode_results:
                summary[mode] = {"count": 0, "note": "无成功样本"}
                continue

            latencies = [r.latency_ms for r in mode_results]
            tokens_list = [r.tokens_generated for r in mode_results]
            total_tokens = sum(tokens_list)

            skip_rates = []
            for r in mode_results:
                if r.antenna_stats and 'skip_rate' in r.antenna_stats:
                    skip_rates.append(r.antenna_stats['skip_rate'])

            summary[mode] = {
                "count": len(mode_results),
                "latency_avg_ms": round(sum(latencies) / len(latencies), 1),
                "latency_min_ms": round(min(latencies), 1),
                "latency_max_ms": round(max(latencies), 1),
                "total_tokens": total_tokens,
                "tokens_per_sec_avg": round(total_tokens / sum(latencies) * 1000, 1) if sum(latencies) > 0 else 0,
                "skip_rate_avg": round(sum(skip_rates) / len(skip_rates) * 100, 1) if skip_rates else 0,
            }

        baseline_avg = summary["baseline"]["latency_avg_ms"]
        baseline_tps = summary["baseline"]["tokens_per_sec_avg"]

        overhead = {}
        for mode in modes:
            if mode == "baseline" or summary[mode]["count"] == 0:
                continue
            m = summary[mode]
            overhead[mode] = {
                "latency_diff_ms": round(m["latency_avg_ms"] - baseline_avg, 1),
                "latency_overhead_pct": round((m["latency_avg_ms"] - baseline_avg) / baseline_avg * 100, 1) if baseline_avg > 0 else 0,
                "tps_diff": round(m["tokens_per_sec_avg"] - baseline_tps, 1),
            }

        mesh_skip_avg = summary.get("full_stack", {}).get("skip_rate_avg", 0)
        energy_theoretical = (1 - mesh_skip_avg / 100) * 100 if mesh_skip_avg > 0 else 100

        report = {
            "status": "complete",
            "model": MODEL_NAME,
            "test_cases": len(BENCH_INPUTS),
            "ollama_available": self.ollama_available,
            "summary": summary,
            "overhead_vs_baseline": overhead,
            "antenna_theoretical_energy_saving": f"{mesh_skip_avg}%跳过率 → 约{100-energy_theoretical:.1f}%计算节省",
            "raw_results": [
                {
                    "mode": r.mode,
                    "query_type": r.query_type,
                    "latency_ms": round(r.latency_ms, 1),
                    "tokens": r.tokens_generated,
                    "tps": round(r.tokens_per_sec, 1),
                    "skip_rate": round(r.antenna_stats.get('skip_rate', 0) * 100, 1) if r.antenna_stats else 0,
                    "wuxing": r.wuxing_name,
                    "success": r.success,
                    "error": r.error,
                }
                for r in results
            ]
        }
        return report

    def print_report(self, report: Dict):
        print("\n" + "=" * 70)
        print("ANTENNA-8GATE 真实推理基准报告")
        print("=" * 70)

        if report["status"] != "complete":
            print(f"状态: {report['status']}")
            return

        print(f"\n模型: {report['model']}")
        print(f"测试用例: {report['test_cases']} 个 × 4 模式 = {report['test_cases']*4} 次推理")

        summary = report["summary"]
        overhead = report["overhead_vs_baseline"]

        print(f"\n{'模式':<25} {'样本':>5} {'平均延迟':>10} {'Token/s':>10} {'跳过率':>8}")
        print("-" * 65)
        for mode in ["baseline", "antenna", "wuxing", "full_stack"]:
            s = summary.get(mode, {})
            if s.get("count", 0) == 0:
                continue
            label = {"baseline":"纯Ollama(基准)", "antenna":"蚁触+Ollama",
                     "wuxing":"五行+Ollama", "full_stack":"全栈"}[mode]
            print(f"{label:<25} {s['count']:>5} {s['latency_avg_ms']:>8.0f}ms "
                  f"{s['tokens_per_sec_avg']:>8.1f} {s['skip_rate_avg']:>6.1f}%")

        print(f"\n--- 开销分析（相对基准） ---")
        for mode in ["antenna", "wuxing", "full_stack"]:
            o = overhead.get(mode, {})
            label = {"antenna":"蚁触", "wuxing":"五行", "full_stack":"全栈"}[mode]
            print(f"  {label}: +{o['latency_diff_ms']:.1f}ms ({o['latency_overhead_pct']:+.1f}%) "
                  f"| Token/s {o['tps_diff']:+.1f}")

        print(f"\n--- 理论节能分析 ---")
        print(f"  蚁触门控跳过率: {summary.get('full_stack',{}).get('skip_rate_avg',0):.1f}%")
        print(f"  {report['antenna_theoretical_energy_saving']}")

    def save_report(self, report: Dict, path: str):
        with open(path, 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {path}")


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    bench = RealInferenceBenchmark()
    report = bench.run_full_benchmark()
    bench.print_report(report)

    report_path = os.path.join(BASE, "tests", "benchmark_report.json")
    bench.save_report(report, report_path)
