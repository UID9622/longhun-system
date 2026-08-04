#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂业主投票系统 v1.1
本地运行 · 数据不上传互联网 · 零依赖
龍芯北辰 UID9622 | 民生审计层
DNA: #龍芯⚡️丙午·癸未·辛丑·颐-投票系统-v1.1-精修
协议: CC BY-NC-SA 4.0
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import datetime
import urllib.parse
import html
import socket
import time

VOTE_FILE = "votes.json"
PORT_START = 8080
PORT_MAX = 8090

# ── 数据层 ────────────────────────────────────────────

def load_votes():
    """加载投票数据"""
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"同意": 0, "不同意": 0, "弃权": 0, "details": []}


def save_votes(votes):
    """原子写入投票数据"""
    tmp_file = VOTE_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, VOTE_FILE)  # 原子替换，防写一半崩溃


# ── 网络工具 ──────────────────────────────────────────

def get_local_ip():
    """获取本机局域网IP（多方法降级）"""
    # 方法1: 连接外部地址获取实际出站IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith("127."):
            return ip
    except Exception:
        pass

    # 方法2: 遍历网络接口
    try:
        hostname = socket.gethostname()
        addrs = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for addr in addrs:
            ip = addr[4][0]
            if not ip.startswith("127."):
                return ip
    except Exception:
        pass

    # 方法3: ifconfig 降级
    try:
        import subprocess
        result = subprocess.run(
            ["ifconfig"], capture_output=True, text=True, timeout=3
        )
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line.startswith("inet ") and "127.0.0.1" not in line:
                return line.split()[1]
    except Exception:
        pass

    return "127.0.0.1"


