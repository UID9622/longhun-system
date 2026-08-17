#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂蚁群守护进程 v2.0 · Ant Colony Daemon
一键启动/管理蚁群引擎后台服务。

DNA: #龍芯⚡️丙午·辛未·ANT-COLONY-DAEMON-v2.0

用法:
  python3 bin/lh_ant_colony_daemon.py start        # 启动后台守护
  python3 bin/lh_ant_colony_daemon.py stop          # 停止
  python3 bin/lh_ant_colony_daemon.py status        # 查看状态
  python3 bin/lh_ant_colony_daemon.py metrics       # 完整指标 (JSON)
  python3 bin/lh_ant_colony_daemon.py health        # 健康检查 (JSON)
  python3 bin/lh_ant_colony_daemon.py dashboard     # 仪表盘
  python3 bin/lh_ant_colony_daemon.py serve --port 9677  # HTTP 服务模式
"""

import sys
import os
import time
import json
import signal
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·ANT-COLONY-DAEMON-v2.0"
CST = timezone(timedelta(hours=8))

PID_FILE = ROOT / "var" / "ant_colony_daemon.pid"


def get_runtime(verbose: bool = True):
    from engine.ant_colony.runtime import get_runtime as _get
    return _get(verbose=verbose)


def write_pid(pid: int):
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(pid))


def read_pid() -> int:
    if PID_FILE.exists():
        return int(PID_FILE.read_text().strip())
    return 0


def is_running() -> bool:
    pid = read_pid()
    if pid == 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        PID_FILE.unlink(missing_ok=True)
        return False


def cmd_start(args):
    if is_running():
        print(f"  🟡 蚁群守护进程已在运行 (PID={read_pid()})")
        return

    runtime = get_runtime()
    runtime.start()
    write_pid(os.getpid())

    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🐜 龍魂蚁群守护进程 v2.0 · 已启动                  ║
╠══════════════════════════════════════════════════════════╣
║     PID: {os.getpid():<6}    Tick: {runtime.TICK_INTERVAL}s                    ║
║     {DNA}
╚══════════════════════════════════════════════════════════╝
""")
    print(runtime.snapshot().summary())

    # 保持运行
    def _cleanup(sig, frame):
        print("\n  🛑 停止蚁群守护进程...")
        runtime.stop()
        PID_FILE.unlink(missing_ok=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, _cleanup)
    signal.signal(signal.SIGTERM, _cleanup)

    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        _cleanup(None, None)


def cmd_stop(args):
    if not is_running():
        print("  🟡 蚁群守护进程未在运行")
        return
    pid = read_pid()
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        if is_running():
            os.kill(pid, signal.SIGKILL)
        PID_FILE.unlink(missing_ok=True)
        print(f"  ✅ 已停止 (PID={pid})")
    except OSError as e:
        print(f"  ❌ 停止失败: {e}")


def cmd_status(args):
    if is_running():
        runtime = get_runtime()
        state = runtime.snapshot()
        print(f"\n{state.summary()}\n")
        print(f"  PID: {read_pid()}  ·  运行中 🟢")
        print(f"  快照时间: {state.timestamp}")
    else:
        print(f"\n  🔴 蚁群守护进程未运行\n")


def cmd_metrics(args):
    runtime = get_runtime()
    if not is_running():
        runtime.start()
        time.sleep(1.5)
    print(json.dumps(runtime.get_metrics(), indent=2, ensure_ascii=False))


def cmd_health(args):
    runtime = get_runtime()
    if not is_running():
        runtime.start()
        time.sleep(1.5)
    print(json.dumps(runtime.get_health(), ensure_ascii=False))


