#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂跨平台同步工作流 — 端到端可执行脚本 v2.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
================================================
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-XSYNC-WORKFLOW-v2.0-UID9622
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

能力:
  discover     mDNS 发现局域网龍魂同步节点
  advertise    发布本机龍魂同步服务（含HTTP健康检查）
  pair-qr      生成 ECDH 公钥二维码
  pair-scan    扫描/读取对端公钥并完成密钥协商
  serve        启动同步服务端（在线ECDH + 记忆/文件同步）
  sync-memory  从服务端拉取记忆摘要
  sync-file    从服务端拉取任意文件
  demo         单机双线程 loopback 端到端加密同步演示

设计原则:
- 数据根留中国，不经过外网
- 先加密再出应用：SM4-CBC + HMAC-SHA256
- 密钥不离设备：ECDH Curve25519 + HKDF-SHA256
- 本地网络直连：mDNS / TCP LAN / WiFi Direct / BLE
- 端口冲突自动检测：默认避开 9622/8799

用法示例:
  # Mac 端启动同步服务
  python xsync_workflow.py serve --port 19622

  # 鸿蒙端拉取记忆
  python xsync_workflow.py sync-memory --host 192.168.31.100 --port 19622

  # 鸿蒙端拉取文件
  python xsync_workflow.py sync-file --host 192.168.31.100 --port 19622 \
      --remote ~/.longhun/memory/latest_digest.json --local /tmp/memory.json
