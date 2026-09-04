#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-CORE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 鲲鹏 MCP Server · 共享协议引擎 v1.0
================================================================
深度绑定龍魂生态的 MCP 服务器核心：JSON-RPC 2.0 over
Streamable HTTP / stdio（MCP 协议版本 2025-03-26），零三方依赖。

设计（M77 零中间层 · P0）:
  - 纯 Python 标准库 · 单文件可跑 · ARM/x86 天然兼容免编译
  - 三个独立 Server（readonly 8763 / audit 8764 / admin 8767·2026-09-04 裁决自 8765 迁入，原 8765 归鲲鹏 longhun-cal）共享本引擎
  - 工具 = 薄路由层 → 委托现有 lh 引擎（生态一致·业务逻辑零复制）
  - 可审计：每请求记录 调用方/工具/结果三色 → ~/.longhun/logs/mcp/
  - 受控：高危 Server 强制 X-Confirm: yes + IP 白名单 + 操作日志

用法:
  python3 lh_mcp_readonly.py --port 8763        # HTTP 模式
  python3 lh_mcp_readonly.py --stdio            # stdio 模式(桌面端 command)
"""

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROTOCOL_VERSION = "2025-03-26"
MCP_JSONRPC = "2.0"
BJ_TZ = timezone(timedelta(hours=8))  # 北京时间 UTC+8

# ── JSON-RPC 错误码 ──
ERR_PARSE = -32700
ERR_INVALID_REQ = -32600
ERR_METHOD_NOT_FOUND = -32601
ERR_INVALID_PARAMS = -32602
ERR_INTERNAL = -32603
ERR_TOOL = -32000
ERR_AUTH = -32001
ERR_CONFIRM = -32002


def now_iso() -> str:
    return datetime.now(BJ_TZ).strftime("%Y-%m-%dT%H:%M:%S%z")


def _log(msg: str, tag: str = "lh-mcp"):
    """stdout 被协议占用 → 全部日志走 stderr"""
    print(f"[{tag}] {now_iso()} {msg}", file=sys.stderr, flush=True)


def _sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()


def _sanitize(value, limit: int = 200_000):
    """递归截断超长文本/字符串（防日志与响应爆内存）"""
    if isinstance(value, str):
        if len(value) <= limit:
            return value
        return value[:limit] + f"…<truncated {len(value) - limit} chars>"
    if isinstance(value, dict):
        return {k: _sanitize(v, limit) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_sanitize(v, limit) for v in value]
    return value


class MCPError(Exception):
    def __init__(self, code: int, message: str, data=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


# ═══════════════════════════════════════════════════════════════
# 龍魂生态解析器（零三方 · 供 readonly 直接读文件）
# ═══════════════════════════════════════════════════════════════

def resolve_root(cfg: dict) -> Path:
    """定位 longhun-system 根：env LH_ROOT > config lh_root > 自动探测"""
    env = os.environ.get("LH_ROOT", "").strip()
    if env:
        return Path(env)
    from_cfg = (cfg.get("lh_root") or "").strip()
    if from_cfg:
        return Path(from_cfg)
    # deploy/longhun-mcp/lh_mcp_core.py → parents[2] = longhun-system/
    auto = Path(__file__).resolve()
    for _ in range(4):
        if (auto / ".codebuddy" / "longhun_neural_net.json").exists():
            return auto
        auto = auto.parent
    return Path(__file__).resolve().parents[2]


def find_topo_files(root: Path) -> list:
    d = root / "docs" / "topology"
    if not d.is_dir():
        return []
    return sorted(f for f in d.iterdir() if f.is_file() and f.name.endswith("_topo.json"))


def load_topo(root: Path, name: str = ""):
    """读指定图谱缓存；空 name → 全部图谱清单"""
    files = find_topo_files(root)
    kw = (name or "").strip()
    if not kw:
        return {"graphs": [{"topo_name": _json_safe(f, "topo_name", f.stem.replace("_topo", "")),
                            "display": _json_safe(f, "display", ""),
                            "last_sync": _json_safe(f, "last_sync", "?")} for f in files],
                "total": len(files)}
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("topo_name") == kw or kw in data.get("topo_name", "") or kw in data.get("display", ""):
            return data
    raise MCPError(ERR_INVALID_PARAMS, f"未找到图谱「{kw}」，可用 get_topo(name='') 查看清单")


def _json_safe(f: Path, key: str, default=""):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data.get(key, default)
    except Exception:
        return default


def topo_root_hash(data: dict) -> str:
    """图谱聚合根哈希：group|name|dna 排序拼接 → SHA-256 前16位（与 lh_topo 一致）"""
    lines = []
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            lines.append(f"{g.get('name','')}|{a.get('name')}|{a.get('dna')}")
    for sg in data.get("subgraphs", []):
        lines.append(f"🗄️ {sg.get('name','')}|{sg.get('name')}|{sg.get('dna')}")
        for a in sg.get("assets", []):
            lines.append(f"🗄️ {sg.get('name','')}·笔记|{a.get('name')}|{a.get('dna')}")
    return hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()[:16].upper()


def read_memorial(root: Path) -> dict:
    """读贡献者铭碑 JSON → 含 root_hash / 贡献者清单"""
    f = root / "07_AUDIT" / "contributor_memorial.json"
    if not f.exists():
        return {"loaded": False, "root_hash": None, "reason": f"{f.name} 不存在(未 build)"}
    data = json.loads(f.read_text(encoding="utf-8"))
    root_hash = (data.get("root_hash") or data.get("merkle_root")
                 or data.get("root") or "")
    return {"loaded": True, "root_hash": root_hash,
            "contributors": len(data.get("contributors") or data.get("leaves") or []),
            "updated": data.get("built_at") or data.get("updated") or "?"}


# ═══════════════════════════════════════════════════════════════
# 引擎委托（工具 = 薄路由 → 现成 lh 引擎，生态一致）
# ═══════════════════════════════════════════════════════════════

def run_engine(root: Path, engine: str, args: list, timeout: int = 60,
               cwd: Path | None = None) -> dict:
    """调用龍魂引擎子进程；只允许白名单引擎（防注入）"""
    allow = {"cnsh.py", "lh_topo.py", "lh_memorial.py", "cnsh_pm.py", "lh_judge.py", "lh.py"}
    if engine not in allow:
        raise MCPError(ERR_TOOL, f"引擎不在白名单: {engine}")
    ep = root / "08_BIN" / engine
    if not ep.exists():
        ep = root / "bin" / engine
    if not ep.exists():
        raise MCPError(ERR_TOOL, f"引擎不存在: {engine}")
    try:
        p = subprocess.run([sys.executable, str(ep), *args],
                           cwd=str(cwd or root), capture_output=True, text=True,
                           timeout=timeout, env=os.environ.copy())
    except subprocess.TimeoutExpired:
        raise MCPError(ERR_TOOL, f"引擎执行超时({timeout}s): {engine} {' '.join(args)}")
    except Exception as exc:
        raise MCPError(ERR_TOOL, f"引擎执行失败: {engine}: {exc}")
    return {"engine": engine, "args": args, "rc": p.returncode,
            "stdout": _sanitize(p.stdout or "", 150_000),
            "stderr": _sanitize(p.stderr or "", 50_000)}


# ═══════════════════════════════════════════════════════════════
# MCP Server 核心
# ═══════════════════════════════════════════════════════════════

class MCPServer:
    """单 Server：注册 tools/resources → 处理 JSON-RPC 消息"""

    def __init__(self, name: str, version: str, cfg: dict):
        self.name = name
        self.version = version
        self.cfg = cfg
        self.tools = {}      # name -> {"schema","handler","confirm"}
        self.resources = {}  # uri -> {"name","desc","handler","mime","prefix"} prefix 支持动态 uri
        self.root = resolve_root(cfg)
        self.log_dir = self._log_dir(cfg)
        self._lock = threading.Lock()

    def _log_dir(self, cfg: dict) -> Path:
        d = cfg.get("log_dir") or "~/.longhun/logs/mcp"
        p = Path(d).expanduser()
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return p

    # ── 注册 ──
    def add_tool(self, name: str, description: str, schema: dict, handler, confirm: bool = False):
        schema.setdefault("type", "object")
        schema.setdefault("properties", {})
        self.tools[name] = {"schema": schema, "handler": handler,
                            "description": description, "confirm": confirm}

    def add_resource(self, uri: str, name: str, description: str, handler, mime: str = "application/json"):
        """uri 形如 resource://topo/<name>：尾部 <name> 可用 * 通配（prefix 匹配）"""
        prefix = None
        if uri.endswith("/*"):
            prefix, uri = uri[:-2], uri[:-2]
        self.resources[uri] = {"name": name, "description": description,
                               "handler": handler, "mime": mime, "prefix": prefix}

    # ── 工具/资源 → 协议条目 ──
    def tool_specs(self) -> list:
        return [{"name": n, "description": t["description"], "inputSchema": t["schema"]}
                for n, t in self.tools.items()]

    def resource_specs(self) -> list:
        out = []
        for uri, r in self.resources.items():
            out.append({"uri": uri + ("/*" if r["prefix"] else ""),
                        "name": r["name"], "description": r["description"],
                        "mimeType": r["mime"]})
        return out

    # ── JSON-RPC 分发 ──
    def handle(self, msg: dict, headers: dict | None = None) -> list:
        """处理一条入站消息 → 0..n 条响应。notification(无 id) 不响应。"""
        headers = headers or {}
        if not isinstance(msg, dict):
            return [self._error(None, ERR_INVALID_REQ, "消息必须是 JSON 对象")]
        method = msg.get("method")
        params = msg.get("params") or {}
        rid = msg.get("id")
        is_notify = "id" not in msg

        try:
            if method == "initialize":
                r = self._initialize(params)
                return [] if is_notify else [self._result(rid, r)]
            if method == "ping":
                return [] if is_notify else [self._result(rid, {})]
            if method in ("notifications/initialized", "initialized"):
                return []
            if method == "tools/list":
                return [self._result(rid, {"tools": self.tool_specs()})]
            if method == "tools/call":
                return [self._call_tool(rid, params, headers)]
            if method == "resources/list":
                return [self._result(rid, {"resources": self.resource_specs()})]
            if method == "resources/read":
                return [self._read_resource(rid, params)]
            if method == "prompts/list":
                return [self._result(rid, {"prompts": []})]
            if method == "completion/complete":
                return [self._result(rid, {"completion": {"values": [], "total": 0}})]
            # 未知方法
            err = self._error(rid, ERR_METHOD_NOT_FOUND, f"未知方法: {method}")
            return [] if is_notify else [err]
        except MCPError as exc:
            return [] if is_notify else [self._error(rid, exc.code, exc.message)]
        except Exception as exc:  # 兜底：永不裸崩
            traceback.print_exc(file=sys.stderr)
            return [] if is_notify else [self._error(rid, ERR_INTERNAL, f"内部错误: {exc}")]

    def _initialize(self, params: dict) -> dict:
        return {"protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False},
                                 "resources": {"subscribe": False, "listChanged": False},
                                 "prompts": {}},
                "serverInfo": {"name": self.name, "version": self.version}}

    def _auth_ok(self, headers: dict) -> bool:
        """认证：config auth.mode ∈ none | token；token 匹配即过"""
        auth = self.cfg.get("auth") or {"mode": "none"}
        mode = auth.get("mode", "none")
        if mode == "none":
            return True
        expect = str(auth.get("token") or "").strip()
        if not expect:
            return True
        got = ""
        for h in ("x-lh-token", "x-api-key"):
            if headers.get(h):
                got = str(headers[h]).strip()
                break
        if not got and headers.get("authorization", "").lower().startswith("bearer "):
            got = headers["authorization"][7:].strip()
        return got == expect or base64.b64encode(expect.encode()).decode() == got

    def _call_tool(self, rid, params: dict, headers: dict) -> dict:
        name = params.get("name", "")
        args = params.get("arguments") or {}
        tool = self.tools.get(name)
        if not tool:
            return self._error(rid, ERR_METHOD_NOT_FOUND, f"工具不存在: {name}")
        if not isinstance(args, dict):
            return self._error(rid, ERR_INVALID_PARAMS, "arguments 必须是对象")
        if not self._auth_ok(headers):
            return self._error(rid, ERR_AUTH, "认证失败: 缺 X-LH-Token / X-API-Key / Bearer")
        # 来源 IP 白名单（admin 层：peer_allowlist 非空才生效）
        # x-peer 由 HTTP 层注入(client_address)；stdio 本地进程无该头 → 进程级已受限，视为本机放行
        peers = self.cfg.get("peer_allowlist") or []
        peer_ip = headers.get("x-peer", "")
        if peers and peer_ip and peer_ip not in peers:
            return self._error(rid, ERR_AUTH,
                               f"来源 IP 不在白名单: {peer_ip}")
        # 高危二次确认（admin 层）：请求头 X-Confirm: yes，或参数 _confirm: "yes"
        if tool["confirm"]:
            h_ok = str(headers.get("x-confirm", "")).strip().lower() == "yes"
            a_ok = args.get("_confirm") == "yes"
            if not (h_ok or a_ok):
                return self._error(rid, ERR_CONFIRM,
                                   "高危操作需请求头 X-Confirm: yes 确认（默认拒绝）")
        # 入参 schema 校验（缺必填 → 拒；多余字段容忍）
        schema = tool["schema"]
        for k in schema.get("required") or []:
            if k not in args:
                return self._error(rid, ERR_INVALID_PARAMS, f"缺必填参数: {k}")
        self._audit_log("tool_call", {"tool": name, "args": _sanitize(args, 2000),
                                      "client": self._peer(headers)})
        started = time.time()
        try:
            result = tool["handler"](args)
        except MCPError as exc:
            self._audit_log("tool_error", {"tool": name, "code": exc.code,
                                           "message": exc.message})
            return self._error(rid, exc.code, exc.message, exc.data)
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            self._audit_log("tool_error", {"tool": name, "message": str(exc)})
            return self._error(rid, ERR_TOOL, f"工具执行失败: {exc}")
        ms = round((time.time() - started) * 1000)
        self._audit_log("tool_ok", {"tool": name, "ms": ms})
        text = json.dumps(result, ensure_ascii=False, default=str)
        text = _sanitize(text, 190_000)
        return self._result(rid, {"content": [{"type": "text", "text": text}],
                                  "isError": False})

    def _read_resource(self, rid, params: dict) -> dict:
        uri = params.get("uri", "")
        if not isinstance(uri, str):
            return self._error(rid, ERR_INVALID_PARAMS, "缺 uri")
        entry = self.resources.get(uri)
        if not entry and uri:
            for k, r in self.resources.items():
                if r["prefix"] and uri.startswith(r["prefix"]):
                    entry = r
                    break
        if not entry:
            return self._error(rid, ERR_METHOD_NOT_FOUND, f"资源不存在: {uri}")
        try:
            data = entry["handler"](uri)
        except MCPError as exc:
            return self._error(rid, exc.code, exc.message)
        except Exception as exc:
            return self._error(rid, ERR_TOOL, f"资源读取失败: {exc}")
        text = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, default=str)
        return self._result(rid, {"contents": [{"uri": uri, "mimeType": entry["mime"],
                                                "text": text}]})

    # ── 响应/日志 ──
    def _result(self, rid, result) -> dict:
        return {"jsonrpc": MCP_JSONRPC, "id": rid, "result": result}

    def _error(self, rid, code: int, message: str, data=None) -> dict:
        e = {"code": code, "message": message}
        if data is not None:
            e["data"] = data
        return {"jsonrpc": MCP_JSONRPC, "id": rid, "error": e}

    def _peer(self, headers: dict) -> str:
        return str(headers.get("x-forwarded-for") or headers.get("user-agent") or "?")

    def _audit_log(self, kind: str, payload: dict):
        """append-only 操作审计 → ~/.longhun/logs/mcp/<name>.jsonl"""
        try:
            with self._lock:
                line = json.dumps({"ts": now_iso(), "server": self.name,
                                   "kind": kind, **payload},
                                  ensure_ascii=False, default=str)
                with open(self.log_dir / f"{self.name}.jsonl", "a", encoding="utf-8") as f:
                    f.write(line + "\n")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