def cmd_dashboard(args):
    """显示仪表盘"""
    runtime = get_runtime()
    if not is_running():
        runtime.start()
        time.sleep(2)

    state = runtime.snapshot()
    w = 64

    print(f"""
╔{'═'*w}╗
║{'🐜 龍魂蚁群仪表盘 v2.0':^{w}}║
╠{'═'*w}╣
║  Tick: {state.tick_count:<6}  {'运行中 🟢' if is_running() else '已停止 🔴':>{w-24}}║
║  涌现质量: E={state.emergence_E:.4f} ({state.emergence_grade}){'':>{w-29-len(state.emergence_grade)}}║
╠{'═'*w}╣
║  种群分布{'':^{w-10}}║""")

    total_modules = sum(state.population_distribution.values()) or 1
    for pop, count in sorted(state.population_distribution.items()):
        bar_len = int((count / total_modules) * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"║  {pop:<6} [{bar}] {count}{'':>{w-47}}║")

    print(f"╠{'═'*w}╣")
    print(f"║  信息素浓度{'':^{w-10}}║")

    max_conc = max(state.pheromone_concentration.values()) if state.pheromone_concentration else 1
    for ptype, conc in state.pheromone_concentration.items():
        bar_len = int((conc / (max_conc or 1)) * 30)
        bar = "▓" * bar_len + "░" * (30 - bar_len)
        print(f"║  {ptype:<10} [{bar}] {conc:6.1f}{'':>{w-52}}║")

    print(f"╠{'═'*w}╣")
    print(f"║  信号统计{'':^{w-10}}║")
    print(f"║  发送: {state.total_signals_sent:<6}  阻断: {state.total_signals_blocked}{'':>{w-36}}║")
    print(f"║  信息素轨迹: {state.pheromone_trails} 条{'':>{w-24}}║")

    if state.top_paths:
        print(f"╠{'═'*w}╣")
        print(f"║  Top 信息素路径{'':^{w-13}}║")
        for i, p in enumerate(state.top_paths[:5], 1):
            path = p.get("path", "?")
            strength = p.get("strength", 0)
            print(f"║  {i}. {path[:40]:<40} {strength:6.1f}{'':>{w-54}}║")

    print(f"╚{'═'*w}╝")
    print(f"\n  🧬 {DNA}")
    print(f"  📊 {state.timestamp}\n")


def cmd_serve(args):
    """HTTP 服务模式 — 提供 /health /metrics /dashboard /config /control 端点"""
    port = args.port or 9677
    quiet = getattr(args, "quiet", False)

    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("❌ 需要 Python 标准库 http.server")
        sys.exit(1)

    runtime = get_runtime(verbose=not quiet)
    runtime.start()
    time.sleep(1)

    def _read_body(handler) -> bytes:
        length = int(handler.headers.get("Content-Length", 0))
        return handler.rfile.read(length) if length > 0 else b""

    class AntColonyHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            if not quiet:
                super().log_message(format, *args)

        def _json_response(self, data, status=200):
            body = json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _html_response(self, html):
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_GET(self):
            if self.path == "/health":
                self._json_response(runtime.get_health())
            elif self.path == "/metrics":
                self._json_response(runtime.get_metrics())
            elif self.path == "/config":
                self._json_response({
                    "config": runtime.get_config(),
                    "description": CONFIG_HELP,
                })
            elif self.path == "/dashboard" or self.path == "/":
                state = runtime.snapshot()
                config = runtime.get_config()
                self._html_response(_dashboard_html(state, config))
            elif self.path == "/tick":
                state = runtime.tick()
                self._json_response({"ok": True, "tick": state.tick_count, "E": state.emergence_E})
            else:
                self._json_response({"error": "not found"}, 404)

        def do_POST(self):
            body = _read_body(self)
            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
            except json.JSONDecodeError:
                self._json_response({"error": "invalid json"}, 400)
                return

            if self.path == "/config":
                result = runtime.set_config(payload)
                self._json_response(result)
            elif self.path == "/control":
                action = payload.get("action", "")
                if action == "tick":
                    n = int(payload.get("n", 1))
                    for _ in range(n):
                        runtime.tick()
                    state = runtime.snapshot()
                    self._json_response({"ok": True, "action": "tick", "n": n, "tick": state.tick_count, "E": state.emergence_E})
                elif action == "task":
                    result = runtime.send_task(payload.get("task", "调试任务"))
                    self._json_response({"ok": True, "action": "task", "result": result})
                elif action == "alert":
                    result = runtime.simulate_alert(payload.get("issue", "调试告警"), severity=int(payload.get("severity", 3)))
                    self._json_response({"ok": True, "action": "alert", "result": result})
                elif action == "aggregate":
                    result = runtime.broadcast_aggregate(payload.get("topic", "调试聚集"))
                    self._json_response({"ok": True, "action": "aggregate", "result": result})
                elif action == "verbose":
                    runtime.set_config({"verbose": bool(payload.get("verbose", True))})
                    self._json_response({"ok": True, "action": "verbose", "verbose": runtime.get_config()["verbose"]})
                else:
                    self._json_response({"error": f"unknown action: {action}"}, 400)
            else:
                self._json_response({"error": "not found"}, 404)

    server = HTTPServer(("0.0.0.0", port), AntColonyHandler)
    url = f"http://127.0.0.1:{port}/dashboard"
    mode_str = '安静' if quiet else '调试（console 有输出）'
    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🐜 龍魂蚁群 HTTP 调试控制台 v2.1                   ║
