#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
"""
🐲 龍魂·维权证据固化 Web 服务 v1.0
DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-WITNESS-SERVER-v1.0-UID9622

一个极简的本地 Web 服务器，让老百姓通过浏览器就能固化维权证据。
数据只走本地：浏览器 → 本服务 → lh --witness [--sign] → data/witness/

用法:
    python3 bin/lh_witness_server.py              # 默认端口 8780
    python3 bin/lh_witness_server.py --port 8080  # 指定端口
"""

import json
import re
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-WITNESS-SERVER-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def run_lh_witness(content: str, sign: bool = False) -> dict:
    """调用 08_BIN/lh.py --witness 固化证据，返回解析后的结果。"""
    cmd = ["python3", str(ROOT / "08_BIN" / "lh.py"), "--witness"]
    if sign:
        cmd.append("--sign")

    # 通过 stdin 传入内容，以空行 + done 结束
    input_text = content + "\n\ndone\n"
    proc = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        cwd=str(ROOT),
        timeout=120,
    )

    output = proc.stdout + "\n" + proc.stderr
    if proc.returncode != 0 and "✅ 证据已固化" not in output:
        raise RuntimeError(f"lh --witness 执行失败:\n{output[-800:]}")

    # 解析输出
    result = {"sign": sign}

    m_id = re.search(r"🆔 证据ID:\s*(WITNESS-[\w-]+)", output)
    if m_id:
        result["witness_id"] = m_id.group(1)

    m_enc = re.search(r"✅ 证据已固化并加密:\s*(\S+)", output)
    if m_enc:
        result["enc_file"] = m_enc.group(1)

    m_asc = re.search(r"✍️\s*GPG 签章:\s*(\S+)", output)
    if m_asc:
        result["asc_file"] = m_asc.group(1)

    m_hash = re.search(r"🔐 SHA-256:\s*([a-f0-9]+)", output)
    if m_hash:
        result["sha256"] = m_hash.group(1)

    m_audit = re.search(r"🧩 Agent 审计链:\s*(.+)", output)
    if m_audit:
        result["audit"] = m_audit.group(1).strip()
    elif sign:
        result["audit"] = "已执行"

    if "witness_id" not in result:
        raise RuntimeError(f"无法解析 witness 输出:\n{output[-800:]}")

    return result


class WitnessHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # 简洁日志
        print(f"[{self.log_date_time_string()}] {args[0]}")

    def _send_json(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str):
        if not path.exists():
            self.send_error(404, "File not found")
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/witness"):
            self._send_file(ROOT / "web" / "witness.html", "text/html; charset=utf-8")
        elif parsed.path == "/health":
            self._send_json(200, {"status": "ok", "dna": DNA})
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/witness":
            self.send_error(404, "Not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            self._send_json(400, {"error": "请求体为空"})
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "JSON 解析失败"})
            return

        content = payload.get("content", "").strip()
        sign = bool(payload.get("sign", False))

        if not content:
            self._send_json(400, {"error": "证据内容不能为空"})
            return

        try:
            result = run_lh_witness(content, sign=sign)
            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐲 龍魂·维权证据固化 Web 服务")
    parser.add_argument("--port", type=int, default=8780, help="监听端口 (默认 8780)")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址 (默认 127.0.0.1)")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), WitnessHandler)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🐲 龍魂·维权证据固化 Web 服务 v1.0                       ║
║  DNA: {DNA}   ║
╚══════════════════════════════════════════════════════════╝
📍 访问地址: http://{args.host}:{args.port}/
🔒 仅监听本地，不上传任何数据
🛑 按 Ctrl+C 停止
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹ 服务已停止")
        sys.exit(0)


if __name__ == "__main__":
    main()