# stdio 传输（桌面端 command 模式）
# ═══════════════════════════════════════════════════════════════

def run_stdio(server: MCPServer):
    """JSON-RPC 2.0 over stdin/stdout（每行一条消息）"""
    _log(f"{server.name} stdio 模式就绪 · 版本 {server.version}")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            resp = {"jsonrpc": MCP_JSONRPC, "id": None,
                    "error": {"code": ERR_PARSE, "message": "JSON 解析失败"}}
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue
        for resp in server.handle(msg):
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


# ═══════════════════════════════════════════════════════════════
# Streamable HTTP 传输（端口模式）
# ═══════════════════════════════════════════════════════════════

def _sse_frame(payload: dict) -> bytes:
    body = json.dumps(payload, ensure_ascii=False)
    return f"event: message\ndata: {body}\n\n".encode("utf-8")


def _http_handler_factory(server: MCPServer, bind: str):
    """构造线程化 HTTP handler（Streamable HTTP）"""

    class _Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = f"LonghunMCP/{server.version}"
        sys_version = ""

        def log_message(self, fmt, *args):
            _log(f"{self.address_string()} {fmt % args}", tag=server.name)

        def _read_body(self) -> str:
            try:
                n = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                n = 0
            if n <= 0 or n > 10_000_000:  # 10MB 上限
                raise MCPError(ERR_INVALID_REQ, "Content-Length 非法或超限")
            return self.rfile.read(n).decode("utf-8", errors="replace")

        def _write_json(self, code: int, payload: dict):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_sse(self, code: int, payload: dict):
            """Accept: text/event-stream → 按 MCP SSE 帧封装"""
            raw = _sse_frame(payload)
            self.send_response(code)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _answer(self, payloads: list):
            """按客户端 Accept 选择 JSON 或 SSE 帧响应"""
            if not payloads:
                # 纯 notification：204 No Content
                self.send_response(204)
                self.end_headers()
                return
            payload = payloads[0] if len(payloads) == 1 else {"jsonrpc": MCP_JSONRPC,
                                                              "result": payloads}
            accept = self.headers.get("Accept", "") or ""
            if "text/event-stream" in accept:
                self._write_sse(200, payload)
            else:
                self._write_json(200, payload)

        # ── GET / ：SSE 下行通道（支持 server→client 消息；本实现无推送时发注释保活）──
        def do_GET(self):
            if self.path in ("/", "/mcp"):
                accept = self.headers.get("Accept", "")
                if "text/event-stream" not in accept:
                    self._write_json(400, {"jsonrpc": MCP_JSONRPC, "id": None,
                                           "error": {"code": ERR_INVALID_REQ,
                                                     "message": "GET / 需 Accept: text/event-stream"}})
                    return
                # 长连接心跳：每 25s 一个注释帧；客户端断开即退（线程由断连自然回收）
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                try:
                    while True:
                        self.wfile.write(b": lh-mcp keepalive\n\n")
                        self.wfile.flush()
                        time.sleep(25)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    pass
                return
            self._write_json(404, {"jsonrpc": MCP_JSONRPC, "id": None,
                                   "error": {"code": ERR_METHOD_NOT_FOUND,
                                             "message": f"路径不存在: {self.path}"}})

        def do_POST(self):
            if self.path not in ("/", "/mcp"):
                self._write_json(404, {"jsonrpc": MCP_JSONRPC, "id": None,
                                       "error": {"code": ERR_METHOD_NOT_FOUND,
                                                 "message": f"路径不存在: {self.path}"}})
                return
            headers = {k.lower(): v for k, v in self.headers.items()}
            headers["x-peer"] = self.client_address[0]
            try:
                raw = self._read_body()
                msg = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                self._write_json(400, {"jsonrpc": MCP_JSONRPC, "id": None,
                                       "error": {"code": ERR_PARSE,
                                                 "message": "请求体不是合法 JSON"}})
                return
            except MCPError as exc:
                self._write_json(400, {"jsonrpc": MCP_JSONRPC, "id": None,
                                       "error": {"code": exc.code,
                                                 "message": exc.message}})
                return
            self._answer(server.handle(msg, headers))

    return _Handler


