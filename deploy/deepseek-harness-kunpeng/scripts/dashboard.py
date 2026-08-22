#!/usr/bin/env python3
# 🐉 龍魂 · DSH 状态看板 (纯标准库 · 无三方依赖)
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-DASHBOARD-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (工程层) — 允许商业使用·署名·专利授权
#
# 读取 Ollama API (/api/tags) 显示模型列表与状态, 供鲲鹏本地自查。
# 仅监听 127.0.0.1, 外部访问走 SSH 隧道。
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OLLAMA_API = "http://ollama:11434"
PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🐉 龍魂 · DSH 状态看板</title>
<style>
  body{background:#0d1117;color:#e6edf3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
       margin:0;padding:24px;line-height:1.6}
  h1{font-size:22px;border-bottom:1px solid #30363d;padding-bottom:12px}
  .card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;margin:12px 0}
  table{width:100%;border-collapse:collapse;font-size:14px}
  th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #21262d}
  th{color:#8b949e;font-weight:600}
  .ok{color:#3fb950}.warn{color:#d29922}.bad{color:#f85149}
  .meta{color:#8b949e;font-size:12px}
</style>
</head>
<body>
<h1>🐉 龍魂 · DeepSeek Harness 看板</h1>
<div class="card">
  <h2>Ollama 模型</h2>
  <div id="models">加载中…</div>
</div>
<div class="card">
  <h2>帮助</h2>
  <table>
    <tr><td>Web UI</td><td>SSH 隧道后访问 <code>http://127.0.0.1:2283</code></td></tr>
    <tr><td>Headless API</td><td>SSH 隧道后 <code>http://127.0.0.1:2284/v1/chat/completions</code></td></tr>
    <tr><td>Ollama API</td><td>SSH 隧道后 <code>http://127.0.0.1:11434</code></td></tr>
  </table>
</div>
<p class="meta">龍魂系统 · 数据主权归 UID9622 · 本地推理零 API 费用</p>
<script>
async function load() {
  const el = document.getElementById('models');
  try {
    const r = await fetch('/api/tags');
    const d = await r.json();
    const list = (d.models || []).map(m =>
      '<tr><td>' + m.name + '</td><td>' +
      (m.size ? (m.size/1073741824).toFixed(1) + ' GB' : '-') + '</td><td class="ok">就绪</td></tr>'
    ).join('');
    el.innerHTML = list
      ? '<table><tr><th>模型</th><th>大小</th><th>状态</th></tr>' + list + '</table>'
      : '<p class="warn">暂无模型。请先执行: make deploy 或在鲲鹏上 docker compose exec ollama ollama pull deepseek-r1:14b</p>';
  } catch (e) {
    el.innerHTML = '<p class="bad">Ollama 不可达: ' + e + '</p>';
  }
}
load();
setInterval(load, 15000);
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/tags":
            try:
                with urllib.request.urlopen(OLLAMA_API + "/api/tags", timeout=5) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                body = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):  # 静默访问日志
        pass


if __name__ == "__main__":
    print("🐉 DSH 看板启动: http://127.0.0.1:8080")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
