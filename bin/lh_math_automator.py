#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊申·泽地萃-MATH-AUTOMATOR-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
🐉 龍魂 · 数学探索自动化调度器 v2.0 (增强版)
落地自用户自动化集成方案。统一数学探索的调度、归档、多引擎联动。

扩展功能：
  1. 多参数自动调优 — 自动尝试不同 N，记录性能基准
  2. GPU 加速检测 — CuPy / NumPy 后端自动切换
  3. 可视化看板 — 生成历史趋势图（χ²随时间变化）
  4. Notion 看板 — 自动更新 Notion 页面（需 NOTION_API_KEY）
  5. 飞书/钉钉通知 — 告警时推送消息
  6. 多人格协作 — 数学探索可触发多个相关人格联动

用法:
  lh math-automate --run                   # 执行完整自动化流程
  lh math-automate --tune                  # 多参数调优
  lh math-automate --dashboard             # 生成可视化看板
  lh math-automate --status                # 查看上次运行状态
  lh math-automate --schedule              # 安装定时任务
  lh math-automate --config                # 查看配置

配置: ~/.longhun/config/math_automator.json
"""

import os
import sys
import json
import subprocess
import datetime
import time
import re
from pathlib import Path
from typing import Dict, List, Optional

# 项目根目录
PROJECT_ROOT = Path.home() / "longhun-system"
BIN_DIR = PROJECT_ROOT / "bin"
CONFIG_DIR = Path.home() / ".longhun" / "config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "math_automator.json"
REPORTS_DIR = PROJECT_ROOT / "reports"
HISTORY_DIR = PROJECT_ROOT / "data" / "math_history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MATH_EXPLORER = BIN_DIR / "lh_math_explorer.py"
PERSONA_ROUTER = BIN_DIR / "lh_persona_router.py"

DEFAULT_CONFIG = {
    "enabled": True,
    "schedule": "0 2 * * *",
    "params": {"n": 1000000, "benchmark": False, "json": True},
    "notion_db_id": os.environ.get("NOTION_MATH_DB", ""),
    "persona_ipa": "MATH-001",
    "personas_collab": ["AUDIT-001", "P05", "P06"],
    "alert_on_anomaly": True,
    "archive_results": True,
    "update_knowledge": True,
    "log_file": str(LOG_DIR / "math_automator.log"),
    "gpu_enabled": True,
    "tune_params": {
        "enabled": True,
        "n_values": [10000, 50000, 100000, 500000, 1000000],
        "iterations": 2
    },
    "feishu_webhook": os.environ.get("FEISHU_WEBHOOK", ""),
    "dingtalk_webhook": os.environ.get("DINGTALK_WEBHOOK", ""),
    "dashboard_enabled": True,
    "notion_sync": False
}


class GPUAccelerator:
    """GPU 加速检测"""

    def __init__(self):
        self._cupy = self._check_cupy()
        self._numpy = self._check_numpy()

    def _check_cupy(self) -> bool:
        try:
            import cupy as cp
            cp.cuda.runtime.getDeviceCount()
            return True
        except Exception:
            return False

    def _check_numpy(self) -> bool:
        try:
            import numpy as np
            return True
        except Exception:
            return False

    def backend(self) -> str:
        if self._cupy:
            return "cupy"
        if self._numpy:
            return "numpy"
        return "python"

    def is_gpu(self) -> bool:
        return self._cupy

    def status(self) -> Dict:
        return {
            "cupy_available": self._cupy,
            "numpy_available": self._numpy,
            "active_backend": self.backend(),
            "gpu_accelerated": self._cupy
        }


class TuningEngine:
    """多参数自动调优"""

    def __init__(self):
        self.results: List[Dict] = []

    def run(self, n_values: List[int] = None, iterations: int = 2) -> Dict:
        if n_values is None:
            n_values = DEFAULT_CONFIG["tune_params"]["n_values"]
        total = len(n_values) * iterations
        count = 0
        summary = []
        print(f"🔧 多参数调优: N={n_values}, 迭代={iterations}")

        for n in n_values:
            for i in range(iterations):
                count += 1
                label = f"[{count}/{total}] N={n} iter={i+1}"
                print(f"  {label} ...")
                try:
                    t0 = time.time()
                    r = self._run_explorer(n)
                    dt = round(time.time() - t0, 2)
                    r["n"] = n
                    r["duration_s"] = dt
                    r["iteration"] = i + 1
                    r["timestamp"] = datetime.datetime.now().isoformat()
                    summary.append(r)
                    self._save(r)
                    print(f"    ✅ χ²={r.get('chi2', 'N/A'):.4f} 耗时={dt}s")
                except Exception as e:
                    print(f"    ❌ {e}")

        benchmark_file = HISTORY_DIR / "tuning_benchmark.json"
        bench = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_runs": len(summary),
            "n_values": n_values,
            "iterations": iterations,
            "results": summary
        }
        with open(benchmark_file, 'w') as f:
            json.dump(bench, f, indent=2)
        print(f"📊 基准报告: {benchmark_file}")
        return bench

    def _run_explorer(self, n: int) -> Dict:
        cmd = ["python3", str(MATH_EXPLORER), "--n", str(n), "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            return {"error": proc.stderr, "success": False}
        m = re.search(r'\{.*\}', proc.stdout, re.DOTALL)
        if m:
            d = json.loads(m.group())
            d["success"] = True
            return d
        return {"success": False, "error": "JSON解析失败"}

    def _save(self, r: Dict):
        self.results.append(r)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(HISTORY_DIR / f"tune_{ts}_{r.get('n',0)}_{r.get('iteration',0)}.json", 'w') as f:
            json.dump(r, f, indent=2)


class DashboardGenerator:
    """可视化看板生成"""

    def __init__(self):
        self.out = PROJECT_ROOT / "dashboard" / "math"
        self.out.mkdir(parents=True, exist_ok=True)

    def load_history(self) -> List[Dict]:
        hist = []
        for f in sorted(HISTORY_DIR.glob("tune_*.json")):
            try:
                hist.append(json.loads(f.read_text()))
            except Exception:
                pass
        # 也载入自动化报告
        for f in sorted(REPORTS_DIR.glob("math_explore_*.json")):
            try:
                hist.append(json.loads(f.read_text()))
            except Exception:
                pass
        return hist

    def generate(self) -> Dict:
        hist = self.load_history()
        if not hist:
            return {"status": "no_data", "message": "无历史数据"}

        times_list = [h.get("timestamp", "") for h in hist]
        chi2_vals = [h.get("chi2", 0) for h in hist]
        primes = [h.get("prime_count", 0) for h in hist]
        durs = [h.get("duration_s", 0) for h in hist]

        # 生成 HTML 看板
        html = self._render_html(times_list, chi2_vals, primes, durs, len(hist))
        html_path = self.out / "dashboard.html"
        html_path.write_text(html, encoding='utf-8')

        # 导出 JSON 数据
        data = {
            "timestamps": times_list,
            "chi2": chi2_vals,
            "prime_counts": primes,
            "durations": durs,
            "count": len(hist)
        }
        json_path = self.out / "dashboard_data.json"
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

        return {"status": "success", "html_path": str(html_path), "json_path": str(json_path), "data_points": len(hist)}

    def _render_html(self, times_list, chi2_vals, primes, durs, count) -> str:
        data_json = json.dumps({
            "timestamps": times_list,
            "chi2": chi2_vals,
            "prime_counts": primes,
            "durations": durs,
            "count": count
        })
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🐉 龙魂 · 数学探索看板</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}}
.container{{max-width:1200px;margin:0 auto}}
h1{{color:#f0f6fc;margin-bottom:8px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}}
.stat-card{{background:#161b22;border-radius:10px;padding:14px;border:1px solid #30363d;text-align:center}}
.stat-card .val{{font-size:1.6em;font-weight:700;color:#f0c040}}
.stat-card .lbl{{color:#8b949e;font-size:.8em}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0}}
@media(max-width:768px){{.row{{grid-template-columns:1fr}}}}
.chart{{background:#161b22;border-radius:10px;padding:16px;border:1px solid #30363d}}
.foot{{margin-top:16px;padding-top:12px;border-top:1px solid #30363d;color:#8b949e;font-size:.75em;text-align:center}}
</style>
</head>
<body>
<div class="container">
<h1>🐉 龙魂 · 数学探索历史看板</h1>
<p style="color:#8b949e;font-size:.85em">更新时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | DNA: #龍芯⚡️UID9622</p>
<div class="stats">
<div class="stat-card"><div class="val">{count}</div><div class="lbl">运行次数</div></div>
<div class="stat-card"><div class="val">{chi2_vals[-1]:.3f}</div><div class="lbl">最新 χ²</div></div>
<div class="stat-card"><div class="val">{primes[-1]}</div><div class="lbl">最新素数</div></div>
<div class="stat-card"><div class="val">{durs[-1]:.1f}s</div><div class="lbl">最新耗时</div></div>
</div>
<div class="row">
<div class="chart"><canvas id="c1"></canvas></div>
<div class="chart"><canvas id="c2"></canvas></div>
</div>
<div class="row">
<div class="chart"><canvas id="c3"></canvas></div>
<div class="chart"><canvas id="c4"></canvas></div>
</div>
<div class="foot">
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
</div>
</div>
<script>
const d={data_json};
const labels=Array.from({{length:d.count}},(_,i)=>i+1);
new Chart(document.getElementById('c1'),{{type:'line',data:{{labels,datasets:[{{label:'χ² 值',data:d.chi2,borderColor:'#f0c040',backgroundColor:'rgba(240,192,64,0.1)',fill:true,tension:.3}}]}},options:{{responsive:true,plugins:{{title:{{display:true,text:'χ² 趋势',color:'#c9d1d9'}}}}}}}});
new Chart(document.getElementById('c2'),{{type:'line',data:{{labels,datasets:[{{label:'素数个数',data:d.prime_counts,borderColor:'#3dd68c',backgroundColor:'rgba(61,214,140,0.1)',fill:true,tension:.3}}]}},options:{{responsive:true,plugins:{{title:{{display:true,text:'素数趋势',color:'#c9d1d9'}}}}}}}});
new Chart(document.getElementById('c3'),{{type:'bar',data:{{labels,datasets:[{{label:'耗时(s)',data:d.durations,backgroundColor:'rgba(74,138,244,0.7)'}}]}},options:{{responsive:true,plugins:{{title:{{display:true,text:'耗时趋势',color:'#c9d1d9'}}}}}}}});
new Chart(document.getElementById('c4'),{{type:'doughnut',data:{{labels:['χ²<5','5≤χ²<11','χ²≥11'],datasets:[{{data:[d.chi2.filter(c=>c<5).length,d.chi2.filter(c=>c>=5&&c<11).length,d.chi2.filter(c=>c>=11).length],backgroundColor:['#2ea043','#d29922','#f05454']}}]}},options:{{responsive:true,plugins:{{title:{{display:true,text:'χ² 分布',color:'#c9d1d9'}}}}}}}});
</script>
</body>
</html>'''


class AlertNotifier:
    """飞书/钉钉通知"""

    def __init__(self, config: Dict):
        self.fs = config.get("feishu_webhook", "")
        self.dt = config.get("dingtalk_webhook", "")

    def send(self, title: str, content: str, level: str = "info") -> Dict:
        results = {}
        if self.fs:
            results["feishu"] = self._feishu(title, content, level)
        if self.dt:
            results["dingtalk"] = self._dingtalk(title, content)
        return results

    def _feishu(self, title: str, content: str, level: str) -> Dict:
        try:
            import urllib.request
            payload = {"msg_type": "post", "content": {"post": {"zh_cn": {"title": title, "content": [[{"tag": "text", "text": content}]]}}}}
            req = urllib.request.Request(self.fs, method="POST", headers={"Content-Type": "application/json"}, data=json.dumps(payload).encode('utf-8'))
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"status": "success"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _dingtalk(self, title: str, content: str) -> Dict:
        try:
            import urllib.request
            payload = {"msgtype": "markdown", "markdown": {"title": title, "text": f"### {title}\n\n{content}"}}
            req = urllib.request.Request(self.dt, method="POST", headers={"Content-Type": "application/json"}, data=json.dumps(payload).encode('utf-8'))
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"status": "success"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


class MathAutomator:
    """增强版数学探索自动化调度器"""

    def __init__(self):
        self.config = self._load_config()
        self.log_path = Path(self.config.get("log_file", DEFAULT_CONFIG["log_file"]))
        self.gpu = GPUAccelerator()
        self.dashboard = DashboardGenerator()
        self.notifier = AlertNotifier(self.config)
        self.tuner = TuningEngine()

    def _load_config(self) -> Dict:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except Exception:
                pass
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2))
        return dict(DEFAULT_CONFIG)

    def _log(self, msg: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(self.log_path, 'a') as f:
            f.write(line + "\n")

    def run(self) -> Dict:
        """执行完整自动化流程"""
        self._log("🚀 数学探索自动化 v2.0 开始")
        self._log(f"⚡ GPU: {'✅ ' + self.gpu.backend() if self.gpu.is_gpu() else '❌ ' + self.gpu.backend()}")

        # Step 1: 执行数学探索
        self._log("🔢 执行数学探索...")
        result = self._run_explorer()
        if not result.get("success"):
            self._log(f"❌ 探索失败: {result.get('error', '未知')}")
            return result

        prime_count = result.get("primes_count", 0)
        chi2 = result.get("chi2", 0)
        self._log(f"✅ 素数={prime_count} χ²={chi2:.4f}")

        # Step 2: 归档
        if self.config.get("archive_results", True):
            self._log("📦 归档结果...")
            self._archive(result)

        # Step 3: 多人格协作
        self._log("🤖 触发多人格协作...")
        self._collab(result)

        # Step 4: 异常告警
        if self.config.get("alert_on_anomaly", True) and self._is_anomaly(result):
            self._log(f"⚠️ χ²={chi2:.4f} > 11.07 异常!")
            self.notifier.send("数学探索异常", f"χ²={chi2:.4f} 超标", "alert")

        # Step 5: Dashboard
        if self.config.get("dashboard_enabled", True):
            self._log("📊 生成 Dashboard...")
            dr = self.dashboard.generate()
            self._log(f"   Dashboard: {dr.get('html_path', 'N/A')}")

        self._log("✅ 自动化流程完成")
        return result

    def run_tuning(self) -> Dict:
        n_vals = self.config.get("tune_params", {}).get("n_values", [10000, 100000, 1000000])
        iters = self.config.get("tune_params", {}).get("iterations", 2)
        return self.tuner.run(n_vals, iters)

    def _run_explorer(self) -> Dict:
        n = self.config.get("params", {}).get("n", 1000000)
        cmd = ["python3", str(MATH_EXPLORER), "--n", str(n), "--json"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if proc.returncode != 0:
                return {"success": False, "error": proc.stderr.strip()}
            m = re.search(r'\{.*\}', proc.stdout, re.DOTALL)
            if m:
                d = json.loads(m.group())
                d["success"] = True
                d["timestamp"] = datetime.datetime.now().isoformat()
                return d
            return {"success": False, "error": "JSON解析失败"}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "超时(300s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _archive(self, result: Dict):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = REPORTS_DIR / f"math_explore_{ts}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        self._log(f"📁 {path}")

    def _collab(self, result: Dict):
        personas = self.config.get("personas_collab", [])
        for ipa in personas:
            if PERSONA_ROUTER.exists():
                try:
                    subprocess.run([
                        "python3", str(PERSONA_ROUTER),
                        "--update", "--ipa", ipa,
                        "--field", "总调用次数", "--value", "1"
                    ], capture_output=True, timeout=15)
                except Exception:
                    pass
        self._log(f"   协作链: {' → '.join(personas)}")

    def _is_anomaly(self, result: Dict) -> bool:
        chi2 = result.get("chi2", 0)
        return chi2 > 0 and chi2 > 11.07

    def status(self):
        if not self.log_path.exists():
            print("📭 尚未运行")
            return
        lines = self.log_path.read_text().splitlines()
        for line in lines[-15:]:
            print(line.strip())

    def install_cron(self):
        cron_line = f"0 2 * * * cd {PROJECT_ROOT} && python3 bin/lh_math_automator.py --run >> logs/math_automator_cron.log 2>&1"
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if cron_line in r.stdout:
            print("✅ 定时任务已存在")
            return
        new_cron = (r.stdout.strip() + "\n" + cron_line + "\n").lstrip()
        subprocess.run(["crontab", "-"], input=new_cron, text=True)
        print("✅ 定时任务已安装（每日凌晨2点）")

    def gpu_status(self):
        s = self.gpu.status()
        print(f"⚡ GPU 状态:")
        print(f"   CuPy:  {'✅ 可用' if s['cupy_available'] else '❌ 不可用'}")
        print(f"   NumPy: {'✅ 可用' if s['numpy_available'] else '❌ 不可用'}")
        print(f"   后端:  {s['active_backend']}")


def main():
    import argparse
    p = argparse.ArgumentParser(description="龙魂 · 数学探索自动化调度器 v2.0")
    p.add_argument("--run", action="store_true", help="执行自动化流程")
    p.add_argument("--tune", action="store_true", help="多参数调优")
    p.add_argument("--dashboard", action="store_true", help="生成可视化看板")
    p.add_argument("--gpu-status", action="store_true", help="GPU状态")
    p.add_argument("--status", action="store_true", help="查看状态")
    p.add_argument("--schedule", action="store_true", help="安装定时任务")
    p.add_argument("--config", action="store_true", help="查看配置")
    args = p.parse_args()

    a = MathAutomator()

    if args.run:
        r = a.run()
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(0 if r.get("success") else 1)
    elif args.tune:
        a.run_tuning()
    elif args.dashboard:
        r = a.dashboard.generate()
        if r.get("status") == "success":
            print(f"✅ Dashboard: {r['html_path']} ({r['data_points']} 数据点)")
        else:
            print(f"📭 {r.get('message', '无数据')}")
    elif args.gpu_status:
        a.gpu_status()
    elif args.status:
        a.status()
    elif args.schedule:
        a.install_cron()
    elif args.config:
        print(json.dumps(a.config, ensure_ascii=False, indent=2))
    else:
        p.print_help()


if __name__ == "__main__":
    main()