def run_http(server: MCPServer, host: str, port: int):
    handler = _http_handler_factory(server, host)
    httpd = ThreadingHTTPServer((host, port), handler)
    httpd.daemon_threads = True
    _log(f"{server.name} HTTP 模式就绪 · http://{host}:{port}/mcp · 版本 {server.version}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        _log(f"{server.name} 收到中断，退出")
    finally:
        httpd.server_close()


# ═══════════════════════════════════════════════════════════════
# 通用 CLI 入口（供三个 Server 复用）
# ═══════════════════════════════════════════════════════════════

def build_parser(server_name: str, default_port: int) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog=f"lh-mcp-{server_name}",
                                 description=f"🐉 鲲鹏 MCP Server · {server_name}")
    ap.add_argument("--port", type=int, default=default_port, help=f"监听端口 (默认 {default_port})")
    ap.add_argument("--host", default="127.0.0.1", help="绑定地址 (默认 127.0.0.1)")
    ap.add_argument("--stdio", action="store_true", help="stdio 模式（桌面端 command 用）")
    ap.add_argument("--config", default="", help="mcp-config.json 路径")
    ap.add_argument("--version", action="store_true", help="输出版本")
    return ap


def load_config(default_cfg: dict, config_path: str = "") -> dict:
    """合并 mcp-config.json → 覆盖默认值"""
    cfg = dict(default_cfg)
    candidates = []
    if config_path:
        candidates.append(Path(config_path))
    candidates.append(Path(__file__).resolve().parent / "config" / "mcp-config.json")
    for p in candidates:
        if p.is_file():
            try:
                ext = json.loads(p.read_text(encoding="utf-8"))
                # 支持 {server: {...}} 与平铺两种
                if isinstance(ext, dict):
                    mine = ext.get(cfg.get("server")) or ext
                    if isinstance(mine, dict):
                        cfg.update({k: v for k, v in mine.items() if k != "server"})
                    else:
                        cfg.update(ext)
            except Exception as exc:
                _log(f"配置加载失败 {p}: {exc}")
            break
    return cfg


def run_from_cli(server: MCPServer, server_name: str, default_port: int, default_cfg: dict):
    ap = build_parser(server_name, default_port)
    args = ap.parse_args()
    if args.version:
        print(f"🐉 鲲鹏 MCP Server · {server_name} · {server.version}")
        print(f"DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-{server_name.upper()}-v1.0-UID9622")
        print("归属名: 诸葛鑫 | UID9622 · 龍芯北辰")
        return 0
    cfg = load_config(default_cfg, args.config)
    cfg["host"] = args.host
    cfg["port"] = args.port
    if args.stdio:
        run_stdio(server)
    else:
        run_http(server, args.host, args.port)
    return 0


if __name__ == "__main__":
    print("共享协议引擎 · import 由 lh-mcp-readonly/audit/admin 使用", file=sys.stderr)