"""

import argparse
import base64
import io
import json
import logging
import os
import socket
import struct
import sys
import tempfile
import threading
import time
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# 将脚本所在目录加入路径，确保能找到中文模块名
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import 加密信封
import 传输管理器
import 密钥协商器
import 版本向量时钟
import 冲突解决器
import 主权网关
import 设备发现器

DNA = "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-XSYNC-WORKFLOW-v2.0-UID9622"
DNA_PREFIX = "#龍芯⚡️"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DEFAULT_PORT = 19622  # 避开 9622(网关)/8799(hub)
OCCUPIED_PORTS = {9622, 8765, 8799, 11434, 11435}
MEMORY_PATH = Path.home() / ".longhun" / "memory" / "latest_digest.json"
SESSION_TTL_SECONDS = 24 * 3600  # 会话密钥有效期 24 小时


def _指纹(数据: bytes) -> str:
    import hashlib
    return hashlib.sha256(数据).hexdigest()[:16]


def _配置日志(详细: bool = False):
    level = logging.DEBUG if 详细 else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def _静默实例化(类, *args, **kwargs):
    """临时屏蔽 print，避免君子协议刷屏。"""
    buf = io.StringIO()
    with redirect_stdout(buf):
        return 类(*args, **kwargs)


def _生成二维码图片(文本: str, 输出路径: Path) -> Path:
    try:
        import qrcode
    except ImportError as e:
        raise RuntimeError("请先安装 qrcode: pip install qrcode[pil]") from e
    qr = qrcode.QRCode(version=3, box_size=4, border=2)
    qr.add_data(文本)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    输出路径.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(输出路径))
    return 输出路径


def _获取可用端口(首选端口: int) -> int:
    """检查端口是否可用，避开已知占用端口，必要时自增。"""
    port = 首选端口
    for _ in range(100):
        if port in OCCUPIED_PORTS:
            port += 1
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                logging.warning("🟡 端口 %d 被占用，尝试 %d", port, port + 1)
                port += 1
    raise RuntimeError("找不到可用端口")


def _是本地地址(ip: str) -> bool:
    """RFC1918 / RFC4193 / loopback / link-local 检查。"""
    try:
        import ipaddress
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
        )
    except Exception:
        return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# =================== 子命令实现 ===================

def cmd_discover(args):
    设备列表 = 设备发现器.发现设备(超时秒=args.timeout)
    设备发现器.打印发现结果(设备列表)
    return 设备列表


def cmd_advertise(args):
    port = _获取可用端口(args.port)
    属性 = {"platform": args.platform, "role": args.role, "version": "v5.4"}
    if args.pubkey:
        属性["pubkey"] = Path(args.pubkey).read_text().strip()
    if port != args.port:
        logging.warning("🟡 端口从 %d 自动切换到 %d（原端口占用/冲突）", args.port, port)
    print(f"\n{'='*60}")
    print("  龍魂同步服务广播")
    print(f"  端口: {port}")
    print(f"  服务名: {args.name or 'longhun-mac-9622'}")
    print(f"  DNA: {DNA}")
    print(f"{'='*60}\n")
    设备发现器.发布服务(
        端口=port,
        服务名=args.name or "longhun-mac-9622",
        属性=属性,
        超时秒=args.timeout,
    )


def cmd_pair_qr(args):
    协商 = _静默实例化(密钥协商器.密钥协商器)
    公钥 = 协商.生成密钥对()
    二维码数据 = 协商.公钥转二维码数据(公钥)

    print(f"\n{'='*60}")
    print("  龍魂 ECDH 公钥二维码")
    print(f"  DNA: {DNA}")
    print(f"  公钥指纹: {_指纹(公钥)}")
    print(f"{'='*60}\n")

    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=2, border=1)
        qr.add_data(二维码数据)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        print(二维码数据)

    if args.out:
        path = _生成二维码图片(二维码数据, Path(args.out))
        print(f"\n🟢 二维码图片已保存: {path}")

    if args.text_out:
        Path(args.text_out).write_text(二维码数据, encoding="utf-8")
        print(f"🟢 二维码文本已保存: {args.text_out}")

    return 二维码数据


def _读取文本(path: Optional[str]) -> str:
    if path in (None, "-"):
        print("🟡 等待从标准输入读取公钥数据（粘贴后按 Ctrl+D / Ctrl+Z）:")
        return sys.stdin.read().strip()
    return Path(path).read_text(encoding="utf-8").strip()


def cmd_pair_scan(args):
    """
    作为配对响应方：读取对端公钥，生成本机临时密钥对，
    计算共享密钥并派生 SM4 会话密钥。
    """
    对端公钥数据 = _读取文本(args.input)
    协商 = _静默实例化(密钥协商器.密钥协商器)
    本机公钥 = 协商.生成密钥对()

    对端公钥 = 协商.二维码数据转公钥(对端公钥数据)
    共享密钥 = 协商.计算共享密钥(对端公钥)
    会话密钥 = 协商.派生会话密钥(共享密钥)

    print(f"\n{'='*60}")
    print("  龍魂密钥协商完成")
    print(f"  对端公钥指纹: {_指纹(对端公钥)}")
    print(f"  本机公钥指纹: {_指纹(本机公钥)}")
    print(f"  会话密钥指纹: {_指纹(会话密钥)}")
    print(f"{'='*60}\n")

    if args.client_out:
        本机二维码 = 协商.公钥转二维码数据(本机公钥)
        Path(args.client_out).write_text(本机二维码, encoding="utf-8")
        print(f"🟢 本机公钥已保存，供对端扫描: {args.client_out}")

    if args.key_out:
        # 会话密钥敏感，Base64 编码后保存；用户需安全传递或仅存内存
        Path(args.key_out).write_text(base64.b64encode(会话密钥).decode(), encoding="utf-8")
        print(f"🟢 会话密钥已保存: {args.key_out}")

    return 会话密钥


# =================== 在线同步协议 ===================

class _最小设备信息:
    def __init__(self, ip: str, 平台: str = "unknown", 名: str = "peer"):
        self.IP地址 = ip
        self.平台 = 平台
        self.设备名 = 名


def _构建信封(信封管理器, 数据: Dict, 源: str, 目标: str, 向量: Dict) -> Dict:
    return 信封管理器.构建信封(
        数据=数据,
        源设备=源,
        目标设备=目标,
        版本向量=向量,
    )


def _发送原始(sock: socket.socket, 数据: Dict):
    字节 = json.dumps(数据, ensure_ascii=False).encode("utf-8")
    前缀 = struct.pack(">I", len(字节))
    sock.sendall(前缀 + 字节)


def _接收原始(sock: socket.socket, timeout: float = 60.0) -> Optional[Dict]:
    sock.settimeout(timeout)
    try:
        长度数据 = sock.recv(4)
        if not 长度数据 or len(长度数据) < 4:
            return None
        长度 = struct.unpack(">I", 长度数据)[0]
        数据块 = b""
        while len(数据块) < 长度:
            片段 = sock.recv(min(8192, 长度 - len(数据块)))
            if not 片段:
                return None
            数据块 += 片段
        return json.loads(数据块.decode("utf-8"))
    except socket.timeout:
        return None


def _在线协商服务端(sock: socket.socket) -> bytes:
    """服务端：发送公钥，接收客户端公钥，返回 SM4 会话密钥。"""
    协商 = _静默实例化(密钥协商器.密钥协商器)
    服务端公钥 = 协商.生成密钥对()
    公钥数据 = 协商.公钥转二维码数据(服务端公钥)
    _发送原始(sock, {"type": "pubkey", "pubkey": 公钥数据, "role": "server"})

    响应 = _接收原始(sock, timeout=30.0)
    if not 响应 or 响应.get("type") != "pubkey":
        raise RuntimeError("未收到客户端公钥")
    客户端公钥 = 协商.二维码数据转公钥(响应["pubkey"])
    共享密钥 = 协商.计算共享密钥(客户端公钥)
    会话密钥 = 协商.派生会话密钥(共享密钥)
    logging.info("🟢 [服务端] 在线密钥协商完成，指纹: %s", _指纹(会话密钥))
    return 会话密钥


def _在线协商客户端(sock: socket.socket) -> bytes:
    """客户端：接收服务端公钥，发送本机公钥，返回 SM4 会话密钥。"""
    响应 = _接收原始(sock, timeout=30.0)
    if not 响应 or 响应.get("type") != "pubkey":
        raise RuntimeError("未收到服务端公钥")

    协商 = _静默实例化(密钥协商器.密钥协商器)
    客户端公钥 = 协商.生成密钥对()
    公钥数据 = 协商.公钥转二维码数据(客户端公钥)
    _发送原始(sock, {"type": "pubkey", "pubkey": 公钥数据, "role": "client"})

    服务端公钥 = 协商.二维码数据转公钥(响应["pubkey"])
    共享密钥 = 协商.计算共享密钥(服务端公钥)
    会话密钥 = 协商.派生会话密钥(共享密钥)
    logging.info("🟢 [客户端] 在线密钥协商完成，指纹: %s", _指纹(会话密钥))
    return 会话密钥


def _验证HTTP请求头(handler) -> bool:
    """验证请求是否携带有效的龍魂确认码或DNA头（支持emoji在HTTP头中的编码差异）。"""
    confirm = handler.headers.get("X-LongHun-Confirm", "")
    dna = handler.headers.get("X-Dragon-DNA", "")
    # 宽松验证：确认码包含核心令牌 LK9X-772Z，或DNA头以 #龍芯 开头
    valid = "LK9X-772Z" in confirm or dna.startswith(DNA_PREFIX)
    if not valid:
        logging.warning("🟡 HTTP 请求缺少有效认证头")
    return valid


def _启动HTTP服务(port: int, 状态: Dict):
    """启动 HTTP 服务：健康检查 + 记忆同步 + 文件同步。"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    class HTTPHandler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _send_json(self, data: Dict, code: int = 200):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_bytes(self, data: bytes, content_type: str = "application/octet-stream", code: int = 200):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _read_body(self) -> Dict:
            try:
                length = int(self.headers.get("Content-Length", 0))
                if length == 0:
                    return {}
                raw = self.rfile.read(length)
                return json.loads(raw.decode("utf-8"))
            except Exception:
                return {}

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Dragon-DNA, X-LongHun-Confirm")
            self.end_headers()

        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            client_ip = self.client_address[0]
            if not _是本地地址(client_ip):
                self._send_json({"error": "external_ip_blocked", "ip": client_ip}, 403)
                return

            if path == "/health":
                self._send_json(状态)
                return

            if path == "/sync/memory":
                if not _验证HTTP请求头(self):
                    self._send_json({"error": "unauthorized", "hint": "缺少 X-LongHun-Confirm 或 X-Dragon-DNA"}, 401)
                    return
                if MEMORY_PATH.exists():
                    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
                    self._send_json({
                        "status": "ok",
                        "resource": "memory",
                        "dna": DNA,
                        "confirm": CONFIRM,
                        "payload": payload,
                        "timestamp": _now_iso(),
                    })
                else:
                    self._send_json({"error": "memory_not_found", "path": str(MEMORY_PATH)}, 404)
                return

            if path == "/sync/file":
                if not _验证HTTP请求头(self):
                    self._send_json({"error": "unauthorized", "hint": "缺少 X-LongHun-Confirm 或 X-Dragon-DNA"}, 401)
                    return
                remote_path = query.get("path", [""])[0]
                if not remote_path:
                    self._send_json({"error": "missing_path"}, 400)
                    return
                target = Path(remote_path).expanduser().resolve()
                home = Path.home().resolve()
                try:
                    target.relative_to(home)
                    if target.exists() and target.is_file():
                        self._send_json({
                            "status": "ok",
                            "resource": "file",
                            "path": remote_path,
                            "content": base64.b64encode(target.read_bytes()).decode(),
                            "mtime": target.stat().st_mtime,
                            "dna": DNA,
                        })
                    else:
                        self._send_json({"error": "file_not_found", "path": remote_path}, 404)
                except ValueError:
                    self._send_json({"error": "path_not_allowed", "path": remote_path}, 403)
                return

            self._send_json({"error": "not_found", "path": path}, 404)

        def do_POST(self):
            parsed = urlparse(self.path)
            path = parsed.path

            client_ip = self.client_address[0]
            if not _是本地地址(client_ip):
                self._send_json({"error": "external_ip_blocked", "ip": client_ip}, 403)
                return

            if path == "/sync/file":
                if not _验证HTTP请求头(self):
                    self._send_json({"error": "unauthorized"}, 401)
                    return
                body = self._read_body()
                remote_path = body.get("path", "")
                content_b64 = body.get("content", "")
                if not remote_path or not content_b64:
                    self._send_json({"error": "missing_path_or_content"}, 400)
                    return
                target = Path(remote_path).expanduser().resolve()
                home = Path.home().resolve()
                try:
                    target.relative_to(home)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(base64.b64decode(content_b64))
                    self._send_json({
                        "status": "ok",
                        "resource": "file",
                        "path": remote_path,
                        "size": target.stat().st_size,
                        "dna": DNA,
                    })
                except ValueError:
                    self._send_json({"error": "path_not_allowed", "path": remote_path}, 403)
                except Exception as e:
                    self._send_json({"error": "write_failed", "detail": str(e)}, 500)
                return

            self._send_json({"error": "not_found", "path": path}, 404)

    def run():
        try:
            server = HTTPServer(("0.0.0.0", port), HTTPHandler)
            server.serve_forever()
        except Exception as e:
            logging.warning("🟡 HTTP 服务启动失败: %s", e)

    t = threading.Thread(target=run, daemon=True, name="longhun-http")
    t.start()


