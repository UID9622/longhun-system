#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一控制台 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-UNIFIED-CONSOLE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能: Web仪表盘（暗色龍魂金主题） + CLI状态汇总 + API端点
用法:
  lh 控制台 --web           启动Web仪表盘（端口8999）
  lh 控制台 --status        CLI一键状态汇总
  lh 控制台 --api           仅启动API（无前端）
联动: lh_engine_verify.py（引擎状态数据源）/ lh_alert_engine.py（告警触发）
端口: 8999（量子卦象9000·避免冲突）
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List

# 确保能 import 同目录引擎
sys.path.insert(0, str(Path(__file__).resolve().parent))

DEFAULT_PORT = 8999

# ═══════════════════════════════════════════════════
#  Web仪表盘 HTML（暗色龍魂金主题·单页SPA·每30s自动刷新）
# ═══════════════════════════════════════════════════
CONSOLE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🐉 龍魂 · 统一控制台</title>
<style>
:root {
  --bg: #0d1117; --card: #161b22; --border: #30363d;
  --text: #c9d1d9; --text-dim: #8b949e; --head: #f0f6fc;
  --gold: #d4a843; --gold-bright: #f0c060;
  --green: #2ea043; --yellow: #d29922; --red: #f05454;
  --accent: #58a6ff;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);padding:20px;min-height:100vh}
h1{color:var(--head);font-size:1.6em;margin-bottom:4px}
h1 span{color:var(--gold-bright)}
.subtitle{color:var(--text-dim);font-size:0.85em;margin-bottom:24px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:24px}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 16px;text-align:center}
.stat-card .num{font-size:2.2em;font-weight:700}
.stat-card .label{font-size:0.8em;color:var(--text-dim);margin-top:4px;text-transform:uppercase;letter-spacing:1px}
.stat-card.green{border-color:var(--green)} .stat-card.green .num{color:var(--green)}
.stat-card.yellow{border-color:var(--yellow)} .stat-card.yellow .num{color:var(--yellow)}
.stat-card.red{border-color:var(--red)} .stat-card.red .num{color:var(--red)}
.stat-card.gold{border-color:var(--gold)} .stat-card.gold .num{color:var(--gold-bright)}