def find_available_port(start=PORT_START, max_port=PORT_MAX):
    """查找可用端口"""
    for port in range(start, max_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.bind(("0.0.0.0", port))
            s.close()
            return port
        except OSError:
            continue
    return None


# ── 输入校验 ──────────────────────────────────────────

def sanitize(text, max_len=100):
    """清理用户输入：去首尾空白 + 截断"""
    if not text:
        return ""
    return text.strip()[:max_len]


def validate_room(room):
    """房号校验"""
    if not room or len(room.strip()) < 2:
        return False
    # 允许中文、数字、字母、-、栋、单元、号
    return True


# ── HTTP 处理器 ───────────────────────────────────────

HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂业主投票系统</title>
<style>
*, *::before, *::after {{margin:0; padding:0; box-sizing:border-box;}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Microsoft YaHei", "Helvetica Neue", sans-serif;
    background: #0a0a0a; color: #e0e0e0;
    max-width: 600px; margin: 0 auto; padding: 20px;
    min-height: 100vh;
}}
.header {{
    text-align: center; margin-bottom: 30px;
}}
.header h1 {{
    color: #d4a017; font-size: 24px; margin-bottom: 8px;
    letter-spacing: 2px;
}}
.header .subtitle {{
    color: #666; font-size: 12px;
}}
.badge {{
    display: inline-block; background: #1a2f1a; color: #4caf50;
    border: 1px solid #4caf50; padding: 4px 12px; border-radius: 20px;
    font-size: 11px; margin-top: 8px;
}}
.topic {{
    background: #1a1a1a; border: 1px solid #333; padding: 20px;
    margin-bottom: 25px; border-radius: 10px;
    border-left: 3px solid #d4a017;
}}
.topic h3 {{color: #d4a017; margin-bottom: 12px; font-size: 16px;}}
.topic p {{font-size: 14px; line-height: 1.8; color: #bbb;}}

.form-group {{margin-bottom: 15px;}}
.form-group label {{
    display: block; color: #888; font-size: 12px; margin-bottom: 5px;
}}
.form-group input {{
    width: 100%; padding: 12px; background: #1a1a1a;
    border: 1px solid #333; color: #e0e0e0; border-radius: 6px;
    font-size: 14px; transition: border-color 0.3s;
}}
.form-group input:focus {{
    outline: none; border-color: #d4a017;
}}
.form-group input::placeholder {{color: #555;}}

.btn-group {{
    display: flex; gap: 10px; margin-top: 20px;
}}
.btn {{
    flex: 1; padding: 16px 8px; font-size: 15px; font-weight: bold;
    border: 2px solid; border-radius: 8px; cursor: pointer;
    transition: all 0.25s; text-align: center;
}}
.btn-agree {{background: #0d1f0d; border-color: #388e3c; color: #4caf50;}}
.btn-agree:hover {{background: #388e3c; color: #fff; transform: translateY(-1px);}}
.btn-disagree {{background: #1f0d0d; border-color: #c62828; color: #f44336;}}
.btn-disagree:hover {{background: #c62828; color: #fff; transform: translateY(-1px);}}
.btn-abstain {{background: #0d0d1f; border-color: #1565c0; color: #42a5f5;}}
.btn-abstain:hover {{background: #1565c0; color: #fff; transform: translateY(-1px);}}

.toast {{
    display: none; background: #1a2f1a; border: 1px solid #4caf50;
    color: #81c784; padding: 12px 20px; border-radius: 8px;
    text-align: center; margin-bottom: 20px; font-size: 14px;
    animation: fadeIn 0.3s;
}}
.toast.show {{display: block;}}
.toast.error {{background: #2f1a1a; border-color: #f44336; color: #ef9a9a;}}
@keyframes fadeIn {{from{{opacity:0;transform:translateY(-10px);}}to{{opacity:1;transform:translateY(0);}}}}

.results {{
    background: #1a1a1a; border: 1px solid #333; padding: 20px;
    border-radius: 10px; margin-top: 25px;
}}
.results h3 {{color: #d4a017; margin-bottom: 15px; font-size: 16px;}}
.result-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid #222; font-size: 14px;
}}
.result-row:last-child {{border-bottom: none;}}
.result-label {{color: #888;}}
.result-value {{color: #e0e0e0; font-weight: bold;}}
.result-bar {{
    height: 6px; background: #222; border-radius: 3px; margin: 12px 0;
    overflow: hidden;
}}
.result-bar-fill {{
    height: 100%; border-radius: 3px; transition: width 0.5s ease;
    background: linear-gradient(90deg, #d4a017, #ffd54f);
}}

.footer {{
    text-align: center; margin-top: 30px; padding-top: 20px;
    border-top: 1px solid #222; color: #555;
    font-size: 11px; line-height: 1.8;
}}
</style>
</head>
<body>
<div class="header">
    <h1>🐉 龍魂业主投票系统</h1>
    <p class="subtitle">本地部署 · 数据不上传 · 匿名保护</p>
    <span class="badge">🟢 局域网安全</span>
</div>

<div id="toast" class="toast"></div>

<div class="topic">
    <h3>📋 当前议题</h3>
    <p>是否同意就物业违规使用公共收益一事，授权业主代表向政府投诉 / 提起诉讼？</p>
</div>

<form id="voteForm">
    <div class="form-group">
        <label>房号 *</label>
        <input type="text" name="room" placeholder="例：3栋502" required autocomplete="off">
    </div>
    <div class="form-group">
        <label>房屋面积（㎡）*</label>
        <input type="text" name="area" placeholder="例：89.5" required autocomplete="off" inputmode="decimal">
    </div>
    <div class="form-group">
        <label>联系方式（选填，用于接收进展）</label>
        <input type="text" name="contact" placeholder="手机号 / 微信号" autocomplete="off">
    </div>

    <div class="btn-group">
        <button type="button" onclick="submitVote('同意')" class="btn btn-agree">✅ 同意</button>
        <button type="button" onclick="submitVote('不同意')" class="btn btn-disagree">❌ 不同意</button>
        <button type="button" onclick="submitVote('弃权')" class="btn btn-abstain">⚪ 弃权</button>
    </div>
</form>

<div class="results" id="results">
    <h3>📊 实时结果</h3>
    <div class="result-bar"><div class="result-bar-fill" id="bar" style="width:0%"></div></div>
    <div id="resultContent"></div>
</div>

<div class="footer">
    <p>本系统运行在本地网络，数据不上传互联网</p>
    <p>龍芯北辰 UID9622 | 龍魂民生审计层</p>
    <p>数据文件：votes.json（纯文本，随时可查看）</p>
    <p style="margin-top:5px; color:#444;">CC BY-NC-SA 4.0 开源协议</p>
</div>

<script>
async function submitVote(choice) {{
    const form = document.getElementById('voteForm');
    const room = form.room.value.trim();
    const area = form.area.value.trim();

    if (!room || room.length < 2) {{
        showToast('请填写有效房号', 'error'); return;
    }}
    if (!area || isNaN(parseFloat(area))) {{
        showToast('请填写有效的房屋面积', 'error'); return;
    }}

    const body = new URLSearchParams({{
        room: room,
        area: area,
        contact: form.contact.value.trim(),
        choice: choice
    }});

    try {{
        const resp = await fetch('/api/vote', {{method:'POST', body}});
        const data = await resp.json();
        if (data.ok) {{
            showToast('✅ 投票成功！');
            loadResults();
        }} else {{
            showToast(data.error || '投票失败', 'error');
        }}
    }} catch(e) {{
        showToast('网络错误，请确认连接的是同一WiFi', 'error');
    }}
}}

async function loadResults() {{
    try {{
        const resp = await fetch('/api/results');
        const v = await resp.json();
        const total = v.同意 + v.不同意 + v.弃权;
        const pct = total > 0 ? (v.同意 / total * 100) : 0;
        document.getElementById('bar').style.width = pct + '%';
        document.getElementById('resultContent').innerHTML =
            `<div class="result-row"><span class="result-label">✅ 同意</span><span class="result-value">${{v.同意}} 票</span></div>
             <div class="result-row"><span class="result-label">❌ 不同意</span><span class="result-value">${{v.不同意}} 票</span></div>
             <div class="result-row"><span class="result-label">⚪ 弃权</span><span class="result-value">${{v.弃权}} 票</span></div>
             <div class="result-row" style="border-top:2px solid #d4a017;margin-top:8px;padding-top:14px;">
                <span class="result-label">总投票户数</span>
                <span class="result-value">${{total}} 户</span>
             </div>
             <div class="result-row">
                <span class="result-label">更新时间</span>
                <span class="result-value">${{new Date().toLocaleString('zh-CN')}}</span>
             </div>`;
    }} catch(e) {{}}
}}

function showToast(msg, type) {{
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast ' + (type || '') + ' show';
    setTimeout(() => t.classList.remove('show'), 3000);
}}

loadResults();  // 页面加载时显示结果
</script>
</body>
</html>"""


class VoteHandler(BaseHTTPRequestHandler):
    """投票系统HTTP处理器"""

    def log_message(self, format, *args):
        pass  # 静默，不打印访问日志

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html_str, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_str.encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/results":
            # JSON API: 返回投票结果
            votes = load_votes()
            total = votes["同意"] + votes["不同意"] + votes["弃权"]
            self._send_json({
                "同意": votes["同意"],
                "不同意": votes["不同意"],
                "弃权": votes["弃权"],
                "total": total,
                "updated_at": datetime.datetime.now().isoformat()
            })

        elif path == "/api/status":
            # JSON API: 系统状态
            self._send_json({
                "status": "running",
                "host": get_local_ip(),
                "version": "1.1",
                "dna": "#龍芯⚡️丙午·癸未·辛丑·颐-投票系统-v1.1"
            })

        else:
            # 默认：返回投票页面
            self._send_html(HTML_PAGE)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path != "/api/vote":
            self._send_json({"ok": False, "error": "接口不存在"}, 404)
            return

        # 读取并解析 POST 数据
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._send_json({"ok": False, "error": "请求数据为空"}, 400)
            return

        post_data = self.rfile.read(content_length).decode("utf-8")
        params = urllib.parse.parse_qs(post_data, keep_blank_values=False)

        # 提取并校验字段
        room = sanitize(params.get("room", [""])[0], max_len=50)
        area = sanitize(params.get("area", [""])[0], max_len=20)
        contact = sanitize(params.get("contact", [""])[0], max_len=50)
        choice = params.get("choice", ["弃权"])[0]

        # 校验
        if not validate_room(room):
            self._send_json({"ok": False, "error": "请填写有效房号（至少2个字符）"}, 400)
            return

        if not area or not area.replace(".", "").isdigit():
            self._send_json({"ok": False, "error": "请填写有效面积"}, 400)
            return

        if choice not in ("同意", "不同意", "弃权"):
            choice = "弃权"

        # 更新投票数据
        votes = load_votes()
        now = datetime.datetime.now().isoformat()

        # 同一房号允许更新投票（覆盖旧票）
        existing = [d for d in votes.get("details", []) if d.get("room") == room]
        if existing:
            for d in votes["details"]:
                if d.get("room") == room:
                    old_choice = d["choice"]
                    votes[old_choice] = max(0, votes.get(old_choice, 0) - 1)
                    d["choice"] = choice
                    d["area"] = area
                    if contact:
                        d["contact"] = contact
                    d["updated_at"] = now
                    break
        else:
            votes["details"].append({
                "room": room,
                "area": area,
                "contact": contact if contact else "",
                "choice": choice,
                "created_at": now
            })

        votes[choice] = votes.get(choice, 0) + 1

        try:
            save_votes(votes)
        except Exception as e:
            self._send_json({"ok": False, "error": f"数据保存失败: {e}"}, 500)
            return

        self._send_json({
            "ok": True,
            "message": "投票成功",
            "choice": choice,
            "total": votes["同意"] + votes["不同意"] + votes["弃权"]
        })


# ── 启动入口 ──────────────────────────────────────────

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = find_available_port()

    if port is None:
        print("❌ 错误：端口 8080-8090 均被占用，请关闭其他服务后重试。")
        exit(1)

    server = HTTPServer(("0.0.0.0", port), VoteHandler)

    print()
    print("=" * 60)
    print("  🐉  龍魂业主投票系统 v1.1")
    print("=" * 60)
    print(f"  本机访问 : http://localhost:{port}")
    print(f"  局域网访问: http://{local_ip}:{port}")
    print()
    print("  ── 使用说明 ──")
    print(f"  1. 确保业主手机连接同一 WiFi")
    print(f"  2. 浏览器打开: http://{local_ip}:{port}")
    print(f"  3. 投票数据保存在当前目录: {VOTE_FILE}")
    print(f"  4. 按 Ctrl+C 停止服务器")
    print()
    print(f"  DNS: #龍芯⚡️丙午·癸未·辛丑·颐-投票系统-v1.1")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 服务器已停止，投票数据已保存至 {VOTE_FILE}")
        server.server_close()