def cmd_serve(args):
    """启动同步服务端：接收记忆/文件拉取请求，支持在线ECDH。"""
    port = _获取可用端口(args.port)
    会话记录: Dict[str, Dict[str, Any]] = {}
    健康状态 = {
        "service": "longhun-sync-server",
        "dna": DNA,
        "port": port,
        "status": "running",
        "sessions": 0,
        "start_time": _now_iso(),
    }

    if port != args.port:
        logging.warning("🟡 端口从 %d 自动切换到 %d", args.port, port)

    # 启动 HTTP 服务（端口 +1）：健康检查 + /sync/memory + /sync/file
    http_port = _获取可用端口(port + 1)
    _启动HTTP服务(http_port, 健康状态)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)

    print(f"\n{'='*70}")
    print("  🐉 龍魂跨设备同步服务端 v2.0")
    print(f"  TCP同步端口: {port}")
    print(f"  HTTP服务端口: {http_port}")
    print(f"  记忆文件: {MEMORY_PATH}")
    print(f"  DNA: {DNA}")
    print(f"{'='*70}\n")
    print("按 Ctrl+C 停止\n")

    try:
        while True:
            conn, addr = sock.accept()
            client_ip = addr[0]
            if not _是本地地址(client_ip):
                logging.error("🔴 拒绝非本地连接: %s", client_ip)
                conn.close()
                continue

            t = threading.Thread(
                target=_处理同步连接,
                args=(conn, client_ip, 会话记录, 健康状态, args),
                daemon=True,
            )
            t.start()
    except KeyboardInterrupt:
        print("\n🛑 同步服务端已停止")
    finally:
        sock.close()