╠══════════════════════════════════════════════════════════╣
║     {url:<52} ║
╠══════════════════════════════════════════════════════════╣
║  端点:                                                  ║
║    GET  /dashboard     可视化仪表盘（可调参数）          ║
║    GET  /config        当前可调参数                     ║
║    POST /config        热更新参数 (JSON body)            ║
║    POST /control       action=tick/task/alert/aggregate/verbose   ║
║    GET  /metrics       完整 JSON 指标                   ║
║    GET  /health        健康检查                         ║
╠══════════════════════════════════════════════════════════╣
║  模式: {mode_str:<36} ║
║  {DNA}
╚══════════════════════════════════════════════════════════╝
""")
    print(f"  📡 按 Ctrl+C 停止\n")

    # 尝试打开浏览器（macOS/Linux 桌面环境）
    if not quiet:
        try:
            import platform, subprocess
            if platform.system() == 'Darwin':
                _ = subprocess.run(['open', url], capture_output=True, timeout=5)
            else:
                _ = subprocess.run(['xdg-open', url], capture_output=True, timeout=5)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  🛑 停止 HTTP 服务...")
        server.shutdown()
        runtime.stop()


CONFIG_HELP = {
    "tick_interval": "滴答间隔（秒），控制主循环速度",
    "decay_tick": "每 N 个 tick 衰减一次信息素",
    "snapshot_tick": "每 N 个 tick 保存快照",
    "emergence_tick": "每 N 个 tick 计算一次涌现质量 E",
    "persist_tick": "每 N 个 tick 写入 SQLite 持久化",
    "verbose": "是否打印 console 调试日志",
}


def _dashboard_html(state, config) -> str:
    """带参数调试面板的仪表盘 HTML"""
    pops_html = "".join(
        f'<div class="metric"><span class="label">{p}</span><span class="value">{c}</span></div>'
        for p, c in sorted(state.population_distribution.items())
    ) if state.population_distribution else '<div class="metric"><span class="label">暂无</span></div>'

    pheros_html = "".join(
        f'<div class="metric"><span class="label">{k}</span><span class="value">{v:.1f}</span></div>'
        f'<div class="bar"><div class="bar-fill" style="width:{min(v, 100):.0f}%;background:linear-gradient(90deg,#a00,#f80)"></div></div>'
        for k, v in state.pheromone_concentration.items()
    ) if state.pheromone_concentration else '<div class="metric"><span class="label">暂无</span></div>'

    cfg_inputs = "".join(
        f'''<div class="cfg-row">
            <label>{k}</label>
            <input type="text" id="cfg_{k}" value="{v}">
            <span class="hint">{CONFIG_HELP.get(k, "")}</span>
        </div>'''
        for k, v in config.items()
    )

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🐜 龍魂蚁群调试控制台</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a1a;color:#e0e0e0;font-family:-apple-system,system-ui,sans-serif;padding:20px;min-height:100vh}}
h1{{color:#ffd700;margin-bottom:8px;font-size:1.5em}}
.sub{{color:#999;font-size:.85em;margin-bottom:20px}}
.card{{background:#111133;border-radius:12px;padding:16px;margin-bottom:16px;border:1px solid #222}}
.card h2{{color:#aaa;font-size:.9em;margin-bottom:12px}}
.row{{display:flex;gap:16px;flex-wrap:wrap}}
.col{{flex:1;min-width:280px}}
.metric{{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1a1a3a}}
.metric .label{{color:#888}}
.metric .value{{color:#ffd700;font-weight:bold;font-family:monospace}}
.bar{{height:8px;background:#1a1a3a;border-radius:4px;margin:4px 0;overflow:hidden}}
.bar-fill{{height:100%;border-radius:4px;transition:width .3s}}
.pop-control{{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}}
.btn{{background:#222;color:#ffd700;border:1px solid #444;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.85em}}
.btn:hover{{background:#333}}
.btn-primary{{background:#1a3a1a;border-color:#3a6a3a;color:#0f0}}
.btn-danger{{background:#3a1a1a;border-color:#6a3a3a;color:#f66}}
.btn-warning{{background:#3a3a1a;border-color:#6a6a3a;color:#ff0}}
@keyframes pulse{{50%{{opacity:.6}}}}
.live{{animation:pulse 2s infinite;color:#0f0}}
.cfg-row{{display:flex;align-items:center;gap:10px;margin:8px 0;flex-wrap:wrap}}
.cfg-row label{{width:110px;color:#aaa;font-family:monospace}}
.cfg-row input{{background:#0a0a1a;border:1px solid #333;color:#ffd700;padding:5px 8px;border-radius:4px;width:120px}}
.cfg-row .hint{{color:#666;font-size:.8em;flex:1}}
textarea{{background:#0a0a1a;border:1px solid #333;color:#e0e0e0;padding:8px;border-radius:6px;width:100%;min-height:60px;resize:vertical}}
#toast{{position:fixed;bottom:20px;right:20px;background:#1a3a1a;color:#0f0;padding:10px 16px;border-radius:8px;display:none;z-index:100}}
</style>
</head>
<body>
<h1>🐜 龍魂蚁群调试控制台 v2.1</h1>
<div class="sub">Tick #{state.tick_count} · E={state.emergence_E:.4f} ({state.emergence_grade}) · 模块 {state.active_modules} · <span class="live">● LIVE</span></div>

<div class="row">
<div class="col">
<div class="card">
<h2>🧬 涌现质量</h2>
<div class="metric"><span class="label">E 值</span><span class="value">{state.emergence_E:.4f}</span></div>
<div class="metric"><span class="label">等级</span><span class="value">{state.emergence_grade}</span></div>
<div class="bar"><div class="bar-fill" style="width:{min(state.emergence_E*66,100):.0f}%;background:linear-gradient(90deg,#00a,#0af)"></div></div>
</div>
<div class="card">
<h2>📡 信号统计</h2>
<div class="metric"><span class="label">发送</span><span class="value">{state.total_signals_sent}</span></div>
<div class="metric"><span class="label">阻断</span><span class="value">{state.total_signals_blocked}</span></div>
<div class="metric"><span class="label">信息素轨迹</span><span class="value">{state.pheromone_trails}</span></div>
</div>
<div class="card">
<h2>⚡ 快速操作</h2>
<div class="pop-control">
<button class="btn btn-primary" onclick="control('tick', {{n:1}})">Tick +1</button>
<button class="btn btn-primary" onclick="control('tick', {{n:10}})">+10</button>
<button class="btn" onclick="location.href='/metrics'">📊 JSON</button>
<button class="btn" onclick="location.href='/health'">💚 Health</button>
</div>
</div>
</div>

<div class="col">
<div class="card">
<h2>🏘️ 种群分布</h2>
{pops_html}
</div>
<div class="card">
<h2>🧪 信息素浓度</h2>
{pheros_html}
</div>
</div>
</div>

<div class="card">
<h2>🔧 参数调配（热更新，不重启）</h2>
<form id="cfgForm" onsubmit="return saveConfig()">
{cfg_inputs}
<div class="pop-control" style="margin-top:12px">
<button class="btn btn-primary" type="submit">💾 保存参数</button>
<button class="btn" type="button" onclick="loadConfig()">🔄 重置</button>
</div>
</form>
</div>

<div class="card">
<h2>🎮 注入测试信号</h2>
<div class="cfg-row" style="align-items:flex-start">
<label>任务内容</label>
<textarea id="taskText" placeholder="输入任务内容，点击发送"></textarea>
<button class="btn btn-primary" onclick="control('task', {{task: document.getElementById('taskText').value}})">📤 发任务</button>
</div>
<div class="cfg-row" style="align-items:flex-start;margin-top:10px">
<label>告警内容</label>
<textarea id="alertText" placeholder="输入告警内容"></textarea>
<button class="btn btn-danger" onclick="control('alert', {{issue: document.getElementById('alertText').value, severity:3}})">🚨 发告警</button>
</div>
<div class="cfg-row" style="align-items:flex-start;margin-top:10px">
<label>聚集主题</label>
<textarea id="aggText" placeholder="输入聚集主题"></textarea>
<button class="btn btn-warning" onclick="control('aggregate', {{topic: document.getElementById('aggText').value}})">🐝 发起聚集</button>
</div>
</div>

<div class="card">
<h2>📖 字段说明</h2>
<div style="color:#888;font-size:.85em;line-height:1.6">
tick: 主循环次数（每 tick_interval 秒 +1）<br>
E: 涌现质量 = f(种群多样性, 连接密度, 一致性, 变异容忍)<br>
模块: 注册在总线上的模块数量（16人格映射到五大蚁群种群）<br>
信息素: RECRUIT(绿·调度) / ALERT(红·安全) / TRAIL(黄·路径) / AGGREGATE(蓝·协作)<br>
阻断: 被不动点/颜色路由/伦理规则拦截的信号数
</div>
</div>

<div class="sub" style="margin-top:12px">🧬 {DNA} · {state.timestamp}</div>
<div id="toast"></div>

<script>
function showToast(msg) {{
    const t = document.getElementById('toast'); t.innerText = msg; t.style.display='block';
    setTimeout(()=>t.style.display='none', 2000);
}}
async function control(action, payload) {{
    payload.action = action;
    const r = await fetch('/control', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(payload)}});
    const d = await r.json();
    showToast(action + ' ✅ ' + JSON.stringify(d.tick ?? d.result?.signal_id ?? ''));
    setTimeout(()=>location.reload(), 500);
}}
function cfgPayload() {{
    const keys = {json.dumps(list(config.keys()))};
    const obj = {{}};
    keys.forEach(k=>{{ obj[k] = document.getElementById('cfg_'+k).value; }});
    return obj;
}}
async function saveConfig() {{
    const r = await fetch('/config', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(cfgPayload())}});
    const d = await r.json();
    showToast('参数已保存 ✅');
    setTimeout(()=>location.reload(), 600);
    return false;
}}
function loadConfig() {{ location.reload(); }}
setTimeout(()=>location.reload(), 8000);
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description="🐜 龍魂蚁群守护进程 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-ant-colony start              启动后台守护进程
  lh-ant-colony status             查看运行状态
  lh-ant-colony dashboard          仪表盘
  lh-ant-colony serve --port 9677  HTTP 服务模式
  lh-ant-colony metrics            完整 JSON 指标
  lh-ant-colony health             健康检查""",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("start", help="启动后台守护进程")
    sub.add_parser("stop", help="停止守护进程")
    sub.add_parser("status", help="查看运行状态")
    sub.add_parser("metrics", help="完整 JSON 指标")
    sub.add_parser("health", help="健康检查 (JSON)")
    sub.add_parser("dashboard", help="仪表盘")

    serve_p = sub.add_parser("serve", help="HTTP 服务模式")
    serve_p.add_argument("--port", type=int, default=9677, help="端口 (默认 9677)")
    serve_p.add_argument("--quiet", action="store_true", help="安静模式：不输出调试日志也不自动打开浏览器")

    args = parser.parse_args()

    cmds = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "metrics": cmd_metrics,
        "health": cmd_health,
        "dashboard": cmd_dashboard,
        "serve": cmd_serve,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        # 默认显示仪表盘
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
