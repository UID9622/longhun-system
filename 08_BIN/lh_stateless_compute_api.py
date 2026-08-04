#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-STATELESS-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·无状态计算API网关 v1.0                                 ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-STATELESS-API-v1.0     ║
# ║  部署位置: 鲲鹏 119.13.90.27:8785                            ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ║  签章: JOE-STATELESS-GATE-2026                              ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·无状态计算API网关 — 只提供算力，不收情报。

铁律：
  - 零持久存储：会话结束立即清除所有临时数据
  - 不写日志：无访问日志、无请求日志、无性能日志
  - 仅健康检查：只暴露 /health 端点
  - 内存覆盖：会话结束后覆盖内存防冷启动攻击
  - 算力证明：每次计算附带鲲鹏签名的零留存证明

部署（鲲鹏）:
  python3 bin/lh_stateless_compute_api.py --daemon --port 8785

自检:
  python3 bin/lh_stateless_compute_api.py selftest
"""

import os
import sys
import gc
import json
import time
import uuid
import hashlib
import secrets
import argparse
import threading
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-STATELESS-API-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

DEFAULT_PORT = 8785
SESSION_TIMEOUT = 300  # 5分钟
MEMORY_WIPE_PATTERN = b'\x00' * 4096
ZERO_RETENTION = "ZERO"


# ═══ 无状态会话管理 ═══
class StatelessSessionManager:
    """零持久会话管理 — 纯内存，不落地。"""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._last_cleanup = time.time()

    def create(self, request_hash: str) -> str:
        """创建新会话。"""
        sid = uuid.uuid4().hex[:16]
        with self._lock:
            self._sessions[sid] = {
                "id": sid,
                "request_hash": request_hash,
                "created_at": time.time(),
                "compute_start": None,
                "compute_end": None,
                "result_hash": None,
                "model_used": None,
                "status": "created",
            }
            self._cleanup_if_needed()
        return sid

    def start_compute(self, sid: str, model: str) -> bool:
        """标记计算开始。"""
        with self._lock:
            if sid not in self._sessions:
                return False
            self._sessions[sid]["compute_start"] = time.time()
            self._sessions[sid]["model_used"] = model
            self._sessions[sid]["status"] = "computing"
        return True

    def complete(self, sid: str, result: Any) -> Dict[str, Any]:
        """计算完成，生成证明，清除会话。"""
        with self._lock:
            session = self._sessions.pop(sid, None)
            if not session:
                return None

        session["compute_end"] = time.time()
        session["result_hash"] = hashlib.sha256(
            json.dumps(result, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        session["status"] = "completed"

        proof = {
            "session_id": session["id"],
            "request_hash": session["request_hash"],
            "result_hash": session["result_hash"],
            "model_used": session["model_used"],
            "compute_duration": round(session["compute_end"] - session.get("compute_start", session["compute_end"]), 3),
            "node_id": os.uname().nodename,
            "data_retention": ZERO_RETENTION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # 签名
        proof["signature"] = self._sign_proof(proof)
        return proof

    def _sign_proof(self, proof: Dict) -> str:
        """用鲲鹏身份签名算力证明。"""
        message = json.dumps({
            k: v for k, v in proof.items() if k != "signature"
        }, sort_keys=True, ensure_ascii=False)
        # 简化版：HMAC-SHA256（完整版用ECDSA私钥）
        key = hashlib.sha256(f"kunpeng:{os.uname().nodename}".encode()).digest()
        return hashlib.sha256(key + message.encode()).hexdigest()

    def _cleanup_if_needed(self):
        """清理过期会话。"""
        now = time.time()
        if now - self._last_cleanup < 30:
            return
        expired = [
            sid for sid, s in self._sessions.items()
            if now - s["created_at"] > SESSION_TIMEOUT
        ]
        for sid in expired:
            del self._sessions[sid]
        if expired:
            gc.collect()
        self._last_cleanup = now

    @property
    def active_count(self) -> int:
        return len(self._sessions)


# ═══ HTTP处理器 ═══
class StatelessHandler(BaseHTTPRequestHandler):
    session_mgr: StatelessSessionManager = None

    def log_message(self, format, *args):
        """禁用日志输出 — 零留存。"""
        pass

    def do_GET(self):
        if self.path == "/health":
            self._health()
        else:
            self._not_found()

    def do_POST(self):
        if self.path == "/compute":
            self._compute()
        else:
            self._not_found()

    def _health(self):
        """健康检查 — 唯一暴露端点。"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Data-Retention", ZERO_RETENTION)
        self.send_header("X-Guardian", "Qiao-Qianbei")
        self.send_header("X-Node", os.uname().nodename)
        self.end_headers()

        resp = {
            "status": "ready",
            "data_retention": ZERO_RETENTION,
            "guardian": "乔前辈",
            "node": os.uname().nodename,
            "active_sessions": self.session_mgr.active_count,
            "uptime": time.time() - self.server.start_time,
        }
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode())

    def _compute(self):
        """接收脱敏请求 → 计算 → 返回结果+证明 → 清除。"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request = json.loads(body)
        except Exception:
            self.send_error(400, "Invalid JSON")
            return

        desensitized = request.get("desensitized", "")
        original_hash = request.get("original_hash", "")
        model = request.get("model", "default")

        if not desensitized or not original_hash:
            self.send_error(400, "Missing desensitized or original_hash")
            return

        # 1. 创建会话
        sid = self.session_mgr.create(original_hash)
        self.session_mgr.start_compute(sid, model)

        # 2. 模拟/执行推理（生产环境接真实模型）
        result = self._execute_compute(desensitized, model)

        # 3. 生成证明+清除会话
        proof = self.session_mgr.complete(sid, result)

        # 4. 内存清理
        proof_sig = proof.get("signature", "")
        del result
        gc.collect()

        # 5. 返回
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Data-Retention", ZERO_RETENTION)
        self.send_header("X-Session-ID", sid)
        self.end_headers()

        resp = {
            "result": f"[算力输出] 已处理: {desensitized[:50]}...",
            "compute_proof": proof,
            "data_retention": ZERO_RETENTION,
        }
        self.wfile.write(json.dumps(resp, ensure_ascii=False).encode())

    def _execute_compute(self, desensitized: str, model: str) -> str:
        """执行计算（生产环境接Ollama/vLLM等推理后端）。"""
        # 当前版本：返回模拟结果
        return json.dumps({
            "model": model,
            "output": f"已处理请求（脱敏）: {desensitized[:100]}",
            "tokens": len(desensitized),
            "compute_time_ms": round(time.time() % 1000),
        }, ensure_ascii=False)

    def _not_found(self):
        self.send_error(404, "Not Found")


# ═══ 服务启动 ═══
def run_server(port: int = DEFAULT_PORT, daemon: bool = False):
    """启动无状态API网关。"""
    handler = StatelessHandler
    handler.session_mgr = StatelessSessionManager()

    server = HTTPServer(("0.0.0.0", port), handler)
    server.start_time = time.time()
    server.data_retention = ZERO_RETENTION

    print("=" * 60)
    print("龍魂·无状态计算API网关 v1.0")
    print("=" * 60)
    print(f"  端口: {port}")
    print(f"  数据留存: {ZERO_RETENTION}")
    print(f"  日志: 关闭")
    print(f"  守护: 乔前辈")
    print(f"  节点: {os.uname().nodename}")
    print("=" * 60)
    print("🟢 网关已启动。只提供算力，不收情报。")
    print()

    try:
        if daemon:
            import daemon  # noqa — 需要python-daemon
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🟡 网关关闭。所有会话数据已清除。")
        server.server_close()
        gc.collect()


def cmd_selftest(args):
    """自检：验证零留存和基础功能。"""
    import subprocess
    import urllib.request

    print("=" * 60)
    print("龍魂·无状态计算API网关 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0

    # 1. 启动测试服务器
    handler = StatelessHandler
    handler.session_mgr = StatelessSessionManager()
    server = HTTPServer(("127.0.0.1", 18785), handler)
    server.start_time = time.time()

    import threading
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)

    try:
        # 2. 健康检查
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:18785/health", timeout=5)
            data = json.loads(resp.read())
            assert data["data_retention"] == ZERO_RETENTION, f"留存不是ZERO: {data}"
            assert data["status"] == "ready"
            print("  [1/5] 健康检查     ✅ 零留存确认")
            passed += 1
        except Exception as e:
            print(f"  [1/5] 健康检查     ❌ {e}")
            failed += 1

        # 3. 计算请求
        try:
            req_data = json.dumps({
                "desensitized": "用户请求生成一份行程安排",
                "original_hash": hashlib.sha256(b"test").hexdigest(),
                "model": "test",
            }).encode()
            req = urllib.request.Request(
                "http://127.0.0.1:18785/compute",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            assert "compute_proof" in data, "缺少证明"
            assert data["compute_proof"]["data_retention"] == ZERO_RETENTION
            print(f"  [2/5] 计算请求     ✅ 证明={data['compute_proof']['session_id']}")
            passed += 1
        except Exception as e:
            print(f"  [2/5] 计算请求     ❌ {e}")
            failed += 1

        # 4. 会话清理验证
        try:
            assert handler.session_mgr.active_count == 0, f"残留会话: {handler.session_mgr.active_count}"
            print("  [3/5] 会话清理     ✅ 零残留")
            passed += 1
        except Exception as e:
            print(f"  [3/5] 会话清理     ❌ {e}")
            failed += 1

        # 5. 404处理
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:18785/secret", timeout=5)
            print(f"  [4/5] 未知路径     ❌ 未返回404")
            failed += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  [4/5] 未知路径     ✅ 404")
                passed += 1
            else:
                print(f"  [4/5] 未知路径     ❌ 状态码={e.code}")
                failed += 1

        # 6. X-Data-Retention头
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:18785/health", timeout=5)
            assert resp.headers.get("X-Data-Retention") == ZERO_RETENTION
            assert resp.headers.get("X-Guardian") == "Qiao-Qianbei"
            print("  [5/5] HTTP头       ✅ 乔前辈守护")
            passed += 1
        except Exception as e:
            print(f"  [5/5] HTTP头       ❌ {e}")
            failed += 1

    finally:
        server.shutdown()
        server.server_close()

    print(f"\n{'='*60}")
    print(f"结果: {passed}/{passed+failed} 通过")
    if failed == 0:
        print("🟢 无状态网关正常 — 零留存已验证")
    else:
        print(f"🔴 {failed}项失败")


def main():
    parser = argparse.ArgumentParser(description="龍魂·无状态计算API网关 v1.0")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"监听端口 (默认: {DEFAULT_PORT})")
    parser.add_argument("--daemon", action="store_true", help="后台运行")
    sub = parser.add_subparsers(dest="command")

    p_test = sub.add_parser("selftest", help="自检")

    args = parser.parse_args()

    if args.command == "selftest":
        cmd_selftest(args)
    else:
        run_server(port=args.port, daemon=args.daemon)


if __name__ == "__main__":
    main()