def _处理同步连接(conn, client_ip, 会话记录, 健康状态, args):
    try:
        conn.settimeout(args.timeout)
        会话密钥 = _在线协商服务端(conn)
        会话指纹 = _指纹(会话密钥)
        会话记录[会话指纹] = {"ip": client_ip, "created": time.time()}
        健康状态["sessions"] = len(会话记录)

        # 清理过期会话
        now = time.time()
        for k in list(会话记录.keys()):
            if now - 会话记录[k].get("created", 0) > SESSION_TTL_SECONDS:
                del 会话记录[k]

        信封 = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
        信封.设置会话密钥(会话密钥)

        while True:
            加密请求 = _接收原始(conn, timeout=args.timeout)
            if not 加密请求:
                break

            try:
                明文, 元数据 = 信封.解密信封(加密请求)
            except Exception as e:
                logging.error("🔴 解密失败: %s", e)
                响应 = _构建信封(信封, {"error": "decrypt_failed"}, "server", client_ip, {"server": 1})
                _发送原始(conn, 响应)
                continue

            请求类型 = 明文.get("type")
            资源 = 明文.get("resource")
            logging.info("🟢 [服务端] 收到请求: type=%s resource=%s", 请求类型, 资源)

            if 请求类型 == "sync_request" and 资源 == "memory":
                if MEMORY_PATH.exists():
                    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
                else:
                    payload = {"error": "memory_not_found", "path": str(MEMORY_PATH)}
                响应数据 = {
                    "type": "sync_response",
                    "resource": "memory",
                    "payload": payload,
                    "timestamp": _now_iso(),
                }

            elif 请求类型 == "sync_request" and 资源 == "file":
                remote_path = 明文.get("path", "")
                target = Path(remote_path).expanduser().resolve()
                # 限制访问范围：只允许用户主目录下文件
                home = Path.home().resolve()
                try:
                    target.relative_to(home)
                    if target.exists() and target.is_file():
                        payload = {
                            "path": remote_path,
                            "content": base64.b64encode(target.read_bytes()).decode(),
                            "mtime": target.stat().st_mtime,
                        }
                    else:
                        payload = {"error": "file_not_found", "path": remote_path}
                except ValueError:
                    payload = {"error": "path_not_allowed", "path": remote_path}
                响应数据 = {
                    "type": "sync_response",
                    "resource": "file",
                    "payload": payload,
                    "timestamp": _now_iso(),
                }

            elif 请求类型 == "ping":
                响应数据 = {"type": "pong", "timestamp": _now_iso()}

            else:
                响应数据 = {"error": "unknown_request", "type": 请求类型, "resource": 资源}

            响应信封 = _构建信封(信封, 响应数据, "server", client_ip, {"server": 1})
            _发送原始(conn, 响应信封)

    except Exception as e:
        logging.error("🔴 [服务端] 连接处理异常: %s", e)
    finally:
        conn.close()