.bar-wrap{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:24px}
.bar-title{font-size:0.8em;color:var(--text-dim);margin-bottom:8px;text-transform:uppercase;letter-spacing:1px}
.bar{height:10px;background:#21262d;border-radius:5px;overflow:hidden}
.bar-inner{height:100%;border-radius:5px;transition:width 0.6s ease}
.bar-inner.green{background:linear-gradient(90deg,var(--green),#3fb950)}
.bar-inner.yellow{background:linear-gradient(90deg,var(--yellow),#e3b341)}
.bar-inner.red{background:linear-gradient(90deg,var(--red),#ff6b6b)}

table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden}
th{text-align:left;padding:10px 14px;background:#1c2128;color:var(--text-dim);font-size:0.78em;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid var(--border)}
td{padding:10px 14px;border-bottom:1px solid var(--border);font-size:0.9em}
tr:last-child td{border-bottom:none}
tr:hover{background:#1c2128}
td.status{font-size:1.2em;text-align:center}
td.url{font-size:0.78em;color:var(--text-dim);font-family:monospace;max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

.footer{text-align:center;color:var(--text-dim);font-size:0.72em;margin-top:30px;padding-top:16px;border-top:1px solid var(--border)}
.footer span{color:var(--gold)}
.refresh{display:inline-block;margin-left:8px;font-size:0.75em;color:var(--accent);cursor:pointer}
.error-msg{background:#2d1518;border:1px solid var(--red);border-radius:8px;padding:16px;margin-bottom:20px;display:none}
.error-msg.show{display:block}

/* 响应式 */
@media(max-width:600px){
  body{padding:12px}
  .grid2{grid-template-columns:repeat(2,1fr);gap:8px}
  td.url{max-width:120px}
}
</style>
</head>
<body>

<h1>🐉 <span>龍魂</span> · 统一控制台</h1>
<p class="subtitle">全引擎状态监控 · 实时三色审计 · 每30秒自动刷新 <span class="refresh" onclick="fetchStatus()">🔄 立即刷新</span></p>

<div class="error-msg" id="error">⚠️ 数据加载失败，请检查融合桥接服务</div>

<div class="grid2">
  <div class="stat-card green"><div class="num" id="count-green">--</div><div class="label">🟢 可用</div></div>
  <div class="stat-card yellow"><div class="num" id="count-yellow">--</div><div class="label">🟡 异常</div></div>
  <div class="stat-card red"><div class="num" id="count-red">--</div><div class="label">🔴 不可用</div></div>
  <div class="stat-card gold"><div class="num" id="count-total">--</div><div class="label">📊 总计</div></div>
</div>

<div class="bar-wrap">
  <div class="bar-title">系统健康度 <span id="health-pct" style="color:var(--gold-bright)">--</span></div>
  <div class="bar"><div class="bar-inner green" id="health-bar" style="width:0%"></div></div>
</div>

<table>
  <thead><tr><th>状态</th><th>引擎名称</th><th>端点</th></tr></thead>
  <tbody id="engine-table"><tr><td colspan="3" style="text-align:center;color:var(--text-dim)">加载中...</td></tr></tbody>
</table>

<div class="footer">
  龍魂系统 · UID9622 · 诸葛鑫 · <span>#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z</span><br>
  更新时间: <span id="update-time">--</span>
</div>

<script>
async function fetchStatus() {
  const errEl = document.getElementById('error');
  try {
    const resp = await fetch('/api/status');
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    errEl.classList.remove('show');

    const {engines=[], total=0, green=0, yellow=0, red=0, health_pct=0, timestamp} = data;

    document.getElementById('count-green').textContent = green;
    document.getElementById('count-yellow').textContent = yellow;
    document.getElementById('count-red').textContent = red;
    document.getElementById('count-total').textContent = total;
    document.getElementById('health-pct').textContent = Math.round(health_pct) + '%';

    const bar = document.getElementById('health-bar');
    bar.style.width = health_pct + '%';
    bar.className = 'bar-inner ' + (health_pct >= 80 ? 'green' : health_pct >= 50 ? 'yellow' : 'red');

    const tbody = document.getElementById('engine-table');
    tbody.innerHTML = engines.map(e => `
      <tr>
        <td class="status">${e.status||'🔴'}</td>
        <td>${e.name||'?'}</td>
        <td class="url" title="${e.url||''}">${e.url||'N/A'}</td>
      </tr>
    `).join('');

    const dt = new Date(timestamp * 1000);
    document.getElementById('update-time').textContent = dt.toLocaleString('zh-CN');
  } catch(e) {
    errEl.classList.add('show');
    errEl.innerHTML = '⚠️ 数据加载失败: ' + e.message;
  }
}

fetchStatus();
setInterval(fetchStatus, 30000);
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════
#  引擎状态获取
# ═══════════════════════════════════════════════════

def get_engine_status() -> Dict:
    """获取全量引擎状态（委托给 lh_engine_verify）"""
    try:
        from lh_engine_verify import ENGINES, check_engine
    except ImportError:
        return {"error": "lh_engine_verify.py 不可用", "engines": [], "total": 0,
                "green": 0, "yellow": 0, "red": 0, "health_pct": 0, "timestamp": time.time()}

    results = []
    for name, config in ENGINES.items():
        r = check_engine(name, config)
        results.append(r)

    total = len(results)
    green = sum(1 for r in results if r["status"] == "🟢")
    yellow = sum(1 for r in results if r["status"] == "🟡")
    red = sum(1 for r in results if r["status"] == "🔴")
    health_pct = (green / total * 100) if total > 0 else 0

    return {
        "engines": results,
        "total": total,
        "green": green,
        "yellow": yellow,
        "red": red,
        "health_pct": round(health_pct, 1),
        "timestamp": time.time(),
    }


# ═══════════════════════════════════════════════════
#  HTTP 请求处理器
# ═══════════════════════════════════════════════════

class ConsoleHandler(BaseHTTPRequestHandler):
    """统一控制台 HTTP 处理器"""

    def log_message(self, format, *args):
        """静默日志（避免刷屏）"""
        pass

    def _send_json(self, data: Dict, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html: str, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        if self.path == "/api/status":
            data = get_engine_status()
            self._send_json(data)
            return

        if self.path == "/api/health":
            self._send_json({"status": "ok", "service": "unified-console",
                             "timestamp": time.time()})
            return

        if self.path in ("/", "/index.html", ""):
            self._send_html(CONSOLE_HTML)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/alert":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)
                from lh_alert_engine import send_alert
                sent = send_alert(
                    data.get("title", "控制台告警"),
                    data.get("body", ""),
                    data.get("level", "warn"),
                )
                self._send_json({"success": True, "channels": sent})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        self.send_response(405)
        self.end_headers()


# ═══════════════════════════════════════════════════
#  启动函数
# ═══════════════════════════════════════════════════

def start_web(port: int = DEFAULT_PORT, api_only: bool = False):
    """启动Web服务器"""
    server = HTTPServer(("0.0.0.0", port), ConsoleHandler)
    mode = "API-only" if api_only else "仪表盘"
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  🐉 龍魂 · 统一控制台 {mode}模式                 ║")
    print(f"╠══════════════════════════════════════════════════╣")
    if not api_only:
        print(f"  🌐 仪表盘: http://localhost:{port}/")
    print(f"  📡 API:    http://localhost:{port}/api/status")
    print(f"  ❤️  健康:   http://localhost:{port}/api/health")
    print(f"╚══════════════════════════════════════════════════╝")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 控制台已关闭")
        server.shutdown()


def show_status():
    """CLI 状态汇总"""
    data = get_engine_status()
    if "error" in data:
        print(f"🔴 {data['error']}")
        return

    print("╔══════════════════════════════════════════════════╗")
    print("║        📊 龍魂 · 统一控制台状态                    ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"  🟢 {data['green']:2d}   🟡 {data['yellow']:2d}   🔴 {data['red']:2d}   📊 总计 {data['total']}")
    print(f"  健康度: {data['health_pct']}%")
    print("╠══════════════════════════════════════════════════╣")

    for e in data["engines"]:
        marker = e["status"]
        extra = ""
        if "error" in e:
            extra = f" — {e['error']}"
        elif "code" in e and e["code"] != 200:
            extra = f" (HTTP {e['code']})"
        print(f"  {marker} {e['name']:<18s}{extra}")

    print("╚══════════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════
#  CLI入口
# ═══════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂·统一控制台")
    parser.add_argument("--web", action="store_true", help="启动Web仪表盘")
    parser.add_argument("--api", action="store_true", help="仅启动API（无前端）")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"监听端口（默认: {DEFAULT_PORT}）")
    parser.add_argument("--status", action="store_true", help="CLI一键状态汇总")
    args = parser.parse_args()

    if args.web:
        start_web(args.port)
    elif args.api:
        start_web(args.port, api_only=True)
    elif args.status:
        show_status()
    else:
        # 默认无参数 = 显示CLI状态
        show_status()


if __name__ == "__main__":
    main()