def cmd_sync_memory(args):
    """客户端：连接服务端并拉取记忆摘要。"""
    if not _是本地地址(args.host):
        logging.error("🔴 只允许连接本地网络地址: %s", args.host)
        sys.exit(1)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("  🐉 龍魂跨设备记忆同步（客户端）")
    print(f"  目标: {args.host}:{args.port}")
    print(f"  输出: {output}")
    print(f"{'='*60}\n")

    for attempt in range(1, args.retry + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(args.timeout)
            sock.connect((args.host, args.port))
            会话密钥 = _在线协商客户端(sock)

            信封 = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
            信封.设置会话密钥(会话密钥)

            请求数据 = {"type": "sync_request", "resource": "memory", "timestamp": _now_iso()}
            请求信封 = _构建信封(信封, 请求数据, "client", args.host, {"client": 1})
            _发送原始(sock, 请求信封)

            响应信封 = _接收原始(sock, timeout=args.timeout)
            if not 响应信封:
                raise RuntimeError("未收到服务端响应")

            响应明文, _ = 信封.解密信封(响应信封)
            if "error" in 响应明文.get("payload", {}):
                raise RuntimeError(响应明文["payload"]["error"])

            payload = 响应明文["payload"]
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

            print(f"🟢 记忆同步成功: {output}")
            print(f"   会话密钥指纹: {_指纹(会话密钥)}")
            print(f"   记忆条目数: {len(payload) if isinstance(payload, dict) else 'N/A'}")
            return

        except Exception as e:
            logging.error("🔴 同步失败 (%d/%d): %s", attempt, args.retry, e)
            time.sleep(2)
        finally:
            try:
                sock.close()
            except:
                pass

    sys.exit(1)


def cmd_sync_file(args):
    """客户端：连接服务端并拉取指定文件。"""
    if not _是本地地址(args.host):
        logging.error("🔴 只允许连接本地网络地址: %s", args.host)
        sys.exit(1)

    output = Path(args.local)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("  🐉 龍魂跨设备文件同步（客户端）")
    print(f"  目标: {args.host}:{args.port}")
    print(f"  远程文件: {args.remote}")
    print(f"  本地保存: {output}")
    print(f"{'='*60}\n")

    for attempt in range(1, args.retry + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(args.timeout)
            sock.connect((args.host, args.port))
            会话密钥 = _在线协商客户端(sock)

            信封 = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
            信封.设置会话密钥(会话密钥)

            请求数据 = {
                "type": "sync_request",
                "resource": "file",
                "path": args.remote,
                "timestamp": _now_iso(),
            }
            请求信封 = _构建信封(信封, 请求数据, "client", args.host, {"client": 1})
            _发送原始(sock, 请求信封)

            响应信封 = _接收原始(sock, timeout=args.timeout)
            if not 响应信封:
                raise RuntimeError("未收到服务端响应")

            响应明文, _ = 信封.解密信封(响应信封)
            payload = 响应明文.get("payload", {})
            if "error" in payload:
                raise RuntimeError(payload["error"])

            output.write_bytes(base64.b64decode(payload["content"]))
            print(f"🟢 文件同步成功: {output} ({output.stat().st_size} bytes)")
            return

        except Exception as e:
            logging.error("🔴 文件同步失败 (%d/%d): %s", attempt, args.retry, e)
            time.sleep(2)
        finally:
            try:
                sock.close()
            except:
                pass

    sys.exit(1)


def cmd_demo(args):
    """单机 loopback 演示：鸿蒙(server) <-> iOS(client)。"""
    print(f"\n{'='*70}")
    print("  龍魂跨平台同步 · 端到端加密 loopback 演示")
    print(f"  DNA: {DNA}")
    print(f"{'='*70}\n")

    结果锁 = threading.Lock()
    演示结果: Dict[str, any] = {"server_received": None, "ok": False}
    port = _获取可用端口(args.port)

    # 共享公钥数据的同步原语
    qrA_event = threading.Event()
    qrB_event = threading.Event()
    qrA_data: Dict[str, str] = {}
    qrB_data: Dict[str, str] = {}

    def 服务端():
        # 1. 密钥协商
        协商A = _静默实例化(密钥协商器.密钥协商器)
        公钥A = 协商A.生成密钥对()
        qrA_data["text"] = 协商A.公钥转二维码数据(公钥A)
        print(f"[鸿蒙服务端] ECDH 公钥指纹: {_指纹(公钥A)}")
        qrA_event.set()

        # 等待客户端公钥
        if not qrB_event.wait(timeout=10):
            raise TimeoutError("服务端等待客户端公钥超时")
        公钥B = 协商A.二维码数据转公钥(qrB_data["text"])
        共享A = 协商A.计算共享密钥(公钥B)
        会话A = 协商A.派生会话密钥(共享A)
        print(f"[鸿蒙服务端] 会话密钥指纹: {_指纹(会话A)}")

        # 2. 准备信封解密器
        信封A = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
        信封A.设置会话密钥(会话A)

        # 3. 启动 TCP 服务
        传输A = _静默实例化(
            传输管理器.传输管理器,
            None, None,
            首选传输=传输管理器.传输类型.TCP_LAN,
            端口=port,
        )
        print(f"[鸿蒙服务端] 在 0.0.0.0:{port} 等待连接...")
        if not 传输A._作为服务端启动TCP():
            raise RuntimeError("服务端启动失败")
        传输A.状态 = 传输管理器.传输状态.已连接
        传输A.当前传输 = 传输管理器.传输类型.TCP_LAN
        print("[鸿蒙服务端] 客户端已连接")

        # 4. 接收并解密
        收到数据 = 传输A.接收(timeout=30)
        if not 收到数据:
            raise RuntimeError("服务端未收到数据")
        明文, 元数据 = 信封A.解密信封(收到数据)
        print(f"\n[鸿蒙服务端] 解密成功，来源: {元数据.get('源设备')}")
        print(f"[鸿蒙服务端] DNA: {元数据.get('DNA')}")
        print(f"[鸿蒙服务端] 版本向量: {元数据.get('版本向量')}")
        print(f"[鸿蒙服务端] 明文数据:\n{json.dumps(明文, ensure_ascii=False, indent=2)}")

        # 5. 简单冲突解决：把本地一条旧数据与收到的远程数据合并
        本地旧数据 = {"todo_list": ["买菜", "浇水"], "last_sync": 0}
        解决器 = _静默实例化(冲突解决器.冲突解决器, 冲突解决器.冲突策略.字段级合并)
        结果 = 解决器.解决(本地旧数据, 明文)
        print(f"\n[鸿蒙服务端] 冲突解决结果: {结果.类型.value}")
        print(json.dumps(结果.结果数据, ensure_ascii=False, indent=2))

        # 发送确认
        传输A.发送确认(True)
        传输A.断开()
        with 结果锁:
            演示结果["server_received"] = 明文
            演示结果["merged"] = 结果.结果数据
            演示结果["ok"] = True

    def 客户端():
        # 1. 等待服务端公钥
        if not qrA_event.wait(timeout=10):
            raise TimeoutError("客户端等待服务端公钥超时")

        # 2. 密钥协商
        协商B = _静默实例化(密钥协商器.密钥协商器)
        公钥B = 协商B.生成密钥对()
        qrB_data["text"] = 协商B.公钥转二维码数据(公钥B)
        print(f"[iOS客户端] ECDH 公钥指纹: {_指纹(公钥B)}")
        qrB_event.set()

        公钥A = 协商B.二维码数据转公钥(qrA_data["text"])
        共享B = 协商B.计算共享密钥(公钥A)
        会话B = 协商B.派生会话密钥(共享B)
        print(f"[iOS客户端] 会话密钥指纹: {_指纹(会话B)}")

        # 3. 准备信封
        信封B = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
        信封B.设置会话密钥(会话B)

        # 4. 连接服务端（本地回环，模拟同 WiFi 局域网）
        class _FakeDevice:
            def __init__(self, ip):
                self.IP地址 = ip
        本机设备 = _FakeDevice("127.0.0.1")
        对端设备 = _FakeDevice("127.0.0.1")
        传输B = _静默实例化(
            传输管理器.传输管理器,
            本机设备, 对端设备,
            首选传输=传输管理器.传输类型.TCP_LAN,
            端口=port,
        )
        print("[iOS客户端] 连接 127.0.0.1...")
        if not 传输B.连接():
            raise RuntimeError("客户端连接失败")

        # 5. 版本向量递增并构建加密信封
        时钟B = _静默实例化(版本向量时钟.版本向量时钟, "harmonyos", "ios")
        时钟B.递增("ios")
        版本向量 = 时钟B.获取向量()

        业务数据 = {
            "todo_list": ["买菜", "写代码", "运动"],
            "note": "这是 iOS 端创建的本地优先笔记，绝不出境。",
            "level": "internal",
        }
        信封数据 = 信封B.构建信封(
            数据=业务数据,
            源设备="ios|uid9622-iphone-001",
            目标设备="harmonyos|uid9622-harmony-001",
            版本向量=版本向量,
        )

        # 6. 发送
        字节数 = 传输B.发送(信封数据)
        print(f"[iOS客户端] 已发送加密信封: {字节数} bytes")

        # 7. 等待确认
        if 传输B.等待确认(timeout=30):
            print("[iOS客户端] 收到服务端确认 🟢")
        else:
            print("[iOS客户端] 未收到确认 🟡")
        传输B.断开()

    # 启动双线程
    t_server = threading.Thread(target=服务端, name="harmonyos-server", daemon=True)
    t_client = threading.Thread(target=客户端, name="ios-client", daemon=True)
    t_server.start()
    time.sleep(0.2)  # 让服务端先监听
    t_client.start()
    t_server.join(timeout=60)
    t_client.join(timeout=60)

    print(f"\n{'='*70}")
    if 演示结果["ok"]:
        print("  🟢 演示成功：端到端加密 + 本地直连 + 冲突解决 全部通过")
    else:
        print("  🔴 演示失败")
    print(f"{'='*70}\n")
    return 演示结果["ok"]


def main():
    parser = argparse.ArgumentParser(
        description="龍魂跨平台同步工作流 v2.0 · Mac ↔ 鸿蒙记忆互通",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--verbose", action="store_true", help="打印 DEBUG 级日志")
    sub = parser.add_subparsers(dest="command", required=True)

    p_disc = sub.add_parser("discover", help="mDNS 发现局域网龍魂节点")
    p_disc.add_argument("--timeout", type=float, default=5.0, help="发现等待秒数")

    p_adv = sub.add_parser("advertise", help="发布本机龍魂同步服务")
    p_adv.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_adv.add_argument("--name", default=None, help="mDNS 服务名")
    p_adv.add_argument("--platform", default="macos", help="平台标识")
    p_adv.add_argument("--role", default="server", help="角色: server/client/peer")
    p_adv.add_argument("--pubkey", default=None, help="ECDH 公钥文件路径（可选）")
    p_adv.add_argument("--timeout", type=float, default=3600.0, help="保持发布秒数")

    p_qr = sub.add_parser("pair-qr", help="生成 ECDH 公钥二维码")
    p_qr.add_argument("--out", default=None, help="二维码图片保存路径")
    p_qr.add_argument("--text-out", default=None, help="二维码文本保存路径")

    p_scan = sub.add_parser("pair-scan", help="读取对端公钥并完成密钥协商")
    p_scan.add_argument("--input", "-i", required=True, help="对端公钥文件路径（或 - 表示标准输入）")
    p_scan.add_argument("--client-out", default=None, help="保存本机公钥供对端扫描")
    p_scan.add_argument("--key-out", default=None, help="保存会话密钥（Base64，注意保护）")

    p_serve = sub.add_parser("serve", help="启动同步服务端（在线ECDH + 记忆/文件同步）")
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT, help="TCP同步端口")
    p_serve.add_argument("--timeout", type=int, default=30, help="单次请求超时秒数")

    p_sync_mem = sub.add_parser("sync-memory", help="从服务端拉取记忆摘要")
    p_sync_mem.add_argument("--host", required=True, help="服务端 IP")
    p_sync_mem.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_sync_mem.add_argument("--output", "-o", default=str(Path.home() / ".longhun_memory" / "latest_digest.json"))
    p_sync_mem.add_argument("--timeout", type=int, default=30)
    p_sync_mem.add_argument("--retry", type=int, default=3)

    p_sync_file = sub.add_parser("sync-file", help="从服务端拉取任意文件")
    p_sync_file.add_argument("--host", required=True, help="服务端 IP")
    p_sync_file.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_sync_file.add_argument("--remote", required=True, help="服务端文件路径")
    p_sync_file.add_argument("--local", required=True, help="本地保存路径")
    p_sync_file.add_argument("--timeout", type=int, default=30)
    p_sync_file.add_argument("--retry", type=int, default=3)

    p_demo = sub.add_parser("demo", help="单机 loopback 端到端加密同步演示")
    p_demo.add_argument("--port", type=int, default=DEFAULT_PORT)

    args = parser.parse_args()
    _配置日志(args.verbose)

    if args.command == "discover":
        cmd_discover(args)
    elif args.command == "advertise":
        cmd_advertise(args)
    elif args.command == "pair-qr":
        cmd_pair_qr(args)
    elif args.command == "pair-scan":
        cmd_pair_scan(args)
    elif args.command == "serve":
        cmd_serve(args)
    elif args.command == "sync-memory":
        cmd_sync_memory(args)
    elif args.command == "sync-file":
        cmd_sync_file(args)
    elif args.command == "demo":
        ok = cmd_demo(args)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
